"""Fixtures com LLM simulado, sem usar chave nem enviar dados à Groq."""
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
    modelo = ModeloFalso()
    monkeypatch.setattr(fabrica, "criar_modelo", lambda temperatura=0.3: modelo)
    from app.servicos import chat
    chat._memoria.clear()  # Evita que os testes compartilhem sessões antigas.
    return modelo


@pytest.fixture
def api(falso):
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)
