import DownloadIcon from "../Icons/DownloadIcon"
import Eye from "../Icons/Eye"
import "./CardReport.css"

export default function CardReport ({
    date,
    route,
    color
}:{
    date: string,
    route: string,
    color:string
}) {
    return( 
        <div className="card_report_container"
            style={{
                background: `linear-gradient(to right, ${color} 5px, var(--card-background) 5px)`
            }}
        >
            <div>
                <h3>{route} </h3>
                <p>{date}</p>
            </div>

            <div className="icons_container">

            <Eye color="var(--text-principal)" sx={20}/>
            <DownloadIcon color="var(--text-principal)" sx={20}/>
            </div>
        </div>
    )
}