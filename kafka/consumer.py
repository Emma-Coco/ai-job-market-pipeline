from kafka import KafkaConsumer
from sqlalchemy import create_engine, text
import json

engine = create_engine(
    "postgresql://admin:admin@localhost:5432/jobs_db"
)

consumer = KafkaConsumer(
    "jobs_topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x:
    json.loads(x.decode("utf-8"))
)

print("Consumer started...")

for message in consumer:

    job = message.value

    print(job)

    with engine.connect() as conn:

        conn.execute(
            text(
                """
                INSERT INTO live_jobs
                (
                    job_id,
                    title,
                    company,
                    search_role
                )
                VALUES
                (
                    :job_id,
                    :title,
                    :company,
                    :search_role
                )
                ON CONFLICT (job_id)
                DO NOTHING
                """
            ),
            job
        )

        conn.commit()