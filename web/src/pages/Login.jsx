import LoginForm from '../components/LoginForm';
import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();

  const handleLoginSuccess = () => {
    navigate('/reservas'); // 👉 Cambia aquí
  };

  return (
    <div>
      <LoginForm onLogin={handleLoginSuccess} />
    </div>
  );
}

export default Login;
