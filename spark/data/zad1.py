logs = sc.textFile("/data/small.log")

def bob_filter(line):
    return line.split('\t')[1] == 'bob'

def alice_filter(line):
    return line.split('\t')[1] == 'alice'

def extract_bob_time(line):
    cols = line.strip().split('\t')
    if len(cols) == 6:
        return int(cols[5])
    return 0

lines_count = logs.count()
bob_count = logs.filter(bob_filter).count()
alice_count = logs.filter(alice_filter).count()
bob_total_time = logs.filter(bob_filter).map(extract_bob_time).reduce(lambda a, b: a + b)

print(f"Liczba linii w pliku: {lines_count}")
print(f"Liczba wpisów dla bob: {bob_count}")
print(f"Liczba wpisów dla alice: {alice_count}")
print(f"Łączny czas operacji dla boba: {bob_total_time}")
