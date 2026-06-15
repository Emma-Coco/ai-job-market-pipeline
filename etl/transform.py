import json
import pandas as pd

with open("data/raw_jobs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

jobs = []


for job in data["results"]:

    jobs.append(
    {
        "job_id": job.get("id"),
        "title": job.get("title"),
        "search_role": job.get("search_role"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),

        "country": (
            job.get("location", {})
               .get("area", ["Unknown"])[0]
        ),

        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),

        "contract_type": job.get("contract_type"),

        "created_date": job.get("created"),

        "description": job.get("description"),
    }
)

df = pd.DataFrame(jobs)

print(df.head())

df.to_csv("data/jobs_clean.csv", index=False)

print("Clean data saved to data/jobs_clean.csv")