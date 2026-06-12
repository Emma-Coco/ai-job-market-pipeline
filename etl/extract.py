from dotenv import load_dotenv
import os
import requests

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

url = (
    f"https://api.adzuna.com/v1/api/jobs/fr/search/1"
    f"?app_id={APP_ID}"
    f"&app_key={APP_KEY}"
    f"&what=Data Scientist"
    f"&results_per_page=5"
)

response = requests.get(url)

print("Status code:", response.status_code)

data = response.json()

print("Number of jobs:", len(data.get("results", [])))

for job in data.get("results", []):
    print("-" * 50)
    print("Title:", job.get("title"))
    print("Company:", job.get("company", {}).get("display_name"))
    print("Location:", job.get("location", {}).get("display_name"))