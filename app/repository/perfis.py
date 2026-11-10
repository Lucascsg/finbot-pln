"""Perfil de usuario persistente para TODAS as sessoes desse usuario."""
from app.repository import mongo


def _colecao():
    return mongo.banco()["perfis"]


def salvar_perfil(usuario: str, dados: dict) -> None:
    # So salva os campos permitidos pela API.
    permitidos = {chave: dados[chave] for chave in ("nome", "objetivo", "experiencia") if chave in dados}
    _colecao().update_one({"usuario": usuario}, {"$set": {"usuario": usuario, **permitidos}}, upsert=True)


def obter_perfil(usuario: str) -> dict:
    return _colecao().find_one({"usuario": usuario}, {"_id": 0}) or {"usuario": usuario}


def texto_perfil(usuario: str) -> str:
    perfil = obter_perfil(usuario)
    campos = [f"{chave}: {perfil[chave]}" for chave in ("nome", "objetivo", "experiencia") if perfil.get(chave)]
    return "; ".join(campos) or "nao informado"
