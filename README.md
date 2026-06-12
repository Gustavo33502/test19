<img width="1372" height="400" alt="teste sms" src="https://github.com/Gustavo33502/test19/blob/main/printtest19.png" />
Print do test

Para realizar os testes, é necessário fazer a instalação de algumas extensões. Para realizar essas instalações, utilize o comando pip install -r requirements.txt no terminal do seu editor/IDE.

Documento de explicação dos 19 casos de teste do código realizado e como executá-los:

Para executar os testes, utilize o comando: pytest tests/test_tarefas.py::nome_da_função

Módulo: Autenticação
1 - test_ct01_login_valido

2 - test_ct02_login_sem_username

3 - test_ct03_login_sem_password

Módulo: Criar Tarefa

4 - test_ct04_criar_tarefa_valida_com_descricao

5 - test_ct05_criar_tarefa_sem_descricao

6 - test_ct06_criar_tarefa_titulo_vazio

7 - test_ct07_criar_tarefa_sem_titulo

8 - test_ct08_criar_tarefa_titulo_acima_limite

9 - test_ct09_status_inicial_pendente

Módulo: Listar Tarefas

10 - test_ct10_listar_tarefas_vazio

11 - test_ct11_listar_tarefas_apos_criacao

Módulo: Buscar Tarefa por ID

12 - test_ct12_buscar_tarefa_existente

13 - test_ct13_buscar_tarefa_inexistente

14 - test_ct14_buscar_tarefa_id_nao_numerico

Módulo: Deletar Tarefa

15 - test_ct15_deletar_sem_token

16 - test_ct16_deletar_com_token_invalido

17 - test_ct17_deletar_tarefa_existente_com_token

18 - test_ct18_deletar_tarefa_inexistente_com_token

19 - test_ct19_tarefa_deletada_indisponivel

🔐 Módulo: Autenticação
CT-01 — Login com credenciais válidas
O que simula: Um usuário legítimo tentando fazer login informando o usuário (aluno) e a senha (senha123) corretos através de um formulário.

Como age: Envia uma requisição POST para /auth/login passando os dados como data= (Form Data).

O que valida: Garante que a API responde com status 200 OK e entrega um corpo contendo a chave access_token (uma string preenchida) e o token_type como "bearer".

CT-02 — Login sem o campo username
O que simula: Um erro do cliente (ou do frontend) que enviou apenas a senha, esquecendo o nome de usuário.

Como age: Envia um POST para /auth/login contendo apenas o campo password.

O que valida: Garante que o FastAPI intercepte a falta do campo obrigatório e barre a requisição respondendo com status 422 Unprocessable Entity.

CT-03 — Login sem o campo password
O que simula: O oposto do anterior: o usuário digitou o nome de usuário, mas esqueceu a senha.

Como age: Envia um POST para /auth/login contendo apenas o campo username.

O que valida: Assim como o CT-02, valida se a API bloqueia a requisição incompleta com o status 422.

📝 Módulo: Criar Tarefa
CT-04 — Criar tarefa com dados válidos (com descrição)
O que simula: O cadastro perfeito de uma tarefa com todas as informações possíveis preenchidas.

Como age: Dispara um POST para /tarefas com um JSON contendo titulo e descricao.

O que valida: Verifica se o status retornado é 201 Created, se a API gerou um id numérico automático, se os dados batem com o que foi enviado e se o status padrão foi definido como "pendente".

CT-05 — Criar tarefa sem descrição (campo opcional)
O que simula: Criação de uma tarefa rápida, onde o usuário preenche apenas o título, já que a descrição não é obrigatória.

Como age: Envia o JSON para /tarefas omitindo completamente a chave descricao.

O que valida: Garante que a API aceita a requisição, responde com 201 Created e salva o campo descricao explicitamente como nulo (None ou null).

CT-06 — Criar tarefa com título vazio
O que simula: Um usuário tentando salvar uma tarefa enviando o título como uma string vazia ("").

Como age: Envia um POST para /tarefas com {"titulo": ""}.

O que valida: Testa a regra do Pydantic (min_length=1). O teste valida se a API recusa a gravação e devolve status 422.

CT-07 — Criar tarefa sem o campo título
O que simula: O envio de um payload que simplesmente ignora a existência da propriedade titulo.

Como age: Envia um POST para /tarefas contendo apenas a descrição: {"descricao": "..."}.

O que valida: Como o título é obrigatório na estrutura do banco/modelo, o teste valida se a API barra o processo com o status 422.

CT-08 — Criar tarefa com título acima do limite (201 caracteres)
O que simula: Um abuso de caracteres no campo de título (comprimento maior do que o bom senso e o banco permitem).

Como age: Cria uma string gigante multiplicando a letra "A" 201 vezes e envia no POST.

O que valida: Testa a regra do Pydantic (max_length=200). Valida se a API barra a requisição com status 422.

CT-09 — Status inicial da tarefa criada é "pendente"
O que simula: Um usuário malicioso ou confuso tentando "forçar" que uma tarefa nova já nasça com o status de "concluido".

Como age: Envia um POST para criar a tarefa injetando maliciosamente a chave "status": "concluido" no JSON.

O que valida: Garante que a regra de negócio da API prevaleça: ela deve ignorar o status enviado pelo usuário e forçar o retorno do campo status estritamente como "pendente".

🔍 Módulo: Listar Tarefas
CT-10 — Listar tarefas com repositório vazio
O que simula: O primeiro acesso de um usuário ao sistema, quando ele ainda não cadastrou absolutamente nada.

Como age: Faz uma requisição GET direto para /tarefas logo após o reset da memória.

O que valida: Garante que a API responde com 200 OK e entrega uma lista perfeitamente vazia ([]), sem quebrar ou retornar nulo.

CT-11 — Listar tarefas após criação
O que simula: O comportamento da listagem após o sistema já possuir dados cadastrados.

Como age: Primeiro, ele faz um POST interno para criar uma tarefa. Logo em seguida, faz um GET em /tarefas.

O que valida: Garante que o status é 200 OK e que a lista retornada não está vazia, contendo exatamente o item que acabou de ser criado.

🆔 Módulo: Buscar Tarefa por ID
CT-12 — Buscar tarefa existente
O que simula: O usuário clicando em uma tarefa específica para ver os detalhes dela.

Como age: Cria uma tarefa via POST, captura o id gerado por ela e faz um GET para /tarefas/{id}.

O que valida: Valida se a API localiza o registro, retorna status 200 OK e traz os dados idênticos aos do objeto criado.

CT-13 — Buscar tarefa com ID inexistente
O que simula: O usuário tentando acessar uma tarefa digitando um ID qualquer na URL que não existe no sistema (ex: 99999).

Como age: Faz um GET diretamente para /tarefas/99999.

O que valida: Garante que a API trata esse erro优雅mente, retornando o status correto de recurso não encontrado: 404 Not Found.

CT-14 — Buscar tarefa com ID não numérico
O que simula: Uma tentativa de quebra de rota ou inserção de dados inválidos na URL (ex: /tarefas/abc).

Como age: Faz um GET passando letras no lugar do parâmetro identificador.

O que valida: Como a rota foi tipada no FastAPI como tarefa_id: int, o próprio framework deve validar o tipo de dado e recusar a entrada com o status 422.

🗑️ Módulo: Deletar Tarefa
CT-15 — Deletar tarefa sem token de autenticação
O que simula: Um usuário anônimo ou hacker tentando deletar um recurso da aplicação sem estar logado.

Como age: Faz uma requisição DELETE para /tarefas/1 sem incluir nenhum cabeçalho de autorização.

O que valida: Garante que o sistema de segurança bloqueie a operação imediatamente, respondendo com status 401 Unauthorized.

CT-16 — Deletar tarefa com token inválido
O que simula: Um ataque onde alguém tenta falsificar um token de segurança ou envia uma chave expirada/corrompida.

Como age: Envia a requisição DELETE incluindo o cabeçalho Authorization: Bearer token-invalido.

O que valida: Garante que o decodificador JWT da API detecte a assinatura inválida e recuse o acesso com o status 401 Unauthorized.

CT-17 — Deletar tarefa existente com token válido
O que simula: O fluxo ideal e autorizado de exclusão do sistema por um usuário logado.

Como age: 1. Faz login para capturar um token JWT válido.
2. Cria uma tarefa para gerar um ID real.
3. Envia um DELETE para o ID gerado, anexando o token legítimo nos headers.

O que valida: Garante que a API processe a exclusão com sucesso, respondendo com o status padrão de operações de remoção vazias: 204 No Content.

CT-18 — Deletar tarefa inexistente com token válido
O que simula: Um usuário autenticado tentando deletar uma tarefa que já foi excluída ou cujo ID nunca existiu.

Como age: Faz login para obter o token legítimo e envia um DELETE para /tarefas/99999.

O que valida: Mesmo com o usuário autenticado, o recurso não existe. Portanto, a API deve responder com status 404 Not Found.

CT-19 — Tarefa deletada não pode ser encontrada depois
O que simula: A garantia real de persistência da deleção (comprovar que o "deletar" realmente sumiu com o dado).

Como age: Faz o fluxo de autenticação, cria uma tarefa, deleta essa tarefa usando o token e, logo em seguida, tenta fazer um GET na rota de detalhes daquela mesma tarefa deletada.

O que valida: Garante que a API retorne 404 Not Found no último passo, provando que o registro foi de fato expurgado da memória e não está mais acessível. venv/bin/activate
