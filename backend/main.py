# coracao do servidor python:
# codigo que recebe o link do video
# busca a legenda no youtube
# conversa com a IA
# devolve os cortes prontos

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from google import genai
from google.genai import types
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi 

load_dotenv() # carregando o arquivo .env para memória do sistema

app = FastAPI(title="Caçador de Cortes") # instanciando o servidor FastAPI com o nome do projeto

# Configuração do CORS para permitir requisições de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],)

# Definição dos modelos de dados para não quebrar o frontend, usando Pydantic 
class Corte(BaseModel):
    segundo_inicio: int
    titulo_sugerido: str
    categoria: str
    motivo: str

class ListaDeCortes(BaseModel):
    cortes: list[Corte]

# instanciando o cliente da API da GenAI com a chave de API do arquivo .env
client = genai.Client() 

def extrair_id_video(url_ou_id: str) -> str:

    texto = url_ou_id.strip() # removendo espaços em branco do início e do fim da string
    if "http" not in texto: 
        return texto

    parsed = urlparse(texto) # parseando a url para extrair o id do vídeo

    if parsed.hostname in ("www.youtube.be", "youtube.be"):
        return parsed.path.lstrip("/")
    if "/live" in parsed.path or "/shorts" in parsed.path:
        return parsed.path.rstrip("/").split("/")[-1]

    return parse_qs(parsed.query).get("v", [texto])[0] 

@app.get("/analisar", response_model=ListaDeCortes)
def analisar_video(url: str):
    video_id = extrair_id_video(url) # extraindo o id do vídeo 

    try: 
        ytt = YouTubeTranscriptApi() # instanciando a API de transcrição do YouTube
        transcript = ytt.fetch(video_id, languages=["pt"])
    except Exception as erro:
        raise HTTPException(
            status_code = 400,
            detail = f"Não foi possível obter a legenda..."
        )
    
    linhas = [f"[{int(trecho.start)}s] {trecho.text}" for trecho in transcript]
    texto_completo = "\n".join(linhas)

    prompt = f"""
        Você é um editor sênior de cortes para o canal 'Canto Rubro-Negro', focado no Esporte Clube Vitória.
        Analise a transcrição abaixo (com marcações de tempo em segundos) e selecione os 10 melhores momentos para virarem Shorts/Reels, cortes para o YouTube ou instagram.

        Contexto para corrigir erros da legenda automática:
        - O clube é o EC Vitória (Leão, Rubro-Negro, Colossal), estádio Barradão, rival Bahia (Ba-Vi).
        - Priorize momentos de opinião forte, polêmicas de arbitragem, análises táticas claras, desabafos da torcida ou momentos engraçados.
        - Escolha o 'segundo_inicio' alguns segundos ANTES da frase principal começar, para dar contexto ao corte.
        - Classifique a 'categoria' apenas como: Polêmica, Análise Tática, Resenha ou Desabafo.

        Transcrição da live:
        {texto_completo[:100000]}
        """

    try:
        resposta = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ListaDeCortes,
            ),
        )
        return resposta.parsed
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar análise com a IA: {str(erro)}" )