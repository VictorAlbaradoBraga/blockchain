import { useState } from "react";

import { API_URL } from "../../config";

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  async function register() {
    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();
      if (response.ok) {
        alert("Usuário cadastrado com sucesso!");
      } else {
        alert(`Erro: ${data.detail || 'Não foi possível cadastrar.'}`);
      }
    } catch {
      alert("Erro na requisição");
    }
  }

  async function login() {
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();
      if (response.ok) {
        alert("Login feito com sucesso!");
        localStorage.setItem("token", data.token);
      } else {
        alert(`Erro: ${data.detail || 'Não foi possível fazer login.'}`);
      }
    } catch {
      alert("Erro na requisição");
    }
  }

  return (
    <section>
      <h2 className="text-xl font-semibold mb-4">Login ou Cadastro</h2>
      <div className="space-y-4">
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="border border-gray-300 rounded px-4 py-2 w-full" />
        <input type="password" placeholder="Senha" value={password} onChange={e => setPassword(e.target.value)} className="border border-gray-300 rounded px-4 py-2 w-full" />
        <div className="space-x-2">
          <button onClick={register} className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">Cadastrar</button>
          <button onClick={login} className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded">Entrar</button>
        </div>
      </div>
    </section>
  );
}
