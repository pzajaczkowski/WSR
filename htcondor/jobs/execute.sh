#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE=$1

# Read the input file line by line
while IFS=, read -r iter proc seed; do
    DAG_FILE="dag_$(basename "$iter")_$(basename "$proc").dag"
    OUT_FILE="results_$(basename "$iter")_$(basename "$proc")"
    echo "# Generated DAG file" > "$DAG_FILE"
    echo "JOB estimate /home/pdstudent/htcondor/jobs/estimate_pi.sub" >> "$DAG_FILE"
    echo "SCRIPT PRE estimate /home/pdstudent/htcondor/jobs/gen_seeds.py $(basename "$iter") $(basename "$proc") $(basename "$seed") $OUT_FILE)" >> "$DAG_FILE"
    echo "SCRIPT POST estimate /home/pdstudent/htcondor/jobs/aggregate.py $OUT_FILE" >> "$DAG_FILE"
    echo "Executing the DAG file with Condor $DAG_FILE to $OUT_FILE"
    condor_submit_dag "$DAG_FILE"
done < "$INPUT_FILE"

echo "DAG execution complete."
