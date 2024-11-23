# Testes de Integração de APIs Públicas - 4º Período ESBAM
- APIs Testadas

1. Random User API

Descrição: Gera perfis aleatórios de usuários com informações como nome,
localização, email, e foto de perfil.
- Testes Incluídos:
Validação do status code das respostas.
Verificação da estrutura dos dados retornados (chaves como name, location, email).
Teste com parâmetros adicionais como nacionalidade (nat) e número de resultados (results).

2. Joke API

Descrição: Retorna piadas em diferentes formatos (simples ou duas partes) e categorias variadas.
- Testes Incluídos:
Verificação do status code das respostas.
Validação de chaves esperadas na resposta (como category, type, joke, etc.).
Testes com palavras-chave personalizadas (contains) e categorias específicas.

3. Cat Facts API

Descrição: Fornece fatos curiosos sobre gatos.
- Testes Incluídos:
Validação do status code das respostas.
Teste com parâmetros inválidos, como tipo de animal (animal_type).
Checagem de palavras-chave nos fatos retornados.

4. Dog API

Descrição: Fornece informações detalhadas sobre várias raças de cães, como temperamento, peso, altura e expectativa de vida.
- Testes Realizados:
- Testes de Sucesso:
Verifica se a API retorna o status code 200 para requisições válidas.
Verifica se a resposta contém as informações esperadas para uma raça específica, como nome, origem e temperamento.
- Testes de Erro:
Verifica o comportamento da API para raças inválidas.
Testa se a API lida corretamente com parâmetros inválidos.
- Verificação de Dados:
Valida se a resposta contém as chaves esperadas no formato JSON.
Valida se o nome da raça corresponde ao esperado em consultas por nome (como "Pit Bull").

5. COVID-19 API

Descrição: Retorna dados atualizados sobre a pandemia de COVID-19, como casos, mortes e recuperados por país.
- Testes Incluídos:
Validação do status code.
Verificação da estrutura dos dados retornados (como cases, deaths, recovered).
Teste de dados de vacinação, se disponíveis.

# Requisitos
Python 
pip para gerenciar pacotes.

- Instalação das dependências listadas no arquivo (requirements.txt)