#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE=$1

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

tail -n +2 "$INPUT_FILE" | while IFS=, read -r iter proc seed; do
    iter=$(echo "$iter" | tr -d '[:space:]')
    proc=$(echo "$proc" | tr -d '[:space:]')
    seed=$(echo "$seed" | tr -d '[:space:]')

    DAG_FILE="dag_${iter}_${proc}.dag"
    OUT_FOLDER="results_${iter}_${proc}"

    echo "# Generated DAG file" > "$DAG_FILE"
    echo "JOB estimate /jobs/estimate_pi.sub" >> "$DAG_FILE"
    echo "SCRIPT PRE estimate /jobs/gen_seeds.py $iter $proc $seed $OUT_FOLDER" >> "$DAG_FILE"
    echo "SCRIPT POST estimate /jobs/aggregate.py $OUT_FOLDER" >> "$DAG_FILE"

    echo "Executing the DAG file with Condor: $DAG_FILE"
    condor_submit_dag "$DAG_FILE"

    echo "Waiting for DAG $DAG_FILE to complete..."
    condor_wait "$DAG_FILE.dagman.log"
done

echo "All DAG executions complete."
