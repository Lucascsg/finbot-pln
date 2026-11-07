"""Agente de conversa da Aula 2: prompt + janela de histórico + novo pedido."""
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from app.llm import fabrica
from app.prompts import catalogo


def responder(historico: list[BaseMessage], pergunta: str, callbacks: list | None = None) -> AIMessage:
    mensagens = (
        [SystemMessage(content=catalogo.carregar("sistema"))]
        + historico[-10:]
        + [HumanMessage(content=pergunta)]
    )
    return fabrica.criar_modelo().invoke(mensagens, config={"callbacks": callbacks or []})
