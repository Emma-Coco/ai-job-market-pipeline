-- =====================================================
-- COMPANY STATISTICS
-- =====================================================

DROP TABLE IF EXISTS company_statistics;

CREATE TABLE company_statistics AS

SELECT
    company,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY company;


-- =====================================================
-- CONTRACT STATISTICS
-- =====================================================

DROP TABLE IF EXISTS contract_statistics;

CREATE TABLE contract_statistics AS

SELECT
    COALESCE(contract_type, 'unknown') AS contract_type,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY contract_type;


-- =====================================================
-- LOCATION STATISTICS
-- =====================================================

DROP TABLE IF EXISTS location_statistics;

CREATE TABLE location_statistics AS

SELECT
    location,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY location;


-- =====================================================
-- SENIORITY STATISTICS
-- =====================================================

DROP TABLE IF EXISTS seniority_statistics;

CREATE TABLE seniority_statistics AS

SELECT
    CASE
        WHEN title ILIKE '%lead%' THEN 'Lead'
        WHEN title ILIKE '%senior%' THEN 'Senior'
        WHEN title ILIKE '%junior%' THEN 'Junior'
        ELSE 'Mid'
    END AS seniority,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY seniority;


-- =====================================================
-- JOBS BY DAY
-- =====================================================

DROP TABLE IF EXISTS jobs_by_day;

CREATE TABLE jobs_by_day AS

SELECT
    DATE(created_date) AS job_date,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY DATE(created_date)
ORDER BY job_date;


-- =====================================================
-- SKILLS FREQUENCY
-- =====================================================

DROP TABLE IF EXISTS skills_frequency;

CREATE TABLE skills_frequency AS

SELECT
    skill,
    occurrences
FROM (
    VALUES
        (
            'Python',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%python%')
        ),

        (
            'SQL',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%sql%')
        ),

        (
            'AWS',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%aws%')
        ),

        (
            'Azure',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%azure%')
        ),

        (
            'GCP',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%gcp%')
        ),

        (
            'Docker',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%docker%')
        ),

        (
            'Kubernetes',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%kubernetes%')
        ),

        (
            'Kafka',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%kafka%')
        ),

        (
            'Airflow',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%airflow%')
        ),

        (
            'Spark',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%spark%')
        ),

        (
            'Databricks',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%databricks%')
        ),

        (
            'Snowflake',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%snowflake%')
        ),

        (
            'Power BI',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%power bi%')
        ),

        (
            'Tableau',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%tableau%')
        ),

        (
            'TensorFlow',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%tensorflow%')
        ),

        (
            'PyTorch',
            (SELECT COUNT(*) FROM raw_jobs
             WHERE description ILIKE '%pytorch%')
        )

) AS skills(skill, occurrences);