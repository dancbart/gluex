#!/usr/bin/python3

import os
import glob
import re
import time 
import os.path
import subprocess
from subprocess import call


FILES_PER_JOB = 500  # <-- change depending on how many files to process.  USAGE: Submit large 'chunks' of jobs so the batch system 'sees' a few big jobs instead of many small ones.  Example: Instead of 2,000 jobs, "FILES_PER_JOB=500" submits 2000/500 = 5 jobs.  This avoids penalties for inefficient use of resources.

baseDir = "/work/halld/home/dbarton/gluex"


#====================================================================================
# Comment / un-comment run period below
#====================================================================================

# -------------- Spring 2018 RECONSTRUCTED ---------------
# workflow = "pipkslamb_2018-01_FLATTEN_correctVersionXML"
# template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE.sh"
# dataDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/phaseSpace20260630_500M_correctVersionXML/root/trees/"
# baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/phaseSpace20260630_500M_correctVersionXML/root/trees/flatten/"
# fileBaseName = "tree_pipkslamb__B4_M16_M18_gen_amp_V2"
# fileList = glob.glob(dataDir + f"{fileBaseName}_04????_???.root")
# fileList = glob.glob(dataDir + f"{fileBaseName}_04255?_???.root")


# # -------------- Spring 2018 THROWN ---------------
workflow = "pipkslamb_2018-01_THROWN_FLATTEN_correctVersionXML"
template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE_THROWN.sh"
dataDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/phaseSpace20260630_500M_correctVersionXML/root/thrown/"
baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/phaseSpace20260630_500M_correctVersionXML/root/thrown/flatten/"
fileBaseName = "tree_thrown_gen_amp_V2"
fileList = glob.glob(dataDir + f"{fileBaseName}_04????_???.root")
# fileList = glob.glob(dataDir + "{fileBaseName}_04255?_???.root")

# # # -------------- Fall 2018 RECONSTRUCTED ---------------
# workflow = "pipkslamb_2018-08_FLATTEN"
# template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE.sh"
# dataDir = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/trees/"
# baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/trees/flatten/"
# fileBaseName = "tree_pipkslamb__B4_M16_M18_gen_amp_V2"
# fileList = glob.glob(dataDir + f"{fileBaseName}_05????_???.root")
# fileList = glob.glob(dataDir + "{fileBasename}_0517??_???.root")

# # -------------- Fall 2018 THROWN ---------------
# workflow = "pipkslamb_2018-08_THROWN_FLATTEN"
# template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE_THROWN.sh"
# dataDir = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/thrown/"
# baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/thrown/flatten/"
# fileBaseName = "tree_thrown_gen_amp_V2"
# fileList = glob.glob(dataDir + f"{fileBaseName}_05????_???.root")
# fileList = glob.glob(dataDir + "{fileBaseName}_0517??_???.root")

# # -------------- Spring 2020 RECONSTRUCTED ---------------
# workflow = "pipkslamb_2020-01_FLATTEN"
# template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE.sh"
# dataDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2020/phaseSpace20260606_400M/root/trees/"
# baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2020/phaseSpace20260606_400M/root/trees/flatten/"
# fileBaseName = "tree_pipkslamb__B4_M16_M18_gen_amp_V2"
# fileList = glob.glob(dataDir + f"{fileBaseName}_07????_???.root")
# fileList = glob.glob(dataDir + "{fileBaseName}_07????_???.root")

# -------------- Spring 2020 THROWN ---------------
# workflow = "pipkslamb_2020-01_THROWN_FLATTEN"
# template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE_THROWN.sh"
# dataDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2020/phaseSpace20260606_400M/root/thrown/"
# baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2020/phaseSpace20260606_400M/root/thrown/flatten/"
# fileBaseName = "tree_thrown_gen_amp_V2"
# fileList = glob.glob(dataDir + f"{fileBaseName}_07????_???.root")
# fileList = glob.glob(dataDir + "{fileBaseName}_07????_???.root")


#====================================================================================
# ------------- Same for all periods ----------------
#====================================================================================
scriptDir = baseOutputDir + "scripts"

account = "halld"
partition = "production"
experiment = "GlueX"
disk_space = 2
mem_requested = 2
time_limit = 4
NCORES = "1"
# NCORES = "4"

if not os.path.exists(scriptDir): os.makedirs(scriptDir)



# Filter to valid files first (matching the regex)
validFiles = []
for f in fileList:
    if re.search(fileBaseName + r'_(\d+)_(\d+)', f):
        validFiles.append(f)

# Chunk into groups of FILES_PER_JOB
chunks = [validFiles[i:i+FILES_PER_JOB] for i in range(0, len(validFiles), FILES_PER_JOB)]
print(f"Total files: {len(validFiles)}  →  {len(chunks)} jobs (up to {FILES_PER_JOB} files each)")

for chunkIdx, chunk in enumerate(chunks):

    # Build a wrapper script that loops over all files in this chunk
    outputDir = baseOutputDir
    if not os.path.exists(outputDir): os.makedirs(outputDir)

    outScript = scriptDir + "/FSFlat_chunk%04d.sh" % chunkIdx

    # Read the template once, then build a loop body for each file in the chunk
    with open(template, 'r') as TEMP:
        templateData = TEMP.read()

    scriptLines = ["#!/bin/bash", "set -e", ""]

    for f in chunk:
            match = re.search(fileBaseName + r'_(\d+)_(\d+)', f)
            if match is None:
                continue
            # fullTag    = match.group(1)  # e.g. gen_amp_V2_042551_001
            runNumber  = match.group(1)  # e.g. 042551
            fileNumber = match.group(2)  # e.g. 001

            outFile = outputDir + fileBaseName + "_FSflat_" + runNumber + "_" + fileNumber + ".root"

            jobData = templateData
            jobLines = jobData.splitlines()
            bodyLines = [l for l in jobLines if not l.startswith('#!')]
            body = "\n".join(bodyLines)
            body = body.replace('INFILE',  f)
            body = body.replace('OUTFILE', outFile)

            scriptLines.append("# --- %s_%s ---" % (runNumber, fileNumber))
            scriptLines.append(body)
            scriptLines.append("")

    with open(outScript, 'w') as OUT:
        OUT.write("\n".join(scriptLines))

    subprocess.call(["chmod", "777", outScript])

    # One swif2 job per chunk
    chunkLabel = "chunk%04d" % chunkIdx
    cmd  = "swif2 add-job -workflow %s -account %s -partition %s" % (workflow, account, partition)
    cmd += " -name %s_%s" % (workflow, chunkLabel)
    cmd += " -constraint el9"
    cmd += " -stdout /farm_out/dbarton/log_%s_%s.log" % (chunkLabel, workflow)
    cmd += " -stderr /farm_out/dbarton/err_%s_%s.err" % (chunkLabel, workflow)
    cmd += " -create -cores " + NCORES
    cmd += " -disk %dGB"  % int(disk_space)
    cmd += " -ram %dGB"   % int(mem_requested)
    cmd += " -time %dhours" % int(time_limit)
    cmd += " " + outScript
    call(cmd, shell=True)

    print("Submitted chunk %d  (%d files)" % (chunkIdx, len(chunk)))

# After all chunks are submitted, start the workflow
print("\nAll chunks submitted. Starting workflow...")
run_cmd  = "swif2 run %s" % (workflow)
call(run_cmd, shell=True)
print("Workflow %s started." % workflow)