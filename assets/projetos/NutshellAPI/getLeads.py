# getLeads.py
import requests

def getLeads(base_url, headers, limit=100):
    """
    Coleta todos os leads do CRM.

    Args:
        base_url (str): A URL base da API, incluindo parâmetros exceto o número da página.
        headers (dict): Os cabeçalhos da requisição, incluindo autorização.
        limit (int): O número de registros por página, usado para determinar a última página.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário é um lead. Retorna uma lista vazia em caso de erro.
    """
    leads_list = []
    page = 0
    
    print("--- Iniciando coleta de leads ---")

    while True:
        try:
            full_url = f"{base_url}{page}"
            response = requests.get(full_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            temp_leads = data.get("leads", [])

            if not temp_leads:
                print("Nenhum lead encontrado nesta página. Encerrando a coleta.")
                break

            leads_list.extend(temp_leads)
            print(f"Página {page}: {len(temp_leads)} leads coletados. Total: {len(leads_list)}")

            if len(temp_leads) < limit:
                print("Última página alcançada.")
                break
            
            page += 1

        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP crítico: {http_err} | URL: {full_url}")
            return [] # Retorna lista vazia para indicar falha
        except requests.exceptions.RequestException as req_err:
            print(f"Erro de conexão: {req_err}")
            return [] # Retorna lista vazia para indicar falha
        except ValueError:
            print("Erro: A resposta não é um JSON válido.")
            return [] # Retorna lista vazia para indicar falha

    print(f"--- Coleta finalizada. Total de {len(leads_list)} leads obtidos. ---\n")
    return leads_list

# Opcional: Bloco para testar o módulo de forma independente
if __name__ == "__main__":
    print("Executando getLeads.py em modo de teste...")
    
    TEST_URL = "https://app.nutshell.com/rest/leads?sort=-age&page[limit]=100&page[page]="
    TEST_HEADERS = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }

    leads_result = getLeads(TEST_URL, TEST_HEADERS)

    if leads_result:
        print(f"\nTeste bem-sucedido! {len(leads_result)} leads foram coletados.")
        # print("Amostra do primeiro lead:", leads_result[0])
