import pandas as pd
import random

def gerar_nome_usuario():
    nomes = ['Ana', 'Bruno', 'Carlos', 'Diana', 'Eduardo', 'Fernanda', 'Gustavo', 'Helena', 'Igor', 'Juliana']
    sobrenomes = ['Silva', 'Costa', 'Souza', 'Pereira', 'Oliveira', 'Lima', 'Gomes', 'Ribeiro', 'Alves', 'Nascimento']
    return f"{random.choice(nomes)} {random.choice(sobrenomes)}"

def gerar_usuarios(num_usuarios=10, arquivo_saida=r'C:\Users\vncle\OneDrive\Documents\vscode\portfolio\assets\projetos\PyData\data\usuarios.csv'):
    usuarios = []
    for id_usuario in range(1, num_usuarios + 1):
        nome_usuario = gerar_nome_usuario()
        meta_vendas = round(random.uniform(150000, 200000), 2)  # Meta entre 5k e 20k
        usuarios.append({
            'id_usuario': id_usuario,
            'nome_usuario': nome_usuario,
            'meta_vendas': meta_vendas
        })
    df_usuarios = pd.DataFrame(usuarios)
    df_usuarios.to_csv(arquivo_saida, index=False)
    print(f'Arquivo {arquivo_saida} gerado com {num_usuarios} usuários.')

if __name__ == '__main__':
    gerar_usuarios()
