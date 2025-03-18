#!/bin/bash

N=5

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE=$1

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

RESULTS_DIR="final_results"
mkdir -p "$RESULTS_DIR"

cleanup() {
    echo "Cleaning up files..."
    rm -f dag_*
    rm -rf results_*
}

cleanup

tail -n +2 "$INPUT_FILE" | while IFS=, read -r iter proc seed; do
    iter=$(echo "$iter" | tr -d '[:space:]')
    proc=$(echo "$proc" | tr -d '[:space:]')
    seed=$(echo "$seed" | tr -d '[:space:]')

    FINAL_RESULT_FILE="$RESULTS_DIR/final_result_${iter}.txt"
    > "$FINAL_RESULT_FILE"

    for (( i=1; i<=N; i++ )); do
        new_seed=$((seed * i))

        DAG_FILE="dag_${iter}_${proc}_${i}.dag"
        OUT_FILE="results_${iter}_${proc}_${i}"

        echo "# Generated DAG file" > "$DAG_FILE"
        echo "JOB estimate /jobs/estimate_pi.sub" >> "$DAG_FILE"
        echo "SCRIPT PRE estimate /jobs/gen_seeds.py $iter $proc $new_seed $OUT_FILE" >> "$DAG_FILE"
        echo "SCRIPT POST estimate /jobs/aggregate.py $OUT_FILE" >> "$DAG_FILE"

        echo "Executing the DAG file with Condor: $DAG_FILE"
        condor_submit_dag "$DAG_FILE"

        echo "Waiting for DAG $DAG_FILE to complete..."
        condor_wait "$DAG_FILE.dagman.log"

        head -1 "$OUT_FILE/final_result.txt" >> "$FINAL_RESULT_FILE"

        cleanup
    done
done

echo "All DAG executions complete. Final results are in $FINAL_RESULTS_DIR."