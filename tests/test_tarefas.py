import pytest
from fastapi.testclient import TestClient
from src.tarefas.app import app

@pytest.fixture
def client():

    from src.tarefas import app as app_module
    app_module._tarefas = {}
    app_module._proximo_id = 1
    with TestClient(app) as c:
        yield c

def test_ct01_login_valido(client):

    resposta = client.post("/auth/login", data={"username": "aluno", "password": "senha123"})
    assert resposta.status_code == 200
    dados = resposta.json()
    assert "access_token" in dados
    assert dados["access_token"] != ""
    assert dados["token_type"] == "bearer"


def test_ct02_login_sem_username(client):

    resposta = client.post("/auth/login", data={"password": "senha123"})
    assert resposta.status_code == 422


def test_ct03_login_sem_password(client):

    resposta = client.post("/auth/login", data={"username": "aluno"})
    assert resposta.status_code == 422

def test_ct04_criar_tarefa_valida_com_descricao(client):

    payload = {"titulo": "Estudar pytest", "descricao": "Ler a documentação"}
    resposta = client.post("/tarefas", json=payload)
    assert resposta.status_code == 201
    dados = resposta.json()
    assert isinstance(dados["id"], int)
    assert dados["titulo"] == payload["titulo"]
    assert dados["descricao"] == payload["descricao"]
    assert dados["status"] == "pendente"


def test_ct05_criar_tarefa_sem_descricao(client):
 
    payload = {"titulo": "Tarefa sem descricao"}
    resposta = client.post("/tarefas", json=payload)
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["descricao"] is None


def test_ct06_criar_tarefa_titulo_vazio(client):
   
    payload = {"titulo": ""}
    resposta = client.post("/tarefas", json=payload)
    assert resposta.status_code == 422


def test_ct07_criar_tarefa_sem_titulo(client):

    payload = {"descricao": "sem titulo"}
    resposta = client.post("/tarefas", json=payload)
    assert resposta.status_code == 422


def test_ct08_criar_tarefa_titulo_acima_limite(client):
 
    payload = {"titulo": "A" * 201}
    resposta = client.post("/tarefas", json=payload)
    assert resposta.status_code == 422

def test_ct09_status_inicial_pendente(client):

    payload = {"titulo": "Tarefa de Teste"}
    resposta = client.post("/tarefas", json=payload)
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["status"] == "pendente"

def test_ct10_listar_tarefas_vazio(client):

    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


def test_ct11_listar_tarefas_apos_criacao(client):

    client.post("/tarefas", json={"titulo": "Tarefa de Teste"})
    
    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert len(dados) == 1
    assert dados[0]["titulo"] == "Tarefa de Teste"

def test_ct12_buscar_tarefa_existente(client):

    nova_tarefa = client.post("/tarefas", json={"titulo": "Buscar essa"}).json()
    tarefa_id = nova_tarefa["id"]

    resposta = client.get(f"/tarefas/{tarefa_id}")
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Buscar essa"


def test_ct13_buscar_tarefa_inexistente(client):
 
    resposta = client.get("/tarefas/99999")
    assert resposta.status_code == 404


def test_ct14_buscar_tarefa_id_nao_numerico(client):
 
    resposta = client.get("/tarefas/abc")
    assert resposta.status_code == 422

def test_ct15_deletar_sem_token(client):

    resposta = client.delete("/tarefas/1")
    assert resposta.status_code == 401

def test_ct16_deletar_com_token_invalido(client):

    headers = {"Authorization": "Bearer token-completamente-invalido"}
    resposta = client.delete("/tarefas/1", headers=headers)
    assert resposta.status_code == 401

def test_ct17_deletar_tarefa_existente_com_token(client):

    login_res = client.post("/auth/login", data={"username": "aluno", "password": "senha123"}).json()
    token = login_res["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    tarefa = client.post("/tarefas", json={"titulo": "Deletar me"}).json()
    tarefa_id = tarefa["id"]

    resposta = client.delete(f"/tarefas/{tarefa_id}", headers=headers)
    assert resposta.status_code == 204
    assert resposta.text == ""


def test_ct18_deletar_tarefa_inexistente_com_token(client):

    login_res = client.post("/auth/login", data={"username": "aluno", "password": "senha123"}).json()
    token = login_res["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resposta = client.delete("/tarefas/99999", headers=headers)
    assert resposta.status_code == 404

def test_ct19_tarefa_deletada_indisponivel(client):

    login_res = client.post("/auth/login", data={"username": "aluno", "password": "senha123"}).json()
    token = login_res["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    tarefa = client.post("/tarefas", json={"titulo": "Sumiço"}).json()
    tarefa_id = tarefa["id"]

    client.delete(f"/tarefas/{tarefa_id}", headers=headers)

    resposta = client.get(f"/tarefas/{tarefa_id}")
    assert resposta.status_code == 404