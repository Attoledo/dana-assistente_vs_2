#
# import streamlit as st
# from utils.pdf_utils import carregar_pdf
# from utils.youtube_utils import processar_youtube
# from utils.site_utils import carregar_site
# from chat.assistente_dana import (
#     iniciar_assistente,
#     gerar_resumo,
#     salvar_como_pdf,
#     salvar_como_txt,
# )
# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
#
# # streamlit run main.py
#
# # ─────────────────── 1. Configuração e modelo ───────────────────
# load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# if not api_key or not api_key.startswith("gsk_"):
#     st.error("❌ API Key inválida ou ausente. Verifique o arquivo .env.")
#     st.stop()
#
# os.environ["GROQ_API_KEY"] = api_key
# chat = ChatGroq(model="llama3-70b-8192")
#
# st.set_page_config(page_title="Assistente Dana", page_icon="🦙")
# st.title("Dana, seu Assistente Pessoal 😎")
#
# # ─────────────────── 2. Estados de sessão ───────────────────
# if "doc_texto" not in st.session_state:
#     st.session_state.doc_texto = ""
# if "mostrar_assistente" not in st.session_state:
#     st.session_state.mostrar_assistente = False
#
# # ─────────────────── 3. Escolha da fonte ───────────────────
# opcao = st.sidebar.selectbox(
#     "Escolha a fonte de conteúdo:", ["PDF", "YouTube", "Site"]
# )
#
# if opcao == "PDF":
#     st.session_state.doc_texto = carregar_pdf()
# elif opcao == "YouTube":
#     st.session_state.doc_texto = processar_youtube()
# elif opcao == "Site":
#     st.session_state.doc_texto = carregar_site()
#
# # ─────────────────── 4. Se carregou, habilita assistente ───────────────────
# if st.session_state.doc_texto and not st.session_state.mostrar_assistente:
#     st.session_state.mostrar_assistente = True
#
# # ─────────────────── 5. Botões de download e resumo ───────────────────
# if st.session_state.doc_texto:
#     # Salva arquivos
#     salvar_como_txt(st.session_state.doc_texto, "transcricao_formatada.txt")
#     salvar_como_pdf(st.session_state.doc_texto, "transcricao_formatada.pdf")
#
#     # Botões de download
#     st.download_button(
#         "📄 Baixar TXT",
#         data=st.session_state.doc_texto,
#         file_name="transcricao_formatada.txt",
#     )
#     with open("transcricao_formatada.pdf", "rb") as f:
#         st.download_button(
#             "📄 Baixar PDF", data=f, file_name="transcricao_formatada.pdf"
#         )
#
#     # Botão Gerar Resumo (opcional)
#     if st.sidebar.button("Gerar Resumo"):
#         resumo = gerar_resumo(chat, st.session_state.doc_texto)
#         st.markdown("## 📝 Resumo do Conteúdo")
#         st.markdown(resumo)
#
#         salvar_como_txt(resumo, "resumo.txt")
#         salvar_como_pdf(resumo, "resumo.pdf")
#
#         st.download_button(
#             "📄 Baixar Resumo (.txt)", data=resumo, file_name="resumo.txt"
#         )
#         with open("resumo.pdf", "rb") as f:
#             st.download_button(
#                 "📄 Baixar Resumo (.pdf)", data=f, file_name="resumo.pdf"
#             )
#
# # ─────────────────── 6. Inicia o chat da DANA ───────────────────
# if st.session_state.mostrar_assistente:
#     iniciar_assistente(chat, st.session_state.doc_texto)
# else:
#     st.info("📄 Carregue um PDF, URL de YouTube ou Site para conversar com a DANA.")
#
#

# main.py
import streamlit as st
from utils.pdf_utils import carregar_pdf
from utils.youtube_utils import processar_youtube
from utils.site_utils import carregar_site
from chat.assistente_dana import (
    iniciar_assistente,
    gerar_resumo,
    salvar_como_pdf,
    salvar_como_txt,
)
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# ─────────────────── 1. Configuração e modelo ───────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key or not api_key.startswith("gsk_"):
    st.error("❌ API Key inválida ou ausente. Verifique o arquivo .env.")
    st.stop()

os.environ["GROQ_API_KEY"] = api_key
chat = ChatGroq(model="llama3-70b-8192")

st.set_page_config(page_title="Assistente Dana", page_icon="🦙")
st.title("Dana, seu Assistente Pessoal 😎")

# ─────────────────── 2. Estados de sessão ───────────────────
if "doc_texto" not in st.session_state:
    st.session_state.doc_texto = ""
if "mostrar_assistente" not in st.session_state:
    st.session_state.mostrar_assistente = False

# ─────────────────── 3. Escolha da fonte ───────────────────
opcao = st.sidebar.selectbox(
    "Escolha a fonte de conteúdo:", ["PDF", "YouTube", "Site"]
)

if opcao == "PDF":
    st.session_state.doc_texto = carregar_pdf()
elif opcao == "YouTube":
    st.session_state.doc_texto = processar_youtube()
elif opcao == "Site":
    st.session_state.doc_texto = carregar_site()

# ─────────────────── 4. Se carregou, habilita assistente ───────────────────
if st.session_state.doc_texto and not st.session_state.mostrar_assistente:
    st.session_state.mostrar_assistente = True

# ─────────────────── 5. Botões de download e resumo ───────────────────
if st.session_state.doc_texto:
    salvar_como_txt(st.session_state.doc_texto, "transcricao_formatada.txt")
    salvar_como_pdf(st.session_state.doc_texto, "transcricao_formatada.pdf")

    st.download_button(
        "📄 Baixar TXT",
        data=st.session_state.doc_texto,
        file_name="transcricao_formatada.txt",
    )
    with open("transcricao_formatada.pdf", "rb") as f:
        st.download_button(
            "📄 Baixar PDF", data=f, file_name="transcricao_formatada.pdf"
        )

    if st.sidebar.button("Gerar Resumo"):
        resumo = gerar_resumo(chat, st.session_state.doc_texto)
        st.markdown("## 📝 Resumo do Conteúdo")
        st.markdown(resumo)

        salvar_como_txt(resumo, "resumo.txt")
        salvar_como_pdf(resumo, "resumo.pdf")

        st.download_button(
            "📄 Baixar Resumo (.txt)", data=resumo, file_name="resumo.txt"
        )
        with open("resumo.pdf", "rb") as f:
            st.download_button(
                "📄 Baixar Resumo (.pdf)", data=f, file_name="resumo.pdf"
            )

# ─────────────────── 6. Inicia o chat da DANA ───────────────────
if st.session_state.mostrar_assistente:
    iniciar_assistente(chat, st.session_state.doc_texto)

    # Botão para exportar histórico de conversa
    if st.sidebar.button("💾 Baixar histórico (.txt)"):
        conteudo = ""
        for msg in st.session_state.chat:
            conteudo += f"Usuário: {msg['pergunta']}\n"
            conteudo += f"DANA: {msg['resposta']}\n\n"
        st.download_button(
            "⬇️ Download da conversa",
            data=conteudo,
            file_name="conversa_dana.txt",
            mime="text/plain"
        )
else:
    st.info("📄 Carregue um PDF, URL de YouTube ou Site para conversar com a DANA.")
