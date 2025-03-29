from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from pydantic import BaseModel
from typing import Dict
import requests
import uuid
from datetime import datetime
import asyncio
import math
import httpx

CENTRAL_SERVER_URL = "http://0.0.0.0:8000"

simulated_drones = {}

class InstructDroneRequest(BaseModel):
    drone_id: str
    latitude: float
    longitude: float

class DroneUpdate(BaseModel):
    drone_id: str
    station_id: str
    battery: float
    current_latitude: float
    current_longitude: float
    timestamp: str

class EndFlightUpdate(BaseModel):
    drone_id: str
    station_id: str
    images: list
    timestamp: str

class DroneInfo:
    def __init__(self, drone_id: str):
        self.drone_id = drone_id
        self.battery = 100.0
        self.current_latitude = 0.0
        self.current_longitude = 0.0
        self.is_active = False
        self.start_time = None

drones_inventory: Dict[str, DroneInfo] = {}

app = FastAPI(title="Servidor de Estación")

STATION_ID = None

@app.on_event("startup")
async def startup_event():
    global STATION_ID
    try:
        register_payload = {
            "station_name": "Estacion_Sur", 
            "coverage_area": "Zona Sur de la Ciudad"
        }
        response = requests.post(f"{CENTRAL_SERVER_URL}/register_station", json=register_payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        STATION_ID = data["station_id"]
        print(f"[Station Server] Estación registrada correctamente con ID: {STATION_ID}")
    except Exception as e:
        print(f"[Station Server] Error registrando la estación: {e}")

    for i in range(3):
        drone_id = str(uuid.uuid4())
        drones_inventory[drone_id] = DroneInfo(drone_id=drone_id)
    print("[Station Server] Drones inicializados en la estación:")
    for d_id in drones_inventory:
        print(f"   - {d_id}")


def distance_in_degrees(lat1, lon1, lat2, lon2):
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

def generate_route(start_lat, start_lon, target_lat, target_lon):
    mid_lat = (start_lat + target_lat) / 2
    mid_lon = (start_lon + target_lon) / 2

    route = [
        (start_lat, start_lon),
        (mid_lat, mid_lon),
        (target_lat, target_lon),
        (start_lat, start_lon)
    ]
    return route

class SimulatedDrone:
    def __init__(self, station_id: str, start_lat: float, start_lon: float, 
                 target_lat: float, target_lon: float, speed: float = 0.0001, 
                 drone_id: str = None,
                 battery_threshold: float = 30.0):
        self.drone_id = drone_id if drone_id else str(uuid.uuid4())
        self.station_id = station_id
        self.speed = speed
        self.battery = 100.0
        self.start_time = datetime.utcnow()
        self.flight_ended = False
        self.battery_threshold = battery_threshold
        self.route = generate_route(start_lat, start_lon, target_lat, target_lon)
        self.route_index = 0
        self.current_lat, self.current_lon = self.route[0]

    def update_position(self):
        if self.route_index >= len(self.route) - 1:
            return

        next_lat, next_lon = self.route[self.route_index + 1]
        d_lat = next_lat - self.current_lat
        d_lon = next_lon - self.current_lon
        dist = math.sqrt(d_lat**2 + d_lon**2)

        if dist < self.speed:
            self.current_lat = next_lat
            self.current_lon = next_lon
        else:
            self.current_lat += (d_lat / dist) * self.speed
            self.current_lon += (d_lon / dist) * self.speed

    def update_battery(self):
        self.battery = max(0, self.battery - 1)

    def check_if_arrived_waypoint(self):
        current_wp = (self.current_lat, self.current_lon)
        target_wp = self.route[self.route_index + 1] if (self.route_index + 1) < len(self.route) else None

        if target_wp and distance_in_degrees(current_wp[0], current_wp[1],
                                             target_wp[0], target_wp[1]) < 1e-7:
            self.route_index += 1
            if self.route_index == len(self.route) - 1:
                self.flight_ended = True

    def maybe_return_to_station(self):
        if self.battery <= self.battery_threshold and not self.flight_ended:
            station_lat, station_lon = self.route[-1]
            self.route = [
                (self.current_lat, self.current_lon),
                (station_lat, station_lon)
            ]
            self.route_index = 0
            print(f"[SimulatedDrone] Batería baja: ajustando ruta para volver directamente a estación.")

    def has_reached_final_station(self) -> bool:
        return self.flight_ended

async def send_update_to_station(drone: SimulatedDrone):
    async with httpx.AsyncClient() as client:
        payload = {
            "drone_id": drone.drone_id,
            "station_id": drone.station_id,
            "battery": drone.battery,
            "current_latitude": drone.current_lat,
            "current_longitude": drone.current_lon,
            "timestamp": datetime.utcnow().isoformat()
        }
        try:
            response = await client.post("http://0.0.0.0:8100/drone_update", json=payload, timeout=5)
            print(f"[SimulatedDrone] Update enviado. Dron={drone.drone_id}, Código={response.status_code}")
        except Exception as e:
            print(f"[SimulatedDrone] Error enviando update a /drone_update: {e}")


async def send_end_flight_to_station(drone: SimulatedDrone):
    async with httpx.AsyncClient() as client:
        payload = {
            "drone_id": drone.drone_id,
            "station_id": drone.station_id,
            "images": ["FakeImageBase64_1", "FakeImageBase64_2"],
            "timestamp": datetime.utcnow().isoformat()
        }
        try:
            response = await client.post("http://0.0.0.0:8100/end_flight_update", json=payload, timeout=5)
            print(f"[SimulatedDrone] Fin de vuelo enviado. Dron={drone.drone_id}, Código={response.status_code}")
        except Exception as e:
            print(f"[SimulatedDrone] Error enviando fin de vuelo a /end_flight_update: {e}")

async def simulate_drone_flight(drone: SimulatedDrone):
    print(f"[SimulatedDrone] Iniciando simulación para dron {drone.drone_id}")

    while not drone.has_reached_final_station():
        drone.update_position()
        drone.update_battery()
        drone.maybe_return_to_station()
        drone.check_if_arrived_waypoint()
        await send_update_to_station(drone)
        if drone.has_reached_final_station() or drone.battery <= 0:
            break

        await asyncio.sleep(2)
    await send_end_flight_to_station(drone)
    print(f"[SimulatedDrone] Simulación finalizada para dron {drone.drone_id}")

@app.post("/instruct_drone")
def instruct_drone(request: InstructDroneRequest, background_tasks: BackgroundTasks):
    if STATION_ID is None:
        raise HTTPException(
            status_code=500, 
            detail="La estación no se ha registrado correctamente en el servidor central."
        )

    if request.drone_id not in drones_inventory:
        drones_inventory[request.drone_id] = DroneInfo(drone_id=request.drone_id)

    drone_info = drones_inventory[request.drone_id]
    drone_info.is_active = True
    drone_info.start_time = datetime.utcnow()

    start_lat = 40.7128
    start_lon = -74.0060

    target_lat = request.latitude
    target_lon = request.longitude

    simulated_drone = SimulatedDrone(
        station_id=STATION_ID,
        start_lat=start_lat,
        start_lon=start_lon,
        target_lat=target_lat,
        target_lon=target_lon,
        speed=0.0003,
        drone_id=request.drone_id,
        battery_threshold=30
    )
    simulated_drones[request.drone_id] = simulated_drone

    background_tasks.add_task(simulate_drone_flight, simulated_drone)

    return {
        "message": "Dron instruido para volar mediante simulación con ruta y retorno anticipado.",
        "drone_id": request.drone_id
    }

@app.post("/drone_update")
async def drone_update(update: DroneUpdate):
    print(f"[Station Server] Recibido update del simulador: {update.dict()}")
    
    if update.drone_id in drones_inventory:
        local_drone = drones_inventory[update.drone_id]
        local_drone.battery = update.battery
        local_drone.current_latitude = update.current_latitude
        local_drone.current_longitude = update.current_longitude
    else:
        print(f"[Station Server] Advertencia: dron {update.drone_id} no está en el inventario local.")

    try:
        forward_payload = {
            "drone_id": update.drone_id,
            "station_id": update.station_id,
            "battery": update.battery,
            "current_latitude": update.current_latitude,
            "current_longitude": update.current_longitude
        }
        response = requests.post(
            f"{CENTRAL_SERVER_URL}/drone_updates", 
            json=forward_payload, 
            timeout=5
        )
        print(f"[Station Server] Forwarded update to central. Status={response.status_code}")
    except Exception as e:
        print(f"[Station Server] Error forwarding update to central server: {e}")

    return {"message": "Update recibido y reenviado al servidor central."}


@app.post("/end_flight_update")
async def end_flight_update(update: EndFlightUpdate):
    print(f"[Station Server] Recibido fin de vuelo del simulador: {update.dict()}")
    
    if update.drone_id in drones_inventory:
        local_drone = drones_inventory[update.drone_id]
        local_drone.is_active = False
    else:
        print(f"[Station Server] Advertencia: dron {update.drone_id} no encontrado en inventario local.")

    try:
        forward_payload = {
            "drone_id": update.drone_id,
            "station_id": update.station_id,
            "images": update.images
        }
        response = requests.post(
            f"{CENTRAL_SERVER_URL}/end_flight", 
            json=forward_payload, 
            timeout=5
        )
        print(f"[Station Server] Forwarded end flight update. Status={response.status_code}")
    except Exception as e:
        print(f"[Station Server] Error forwarding end flight update to central: {e}")

    return {"message": "Fin de vuelo recibido y reenviado al servidor central."}

@app.post("/force_return")
def force_return(request: dict):
    drone_id = request.get("drone_id")
    if not drone_id:
        raise HTTPException(status_code=400, detail="Falta el drone_id en la solicitud.")

    simulated_drone = simulated_drones.get(drone_id)
    if simulated_drone is None:
         raise HTTPException(status_code=404, detail="Dron simulado no encontrado.")

    simulated_drone.maybe_return_to_station()
    return {"message": "Se ha forzado el retorno del dron.", "drone_id": drone_id}
