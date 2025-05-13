logs_path = "/data/small.log"
logs = sc.textFile(logs_path)

# uncomment for second run
# logs.cache()

user = "bob"

host_times = (
    logs.map(lambda line: line.strip().split("\t"))
    .filter(lambda parts: len(parts) == 6 and parts[1] == user)
    .map(lambda parts: (parts[0], float(parts[5])))
    .reduceByKey(lambda a, b: a + b)
    .collect()
)

print(f"Łączne czasy operacji użytkownika {user} na każdym hoście:")

host_times.sort(key=lambda x: x[1], reverse=True)
for host, total_time in host_times:
    print(f"{host}:\t {total_time}")
