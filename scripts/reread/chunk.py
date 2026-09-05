#!/usr/bin/env python3
"""Print findings blocks for issues [a..b] from kb/reread/cc_findings.md."""
import re, sys, io
a, b = int(sys.argv[1]), int(sys.argv[2])
s = io.open('kb/reread/cc_findings.md', encoding='utf-8').read()
heads = [(int(m.group(1)), m.start()) for m in re.finditer(r'(?m)^## (\d+)\b.*$', s)]
heads.append((10**9, len(s)))
out = []
for i, (n, st) in enumerate(heads[:-1]):
    if a <= n <= b:
        out.append(s[st:heads[i+1][1]])
sys.stdout.write(''.join(out))
