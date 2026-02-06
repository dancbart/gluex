#!/usr/bin/env bash
set -euo pipefail

BASE="/home/dbart013/work/files/pipkslamb/mc/spring2018_500M/thrown/flatten"
LIST="$BASE/fileList.txt"
JOB="/home/dbart013/work/gluex/scripts/runFSFlattenSBATCH_step2_jobScriptForArray.sh"

N=$(wc -l < "$LIST")
echo "Total tasks in fileList: $N"

CHUNK=9000
MAXRUN=200

submit_with_retry () {
  local array_spec="$1"
  local tries=0
  local max_tries=12          # total retries
  local sleep_s=40            # initial backoff

  while true; do
    tries=$((tries+1))
    echo "sbatch --array=${array_spec}%${MAXRUN} ${JOB}  (try ${tries}/${max_tries})"

    # capture stderr to see the real reason, if it keeps failing
    out=$(sbatch --array="${array_spec}%${MAXRUN}" "$JOB" 2>&1) && {
      echo "$out"
      return 0
    }

    echo "sbatch failed: $out"

    if (( tries >= max_tries )); then
      echo "Giving up after ${max_tries} tries for array ${array_spec}."
      return 1
    fi

    echo "Sleeping ${sleep_s}s and retrying..."
    sleep "$sleep_s"
    # exponential backoff, capped
    sleep_s=$(( sleep_s < 300 ? sleep_s*2 : 300 ))
  done
}

for ((start=0; start<N; start+=CHUNK)); do
  end=$((start + CHUNK - 1))
  if (( end >= N )); then end=$((N-1)); fi

  array_spec="${start}-${end}"
  echo "Submitting chunk: ${array_spec} (max running %${MAXRUN})"

  submit_with_retry "$array_spec"

  # be kind to the controller between big submissions
  sleep 5
done

