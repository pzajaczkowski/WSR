logs = sc.textFile("/data/small.log")

user = "bob"

hosts_with_users_and_times = (
    logs.map(lambda line: line.strip().split("\t"))
    .filter(lambda parts: len(parts) == 6)
    .map(lambda parts: (parts[0], (parts[1], float(parts[5]))))
)

hosts_total_time = hosts_with_users_and_times.map(
    lambda x: (x[0], x[1][1])
).reduceByKey(lambda a, b: a + b)

host_user_total_time = (
    hosts_with_users_and_times.filter(lambda x: x[1][0] == user)
    .map(lambda x: (x[0], x[1][1]))
    .reduceByKey(lambda a, b: a + b)
)

percent_times = hosts_total_time.join(host_user_total_time).map(
    lambda x: (x[0], (x[1][1] / x[1][0] * 100))
)

print(f"Procent czasu operacji użytkownika {user} na każdym hoście:")
for host, percent in percent_times.collect():
    print(f"{host}: {percent:.2f}%")
