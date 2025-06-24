import { useState } from 'react';
import api from '../services/api';
import { setAuthToken } from '../services/auth';

function LoginForm({ onLogin }) {
  const [rut, setRut] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('token/', { rut, password });
      setAuthToken(response.data.access);
      onLogin(); // Redirige al Home
    } catch (err) {
      setError('Credenciales incorrectas');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Iniciar sesión</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input
        type="text"
        placeholder="RUT"
        value={rut}
        onChange={(e) => setRut(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Contraseña"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Entrar</button>
    </form>
  );
}

export default LoginForm;
