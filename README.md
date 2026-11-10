# FinBot — Chatbot Educacional com Inteligência Artificial

**Disciplina:** Processamento de Linguagem Natural (PLN) — FATEC  
**Projeto:** FinBot — Aulas 1, 2 e 3  
**Referência didática:** Professora Cíntia Pinho

## Visão geral

O FinBot é um chatbot educacional desenvolvido em Python para explicar conceitos de investimentos no Brasil, como CDI, Tesouro Direto, CDB, renda fixa, ações e fundos imobiliários.

A aplicação utiliza inteligência artificial para responder às perguntas dos usuários, mantendo o histórico das conversas e informações de perfil em um banco de dados MongoDB Atlas.

O projeto tem finalidade acadêmica e não realiza recomendações personalizadas de investimentos.

## Links do projeto

| Recurso | Endereço |
|---|---|
| Código-fonte | https://github.com/Lucascsg/finbot-pln |
| Chatbot no Streamlit | https://finbot-pln-fcraetein3dw3hdc3d2iv5.streamlit.app |
| API no Render | https://finbot-api-d0ut.onrender.com |
| Documentação da API | https://finbot-api-d0ut.onrender.com/docs |

## Tecnologias utilizadas

- **Python:** linguagem principal do projeto.
- **FastAPI:** desenvolvimento da API REST.
- **Streamlit:** interface web do chatbot.
- **Groq:** integração com o modelo de inteligência artificial.
- **LangChain:** manipulação das mensagens e integração com o modelo.
- **LangGraph:** organização do fluxo conversacional e gerenciamento de estado.
- **MongoDB Atlas:** armazenamento de conversas e perfis.
- **Langfuse:** observabilidade, rastreamento e versionamento de prompts.
- **Render:** hospedagem da API.
- **Streamlit Community Cloud:** hospedagem do frontend.
- **GitHub:** versionamento e armazenamento do código.

## Funcionalidades implementadas

### Aula 1 — Chatbot com inteligência artificial

- Organização do projeto Python em módulos.
- Configuração do provedor de linguagem.
- Criação do prompt de sistema.
- Integração com modelo de linguagem.
- Implementação de chatbot utilizando o terminal.

### Aula 2 — API e publicação

- Desenvolvimento da API utilizando FastAPI.
- Implementação das rotas `/saude` e `/chat`.
- Criação da interface web com Streamlit.
- Comunicação entre frontend e backend por HTTP.
- Integração com Langfuse para monitoramento das interações.
- Publicação da API no Render.
- Publicação do frontend no Streamlit Community Cloud.
- Implementação de testes automatizados.

### Aula 3 — Memória persistente e prompts versionados

**1. Integração com MongoDB Atlas**

Implementação de banco de dados para armazenar persistentemente as conversas e os perfis dos usuários.

**2. Integração com LangGraph**

Organização do chatbot utilizando um grafo conversacional, com controle do estado e memória de cada sessão.

**3. Memória de curto prazo**

O FinBot consegue recuperar mensagens anteriores da mesma conversa e utilizar essas informações para responder às próximas perguntas.

**4. Memória de longo prazo**

Armazenamento de informações do perfil do usuário, incluindo nome, objetivo e nível de experiência.

**5. Gerenciamento de conversas**

Implementação de funcionalidades para criar novas conversas, listar históricos e recuperar mensagens de sessões anteriores.

**6. Versionamento de prompts no Langfuse**

Criação do prompt `finbot-sistema`, utilizando versões e a etiqueta `production`. Essa funcionalidade permite atualizar as instruções do chatbot sem alterar diretamente seu código-fonte.

**7. Nova interface do FinBot**

Desenvolvimento de uma interface personalizada com identidade visual tecnológica, incluindo:

- Design futurista e minimalista.
- Alternância entre temas claro e escuro.
- Interface adaptável a diferentes tamanhos de tela.
- Barra lateral para gerenciamento de perfis e conversas.
- Sugestões de perguntas.
- Histórico de mensagens persistente.

## Arquitetura do sistema

O funcionamento do sistema segue este fluxo:

1. O usuário acessa o chatbot pelo Streamlit.
2. A interface envia a mensagem para a API FastAPI.
3. A API encaminha a solicitação ao serviço responsável pelo chat.
4. O LangGraph organiza o processamento da conversa.
5. O MongoDB fornece o histórico e as informações do usuário.
6. O agente utiliza o prompt configurado e consulta o modelo de linguagem.
7. A resposta é enviada ao frontend.
8. O MongoDB mantém o histórico para futuras interações.
9. O Langfuse registra informações para observabilidade.

**Fluxo resumido:**

Usuário → Streamlit → FastAPI → LangGraph → Groq

**Serviços complementares:**

- MongoDB Atlas: memória e persistência.
- Langfuse: prompts e observabilidade.

## Estrutura do projeto

**app/** — Código principal do backend.

- `agents/` — chatbot e grafo LangGraph.
- `api/` — rotas e validação de dados.
- `config/` — configurações do sistema.
- `llm/` — integração com modelos e observabilidade.
- `prompts/` — catálogo e prompt de sistema.
- `repository/` — conexão com MongoDB, perfis, conversas e checkpointer.
- `servicos/` — lógica do serviço de chat.
- `utils/` — tratamento de mensagens.
- `main.py` — inicialização da API.

**frontend/** — Interface web.

- `streamlit_app.py` — interface principal, gerenciamento de conversas, perfis e alternância de temas.
- `requirements.txt` — dependências do frontend.

**.streamlit/** — Configurações visuais.

- `config.toml` — configuração do tema-base.

**scripts/** — Scripts auxiliares.

- `chat_terminal.py`
- `publicar_prompts.py`

**tests/** — Testes automatizados.

- `test_aula1.py`
- `test_aula2.py`
- `test_aula3.py`

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/saude` | Verificação de funcionamento da API |
| POST | `/chat` | Envio de mensagens ao chatbot |
| GET | `/sessoes/{sessao}/mensagens` | Consulta do histórico |
| GET | `/usuarios/{usuario}/conversas` | Listagem de conversas |
| GET | `/usuarios/{usuario}/perfil` | Consulta do perfil |
| PUT | `/usuarios/{usuario}/perfil` | Cadastro e atualização do perfil |

## Testes realizados na Aula 3

### Teste 1 — Persistência de perfil

Foi cadastrado um perfil de usuário com nome, objetivo e experiência. Posteriormente, foi realizada uma consulta para verificar a recuperação dos dados.

**Resultado:** realizado com sucesso.

### Teste 2 — Memória conversacional

O usuário informou ao chatbot que seu investimento favorito era o Tesouro Selic.

Em uma segunda mensagem da mesma sessão, perguntou qual investimento havia mencionado anteriormente.

**Resultado:** o FinBot recuperou corretamente a informação.

### Teste 3 — Persistência após reinicialização

A API foi publicada novamente no Render. Depois da atualização, foi realizada outra pergunta sobre a informação anteriormente armazenada.

**Resultado:** o FinBot recuperou corretamente a informação após o novo deploy.

### Teste 4 — Histórico no Streamlit

Foi acessada uma conversa anterior diretamente pela barra lateral da aplicação.

**Resultado:** as mensagens do usuário e as respostas do chatbot foram recuperadas corretamente.

### Teste 5 — Gerenciamento de perfis

O perfil armazenado foi consultado pela interface web.

**Resultado:** os campos de nome, objetivo e experiência foram exibidos corretamente.

### Teste 6 — Versionamento de prompt

Foi criada uma segunda versão do prompt no Langfuse, acrescentando uma instrução para o FinBot terminar suas respostas com uma pergunta.

Uma nova mensagem foi enviada pela API e a resposta apresentou o comportamento esperado.

**Resultado:** comportamento compatível com a nova versão do prompt.

### Teste 7 — Interface moderna

Foi implementado um novo frontend com identidade visual personalizada e alternância entre temas claro e escuro.

**Resultado:** os dois temas foram testados na aplicação publicada.

## Segurança e configurações

As credenciais utilizadas pelo sistema são armazenadas em variáveis de ambiente.

O projeto não publica senhas, chaves de API ou credenciais de acesso ao MongoDB no repositório.

As variáveis principais são:

- `GROQ_API_KEY`
- `MONGO_URL`
- `MONGO_BANCO`
- `LANGFUSE_PUBLIC_KEY`
- `LANGFUSE_SECRET_KEY`
- `LANGFUSE_HOST`
- `API_URL`

O identificador de usuário utilizado na aplicação é adequado à demonstração acadêmica, mas não substitui um sistema completo de autenticação e autorização.

## Limitações

- O FinBot tem finalidade exclusivamente educacional.
- Não realiza recomendações individualizadas de investimentos.
- Não garante acesso a cotações financeiras em tempo real.
- A hospedagem gratuita pode apresentar lentidão após períodos de inatividade.

## Referências

**Repositório da professora Cíntia Pinho:**

https://github.com/profcintiapinho/chat_multiagente_inves

**Aula 1:**

https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-01.md

**Aula 2:**

https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-02.md

**Aula 3:**

https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-03.md

---

Projeto desenvolvido para fins acadêmicos na disciplina de Processamento de Linguagem Natural (PLN), na FATEC.
