from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("zad1").getOrCreate()

logs = spark.read.csv("/data/small.log", sep="\t", inferSchema=True, header=False).toDF("host", "user", "col3", "col4", "col5", "time")

logs.createOrReplaceTempView("logs")

lines_count = spark.sql("SELECT COUNT(*) AS count FROM logs").first()[0]
bob_count = spark.sql("SELECT COUNT(*) AS count FROM logs WHERE user = 'bob'").first()[0]
alice_count = spark.sql("SELECT COUNT(*) AS count FROM logs WHERE user = 'alice'").first()[0]
bob_total_time = spark.sql("SELECT SUM(time) AS total_time FROM logs WHERE user = 'bob'").first()[0]

print(f"Liczba linii w pliku: {lines_count}")
print(f"Liczba wpisów dla bob: {bob_count}")
print(f"Liczba wpisów dla alice: {alice_count}")
print(f"Łączny czas operacji dla boba: {bob_total_time}")