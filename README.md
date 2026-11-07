# FinBot — Aula 2 de PLN (FATEC)

Projeto acadêmico de chatbot educacional sobre conceitos de investimentos no Brasil. Construído a partir do material das Aulas 1 e 2 da professora Cíntia Pinho.

## Links do projeto (preencher depois dos deploys)

| Recurso | URL |
|---|---|
| Código no GitHub | **A PREENCHER: URL pública do seu repositório** |
| API no Render | **A PREENCHER: URL do serviço .onrender.com** |
| Documentação da API | **A PREENCHER: URL do Render + /docs** |
| Chat no Streamlit | **A PREENCHER: URL do app .streamlit.app** |

> **Atenção:** estes links não estão publicados ainda. Substitua os campos após a publicação. Nunca publique chaves ou o arquivo `.env`.

## O que foi implementado

- Aula 1: fábrica de LLM (Groq/Gemini/Mistral), configurações por `.env`, prompt externo e chat no terminal.
- Aula 2: API FastAPI com `GET /saude`, `POST /chat` e `GET /sessoes/{sessao}/mensagens`.
- Interface conversacional com Streamlit Cloud, conectada à API via HTTP.
- Tracing de conversas no Langfuse, quando as chaves estão configuradas.
- Memória provisória por sessão em RAM; janela de contexto com as 10 últimas mensagens.
- Testes automatizados com um modelo falso (sem gastar tokens).

## Estrutura

```text
app/
  main.py
  api/rotas.py, schemas.py
  agents/chatbot.py
  servicos/chat.py
  llm/fabrica.py, observabilidade.py
  config/settings.py
  prompts/catalogo.py, sistema.md
frontend/streamlit_app.py
scripts/chat_terminal.py
tests/test_aula1.py, test_aula2.py, conftest.py
render.yaml
```

## Executar localmente (Windows / PowerShell)

Requer **Python 3.12** e uma chave Groq válida.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pip install -r frontend/requirements.txt
Copy-Item .env.example .env
```

Abra `.env` e preencha `GROQ_API_KEY`. Para usar Langfuse, preencha também as duas chaves e ajuste o host da região, se necessário.

Terminal 1 (API):

```powershell
uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000/docs` para testar a API. Terminal 2 (front, com ambiente virtual ativado):

```powershell
streamlit run frontend/streamlit_app.py
```

Para o chat do terminal da Aula 1, use `python -m scripts.chat_terminal`.

## Testes

```powershell
pytest -v
```

O teste usa uma resposta simulada e não valida a conectividade com o serviço real da Groq; verifique o chat online depois de publicar.

## Publicação

Veja **`COMO_PUBLICAR.md`** (passo a passo para GitHub, Groq, Langfuse, Render e Streamlit). A entrega no Teams é feita pelos **três links públicos**, não pelo arquivo ZIP.

## Referência didática

- [Material da professora — Aula 1](https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-01.md)
- [Material da professora — Aula 2](https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-02.md)

**Aviso:** FinBot é para fins educacionais e não constitui aconselhamento financeiro.
