#!/usr/bin/python3

import os
import glob
import re
import time 
import os.path

baseDir = "/cache/halld/home/ksaldan/fcal_timing"
dataDir = baseDir + "/output_reaction/data/p3pi_FCALStudy_DSelectorOut"
scriptDir = baseDir + "/copy_files/data"
logDir = scriptDir + "/log"
template = baseDir + "/run_DSelector_TEMPLATE.sh"

workflow = "data_flatten"
account = "halld"
partition = "production"
disk_space = 25
mem_requested = 4
time_limit = 12  

if not os.path.exists(scriptDir): os.makedirs(scriptDir)
if not os.path.exists(logDir): os.makedirs(logDir)

fileList = glob.glob(dataDir + "/*root")

for i in range(len(fileList)):

  runNumber = re.search('DSelectorOut_(......)',fileList[i]).group(1)
  if re.search('DSelectorOut_(......)',fileList[i]) is None: 
    continue
  outputDir = dataDir  + "/flatten"

  if not os.path.exists(outputDir): os.makedirs(outputDir)

  script = scriptDir + "/DSelector_flat_" + runNumber + ".sh"
  outFile = outputDir + "/p3pi_FCALStudy_" + runNumber + ".root"
  with open(template,'r+') as TEMP:
    data = TEMP.read()
    data=data.replace('INFILE',fileList[i])
    data=data.replace('OUTFILE',outFile)	

  with open(script,'w+') as OUT:
    OUT.write(data)
    
  OUT.close()
  TEMP.close() 

  cmd = "swif2 add-job -workflow %s -account %s -partition %s"%(workflow,account,partition)
  cmd += " -name %s"%(workflow)
  cmd += " -os general"
  cmd += " -stdout /farm_out/ksaldan/log_%s.log"%(runNumber)
  cmd += " -stderr /farm_out//ksaldan/err_%s.err"%(runNumber)
  cmd += " -disk %dGB"%int(disk_space)
  cmd += " -ram %dgGB"%int(mem_requested)
  cmd += " -time %dhours"%int(time_limit)
  cmd += " " + script  

  print("Submitting " + "script with run number" + runNumber + "\n");
  os.system(cmd)
