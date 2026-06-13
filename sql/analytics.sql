DROP TABLE IF EXISTS company_statistics;

CREATE TABLE company_statistics AS

SELECT
    company,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY company;



DROP TABLE IF EXISTS contract_statistics;

CREATE TABLE contract_statistics AS

SELECT
    COALESCE(contract_type, 'unknown') AS contract_type,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY contract_type;



DROP TABLE IF EXISTS country_statistics;

CREATE TABLE country_statistics AS

SELECT
    country,
    COUNT(*) AS job_count
FROM raw_jobs
GROUP BY country;