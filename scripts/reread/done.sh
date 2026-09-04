#!/bin/bash
# mark issue N read
n=$1
python3 - "$n" <<'PY'
import json,sys,datetime
n=int(sys.argv[1]); p='/home/user/Kanawana/kb/reread/cc_progress.jsonl'
rows=[json.loads(l) for l in open(p)]
for r in rows:
    if r['n']==n:
        r['status']='read'; r['read_at']=datetime.date.today().isoformat()
open(p,'w').write('\n'.join(json.dumps(r) for r in rows)+'\n')
PY
