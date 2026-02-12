#getPipelines.py
import pandas as pd
import requests

# Função de coleta de pipelines
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

# Função de tratamento da tabela de pipelines
def trataPipelines(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas as transformações de limpeza e padronização no DataFrame de leads.
    
    Args:
        Pipelines (DataFrame): O DataFrame que contém os pipelines sem tratamento.
    
    Returns:
        DataFrame: Um Dataframe com os pipelines tratados.
    
    """
    print("Processando DataFrame...")

    # 1. Padrionização inicial das colunas
    df.columns = [col.replace(".", "_").replace("links_", "id_") for col in df.columns]
    
    # 2. Transformação dos IDs principais em números (int64)
    df["id"] = pd.to_numeric(df["id"].str.extract(r"(\d+)", expand=False), errors="coerce").astype("int64")
    
    # 3. Transformação para garantir que todos os valores dentro desta coluna sejam uma lista
    df["id_stages"] = df["id_stages"].apply(lambda x: x if isinstance(x, list) else ([x] if pd.notna(x) else []))
    
    # 4. Explode os valores em novas linhas
    df = df.explode("id_stages")
    
    # 5. Transformação dos IDs de stages em números (int64)
    df["id_stages"] = pd.to_numeric(df["id_stages"].str.extract(r"(\d+)", expand=False), errors="coerce").astype("int64")
    
    return df

# Função que orquestra a extração e tratamento e salva o resultado tratado
def mainPipelines():
    base_url = "https://app.nutshell.com/rest/stagesets"
    headers = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }
    output_filename = 'pipelines.json'

    try:
        # 1. Coleta de dados
        pipelines_raw = getPipelines(base_url, headers=headers)
        if not pipelines_raw:
                print("Nenhum pipeline retornado pela API. Encerrando.")
                return
        
        # 2. Normalização inicial
        df = pd.json_normalize(pipelines_raw)

        # 3. Processamento e limpeza do DataFrame
        df_processado = trataPipelines(df)

        # 4. Salvando resultado
        df_processado.to_json(output_filename, orient='records', date_format='iso')
        print(f"Processo finalizado com sucesso! {len(df_processado)} registros salvos em '{output_filename}'.")
    
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o processo: {e}")

# Bloco de teste da função.
if __name__ == "__main__":
    print("Executando getPipelines.py em modo de teste...")

    mainPipelines()