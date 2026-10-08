"""Builds index.html (flash kartlar) and sorular.html (tüm sorular) from data/. Run: python3 build.py"""
import json, re, pathlib, sys
TODO = '--todo' in sys.argv
root = pathlib.Path(__file__).parent
rows = json.loads((root/'data/rows.json').read_text(encoding='utf-8'))

# PDF çıkarımında satır sonları kaybolmuş: yapışık alt başlık ve "- " maddelerini ayır.
# Sadece boşluk -> satır sonu; metin değişmez, rows.json'a dokunulmaz.
HEAD = re.compile(r'(?:(?<=[.!?])|(?<=[^\W\d_]{4}\))) +(?=[A-ZÇĞİÖŞÜ][^.:\n]{1,45}:[ \t]*(?:\n|$))')
BUL = re.compile(r'((?:[.!?]|\([^()\n]{12,}\))) +(?=- ?[A-ZÇĞİÖŞÜ])')
for r in rows:
    r['a'] = BUL.sub(r'\1\n', HEAD.sub('\n', r['a']))
sections = json.loads((root/'data/clusters.json').read_text(encoding='utf-8'))
merged_dir = root/'data/merged'
ids, errors, done, multi = set(), [], 0, 0
for s in sections:
    for c in s['clusters']:
        ids.add(c['id'])
        f = merged_dir/f"{c['id']}.md"
        c['merged'] = None
        if len(c['rows']) > 1:
            multi += 1
            if f.exists():
                txt = f.read_text(encoding='utf-8').strip()
                allowed = {chr(65+i) for i in range(len(c['rows']))}
                for grp in re.findall(r'\[([A-Z](?:\s*,\s*[A-Z])*)\]', txt):
                    bad = set(re.split(r'\s*,\s*', grp)) - allowed
                    if bad: errors.append(f"{c['id']}: kaynak harfi yok {sorted(bad)} (izinli: {''.join(sorted(allowed))})")
                c['merged'] = txt; done += 1
single_dir = root/'data/single'
single_ids = {c['id'] for s in sections for c in s['clusters'] if len(c['rows']) == 1}
for s in sections:
    for c in s['clusters']:
        if len(c['rows']) == 1:
            f = single_dir/f"{c['id']}.md"
            if f.exists(): c['merged'] = f.read_text(encoding='utf-8').strip()
if single_dir.exists():
    for f in single_dir.glob('*.md'):
        if f.stem not in single_ids: errors.append(f"data/single/{f.name}: tek kaynaklı küme id'si değil")
for f in merged_dir.glob('*.md'):
    if f.stem not in ids: errors.append(f"{f.name}: böyle bir küme id yok")
if '--todo-single' in sys.argv:
    for s in sections:
        for c in s['clusters']:
            if len(c['rows']) == 1 and not (single_dir/f"{c['id']}.md").exists() and rows[c['rows'][0]]['a'].strip():
                print(f"{c['id']:<22} {c['title']}  rows={c['rows']}")
    sys.exit(0)
ai_dir = root/'data/ai'
all_ids = {c['id'] for s in sections for c in s['clusters']}
for s in sections:
    for c in s['clusters']:
        f = ai_dir/f"{c['id']}.md"
        c['ai'] = f.read_text(encoding='utf-8').strip() if f.exists() else None
if ai_dir.exists():
    for f in ai_dir.glob('*.md'):
        if f.stem not in all_ids: errors.append(f"data/ai/{f.name}: böyle bir küme id yok")
if '--todo-ai' in sys.argv:
    for s in sections:
        for c in s['clusters']:
            if not c['ai']: print(f"{c['id']:<22} {c['title']}")
    sys.exit(0)
if TODO:
    for s in sections:
        for c in s['clusters']:
            if len(c['rows'])>1 and not c['merged']:
                print(f"{c['id']:<22} {len(c['rows'])}x  {c['title']}  rows={c['rows']}")
    sys.exit(0)
if errors:
    print('\n'.join(errors)); sys.exit(1)
data = json.dumps({'rows': rows, 'sections': sections}, ensure_ascii=False).replace('</', '<\\/')
html = (root/'template.html').read_text(encoding='utf-8').replace('__DATA__', data)
(root/'sorular.html').write_text(html, encoding='utf-8')
(root/'index.html').write_text((root/'flash_template.html').read_text(encoding='utf-8').replace('__DATA__', data), encoding='utf-8')
print(f"index.html + sorular.html yazıldı. Birleşik cevap: {done}/{multi} çok-kaynaklı küme.")
