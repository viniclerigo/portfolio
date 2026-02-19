#getAccounts.py

import pandas as pd
import requests


# Função de coleta de accounts
def getAccounts(base_url, headers):
    """
    Coleta todas as accounts do CRM.

    Args:
        base_url (str): A URL base da API, incluindo parâmetros exceto o número da página.
        headers (dict): Os cabeçalhos da requisição, incluindo autorização.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário é um accounts. Retorna uma lista vazia em caso de erro.
    """
    
    print("--- Iniciando a coleta de accounts ---")

    while True:
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            accounts = data.get("accounts", [])

        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP crítico: {http_err} | URL: {base_url}")
            return [] # Retorna lista vazia para indicar falha
        except requests.exceptions.RequestException as req_err:
            print(f"Erro de conexão: {req_err}")
            return [] # Retorna lista vazia para indicar falha
        except ValueError:
            print("Erro: A resposta não é um JSON válido.")
            return [] # Retorna lista vazia para indicar falha

        print(f"--- Coleta finalizada. Total de {len(accounts)} accounts obtidos. ---\n")
        return accounts
    

# Função de tratamento da tabela de accounts
def trataAccounts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas as transformações de limpeza e padronização no DataFrame de accounts.
    
    Args:
        Accounts (DataFrame): O DataFrame que contém os accounts sem tratamento.
    
    Returns:
        DataFrame: Um Dataframe com os accounts tratados.
    
    """
    print("Processando DataFrame...")

    # Lista de colunas para manter no dataframe
    manter = ["id", "type", "name", "description", "emails", "addresses", "phones", "href", "revenue",
              "employeeCount", "htmlUrl", "id_creator", "id_owner", "id_territory", "id_tags",
              "id_followup", "id_recurringTask", "id_contacts", "id_accountType", "id_industry"]

    # 1. Padrionização inicial das colunas
    df.columns = [col.replace(".", "_").replace("links_", "id_") for col in df.columns]

    # 2. Selecionando apenas colunas necessárias
    df = df[manter].copy()

    colunas_id = ["id", "id_creator", "id_owner", "id_territory", "id_tags", "id_followup",
                  "id_recurringTask", "id_contacts", "id_accountType", "id_industry"]
    # 3. Transformação dos IDs principais e dos accountsets (pipelines) em números (int64)
    for col in colunas_id:
        df[col] = pd.to_numeric(df[col].str.extract(r"(\d+)", expand=False), errors="coerce").astype("int64")
    
    return df

    
# Função que orquestra a extração e tratamento e armazena o resultado tratado
def mainAccounts():
    base_url = "https://app.nutshell.com/rest/accounts"
    headers = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }
    output_filename = "accounts.json"
    output_path = f"assets/projetos/NutshellAPI/json/{output_filename}"

    try:
        # 1. Coleta de dados
        accounts_raw = getAccounts(base_url, headers=headers)
        if not accounts_raw:
                print("Nenhum stage retornado pela API. Encerrando.")
                return
        
        # 2. Normalização inicial
        df = pd.json_normalize(accounts_raw)

        # 3. Processamento e limpeza do DataFrame
        df_processado = trataAccounts(df)

        # 4. Armazenando resultado
        df_processado.to_json(output_path, orient="records", date_format="iso")
        print(f"Processo finalizado com sucesso! {len(df_processado)} registros salvos em '{output_filename}'.")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o processo: {e}")

# Bloco de teste da função.
if __name__ == "__main__":
    print("Executando getAccounts.py em modo de teste...")

    # mainAccounts()
    base_url = "https://app.nutshell.com/rest/accounts"
    headers = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }
    teste = getAccounts(base_url, headers=headers)

    df = pd.json_normalize(teste)
    # df.to_csv("assets/projetos/NutshellAPI/teste.csv")
    print(df.info())

    print("Accounts coletados, tratados e armazenados.")
