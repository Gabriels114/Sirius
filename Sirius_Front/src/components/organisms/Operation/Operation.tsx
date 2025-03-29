import PlusIcon from "../../atoms/Icons/PlusIcon";
import Card from "../../moleculs/CardOperations/Card";
import"./Operation.css"

export default function Operation() {
    return(
        <section className="Operation_Container">
            <span style={{display:'flex', alignItems:'center', gap:'5px', marginTop: '20px'}}>
                <h2>En operacion</h2>
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

            <Card/>

        </section>
    )
}
