import pytest
import requests
import time
from unittest.mock import patch

# URL da API
BASE_URL = "https://cat-fact.herokuapp.com/facts/random"

def make_request_with_retries(url, params, retries=3, delay=5):
    """
    Faz uma requisição com tentativas automáticas em caso de falha.
    """
    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response
        print(f"Tentativa {attempt + 1}/{retries} falhou. Código: {response.status_code}. Retentando em {delay}s...")
        time.sleep(delay)
    return response

@pytest.fixture
def default_params():
    """Fixture para parâmetros padrão."""
    return {"animal_type": "cat", "amount": 1}

@patch("requests.get")
def test_success_response_status_code(mock_get, default_params):
    """
    Teste de sucesso: Verifica se a API retorna o status code 200.
    """
    # Mock de uma resposta de sucesso
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"text": "Cats are great!"}

    # Faz a requisição
    response = make_request_with_retries(BASE_URL, params=default_params)
    assert response.status_code == 200, (
        f"Esperado status 200, mas recebeu {response.status_code}. Mensagem: {response.text}"
    )

@patch("requests.get")
def test_invalid_animal_type(mock_get):
    """
    Teste de erro: Simula o uso de um tipo de animal inválido.
    """
    # Mock de uma resposta de erro
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"error": "Invalid animal type"}

    params = {"animal_type": "dragon", "amount": 1}
    response = make_request_with_retries(BASE_URL, params=params)

    assert response.status_code in {200, 400}, (
        f"Status inesperado: {response.status_code}. Mensagem: {response.text}"
    )

    # Verifica se o erro foi sinalizado no JSON retornado
    if response.status_code == 200:
        data = response.json()
        assert "error" in data, "API não sinalizou erro para tipo de animal inválido."

@patch("requests.get")
def test_response_text_contains_keyword(mock_get):
    """
    Teste de verificação: Checa se o texto retornado contém palavras relacionadas a gatos.
    """
    # Mock de uma resposta válida
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"text": "Cats are amazing pets!"}

    params = {"animal_type": "cat", "amount": 1}
    response = make_request_with_retries(BASE_URL, params=params)
    assert response.status_code == 200, (
        f"Esperado status 200, mas recebeu {response.status_code}. Mensagem: {response.text}"
    )

    try:
        data = response.json()
        fact_text = data.get("text", "").lower()

        # Palavras-chave para verificação
        keywords = ["cat", "feline", "kitten"]
        assert any(keyword in fact_text for keyword in keywords), (
            f"O fato retornado não menciona palavras relacionadas a 'cat': {fact_text}"
        )
    except ValueError:
        assert False, "Resposta inesperada: Não foi possível parsear o JSON."
