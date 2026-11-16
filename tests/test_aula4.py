"""Aula 4: tests de ferramentas, ciclo do agente, limites e fontes."""
from datetime import date

from app.agents import grafo
from app.config.settings import settings
from app.tools import mercado


def test_ferramentas_tem_descricoes_detalhadas():
    for ferramenta in mercado.FERRAMENTAS_MERCADO:
        assert len(ferramenta.description) > 80
    assert mercado.cotacao_acao.args["ticker"]["type"] == "string"


def test_dados_e_conversoes_sem_internet(falso):
    indicadores = mercado.indicadores_economicos.invoke({})
    assert indicadores["cdi_aa"]["valor"] == 14.9
    assert indicadores["fonte"] == "Banco Central do Brasil (SGS)"
    assert mercado.cotacao_acao.invoke({"ticker": "petr4"})["preco"] == 38.45
    assert mercado.indicadores_fii.invoke({"ticker": "MXRF11"})["dividend_yield_12m_pct"] == 12.4
    assert mercado.tesouro_direto.invoke({"simbolo": "tesouro-selic-01032031"})["preco_compra"] == 100.0


def test_api_externa_falhou_sem_quebrar(falso, monkeypatch):
    def falhar(*a, **kw):
        raise ConnectionError("Sem rede")
    monkeypatch.setattr(mercado, "get_json", falhar)
    assert "erro" in mercado.indicadores_economicos.invoke({})


def test_loop_chama_ferramenta_e_informa_fonte(falso):
    falso.ferramenta = "cotacao_acao"
    saida = grafo.executar("Quanto esta PETR4?", sessao="aula4-tool", usuario="teste")
    assert falso.chamadas == ["tool:cotacao_acao", "resposta"]
    assert "38.45" in saida["resposta"]
    assert saida["fontes"] == ["brapi.dev"]


def test_guardrail_interrompe_ferramentas_apos_limite(falso, monkeypatch):
    from langchain_core.messages import HumanMessage
    from app.agents.base import criar_agente
    falso.ferramenta = "indicadores_economicos"
    monkeypatch.setattr(settings, "max_passos_agente", 1)
    agente = criar_agente("teste", "sistema", mercado.FERRAMENTAS_MERCADO)
    estado = agente.invoke({"messages": [HumanMessage(content="Selic hoje?")], "passos": 0})
    assert "poucos passos" in estado["messages"][-1].content


def test_contador_reinicia_na_proxima_pergunta(falso, monkeypatch):
    monkeypatch.setattr(settings, "max_passos_agente", 2)
    falso.ferramenta = "cotacao_acao"
    a = grafo.executar("PETR4 agora", sessao="aula4-reset")
    b = grafo.executar("PETR4 novamente", sessao="aula4-reset")
    assert "38.45" in a["resposta"] and "38.45" in b["resposta"]
    assert b["fontes"] == ["brapi.dev"]


def test_falha_no_nome_da_ferramenta_gera_nova_tentativa(falso, monkeypatch):
    from langchain_core.messages import HumanMessage
    from app.agents.base import criar_agente
    original = type(falso).invoke
    falhas = {"total": 0}

    def com_erro(self, mensagens, config=None):
        if self._ferramentas and falhas["total"] == 0:
            falhas["total"] += 1
            raise RuntimeError("tool call validation failed: attempted to call tool 'taxa_bcb'")
        return original(self, mensagens, config)

    falso.ferramenta = "indicadores_economicos"
    monkeypatch.setattr(type(falso), "invoke", com_erro)
    agente = criar_agente("teste", "sistema", mercado.FERRAMENTAS_MERCADO)
    estado = agente.invoke({"messages": [HumanMessage(content="Selic hoje?")], "passos": 0})
    assert falhas["total"] == 1
    assert "resposta de teste" in estado["messages"][-1].content


def test_bcb_consulta_ate_o_dia_atual(falso, monkeypatch):
    parametros = []

    def registrar(url, params=None):
        parametros.append(params)
        return [{"data": "10/11/2026", "valor": "14.90"}]

    monkeypatch.setattr(mercado, "get_json", registrar)
    mercado.buscar_taxas()
    assert all(p["dataFinal"] == date.today().strftime("%d/%m/%Y") for p in parametros)
