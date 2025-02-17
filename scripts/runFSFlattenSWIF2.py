#!/usr/bin/python3

# from: /work/halld/home/ksaldan/fcal_timing/runDSelector.py

import os
import glob
import re
import time 
import os.path
import subprocess
from subprocess import call


baseDir = "/w/halld-scshelf2101/home/dbarton/gluex"
dataDir = "/cache/halld/RunPeriod-2018-08/analysis/ver23/tree_pi0kplamb__B4_M18/merged"
baseOutputDir = "/volatile/halld/home/dbarton/pi0kplamb"
scriptDir = baseOutputDir + "/scripts"
logDir = scriptDir + "/log"
template = baseDir + "/scripts/runFSFlattenSWIF2_TEMPLATE.sh"
envFile = "version.xml"
# -cores # check to see if 'flatten' can run in parallel.

attempt = "_v12"
workflow = "pi0kplamb_flatten" + attempt
account = "halld"
partition = "production"
experiment = "GlueX"
disk_space = 2
mem_requested = 10
time_limit = 12
NCORES = "4"

if not os.path.exists(scriptDir): os.makedirs(scriptDir)
# if not os.path.exists(logDir): os.makedirs(logDir)

fileList = glob.glob(dataDir + "/tree_pi0kplamb__B4_M18_05172?.root")

for i in range(len(fileList)):

  runNumber = re.search('tree_pi0kplamb__B4_M18_(......)',fileList[i]).group(1)
  if re.search('tree_pi0kplamb__B4_M18_(......)',fileList[i]) is None: 
    continue
  # outputDir = baseOutputDir + "/flatten"
  outputDir = baseOutputDir + "/flatten"

  if not os.path.exists(outputDir): os.makedirs(outputDir)

  script = scriptDir + "/FSFlat_" + runNumber + ".sh"
  outFile = outputDir + "/pi0kplamb_2018-08_B4_M18_FSflat_" + runNumber + ".root"
  with open(template,'r+') as TEMP:
    data = TEMP.read()
    data=data.replace('INFILE',fileList[i])
    data=data.replace('OUTFILE',outFile)	

  with open(script,'w+') as OUT:
    OUT.write(data)
    
  OUT.close()
  TEMP.close() 

  command = ["chmod","777",script]
  subprocess.call(command)

  cmd = "swif2 add-job -workflow %s -account %s -partition %s"%(workflow,account,partition)
  cmd += " -name %s"%(workflow)
  cmd += " -constraint el9"
  cmd += " -stdout /farm_out/dbarton/log_%s.log"%(runNumber + workflow)
  # cmd += " -stdout /w/halld-scshelf2101/home/dbarton/gluex/scripts/log/log_%s.log"%(runNumber + attempt)
  cmd += " -stderr /farm_out/dbarton/err_%s.err"%(runNumber + workflow)
  # cmd += " -stderr /w/halld-scshelf2101/home/dbarton/gluex/scripts/log/err_%s.err"%(runNumber + attempt)
  cmd += " -create -cores " + NCORES
  cmd += " -disk %dGB"%int(disk_space)
  cmd += " -ram %dGB"%int(mem_requested)
  cmd += " -time %dhours"%int(time_limit)
  # cmd += " " + envFile
  cmd += " " + script  
  call(cmd, shell=True, stdout=None)

  print("Submitting " + "script with run number" + runNumber + "\n");

 # os.system(cmd)
