import { Link } from "react-router-dom"
import StateDron from "../../atoms/StateDron/StateDron"
import "./Card.css"

export default function Card ({
    title,
    route,
    percentage,
    color,
    img,
    timeArrive,
    timeStart,
    batteryArrive,
    batteryStart
}:{
    title: string,
    route: string,
    percentage: number,
    color: string,
    img:string,
    timeArrive: string,
    timeStart: string,
    batteryArrive: number,
    batteryStart: number
}){
    const timeArr = timeArrive.split("T")
    const timeSt = timeStart.split("T")



    return(
        <div className="Card_Container">
            <div className="Card_Text"
                style={{
                    background: `linear-gradient(to right, ${color} 5px, var(--card-background) 5px)`
    
                }}
            >
                <h3>{title}</h3>
                <p style={{fontWeight:"bold", color:"var(--text-subtitles-100)"}}>{route}</p>
                <p style={{fontWeight:"100", lineHeight:".75", marginBottom:"10px"}}>{percentage}% del trayecto</p>

                <StateDron  battery={batteryStart} state="Salida" time={timeSt[1].split(".")[0]}/>
                <StateDron  battery={batteryArrive} state="Salida" time={timeArr[1].split(".")[0]}/>

            </div>
            <div className="Card_Container_Image" 
                style={{
                    background: `linear-gradient(to bottom, transparent 70%, var(--background) 100%), url(${img}) no-repeat center center`,
                    backgroundSize: "cover"
                }}
            >
                    <Link to={`/drone_operator/${title}`} children="Ver Trayecto"/>
                    <button children="Forzar regreso" style={{color: 'var(--red-alert)' }}/>
            </div>
        </div>
    ) 
}