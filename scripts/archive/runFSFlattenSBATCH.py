#!/usr/bin/env python3
"""
Slurm submission version of the SWIF2 submitter used at JLab.

What it does:
  1) Finds input ROOT trees in dataDir matching your glob
  2) For each file:
       - generates a runnable script from your template (FSFlat_<run>.sh)
       - generates an sbatch wrapper (sbatch_FSFlat_<run>.sh)
       - submits the wrapper with sbatch
"""

import os
import glob
import re
import stat
import subprocess

# -----------------------------
# User config
# -----------------------------
workflow = "MC_pipkslamb_2018-08_SBT_FLATTEN"

baseDir = "/home/dbart013/work/gluex"
dataDir = "/home/dbart013/work/files/pipkslamb/mc/spring2018_500M/trees/"
baseOutputDir = "/home/dbart013/work/files/pipkslamb/mc/spring2018_500M/trees/flatten/"
scriptDir = os.path.join(baseOutputDir, "scripts")
slurmDir  = os.path.join(baseOutputDir, "slurm")   # sbatch wrappers go here
logDir    = os.path.join(baseOutputDir, "logs")    # stdout/stderr go here

template = os.path.join(baseDir, "scripts", "runFSFlattenSBATCH_TEMPLATE.sh")

# ---- Slurm resources (EDIT FOR ODU or other institution, JLab, etc.) ----
account = None        # possibly 'admin' or can be None/""
partition = "main" # likely needs change (e.g. "standard", "main", etc.)
constraint = None        # e.g. "el9" at JLab; probably None at ODU
cpus_per_task = 4
mem_gb = 10
time_hours = 12

# Submission behavior
dry_run = False          # set True to only generate scripts, not submit
nice_name_prefix = "FSFlat"  # Slurm job-name prefix

# File selection
pattern = os.path.join(dataDir, "tree_pipkslamb__B4_M16_M18_gen_amp_V2_042559_02?.root")
fileList = sorted(glob.glob(pattern))

# -----------------------------
# Helpers
# -----------------------------
def mkdir_p(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def make_executable(path: str) -> None:
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def slurm_time_string(hours: int) -> str:
    # Slurm accepts "HH:MM:SS" or "D-HH:MM:SS". Keep simple:
    return f"{hours:02d}:00:00"

def write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

# -----------------------------
# Main
# -----------------------------
mkdir_p(scriptDir)
mkdir_p(slurmDir)
mkdir_p(logDir)

if not fileList:
    raise SystemExit(f"No files matched: {pattern}")

for infile in fileList:
    m = re.search(r"tree_pipkslamb__B4_M16_M18_gen_amp_V2_(......)", infile)
    if not m:
        continue
    runNumber = m.group(1)

    m = re.search(r"tree_pipkslamb__B4_M16_M18_gen_amp_V2_(\d{6})_(\d{3})\.root$", infile)
    if not m:
        continue

    runNumber = m.group(1)    # e.g. "042559"
    fileNumber = m.group(2)   # e.g. "020", "021", "022"
    job_id = f"{runNumber}_{fileNumber}"

    outputDir = baseOutputDir
    mkdir_p(outputDir)

    # Per-file outputs
    outFile = os.path.join(
        outputDir,
        f"tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSflat_{job_id}.root"
    )

    # 1) Build the runnable job script from your template
    outScript = os.path.join(scriptDir, f"FSFlat_{job_id}.sh")
    with open(template, "r", encoding="utf-8") as TEMP:
        data = TEMP.read()
    data = data.replace("INFILE", infile)
    data = data.replace("OUTFILE", outFile)
    write_text(outScript, data)
    make_executable(outScript)

    # 2) Build sbatch wrapper
    job_name = f"{nice_name_prefix}_{job_id}"
    slurm_out = os.path.join(logDir, f"{job_name}.%j.out")
    slurm_err = os.path.join(logDir, f"{job_name}.%j.err")
    sbatch_script = os.path.join(slurmDir, f"sbatch_{job_name}.sh")

    header_lines = [
        "#!/usr/bin/env bash",
        "# Auto-generated sbatch wrapper",
        f"# workflow: {workflow}",
        "",
        f"#SBATCH --job-name={job_name}",
        f"#SBATCH --cpus-per-task={cpus_per_task}",
        f"#SBATCH --mem={mem_gb}G",
        f"#SBATCH --time={slurm_time_string(time_hours)}",
        f"#SBATCH --output={slurm_out}",
        f"#SBATCH --error={slurm_err}",
    ]

    # account/partition/constraint are cluster-specific; include only if set
    if account:
        header_lines.append(f"#SBATCH --account={account}")
    if partition:
        header_lines.append(f"#SBATCH --partition={partition}")
    if constraint:
        header_lines.append(f"#SBATCH --constraint={constraint}")

    # Body: run your generated script
    body_lines = [
        "",
        "set -euo pipefail",
        'echo "HOST: $(hostname)"',
        'echo "PWD:  $(pwd)"',
        'echo "DATE: $(date)"',
        "",
        f'echo "Running: {outScript}"',
        f'bash "{outScript}"',
        "",
        'echo "DONE: $(date)"',
    ]

    write_text(sbatch_script, "\n".join(header_lines + body_lines) + "\n")
    make_executable(sbatch_script)

    # 3) Submit
    if dry_run:
        print(f"[DRY RUN] Would submit: sbatch {sbatch_script}")
    else:
        res = subprocess.run(
            ["sbatch", sbatch_script],
            check=True,
            text=True,
            capture_output=True,
        )
        print(res.stdout.strip())

    print(f"Submitted run {job_id}  infile={os.path.basename(infile)}")

print("All jobs processed.")
