CREATE TABLE IF NOT EXISTS raw_jobs (

    job_id VARCHAR(255) PRIMARY KEY,

    title TEXT,

    company TEXT,

    location TEXT,

    country TEXT,

    salary_min NUMERIC,

    salary_max NUMERIC,

    contract_type TEXT,

    created_date TIMESTAMP,

    description TEXT,

    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analytics_jobs (

    id SERIAL PRIMARY KEY,

    country TEXT,

    skill TEXT,

    job_count INTEGER,

    average_salary NUMERIC,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);