import PlusIcon from "../../atoms/Icons/PlusIcon";

export default function SubTitle({title}: {title:string}){
    return(

    <span style={{display:'flex', alignItems:'center', gap:'5px', marginTop: '20px'}}>
        <h2>{title}</h2>
        <button children={PlusIcon({color: "var(--background)", sx:13 })}
                style={{
                    borderRadius: '50%',
                    backgroundColor: 'var(--text-principal)',
                    border: 'none',
                    width: '19px',
                    height: '19px',
                    display: "grid",
                    placeItems: "center",
                }}
                />
        </span>
    )
}