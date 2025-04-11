const API_URL = "http://localhost:8000"; // Muda aqui se o backend estiver hospedado em outro lugar

function showPage(pageId) {
  document.querySelectorAll('.page').forEach(page => {
    page.classList.add('hidden');
  });
  document.getElementById(pageId).classList.remove('hidden');
  document.getElementById(pageId).classList.add('active');
}

async function register() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

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
}

async function login() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await response.json();
  if (response.ok) {
    alert("Login feito com sucesso!");
    localStorage.setItem("token", data.token); // Salva o token
  } else {
    alert(`Erro: ${data.detail || 'Não foi possível fazer login.'}`);
  }
}

async function uploadFile() {
  const fileInput = document.getElementById('file');
  const filenameInput = document.getElementById('filename');
  const file = fileInput.files[0];
  const name = filenameInput.value;

  if (!file || !name) {
    alert("Selecione um arquivo e dê um nome!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("name", name);

  const token = localStorage.getItem("token");
  if (!token) {
    alert("Você precisa estar logado para fazer upload.");
    return;
  }

  const response = await fetch(`${API_URL}/files/upload`, {
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
}

async function listCertificates() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Faça login primeiro!");
    return;
  }

  const response = await fetch(`${API_URL}/certificates/list`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const data = await response.json();
  const listDiv = document.getElementById('certificates-list');
  listDiv.innerHTML = "";

  if (response.ok) {
    if (data.length === 0) {
      listDiv.innerHTML = "<p class='text-gray-500'>Nenhum certificado encontrado.</p>";
      return;
    }
    
    data.forEach(cert => {
      const certCard = document.createElement('div');
      certCard.className = "bg-white shadow-md p-4 rounded-lg mb-4";
      certCard.innerHTML = `
        <p><strong>Nome:</strong> ${cert.name}</p>
        <p><strong>Hash:</strong> ${cert.hash}</p>
        <p><strong>Data:</strong> ${new Date(cert.timestamp * 1000).toLocaleString()}</p>
        <button onclick="generateCertificate('${cert.hash}')" class="mt-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
          Visualizar Certificado
        </button>
      `;
      listDiv.appendChild(certCard);
    });
  } else {
    listDiv.innerHTML = `<p class="text-red-500">Erro ao carregar certificados: ${data.detail || 'Erro desconhecido'}</p>`;
  }
}

async function generateCertificate(hash) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Faça login primeiro!");
    return;
  }

  // Aqui pode ser GET, depende como você fez no backend
  const response = await fetch(`${API_URL}/certificates/view/${hash}`, {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  if (response.ok) {
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    window.open(url, "_blank");
  } else {
    const data = await response.json();
    alert(`Erro: ${data.detail || 'Não foi possível gerar certificado'}`);
  }
}
function showPage(pageId) {
  document.querySelectorAll('.page').forEach(page => {
    page.classList.add('hidden');
    page.classList.remove('active'); // <-- adicionado para limpar a active antiga
  });
  const pageToShow = document.getElementById(pageId);
  pageToShow.classList.remove('hidden');
  pageToShow.classList.add('active');
}

