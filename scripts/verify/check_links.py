import re, os

wiki_root = 'wiki'
files = {}
for root, dirs, fnames in os.walk(wiki_root):
    for f in fnames:
        if f.endswith('.md'):
            rel = os.path.relpath(os.path.join(root, f), wiki_root)
            key = rel[:-3]
            files[key] = os.path.join(root, f)

link_re = re.compile(r'\[\[([^\]]+?)\]\]')
broken = []
total_links = 0
for key, path in files.items():
    text = open(path, encoding='utf-8').read()
    for m in link_re.finditer(text):
        inner = m.group(1).strip()
        # split on literal backslash-pipe (display text separator) or plain pipe
        target = re.split(r'\\\|', inner)[0]
        target = target.split('|')[0].strip()
        total_links += 1
        if target not in files:
            broken.append((key, target))

print('total files:', len(files))
print('total links:', total_links)
print('broken links:', len(broken))
for b in broken[:60]:
    print(b)
