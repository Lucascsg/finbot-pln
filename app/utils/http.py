"""HTTP para APIs publicas, com timeout e chave enviada apenas a brapi."""
import requests
from app.config.settings import settings


def get_json(url: str, params: dict | None = None):
    headers = {"User-Agent": "FinBot-FATEC/1.0", "Accept": "application/json"}
    token = settings.brapi_token.get_secret_value() if settings.brapi_token else ""
    if token and url.startswith("https://brapi.dev/api/"):
        headers["Authorization"] = f"Bearer {token}"
    resposta = requests.get(url, params=params, headers=headers, timeout=15)
    resposta.raise_for_status()
    return resposta.json()
