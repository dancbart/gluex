#!/usr/bin/env bash
set -euo pipefail

# ----------------------------
# User settings
# ----------------------------
INDIR="/home/dbart013/work/files/pipkslamb/mc/fall2018_500M/thrown/flatten/"
PATTERN="tree_thrown_gen_amp_V2_FSFlat_*.root"

# Final merged output:
OUTFINAL="${INDIR}tree_thrown_gen_amp_V2_FSFlat_ALL.root"

# Staging directory (will be created inside INDIR):
STAGEDIR="${INDIR}hadd_stage"

# How many input files per stage-1 hadd:
BATCH_SIZE=500

# Extra hadd flags:
# -f overwrite output, -k keep going if some inputs are bad
HADD_FLAGS="-f -k"

# ----------------------------
# Helpers
# ----------------------------
log() { echo "[$(date '+%F %T')] $*"; }

# ----------------------------
# Main
# ----------------------------
mkdir -p "$STAGEDIR"

# Collect inputs
# mapfile -t FILES < <(ls -1 "${INDIR}${PATTERN}" 2>/dev/null | LC_ALL=C sort)
mapfile -t FILES < <(
  find "$INDIR" -maxdepth 1 -type f -name "$PATTERN" -print | LC_ALL=C sort
)

N=${#FILES[@]}
if [[ "$N" -eq 0 ]]; then
  echo "No files matched: ${INDIR}${PATTERN}"
  exit 1
fi

log "Found $N input files"
log "Stage dir: $STAGEDIR"
log "Batch size: $BATCH_SIZE"
log "Final output: $OUTFINAL"

# Stage-1: hadd batches into stage files
stage_count=$(( (N + BATCH_SIZE - 1) / BATCH_SIZE ))
log "Stage-1 will produce $stage_count intermediate files"

for ((b=0; b<stage_count; b++)); do
  start=$(( b * BATCH_SIZE ))
  end=$(( start + BATCH_SIZE ))
  if (( end > N )); then end=$N; fi

  stage_out="${STAGEDIR}/stage1_${b}.root"

  # Skip if already created and non-empty (resume-friendly)
  if [[ -s "$stage_out" ]]; then
    log "Skipping existing: $stage_out"
    continue
  fi

  log "Building $stage_out from inputs [$start, $((end-1))]"

  # Build the hadd command with the slice of files
  # shellcheck disable=SC2068
  hadd $HADD_FLAGS "$stage_out" "${FILES[@]:start:end-start}"
done

# Stage-2 (and beyond): repeatedly hadd stage outputs until one file remains
current_glob="${STAGEDIR}/stage1_*.root"
round=2

while true; do
  mapfile -t STAGE_FILES < <(ls -1 $current_glob 2>/dev/null | LC_ALL=C sort || true)
  M=${#STAGE_FILES[@]}

  if [[ "$M" -eq 0 ]]; then
    echo "No stage files found for glob: $current_glob"
    exit 2
  fi

  if [[ "$M" -eq 1 ]]; then
    log "Only one intermediate remains: ${STAGE_FILES[0]}"
    log "Moving to final: $OUTFINAL"
    mv -f "${STAGE_FILES[0]}" "$OUTFINAL"
    log "Done."
    exit 0
  fi

  log "Round $round: reducing $M files"

  # Decide batch size for reduction rounds (can be larger than stage-1)
  # Keep it conservative to avoid open-file limits:
  REDUCE_BATCH=200

  next_prefix="${STAGEDIR}/stage${round}_"
  next_glob="${next_prefix}*.root"

  # Clean up any partial outputs from a previous interrupted run of this round
  # (optional; comment out if you prefer to keep them)
  # rm -f $next_glob 2>/dev/null || true

  next_count=$(( (M + REDUCE_BATCH - 1) / REDUCE_BATCH ))
  for ((b=0; b<next_count; b++)); do
    start=$(( b * REDUCE_BATCH ))
    end=$(( start + REDUCE_BATCH ))
    if (( end > M )); then end=$M; fi

    out="${next_prefix}${b}.root"
    if [[ -s "$out" ]]; then
      log "Skipping existing: $out"
      continue
    fi

    log "  -> $out from intermediates [$start, $((end-1))]"
    # shellcheck disable=SC2068
    hadd $HADD_FLAGS "$out" "${STAGE_FILES[@]:start:end-start}"
  done

  # Advance to next round
  current_glob="$next_glob"
  round=$((round + 1))
done

