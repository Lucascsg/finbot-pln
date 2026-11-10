"""Publica o prompt local no Langfuse e marca a versao como production.

Rodar localmente, com LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY e LANGFUSE_HOST no .env:
    python -m scripts.publicar_prompts
    python -m scripts.publicar_prompts --forcar
"""
import sys
from app.config.settings import settings
from app.llm.observabilidade import cliente_langfuse
from app.prompts import catalogo


def publicar(forcar: bool = False) -> None:
    if not settings.langfuse_ativo:
        print("Configure as duas chaves do Langfuse no .env local primeiro.")
        return
    lf = cliente_langfuse()
    for nome in catalogo.nomes_locais():
        texto, remoto = catalogo.carregar(nome), catalogo.nome_langfuse(nome)
        try:
            atual = lf.get_prompt(remoto, label="production", cache_ttl_seconds=0)
            if not forcar or atual.prompt == texto:
                print(f"= {remoto}: ja existe (versao {atual.version})")
                continue
        except Exception:
            pass
        novo = lf.create_prompt(name=remoto, prompt=texto, labels=["production"],
                               commit_message="Aula 3: prompt do FinBot")
        print(f"+ {remoto}: versao {novo.version} (production)")
    lf.flush()


if __name__ == "__main__":
    publicar(forcar="--forcar" in sys.argv)
