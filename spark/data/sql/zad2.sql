from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("zad2").getOrCreate()

logs = spark.read.csv("/data/small.log", sep="\t", inferSchema=True, header=False).toDF("host", "user", "col3", "col4", "col5", "time")

logs.createOrReplaceTempView("logs")

user = 'bob'

query = f"""
    SELECT 
        host, 
        SUM(time) AS total_time 
    FROM logs 
    WHERE user = '{user}' 
    GROUP BY host 
    ORDER BY total_time DESC
"""

host_times = spark.sql(query).collect()

print(f"Łączne czasy operacji użytkownika {user} na każdym hoście:")
for row in host_times:
    print(f"{row['host']}: {row['total_time']}")