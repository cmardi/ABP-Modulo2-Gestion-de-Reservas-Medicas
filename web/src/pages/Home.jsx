import { Link } from 'react-router-dom';

function Home() {
  return (
    <div>
      <h1>Bienvenido al sistema de reservas médicas</h1>
      <Link to="/login">Iniciar sesión</Link>
      <br />
      <br />
      <Link to="/register">Registrarse</Link>
      <br />
      <Link to="/reservas">Ver reservas</Link>
    </div>
  );
}

export default Home;