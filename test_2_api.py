import requests
import pytest

# URL da API
BASE_URL = "https://v2.jokeapi.dev/joke/Any"

@pytest.fixture
def default_params():
    """Fixture para parâmetros padrão."""
    return {"type": "single", "contains": "love"}  # Ajustei para termos mais genéricos, caso seja necessário.

def test_success_response_status_code(default_params):
    """
    Teste de sucesso: Verifica se a API retorna o status code 200 ou trata corretamente o caso de ausência de piadas.
    """
    response = requests.get(BASE_URL, params=default_params)
    if response.status_code == 400:
        error_data = response.json()
        assert error_data["code"] == 106, "Esperado erro 106 para piadas não encontradas."
    else:
        assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}."

def test_invalid_category():
    """
    Teste de erro: Simula o uso de uma categoria inválida.
    """
    invalid_url = "https://v2.jokeapi.dev/joke/InvalidCategory"
    response = requests.get(invalid_url)
    assert response.status_code == 400, f"Esperado status 400, mas recebeu {response.status_code}. Mensagem: {response.text}"

def test_response_contains_expected_keys(default_params):
    """
    Teste de verificação de dados: Valida se a resposta contém as chaves esperadas.
    """
    response = requests.get(BASE_URL, params=default_params)
    if response.status_code == 400:
        error_data = response.json()
        assert error_data["code"] == 106, "Esperado erro 106 para piadas não encontradas."
    else:
        assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}."
        data = response.json()
        expected_keys = {"category", "type", "joke", "id"}
        assert expected_keys.issubset(data.keys()), f"Faltam chaves esperadas: {expected_keys - set(data.keys())}"

def test_query_with_custom_word():
    """
    Teste de sucesso: Verifica se as piadas retornadas contêm a palavra especificada.
    """
    params = {"type": "single", "contains": "romance"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 400:
        error_data = response.json()
        assert error_data["code"] == 106, "Esperado erro 106 para piadas não encontradas."
    else:
        assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}."
        data = response.json()
        if "joke" in data:
            assert "romance" in data["joke"].lower(), "A piada não contém a palavra esperada ('romance')."

def test_fetch_two_part_joke():
    """
    Teste de sucesso: Verifica se uma piada do tipo 'twopart' retorna os campos esperados.
    """
    params = {"type": "twopart"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}."
    data = response.json()
    if data["type"] == "twopart":
        assert "setup" in data, "O campo 'setup' não está presente na resposta para piadas do tipo 'twopart'."
        assert "delivery" in data, "O campo 'delivery' não está presente na resposta para piadas do tipo 'twopart'."
