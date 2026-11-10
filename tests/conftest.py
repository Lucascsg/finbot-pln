"""Dependencias simuladas: testes sem acesso real a Groq ou MongoDB Atlas."""
import os
import sys
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
for chave in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "API_URL"):
    os.environ[chave] = ""

from app.llm import fabrica  # noqa: E402


class ModeloFalso:
    def __init__(self):
        self.vistas = []

    def invoke(self, mensagens, config=None):
        self.vistas = mensagens
        return AIMessage(content="resposta de teste")


@pytest.fixture
def falso(monkeypatch):
    import mongomock
    from langgraph.checkpoint.memory import MemorySaver
    from app.agents import grafo
    from app.repository import mongo

    modelo = ModeloFalso()
    monkeypatch.setattr(fabrica, "criar_modelo", lambda temperatura=0.3: modelo)
    banco_falso = mongomock.MongoClient()["finbot_test"]
    monkeypatch.setattr(mongo, "banco", lambda: banco_falso)
    memoria = MemorySaver()
    # Garante que a fixture usa a mesma memoria durante toda a execucao do teste.
    grafo_teste = grafo.montar_grafo(memoria=memoria)
    monkeypatch.setattr(grafo, "grafo", lambda: grafo_teste)
    return modelo


@pytest.fixture
def api(falso):
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)
