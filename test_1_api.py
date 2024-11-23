import requests
import pytest

#  URL da API pública que gera perfis de usuários
BASE_URL = "https://randomuser.me/api/"

@pytest.fixture
def default_params():
    """Fixture para parâmetros padrão das requisições."""
    return {"results": 1}

def test_success_response_status_code(default_params):
    """
    Teste de sucesso: Verifica se a API retorna o status code 200.
    """
    response = requests.get(BASE_URL, params=default_params)
    assert response.status_code == 200, "A API não retornou o status code esperado (200)."

def test_invalid_request():
    """
    Teste de erro: Verifica o comportamento da API para um parâmetro inválido.
    """
    invalid_params = {"invalid_param": "abc"}
    response = requests.get(BASE_URL, params=invalid_params)
    
    # A API deve retornar status 200, mas verificamos o conteúdo da resposta
    assert response.status_code == 200, "A API não retornou status code 200 para um parâmetro inválido."
    
    # Verificar se a resposta não contém dados válidos ou retorna algum erro no conteúdo
    data = response.json()
    assert "error" not in data, "A resposta contém um erro inesperado."
    # Opcional: adicionar validações específicas para verificar que o parâmetro inválido foi ignorado

def test_response_structure(default_params):
    """
    Teste de verificação de dados: Valida se a resposta contém as chaves esperadas.
    """
    response = requests.get(BASE_URL, params=default_params)
    assert response.status_code == 200, "A API não retornou o status code esperado (200)."
    
    data = response.json()
    assert "results" in data, "A resposta não contém a chave 'results'."
    assert len(data["results"]) == default_params["results"], "A quantidade de resultados não corresponde ao esperado."
    
    # Validar as chaves de um usuário dentro de "results"
    user = data["results"][0]
    expected_keys = {"gender", "name", "location", "email", "dob"}
    assert expected_keys.issubset(user.keys()), f"Faltam chaves esperadas na resposta: {expected_keys - set(user.keys())}"

def test_multiple_users_request():
    """
    Teste de sucesso: Solicita múltiplos usuários e verifica o tamanho da lista retornada.
    """
    params = {"results": 5}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200, "A API não retornou o status code esperado (200)."
    
    data = response.json()
    assert len(data["results"]) == params["results"], "O número de usuários retornados não corresponde ao solicitado."

def test_query_specific_fields():
    """
    Teste de verificação de dados: Filtra resultados para campos específicos.
    """
    params = {"results": 1, "nat": "US"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200, "A API não retornou o status code esperado (200)."
    
    data = response.json()
    user = data["results"][0]
    assert user["nat"] == "US", "A nacionalidade do usuário não corresponde ao filtro solicitado ('US')."
