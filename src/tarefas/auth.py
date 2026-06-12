from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# senha secreta
SECRET_KEY = 'chave-secreta-para-testes'

# criptografia para proteger o token
ALGORITHM = 'HS256'

# tempo de validade do token, expira em 30 min
EXPIRE_MIN = 30

# configuração para criptografar senhas no banco de dados
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# diz ao fastAPI onde os usuarios devem ir para fazer o login e pegar o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def criar_token(dados: dict) -> str:
    # Copia os dados do usuário (ex: id, nome) que vão rodar dentro do token
    payload = dados.copy()
    # Define a data e hora exata em que o token vai vencer (daqui a 30 minutos)
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MIN)
    # Junta os dados, a chave secreta, o algoritmo e transforma tudo em uma string criptografada (o Token)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        # Tenta ler o token usando a nossa chave secreta para ver se ele é legítimo e não expirou
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Se deu tudo certo, devolve os dados do usuário que estavam no token
        return payload
    except JWTError:
        # Se o token foi adulterado, está errado ou já passou dos 30 minutos, barra o usuário aqui
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, # erro 401 não autorizado
            detail='Token invalido ou expirado',
        )