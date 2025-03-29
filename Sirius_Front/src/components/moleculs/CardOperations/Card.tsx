import "./Card.css"

export default function Card (){
    return(
        <div className="Card_Container">
            <div>

            </div>

            <div className="Card_Container_Image">
                <section className='Card_Container_Image_Section'>
                    <button children="Visualizar Ruta"/>
                    <button children="Forzar regreso" style={{color: 'var(--red-alert)' }}/>


                </section>
            </div>
        </div>
    ) 
}