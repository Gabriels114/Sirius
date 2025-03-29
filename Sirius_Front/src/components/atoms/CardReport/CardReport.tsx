import DownloadIcon from "../Icons/DownloadIcon"
import Eye from "../Icons/Eye"
import "./CardReport.css"
// import fileContent from "../../../assets/reports/gemini_report.txt"

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

            <button>
            <Eye color="var(--text-principal)" sx={20} />
            </button>
            <DownloadIcon color="var(--text-principal)" sx={20}/>
            </div>

            {/* {fileContent && (
                <pre style={{
                    marginTop: "20px",
                    padding: "10px",
                    border: "1px solid #ccc",
                    borderRadius: "5px",
                    background: "#f9f9f9",
                    whiteSpace: "pre-wrap",
                    textAlign: "left"
                }}>
                    {fileContent}
                </pre>
            )} */}
        </div>
    )
}