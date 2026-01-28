BASE="/home/dbart013/work/files/pipkslamb/mc/spring2018_500M/trees/flatten"
N=$(wc -l < "$BASE/fileList.txt")

sbatch --array=0-$((N-1))%200 runFSFlattenSBATCH_step2_jobScriptForArray.sh
# sbatch --array=0-20%5 runFSFlattenSBATCH_step2_jobScriptForArray.sh

