# AI Job Market Analytics Pipeline

## GitHub Repository

🚀 **Project Repository**

**https://github.com/Emma-Coco/ai-job-market-pipeline**

This project implements an end-to-end Data Engineering pipeline for collecting, processing, analyzing, and visualizing Artificial Intelligence and Data Science job offers from the Adzuna API.

The solution combines Batch ETL, ELT analytics, Kafka streaming, Airflow orchestration, PostgreSQL storage, and a Streamlit dashboard.

---

# Project Overview

The objective of this project is to monitor the AI and Data Science job market by:

* Collecting job offers from the Adzuna API
* Cleaning and transforming the data using Apache Spark
* Loading the data into PostgreSQL
* Building analytics tables through SQL transformations
* Streaming live job offers using Apache Kafka
* Visualizing insights through a Streamlit dashboard

The project was developed as part of the **ETL & Pipeline Orchestration** course at **ESILV (MSc Data Science & Artificial Intelligence)**.

---

# Architecture

The project contains two complementary pipelines.

## Batch Pipeline (Airflow)

Adzuna API

↓

Extract

↓

Transform (Apache Spark)

↓

Load

↓

PostgreSQL

↓

Analytics SQL Layer

↓

Streamlit Dashboard

### Workflow

1. Extract job offers from the Adzuna API
2. Clean and normalize data using Apache Spark
3. Load cleaned records into PostgreSQL
4. Build analytics tables through SQL aggregations
5. Display insights through Streamlit

---

## Streaming Pipeline (Kafka)

Adzuna API

↓

Kafka Producer

↓

Kafka Topic

↓

Kafka Consumer

↓

PostgreSQL (live_jobs)

↓

Streamlit Dashboard

### Workflow

1. Producer fetches job offers
2. Producer publishes events to Kafka
3. Consumer listens continuously
4. Consumer stores messages into PostgreSQL
5. Dashboard displays near real-time metrics

---

# Architecture Diagram

![Architecture](docs/architecture.png)

---

# Technology Stack

## Data Engineering

* Python
* Apache Spark (PySpark)
* PostgreSQL
* Apache Kafka
* Apache Airflow
* Docker

## Analytics

* SQL
* Pandas

## Visualization

* Streamlit
* Plotly

---

# Project Structure

```text
ai-job-market-pipeline/
│
├── airflow/
│   └── jobs_pipeline.py
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── kafka/
│   ├── producer.py
│   └── consumer.py
│
├── sql/
│   ├── init.sql
│   └── analytics.sql
│
├── dashboard/
│   └── app.py
│
├── data/
│
├── docker-compose.yml
│
├── README.md
│
└── .env
```

---

# Data Flow

```text
Adzuna API
    ↓
extract.py
    ↓
raw_jobs.json
    ↓
transform.py (Spark)
    ↓
jobs_clean.csv
    ↓
load.py
    ↓
raw_jobs (PostgreSQL)
    ↓
analytics.sql
    ↓
Analytics Tables
    ↓
Streamlit Dashboard
```

---

# Database Structure

## Raw Layer

### raw_jobs

Stores cleaned job offers extracted from the API.

Fields:

* job_id
* title
* company
* location
* country
* salary_min
* salary_max
* contract_type
* created_date
* search_role

---

## Streaming Layer

### live_jobs

Stores job offers received through Kafka.

Fields:

* job_id
* title
* company
* search_role
* received_at

---

## Analytics Layer

Generated through analytics.sql.

Tables:

* company_statistics
* contract_statistics
* location_statistics
* seniority_statistics
* skills_frequency
* jobs_by_day

---

# Airflow Orchestration

The Batch pipeline is automated using Apache Airflow.

DAG:

```text
extract_jobs
      ↓
transform_jobs
      ↓
load_jobs
      ↓
build_analytics_tables
      ↓
quality_check
```

Features:

* Daily scheduling
* Task dependencies
* Retry mechanism
* Monitoring through Airflow UI

---

# Apache Spark Transformations

The transformation layer uses Apache Spark (PySpark).

Operations performed:

* JSON parsing
* Flattening nested structures
* Data cleaning
* Data normalization
* Null filtering
* Deduplication
* CSV generation

Although the dataset size remains moderate, Spark was integrated to demonstrate distributed processing concepts commonly used in production Data Engineering environments.

---

# ELT Analytics Layer

Analytics tables are generated through SQL transformations.

Examples:

* Top recruiting companies
* Contract type distribution
* Seniority distribution
* Skills frequency analysis
* Location analysis
* Job publication trends

This layer follows an ELT approach:

```text
Raw Data
    ↓
PostgreSQL
    ↓
SQL Transformations
    ↓
Analytics Tables
```

---

# Kafka Streaming

Kafka demonstrates near real-time ingestion.

## Producer

Fetches job offers from Adzuna and publishes events.

## Topic

Receives job events.

## Consumer

Consumes messages and stores them in PostgreSQL.

---

# Dashboard

The Streamlit dashboard provides:

## KPIs

* Total job offers
* Companies
* Locations
* Skills identified
* Live streamed jobs

## Visualizations

* Top recruiting companies
* Most requested skills
* Contract type distribution
* Seniority distribution
* Geographic distribution
* Job publication timeline

## Streaming Monitoring

* Kafka streamed jobs count
* Latest streamed offers

---

# Idempotency

The pipeline is designed to be idempotent.

Before inserting data into PostgreSQL, existing job identifiers are retrieved and compared with incoming records.

Only new job offers are inserted.

This allows the pipeline to be safely re-executed without creating duplicate records.

---

# Environment Variables

Create a `.env` file:

```env
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=jobs_db
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

---

# Running the Project

## Clone Repository

```bash
git clone https://github.com/Emma-Coco/ai-job-market-pipeline.git

cd ai-job-market-pipeline
```

---

## Start Infrastructure

```bash
docker compose up -d
```

Verify containers:

```bash
docker ps
```

---

## Configure Java (Spark)

MacOS:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)

export PATH="$JAVA_HOME/bin:$PATH"
```

---

## Run Batch ETL Manually

### Extract

```bash
python etl/extract.py
```

### Transform

```bash
python etl/transform.py
```

### Load

```bash
python etl/load.py
```

---

## Run Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow

airflow standalone
```

Airflow UI:

```text
http://localhost:8080
```

---

## Run Kafka Streaming

Terminal 1:

```bash
python kafka/consumer.py
```

Terminal 2:

```bash
python kafka/producer.py
```

---

## Launch Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

# Learning Objectives

This project demonstrates:

* ETL design
* ELT analytics
* Apache Spark transformations
* PostgreSQL data warehousing
* Kafka streaming
* Airflow orchestration
* Dashboard development
* Dockerized infrastructure
* Idempotent pipeline design

---

# Future Improvements

Potential future enhancements:

* Deploy on AWS
* Replace Python Consumer with Spark Structured Streaming
* Add dbt transformations
* Add Grafana monitoring
* Add salary trend analytics
* Add machine learning forecasting

---

# Author

**Emma Coco**

ESILV – Data Science & Artificial Intelligence

ETL & Pipeline Orchestration – Final Project

GitHub Repository:

https://github.com/Emma-Coco/ai-job-market-pipeline
