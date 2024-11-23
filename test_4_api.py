import pytest
import requests

# URL da API para obter dados sobre cães
BASE_URL = "https://api.thedogapi.com/v1/breeds"

# Chave varia conforme teste
HEADERS = {"x-api-key": "SUA_CHAVE_DE_API"}

@pytest.fixture
def default_params():
    """Fixture para parâmetros padrão das requisições."""
    return {}

def test_success_response_status_code(default_params):
    """
    Teste de sucesso: Verifica se a API retorna o status code 200.
    """
    response = requests.get(BASE_URL, params=default_params, headers=HEADERS)
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}. Mensagem: {response.text}"

def test_invalid_breed_query():
    """
    Teste de erro: Verifica o comportamento da API para uma raça de cão inválida.
    """
    invalid_params = {"name": "InvalidBreed"}
    response = requests.get(BASE_URL, params=invalid_params, headers=HEADERS)

    # A API pode retornar status 200, mas a resposta não deve conter a raça solicitada
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}. Mensagem: {response.text}"

    data = response.json()
    assert isinstance(data, list), "A resposta não é uma lista."
    # Verificar se a resposta não contém a raça solicitada
    breed_names = [breed["name"] for breed in data]
    assert "InvalidBreed" not in breed_names, "A raça inválida foi encontrada na resposta."

def test_breed_data_contains_expected_keys():
    """
    Teste de verificação de dados: Verifica se os dados da raça de cachorro contêm chaves esperadas.
    """
    response = requests.get(BASE_URL, params={"name": "American Bulldog"}, headers=HEADERS)
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}."
    
    data = response.json()
    assert len(data) > 0, "Nenhuma raça foi retornada para 'American Bulldog'."
    
    breed = data[0]
    expected_keys = {"id", "name", "origin", "weight", "height", "temperament"}
    assert expected_keys.issubset(breed.keys()), f"Faltam chaves esperadas: {expected_keys - set(breed.keys())}"

def test_valid_breed_info():
    """
    Teste de verificação: Verifica se as informações sobre uma raça são válidas.
    """
    response = requests.get(BASE_URL, params={"name": "Pit Bull"}, headers=HEADERS)
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}."

    data = response.json()
    assert isinstance(data, list), "A resposta não é uma lista."
    
    # Verificar que alguma raça com nome semelhante a "Pit Bull" esteja presente
    breed_names = [breed["name"] for breed in data]
    assert any("Pit Bull" in name for name in breed_names), f"Nenhuma raça contendo 'Pit Bull' foi encontrada. Recebido: {breed_names}"

def test_multiple_breeds_request():
    """
    Teste de sucesso: Solicita múltiplas raças e verifica o número de resultados.
    """
    response = requests.get(BASE_URL, params={"limit": 5}, headers=HEADERS)
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}."
    
    data = response.json()
    assert len(data) == 5, f"Esperado 5 raças, mas retornou {len(data)}."
