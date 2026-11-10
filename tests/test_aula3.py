"""Testes da Aula 3: memoria, perfil e listagem de conversas, sem usar Atlas/Groq reais."""


def test_perfil_persiste(api):
    r = api.put("/usuarios/aluno1/perfil", json={
        "nome": "Ana", "objetivo": "reserva de emergencia", "experiencia": "iniciante"})
    assert r.status_code == 200
    assert api.get("/usuarios/aluno1/perfil").json()["nome"] == "Ana"


def test_lista_conversas(api):
    api.post("/chat", json={"mensagem": "O que e CDI?", "sessao": "teste-conversa", "usuario": "aluno1"})
    r = api.get("/usuarios/aluno1/conversas")
    assert r.status_code == 200
    assert any(c["sessao"] == "teste-conversa" for c in r.json())


def test_conversa_mantem_historico_no_checkpointer(api):
    api.post("/chat", json={"mensagem": "Meu nome e Ana", "sessao": "persistencia"})
    api.post("/chat", json={"mensagem": "Qual e meu nome?", "sessao": "persistencia"})
    r = api.get("/sessoes/persistencia/mensagens")
    assert r.status_code == 200
    assert len(r.json()) == 4
    assert r.json()[0]["conteudo"] == "Meu nome e Ana"


def test_usuarios_têm_conversas_separadas(api):
    api.post("/chat", json={"mensagem": "Oi A", "sessao": "a-sessao", "usuario": "A"})
    api.post("/chat", json={"mensagem": "Oi B", "sessao": "b-sessao", "usuario": "B"})
    lista_a = api.get("/usuarios/A/conversas").json()
    assert len(lista_a) == 1 and lista_a[0]["sessao"] == "a-sessao"


def test_prompt_local_compila_perfil():
    from app.prompts.catalogo import PromptLocal, carregar
    p = PromptLocal(carregar("sistema"))
    assert "Ana" in p.compile(perfil="nome: Ana")
