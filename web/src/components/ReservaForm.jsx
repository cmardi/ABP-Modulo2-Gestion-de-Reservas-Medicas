import { useState, useEffect } from 'react';
import ReservaLista from '../components/ReservaLista';
import api from '../services/api';
import { getAuthToken } from '../services/auth';

function Reservas() {
  const [reservas, setReservas] = useState([]);

  useEffect(() => {
    const fetchReservas = async () => {
      try {
        const token = getAuthToken();
        const response = await api.get('reservas/', {
          headers: {
            Authorization: `Bearer ${token}`
          },
        });
        setReservas(response.data);
      } catch (error) {
        console.error(error);
      }
    };
    fetchReservas();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-700">Gestión de Reservas</h1>
      <ReservaLista reservas={reservas} />
    </div>
  );
}

export default Reservas;
