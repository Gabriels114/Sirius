import { useParams } from "react-router-dom";
import Title from "../../atoms/title/Title";
import useFetchData from "../../../hooks/useFetchData";
import img1 from "../../../assets/city_1.jpg"
import useFlightProgress from "../../../hooks/useFlightProgress";


export default function DroneDetail(){
    const {id} = useParams()
    const data = useFetchData()
    const dataCurr = data.data?.find(val => val.drone_id === id) 
    const departure = dataCurr?.departure_time
    const arrival = dataCurr?.estimated_arrival
    const minutes = dataCurr?.flight_time_minutes

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
                <>
                    <h3>{dataCurr.drone_id}</h3>
                    <p style={{ fontWeight: "bold", color: "var(--text-subtitles-100)" }}>Ruta 2</p>
                    <p style={{ fontWeight: "100", lineHeight: ".75", marginBottom: "10px" }}>
                        {prog}% del trayecto
                    </p>

                    <p>{dataCurr.current_latitude}</p>
                    <p>{dataCurr.current_longitude}</p>
                    <p>{dataCurr.station_id}</p>
                </>
            )}
        </main>
    )
}