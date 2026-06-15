from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT_PATH = "/Users/emmacoco/Desktop/ETL & Pipeline Orch/Final_project/ai-job-market-pipeline"

default_args = {
    "owner": "Emma",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

dag = DAG(
    dag_id="ai_job_market_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    description="AI Job Market Analytics Pipeline",
)

extract_task = BashOperator(
    task_id="extract_jobs",
    bash_command=f'cd "{PROJECT_PATH}" && python etl/extract.py',
    dag=dag,
)

transform_task = BashOperator(
    task_id="transform_jobs",
    bash_command=f'cd "{PROJECT_PATH}" && python etl/transform.py',
    dag=dag,
)

load_task = BashOperator(
    task_id="load_jobs",
    bash_command=f'cd "{PROJECT_PATH}" && python etl/load.py',
    dag=dag,
)

analytics_task = BashOperator(
    task_id="build_analytics_tables",
    bash_command=f'''
    docker cp "{PROJECT_PATH}/sql/analytics.sql" postgres_jobs:/analytics.sql &&
    docker exec postgres_jobs psql -U admin -d jobs_db -f /analytics.sql
    ''',
    dag=dag,
)

quality_check_task = BashOperator(
    task_id="quality_check",
    bash_command="""
    docker exec postgres_jobs psql -U admin -d jobs_db -c 'SELECT COUNT(*) FROM raw_jobs;'
    """,
    dag=dag,
)

extract_task >> transform_task >> load_task >> analytics_task >> quality_check_task