"""Chat web - API FastAPI no Render; sem acesso direto a senhas nem ao MongoDB."""
import os
import uuid
import requests
import streamlit as st


def config(nome: str, padrao: str) -> str:
    try:
        return os.getenv(nome) or st.secrets.get(nome, padrao)
    except Exception:
        return padrao


API_URL = config("API_URL", "http://127.0.0.1:8000").rstrip("/")
TEMPO_LIMITE = 120


def api(metodo: str, caminho: str, **kwargs):
    resposta = requests.request(metodo, f"{API_URL}{caminho}", timeout=TEMPO_LIMITE, **kwargs)
    resposta.raise_for_status()
    return resposta.json()


st.set_page_config(page_title="FinBot - Aula 3", page_icon="💬")
st.title("💬 FinBot")
st.caption("Chat educacional sobre investimentos — não é recomendação financeira.")

if "sessao" not in st.session_state:
    st.session_state.sessao = uuid.uuid4().hex[:12]
    st.session_state.mensagens = []

with st.sidebar:
    st.header("Meu FinBot")
    usuario = st.text_input("Seu usuário", value="aluno1").strip() or "aluno1"
    # Ao trocar de usuario, comecamos outra conversa para evitar misturar sessoes.
    if st.session_state.get("usuario_atual") != usuario:
        st.session_state.usuario_atual = usuario
        st.session_state.sessao = uuid.uuid4().hex[:12]
        st.session_state.mensagens = []

    with st.expander("Meu perfil"):
        try:
            perfil = api("GET", f"/usuarios/{usuario}/perfil")
            with st.form("perfil"):
                nome = st.text_input("Nome", perfil.get("nome", ""))
                objetivo = st.text_input("Objetivo", perfil.get("objetivo", ""))
                niveis = ["", "iniciante", "intermediário", "avançado"]
                nivel = perfil.get("experiencia", "")
                experiencia = st.selectbox("Experiência", niveis, index=niveis.index(nivel) if nivel in niveis else 0)
                if st.form_submit_button("Salvar perfil"):
                    api("PUT", f"/usuarios/{usuario}/perfil",
                        json={"nome": nome, "objetivo": objetivo, "experiencia": experiencia})
                    st.success("Perfil salvo!")
        except Exception as erro:
            st.warning(f"Perfil indisponível: {erro}")

    if st.button("➕ Nova conversa", use_container_width=True):
        st.session_state.sessao = uuid.uuid4().hex[:12]
        st.session_state.mensagens = []

    st.subheader("Conversas")
    try:
        for c in api("GET", f"/usuarios/{usuario}/conversas"):
            if st.button(c.get("titulo", "Conversa"), key=f"conversa_{c['sessao']}", use_container_width=True):
                st.session_state.sessao = c["sessao"]
                st.session_state.mensagens = api("GET", f"/sessoes/{c['sessao']}/mensagens")
    except Exception as erro:
        st.warning(f"Lista de conversas indisponível: {erro}")


def mostrar(msg: dict):
    with st.chat_message(msg["papel"]):
        st.markdown(msg["conteudo"])


for msg in st.session_state.mensagens:
    mostrar(msg)

if pergunta := st.chat_input("Pergunte sobre CDI, Tesouro, FIIs, ações..."):
    st.session_state.mensagens.append({"papel": "user", "conteudo": pergunta})
    mostrar(st.session_state.mensagens[-1])
    with st.spinner("Pensando..."):
        try:
            r = api("POST", "/chat", json={"mensagem": pergunta,
                "sessao": st.session_state.sessao, "usuario": usuario})
            msg = {"papel": "assistant", "conteudo": r["resposta"]}
        except Exception as erro:
            msg = {"papel": "assistant", "conteudo": f"⚠️ Erro ao falar com a API: {erro}"}
    st.session_state.mensagens.append(msg)
    mostrar(msg)
