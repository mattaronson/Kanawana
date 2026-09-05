#!/bin/bash
n=$1
S=/tmp/claude-0/-home-user-Kanawana/ce12d240-1458-5962-bfe6-737b75558607/scratchpad
f=$(python3 -c "
import json,sys
for l in open('/home/user/Kanawana/kb/reread/cc_progress.jsonl'):
    r=json.loads(l)
    if r['n']==int(sys.argv[1]): print(r['file'])
" $n)
D=$S/pt/$n
rm -rf $D; mkdir -p $D
sed -e 's/[[:space:]]\+/ /g' -e '/^ *$/d' "/home/user/Kanawana/sources/cache/canadian-camping/$f" > $D/w.txt
split -C 24000 -d -a 2 $D/w.txt $D/p
echo "ISSUE $n : $f"
ls $D/p* | sed "s|$D/||" | tr '\n' ' '
