import './App.css'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/organisms/Home/Home';
import DroneDetail from './components/organisms/DroneDeatail/DroneDeatil';

function App() {


  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/drone_operator/:id' element={<DroneDetail/>}/>
      </Routes>
    </Router>
  )
}

export default App
