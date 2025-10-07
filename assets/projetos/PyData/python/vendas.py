import pandas as pd
import random
import os
from datetime import datetime, timedelta

def gerar_vendas_melhorado(num_vendas=200, 
                            arquivo_saida_vendas='vendas.csv', 
                            arquivo_saida_itens='itens_venda.csv'):
    """
    Gera dados de vendas e seus itens, lendo os arquivos de usuários,
    clientes e produtos. O valor total da venda é calculado e armazenado
    na tabela de vendas resumida.
    """
    # --- Lógica para encontrar os arquivos na pasta 'data' ---
    try:
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        pasta_dados = os.path.join(diretorio_script, 'data')
        
        df_usuarios = pd.read_csv(os.path.join(pasta_dados, 'usuarios.csv'))
        df_clientes = pd.read_csv(os.path.join(pasta_dados, 'clientes.csv'))
        df_produtos = pd.read_csv(os.path.join(pasta_dados, 'produtos.csv'))

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado. Certifique-se que os arquivos necessários estão na pasta 'data'.")
        print(f"Detalhe: {e}")
        return

    # Converte a coluna de data para o formato datetime para fazer comparações
    df_clientes['data_cadastro'] = pd.to_datetime(df_clientes['data_cadastro'])

    lista_vendas = []
    lista_itens_venda = []
    id_item_venda_counter = 1

    print(f"Gerando {num_vendas} vendas com consolidação de valor total...")

    # Loop para criar cada venda
    for id_venda in range(1, num_vendas + 1):
        # 1. Seleciona os participantes da venda (cliente e vendedor)
        cliente = df_clientes.sample(n=1).iloc[0]
        usuario = df_usuarios.sample(n=1).iloc[0]
        
        # 2. Define a data da venda (sempre após o cadastro do cliente)
        data_minima_venda = cliente['data_cadastro']
        dias_desde_cadastro = (datetime.now() - data_minima_venda).days
        dias_aleatorios = random.randint(0, dias_desde_cadastro)
        data_venda = data_minima_venda + timedelta(days=dias_aleatorios)
        
        # 3. Gera os itens da venda e calcula o valor total
        num_produtos_na_venda = random.randint(1, 3)
        produtos_vendidos = df_produtos.sample(n=num_produtos_na_venda)
        
        valor_total_venda = 0
        for _, produto in produtos_vendidos.iterrows():
            quantidade = 1 # Quantidade fixa
            valor_item = quantidade * produto['preco_unitario']
            valor_total_venda += valor_item
            
            # Adiciona o item à lista de itens_venda
            lista_itens_venda.append({
                'id_item_venda': id_item_venda_counter,
                'id_venda': id_venda,
                'id_produto': produto['id_produto'],
                'quantidade': quantidade,
                'valor_total': valor_item # Renomeado de valor_unitario para valor_total
            })
            id_item_venda_counter += 1

        # 4. Adiciona a venda consolidada à lista de vendas
        lista_vendas.append({
            'id_venda': id_venda,
            'data_venda': data_venda.strftime('%Y-%m-%d'),
            'id_cliente': cliente['id_cliente'],
            'id_usuario': usuario['id_usuario'],
            'valor_total_venda': round(valor_total_venda, 2)
        })

    # 5. Cria e salva os DataFrames
    df_vendas = pd.DataFrame(lista_vendas)
    df_itens_venda = pd.DataFrame(lista_itens_venda)

    caminho_vendas = os.path.join(pasta_dados, arquivo_saida_vendas)
    caminho_itens = os.path.join(pasta_dados, arquivo_saida_itens)
    
    df_vendas.to_csv(caminho_vendas, index=False)
    df_itens_venda.to_csv(caminho_itens, index=False)
    
    print(f"Arquivo '{caminho_vendas}' gerado com {len(df_vendas)} registros.")
    print(f"Arquivo '{caminho_itens}' gerado com {len(df_itens_venda)} registros.")

if __name__ == '__main__':
    gerar_vendas_melhorado()
