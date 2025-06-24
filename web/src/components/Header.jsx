import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-green-600 p-4 flex justify-between items-center">
      <h1 className="text-white text-xl font-bold">ABP Reservas</h1>
      <nav className="flex space-x-4 text-white">
        <Link to="/" className="hover:underline">Inicio</Link>
        <Link to="/reservas" className="hover:underline">Reservas</Link>
        <Link to="/login" className="hover:underline">Iniciar Sesión</Link>
        <Link to="/register" className="hover:underline">Registrarse</Link>
      </nav>
    </header>
  );
}

export default Header;
