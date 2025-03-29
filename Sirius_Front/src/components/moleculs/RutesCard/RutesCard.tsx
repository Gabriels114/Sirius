import WatchIcon from "../../atoms/Icons/WatchIcon";

export default function RutesCard({
    time,
    title
}:{
    time:string,
    title:string
}){
    return(
        <div className="Card_rutes">
            <h3>{title}</h3>
            <div><WatchIcon color="var(--text-subtitles-100)" sx={10}/>{time}</div>
        </div>
    )
}