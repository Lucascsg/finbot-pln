"""Memoria conversacional limpa e resultados de ferramentas no turno atual."""
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage


def conversa_limpa(mensagens: list[AnyMessage], limite: int = 10) -> list[AnyMessage]:
    limpas = [m for m in mensagens if isinstance(m, HumanMessage)
              or (isinstance(m, AIMessage) and m.content and not m.tool_calls)]
    return limpas[-limite:]


def turno_atual(mensagens: list[AnyMessage], limite: int = 10) -> list[AnyMessage]:
    """Junta historico normal e TODAS as mensagens deste turno, incluindo ToolMessage."""
    ultima = max((i for i, m in enumerate(mensagens) if isinstance(m, HumanMessage)), default=0)
    return conversa_limpa(mensagens[:ultima], limite) + list(mensagens[ultima:])
