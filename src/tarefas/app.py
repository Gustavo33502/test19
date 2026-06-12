from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse 
from fastapi.security import OAuth2PasswordRequestForm
from .modelos import TarefaCreate, TarefaResponse, StatusTarefa
from .auth import verificar_token, criar_token


# Cria a aplicação FastAPI e define o título da API
app = FastAPI(title='API de Tarefas')

# Redireciona a raiz da aplicação para a documentação automática gerada pelo FastAPI (Swagger UI)
@app.get('/', include_in_schema=False)
def raiz():
    return RedirectResponse(url='/docs') # Redireciona para a documentação automática

_tarefas: dict[int, dict] = {} # Dicionário para armazenar as tarefas, onde a chave é o ID da tarefa e o valor é um dicionário com os detalhes da tarefa

_proximo_id = 1 # Variável para controlar o próximo ID a ser atribuído a uma nova tarefa, começa em 1 e é incrementada a cada nova tarefa criada

# Rota de login para gerar um token JWT para o usuário, recebe os dados do formulário de login e retorna um token de acesso
@app.post('/auth/login', tags=['auth'])
# O token é criado usando a função criar_token, que inclui o nome de usuário e um papel (role) no payload do token. O token é retornado como resposta para o cliente, que pode usá-lo para autenticar futuras requisições.
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aqui, para fins de teste, estamos aceitando qualquer nome de usuário e senha e gerando um token para eles. Em uma aplicação real, você deveria verificar as credenciais do usuário antes de gerar o token.
    token = criar_token({'sub': form_data.username, 'role': 'user'})
    # O token é retornado em um formato que o cliente pode usar para autenticar futuras requisições, indicando que o tipo de token é 'bearer' (portador).
    return {'access_token': token, 'token_type': 'bearer'}

# Rota para listar todas as tarefas, retorna uma lista de tarefas no formato definido por TarefaResponse
@app.get('/tarefas', response_model=list[TarefaResponse], tags=['tarefas'])
def listar_tarefas():
    return list(_tarefas.values())

# Rota para criar uma nova tarefa, recebe os dados da tarefa no formato definido por TarefaCreate e retorna a tarefa criada no formato definido por TarefaResponse. O status code 201 indica que a tarefa foi criada com sucesso.
@app.post('/tarefas', response_model=TarefaResponse, status_code=201, tags=['tarefas'])
def criar_tarefa(tarefa: TarefaCreate):
    global _proximo_id
    nova = {
        'id': _proximo_id,
        'titulo': tarefa.titulo,
        'descricao': tarefa.descricao,
        'status': StatusTarefa.pendente
    }
    _tarefas[_proximo_id] = nova
    _proximo_id += 1
    return nova

# Rota para buscar uma tarefa específica pelo ID, retorna a tarefa no formato definido por TarefaResponse.
@app.get('/tarefas/{tarefa_id}', response_model=TarefaResponse, tags=['tarefas'])
def buscar_tarefa(tarefa_id: int):
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail='Tarefa não encontrada')
    return _tarefas[tarefa_id]

# Rota para deletar tarefa específica pelo ID
@app.delete('/tarefas/{tarefa_id}', status_code=204, tags=['tarefas'])
def deletar_tarefa(tarefa_id: int, usuario=Depends(verificar_token)):
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail='Tarefa não encontrada')
    del _tarefas[tarefa_id]