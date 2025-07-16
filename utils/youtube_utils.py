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

#
# import os, re, subprocess
# import webvtt
# from difflib import SequenceMatcher
# from youtube_transcript_api import YouTubeTranscriptApi
# import streamlit as st
#
# AMBIENTE = st.secrets.get("ambiente", "local")
#
# def limpar_trechos_sem_repeticoes(trechos):
#     texto_limpo, ultimo_trecho = [], ""
#     for t in trechos:
#         trecho = re.sub(r'\s+', ' ', t["text"].strip())
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
# def processar_legenda_vtt(vtt_file_path):
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
#     if not url:
#         return ""
#
#     clean_url = url.split("&")[0]
#
#     if AMBIENTE == "local":
#         try:
#             for f in os.listdir():
#                 if f.endswith(".vtt"):
#                     os.remove(f)
#
#             subprocess.run(
#                 f'yt-dlp --write-auto-sub --sub-lang "pt" --skip-download --output "legenda.%(ext)s" "{clean_url}"',
#                 shell=True,
#                 check=True
#             )
#
#             vtt_name = next((f for f in os.listdir() if f.endswith(".vtt")), None)
#             if not vtt_name:
#                 st.warning("⚠️ Legenda automática não encontrada.")
#                 return ""
#
#             texto = processar_legenda_vtt(vtt_name)
#             os.remove(vtt_name)
#             return texto
#
#         except Exception as e:
#             st.error(f"❌ Erro ao processar localmente: {e}")
#             return ""
#
#     else:
#         try:
#             video_id = clean_url.split("v=")[-1]
#             transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["pt", "pt-BR"])
#             texto = limpar_trechos_sem_repeticoes(transcript)
#             return texto
#         except Exception as e:
#             st.warning(f"⚠️ Legenda automática não disponível: {e}")
#             return ""

import streamlit as st
import os, re
from difflib import SequenceMatcher

# Versão cloud usa youtube_transcript_api (sem yt-dlp)
try:
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
    TRANSCRIPT_API_OK = True
except ImportError:
    TRANSCRIPT_API_OK = False


def processar_legenda_sem_repeticoes(trechos):
    texto_limpo, ultimo_trecho = [], ""
    for trecho in trechos:
        texto = re.sub(r'\s+', ' ', trecho.strip())
        palavras_prev, palavras_curr = ultimo_trecho.split(), texto.split()
        for n in range(min(len(palavras_prev), len(palavras_curr), 10), 0, -1):
            if palavras_prev[-n:] == palavras_curr[:n]:
                texto = " ".join(palavras_curr[n:]).strip()
                break
        if not texto or SequenceMatcher(None, ultimo_trecho, texto).ratio() > 0.9:
            continue
        texto_limpo.append(texto)
        ultimo_trecho = texto
    return "\n\n".join(re.split(r'(?<=[.!?]) +', " ".join(texto_limpo).strip()))[:15000]


def extrair_id_video(url):
    import re
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    return match.group(1) if match else None


def processar_youtube():
    st.subheader("🎥 Processador de Vídeo YouTube")
    url = st.text_input("Cole a URL do vídeo do YouTube:")
    if not url:
        return ""

    ambiente = st.secrets.get("ambiente", "local")
    video_id = extrair_id_video(url)

    if ambiente == "cloud" and TRANSCRIPT_API_OK:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
            trechos = [t['text'] for t in transcript]
            texto = processar_legenda_sem_repeticoes(trechos)
            return texto
        except (TranscriptsDisabled, NoTranscriptFound):
            st.warning("⚠️ Legenda automática não disponível para este vídeo.")
        except Exception as e:
            st.error(f"❌ Erro ao buscar legenda com API: {e}")
        return ""

    else:
        try:
            import subprocess, webvtt

            # Limpa arquivos .vtt
            for f in os.listdir():
                if f.endswith(".vtt"):
                    os.remove(f)

            # Baixa legenda automática
            subprocess.run(
                f'yt-dlp --write-auto-sub --sub-lang "pt" --skip-download --output "legenda.%(ext)s" "{url}"',
                shell=True,
                check=True
            )

            vtt_file = next((f for f in os.listdir() if f.endswith(".vtt")), None)
            if not vtt_file:
                st.warning("⚠️ Legenda automática não encontrada.")
                return ""

            trechos = [cap.text.strip() for cap in webvtt.read(vtt_file)]
            texto = processar_legenda_sem_repeticoes(trechos)
            os.remove(vtt_file)
            return texto

        except subprocess.CalledProcessError as e:
            st.error(f"❌ yt-dlp falhou: {e}")
        except Exception as e:
            st.error(f"❌ Erro inesperado: {e}")
        return ""