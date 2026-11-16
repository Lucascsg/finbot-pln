"""LLM, Mongo e respostas das APIs simulados: pytest sem segredos nem internet."""
import os
import sys
from pathlib import Path
from datetime import date

import pytest
from langchain_core.messages import AIMessage, ToolMessage

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
for chave in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "API_URL"):
    os.environ[chave] = ""

from app.llm import fabrica  # noqa: E402


class ModeloFalso:
    def __init__(self):
        self.vistas = []
        self.chamadas = []
        self.ferramenta = None
        self._ferramentas = []

    def bind_tools(self, ferramentas):
        self._ferramentas = ferramentas
        return self

    def invoke(self, mensagens, config=None):
        self.vistas = mensagens
        if self.ferramenta:
            if not any(isinstance(m, ToolMessage) for m in mensagens):
                argumentos = {
                    "cotacao_acao": {"ticker": "PETR4"},
                    "indicadores_fii": {"ticker": "MXRF11"},
                    "tesouro_direto": {"simbolo": "tesouro-selic-01032031"},
                    "indicadores_economicos": {},
                }[self.ferramenta]
                self.chamadas.append(f"tool:{self.ferramenta}")
                return AIMessage(content="", tool_calls=[{
                    "name": self.ferramenta, "args": argumentos, "id": "teste-call-1", "type": "tool_call",
                }])
            self.chamadas.append("resposta")
            return AIMessage(content="resposta de teste: PETR4 R$ 38.45 (brapi.dev).")
        return AIMessage(content="resposta de teste")


@pytest.fixture
def falso(monkeypatch):
    import mongomock
    from langgraph.checkpoint.memory import MemorySaver
    from app.agents import grafo
    from app.repository import mongo
    from app.tools import mercado

    modelo = ModeloFalso()
    monkeypatch.setattr(fabrica, "criar_modelo", lambda temperatura=0.3: modelo)
    banco_falso = mongomock.MongoClient()["finbot_test"]
    monkeypatch.setattr(mongo, "banco", lambda: banco_falso)

    def api_falsa(url, params=None):
        if "bcdata.sgs" in url:
            return [{"data": date.today().strftime("%d/%m/%Y"), "valor": "14.90"}]
        if "/stocks/quote" in url:
            return {"results": [{"symbol": "PETR4", "data": {
                "longName": "Petrobras", "regularMarketPrice": 38.45,
                "regularMarketChangePercent": 0.5, "regularMarketTime": "2026-11-13T18:00:00Z",
            }}]}
        if "/fii/indicators" in url:
            return {"fiis": [{"price": 9.2, "priceToNav": 0.97,
                               "dividendYield12m": 0.124, "segmentType": "papel",
                               "asOfDate": "2026-11-13"}]}
        if "/treasury/indicators" in url:
            return {"results": [{"symbol": "tesouro-selic-01032031", "bondType": "Tesouro Selic",
                                 "maturityDate": "2031-03-01", "buyRate": 0.1,
                                 "buyPrice": 100.0, "rateInfo": {"description": "Selic mais adicional"},
                                 "baseDate": "2026-11-13"}]}
        raise ValueError(f"URL inesperada no teste: {url}")

    monkeypatch.setattr(mercado, "get_json", api_falsa)
    memoria = MemorySaver()
    grafo_teste = grafo.montar_grafo(memoria=memoria)
    monkeypatch.setattr(grafo, "grafo", lambda: grafo_teste)
    return modelo


@pytest.fixture
def api(falso):
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)
