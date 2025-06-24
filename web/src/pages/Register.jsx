import RegisterForm from "../components/RegisterForm";

function Register() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-blue-100 to-green-100">
      <div className="bg-white rounded-2xl p-8 shadow-xl max-w-sm w-full">
        <h1 className="text-2xl font-bold text-center text-gray-700">Regístrate</h1>
        <p className="text-gray-500 text-center mt-2">Crea tu cuenta para reservar</p>
        <div className="mt-4">
          <RegisterForm />
        </div>
      </div>
    </div>
  );
}

export default Register;
