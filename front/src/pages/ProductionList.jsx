import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import { API_URL } from "../../config";

export default function ProductionsList() {
  const [productions, setProductions] = useState([]);
  const token = localStorage.getItem("token");

  useEffect(() => {
    async function fetchProductions() {
      try {
        const response = await fetch(`${API_URL}/productions/list`, {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setProductions(data);
        } else {
          alert(`Erro: ${data.detail || "Erro ao listar produções"}`);
        }
      } catch {
        alert("Erro na requisição");
      }
    }
    fetchProductions();
  }, [token]);

  return (
    <section className="max-w-6xl mx-auto p-8 grid grid-cols-2 md:grid-cols-4 gap-6">
      {productions.map(prod => (
        <Link key={prod.id} to={`/producao/${prod.id}`} className="bg-white rounded-xl shadow-md overflow-hidden hover:scale-105 transition-transform">
          <img src={`https://via.placeholder.com/300x400?text=${encodeURIComponent(prod.title)}`} alt={prod.title} className="w-full h-48 object-cover" />
          <div className="p-4">
            <h3 className="font-bold text-lg">{prod.title}</h3>
            <p className="text-gray-500 text-sm mt-1">{prod.description.slice(0, 60)}...</p>
          </div>
        </Link>
      ))}
    </section>
  );
}
