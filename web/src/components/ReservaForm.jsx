import { useState, useEffect } from 'react';
import api from '../services/api';
import { getAuthToken } from '../services/auth';

function ReservaForm({ onReservaCreada }) {
  const [medicos, setMedicos] = useState([]);
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [medico, setMedico] = useState('');
  const [motivo, setMotivo] = useState('');
  const [mensaje, setMensaje] = useState('');

  useEffect(() => {
    const fetchMedicos = async () => {
      try {
        const token = getAuthToken();
        const res = await api.get('usuarios/medicos/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setMedicos(res.data);
      } catch (err) {
        console.error('Error cargando médicos:', err);
      }
    };
    fetchMedicos();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = getAuthToken();
      await api.post(
        'reservas/',
        {
          medico,
          fecha_inicio: fechaInicio,
          fecha_fin: fechaFin,
          motivo,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setMensaje('✅ Reserva creada con éxito.');
      setFechaInicio('');
      setFechaFin('');
      setMedico('');
      setMotivo('');
      onReservaCreada(); // Actualiza lista
    } catch (error) {
      setMensaje('❌ Error al crear la reserva.');
      console.error(error);
    }
  };

  return (
    <div>
      <h3>Crear nueva reserva</h3>
      {mensaje && <p>{mensaje}</p>}
      <form onSubmit={handleSubmit}>
        <label>Médico:</label>
        <select value={medico} onChange={(e) => setMedico(e.target.value)} required>
          <option value="">Selecciona un médico</option>
          {medicos.map((m) => (
            <option key={m.id} value={m.id}>{m.nombre_completo}</option>
          ))}
        </select>

        <label>Fecha Inicio:</label>
        <input type="datetime-local" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} required />

        <label>Fecha Fin:</label>
        <input type="datetime-local" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} required />

        <label>Motivo:</label>
        <textarea value={motivo} onChange={(e) => setMotivo(e.target.value)} />

        <button type="submit">Crear Reserva</button>
      </form>
    </div>
  );
}

export default ReservaForm;
