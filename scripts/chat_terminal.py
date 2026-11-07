"""Chat da Aula 1 preservado para comparação com a API da Aula 2."""
from langchain_core.messages import HumanMessage, SystemMessage
from app.config.settings import settings
from app.llm.fabrica import criar_modelo
from app.prompts import catalogo


def main():
    modelo = criar_modelo()
    historico = [SystemMessage(content=catalogo.carregar("sistema"))]
    print(f"FinBot ({settings.llm_provedor} / {settings.modelo}) — digite 'sair' para encerrar\n")
    while True:
        pergunta = input("Você: ").strip()
        if pergunta.lower() in {"sair", "exit"}:
            break
        if not pergunta:
            continue
        historico.append(HumanMessage(content=pergunta))
        resposta = modelo.invoke(historico)
        historico.append(resposta)
        print(f"FinBot: {resposta.content}\n")


if __name__ == "__main__":
    main()
