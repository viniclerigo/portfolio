from faker import Faker
import pandas as pd
import random
import os

# Inicializa o Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

def gerar_usuarios(num_usuarios=10, arquivo_saida='usuarios.csv'):
    """
    Gera uma lista de usuários (consultores/vendedores) com nomes realistas
    e salva em um arquivo CSV.
    """
    usuarios = []
    for id_usuario in range(1, num_usuarios + 1):
        usuarios.append({
            'id_usuario': id_usuario,
            'nome_usuario': fake.name(), # Gera um nome completo realista
            'meta_vendas': round(random.uniform(150000, 200000), 0)
        })
    
    df_usuarios = pd.DataFrame(usuarios)

    # --- Lógica para salvar o arquivo na pasta 'data' ---
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta_dados = os.path.join(diretorio_script, 'data')
    
    # if not os.path.exists(pasta_dados):
    #     os.makedirs(pasta_dados)

    caminho_arquivo = os.path.join(pasta_dados, arquivo_saida)
    df_usuarios.to_csv(caminho_arquivo, index=False)
    
    print(f"Arquivo '{caminho_arquivo}' gerado com {num_usuarios} usuários.")

if __name__ == '__main__':
    gerar_usuarios()
