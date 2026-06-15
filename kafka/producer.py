from kafka import KafkaProducer
from dotenv import load_dotenv
import requests
import json
import os

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

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v:
    json.dumps(v).encode("utf-8")
)

total_sent = 0

for role in SEARCH_ROLES:

    print(f"\nFetching jobs for: {role}")

    url = (
        f"https://api.adzuna.com/v1/api/jobs/fr/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&what={role}"
        f"&results_per_page=10"
    )

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error for {role}: {response.status_code}")
        continue

    data = response.json()

    jobs = data.get("results", [])

    print(f"Found {len(jobs)} jobs")

    for job in jobs:

        message = {
            "job_id": str(job.get("id")),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "search_role": role
        }

        producer.send(
            "jobs_topic",
            value=message
        )

        total_sent += 1

        print(
            f"Sent [{role}] -> {message['title']}"
        )

producer.flush()

print(f"\nProducer completed ({total_sent} messages sent)")