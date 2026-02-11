#!/usr/bin/env bash
#SBATCH --job-name=FSFlat
#SBATCH --partition=main
#SBATCH --cpus-per-task=4
#SBATCH --mem=10G
#SBATCH --time=12:00:00
#SBATCH --output=/.bscratch/data/dbart013/files/pipkslamb/data/spring2020/flatten/logs/FSFlat_%A_%a.out
#SBATCH --error=/.bscratch/data/dbart013/files/pipkslamb/data/spring2020/flatten/logs/FSFlat_%A_%a.err
# Optional:
#SBATC H --account=YOUR_ACCOUNT

set -euo pipefail

BASE="/.bscratch/data/dbart013/files/pipkslamb/data/spring2020/flatten"
LIST="$BASE/fileList.txt"
TEMPLATE="/home/dbart013/work/gluex/scripts/runFSFlattenSBATCH_TEMPLATE.sh"

# ---- pick file for this array task ----
INFILE=$(sed -n "$((SLURM_ARRAY_TASK_ID+1))p" "$LIST")
if [[ -z "$INFILE" ]]; then
  echo "No file for task $SLURM_ARRAY_TASK_ID"
  exit 0
fi

# ---- build unique job id from filename ----
BN=$(basename "$INFILE")
if [[ "$BN" =~ tree_pipkslamb__B4_M16_M18_([0-9]{6})\.root$ ]]; then
#  JOBID="${BASH_REMATCH[1]}_${BASH_REMATCH[2]}"
  JOBID="${BASH_REMATCH[1]}"
else
  echo "Unexpected filename: $BN"
  exit 2
fi

OUTFILE="$BASE/tree_pipkslamb__B4_M16_M18_FSFlat_${JOBID}.root"

# ---- skip if already done (safe re-runs) ----
if [[ -s "$OUTFILE" ]]; then
  echo "Already exists, skipping: $OUTFILE"
  exit 0
fi

# ---- run in local scratch ----
RUNDIR="${SLURM_TMPDIR:-/tmp}/FSFlat_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
mkdir -p "$RUNDIR"
SCRIPT="$RUNDIR/FSFlat_${JOBID}.sh"

sed -e "s|INFILE|$INFILE|g" \
    -e "s|OUTFILE|$OUTFILE|g" \
    "$TEMPLATE" > "$SCRIPT"

chmod +x "$SCRIPT"
bash "$SCRIPT"

