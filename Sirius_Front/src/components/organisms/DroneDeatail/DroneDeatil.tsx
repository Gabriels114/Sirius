import { useParams } from "react-router-dom";
import Title from "../../atoms/title/Title";
import useFetchData from "../../../hooks/useFetchData";
import img1 from "../../../assets/city_1.jpg"
import useFlightProgress from "../../../hooks/useFlightProgress";
import "./DroneDetail.css"
import CompassIcon from "../../atoms/Icons/CompassIcons";
import AddressIcon from "../../atoms/Icons/AddressIcon";


export default function DroneDetail(){
    const {id} = useParams()
    const {data} = useFetchData()
    const dataCurr = data && data?.find(val => val.drone_id.substring(0,5) === id) 



    const departure = data && dataCurr?.departure_time
    const arrival = data && dataCurr?.estimated_arrival
    const minutes = data && dataCurr?.flight_time_minutes

    const prog = useFlightProgress({
        departure: departure || "", 
        arrival: arrival || "", 
        minutes: minutes || 0
    })

    return(
        <main key="main_2">
            <Title base='Base 1' title='Edificio Central / Detalle del vuelo'/>

            <div style={{
                background: `url(${img1}) center no-repeat`,
                backgroundSize: "cover",
                width: "100%",
                aspectRatio: "1/1",
                margin: "15px 0px"
            }}/>

            {dataCurr && (
                <section className="details_container">
                    <h3>Detalles de: {id}</h3>
                    <p style={{ fontWeight: "bold", color: "var(--text-subtitles-100)" }}>Ruta 2</p>
                    <p style={{ fontWeight: "100", lineHeight: ".75", marginBottom: "10px" }}>
                            {prog}% del trayecto
                        </p>

                        <span className="coordinates_container">
                            <div className="title_coor">
                            <CompassIcon color="var( --text-subtitles)" sx={12}/>
                            <p>Coordenadas:</p>
                            </div>
                            <div className="data_coor">
                                <p><strong>latitud:</strong> {dataCurr!.current_latitude}</p>
                                <p><strong>longitud:</strong> {dataCurr!.current_longitude}</p>
                            </div>
                        </span>
                        
                        <span>
                            <div className="title_coor">
                                <AddressIcon color="var( --text-subtitles)" sx={12}/>
                                <p>Id de la Unidad:</p>
                            </div>
                            <p className="data_id"><strong>Id:</strong> {dataCurr!.station_id}</p>
                        </span>

                        <button children="Forzar regreso"/>
                    </section>
                )}
            
        </main>
    )
}