# getLeads.py
import pandas as pd
import requests

# Função para coleta de leads
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

# Função de tratamento da tabela de leads
def trataLeads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas as transformações de limpeza e padronização no DataFrame de leads.
    """
    # --- Constantes e Configurações ---
    colunas_deletar = [
        "type", "isCurrentUserWatching", "ownerType", "mcfxContactIds", "href", 
        "htmlUrl", "htmlUrlPath", "avatarUrl", "initials", "value_currency", 
        "value_formatted", "createdTime_absoluteLocalizedString", "createdTime_value", 
        "dueTime_absoluteLocalizedString", "dueTime_value", 
        "anticipatedClosedTime_absoluteLocalizedString", "anticipatedClosedTime_value",
        "links_files", "links_relatedFiles", "links_destinations", "links_productMaps", 
        "links_competitorMaps", "lastContactedTime_absoluteLocalizedString", 
        "lastContactedTime_value", "overdueTime_fromNowLocalizedString", 
        "overdueTime_value", "closedTime_absoluteLocalizedString", "closedTime_value"
    ]
    
    # 1. Padronização inicial de colunas
    df.columns = [col.replace('.', '_').replace('links_', 'id_') for col in df.columns]
    
    # 2. Limpeza de colunas
    df.drop(columns=colunas_deletar, errors='ignore', inplace=True)
    
    # 3. Tratamento de IDs principais
    df['id'] = pd.to_numeric(df['id'].str.extract(r'(\d+)', expand=False), errors='coerce').astype('Int64')

    # 4. Tratamento das colunas de ID (explode e extração)
    colunas_links = [col for col in df.columns if col.startswith('id_')]
    for col in colunas_links:
        # Garante que todos os valores sejam listas para o explode
        df[col] = df[col].apply(lambda x: x if isinstance(x, list) else ([x] if pd.notna(x) else []))
        df = df.explode(col)
        # Extrai o ID numérico
        df[col] = pd.to_numeric(df[col].str.extract(r'(\d+)', expand=False), errors='coerce').astype('Int64')
    
    # Após múltiplos explodes, é crucial resetar o índice uma vez
    df.reset_index(drop=True, inplace=True)

    # 5. Tratamento de colunas de data/hora
    colunas_datetime = [col for col in df.columns if any(sub in col.lower() for sub in ["time", "date"])]
    for col in colunas_datetime:
        df[col] = pd.to_datetime(df[col], unit="s", errors="coerce")

    # 6. Tratamento de colunas numéricas
    colunas_numericas = ["value_amount", "confidence"]
    for col in colunas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    return df

# Função que orquestra a extração e tratamento e salva o resultado tratado
def mainLeads():
    """
    Função principal que orquestra a coleta, tratamento e salvamento dos dados.
    """
    base_url = "https://app.nutshell.com/rest/leads?sort=-age&page[limit]=100&page[page]="
    headers = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }
    output_filename = 'leads.json'
    print("Iniciando processo de tratamento de leads...")
    try:
        # Coleta de Dados
        leads_raw = getLeads(base_url, headers)
        if not leads_raw:
            print("Nenhum lead retornado pela API. Encerrando.")
            return

        # Normalização inicial
        df = pd.json_normalize(leads_raw)
        
        # Processamento e Limpeza do DataFrame
        df_processado = trataLeads(df)
        
        # Salvamento do Resultado
        df_processado.to_json(output_filename, orient='records', date_format='iso')
        print(f"Processo finalizado com sucesso! {len(df_processado)} registros salvos em '{output_filename}'.")

    except FileNotFoundError:
        print("Erro: O arquivo 'getLeads.py' não foi encontrado. Verifique se ele está no mesmo diretório.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o processo: {e}")

# Bloco de teste da função.
if __name__ == "__main__":
    print("Executando getLeads.py em modo de teste...")
    
    mainLeads()