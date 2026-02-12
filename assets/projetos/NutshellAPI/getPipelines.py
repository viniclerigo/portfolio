#getPipelines.py
import requests

def getPipelines(base_url, headers):
    """
    Coleta todos os pipelines do CRM.

    Args:
        base_url (str): A URL base da API, incluindo parâmetros exceto o número da página.
        headers (dict): Os cabeçalhos da requisição, incluindo autorização.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário é um pipeline. Retorna uma lista vazia em caso de erro.
    """
    
    print("--- Iniciando a coleta de pipelines ---")

    while True:
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            pipelines = data.get("stagesets", [])

        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP crítico: {http_err} | URL: {base_url}")
            return [] # Retorna lista vazia para indicar falha
        except requests.exceptions.RequestException as req_err:
            print(f"Erro de conexão: {req_err}")
            return [] # Retorna lista vazia para indicar falha
        except ValueError:
            print("Erro: A resposta não é um JSON válido.")
            return [] # Retorna lista vazia para indicar falha

        print(f"--- Coleta finalizada. Total de {len(pipelines)} pipelines obtidos. ---\n")
        return pipelines

# Bloco de teste da função.
if __name__ == "__main__":
    print("Executando getPipelines.py em modo de teste...")

    TEST_URL = "https://app.nutshell.com/rest/stagesets"
    TEST_HEADERS = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }

    pipelines = getPipelines(TEST_URL, TEST_HEADERS)

    if pipelines:
        print(f"\nTeste bem sucedido! {len(pipelines)} pipelines foram coletados")
        print("Amostra do primeiro pipeline:", pipelines[0])
