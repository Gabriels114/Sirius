import { useParams } from "react-router-dom";
import Title from "../../atoms/title/Title";
import useFetchData from "../../../hooks/useFetchData";
import img1 from "../../../assets/city_1.jpg"


export default function DroneDetail(){
    const {idPar} = useParams()
    const data = useFetchData()
    const dataCurr = data.data?.find(val => val.drone_id === idPar)

    return(
        <main>
            <Title base='Base 1' title='Edificio Central / Detalle del vuelo'/>

            <div style={{
                background: `url(${img1}) center no-repeat`,
                backgroundSize: "cover",
                width: "100%",
                aspectRatio: "1/1",
                margin: "15px 0px"
            }}/>

                <h3>{dataCurr?.drone_id}</h3>
                <p style={{fontWeight:"bold", color:"var(--text-subtitles-100)"}}>Ruta 2</p>
                <p style={{fontWeight:"100", lineHeight:".75", marginBottom:"10px"}}>{dataCurr.}% del trayecto</p>
        </main>
    )
}