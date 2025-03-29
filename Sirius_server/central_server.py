from fastapi import FastAPI, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import requests

MONGO_URI = "mongodb+srv://Sirius:Pepe123@sirius.ycgl08q.mongodb.net/?retryWrites=true&w=majority&appName=Sirius"
DATABASE_NAME = "drones_system"

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client[DATABASE_NAME]

class StationRegistrationRequest(BaseModel):
    station_name: str
    coverage_area: str

class StationModel(BaseModel):
    station_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    station_name: str
    coverage_area: str
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    station_url: str = "http://0.0.0.0:8100"

class DeployDroneRequest(BaseModel):
    latitude: float
    longitude: float

class DroneStatus(BaseModel):
    drone_id: str
    station_id: str
    battery: float
    video_feed_url: str
    current_latitude: float
    current_longitude: float
    departure_time: datetime
    estimated_arrival: datetime
    flight_time_minutes: float  

class DroneUpdateRequest(BaseModel):
    drone_id: str
    station_id: str
    battery: float
    current_latitude: float
    current_longitude: float

class FlightEndRequest(BaseModel):
    drone_id: str
    station_id: str
    images: List[str]

def process_images_with_gemini(images: List[str]) -> str:
    return "Reporte de vuelo generado por LLM Gemini. (Resumen de imágenes)"

app = FastAPI(title="Servidor Central de Drones")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register_station", response_model=StationModel)
def register_station(reg_request: StationRegistrationRequest):
    new_station = StationModel(
        station_name=reg_request.station_name,
        coverage_area=reg_request.coverage_area
    )
    db["stations"].insert_one(new_station.dict())
    return new_station


@app.post("/deploy_drone")
def deploy_drone(req: DeployDroneRequest):
    station_doc = db["stations"].find_one({})
    if not station_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay estaciones registradas para desplegar drones."
        )

    station_id = station_doc["station_id"]
    station_url = station_doc.get("station_url", "http://0.0.0.0:8100")

    drone_id = str(uuid.uuid4())
    now = datetime.utcnow()
    arrival_est = now + timedelta(minutes=10)

    drone_data = {
        "drone_id": drone_id,
        "station_id": station_id,
        "battery": 100.0,
        "video_feed_url": f"http://fake_video_feed/{drone_id}",
        "current_latitude": req.latitude,
        "current_longitude": req.longitude,
        "departure_time": now,
        "estimated_arrival": arrival_est,
    }

    db["active_drones"].insert_one(drone_data)

    instruct_endpoint = f"{station_url}/instruct_drone"
    try:
        payload = {
            "drone_id": drone_id,
            "latitude": req.latitude,
            "longitude": req.longitude
        }
        resp = requests.post(instruct_endpoint, json=payload, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as e:
        db["active_drones"].delete_one({"drone_id": drone_id})
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo instruir al dron en la estación: {e}"
        )

    return {
        "message": "Dron desplegado correctamente.",
        "drone_id": drone_id,
        "station_id": station_id
    }

@app.post("/force_return")
def force_return_drone(drone_id: str = Body(..., embed=True)):
    drone_doc = db["active_drones"].find_one({"drone_id": drone_id})
    if not drone_doc:
        raise HTTPException(
            status_code=404,
            detail="Dron no encontrado o no se encuentra activo en el servidor central."
        )
    
    station_id = drone_doc["station_id"]
    station_doc = db["stations"].find_one({"station_id": station_id})
    if not station_doc:
        raise HTTPException(
            status_code=404,
            detail="Estación asociada al dron no encontrada."
        )
    station_url = station_doc.get("station_url", "http://0.0.0.0:8100")
    
    try:
        force_return_endpoint = f"{station_url}/force_return"
        payload = {"drone_id": drone_id}
        response = requests.post(force_return_endpoint, json=payload, timeout=5)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al forzar el retorno en la estación: {e}"
        )
    
    return {"message": "Retorno forzado exitosamente para el dron.", "drone_id": drone_id}

@app.get("/active_drones", response_model=List[DroneStatus])
def get_active_drones():
    results = []
    for doc in db["active_drones"].find({}):
        departure_time = doc["departure_time"]
        time_diff = (datetime.utcnow() - departure_time).total_seconds() / 60.0

        drone_status = DroneStatus(
            drone_id=doc["drone_id"],
            station_id=doc["station_id"],
            battery=doc["battery"],
            video_feed_url=doc["video_feed_url"],
            current_latitude=doc["current_latitude"],
            current_longitude=doc["current_longitude"],
            departure_time=departure_time,
            estimated_arrival=doc["estimated_arrival"],
            flight_time_minutes=time_diff
        )
        results.append(drone_status)
    return results


@app.post("/drone_updates")
def update_drone_status(update_req: DroneUpdateRequest):
    drone_doc = db["active_drones"].find_one({"drone_id": update_req.drone_id})
    if not drone_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El dron no está registrado como activo en el servidor central."
        )

    db["active_drones"].update_one(
        {"drone_id": update_req.drone_id},
        {"$set": {
            "battery": update_req.battery,
            "current_latitude": update_req.current_latitude,
            "current_longitude": update_req.current_longitude,
        }}
    )
    return {"message": "Estado del dron actualizado correctamente en servidor central."}


@app.post("/end_flight")
def end_flight(flight_end_req: FlightEndRequest):
    drone_doc = db["active_drones"].find_one({"drone_id": flight_end_req.drone_id})
    if not drone_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El dron no está activo o no existe en el servidor central."
        )

    report = process_images_with_gemini(flight_end_req.images)

    flight_record = {
        "drone_id": flight_end_req.drone_id,
        "station_id": flight_end_req.station_id,
        "images_count": len(flight_end_req.images),
        "report": report,
        "end_time": datetime.utcnow()
    }
    db["flights_history"].insert_one(flight_record)
    db["active_drones"].delete_one({"drone_id": flight_end_req.drone_id})

    return {
        "message": "Vuelo finalizado. Reporte generado en servidor central.",
        "report": report
    }
