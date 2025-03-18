#!/usr/bin/python3
import glob
import sys

if len(sys.argv) != 2:
    print("Usage: aggregate.py <results_dir>")
    sys.exit(1)

results_dir = sys.argv[1]
total_inside, total_points, total_cpu_time = 0, 0, 0
results = []

for file in glob.glob(f"{results_dir}/result_*.txt"):
    with open(file, "r") as f:
        inside, points, exec_time = map(int, f.readlines())
        total_inside += inside
        total_points += points
        total_cpu_time += exec_time

with open(f"{results_dir}/final_result.txt", "w") as f:
    if total_points > 0:
        f.write(f"{4 * total_inside / total_points}\n{total_cpu_time}")
    else:
        f.write("Error: No results found.")


