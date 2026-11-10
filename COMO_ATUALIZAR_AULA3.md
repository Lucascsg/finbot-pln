# FinBot — Atualizacao da Aula 3 (FATEC / PLN)

Esta pasta contem **somente arquivos novos ou modificados** em relacao ao seu repositorio da Aula 2.
Nao apague as pastas e os arquivos antigos do GitHub. Continue usando o mesmo repositorio.

## 1. Enviar para o GitHub

1. Extraia o ZIP no computador.
2. Abra o repositorio `https://github.com/Lucascsg/finbot-pln` > **Add file > Upload files**.
3. Arraste **todo o conteudo de dentro desta pasta extraida**, preservando a estrutura das pastas `app`, `frontend`, `scripts`, `tests`.
4. Confirme o commit `Aula 3: memoria com LangGraph e MongoDB`.
5. Confira que `app/agents/grafo.py` e `app/repository/mongo.py` aparecem no GitHub.

Importante: NAO faca upload do ZIP fechado e NAO envie `.env` ou a URL do Atlas com senha ao GitHub.

## 2. Render (somente depois de publicar o codigo)

Em Render > `finbot-api` > **Environment**, configure:
- `MONGO_URL`: sua URL MongoDB Atlas (comece por `mongodb+srv://`, com usuario e senha preenchidos). Esse valor deve ficar apenas no painel, nunca no codigo.
- `MONGO_BANCO`: `finbot`.

Seu `render.yaml` atualizado ja declara essas variaveis, mas e preciso conferir se os valores estao corretos no painel. Salve as alteracoes e realize um deploy se necessario.

## 3. Streamlit

O arquivo `frontend/streamlit_app.py` foi atualizado. O app deve fazer deploy automatico a partir do mesmo repositorio. O Secret `API_URL` continua igual ao da Aula 2; nao precisa alterar nem inserir senhas no Streamlit.

## 4. Langfuse: prompt versionado

No Langfuse, em **Prompt Management > Prompts**, crie um prompt de texto `finbot-sistema` com o texto completo de `app/prompts/sistema.md`, incluindo a variavel `{{perfil}}`, e aplique o label `production`.

Como alternativa, rode localmente `python -m scripts.publicar_prompts`, com as credenciais do Langfuse configuradas em um `.env` privado no computador.

## 5. Validacao

Teste `/saude` (200) e `/chat` com sessao fixa. No Streamlit, preencha o perfil, envie duas mensagens e abra outra conversa. Depois reinicie o backend ou aguarde o Render reiniciar: a conversa deve continuar disponivel. No Atlas, verifique `conversas`, `perfis`, `checkpoints` e `checkpoint_writes`.

## 6. Tests locais

`pip install -r requirements-dev.txt` e `pytest -v` (modelo falso e banco em memoria, nao usam Groq/Atlas).

**Seguranca:** nao compartilhe a string de conexao completa com ninguem, e nunca inclua segredos em commits.
