import { useState } from 'react';

import { API_URL } from "../../config";

export default function LoginModal({ open, onClose, onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [creatorType, setCreatorType] = useState('');

  if (!open) return null;

  async function handleSubmit() {
    try {
      const url = isLogin ? `${API_URL}/auth/login` : `${API_URL}/auth/register`;
      const body = isLogin ? { email, password } : { email, password, name, creator_type: creatorType };

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (response.ok) {
        if (isLogin) {
          onLoginSuccess(data.token);
        } else {
          alert("Cadastro feito! Agora faça login.");
          setIsLogin(true);
        }
      } else {
        alert(`Erro: ${data.detail || 'Erro ao autenticar'}`);
      }
    } catch (error) {
      alert("Erro na requisição.");
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">{isLogin ? "Login" : "Cadastro"}</h2>
        <div className="space-y-4">
          {!isLogin && (
            <>
              <input type="text" placeholder="Nome" value={name} onChange={e => setName(e.target.value)} className="border w-full px-4 py-2 rounded" />
              <input type="text" placeholder="Tipo de criador" value={creatorType} onChange={e => setCreatorType(e.target.value)} className="border w-full px-4 py-2 rounded" />
            </>
          )}
          <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="border w-full px-4 py-2 rounded" />
          <input type="password" placeholder="Senha" value={password} onChange={e => setPassword(e.target.value)} className="border w-full px-4 py-2 rounded" />
          <div className="flex justify-between">
            <button onClick={handleSubmit} className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
              {isLogin ? "Entrar" : "Cadastrar"}
            </button>
            <button onClick={() => setIsLogin(!isLogin)} className="text-blue-600 hover:underline">
              {isLogin ? "Criar conta" : "Já tenho conta"}
            </button>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-sm mt-2">Fechar</button>
        </div>
      </div>
    </div>
  );
}
