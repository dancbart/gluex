BASE="/home/dbart013/work/files/pipkslamb/mc/spring2018_500M/thrown"
OUT="/home/dbart013/work/files/pipkslamb/mc/spring2018_500M/thrown/flatten"
mkdir -p "$OUT"

ls -1 "$BASE"/tree_thrown_gen_amp_V2_*.root \
  | LC_ALL=C sort \
  > "$OUT/fileList.txt"

wc -l "$OUT/fileList.txt"

