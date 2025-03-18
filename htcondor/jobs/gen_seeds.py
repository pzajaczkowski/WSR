#!/usr/bin/python3
import sys
import random
import os


def generate_seeds(num_seeds, seed):
    random.seed(seed)
    return [random.randint(1, 1_000_000_000_000) for _ in range(num_seeds)]

if len(sys.argv) != 5:
    print("Usage: generate_seeds.py <iterations> <num_seeds> <initial_seed> <results_folder>")
    sys.exit(1)

iterations = int(sys.argv[1])
num_seeds = int(sys.argv[2])
init_seed = int(sys.argv[3])
results_folder = sys.argv[4]

dir = f"{os.path.abspath(os.getcwd())}/{results_folder}"
if not os.path.isdir(dir):
   os.makedirs(dir)

seeds = generate_seeds(num_seeds, init_seed)
iterations_per_process = int(iterations/num_seeds)
with open("params.txt", "w") as f:
    for seed in seeds:
        f.write(f"{iterations_per_process}, {seed}, {results_folder}\n")
