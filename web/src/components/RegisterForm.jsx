import { useState } from 'react';
import api from '../services/api';

function RegisterForm({ onRegister }) {
  const [form, setForm] = useState({
    rut: '',
    nombre_completo: '',
    email: '',
    password: '',
    is_cliente: true, // o is_medico según el tipo de usuario
  });
  const [mensaje, setMensaje] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('auth/register/', form);
      setMensaje('Usuario registrado con éxito');
      if (onRegister) onRegister();
    } catch (error) {
      if (error.response && error.response.data) {
        setMensaje('Error: ' + JSON.stringify(error.response.data));
      } else {
        setMensaje('Error al registrar usuario');
      }
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <h2>Registro de usuario</h2>
      {mensaje && <p>{mensaje}</p>}
      <input name="rut" placeholder="RUT" value={form.rut} onChange={handleChange} required />
      <input name="nombre_completo" placeholder="Nombre completo" value={form.nombre_completo} onChange={handleChange} required />
      <input name="email" type="email" placeholder="Email" value={form.email} onChange={handleChange} required />
      <input name="password" type="password" placeholder="Contraseña" value={form.password} onChange={handleChange} required />
      <select name="is_cliente" value={form.is_cliente} onChange={handleChange}>
        <option value={true}>Paciente</option>
        <option value={false}>Médico</option>
      </select>
      <button type="submit">Registrar</button>
    </form>
  );
}

export default RegisterForm;