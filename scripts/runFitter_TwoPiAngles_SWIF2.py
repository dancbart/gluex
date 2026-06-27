#!/usr/bin/python3

import os
from subprocess import call
from datetime import datetime

workflow      = "FIT_pipkslamb_TwoPiAngles"
timestamp     = datetime.today().strftime("%Y%m%d_%H%M%S")  # e.g. 20260601_143022

baseDir       = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/"
outputDir     = os.path.join(baseDir, "fits", "%s_%s" % (workflow, timestamp))
# configFile    = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/config/fit_TwoPiAngles_allPol.cfg"
configFile    = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/config/fit_TwoPiAngles_allPol_bkg.cfg"
num_fits      = 5

account       = "halld"
partition     = "production"
disk_space    = 6
mem_requested = 1
time_limit    = 5
NCORES        = "1" # change to 4 (or higher?) if script uses multi-threading.

# Create shared output directory (same folder for all fits)
os.makedirs(outputDir, exist_ok=True)

for fitNumber in range(1, num_fits + 1):

    # --- Write a per-fit wrapper bash script ---
    jobName    = "%s_fit%04d" % (workflow, fitNumber)
    scriptPath = os.path.join(outputDir, "run_fit_%04d.sh" % fitNumber)
    logFile    = "/farm_out/dbarton/log_%s.log" % jobName
    errFile    = "/farm_out/dbarton/err_%s.err" % jobName

    with open(scriptPath, "w") as f:
        f.write("#!/bin/bash\n\n")
        f.write("echo \"=== Fit %d of %d ===\"\n" % (fitNumber, num_fits))
        f.write("echo \"Start time: $(date '+%%Y-%%m-%%d %%H:%%M:%%S')\"\n")
        f.write("echo \"\"\n\n")
        f.write("cd %s\n\n" % outputDir)
        f.write("/work/halld/home/dbarton/software/halld_sim/src/.Linux_Alma9-x86_64-gcc11.5.0/programs/AmplitudeAnalysis/fit/fit -r %d -c %s\n\n" % (fitNumber, configFile))
        f.write("echo \"\"\n")
        f.write("echo \"End time:   $(date '+%%Y-%%m-%%d %%H:%%M:%%S')\"\n")
        f.write("echo \"=== Fit %d complete ===\"\n" % fitNumber)

    os.chmod(scriptPath, 0o755)

    # --- Submit one job per fit, all under the same workflow ---
    cmd  = "swif2 add-job -workflow %s -account %s -partition %s" % (workflow, account, partition)
    cmd += " -name %s"      % jobName
    cmd += " -constraint el9"
    cmd += " -stdout %s"    % logFile
    cmd += " -stderr %s"    % errFile
    cmd += " -create -cores " + NCORES
    cmd += " -disk %dGB"    % int(disk_space)
    cmd += " -ram %dGB"     % int(mem_requested)
    cmd += " -time %dhours" % int(time_limit)
    cmd += " " + scriptPath

    print("Submitting: %s -> %s" % (jobName, scriptPath))
    call(cmd, shell=True, stdout=None)

print("\nDone. Submitted %d jobs under workflow: %s" % (num_fits, workflow))
print("Output directory: %s" % outputDir)
print("Logs:             /farm_out/dbarton/log_%s_fit*.log" % workflow)

# --- Start the workflow ---
run_cmd = "swif2 run %s" % workflow
print("\nStarting workflow: %s" % workflow)
call(run_cmd, shell=True, stdout=None)

# import os
# from subprocess import call
# from datetime import datetime

# workflow      = "pipkslamb_FIt_TwoPiAngles_v1"
# date          = datetime.today().strftime("%Y%m%d")

# baseDir       = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/"
# outputDir     = os.path.join(baseDir, "fits", date)
# configFile    = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/config/fit_TwoPiAngles_allPol.cfg"  # <-- FILL IN MANUALLY!!
# num_fits      = 5

# account       = "halld"
# partition     = "production"
# disk_space    = 2         # bumped up since one job does all the work
# mem_requested = 10
# time_limit    = 12         # bumped up to cover full run
# NCORES        = "4"

# # Create output directory
# os.makedirs(outputDir, exist_ok=True)

# # --- Write a wrapper bash script that runs all fits sequentially ---
# scriptPath = os.path.join(outputDir, "run_all_fits.sh")
# with open(scriptPath, "w") as f:
#     f.write("#!/bin/bash\n\n")
#     f.write("set -e\n")  # stop on error
#     f.write("outputDir=\"%s\"\n\n" % outputDir)
#     for fitNumber in range(1, num_fits + 1):
#         # Each fit writes to its own subdirectory so you can check them as they finish
#         fitOutDir = os.path.join(outputDir, "fit_%04d" % fitNumber)
#         f.write("mkdir -p %s\n" % fitOutDir)
#         f.write("echo \"Starting fit %d of %d...\"\n" % (fitNumber, num_fits))
#         f.write("cd %s\n" % fitOutDir)
#         f.write("fit -r %d -c %s\n" % (fitNumber, configFile))
#         f.write("echo \"Fit %d complete.\"\n\n" % fitNumber)

# os.chmod(scriptPath, 0o755)

# # --- Submit ONE job that runs the wrapper script ---
# jobName = "%s_all_fits_%s" % (workflow, date)
# logFile = "/farm_out/dbarton/log_%s.log" % jobName
# errFile = "/farm_out/dbarton/err_%s.err" % jobName

# cmd  = "swif2 add-job -workflow %s -account %s -partition %s" % (workflow, account, partition)
# cmd += " -name %s"      % jobName
# cmd += " -constraint el9"
# cmd += " -stdout %s"    % logFile
# cmd += " -stderr %s"    % errFile
# cmd += " -create -cores " + NCORES
# cmd += " -disk %dGB"    % int(disk_space)
# cmd += " -ram %dGB"     % int(mem_requested)
# cmd += " -time %dhours" % int(time_limit)
# cmd += " " + scriptPath

# print("Submitting single job: %s" % jobName)
# print("Wrapper script: %s" % scriptPath)
# print("Output will appear incrementally in: %s" % outputDir)
# call(cmd, shell=True, stdout=None)