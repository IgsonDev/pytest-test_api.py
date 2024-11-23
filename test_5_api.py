import pytest
import requests

# URL da API (dados sobre COVID-19)
BASE_URL = "https://disease.sh/v3/covid-19/countries"

@pytest.fixture
def default_params():
    """Fixture para parâmetros padrão."""
    return {"country": "Brazil"}  # Altere o país conforme necessário

def test_success_response_status_code(default_params):
    """
    Teste de sucesso: Verifica se a API retorna o status code 200.
    """
    response = requests.get(BASE_URL, params=default_params)
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}. Mensagem: {response.text}"

def test_covid_data_validity(default_params):
    """
    Teste de verificação: Verifica se os dados COVID-19 retornados são válidos.
    """
    response = requests.get(BASE_URL, params=default_params)
    data = response.json()

    # Verifica se os dados principais estão presentes
    assert "cases" in data[0], "Número de casos não encontrado."
    assert "deaths" in data[0], "Número de mortes não encontrado."
    assert "recovered" in data[0], "Número de recuperados não encontrado."

    # Verifica se dados de vacinação estão presentes, se disponível
    if "vaccinated" in data[0]:
        assert isinstance(data[0]["vaccinated"], int), "Dados de vacinação inválidos."
    else:
        print("Dados de vacinação não disponíveis para este país.")

def test_vaccination_data(default_params):
    """
    Teste de verificação: Verifica se os dados de vacinação estão presentes e são válidos.
    """
    response = requests.get(BASE_URL, params=default_params)
    data = response.json()

    # Verifica se a chave 'vaccinated' existe e é um número
    vaccinated = data[0].get("vaccinated")
    if vaccinated is not None:
        assert isinstance(vaccinated, int), f"Esperado número de vacinados, mas recebeu: {vaccinated}"
    else:
        print("Dados de vacinação não encontrados para este país.")

def test_data_for_another_country():
    """
    Teste para outro país (ex: EUA) para verificar se a API retorna dados corretamente.
    """
    params = {"country": "USA"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200, f"Esperado status 200, mas recebeu {response.status_code}. Mensagem: {response.text}"
    
    data = response.json()
    
    # Verificar a presença dos dados essenciais
    assert "cases" in data[0], "Número de casos não encontrado."
    assert "deaths" in data[0], "Número de mortes não encontrado."
    assert "recovered" in data[0], "Número de recuperados não encontrado."

    # Verificar dados de vacinação, se presentes
    if "vaccinated" in data[0]:
        assert isinstance(data[0]["vaccinated"], int), f"Esperado número de vacinados, mas recebeu: {data[0]['vaccinated']}"
    else:
        print("Dados de vacinação não encontrados para este país.")
