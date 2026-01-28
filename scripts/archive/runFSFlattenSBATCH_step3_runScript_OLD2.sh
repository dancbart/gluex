#!/usr/bin/env bash
set -euo pipefail

BASE="/home/dbart013/work/files/pipkslamb/mc/spring2018_500M/trees/flatten"
LIST="$BASE/fileList.txt"
JOB="/home/dbart013/work/gluex/scripts/runFSFlattenSBATCH_step2_jobScriptForArray.sh"

N=$(wc -l < "$LIST")
echo "Total tasks in fileList: $N"

CHUNK=9000     # <= MaxJobCount (10000), leave headroom
MAXRUN=200     # your concurrency cap per chunk

for ((start=0; start<N; start+=CHUNK)); do
  end=$((start + CHUNK - 1))
  if (( end >= N )); then end=$((N-1)); fi

  echo "Submitting chunk: ${start}-${end} (max running %${MAXRUN})"
  sbatch --array=${start}-${end}%${MAXRUN} "$JOB"

  # avoid hammering the controller
  sleep 2
done

