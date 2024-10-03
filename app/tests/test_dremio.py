import pytest
from unittest.mock import patch
from fastapi import HTTPException
from app.services.dremio_connection import collect_dremio_token, sql_validation, dremio_query
from app.config import settings

# Mock para o retorno de token de autenticação do Dremio
@patch('app.services.dremio_connection.get_token')
def test_collect_dremio_token_success(mock_get_token):
    mock_get_token.return_value = "mocked_token"
    token = collect_dremio_token()
    assert token == "mocked_token"

@patch('app.services.dremio_connection.get_token')
def test_collect_dremio_token_auth_failure(mock_get_token):
    mock_get_token.side_effect = HTTPException(status_code=401, detail="Erro de autenticação")
    with pytest.raises(HTTPException):
        collect_dremio_token()

# Teste para validar a query com palavras proibidas
def test_sql_validation_valid_query():
    query = "SELECT * FROM users"
    assert sql_validation(query) is True

def test_sql_validation_invalid_query():
    query = "DROP TABLE users"
    with pytest.raises(HTTPException):
        sql_validation(query)

# Mock para a execução de uma query no Dremio
@patch('app.services.dremio_connection.DremioConnection.toPolars')
@patch('app.services.dremio_connection.collect_dremio_token')
def test_dremio_query_success(mock_collect_token, mock_to_polars):
    mock_collect_token.return_value = "mocked_token"
    mock_to_polars.return_value = "mocked_dataframe"

    query = "SELECT * FROM users"
    result = dremio_query(query)
    assert result == "mocked_dataframe"

@patch('app.services.dremio_connection.DremioConnection.toPolars')
@patch('app.services.dremio_connection.collect_dremio_token')
def test_dremio_query_failure(mock_collect_token, mock_to_polars):
    mock_collect_token.return_value = "mocked_token"
    mock_to_polars.side_effect = HTTPException(status_code=500, detail="Erro ao executar query")

    query = "SELECT * FROM users"
    with pytest.raises(HTTPException):
        dremio_query(query)
