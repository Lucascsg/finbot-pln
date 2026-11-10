"""FinBot — interface Streamlit da Aula 3.

Visual renovado, sem alterar as rotas da FastAPI nem o armazenamento MongoDB.
A API continua sendo o único componente com acesso ao banco e às chaves.
"""

from __future__ import annotations

import os
import uuid
from urllib.parse import quote

import requests
import streamlit as st


st.set_page_config(
    page_title="FinBot | Inteligência Financeira",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "FinBot — Projeto acadêmico de Processamento de Linguagem Natural."},
)


def config(nome: str, padrao: str) -> str:
    """Lê a URL pública da API sem colocar segredos no frontend."""
    try:
        return os.getenv(nome) or st.secrets.get(nome, padrao)
    except Exception:
        return padrao


API_URL = config("API_URL", "http://127.0.0.1:8000").rstrip("/")
TEMPO_LIMITE = 120


def api(metodo: str, caminho: str, **kwargs):
    resposta = requests.request(
        metodo, f"{API_URL}{caminho}", timeout=TEMPO_LIMITE, **kwargs
    )
    resposta.raise_for_status()
    return resposta.json()


def rota_usuario(usuario: str, recurso: str) -> str:
    return f"/usuarios/{quote(usuario, safe='')}/{recurso}"


# CSS decorativo, sem JavaScript nem dependências adicionais. O tema do Streamlit
# também é definido no .streamlit/config.toml incluído no pacote.
st.markdown(
    """
<style>
:root { color-scheme: dark; }
html, body { font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif; }
[data-testid="stAppViewContainer"] {
    background:
      radial-gradient(ellipse 48rem 27rem at 89% -5%, rgba(80,92,246,.12), transparent 73%),
      radial-gradient(ellipse 45rem 27rem at 10% 5%, rgba(15,185,173,.065), transparent 72%),
      #090d16;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stMainBlockContainer"] {
    max-width: 980px; padding-top: 2.2rem; padding-bottom: 8rem;
}
[data-testid="stSidebar"] {
    background: #101624;
    border-right: 1px solid rgba(160,174,210,.11);
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .65rem; }
[data-testid="stSidebar"] .stButton > button {
    background: #171e30; border: 1px solid #293347;
    color: #dce5f4; text-align: left; border-radius: 12px;
    min-height: 2.6rem; transition: border-color .2s ease, background .2s ease;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #202c43; border-color: #7183ff; color: #fff;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: 1px solid #283246; border-radius: 14px; background: #131b2b;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #151d2d !important; border-radius: 10px !important;
    border-color: #364056 !important;
}
[data-testid="stChatMessage"] {
    border: 1px solid rgba(145,161,199,.12);
    border-radius: 18px; padding: 1.1rem 1.25rem;
    background: rgba(22,30,46,.75); margin-bottom: .85rem;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
    line-height: 1.72; color: #e3e9f5;
}
[data-testid="stChatInput"] { border: 1px solid #344461; border-radius: 15px; }
[data-testid="stChatInput"]:focus-within {
    border-color: #8492ff; box-shadow: 0 0 0 2px rgba(119,132,244,.12);
}
[data-testid="stChatInput"] textarea { font-size: .95rem; }
[data-testid="stBottom"] { background: linear-gradient(transparent, #090d16 35%); }
[data-testid="stForm"] { background: transparent; border: 0; padding: 0; }
.stButton > button[kind="primary"],
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(120deg, #6275f4, #8b6eef);
    color: #fff; border: 0; border-radius: 12px;
}
.stButton > button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover { color:#fff; filter:brightness(1.1); }
.fb-brand { display:flex; align-items:center; gap:.7rem; padding:.35rem 0 1rem; }
.fb-logo { display:flex; align-items:center; justify-content:center;
    height:40px; width:40px; border-radius:13px; font-size:21px;
    color:#fff; background:linear-gradient(135deg,#687bff,#29c5c6); box-shadow:0 7px 22px #576bfa2c; }
.fb-brand-name { font-size:1.26rem; font-weight:800; letter-spacing:-.045em; color:#f3f6ff; }
.fb-brand-sub { font-size:.71rem; color:#91a2bf; margin-top:-.15rem; }
.fb-kicker { display:flex; align-items:center; gap:.5rem; font-size:.72rem;
    font-weight:700; letter-spacing:.15em; color:#9aabff; text-transform:uppercase; }
.fb-dot { display:inline-block; height:7px; width:7px; border-radius:50%; background:#43dac5;
    box-shadow:0 0 0 4px #43dac51c; }
.fb-hero { margin:.4rem 0 1.8rem; }
.fb-title { font-weight:800; font-size:clamp(2.6rem,5vw,4.15rem); letter-spacing:-.075em;
    line-height:1.04; color:#f5f8ff; margin:.7rem 0 .85rem; }
.fb-title span { color:#b1b7ff; }
.fb-subtitle { font-size:1rem; line-height:1.7; color:#94a3bd; max-width:650px; }
.fb-divider { width:100%; height:1px; margin:1.4rem 0; background:linear-gradient(90deg,#41527480,transparent); }
.fb-section { font-size:.8rem; font-weight:700; letter-spacing:.07em;
    color:#9daecb; text-transform:uppercase; margin-bottom:.8rem; }
.fb-empty { border:1px solid #29354a; border-radius:20px;
    background:linear-gradient(135deg,rgba(31,40,67,.6),rgba(17,25,39,.4));
    padding:1.7rem 1.7rem 1.25rem; margin:1.75rem 0 1rem; }
.fb-empty-title { font-size:1.08rem; color:#f1f4ff; font-weight:750; margin-bottom:.35rem; }
.fb-empty-body { font-size:.9rem; color:#95a6c1; line-height:1.6; }
.fb-note { font-size:.77rem; color:#7184a2; margin-top:1.15rem; }
.fb-smalltitle { font-size:.76rem; color:#8193b0; text-transform:uppercase;
    letter-spacing:.10em; font-weight:700; margin:.75rem 0 .2rem; }
.fb-sidebar-note { color:#91a2be; font-size:.76rem; line-height:1.55;
    border-top:1px solid #293347; padding-top:1rem; margin-top:1.1rem; }
.fb-active { display:inline-flex; align-items:center; border:1px solid #2a514b;
    background:#102824; color:#a0eedf; font-size:.72rem; padding:.35rem .62rem;
    border-radius:99px; margin-bottom:.9rem; gap:.45rem; }
@media(max-width: 760px) {
 [data-testid="stMainBlockContainer"] { padding: 1.2rem .7rem 7rem; }
 .fb-title { font-size:2.65rem; }
 .fb-empty { padding:1.25rem; }
 [data-testid="stChatMessage"] { padding:.8rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# Sessão = identificador da conversa no checkpointer do LangGraph.
if "sessao" not in st.session_state:
    st.session_state.sessao = uuid.uuid4().hex[:12]
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


with st.sidebar:
    st.markdown(
        '<div class="fb-brand"><div class="fb-logo">✦</div><div>'
        '<div class="fb-brand-name">finbot<span style="color:#88a2ff">.</span></div>'
        '<div class="fb-brand-sub">INTELIGÊNCIA FINANCEIRA</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown('<span class="fb-active"><span class="fb-dot"></span> Memória inteligente ativada</span>', unsafe_allow_html=True)
    # O seletor controla apenas a aparência; as sessões do MongoDB não mudam.
    st.markdown('<div class="fb-smalltitle">Aparência</div>', unsafe_allow_html=True)
    tema_visual = st.segmented_control(
        "Tema do FinBot",
        options=["Escuro", "Claro"],
        default="Escuro",
        key="tema_visual",
        format_func=lambda modo: "☾ Escuro" if modo == "Escuro" else "☀ Claro",
        required=True,
        label_visibility="collapsed",
        width="stretch",
        bind="query-params",
    )
    usuario = st.text_input(
        "Seu usuário", value="aluno1", help="Identificação para organizar perfil e histórico."
    ).strip() or "aluno1"

    # Evita misturar mensagens de usuários diferentes na mesma sessão local.
    if st.session_state.get("usuario_atual") != usuario:
        st.session_state.usuario_atual = usuario
        st.session_state.sessao = uuid.uuid4().hex[:12]
        st.session_state.mensagens = []

    if st.button("＋  Nova conversa", use_container_width=True, type="primary"):
        st.session_state.sessao = uuid.uuid4().hex[:12]
        st.session_state.mensagens = []
        st.rerun()

    st.markdown('<div class="fb-smalltitle">Seu espaço</div>', unsafe_allow_html=True)
    with st.expander("◈  Meu perfil"):
        try:
            perfil = api("GET", rota_usuario(usuario, "perfil"))
            with st.form("perfil"):
                nome = st.text_input("Nome", perfil.get("nome", ""))
                objetivo = st.text_input("Objetivo", perfil.get("objetivo", ""))
                niveis = ["", "iniciante", "intermediário", "avançado"]
                atual = perfil.get("experiencia", "")
                experiencia = st.selectbox(
                    "Experiência", niveis,
                    index=niveis.index(atual) if atual in niveis else 0,
                )
                if st.form_submit_button("Salvar perfil", use_container_width=True):
                    api(
                        "PUT", rota_usuario(usuario, "perfil"),
                        json={"nome": nome, "objetivo": objetivo, "experiencia": experiencia},
                    )
                    st.success("Perfil atualizado!")
        except requests.RequestException:
            st.warning("Não foi possível carregar o perfil. Confira a API do Render.")

    st.markdown('<div class="fb-smalltitle">Histórico de conversas</div>', unsafe_allow_html=True)
    try:
        conversas = api("GET", rota_usuario(usuario, "conversas"))
        if not conversas:
            st.caption("As conversas salvas aparecerão aqui.")
        for c in conversas:
            sessao = c.get("sessao", "")
            if not sessao:
                continue
            titulo = c.get("titulo") or "Conversa sem título"
            if st.button(
                f"◦  {titulo}", key=f"conversa_{sessao}",
                use_container_width=True, help="Abrir esta conversa",
            ):
                try:
                    mensagens = api("GET", f"/sessoes/{quote(sessao, safe='')}/mensagens")
                    st.session_state.sessao = sessao
                    st.session_state.mensagens = mensagens
                    st.rerun()
                except requests.RequestException:
                    st.error("Não foi possível recuperar esta conversa.")
    except requests.RequestException:
        st.warning("Histórico temporariamente indisponível.")

    st.markdown(
        '<div class="fb-sidebar-note">FinBot • Aula 3 de PLN<br>'
        'Histórico e perfil armazenados pelo MongoDB.<br>'
        'Conteúdo educacional, não é consultoria financeira.</div>',
        unsafe_allow_html=True,
    )


# Mantemos o tema original como padrão e aplicamos overrides exclusivamente
# no modo claro. A opção fica salva na URL para resistir ao recarregamento.
if tema_visual == "Claro":
    st.markdown(
        """
<style>
:root { color-scheme: light; }
html, body, .stApp { color: #20304b !important; }
[data-testid="stAppViewContainer"] {
    background:
      radial-gradient(ellipse 45rem 26rem at 88% -6%, rgba(108,122,255,.11), transparent 74%),
      radial-gradient(ellipse 45rem 26rem at 7% 4%, rgba(27,164,165,.07), transparent 76%),
      #f7f9fe !important;
    color: #20304b !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stBottom"] {
    background: linear-gradient(transparent, #f7f9fe 37%) !important;
}
[data-testid="stSidebar"] {
    background: #ffffff !important;
    color: #22324c !important;
    border-right: 1px solid #e1e7f1 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] summary,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #24344f !important;
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {
    background: #f5f7fe !important;
    color: #283753 !important;
    border: 1px solid #dce4f2 !important;
}
[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {
    background: #ecf0ff !important;
    border-color: #8894e9 !important;
    color: #293bbb !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    color: #fff !important;
    background: linear-gradient(120deg,#5368e6,#8873e2) !important;
    border: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: #f7f9ff !important;
    border: 1px solid #dce4f2 !important;
}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [data-baseweb="input"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #f7f9ff !important;
    color: #172741 !important;
    -webkit-text-fill-color: #172741 !important;
    border-color: #ccd8ea !important;
}
[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button,
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button {
    color: #2a3d60 !important;
    border-color: #d8e0ef !important;
}
[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button[aria-pressed="true"],
[data-testid="stSidebar"] [data-testid="stButtonGroup"] button[aria-pressed="true"] {
    background: #e5e9ff !important;
    color: #3547bb !important;
}
.fb-brand-name { color: #1a2944 !important; }
.fb-brand-sub { color: #637693 !important; }
.fb-smalltitle { color: #667995 !important; }
.fb-sidebar-note { color: #687a94 !important; border-color: #dce5f2 !important; }
.fb-active { border-color: #a7e1d5 !important; background: #e6f8f2 !important;
    color: #167966 !important; }
.fb-dot { background: #18a895 !important; box-shadow: 0 0 0 4px #16aa9520 !important; }
.fb-kicker { color: #5064c9 !important; }
.fb-title { color: #1a2741 !important; }
.fb-title span { color: #6570d9 !important; }
.fb-subtitle { color: #5c6e89 !important; }
.fb-divider { background: linear-gradient(90deg, #c7d3e7, transparent) !important; }
.fb-section { color: #536681 !important; }
.fb-empty { background: linear-gradient(135deg,#ffffff,#f0f4ff) !important;
    border: 1px solid #dce5f2 !important; box-shadow: 0 8px 26px #1b39750c; }
.fb-empty-title { color: #253651 !important; }
.fb-empty-body { color: #61728c !important; }
.fb-note { color: #63748d !important; }
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border-color: #dfe6f1 !important;
    box-shadow: 0 5px 20px #22375f0a !important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
    color: #243650 !important;
}
[data-testid="stChatInput"] {
    border-color: #cbd7eb !important;
    background: #ffffff !important;
    box-shadow: 0 4px 24px #283a600c;
}
[data-testid="stChatInput"] textarea {
    color: #23334f !important;
    -webkit-text-fill-color: #23334f !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #71809c !important; }
[data-testid="stChatInput"]:focus-within {
    border-color: #6879eb !important;
    box-shadow: 0 0 0 3px #6476e823 !important;
}
/* Cards das perguntas sugeridas e botões secundários no conteúdo */
[data-testid="stMain"] .stButton > button:not([kind="primary"]) {
    color: #344966 !important;
    background: #ffffff !important;
    border: 1px solid #d7e0ee !important;
}
[data-testid="stMain"] .stButton > button:not([kind="primary"]):hover {
    color: #344ac5 !important;
    background: #eef1ff !important;
    border-color: #8d9ae6 !important;
}
[data-testid="stMain"] [data-testid="stMarkdownContainer"] p { color: #31435e; }
[data-testid="stSpinner"] { color: #4053bd !important; }
@media (max-width: 760px) {
  [data-testid="stSidebar"] { border-right: none !important; }
}
</style>
""",
        unsafe_allow_html=True,
    )


st.markdown(
    '<div class="fb-hero">'
    '<div class="fb-kicker"><span class="fb-dot"></span> Assistente de investimentos com IA</div>'
    '<div class="fb-title">Seu próximo passo<br><span>começa com uma pergunta.</span></div>'
    '<div class="fb-subtitle">Explore o mundo dos investimentos com explicações claras, '
    'conversas que continuam de onde você parou e uma experiência feita para aprender.</div>'
    '</div>',
    unsafe_allow_html=True,
)


def mostrar(msg: dict) -> None:
    papel = msg.get("papel", "assistant")
    if papel not in ("user", "assistant"):
        papel = "assistant"
    with st.chat_message(papel, avatar="🤖" if papel == "assistant" else "👤"):
        st.markdown(str(msg.get("conteudo", "")))


for mensagem in st.session_state.mensagens:
    mostrar(mensagem)

atalho = None
if not st.session_state.mensagens:
    st.markdown(
        '<div class="fb-empty">'
        '<div class="fb-empty-title">O que vamos descobrir hoje?</div>'
        '<div class="fb-empty-body">Escolha um assunto para começar ou escreva sua própria pergunta.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("↗  O que é CDI?", use_container_width=True):
            atalho = "O que é CDI? Explique de forma simples."
    with col2:
        if st.button("◈  Tesouro Direto", use_container_width=True):
            atalho = "Quais são os tipos de títulos do Tesouro Direto?"
    with col3:
        if st.button("▤  Renda fixa", use_container_width=True):
            atalho = "Como funciona um investimento de renda fixa?"
    st.markdown(
        '<div class="fb-note">✧ Aprenda no seu ritmo. As respostas são educativas e não indicam compras ou vendas.</div>',
        unsafe_allow_html=True,
    )


pergunta = st.chat_input("Pergunte sobre CDI, renda fixa, ações, FIIs...")
if atalho:
    pergunta = atalho

if pergunta and pergunta.strip():
    pergunta = pergunta.strip()
    st.session_state.mensagens.append({"papel": "user", "conteudo": pergunta})
    mostrar(st.session_state.mensagens[-1])

    with st.spinner("Analisando sua pergunta..."):
        try:
            resultado = api(
                "POST", "/chat",
                json={
                    "mensagem": pergunta,
                    "sessao": st.session_state.sessao,
                    "usuario": usuario,
                },
            )
        except requests.RequestException:
            # Mantém a conversa anterior e informa o erro sem gravar uma
            # resposta artificial no MongoDB.
            st.session_state.mensagens.pop()
            st.error("Não foi possível falar com a API. Confira o serviço no Render e tente novamente.")
        else:
            mensagem = {"papel": "assistant", "conteudo": resultado.get("resposta", "")}
            st.session_state.mensagens.append(mensagem)
            mostrar(mensagem)
            st.rerun()  # Atualiza a lista de conversas da barra lateral.
