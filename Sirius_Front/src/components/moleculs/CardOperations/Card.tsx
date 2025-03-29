import StateDron from "../../atoms/StateDron/StateDron"
import "./Card.css"

export default function Card ({
    title,
    route,
    percentage,
    color,
    img
}:{
    title: string,
    route: string,
    percentage: number,
    color: string,
    img: string
}){
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

                <StateDron  battery={98} state="Salida" time="13:30:00"/>
                <StateDron  battery={50} state="Salida" time="13:30:00"/>
                <StateDron  battery={15} state="Salida" time="13:30:00"/>

            </div>

            <div className="Card_Container_Image" 
                style={{
                    background: `linear-gradient(to bottom, transparent 70%, var(--background) 100%), url(${img}) no-repeat center center`,
                    backgroundSize: "cover"
                }}
            >
                    <button children="Visualizar Ruta"/>
                    <button children="Forzar regreso" style={{color: 'var(--red-alert)' }}/>
            </div>
        </div>
    ) 
}