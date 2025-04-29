logs = sc.textFile("/data/small.log")

user = 'bob'

def host_time_for_user(line):
    cols = line.strip().split('\t')
    if len(cols) == 6 and cols[1] == user:
        return (cols[0], float(cols[5]))
    return None

host_times = (
    logs.map(host_time_for_user)
        .filter(lambda x: x is not None)
        .reduceByKey(lambda a, b: a + b)
        .collect()
)

print(f"Łączne czasy operacji użytkownika {user} na każdym hoście:")

host_times.sort(key=lambda x: x[1], reverse=True)

for host, total_time in host_times:
    print(f"{host}:\t {total_time}")
