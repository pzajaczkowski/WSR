#!/usr/bin/python3
import sys
import random


def generate_seeds(num_seeds, seed):
    random.seed(seed)
    return [random.randint(1, 1_000_000_000_000) for _ in range(num_seeds)]


if len(sys.argv) != 3:
    print("Usage: generate_seeds.py <iterations> <num_seeds> <initial_seed>")
    sys.exit(1)

iterations = int(sys.argv[1])
num_seeds = int(sys.argv[2])
init_seed = int(sys.argv[3])

seeds = generate_seeds(num_seeds, init_seed)
with open("params.txt", "w") as f:
    for seed in seeds:
        f.write(f"{iterations}, {seed}\n")
