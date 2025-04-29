logs = sc.textFile("/data/small.log")

user = "bob"


def host_with_users_and_times(line):
    fields = line.strip().split("\t")
    if len(fields) == 6:
        return (host, (fields[1], fields[5]))
    return None


hosts_with_users_and_times = (
    logs.map(host_with_users_and_times)
    .filter(lambda x: x is not None)
)

hosts_total_time = (
    hosts_with_users_and_times.map(lambda x: (x[0], x[1][1]))
    .reduceByKey(lambda a, b: a + b)
    .collectAsMap()
)
host_user_total_time = (
    host_user_times.filter(lambda x: x[1][0] == user)
    .map(lambda x: (x[0], x[1][1]))
    .reduceByKey(lambda a, b: a + b)
    .collectAsMap()
)
print(f"[Task 3] Procent czasu operacji użytkownika {user} na każdym hoście:")
for host in hosts_total_time:
    user_time = host_user_total_time.get(host, 0.0)
    total_time = hosts_total_time[host]
    percent = (user_time / total_time * 100) if total_time > 0 else 0
    print(f"{host}: {percent:.2f}%")
