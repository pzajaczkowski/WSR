from pyspark.sql import SparkSession

logs_path = "/data/small.log"

spark = SparkSession.builder.appName("zad2").getOrCreate()

logs = spark.read.csv(logs_path, sep="\t", inferSchema=True, header=False).toDF(
    "host", "user", "col3", "col4", "col5", "time"
)

logs.createOrReplaceTempView("logs")

user = "bob"

print(f"Łączne czasy operacji użytkownika {user} na każdym hoście:")

query = f"""
    SELECT 
        host, 
        SUM(time) AS total_time 
    FROM logs 
    WHERE user = '{user}' 
    GROUP BY host 
    ORDER BY total_time DESC
"""
host_times = spark.sql(query).show()
