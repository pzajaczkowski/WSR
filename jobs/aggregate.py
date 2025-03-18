#!/usr/bin/env python3
import glob

results_dir = "/jobs/results"
total_inside, total_points = 0, 0

for file in glob.glob(f"{results_dir}/result_*.txt"):
    with open(file, 'r') as f:
        inside, points = map(int, f.readlines())
        total_inside += inside
        total_points += points

if total_points > 0:
    print("Estimated value of Pi:", 4 * total_inside / total_points)
else:
    print("No results found.")
