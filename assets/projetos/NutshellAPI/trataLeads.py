import pandas as pd

# --- Constantes e Configurações ---
COLUNAS_DELETAR = [
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

def trataLeads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica todas as transformações de limpeza e padronização no DataFrame de leads.
    """
    # 1. Padronização inicial de colunas
    df.columns = [col.replace('.', '_').replace('links_', 'id_') for col in df.columns]
    
    # 2. Limpeza de colunas
    df.drop(columns=COLUNAS_DELETAR, errors='ignore', inplace=True)
    
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

