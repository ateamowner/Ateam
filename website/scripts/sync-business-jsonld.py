#!/usr/bin/env python3
"""SCH-1 (site audit 2026-11-13): one shared source for the #business JSON-LD node.

The site is static (no build step), so instead of a server-side include this script copies
scripts/business.jsonld.json into every page's <script type="application/ld+json"> block whose
@id ends in "#business". Edit the JSON file, run this script, commit the result.

    python3 scripts/sync-business-jsonld.py          # rewrite pages
    python3 scripts/sync-business-jsonld.py --check  # exit 1 if any page differs
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'scripts', 'business.jsonld.json')
BLOCK = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

def main(check=False):
    canon = json.load(open(SRC, encoding='utf-8'))
    canon_txt = json.dumps(canon, ensure_ascii=False, separators=(',', ':'))
    changed, missing = [], []
    for path in sorted(glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True)):
        rel = os.path.relpath(path, ROOT)
        html = open(path, encoding='utf-8').read()
        hit = [False]
        def repl(m):
            try:
                node = json.loads(m.group(2))
            except ValueError:
                return m.group(0)
            if isinstance(node, dict) and str(node.get('@id', '')).endswith('#business'):
                hit[0] = True
                return m.group(1) + canon_txt + m.group(3)
            return m.group(0)
        new = BLOCK.sub(repl, html)
        if not hit[0]:
            missing.append(rel)
        if new != html:
            changed.append(rel)
            if not check:
                open(path, 'w', encoding='utf-8').write(new)
    print(('would change' if check else 'changed'), len(changed), 'pages')
    for r in changed: print('  ', r)
    if missing: print('no #business node on', len(missing), 'pages (left alone):', ', '.join(missing))
    return 1 if (check and changed) else 0

if __name__ == '__main__':
    sys.exit(main('--check' in sys.argv))
