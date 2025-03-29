import Title from '../../atoms/title/Title'
import Operation from '../../organisms/Operation/Operation'
import Map from '../../organisms/Map/Map.tsx'
import Rutes from '../../organisms/Rutes/RutesPage.tsx';

const mapPoints = [
    { posX: 50, posY: 100, bgRoute: "/images/map1.png" },
    { posX: 200, posY: 300, bgRoute: "/images/map2.png" },
];

export default function Home(){

    return(
        <main>
        <Title base='Base 1' title='Edificio Central'/>
        <Map mapData={mapPoints} />
        <Operation />
        <Rutes />
        
        </main>
    )
}