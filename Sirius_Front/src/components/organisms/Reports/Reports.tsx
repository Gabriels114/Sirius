import CardReport from "../../atoms/CardReport/CardReport";
import SubTitle from "../../moleculs/SubTitle_btn/SubTitleBtn";
import "./Report.css"

export default function Reports(){
    return(
        <section className="reports_container">
            <SubTitle title="Reportes"/>

            <CardReport route="Ruta A" date="29 / 03 / 2025" color="#b00"/>
            <CardReport route="Ruta A" date="29 / 03 / 2025" color="#bb0"/>
            <CardReport route="Ruta A" date="29 / 03 / 2025" color="#b0b"/>
            <CardReport route="Ruta A" date="29 / 03 / 2025" color="#0bb"/>
        </section>
    )
}