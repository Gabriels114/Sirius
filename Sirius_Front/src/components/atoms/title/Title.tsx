export default function Title({ base,title }: { base: string,title: string }) {
    return(
        <>
            <span
                style={{
                    display: "flex",
                    alignItems: "center",
                    gap: '5px',
                    color: 'var(--text-principal)',
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
                    fontSize: 'var(--font-xl)',
                    color: 'var(--text-principal)',
                }}
            >{title}</h1>
        </>
    )
}