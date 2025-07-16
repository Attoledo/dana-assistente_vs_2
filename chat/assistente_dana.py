# import streamlit as st
# import re
# from langchain.prompts import ChatPromptTemplate
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.units import cm
#
# def salvar_como_pdf(texto, caminho):
#     doc = SimpleDocTemplate(caminho, pagesize=A4,
#                             rightMargin=2*cm, leftMargin=2*cm,
#                             topMargin=2*cm, bottomMargin=2*cm)
#     styles = getSampleStyleSheet()
#     estilo = styles["Normal"]
#     estilo.fontName = "Helvetica"
#     estilo.fontSize = 12
#     estilo.leading = 16
#     estilo.alignment = 4  # Justificado
#
#     partes = texto.split("\n\n")
#     elementos = [Paragraph(par.strip(), estilo) for par in partes if par.strip()]
#     for i in range(len(elementos)-1):
#         elementos.insert(i*2 + 1, Spacer(1, 12))
#
#     doc.build(elementos)
#
# def salvar_como_txt(texto, caminho):
#     with open(caminho, "w", encoding="utf-8") as f:
#         f.write(texto)
#
# def gerar_resumo(chat, texto_base):
#     prompt = ChatPromptTemplate.from_template(
#         "Resuma o conteúdo abaixo em tópicos objetivos, em português do Brasil:\n\n{texto}\nEste resumo deve ser um pouco mais descritivo de modo a dar um entendimento mais claro sobre o assunto."
#     )
#     mensagem = prompt.format_messages(texto=texto_base[:3000])
#     resposta = chat.invoke(mensagem)
#     return resposta.content.strip()
#
# # def iniciar_assistente(chat, texto_base):
# #     template = ChatPromptTemplate.from_messages([
# #         ('system', 'O seu nome é Dana, um assistente pessoal sempre disponível. Fale com empatia, entusiasmo e com uma linguagem comum a todos.'
# #                    'Voce possui características técnicas quando necessário usando todo o seu conhecimento '
# #                    'Use as informações abaixo:\n\n{informacoes}'),
# #         ('user', '{input}')
# #     ])
# #     chain = template | chat
# #
# #     if 'chat' not in st.session_state:
# #         st.session_state.chat = []
# #         if 'nome_usuario' not in st.session_state:
# #             nome = st.text_input("Olá, qual é o seu nome?", placeholder="Ex: Roberto")
# #             if nome:
# #                 st.session_state.nome_usuario = nome
# #                 st.rerun()
# #         else:
# #             nome = st.session_state.nome_usuario
# #             for entrada in st.session_state.chat:
# #                 with st.chat_message("user"):
# #                     st.markdown(entrada["pergunta"])
# #                 with st.chat_message("assistant"):
# #                     st.markdown(entrada["resposta"])
# #
# #             pergunta = st.chat_input(f"Como posso te ajudar, {nome}:")
# #             if pergunta:
# #                 with st.chat_message("user"):
# #                     st.markdown(pergunta)
# #                 with st.spinner("Estou analisando a melhor resposta..."):
# #                     resposta = chain.invoke({
# #                         'informacoes': texto_base,
# #                         'input': pergunta,
# #                         'nome_usuario': nome
# #                     }).content
# #                 with st.chat_message("assistant"):
# #                     st.markdown(resposta)
# #                 st.session_state.chat.append({
# #                     "pergunta": pergunta,
# #                     "resposta": resposta
# #                 })
#
#
# def iniciar_assistente(chat, texto_base):
#     template = ChatPromptTemplate.from_messages([
#         ('system', 'O seu nome é Dana, um assistente pessoal sempre disponível. Fale com empatia, entusiasmo e com uma linguagem comum a todos.'
#                    'Você possui características técnicas quando necessário, usando todo o seu conhecimento. '
#                    'Use as informações abaixo:\n\n{informacoes}'),
#         ('user', '{input}')
#     ])
#     chain = template | chat
#
#     # Inicializa histórico de chat se ainda não existir
#     if 'chat' not in st.session_state:
#         st.session_state.chat = []
#
#     # Captura nome do usuário
#     if 'nome_usuario' not in st.session_state:
#         nome = st.text_input("Olá, qual é o seu nome?", placeholder="Ex: Roberto")
#         if nome:
#             st.session_state.nome_usuario = nome
#             st.rerun()
#         return  # Aguarda nome ser inserido
#
#     # Exibe histórico de mensagens
#     nome = st.session_state.nome_usuario
#     for entrada in st.session_state.chat:
#         with st.chat_message("user"):
#             st.markdown(entrada["pergunta"])
#         with st.chat_message("assistant"):
#             st.markdown(entrada["resposta"])
#
#     # Input do usuário
#     pergunta = st.chat_input(f"Como posso te ajudar, {nome}:")
#     if pergunta:
#         with st.chat_message("user"):
#             st.markdown(pergunta)
#         with st.spinner("Estou analisando a melhor resposta..."):
#             resposta = chain.invoke({
#                 'informacoes': texto_base,
#                 'input': pergunta,
#                 'nome_usuario': nome
#             }).content
#         with st.chat_message("assistant"):
#             st.markdown(resposta)
#
#         # Atualiza histórico
#         st.session_state.chat.append({
#             "pergunta": pergunta,
#             "resposta": resposta
#         })
#



# assistente_dana.py
import streamlit as st
import re
import json
from langchain.prompts import ChatPromptTemplate
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def salvar_como_pdf(texto, caminho):
    doc = SimpleDocTemplate(caminho, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    estilo = styles["Normal"]
    estilo.fontName = "Helvetica"
    estilo.fontSize = 12
    estilo.leading = 16
    estilo.alignment = 4  # Justificado

    partes = texto.split("\n\n")
    elementos = [Paragraph(par.strip(), estilo) for par in partes if par.strip()]
    for i in range(len(elementos)-1):
        elementos.insert(i*2 + 1, Spacer(1, 12))

    doc.build(elementos)

def salvar_como_txt(texto, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)

def gerar_resumo(chat, texto_base):
    prompt = ChatPromptTemplate.from_template(
        "Resuma o conteúdo abaixo em tópicos objetivos, em português do Brasil:\n\n{texto}\nEste resumo deve ser um pouco mais descritivo de modo a dar um entendimento mais claro sobre o assunto."
    )
    mensagem = prompt.format_messages(texto=texto_base[:3000])
    resposta = chat.invoke(mensagem)
    return resposta.content.strip()

def iniciar_assistente(chat, texto_base):
    template = ChatPromptTemplate.from_messages([
        ('system', '''Você é DANA, um assistente amigável e confiável da DNA Agência. Seu nome representa os pilares da organização: Desenvolvimento, Necessidades Humanas e Aprendizagem Adaptativa.

Você sempre se dirige ao usuário pelo nome {nome_usuario}, e responde com empatia, clareza e profissionalismo.

Use as informações abaixo para fornecer respostas úteis, acolhedoras e alinhadas com os valores da DNA Agência:

{informacoes}

Durante a conversa, você deve:
- Compreender o contexto e o tom da mensagem do usuário
- Fornecer respostas claras, relevantes e concisas
- Utilizar uma linguagem cordial, respeitosa e acolhedora
- Apresentar explicações adicionais ou exemplos práticos sempre que necessário
- Redirecionar para fontes confiáveis ou conteúdos da DNA Agência quando apropriado
- Manter o contexto da conversa durante toda a sessão
- Ser proativa ao esclarecer dúvidas ou limitações de informação, com transparência e empatia

Você representa a excelência da DNA Agência. Responda sempre com foco em agregar valor, oferecer soluções e proporcionar uma experiência humana e positiva ao usuário.'''),
        ('user', '{input}')
    ])
    chain = template | chat

    if 'chat' not in st.session_state:
        st.session_state.chat = []

    if 'nome_usuario' not in st.session_state:
        nome = st.text_input("Olá, qual é o seu nome?", placeholder="Ex: Roberto")
        if nome:
            st.session_state.nome_usuario = nome
            st.rerun()
        return

    nome = st.session_state.nome_usuario
    for entrada in st.session_state.chat:
        with st.chat_message("user"):
            st.markdown(entrada["pergunta"])
        with st.chat_message("assistant"):
            st.markdown(entrada["resposta"])

    pergunta = st.chat_input(f"Como posso te ajudar, {nome}:")
    if pergunta:
        with st.chat_message("user"):
            st.markdown(pergunta)
        with st.spinner("Estou analisando a melhor resposta..."):
            resposta = chain.invoke({
                'informacoes': texto_base,
                'input': pergunta,
                'nome_usuario': nome
            }).content
        with st.chat_message("assistant"):
            st.markdown(resposta)

        st.session_state.chat.append({
            "pergunta": pergunta,
            "resposta": resposta
        })

        # Botões de feedback
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Foi útil", key=f"feedback_util_{len(st.session_state.chat)}"):
                st.success("Obrigado pelo feedback!")
        with col2:
            if st.button("👎 Não foi útil", key=f"feedback_nao_util_{len(st.session_state.chat)}"):
                st.info("Obrigado! Vamos melhorar nas próximas respostas.")

        # Salva histórico em JSON local
        with open("historico_conversa.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state.chat, f, ensure_ascii=False, indent=2)