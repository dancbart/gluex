#!/usr/bin/python3

# from: /work/halld/home/ksaldan/fcal_timing/runDSelector.py

import os
import glob
import re
import time 
import os.path
import subprocess
from subprocess import call

attempt = "_v1"
analysisLaunch = "fall2018"
workflow = "pipkslamb_flatten_genAmp2_" + analysisLaunch + attempt

baseDir = "/work/halld/home/dbarton/gluex"
# dataDir = "/cache/halld/RunPeriod-2018-08/analysis/ver22/tree_pipkslamb__B4_M16_M18/merged"
# dataDir = "/cache/halld/RunPeriod-2018-01/analysis/ver23/tree_pipkslamb__B4_M16_M18/merged"
# dataDir = "/cache/halld/RunPeriod-2018-08/analysis/bggen/ver01/batch01/tree_pipkslamb/merged/"
dataDir = "/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/v2/root/trees/"
# baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/bggen/fall2018"
baseOutputDir = "/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/v2/root/trees/flatten/"
scriptDir = baseOutputDir + "scripts"
template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE.sh"
# envFile = "version.xml"
# -cores # check to see if 'flatten' can run in parallel.

account = "halld"
partition = "production"
experiment = "GlueX"
disk_space = 2
mem_requested = 10
time_limit = 12
NCORES = "4"

if not os.path.exists(scriptDir): os.makedirs(scriptDir)

# fileList = glob.glob(dataDir + "/tree_pipkslamb_??????.root")
# fileList = glob.glob(dataDir + "/tree_pipkslamb_05????.root")
fileList = glob.glob(dataDir + "tree_pipkslamb__B4_M16_M18_gen_amp_V2_*")

for i in range(len(fileList)):

  # runNumber = re.search('tree_pipkslamb__B4_M16_M18_(......)',fileList[i]).group(1)
  runNumber = re.search('tree_pipkslamb__B4_M16_M18_gen_amp_V2_051768_0(..)',fileList[i]).group(1)
  if re.search('tree_pipkslamb__B4_M16_M18_gen_amp_V2_051768_0(..)',fileList[i]) is None: 
    continue
  outputDir = baseOutputDir

  if not os.path.exists(outputDir): os.makedirs(outputDir)

  outScript = scriptDir + "/FSFlat_" + runNumber + ".sh"
  outFile = outputDir + "tree_pipkslamb__B4_M16_M18_gen_amp_V2_051768_FSflat_" + runNumber + ".root"
  with open(template,'r+') as TEMP:
    data = TEMP.read()
    data=data.replace('INFILE',fileList[i])
    data=data.replace('OUTFILE',outFile)	

  with open(outScript,'w+') as OUT:
    OUT.write(data)
    
  OUT.close()
  TEMP.close() 

  command = ["chmod","777",outScript]
  subprocess.call(command)

  cmd = "swif2 add-job -workflow %s -account %s -partition %s"%(workflow,account,partition)
  cmd += " -name %s"%(workflow)
  cmd += " -constraint el9"
  cmd += " -stdout /farm_out/dbarton/log_%s.log"%(runNumber + workflow)
  cmd += " -stderr /farm_out/dbarton/err_%s.err"%(runNumber + workflow)
  cmd += " -create -cores " + NCORES
  cmd += " -disk %dGB"%int(disk_space)
  cmd += " -ram %dGB"%int(mem_requested)
  cmd += " -time %dhours"%int(time_limit)
  cmd += " " + outScript  
  call(cmd, shell=True, stdout=None)

  print("Submitting " + "script with run number" + runNumber + "\n");