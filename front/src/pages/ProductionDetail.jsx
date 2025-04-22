import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

import { API_URL } from "../../config";

export default function ProductionDetail() {
  const { id } = useParams();
  const [production, setProduction] = useState(null);
  const token = localStorage.getItem("token");

  useEffect(() => {
    async function fetchProduction() {
      try {
        const response = await fetch(`${API_URL}/production/${id}`, {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setProduction(data);
        } else {
          alert(`Erro: ${data.detail || "Erro ao obter detalhes da produção"}`);
        }
      } catch {
        alert("Erro na requisição");
      }
    }
    fetchProduction();
  }, [id, token]);

  if (!production) return <p>Carregando...</p>;

  return (
    <section className="max-w-4xl mx-auto p-8">
      <img src={`https://via.placeholder.com/800x400?text=${encodeURIComponent(production.title)}`} alt={production.title} className="w-full h-64 object-cover rounded-lg mb-6" />
      <h2 className="text-3xl font-bold mb-4">{production.title}</h2>
      <p className="text-gray-700 mb-6">{production.description}</p>
      <p className="text-gray-500 text-sm">Criador: {production.creator_email}</p>
      <button disabled className="mt-6 bg-green-500 text-white font-bold px-6 py-3 rounded-lg opacity-50 cursor-not-allowed">
        Comprar (Em breve)
      </button>
    </section>
  );
}
