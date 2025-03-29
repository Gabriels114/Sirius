import usePercentageColor from "../../../hooks/usePercentageColor"
import Battery from "../Icons/Battery"
import WatchIcon from "../Icons/WatchIcon"
import "./StateDron.css"

export default function StateDron({
    time,
    state,
    battery
}:{
    time: string,
    state: "Salida"|"Actual"|"Vuelta",
    battery: number
}){
    const color = usePercentageColor(battery)

    return(
            <div className="data_dron">
                <p>{state}: </p>
                <p>{time}</p>
                <WatchIcon color="var(--text-subtitles-100)" sx={12}/>
                <p>{battery}%</p>
                <Battery color={color} sx={12}/>
            </div>
    )
}