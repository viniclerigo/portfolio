from faker import Faker
import pandas as pd
import random
import os

# Inicializa o Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

def gerar_clientes(num_clientes=500, arquivo_saida='clientes.csv'):
    """
    Gera uma lista de clientes com nomes de empresas realistas e
    dados aleatórios, salvando em um arquivo CSV.
    """
    # Listas fixas conforme solicitado
    canais_aquisicao = ['Meta', 'Google', 'Site']
    regioes = ['Sul', 'Sudeste', 'Centro-Oeste', 'Nordeste', 'Norte']
    
    clientes = []
    for id_cliente in range(1, num_clientes + 1):
        clientes.append({
            'id_cliente': id_cliente,
            'nome_cliente': fake.company(), # Gera um nome de empresa realista
            'região': random.choice(regioes),
            'canal_aquisicao': random.choice(canais_aquisicao),
            'data_cadastro': fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
        })
    
    df_clientes = pd.DataFrame(clientes)

    # --- Lógica para salvar o arquivo na pasta 'data' ---
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta_dados = os.path.join(diretorio_script, 'data')
    
    # if not os.path.exists(pasta_dados):
    #     os.makedirs(pasta_dados)

    caminho_arquivo = os.path.join(pasta_dados, arquivo_saida)
    df_clientes.to_csv(caminho_arquivo, index=False)
    
    print(f"Arquivo '{caminho_arquivo}' gerado com {num_clientes} clientes.")

if __name__ == '__main__':
    gerar_clientes()
