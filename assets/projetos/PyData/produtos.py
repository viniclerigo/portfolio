import pandas as pd
import os

def gerar_produtos(arquivo_saida='produtos.csv'):
    """
    Cria uma tabela fixa com 5 produtos/serviços e salva em um arquivo CSV.
    """
    # Lista de produtos/serviços com seus preços
    produtos_data = [
        {'id_produto': 1, 'nome_servico': 'Desenvolvimento de Software Sob Medida', 'descricao': 'Criação de solução de software personalizada.', 'preco_unitario': 150000.00},
        {'id_produto': 2, 'nome_servico': 'Desenvolvimento de Aplicativos (Mobile/Web)', 'descricao': 'Criação de aplicativos para iOS, Android e Web.', 'preco_unitario': 100000.00},
        {'id_produto': 3, 'nome_servico': 'Consultoria em Arquitetura de Software', 'descricao': 'Planejamento e desenho da estrutura técnica de sistemas.', 'preco_unitario': 50000.00},
        {'id_produto': 4, 'nome_servico': 'Alocação de Squads (Outsourcing)', 'descricao': 'Fornecimento de equipes de desenvolvimento completas.', 'preco_unitario': 100000.00},
        {'id_produto': 5, 'nome_servico': 'Manutenção e Suporte de Sistemas', 'descricao': 'Contratos de suporte e evolução de software legado.', 'preco_unitario': 10000.00}
    ]
    
    df_produtos = pd.DataFrame(produtos_data)

    # --- Lógica para salvar o arquivo na pasta 'data' ---
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta_dados = os.path.join(diretorio_script, 'data')
    
    if not os.path.exists(pasta_dados):
        os.makedirs(pasta_dados)

    caminho_arquivo = os.path.join(pasta_dados, arquivo_saida)
    df_produtos.to_csv(caminho_arquivo, index=False)
    
    print(f"Arquivo '{caminho_arquivo}' gerado com {len(produtos_data)} produtos.")

if __name__ == '__main__':
    gerar_produtos()
