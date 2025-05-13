logs_path = "/data/small.log"
logs = sc.textFile(logs_path)

lines_count = logs.count()
bob_count = logs.filter(lambda line: line.split("\t")[1] == "bob").count()
alice_count = logs.filter(lambda line: line.split("\t")[1] == "alice").count()
bob_total_time = (
    logs.filter(lambda line: line.split("\t")[1] == "bob")
    .map(
        lambda line: int(line.strip().split("\t")[5])
        if len(line.strip().split("\t")) == 6
        else 0
    )
    .reduce(lambda a, b: a + b)
)

print(f"Liczba linii w pliku: {lines_count}")
print(f"Liczba wpisów dla bob: {bob_count}")
print(f"Liczba wpisów dla alice: {alice_count}")
print(f"Łączny czas operacji dla boba: {bob_total_time}")
