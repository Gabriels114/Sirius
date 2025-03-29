import PlusIcon from "../../atoms/Icons/PlusIcon";

export default function SubTitle({
    title,
    onClick,
}: {title:string,
    onClick?: () => void,
}){ 
    return (
        <>
        <span style={{ display: 'flex', alignItems: 'center', gap: '5px', marginTop: '20px' }}>
            <h2>{title}</h2>
            <button 
                children={PlusIcon({ color: "var(--background)", sx: 13 })}
                onClick={onClick}
                style={{
                    borderRadius: '50%',
                    backgroundColor: 'var(--text-principal)',
                    border: 'none',
                    width: '19px',
                    height: '19px',
                    display: "grid",
                    placeItems: "center",
                    cursor: "pointer"
                }}
                />
        </span>
        </>
    )
}