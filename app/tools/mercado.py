"""Aula 4: dados de mercado consultados por ferramentas, nao inventados pelo LLM."""
from datetime import date, timedelta
from functools import wraps

from langchain_core.tools import tool
from app.utils.http import get_json

BCB = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
BRAPI = "https://brapi.dev/api/v2"
SERIES_BCB = {"selic_meta_aa": 432, "cdi_aa": 4389, "ipca_12m": 13522}


def _seguro(funcao):
    """Converte falhas externas em avisos, sem derrubar o chatbot."""
    @wraps(funcao)
    def envolvida(*args, **kwargs):
        try:
            return funcao(*args, **kwargs)
        except Exception as erro:
            return {"erro": f"Dados indisponiveis no momento ({type(erro).__name__}). Tente novamente mais tarde."}
    return envolvida


def buscar_taxas() -> dict:
    """Busca o ultimo registro disponivel de cada serie ate a data atual."""
    hoje = date.today()
    periodo = {
        "formato": "json",
        "dataInicial": (hoje - timedelta(days=120)).strftime("%d/%m/%Y"),
        "dataFinal": hoje.strftime("%d/%m/%Y"),
    }
    taxas = {}
    for nome, codigo in SERIES_BCB.items():
        registros = get_json(BCB.format(codigo=codigo), periodo)
        if not isinstance(registros, list) or not registros:
            raise ValueError(f"Sem dados publicados para {nome}")
        ultimo = registros[-1]
        taxas[nome] = {"valor": float(ultimo["valor"].replace(",", ".")), "data": ultimo["data"]}
    taxas["fonte"] = "Banco Central do Brasil (SGS)"
    return taxas


@tool
@_seguro
def indicadores_economicos() -> dict:
    """Consulta valores ATUAIS dos indicadores brasileiros: meta Selic em % ao ano, CDI anualizado em % ao ano e IPCA acumulado em 12 meses em %, com a data de cada observacao e fonte Banco Central. Use para perguntas sobre taxas ou inflacao de hoje, NAO para explicacoes puramente conceituais."""
    return buscar_taxas()


@tool
@_seguro
def cotacao_acao(ticker: str) -> dict:
    """Consulta cotacao atual de UMA acao negociada na B3: preco em reais, variacao diaria em % e horario da cotacao. Recebe ticker da acao, por exemplo PETR4, VALE3, ITUB4, MGLU3. Use somente para acoes; FIIs devem usar indicadores_fii."""
    simbolo = ticker.strip().upper()
    dados = get_json(f"{BRAPI}/stocks/quote", {"symbols": simbolo})
    resultado = (dados.get("results") or [{}])[0]
    item = resultado.get("data") or {}
    if not item or item.get("regularMarketPrice") is None:
        return {"erro": f"Cotacao de {simbolo} indisponivel; alguns ativos exigem token ou plano da brapi.dev."}
    return {
        "ticker": resultado.get("symbol") or simbolo,
        "nome": item.get("longName") or item.get("shortName"),
        "preco": item.get("regularMarketPrice"),
        "variacao_dia_pct": item.get("regularMarketChangePercent"),
        "data": item.get("regularMarketTime") or dados.get("requestedAt"),
        "fonte": "brapi.dev",
    }


@tool
@_seguro
def indicadores_fii(ticker: str) -> dict:
    """Consulta indicadores de UM Fundo Imobiliario (FII) listado na B3: preco da cota, P/VP, dividend yield dos ultimos 12 meses em porcentagem, segmento e data de referencia. Recebe ticker terminado em 11, como MXRF11 ou HGLG11. Nao use para acoes."""
    simbolo = ticker.strip().upper()
    dados = get_json(f"{BRAPI}/fii/indicators", {"symbols": simbolo})
    itens = dados.get("fiis") or []
    if not itens:
        return {"erro": f"Indicadores de FII {simbolo} indisponiveis; consulte o acesso da brapi.dev."}
    item = itens[0]
    dy = item.get("dividendYield12m")
    if dy is not None:
        dy = round(float(dy) * 100, 2)  # API retorna uma fracao: 0.124 equivale a 12,4%.
    return {
        "ticker": simbolo,
        "preco": item.get("price"),
        "p_vp": item.get("priceToNav"),
        "dividend_yield_12m_pct": dy,
        "segmento": item.get("segmentType"),
        "data": item.get("asOfDate") or dados.get("requestedAt"),
        "fonte": "brapi.dev",
    }


@tool
@_seguro
def tesouro_direto(simbolo: str) -> dict:
    """Consulta taxa e preco atuais de UM titulo do Tesouro Direto. Exemplos de simbolo: tesouro-selic-01032031, tesouro-prefixado-com-juros-semestrais-01012037 ou tesouro-ipca-com-juros-semestrais-15082060. A taxa deve ser interpretada de acordo com o tipo e vencimento do titulo."""
    codigo = simbolo.strip().lower()
    dados = get_json(f"{BRAPI}/treasury/indicators", {"symbols": codigo})
    itens = dados.get("results") or []
    if not itens:
        return {"erro": f"Titulo {codigo} nao encontrado ou indisponivel na brapi.dev."}
    item = itens[0]
    return {
        "titulo": item.get("bondType"),
        "simbolo": item.get("symbol") or codigo,
        "vencimento": item.get("maturityDate"),
        "taxa_compra_aa": item.get("buyRate"),
        "preco_compra": item.get("buyPrice"),
        "como_ler_a_taxa": (item.get("rateInfo") or {}).get("description"),
        "data": item.get("baseDate") or dados.get("requestedAt"),
        "fonte": "brapi.dev (Tesouro Direto)",
    }


FERRAMENTAS_MERCADO = [indicadores_economicos, cotacao_acao, indicadores_fii, tesouro_direto]


if __name__ == "__main__":
    from pprint import pprint
    pprint(indicadores_economicos.invoke({}))
    pprint(cotacao_acao.invoke({"ticker": "PETR4"}))
    pprint(indicadores_fii.invoke({"ticker": "MXRF11"}))
    pprint(tesouro_direto.invoke({"simbolo": "tesouro-selic-01032031"}))
