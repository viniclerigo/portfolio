import pandas as pd
import requests

BASE_URL = "https://app.nutshell.com/rest/stagesets"

HEADERS = {
        "accept": "application/json",
        "authorization": "Basic amltQGRlbW8ubnV0c2hlbGwuY29tOjQzYzc4OWQ0ODNmZDc2NTQ3YjFmMTU3ZTNjZjVlNTgwYjk1YjlkOGM="
    }

response = requests.get(BASE_URL, headers=HEADERS)

data = response.json()

pipelines = pd.json_normalize(data.get("stagesets"))
pipelines.columns = [col.replace(".", "_").replace("links_", "id_") for col in pipelines.columns]
pipelines["id"] = pd.to_numeric(pipelines["id"].str.extract(r"(\d+)", expand=False), errors="coerce").astype("int64")
pipelines["id_stages"] = pipelines["id_stages"].apply(lambda x: x if isinstance(x, list) else ([x] if pd.notna(x) else []))
pipelines = pipelines.explode("id_stages")
pipelines["id_stages"] = pd.to_numeric(pipelines["id_stages"].str.extract(r"(\d+)", expand=False), errors="coerce").astype("int64")