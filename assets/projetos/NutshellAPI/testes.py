import pandas as pd
# import requests

df = pd.read_json('pipelines.json')

# df.to_csv('teste.csv', index=False)

print(df)

print("fim")