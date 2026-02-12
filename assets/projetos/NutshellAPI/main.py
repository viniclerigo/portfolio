import pandas as pd
from getLeads import *
from trataLeads import *

# --- 1. Configuração ---
BASE_URL = "https://app.nutshell.com/rest/leads?sort=-age&page[limit]=100&page[page]="
HEADERS = {
    "accept": "application/json",
    "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
}
OUTPUT_FILENAME = "leads_processados.json"

def main():
    """
    Função principal que orquestra a coleta, tratamento e salvamento dos dados.
    """
    print("Iniciando processo de tratamento de leads...")
    try:
        # Coleta de Dados
        leads_raw = getLeads(BASE_URL, HEADERS)
        if not leads_raw:
            print("Nenhum lead retornado pela API. Encerrando.")
            return

        # Normalização inicial
        df = pd.json_normalize(leads_raw)
        
        # Processamento e Limpeza do DataFrame
        df_processado = trataLeads(df)
        
        # Salvamento do Resultado
        df_processado.to_json(OUTPUT_FILENAME, orient='records', date_format='iso')
        print(f"Processo finalizado com sucesso! {len(df_processado)} registros salvos em '{OUTPUT_FILENAME}'.")

    except FileNotFoundError:
        print("Erro: O arquivo 'getLeads.py' não foi encontrado. Verifique se ele está no mesmo diretório.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o processo: {e}")

if __name__ == "__main__":
    main()
