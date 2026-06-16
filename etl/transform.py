from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# =====================================================
# SPARK SESSION
# =====================================================

spark = (
    SparkSession.builder
    .appName("AIJobMarketTransform")
    .master("local[*]")
    .getOrCreate()
)

# =====================================================
# LOAD RAW JSON
# =====================================================

raw_df = (
    spark.read
    .option("multiline", "true")
    .json("data/raw_jobs.json")
)

# =====================================================
# EXPLODE RESULTS ARRAY
# =====================================================

jobs_df = raw_df.selectExpr("explode(results) as job")

# =====================================================
# FLATTEN JSON
# =====================================================

df = jobs_df.select(
    col("job.id").alias("job_id"),
    col("job.title").alias("title"),
    col("job.search_role").alias("search_role"),
    col("job.company.display_name").alias("company"),
    col("job.location.display_name").alias("location"),
    col("job.location.area")[0].alias("country"),
    col("job.salary_min").alias("salary_min"),
    col("job.salary_max").alias("salary_max"),
    col("job.contract_type").alias("contract_type"),
    col("job.created").alias("created_date")
)

# =====================================================
# BASIC CLEANING
# =====================================================

df = df.filter(
    col("job_id").isNotNull()
)

df = df.filter(
    col("title").isNotNull()
)

df = df.filter(
    col("company").isNotNull()
)

# =====================================================
# REMOVE DUPLICATES
# =====================================================

df = df.dropDuplicates(
    ["job_id"]
)

# =====================================================
# PREVIEW
# =====================================================

print("\nPreview transformed dataset:\n")

df.show(
    5,
    truncate=False
)

print(
    f"\nRows after transformation: {df.count()}"
)

import shutil
import glob

# =====================================================
# SAVE CSV
# =====================================================

output_dir = "data/jobs_clean_temp"

(
    df.coalesce(1)
    .write
    .mode("overwrite")
    .option("header", True)
    .csv(output_dir)
)

csv_file = glob.glob(
    f"{output_dir}/part-*.csv"
)[0]

shutil.copy(
    csv_file,
    "data/jobs_clean.csv"
)

print(
    "\nClean data saved to data/jobs_clean.csv"
)

# =====================================================
# STOP SPARK
# =====================================================

spark.stop()