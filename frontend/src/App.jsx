import { useState } from "react";
import Header from "./components/Header";
import Main from "./components/Main";

const API_URL = import.meta.env.VITE_API_URL || "https://cut-hunter.onrender.com/analisar";

function extrairIdVideo(url) {
  const regex = /(?:youtube\.com\/(?:watch\?v=|live\/|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/; // Expressão regular para capturar o ID do vídeo do YouTube
  const match = url.trim().match(regex); // Tenta encontrar uma correspondência na URL fornecida
  return match ? match[1] : url.trim(); // Retorna o ID do vídeo se encontrado, caso contrário retorna a URL original
}

function formatarTempo(segundosTotais) {
  const horas = Math.floor(segundosTotais / 3600);
  const minutos = Math.floor((segundosTotais % 3600) / 60);
  const segundos = segundosTotais % 60;

  const mm = String(minutos).padStart(2, "0");
  const ss = String(segundos).padStart(2, "0");

  return horas > 0 ? `${horas}:${mm}:${ss}` : `${mm}:${ss}`;
}

export default function App() {
  const [url, setUrl] = useState("");
  const [videoId, setVideoId] = useState("");
  const [cortes, setCortes] = useState([]);
  const [segundoAtivo, setSegundoAtivo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [copiadoIndex, setCopiadoIndex] = useState(null);

  async function handleBuscarCortes(e) {
    e.preventDefault(); // Evita que o formulário seja enviado e a página seja recarregada
    if (!url.trim()) return; // Evita enviar uma URL vazia

    setLoading(true); // Inicia o estado de carregamento
    setErro(""); // Limpa qualquer erro anterior
    setCortes([]); // Limpa os cortes anteriores
    setSegundoAtivo(null); // Limpa o segundo ativo

    try {
      const resposta = await fetch(`${API_URL}?url=${encodeURIComponent(url.trim())}`); // Faz a requisição para a API com a URL do vídeo
      const textoResposta = await resposta.text();

      let dados;
      try {
        dados = JSON.parse(textoResposta);
      } catch {
        throw new Error("O servidor ainda está acordando ou retornou uma resposta inválida. Tente novamente em alguns segundos.");
      }
      if (!resposta.ok) {
        throw new Error(dados.detail || "Erro ao analisar o vídeo.");
      }

      setVideoId(extrairIdVideo(url)); // Extrai o ID do vídeo da URL e atualiza o estado
      setCortes(dados.cortes); // Atualiza o estado com os cortes retornados pela API
    } catch (err) {
      setErro(err.message); // Atualiza o estado de erro com a mensagem do erro
    } finally {
      setLoading(false); //  Finaliza o estado de carregamento
    }
  }

  function copiarTitulo(e, titulo, index) {
    e.stopPropagation();
    navigator.clipboard.writeText(titulo);
    setCopiadoIndex(index);
    setTimeout(() => setCopiadoIndex(null), 2000);
  }

  const playerSrc = videoId
    ? `https://www.youtube.com/embed/${videoId}${
        segundoAtivo !== null ? `?start=${segundoAtivo}&autoplay=1` : ""
      }`
    : "";

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 pb-12 font-sans">
   
      <Header 
        handleBuscarCortes={handleBuscarCortes} 
        url={url} 
        setUrl={setUrl} 
        loading={loading}
      />

      
      <Main 
        loading={loading}
        erro={erro}
        cortes={cortes}
        segundoAtivo={segundoAtivo}
        setSegundoAtivo={setSegundoAtivo}
        copiarTitulo={copiarTitulo}
        copiadoIndex={copiadoIndex}
        playerSrc={playerSrc}
        formatarTempo={formatarTempo}
      />
    </div>
  );
}