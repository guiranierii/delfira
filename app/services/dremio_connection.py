import os
import logging

from dremio_simple_query.connect import get_token, DremioConnection
from fastapi import HTTPException
from app.config import settings

# Autenticação com o Dremio
def collect_dremio_token():
    payload = {
        "userName": settings.dremio_user,
        "password": settings.dremio_password
    }
    try:
        token = get_token(uri=settings.dremio_login_endpoint, payload=payload)
        return token
    except Exception as e:
        logging.error("Erro ao logar no Dremio")
        raise HTTPException(status_code=500, detail=f"Não foi possível se conectar ao Dremio: {e}")
    except Exception as e:
        logging.error("Confere a senha ai mano")
        raise HTTPException(status_code=401, detail=f"Erro de autenticação: {e}")
    except Exception as e:
        logging.error("Esse erro aqui eu nunca vi não, complicado, viu?")
        raise HTTPException(status_code=500, detail=f"Erro tenso, sei o que é não: {e}")

# Validar query para evitar SQL Injectiom
def sql_validation(query):
    logging.info("Deixaa eu ver se você não tá fazendo query errada...")
    forbbiden_words = ["DROP", "ALTER", "SET", "DELETE", "UPDATE", "INSERT", "--", ";"]
    for keyword in forbbiden_words:
        if keyword.upper() in query.upper():
            logging.warning("Mano, tá tirando? Corrige essa query")
            raise HTTPException(status_code=500, detail=f"Não pode SQL Injection aqui não, fi: {keyword}")
        logging.info("Query bonita, query formosa... tá tudo ok.")
        return True

# Função para executar uma query no Dremio e retornar um DataFrame Polars
def dremio_query(query):

    sql_validation(query)
    token = collect_dremio_token()
    
    try:
        logging.info("Deixa eu chamnar o Dremio")
        dremio = DremioConnection(token, settings.dremio_arrow_endpoint)
        df = dremio.toPolars(query)
        logging.info("Era essa query que você queria?")
        return df
    except Exception as e:
        logging.error("Vish, deu certo essa query não")
        raise HTTPException(status_code=500, detail=f"Não foi possível executar a query: {e}")
    except Exception as e:
        logging.error("Vish, deu certo essa query não, vê ai: {e}")
        raise HTTPException(status_code=500, detail=f"Erro tenso, sei o que é não: {e}")
