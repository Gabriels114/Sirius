import { useEffect, useState } from "react";
const ApiDataDrone = "https://kvq8ctwm-8000.usw3.devtunnels.ms/active_drones"

interface DroneData {
    drone_id: string;
    station_id: string;
    battery: number;
    video_feed_url: string;
    current_latitude: number;
    current_longitude: number;
    departure_time: string;
    estimated_arrival: string;
    flight_time_minutes: number;
}

interface DataFetch {
    data: DroneData[] | null; 
    loading: boolean;
    error: string | null;
}

export default function useFetchData(){

    const dataFetch: DataFetch = {
        data: null,
        loading: false,
        error: null
    }

    const [data, setData] = useState(dataFetch)

    const fetchData = async () => {
        setData(prevState => ({
            ...prevState,
            loading: true
        }));

        try {
            const response = await fetch(ApiDataDrone);
            if (!response.ok) throw new Error("Error en la respuesta del servidor");
            const result: DroneData[] = await response.json();  // Definimos que 'result' es un array de DroneData

            setData(prevState => ({
                ...prevState,
                data: result,
                loading: false,
                error: null
            }));
        } catch (err: unknown) {
            if (err instanceof Error) {
                setData(prevState => ({
                    ...prevState,
                    loading: false,
                    error: err.message
                }));
            } else {
                setData(prevState => ({
                    ...prevState,
                    loading: false,
                    error: "Unknown error occurred"
                }));
            }
        }
    };

    useEffect(() => {
        fetchData(); 
        const interval = setInterval(fetchData, 30000)

        return () => clearInterval(interval)
    },[])

    return data;
}