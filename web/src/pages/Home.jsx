import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white p-4">
      <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md text-center">
        <h1 className="text-3xl font-bold text-blue-600">
          Bienvenido al Sistema de Reservas Médicas
        </h1>
        <p className="text-gray-600 mt-3">
          Agenda tu cita de manera fácil, segura y rápida.
        </p>

        <div className="mt-6 space-y-3">
          <Link
            to="/login"
            className="block rounded-xl bg-blue-600 text-white font-semibold py-3 hover:bg-blue-700 transition"
          >
            Iniciar sesión
          </Link>
          
          <Link
            to="/register"
            className="block rounded-xl bg-orange-500 text-white font-semibold py-3 hover:bg-orange-600 transition"
          >
            Registrarse
          </Link>
          
          <Link
            to="/reservas"
            className="block rounded-xl border-2 border-blue-600 text-blue-600 font-semibold py-3 hover:bg-blue-100 transition"
          >
            Ver Reservas
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;