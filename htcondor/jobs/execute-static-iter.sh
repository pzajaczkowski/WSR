#!/bin/bash

WORK_DIR=""

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

    DAG_FILE="dag_${proc}_${iter}.dag"
    RESULT_FOLDER="./results_${proc}_${iter}"
    OUTPUT_FOLDER="./outputs/output_${proc}_${iter}"
    DAG_FOLDER="$OUTPUT_FOLDER/dags"

    mkdir -p "$OUTPUT_FOLDER"
    mkdir -p "$DAG_FOLDER"
    mkdir -p "$RESULT_FOLDER"

    echo "# Generated DAG file" > "$DAG_FILE"
    echo "JOB estimate $WORK_DIR/jobs/estimate_pi.sub" >> "$DAG_FILE"
    echo "SCRIPT PRE estimate $WORK_DIR/jobs/gen_seeds.py $iter $proc $seed $RESULT_FOLDER" >> "$DAG_FILE"
    echo "SCRIPT POST estimate $WORK_DIR/jobs/aggregate.py $RESULT_FOLDER" >> "$DAG_FILE"

    echo "Executing the DAG file with Condor: $DAG_FILE"
    start_time=$(date +%s%6N)
    condor_submit_dag "$DAG_FILE"
    condor_wait "$DAG_FILE.dagman.log"
    end_time=$(date +%s%6N)

    wall_clock_time=$((end_time - start_time))
    echo "$wall_clock_time" >> "$RESULT_FOLDER/wall_clock_time.txt"

    mv "$DAG_FILE" "$DAG_FOLDER"
    mv "$RESULT_FOLDER" "$OUTPUT_FOLDER"
    mv "$DAG_FILE."* "$DAG_FOLDER"

done

echo "All DAG executions complete 👍"