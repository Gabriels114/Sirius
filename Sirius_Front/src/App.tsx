import './App.css'
import Title from './components/atoms/title/Title'
import Operation from './components/organisms/Operation/Operation'
import Map from './components/organisms/Map/Map.tsx'
import Rutes from './components/organisms/Rutes/RutesPage.tsx';

function App() {
  const mapPoints = [
    { posX: 50, posY: 100, bgRoute: "/images/map1.png" },
    { posX: 200, posY: 300, bgRoute: "/images/map2.png" },
];

  return (
      <main>
        <Title base='Base 1' title='Edificio Central'/>
        <Map mapData={mapPoints} />
        <Operation />
        <Rutes />
        
      </main>

  )
}

export default App
