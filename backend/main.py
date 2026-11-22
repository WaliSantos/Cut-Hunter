# coracao do servidor python:
# codigo que recebe o link do video
# busca a legenda no youtube
# conversa com a IA
# devolve os cortes prontos


import os
import time
import logging
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from google import genai
from google.genai import types
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi 

logging.basicConfig(level=logging.INFO)

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

    texto: str
# instanciando o cliente da API da GenAI com a chave de API do arquivo .env
client = genai.Client() 

def extrair_id_video(url_ou_id: str) -> str:

    texto = url_ou_id.strip() # removendo espaços em branco do início e do fim da string
    if "http" not in texto: 
        return texto

    parsed = urlparse(texto) # parseando a url para extrair o id do vídeo

    if parsed.hostname in ("www.youtu.be", "youtu.be"):
        return parsed.path.lstrip("/")
    if "/live" in parsed.path or "/shorts" in parsed.path:
        return parsed.path.rstrip("/").split("/")[-1]

    return parse_qs(parsed.query).get("v", [texto])[0] 

def buscar_transcricao(video_id: str) -> list[dict]:
    """
    Se houver SUPADATA_API_KEY (no Render), usa a Supadata para evitar bloqueio de IP.
    Caso contrário (no PC local), usa a youtube-transcript-api gratuitamente.
    """
    supadata_key = os.getenv("SUPADATA_API_KEY") # pega a chave da Supadata do arquivo .env

    if supadata_key:
        url_limpa = f"https://www.youtube.com/watch?v={video_id}" # cria a url limpa do vídeo para enviar para a Supadata
        resp = requests.get(
            "https://api.supadata.ai/v1/transcript",
            params={"url": url_limpa, "lang": "pt"},
            headers={"x-api-key": supadata_key},
            timeout=30,
        ) # faz a requisição para a Supadata para buscar a transcrição do vídeo
        resp.raise_for_status() # levanta uma exceção se a requisição falhar
        dados = resp.json() # pega o conteúdo da resposta em formato JSON

        conteudo = dados.get("content", []) # pega o conteúdo da transcrição do vídeo, que é uma lista de dicionários com 'offset' e 'text'
        if not isinstance(conteudo, list): # garante que o conteúdo seja uma lista; se não for, retorna uma lista vazia
            return []

        # A Supadata envia 'offset' em milissegundos; dividimos por 1000 para virar segundos
        return [
            {"start": int(item["offset"] / 1000), "text": item["text"]}
            for item in conteudo
        ]

    # Modo local 
    ytt = YouTubeTranscriptApi()
    transcript = ytt.fetch(video_id, languages=["pt", "pt-BR"])
    return [{"start": int(trecho.start), "text": trecho.text} for trecho in transcript]

def chamar_gemini_com_fallback(prompt: str):
    modelos_tentativa = ["gemini-3.8-flash"]

    # Descobre automaticamente outros modelos Flash ativos na sua conta como reserva
    try:
        for m in client.models.list():
            nome = m.name.replace("models/", "")
            if (
                "flash" in nome
                and nome not in modelos_tentativa
                and not any(x in nome for x in ["2.5", "2.0", "1.5", "image", "audio", "tts", "live"])
            ):
                modelos_tentativa.append(nome)
    except Exception:
        pass

    ultimo_erro = None
    for modelo in modelos_tentativa:
        try:
            logging.info(f"Tentando gerar cortes com: {modelo}")
            config_kwargs = {
                "response_mime_type": "application/json",
                "response_schema": ListaDeCortes,
            }
            if "3." in modelo:
                config_kwargs["thinking_config"] = {"thinking_level": "LOW"}

            resposta = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(**config_kwargs),
            )
            logging.info(f"Sucesso com o modelo: {modelo}")
            return resposta
        except Exception as erro:
            ultimo_erro = erro
            logging.warning(f" Modelo {modelo} falhou ou está congestionado. Tentando próximo...")
            continue

    raise ultimo_erro

@app.get("/analisar", response_model=ListaDeCortes)
def analisar_video(url: str):
    inicio_total = time.perf_counter()
    video_id = extrair_id_video(url) # extraindo o id do vídeo 

    try: 
        t0 = time.perf_counter()
        # ytt = YouTubeTranscriptApi() # instanciando a API de transcrição do YouTube
        # transcript = ytt.fetch(video_id, languages=["pt", "pt-BR"]) 

        trechos = buscar_transcricao(video_id) # buscando a transcrição do vídeo

        logging.info(f"Busca da legenda levou: {time.perf_counter() - t0:.2f}s")
    except Exception as erro:
        logging.error(f"Falha ao buscar legenda ({video_id}): {erro}")
        raise HTTPException(
            status_code = 400,
            detail = f"Não foi possível obter a legenda deste vídeo. Verifique se é público e possui legendas"
        )
    if not trechos:
        raise HTTPException(
            status_code=400,
            detail="A transcrição veio vazia para este vídeo."
        )
    
    # linhas = [f"[{int(trecho.start)}s] {trecho.text}" for trecho in transcript]
    # texto_completo = "\n".join(linhas)

    blocos = []
    texto_atual = []
    inicio_bloco = None

    for trecho in trechos:
        if inicio_bloco is None:
            inicio_bloco = trecho["start"]
        texto_atual.append(trecho["text"].strip())

        if trecho["start"] - inicio_bloco >= 60:
            blocos.append(f"[{inicio_bloco}s] {' '.join(texto_atual)}")
            texto_atual = []
            inicio_bloco = None

    if texto_atual and inicio_bloco is not None:
        blocos.append(f"[{inicio_bloco}s] {' '.join(texto_atual)}")

    texto_completo = "\n".join(blocos)


    prompt = f"""
        Você é um editor sênior de cortes para o canal 'Canto Rubro-Negro', focado no Esporte Clube Vitória.
        Analise a transcrição abaixo (com marcações de tempo em segundos) e selecione os 5 melhores momentos para virarem Shorts/Reels, cortes para o YouTube ou instagram.

        Contexto para corrigir erros da legenda automática:
        - O clube é o EC Vitória (Leão, Rubro-Negro, Colossal), estádio Barradão, rival Bahia (Ba-Vi).
        - Priorize momentos de opinião forte, polêmicas de arbitragem, análises táticas claras, desabafos da torcida ou momentos engraçados.
        - Escolha o 'segundo_inicio' alguns segundos ANTES da frase principal começar, para dar contexto ao corte.
        - Classifique a 'categoria' apenas como: Polêmica, Análise Tática, Resenha ou Desabafo.

        Transcrição da live:
        {texto_completo[:60000]}
        """

    try:
        t1 = time.perf_counter()
        # resposta = client.models.generate_content(
        #     model="gemini-3.8-flash",
        #     contents=prompt,
        #     config=types.GenerateContentConfig(
        #         response_mime_type="application/json",
        #         response_schema=ListaDeCortes,
        #         thinking_config={"thinking_level": "LOW"}),
        # )
        resposta = chamar_gemini_com_fallback(prompt)
        print(f"Gemini levou: {time.perf_counter() - t1:.2f}s")
        print(f"Tempo total: {time.perf_counter() - inicio_total:.2f}s")
        print(f"Tokens usados: {resposta.usage_metadata}")
        return resposta.parsed
    except Exception as erro:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar análise com a IA: {str(erro)}" )