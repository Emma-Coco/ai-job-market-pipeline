# AI Job Market Analytics Pipeline

## Project Overview

This project implements an end-to-end data engineering pipeline for analyzing the Artificial Intelligence and Data Science job market.

The solution combines:

* Batch ETL processing
* SQL analytics transformations (ELT)
* Streaming data ingestion with Kafka
* Workflow orchestration with Airflow
* PostgreSQL data warehouse
* Interactive dashboard with Streamlit and Plotly

The objective is to collect, process, store and visualize AI/Data job offers while demonstrating modern data engineering concepts.

---

# Architecture

The project consists of two complementary pipelines.

## Batch Pipeline

Adzuna API → Extract → Transform → Load → PostgreSQL → Analytics → Dashboard

The batch pipeline is orchestrated by Apache Airflow and processes job offers periodically.

### Workflow

1. Extract job offers from the Adzuna API
2. Clean and normalize the data
3. Load records into PostgreSQL
4. Build analytics tables using SQL transformations
5. Display insights in Streamlit

---

## Streaming Pipeline

Producer → Kafka Topic → Consumer → PostgreSQL → Dashboard

The streaming pipeline demonstrates near real-time ingestion using Apache Kafka.

### Workflow

1. Producer publishes job offers into a Kafka topic
2. Consumer listens continuously for new messages
3. Incoming records are stored in the `live_jobs` table
4. Dashboard displays streaming metrics

---

# Technology Stack

## Data Engineering

* Python
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

# Database Structure

## Raw Layer

### raw_jobs

Stores raw job offers extracted from the API.

Main fields:

* job_id
* title
* company
* location
* country
* salary_min
* salary_max
* contract_type
* created_date
* description
* search_role

---

## Streaming Layer

### live_jobs

Stores job offers received through Kafka.

Main fields:

* job_id
* title
* company
* search_role
* received_at

---

## Analytics Layer

Generated through `analytics.sql`.

Tables:

* company_statistics
* contract_statistics
* location_statistics
* seniority_statistics
* skills_frequency
* jobs_by_day

---

# Airflow Orchestration

The pipeline is automated using Apache Airflow.

DAG:

```
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
* Execution monitoring through Airflow UI

---

# Kafka Streaming

Kafka is used to demonstrate event-driven ingestion.

Components:

### Producer

Publishes job offers to Kafka.

### Topic

Receives job messages.

### Consumer

Consumes messages and stores them into PostgreSQL.

---

# Dashboard

The Streamlit dashboard provides:

### KPIs

* Total job offers
* Companies
* Locations
* Skills identified
* Live streamed jobs

### Visualizations

* Top recruiting companies
* Most requested skills
* Contract type distribution
* Seniority distribution
* Geographic distribution
* Job publication timeline

### Streaming Section

* Number of Kafka streamed jobs
* Latest streamed offers

---

# Running the Project

## Start Infrastructure

```bash
docker start postgres_jobs kafka zookeeper
```

## Launch Airflow

```bash
export AIRFLOW_HOME=$(pwd)/airflow

airflow standalone
```

## Launch Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Learning Objectives

This project demonstrates:

* ETL pipeline design
* ELT transformations
* Data warehousing principles
* Batch processing
* Streaming architectures
* Workflow orchestration
* Data visualization
* Dockerized infrastructure

---

# Author

Emma Coco

ESILV – Data Science & Artificial Intelligence

ETL & Pipeline Orchestration – Final Project
