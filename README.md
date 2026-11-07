
# FinBot — Chatbot de Investimentos com Inteligência Artificial

Projeto acadêmico desenvolvido para a disciplina de Processamento de Linguagem Natural (PLN), na FATEC, com base nas Aulas 1 e 2 da professora Cíntia Pinho.

## Sobre o projeto

O FinBot é um chatbot educacional sobre investimentos no Brasil. Seu objetivo é utilizar técnicas de Processamento de Linguagem Natural e modelos de linguagem (LLMs) para responder a perguntas sobre conceitos financeiros de maneira simples e acessível.

O usuário pode interagir com a inteligência artificial por meio de uma interface web, realizando perguntas sobre CDI, Tesouro Direto, renda fixa, ações, fundos imobiliários e outros temas de investimentos.

O sistema foi desenvolvido em Python, utilizando FastAPI para a API, Streamlit para a interface, Groq para o modelo de linguagem e Langfuse para rastreamento das interações.

## Links do projeto

| Recurso | Link |
|---|---|
| Repositório GitHub | https://github.com/Lucascsg/finbot-pln |
| API no Render | https://finbot-api-d0ut.onrender.com |
| Documentação interativa da API | https://finbot-api-d0ut.onrender.com/docs |
| Chat no Streamlit | https://finbot-pln-fcraetein3dw3hdc3d2iv5.streamlit.app |

## Tecnologias utilizadas

- Python — linguagem de programação.
- FastAPI — desenvolvimento da API REST.
- Streamlit — interface web do chatbot.
- Groq — acesso ao modelo de inteligência artificial.
- LangChain — integração e gerenciamento das mensagens do LLM.
- Langfuse — observabilidade e rastreamento das conversas.
- Pydantic — validação dos dados da API.
- Render — hospedagem da API.
- Streamlit Community Cloud — hospedagem da interface.
- GitHub — versionamento e armazenamento do código.

## Funcionalidades implementadas

### Aula 1 — Ambiente e primeiro chatbot

- Organização do projeto Python em módulos.
- Configuração de provedores de modelos de linguagem.
- Criação do prompt de sistema do FinBot.
- Integração com modelos de linguagem.
- Implementação de uma interface de conversação pelo terminal.

### Aula 2 — API, interface e publicação

- Desenvolvimento da API com FastAPI.
- Implementação da rota de verificação de saúde.
- Implementação de envio de mensagens ao chatbot.
- Histórico temporário de conversas separado por sessão.
- Criação da interface web utilizando Streamlit.
- Integração entre frontend e backend via HTTP.
- Integração com Langfuse para monitoramento das interações.
- Publicação da API no Render.
- Publicação da interface no Streamlit Community Cloud.
- Implementação de testes automatizados para as funcionalidades da API.

## Arquitetura do sistema

O funcionamento segue este fluxo:

1. O usuário digita uma pergunta na interface Streamlit.
2. O Streamlit envia a mensagem à API FastAPI hospedada no Render.
3. A API encaminha a pergunta ao serviço de conversação.
4. O agente utiliza o modelo de linguagem disponibilizado pela Groq.
5. A resposta é devolvida à API e apresentada na interface.
6. O Langfuse registra informações sobre a interação com o modelo.

Fluxo resumido:

Usuário → Streamlit → FastAPI → LangChain → Groq (LLM)

O Langfuse realiza o rastreamento das chamadas ao modelo de linguagem.

## Estrutura do projeto

```text
app/
  agents/
    chatbot.py
  api/
    rotas.py
    schemas.py
  config/
    settings.py
  llm/
    fabrica.py
    observabilidade.py
  prompts/
    catalogo.py
    sistema.md
  servicos/
    chat.py
  main.py

frontend/
  streamlit_app.py
  requirements.txt

scripts/
  chat_terminal.py

tests/
  conftest.py
  test_aula1.py
  test_aula2.py

COMO_PUBLICAR.md
README.md
render.yaml
requirements.txt
requirements-dev.txt
```

## Endpoints da API

### GET /saude

Verifica se a API está disponível e informa o provedor e o modelo configurados.

Exemplo:

```json
{
  "status": "ok",
  "provedor": "groq",
  "modelo": "openai/gpt-oss-120b"
}
```

### POST /chat

Recebe a pergunta do usuário e retorna uma resposta gerada pela inteligência artificial.

Exemplo de requisição:

```json
{
  "mensagem": "O que é CDI?",
  "sessao": "teste1",
  "usuario": "aluno1"
}
```

### GET /sessoes/{sessao}/mensagens

Consulta o histórico temporário de mensagens de uma sessão.

A documentação interativa da API está disponível em:

https://finbot-api-d0ut.onrender.com/docs

## Execução local

Requisitos:

- Python 3.12.
- Chave de API de um provedor de LLM, como a Groq.
- Dependências Python instaladas.

No terminal, na raiz do projeto, execute:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pip install -r frontend/requirements.txt
```

Crie um arquivo `.env` na raiz do projeto e configure as variáveis necessárias, incluindo `GROQ_API_KEY` e, opcionalmente, as credenciais do Langfuse.

Não publique o arquivo `.env` nem as chaves de API no GitHub.

Inicie a API:

```powershell
uvicorn app.main:app --reload
```

Em outro terminal, inicie a interface:

```powershell
streamlit run frontend/streamlit_app.py
```

Para executar o chatbot da Aula 1 pelo terminal:

```powershell
python -m scripts.chat_terminal
```

## Testes

O projeto inclui testes automatizados para verificar as rotas da API, o histórico de mensagens, a separação das sessões e a validação das entradas.

Para executar os testes:

```powershell
pytest -v
```

Os testes automatizados utilizam respostas simuladas para não dependerem de chamadas pagas ao modelo de linguagem.

Também foram realizados testes manuais na aplicação publicada:

- API `/saude` retornando status 200.
- API `/chat` respondendo à pergunta "O que é CDI?".
- Interface Streamlit respondendo à pergunta "O que é Tesouro Direto?".
- Langfuse registrando as duas interações com o modelo ChatGroq.

## Observabilidade com Langfuse

O Langfuse permite acompanhar as chamadas realizadas ao modelo de inteligência artificial, registrando informações sobre entradas, saídas e execução das interações.

A integração foi configurada no backend por meio de variáveis de ambiente, mantendo as credenciais fora do código público.

## Limitações da versão atual

- O histórico de conversas é temporário e armazenado na memória do servidor.
- Os dados não são persistidos em um banco de dados.
- O chatbot tem finalidade educacional e não fornece recomendações personalizadas de investimento.
- A integração não garante acesso a cotações financeiras em tempo real.
- A hospedagem gratuita pode apresentar atraso na primeira requisição após períodos de inatividade.

## Referências

Material da professora Cíntia Pinho:

https://github.com/profcintiapinho/chat_multiagente_inves

Aula 1:

https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-01.md

Aula 2:

https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-02.md

## Finalidade acadêmica

Projeto desenvolvido para fins de aprendizagem na disciplina de Processamento de Linguagem Natural (PLN).

As respostas do FinBot são informativas e não substituem a orientação de profissionais habilitados do mercado financeiro.
