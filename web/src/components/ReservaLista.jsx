import { motion } from 'framer-motion';

function ReservaLista({ reservas }) {
  if (!reservas || reservas.length === 0) {
    return <p className="text-gray-600">No hay reservas registradas aún.</p>;
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-lg space-y-4">
      <h2 className="text-xl font-bold text-gray-700">Mis Reservas</h2>
      <div className="grid gap-3">
        {reservas.map((reserva, index) => (
          <motion.div
            key={index}
            className="p-4 rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <p><strong>Fecha:</strong> {reserva.fecha}</p>
            <p><strong>Hora:</strong> {reserva.hora}</p>
            <p><strong>Especialidad:</strong> {reserva.especialidad}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export default ReservaLista;
