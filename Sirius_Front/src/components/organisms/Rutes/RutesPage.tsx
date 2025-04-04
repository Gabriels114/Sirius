import WatchIcon from "../../atoms/Icons/WatchIcon";
import SubTitle from "../../moleculs/SubTitle_btn/SubTitleBtn";
import "./RutesPage.css"

export default function Rutes(){
    return(
        <section className="rutes_container">
            <SubTitle title="Rutas Predifinidas"/>

            <div className="card_container">
                <div className="Card_rutes">
                    <h3>Ruta: A</h3>
                    <div><WatchIcon color="var(--text-subtitles-100)" sx={10}/> 45 min</div>
                </div>
                <div className="Card_rutes">
                    <h3>Ruta: B</h3>
                    <div><WatchIcon color="var(--text-subtitles-100)" sx={10}/> 35 min</div>
                </div>
            </div>
        </section>
    )
}