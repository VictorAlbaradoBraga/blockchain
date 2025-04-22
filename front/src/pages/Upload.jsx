import { useState } from "react";
import { API_URL } from "../../config";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState('');
  const [description, setDescription] = useState('');
  const token = localStorage.getItem("token");

  async function uploadFile() {
    if (!file || !filename || !description) {
      alert("Selecione um arquivo, dê um nome e uma descrição!");
      return;
    }

    if (!token) {
      alert("Você precisa estar logado para fazer upload.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("title", filename); // Envia o nome do arquivo como título
    formData.append("description", description); // Envia a descrição

    try {
      console.log(formData)
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`
        },
          
        body: formData
      });

      const data = await response.json();
      if (response.ok) {
        alert("Arquivo enviado e registrado na blockchain!");
      } else {
        alert(`Erro: ${data.detail || 'Falha ao enviar arquivo.'}`);
      }
    } catch {
      console.error("Erro na requisição: ", error); // Captura e imprime o erro
      alert("Erro na requisição");
    }
  }

  return (
    <section>
      <h2 className="text-xl font-semibold mb-4">Upload de Arquivo</h2>
      <div className="space-y-4">
        <input 
          type="file" 
          onChange={e => setFile(e.target.files[0])} 
          className="border border-gray-300 rounded px-4 py-2 w-full" 
        />
        <input 
          type="text" 
          placeholder="Nome da obra" 
          value={filename} 
          onChange={e => setFilename(e.target.value)} 
          className="border border-gray-300 rounded px-4 py-2 w-full" 
        />
        <textarea 
          placeholder="Descrição da obra" 
          value={description} 
          onChange={e => setDescription(e.target.value)} 
          className="border border-gray-300 rounded px-4 py-2 w-full" 
        />
        <button 
          onClick={uploadFile} 
          className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded"
        >
          Enviar
        </button>
      </div>
    </section>
  );
}
