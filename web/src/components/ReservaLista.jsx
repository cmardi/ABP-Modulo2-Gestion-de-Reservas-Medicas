import { useEffect, useState } from 'react';
import api from '../services/api';
import { getAuthToken } from '../services/auth';

function ReservaLista() {
  const [reservas, setReservas] = useState([]);

  useEffect(() => {
    const fetchReservas = async () => {
      try {
        const token = getAuthToken();
        const response = await api.get('reservas/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setReservas(response.data);
      } catch (error) {
        console.error('Error al cargar reservas:', error);
      }
    };

    fetchReservas();
  }, []);

  return (
    <div>
      <h2>Listado de Reservas</h2>
      <ul>
        {reservas.map((reserva) => (
          <li key={reserva.id}>
            Paciente: {reserva.paciente_nombre} | Médico: {reserva.medico_nombre} | Inicio: {new Date(reserva.fecha_inicio).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReservaLista;
