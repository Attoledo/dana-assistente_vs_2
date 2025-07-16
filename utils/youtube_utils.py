# import streamlit as st
# import subprocess, os, re, webvtt
# from difflib import SequenceMatcher
#
# def processar_legenda_sem_repeticoes(vtt_file_path):
#     texto_limpo, ultimo_trecho = [], ""
#     for cap in webvtt.read(vtt_file_path):
#         trecho = re.sub(r'\s+', ' ', cap.text.strip())
#         palavras_prev, palavras_curr = ultimo_trecho.split(), trecho.split()
#         for n in range(min(len(palavras_prev), len(palavras_curr), 10), 0, -1):
#             if palavras_prev[-n:] == palavras_curr[:n]:
#                 trecho = " ".join(palavras_curr[n:]).strip()
#                 break
#         if not trecho or SequenceMatcher(None, ultimo_trecho, trecho).ratio() > 0.9:
#             continue
#         texto_limpo.append(trecho)
#         ultimo_trecho = trecho
#     texto = " ".join(texto_limpo)
#     return "\n\n".join(re.split(r'(?<=[.!?]) +', texto.strip()))[:15000]
#
# def processar_youtube():
#     st.subheader("🎥 Processador de Vídeo YouTube")
#     url = st.text_input("Cole a URL do vídeo do YouTube:")
#     if url:
#         try:
#             clean_url = url.split("&")[0]
#
#             # 🧹 Limpa arquivos .vtt antigos
#             for f in os.listdir():
#                 if f.endswith(".vtt"):
#                     os.remove(f)
#
#             # 🛠️ Tenta baixar legendas automáticas (português ou inglês como fallback)
#             subprocess.run(
#                 f'yt-dlp --write-auto-sub --sub-lang "pt" --skip-download --output "legenda.%(ext)s" "{clean_url}"',
#                 shell=True,
#                 check=True
#             )
#
#             # 🔎 Busca qualquer .vtt disponível
#             vtt_name = next((f for f in os.listdir() if f.endswith(".vtt")), None)
#
#             if not vtt_name:
#                 st.warning("⚠️ Legenda automática não encontrada para este vídeo. Tente outro link.")
#                 return ""
#
#             # ✅ Processa e retorna o texto limpo
#             texto = processar_legenda_sem_repeticoes(vtt_name)
#             os.remove(vtt_name)
#             return texto
#
#         except subprocess.CalledProcessError as e:
#             st.error(f"❌ yt-dlp falhou ao baixar a legenda: {e}")
#         except Exception as e:
#             st.error(f"❌ Erro inesperado: {e}")
#     return ""
#


import os, re, subprocess
import webvtt
from difflib import SequenceMatcher
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st

AMBIENTE = st.secrets.get("ambiente", "local")

def limpar_trechos_sem_repeticoes(trechos):
    texto_limpo, ultimo_trecho = [], ""
    for t in trechos:
        trecho = re.sub(r'\s+', ' ', t["text"].strip())
        palavras_prev, palavras_curr = ultimo_trecho.split(), trecho.split()
        for n in range(min(len(palavras_prev), len(palavras_curr), 10), 0, -1):
            if palavras_prev[-n:] == palavras_curr[:n]:
                trecho = " ".join(palavras_curr[n:]).strip()
                break
        if not trecho or SequenceMatcher(None, ultimo_trecho, trecho).ratio() > 0.9:
            continue
        texto_limpo.append(trecho)
        ultimo_trecho = trecho
    texto = " ".join(texto_limpo)
    return "\n\n".join(re.split(r'(?<=[.!?]) +', texto.strip()))[:15000]

def processar_legenda_vtt(vtt_file_path):
    texto_limpo, ultimo_trecho = [], ""
    for cap in webvtt.read(vtt_file_path):
        trecho = re.sub(r'\s+', ' ', cap.text.strip())
        palavras_prev, palavras_curr = ultimo_trecho.split(), trecho.split()
        for n in range(min(len(palavras_prev), len(palavras_curr), 10), 0, -1):
            if palavras_prev[-n:] == palavras_curr[:n]:
                trecho = " ".join(palavras_curr[n:]).strip()
                break
        if not trecho or SequenceMatcher(None, ultimo_trecho, trecho).ratio() > 0.9:
            continue
        texto_limpo.append(trecho)
        ultimo_trecho = trecho
    texto = " ".join(texto_limpo)
    return "\n\n".join(re.split(r'(?<=[.!?]) +', texto.strip()))[:15000]

def processar_youtube():
    st.subheader("🎥 Processador de Vídeo YouTube")
    url = st.text_input("Cole a URL do vídeo do YouTube:")
    if not url:
        return ""

    clean_url = url.split("&")[0]

    if AMBIENTE == "local":
        try:
            for f in os.listdir():
                if f.endswith(".vtt"):
                    os.remove(f)

            subprocess.run(
                f'yt-dlp --write-auto-sub --sub-lang "pt" --skip-download --output "legenda.%(ext)s" "{clean_url}"',
                shell=True,
                check=True
            )

            vtt_name = next((f for f in os.listdir() if f.endswith(".vtt")), None)
            if not vtt_name:
                st.warning("⚠️ Legenda automática não encontrada.")
                return ""

            texto = processar_legenda_vtt(vtt_name)
            os.remove(vtt_name)
            return texto

        except Exception as e:
            st.error(f"❌ Erro ao processar localmente: {e}")
            return ""

    else:
        try:
            video_id = clean_url.split("v=")[-1]
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["pt", "pt-BR"])
            texto = limpar_trechos_sem_repeticoes(transcript)
            return texto
        except Exception as e:
            st.warning(f"⚠️ Legenda automática não disponível: {e}")
            return ""