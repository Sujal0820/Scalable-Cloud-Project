from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    hour,
    to_timestamp,
    date_format
)

# ---------------------------------
# Spark Session
# ---------------------------------

spark = SparkSession.builder \
    .appName("DevPulse Batch Analytics") \
    .getOrCreate()

# ---------------------------------
# Read Raw GitHub Events
# ---------------------------------

df = spark.read.json(
    "s3://devpulse-github-data-2026/raw-events/"
)

# ---------------------------------
# Flatten Required Columns
# ---------------------------------

events = df.select(

    col("event_type"),

    col("repository.full_name").alias("repository"),

    col("actor.username").alias("developer"),

    col("timestamps.github").alias("github_time")

)

events = events.withColumn(
    "github_time",
    to_timestamp("github_time")
)

# ---------------------------------
# Total Events Per Repository
# ---------------------------------

repo_stats = events.groupBy(

    "repository"

).agg(

    count("*").alias("events")

)

repo_stats.write.mode("overwrite").json(

    "s3://devpulse-github-data-2026/batch-layer/repository_stats/"

)

# ---------------------------------
# Event Distribution
# ---------------------------------

event_stats = events.groupBy(

    "event_type"

).agg(

    count("*").alias("count")

)

event_stats.write.mode("overwrite").json(

    "s3://devpulse-github-data-2026/batch-layer/event_stats/"

)

# ---------------------------------
# Hourly Activity
# ---------------------------------

hourly = events.withColumn(

    "hour",

    hour("github_time")

).groupBy(

    "hour"

).agg(

    count("*").alias("events")

)

hourly.write.mode("overwrite").json(

    "s3://devpulse-github-data-2026/batch-layer/hourly_activity/"

)

# ---------------------------------
# Daily Activity
# ---------------------------------

daily = events.withColumn(

    "day",

    date_format("github_time", "yyyy-MM-dd")

).groupBy(

    "day"

).agg(

    count("*").alias("events")

)

daily.write.mode("overwrite").json(

    "s3://devpulse-github-data-2026/batch-layer/daily_activity/"

)

# ---------------------------------
# Summary
# ---------------------------------

summary = events.agg(

    count("*").alias("total_events")

)

summary.write.mode("overwrite").json(

    "s3://devpulse-github-data-2026/batch-layer/summary/"

)

spark.stop()