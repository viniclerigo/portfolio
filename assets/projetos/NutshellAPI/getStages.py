#getStages.py

import pandas as pd
import requests


# Função de coleta de stages
def getStages(base_url, headers):
    """
    Coleta todos os stages do CRM.

    Args:
        base_url (str): A URL base da API, incluindo parâmetros exceto o número da página.
        headers (dict): Os cabeçalhos da requisição, incluindo autorização.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário é um stages. Retorna uma lista vazia em caso de erro.
    """
    
    print("--- Iniciando a coleta de stages ---")

    while True:
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()

            data = response.json()
            stages = data.get("stages", [])

        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP crítico: {http_err} | URL: {base_url}")
            return [] # Retorna lista vazia para indicar falha
        except requests.exceptions.RequestException as req_err:
            print(f"Erro de conexão: {req_err}")
            return [] # Retorna lista vazia para indicar falha
        except ValueError:
            print("Erro: A resposta não é um JSON válido.")
            return [] # Retorna lista vazia para indicar falha

        print(f"--- Coleta finalizada. Total de {len(stages)} stages obtidos. ---\n")
        return stages
    

# Função de tratamento da tabela de stages
def trataStages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas as transformações de limpeza e padronização no DataFrame de stages.
    
    Args:
        Stages (DataFrame): O DataFrame que contém os stages sem tratamento.
    
    Returns:
        DataFrame: Um Dataframe com os stages tratados.
    
    """
    print("Processando DataFrame...")

    # Lista de colunas para manter no dataframe
    manter = ["id", "type", "name", "description", "position", "id_stageset"]

    # 1. Padrionização inicial das colunas
    df.columns = [col.replace(".", "_").replace("links_", "id_") for col in df.columns]

    # 2. Selecionando apenas colunas necessárias
    df = df[manter].copy()

    # 3. Transformação dos IDs principais e dos stagesets (pipelines) em números (int64)
    df["id"] = pd.to_numeric(df["id"].str.extract(r"(\d+)", expand=False), errors="coerce").astype("int64")
    df["id_stageset"] = pd.to_numeric(df["id_stageset"].str.extract(r"(\d+)", expand=False), errors="coerce").astype("int64")
    
    return df

    
# Função que orquestra a extração e tratamento e armazena o resultado tratado
def mainStages():
    base_url = "https://app.nutshell.com/rest/stages"
    headers = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }
    output_filename = 'stages.json'

    try:
        # 1. Coleta de dados
        stages_raw = getStages(base_url, headers=headers)
        if not stages_raw:
                print("Nenhum stage retornado pela API. Encerrando.")
                return
        
        # 2. Normalização inicial
        df = pd.json_normalize(stages_raw)

        # 3. Processamento e limpeza do DataFrame
        df_processado = trataStages(df)

        # 4. Salvando resultado
        df_processado.to_json(output_filename, orient='records', date_format='iso')
        print(f"Processo finalizado com sucesso! {len(df_processado)} registros salvos em '{output_filename}'.")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o processo: {e}")

# Bloco de teste da função.
if __name__ == "__main__":
    print("Executando getStages.py em modo de teste...")

    mainStages()

    print("Stages coletados, tratados e armazenados.")