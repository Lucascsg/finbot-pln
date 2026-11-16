"""Aula 4: grafo reutilizavel com loop pensar -> ferramentas -> pensar."""
import json
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, AnyMessage, SystemMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from app.config.settings import settings
from app.llm import fabrica
from app.llm.observabilidade import config_prompt
from app.prompts import catalogo
from app.utils.mensagens import turno_atual


class EstadoAgente(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    perfil: str
    passos: int


def criar_agente(nome: str, nome_prompt: str, ferramentas: list, checkpointer=None):
    """Compila um agente com ferramentas e limite de iteracoes verificavel."""
    nomes_validos = ", ".join(f.name for f in ferramentas)

    def pensar(estado: EstadoAgente) -> dict:
        prompt = catalogo.obter(nome_prompt)
        texto_sistema = prompt.compile(perfil=estado.get("perfil", "nao informado"))
        # Tambem vale enquanto o prompt production do Langfuse nao for republicado.
        texto_sistema += (
            "\nREGRA OBRIGATORIA: para qualquer valor ATUAL de Selic, CDI, IPCA, "
            "acao, FII ou Tesouro Direto, consulte uma ferramenta disponivel. "
            "Nunca invente numeros, horarios ou datas; informe a data e a fonte. "
            "Se a consulta falhar, explique que o dado nao esta disponivel."
        )
        sistema = SystemMessage(content=texto_sistema)
        modelo = fabrica.criar_modelo(temperatura=0.1).bind_tools(ferramentas)
        mensagens = [sistema] + turno_atual(estado["messages"])
        try:
            resposta = modelo.invoke(mensagens, config=config_prompt(prompt))
        except Exception as erro:
            if "tool" not in str(erro).lower():
                raise
            lembrete = SystemMessage(content=f"Use APENAS nomes exatos de ferramentas: {nomes_validos}.")
            try:
                resposta = modelo.invoke(mensagens + [lembrete], config=config_prompt(prompt))
            except Exception:
                resposta = AIMessage(content="Ocorreu um problema ao consultar os dados. Tente novamente.")
        resposta.name = nome
        return {"messages": [resposta], "passos": estado.get("passos", 0) + 1}

    def proximo(estado: EstadoAgente) -> str:
        ultima = estado["messages"][-1]
        if not getattr(ultima, "tool_calls", None):
            return END
        if estado.get("passos", 0) >= settings.max_passos_agente:
            return "limite"
        return "ferramentas"

    def limite(estado: EstadoAgente) -> dict:
        return {"messages": [AIMessage(content="Nao consegui concluir a consulta em poucos passos. Pode reformular a pergunta?", name=nome)]}

    g = StateGraph(EstadoAgente)
    g.add_node("pensar", pensar)
    g.add_node("ferramentas", ToolNode(ferramentas))
    g.add_node("limite", limite)
    g.add_edge(START, "pensar")
    g.add_conditional_edges("pensar", proximo, ["ferramentas", "limite", END])
    g.add_edge("ferramentas", "pensar")
    g.add_edge("limite", END)
    return g.compile(checkpointer=checkpointer, name=nome)


def fontes_do_turno(mensagens: list[AnyMessage]) -> list[str]:
    """Extrai fontes unicas de respostas das tools durante o turno atual."""
    fontes = set()
    for msg in mensagens:
        if getattr(msg, "type", None) != "tool":
            continue
        try:
            conteudo = json.loads(msg.content)
        except (ValueError, TypeError):
            continue
        itens = conteudo if isinstance(conteudo, list) else [conteudo]
        fontes.update(item["fonte"] for item in itens if isinstance(item, dict) and item.get("fonte"))
    return sorted(fontes)
