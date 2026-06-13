from dotenv import load_dotenv
import pandas as pd
import os
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

connection_string = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string)

df = pd.read_csv("data/jobs_clean.csv")

existing_jobs = pd.read_sql(
    "SELECT job_id FROM raw_jobs",
    engine
)

existing_ids = set(existing_jobs["job_id"].astype(str))

df["job_id"] = df["job_id"].astype(str)

new_jobs = df[
    ~df["job_id"].isin(existing_ids)
]

print(f"Total jobs in CSV: {len(df)}")
print(f"New jobs to insert: {len(new_jobs)}")

if len(new_jobs) > 0:

    new_jobs.to_sql(
        "raw_jobs",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    print("New jobs inserted")

else:

    print("No new jobs found")