from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("zad3").getOrCreate()

logs = spark.read.csv("/data/small.log", sep="\t", inferSchema=True, header=False).toDF("host", "user", "col3", "col4", "col5", "time")

logs.createOrReplaceTempView("logs")

user = 'bob'

query = f"""
    SELECT 
        l1.host, 
        CASE 
            WHEN total_time > 0 THEN (user_time / total_time) * 100
            ELSE 0
        END AS percentage
    FROM (
        SELECT 
            host, 
            SUM(time) AS total_time, 
            SUM(CASE WHEN user = '{user}' THEN time ELSE 0 END) AS user_time
        FROM logs
        GROUP BY host
    ) l1
    ORDER BY percentage DESC
"""

host_percentages = spark.sql(query).collect()

print(f"[Task 3] Procent czasu operacji użytkownika {user} na każdym hoście:")
for row in host_percentages:
    print(f"{row['host']}: {row['percentage']:.2f}%")