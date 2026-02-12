import pandas as pd

df = pd.read_json('assets/projetos/NutshellAPI/leads_processados.json')

df.to_csv('teste.csv', index=False)

print("fim")