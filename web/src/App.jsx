import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Reservas from './pages/Reservas';
import Register from './pages/Register';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <Header /> 
      <div className="pt-4">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/reservas" element={<Reservas />} />
        <Route path="/register" element={<Register />} />
      </Routes>
      </div>
      <Footer /> 
    </Router>
  );
}

export default App;
