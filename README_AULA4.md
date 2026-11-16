# FinBot — Aula 4: ferramentas e loop do agente

**Disciplina:** Processamento de Linguagem Natural (PLN) — FATEC  
**Referência:** [Aula 4 da professora Cíntia Pinho](https://github.com/profcintiapinho/chat_multiagente_inves/blob/main/aulas/aula-04.md)

## O que muda

A Aula 4 adiciona ao FinBot quatro ferramentas de consulta a dados financeiros. O agente solicita dados às ferramentas quando a pergunta exige valores atuais, utiliza as respostas para redigir o texto e registra as consultas no Langfuse, mantendo os recursos da Aula 3 (Groq, MongoDB, histórico e perfis).

- `indicadores_economicos`: meta Selic, CDI anualizado e IPCA em 12 meses no Banco Central (SGS).
- `cotacao_acao`: preço e variação de ação da B3 pela brapi.dev.
- `indicadores_fii`: preço, P/VP, dividend yield e segmento de FII pela brapi.dev.
- `tesouro_direto`: taxa e preço de títulos pela brapi.dev.

O grafo passa a ser `START → pensar → ferramentas → pensar → END`, com limite de cinco decisões do modelo por pergunta e tratamento de falhas de API. O endpoint `POST /chat` passa a trazer `fontes` das consultas. As datas e valores são obtidos das APIs, não guardados no código.

## Testes e publicação

Na raiz do projeto, com as dependências instaladas:

```bash
pip install -r requirements-dev.txt
pytest -q
python -m app.tools.mercado
python -m scripts.publicar_prompts --forcar
```

**Atenção ao Langfuse:** o último comando exige que as chaves estejam configuradas em `.env`. Ele substitui o texto da versão de produção pelo conteúdo de `app/prompts/sistema.md`; se o prompt já tiver alterações importantes feitas manualmente no painel, incorpore-as ao arquivo antes de executar. Uma regra equivalente também está aplicada no código do agente para impedir números inventados enquanto o Langfuse não for republicado.

No Render, a variável `BRAPI_TOKEN` é opcional; configure pelo painel **Environment** para ampliar o acesso, dentro dos limites do seu plano. Não a publique no GitHub. Configure `MAX_PASSOS_AGENTE=5` (padrão). Ações PETR4, VALE3, ITUB4 e MGLU3, FIIs MXRF11 e HGLG11 e alguns títulos são exemplos de demonstração sem token, sujeitos a mudanças na API.

Testes no chat (na mesma conversa quando indicado):

1. “Quanto está a Selic hoje?”
2. “Compare PETR4 e VALE3.”
3. “E o MXRF11?”
4. “Qual é a cotação de BBAS3?” (verifique mensagem de indisponibilidade caso não tenha acesso)
5. “O que é CDI?” (não precisa de consulta de valor se for só definição)

Para a evidência, abra **Langfuse → Tracing → Tree** e faça uma captura **real** mostrando `pensar → ferramentas → indicadores_economicos → pensar`. Não use imagem simulada. Verifique que os dados, a fonte e a data aparecem no trace.

Após os testes, publique a atualização no repositório e crie a tag `aula-4`:

```bash
git add .
git commit -m "Aula 4: ferramentas e loop de tool-calling"
git tag aula-4
git push
git push --tags
```

O Render normalmente faz novo deploy a partir da branch conectada. Confirme o estado **Live**, execute perguntas na [interface Streamlit](https://finbot-pln-fcraetein3dw3hdc3d2iv5.streamlit.app), e confira o [endpoint de saúde](https://finbot-api-d0ut.onrender.com/saude).

**Limitações da verificação neste pacote:** os testes de ponta a ponta com as APIs e o modelo dependem da execução no ambiente com credenciais. Os testes automatizados incluídos simulam essas dependências e não substituem capturas reais do Langfuse.
