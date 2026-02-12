import pandas as pd

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