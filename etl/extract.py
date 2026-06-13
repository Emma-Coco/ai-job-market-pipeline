from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

url = (
    f"https://api.adzuna.com/v1/api/jobs/fr/search/1"
    f"?app_id={APP_ID}"
    f"&app_key={APP_KEY}"
    f"&what=Data Scientist"
    f"&results_per_page=20"
)

response = requests.get(url)

data = response.json()

os.makedirs("data", exist_ok=True)

with open("data/raw_jobs.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Raw data saved to data/raw_jobs.json")