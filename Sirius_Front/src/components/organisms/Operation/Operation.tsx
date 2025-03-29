import Card from "../../moleculs/CardOperations/Card";
import img1 from "../../../assets/city_1.jpg"
import"./Operation.css"
import SubTitle from "../../moleculs/SubTitle_btn/SubTitleBtn";
import useFetchData from "../../../hooks/useFetchData";
import Skeleton from "../../atoms/Skeleton/Skeleton";

export default function Operation() {
    const {data} = useFetchData()

    return(
        <section className="Operation_Container">
            <SubTitle title="En operacion"  onClick={async () => {
        try {
            const response = await fetch("https://kvq8ctwm-8000.usw3.devtunnels.ms/deploy_drone", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    latitude: 0,
                    longitude: 0
                })
            });

            if (!response.ok) {
                throw new Error("Error al enviar la solicitud");
            }

            const data = await response.json();
            console.log("Respuesta del servidor:", data);
            alert("Dron forzado a regresar correctamente.");
        } catch (error) {
            console.error("Error:", error);
            alert("Error al forzar el regreso del dron.");
        }
    }}/>


            <div className="Operation_Cards">
                
            {data ? data?.map((drone,i) => (
                
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
                )) :(
                    <>
                        <Skeleton 
                            width={"300"} 
                            height={120} 
                            $variant="body" 
                            $animation={"wave"}
                            style={{borderRadius: "20px",minWidth:"280px"}}
                            />
                        <Skeleton 
                            width={"300"} 
                            height={120} 
                            $variant="body" 
                            $animation={"wave"}
                            style={{borderRadius: "20px",minWidth:"280px"}}
                            />
                        <Skeleton 
                            width={"300"} 
                            height={120} 
                            $variant="body" 
                            $animation={"wave"}
                            style={{borderRadius: "20px",minWidth:"280px"}}
                            />
                    </>
                    
                )}
            </div>
        </section>
    )
}
