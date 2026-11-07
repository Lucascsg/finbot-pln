"""Serviço de chat com memória temporária separada por sessão."""
from langchain_core.messages import AIMessage, HumanMessage
from app.agents.chatbot import responder
from app.llm.observabilidade import callbacks, rastrear

# Aula 2: memória só em RAM. Reiniciar a API apaga o histórico.
_memoria: dict[str, list] = {}


def perguntar(pergunta: str, sessao: str, usuario: str = "anonimo") -> dict:
    historico = _memoria.setdefault(sessao, [])
    with rastrear(sessao, usuario):
        resposta = responder(historico, pergunta, callbacks=callbacks())
    historico.extend([HumanMessage(content=pergunta), AIMessage(content=resposta.content)])
    return {"resposta": resposta.content}


def historico(sessao: str) -> list[dict]:
    return [
        {"papel": "user" if m.type == "human" else "assistant", "conteudo": m.content}
        for m in _memoria.get(sessao, [])
    ]
