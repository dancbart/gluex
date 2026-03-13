BASE="/.bscratch/data/dbart013/files/pipkslamb/data/fall2018"
OUT="/.bscratch/data/dbart013/files/pipkslamb/data/fall2018/flatten"
mkdir -p "$OUT"

ls -1 "$BASE"/tree_pipkslamb__B4_M16_M18_05????.root \
  | LC_ALL=C sort \
  > "$OUT/fileList.txt"

wc -l "$OUT/fileList.txt"

