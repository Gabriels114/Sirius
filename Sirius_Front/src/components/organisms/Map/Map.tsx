import { useEffect, useState } from "react";
import "./Map.css"

interface MapProps {
    posX: number;
    posY: number;
    bgRoute: string;
}

interface MapComponentProps {
    mapData: MapProps[]; 
}

export default function Map({mapData}: MapComponentProps) {
    const [data, setData] = useState<MapProps[]>([]);
    useEffect(() => {
        setData(mapData)
    },[mapData])


    return(
        <section className="Map_Container">
            {data.map(({ posX, posY, bgRoute }, index) => (
                <div
                    key={index} 
                    className="Map"
                    style={{
                        backgroundColor: bgRoute,
                        left: `${posX}px`,
                        top: `${posY}px`,
                        position: "absolute"
                    }}
                />
            ))}
        </section>
    )
}