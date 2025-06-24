import { useState } from 'react';
import ReservaLista from '../components/ReservaLista';
import ReservaForm from '../components/ReservaForm';

function Reservas() {
  const [actualizar, setActualizar] = useState(false);

  const recargarReservas = () => {
    setActualizar(!actualizar); // 🔁 Trigger de actualización
  };

  return (
    <div>
      <h1>Gestión de Reservas</h1>
      <ReservaForm onReservaCreada={recargarReservas} />
      <ReservaLista key={actualizar} />
    </div>
  );
}

export default Reservas;
