import pandas as pd
import os
from datetime import datetime

def gerar_dashboard_json(arquivo_saida='dashboard_data.json'):
    """
    Lê todos os CSVs da pasta 'data', consolida as informações de vendas
    e gera um único arquivo JSON otimizado para o dashboard.
    """
    try:
        # Define o caminho relativo à localização do script
        diretorio_script = os.path.dirname(os.path.abspath(__file__))
        pasta_dados = os.path.join(diretorio_script, 'data')

        # Carrega todos os datasets
        df_vendas = pd.read_csv(os.path.join(pasta_dados, 'vendas.csv'))
        df_itens = pd.read_csv(os.path.join(pasta_dados, 'itens_venda.csv'))
        df_clientes = pd.read_csv(os.path.join(pasta_dados, 'clientes.csv'))
        df_usuarios = pd.read_csv(os.path.join(pasta_dados, 'usuarios.csv'))
        df_produtos = pd.read_csv(os.path.join(pasta_dados, 'produtos.csv'))

    except FileNotFoundError as e:
        print(f"Erro: Arquivo não encontrado. Certifique-se que todos os CSVs estão na pasta 'data'.")
        print(f"Detalhe do erro: {e}")
        return

    # --- 1. Preparação e Unificação dos Dados ---
    
    # Converte colunas de data para o formato datetime
    df_vendas['data_venda'] = pd.to_datetime(df_vendas['data_venda'])
    
    # Junta (merge) todas as tabelas para criar uma visão completa
    # Usamos os campos de ID para conectar as informações
    df_completo = pd.merge(df_itens, df_vendas, on='id_venda')
    df_completo = pd.merge(df_completo, df_produtos, on='id_produto')
    df_completo = pd.merge(df_completo, df_usuarios, on='id_usuario')
    df_completo = pd.merge(df_completo, df_clientes, on='id_cliente')
    
    # --- 2. Criação de Colunas para Análise e Filtros ---
    
    # Extrai ano, mês e trimestre da data da venda
    df_completo['ano'] = df_completo['data_venda'].dt.year
    df_completo['mes'] = df_completo['data_venda'].dt.month
    df_completo['trimestre'] = df_completo['data_venda'].dt.quarter

    # --- 3. Agregação dos Dados ---
    
    # Define as colunas pelas quais queremos agrupar os dados
    colunas_agrupamento = [
        'ano', 'trimestre', 'mes', 
        'regiao', 'canal_aquisicao', 
        'nome_usuario', 'nome_servico'
    ]
    
    # Agrupa os dados e soma o valor de cada item vendido
    df_agregado = df_completo.groupby(colunas_agrupamento, as_index=False)['valor_total'].sum()
    
    # Renomeia a coluna de valor para um nome mais claro
    df_agregado.rename(columns={'valor_total': 'faturamento'}, inplace=True)
    
    # Renomeia a coluna de região para colocar o ~
    # df_agregado.rename(columns={'regiao': 'região'}, inplace=True)

    # --- 4. Exportação para JSON ---

    # Define o caminho final do arquivo JSON de saída
    caminho_saida = os.path.join(pasta_dados, arquivo_saida)
    
    # Salva o DataFrame agregado em um arquivo JSON
    # 'orient=records' cria uma lista de dicionários, ideal para JavaScript
    # 'force_ascii=False' garante a correta codificação de caracteres especiais (como acentos)
    df_agregado.to_json(caminho_saida, orient='records', indent=2, force_ascii=False)
    
    print("--------------------------------------------------")
    print(f"Sucesso! O arquivo do dashboard foi gerado em:")
    print(caminho_saida)
    print("--------------------------------------------------")

if __name__ == '__main__':
    gerar_dashboard_json()

