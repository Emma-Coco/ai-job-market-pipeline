from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

SEARCH_ROLES = [
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "Machine Learning Engineer",
    "AI Engineer"
]

all_jobs = []

for role in SEARCH_ROLES:

    print(f"Fetching: {role}")

    url = (
        f"https://api.adzuna.com/v1/api/jobs/fr/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what={role}"
        f"&results_per_page=20"
    )

    response = requests.get(url)

    data = response.json()

    for job in data.get("results", []):

        job["search_role"] = role

        all_jobs.append(job)

print(f"Total jobs collected: {len(all_jobs)}")

os.makedirs("data", exist_ok=True)

with open(
    "data/raw_jobs.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        {"results": all_jobs},
        f,
        ensure_ascii=False,
        indent=4
    )

print("Raw data saved")