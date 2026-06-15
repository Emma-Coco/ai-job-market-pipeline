from kafka import KafkaProducer
import json
import pandas as pd

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v:
    json.dumps(v).encode("utf-8")
)

df = pd.read_csv("data/jobs_clean.csv")

for _, row in df.head(10).iterrows():

    message = {
        "job_id": str(row["job_id"]),
        "title": row["title"],
        "company": row["company"],
        "search_role": row["search_role"]
    }

    producer.send(
        "jobs_topic",
        value=message
    )

    print(
        f"Sent: {message['title']}"
    )

producer.flush()

print("Producer completed")