import StateDron from "../../atoms/StateDron/StateDron"
import "./Card.css"

export default function Card ({
    title,
    route,
    percentage,
}:{
    title: string,
    route: string,
    percentage: number,
}){
    return(
        <div className="Card_Container">
            <div className="Card_Text">
                <h3>{title}</h3>
                <p style={{fontWeight:"bold", color:"var(--text-subtitles-100)"}}>{route}</p>
                <p style={{fontWeight:"100", lineHeight:".75", marginBottom:"10px"}}>{percentage}% del trayecto</p>

                <StateDron  battery={98} state="Salida" time="13:30:00"/>
                <StateDron  battery={50} state="Salida" time="13:30:00"/>
                <StateDron  battery={15} state="Salida" time="13:30:00"/>

            </div>

            <div className="Card_Container_Image">
                    <button children="Visualizar Ruta"/>
                    <button children="Forzar regreso" style={{color: 'var(--red-alert)' }}/>
            </div>
        </div>
    ) 
}