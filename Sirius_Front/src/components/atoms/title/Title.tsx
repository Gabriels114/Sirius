export default function Title({ base,title }: { base: string,title: string }) {
    return(
        <>
            <span
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: '5px',
                }}
            >
                <div 
                    style={{
                        width: '10px',
                        height: '10px',
                        backgroundColor: '#270477',
                        borderRadius: '50%'
                    }}>
                </div>
                {base}
            </span>
            <h1
                style={{
                    lineHeight: '.75',
                    fontSize: 'var(--font-xl)'
                }}
            >{title}</h1>
        </>
    )
}