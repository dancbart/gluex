#!/usr/bin/env python3

import os
import subprocess
from subprocess import call

# --------------------------------------
# User configuration
# --------------------------------------
fitsToRun    = 5
workflow     = "fitTwoPiAngles_kspiplamb_v2"
baseDir      = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/"
scriptDir    = baseDir + "config"
outDir       = baseDir + "fits"
account      = "halld"
partition    = "production"
disk_space   = 2
mem_requested= 10
time_limit   = 12
NCORES       = "4"
constraint   = "el9"

# --------------------------------------
# Script setup
# --------------------------------------
if not os.path.exists(scriptDir):
    os.makedirs(scriptDir)

fitCommand = f"fit -r {fitsToRun} -c {scriptDir}/fit_TwoPiAngles.cfg"

# Create a small executable script that SWIF2 will run
outScript = os.path.join(scriptDir, "run_fit_job.sh")
with open(outScript, "w") as OUT:
    OUT.write("#!/bin/bash\n")
    OUT.write("set -e\n")
    OUT.write(f"cd {outDir}\n")
    OUT.write(f"{fitCommand}\n")
os.chmod(outScript, 0o755)

# --------------------------------------
# SWIF2 job submission
# --------------------------------------
stdout_path = f"/farm_out/dbarton/log_{workflow}.log"
stderr_path = f"/farm_out/dbarton/err_{workflow}.err"

cmd  = f"swif2 add-job -workflow {workflow} -account {account} -partition {partition}"
cmd += f" -name {workflow}"
cmd += f" -constraint {constraint}"
cmd += f" -stdout {stdout_path}"
cmd += f" -stderr {stderr_path}"
cmd += " -create"
cmd += f" -cores {NCORES}"
cmd += f" -disk {int(disk_space)}GB"
cmd += f" -ram {int(mem_requested)}GB"
cmd += f" -time {int(time_limit)}hours"
cmd += f" {outScript}"

# Submit
print(f"Submitting SWIF2 job for workflow '{workflow}'...\n")
call(cmd, shell=True, stdout=None)

print(f"Submitted job '{workflow}'\n")
print(f"  STDOUT: {stdout_path}")
print(f"  STDERR: {stderr_path}")
print(f"  Script: {outScript}")