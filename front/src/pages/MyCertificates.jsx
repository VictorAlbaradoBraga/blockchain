import { useState, useEffect } from "react";
import { API_URL } from "../../config";
import ProductionList from "./ProductionList"; // Certifique-se de que o componente ProductionList é usado para exibir os produtos.

export default function MyCertificates() {
  const [myProductions, setMyProductions] = useState([]);
  const token = localStorage.getItem("token");

  useEffect(() => {
    async function fetchMyProductions() {
      try {
        const response = await fetch(`${API_URL}/productions/my-list`, {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (response.ok) {
          setMyProductions(data);
        } else {
          alert(`Erro: ${data.detail || "Erro ao obter produções"}`);
        }
      } catch {
        alert("Erro na requisição");
      }
    }
    fetchMyProductions();
  }, [token]);

  return (
    <section className="max-w-6xl mx-auto p-8">
      <h2 className="text-3xl font-bold mb-4">Minhas Produções</h2>
      <ProductionList productions={myProductions} />
    </section>
  );
}
