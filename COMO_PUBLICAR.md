# Guia de publicação — FinBot (Aula 2 de PLN)

## O que enviar no Teams

Exatamente **três links**: (1) seu repositório GitHub público, (2) sua API Render publicada e (3) seu front Streamlit publicado. A Aula 2 continua a Aula 1; se você **já criou um repositório `finbot` na Aula 1**, use esse mesmo repositório, adicionando/atualizando o conteúdo deste pacote, sem apagar seu histórico.

> O pacote de código sozinho **não finaliza** a atividade. Somente envie quando o deploy e os testes públicos estiverem funcionando.

## 1. Faça o upload dos arquivos ao GitHub

- Acesse https://github.com/new e crie um repositório **Public** chamado `finbot-pln` (ou use o seu da Aula 1). Se criar novo, deixe **sem** adicionar README automático.
- Extraia este ZIP. Coloque o **conteúdo** da pasta `FinBot_PLN_Lucas_Aula2` dentro da pasta do seu repositório, para `render.yaml` ficar na raiz e `frontend/streamlit_app.py` existir nesse caminho.
- Opção sem Git no terminal: no repositório, selecione **Add file > Upload files** e arraste todos os arquivos/pastas extraídos. O GitHub pode ignorar arquivos ocultos em certos navegadores; confirme que `.gitignore` e `.env.example` entraram. O GitHub aceita múltiplos arquivos, mas para preservar o histórico da Aula 1 prefira VS Code/Git.

Se usar Git/PowerShell numa pasta **nova**, depois de criar o repositório no site, execute:

```powershell
git init
git branch -M main
git add .
git commit -m "Aulas 1 e 2: FinBot com FastAPI, Streamlit e Langfuse"
git remote add origin https://github.com/SEU_USUARIO/finbot-pln.git
git push -u origin main
```

Se o repositório da Aula 1 já estiver clonado, **não rode `git init` nem substitua o remote**; apenas copie os arquivos para a pasta existente, faça `git add .`, `git commit -m "Aula 2"` e `git push`.

**IMPORTANTE:** Não coloque `.env` nem chaves nos arquivos do GitHub.

## 2. Chave da Groq (LLM)

- Entre em https://console.groq.com/keys e crie uma API Key.
- A chave começa com `gsk_`. Guarde apenas no `.env` local e em **Environment Variables** do Render.
- O modelo padrão é `openai/gpt-oss-120b`. Se aparecer erro de modelo desativado, consulte a lista atual em https://console.groq.com/docs/models e ajuste `LLM_MODELO` no `.env` e no Render.

## 3. Langfuse (tracing)

- Crie conta/projeto em https://cloud.langfuse.com e vá a **Settings > API Keys**.
- Gere `LANGFUSE_PUBLIC_KEY` e `LANGFUSE_SECRET_KEY` e anote o `LANGFUSE_HOST` de sua região (`https://cloud.langfuse.com` ou `https://us.cloud.langfuse.com`).
- Configure essas chaves no painel do Render quando ele solicitar. **Não cole as chaves no repositório**.
- Sem Langfuse, a API pode responder, mas **a etapa de observabilidade da aula não fica completa**.

## 4. Render (API FastAPI)

- Entre em https://dashboard.render.com/ com sua conta GitHub.
- Clique em **New > Blueprint**, conecte seu repositório e use a branch `main`.
- O Render lê `render.yaml` que já está na raiz. Configure o Blueprint Name (por exemplo, `finbot`) e preencha `GROQ_API_KEY`, `LANGFUSE_PUBLIC_KEY` e `LANGFUSE_SECRET_KEY` quando solicitado.
- Se a sua conta Langfuse está nos EUA, altere `LANGFUSE_HOST` em **Environment** para `https://us.cloud.langfuse.com`.
- Após status **Live**, copie a URL `https://...onrender.com` do serviço.
- Confira `https://SEU_SERVICO.onrender.com/saude` (deve retornar `"status":"ok"`).
- Teste `https://SEU_SERVICO.onrender.com/docs`, rota **POST /chat**, opção **Try it out**, com o JSON:

```json
{"mensagem":"O que é CDI?","sessao":"teste1","usuario":"aluno1"}
```

- Uma pergunta vazia deverá dar status `422`, conforme o material.
- Se o status for **Failed**, verifique **Logs** no Render; sem `GROQ_API_KEY` válida não haverá resposta real do LLM.

## 5. Streamlit Cloud (interface)

- Entre em https://share.streamlit.io/ e clique em **Create app / Deploy a public app from GitHub**.
- Selecione seu repositório, branch `main`, e **Main file path = `frontend/streamlit_app.py`**.
- Antes de publicar, abra **Advanced settings > Secrets**, insira:

```toml
API_URL = "https://SEU_SERVICO.onrender.com"
```

- Substitua pelo endereço real do Render, sem `/docs` e sem barra no final.
- Clique em Deploy. Copie a URL `https://...streamlit.app`.
- Faça perguntas pela interface e confira as respostas reais; o Render gratuito pode demorar ao acordar.
- Se o front exibir conexão com `127.0.0.1:8000` recusada, reveja o Secret `API_URL` no Streamlit e salve a alteração.

## 6. Finalize o GitHub

- Abra `README.md` e substitua os quatro **A PREENCHER** pelos seus links reais (GitHub, Render, Render`/docs` e Streamlit).
- Faça commit/push desta atualização. Se a professora exigir exatamente a tag da Aula 2, crie e publique a tag:

```powershell
git tag aula-2
git push --tags
```

- Abra os três links em uma janela anônima para conferir o acesso público.
- No Langfuse, verifique se as conversas aparecem em **Tracing**, com a sessão correspondente.

## 7. Texto da entrega no Teams

```text
Atividade de reposição de 12/09 — PLN
Projeto: FinBot — Aula 2

GitHub: https://github.com/SEU_USUARIO/finbot-pln
API (Render): https://SEU_SERVICO.onrender.com
Front (Streamlit): https://SEU_APP.streamlit.app
```

**Troque cada exemplo pelo endereço real.** Não envie os exemplos literalmente.
