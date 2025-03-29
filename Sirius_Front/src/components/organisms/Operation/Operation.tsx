import Card from "../../moleculs/CardOperations/Card";
import img1 from "../../../assets/city_1.jpg"
import"./Operation.css"
import SubTitle from "../../moleculs/SubTitle_btn/SubTitleBtn";
import useFetchData from "../../../hooks/useFetchData";

export default function Operation() {
    const {data} = useFetchData()

    return(
        <section className="Operation_Container">
            <SubTitle title="En operacion"/>


            <div className="Operation_Cards">
                
            {data && data?.map((drone,i) => (
                
                <Card 
                    key={drone.drone_id} 
                    percentage={drone.battery} 
                    route={"Ruta " + (i+1)} 
                    title={drone.drone_id.substring(0,5)} 
                    color="#2192AC" 
                    img={img1}
                    batteryArrive={15}
                    batteryStart={drone.battery}
                    timeArrive={drone.estimated_arrival}
                    timeStart={drone.departure_time}
                    />
                ))}
            </div>
        </section>
    )
}
