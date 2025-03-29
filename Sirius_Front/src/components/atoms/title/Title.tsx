import { Link } from "react-router-dom"
import "./title.css"

export default function Title({ base,title }: { base: string,title: string }) {
    const titleIsFather = title.includes("/")
    let titleSplited 
    if (titleIsFather) titleSplited = title.split("/")

    return(
        <section className="title_container">
            <span
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: '5px',
                    color: 'var(--text-principal)',
                }}
            >
                <div 
                    style={{
                        width: '10px',
                        height: '10px',
                        backgroundColor: '#270477',
                        borderRadius: '50%'
                    }}>
                </div>
                {base}
            </span>
            {!titleIsFather 
            ?(
                <h1
                    style={{
                        lineHeight: '.75',
                        fontSize: 'var(--font-xl)',
                        color: 'var(--text-principal)',
                    }}
                >{title}</h1>
            ):(
                <Link to="/" style={{ textDecoration:"none"}}>
                <h1
                style={{
                    lineHeight: '.75',
                    fontSize: 'var(--font-xl)',
                    color: 'var(--text-principal)',
                    
                }}
                >{titleSplited![0]}<span style={{fontWeight: "300"}}> / {titleSplited![1]}</span></h1>
                </Link>
            )}

        </section>
    )
}