#!/usr/bin/env python3
"""Pairwise duplicate-content check across the city and service-area pages.

Run from website/. Reports 7-word shingle overlap for every pair, expressed as
a share of the shorter page's shingles. Anything over ~30% means two pages are
saying the same thing in different clothes, which is what Google filters city
sets for. Re-run this before adding a city.
"""
import re, pathlib, itertools, html as H

def body_words(path):
    """Visible <body> prose between </header> and <footer>, lowercased words."""
    h = path.read_text()
    m = re.search(r'</header>(.*?)<footer', h, re.S)
    if not m:
        return []
    b = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', m.group(1), flags=re.S)
    b = re.sub(r'<[^>]+>', ' ', b)
    return re.sub(r'[^a-z0-9 ]', ' ', H.unescape(b).lower()).split()

def main():
    pages = [p for p in sorted(pathlib.Path('.').glob('*-ohio')) if (p / 'index.html').exists()]
    words = {p.name: body_words(p / 'index.html') for p in pages}
    shingles = {n: {tuple(w[i:i + 7]) for i in range(len(w) - 6)} for n, w in words.items()}

    pairs = sorted(
        (len(shingles[a] & shingles[b]) / max(1, min(len(shingles[a]), len(shingles[b]))), a, b)
        for a, b in itertools.combinations(sorted(words), 2)
    )
    pairs.reverse()

    print(f"{len(words)} pages, {len(pairs)} pairs\n")
    print("highest overlap:")
    for r, a, b in pairs[:10]:
        print(f"  {r * 100:5.1f}%  {a}  ~  {b}")

    over = [p for p in pairs if p[0] > 0.30]
    print(f"\npairs over 30%: {len(over)}")
    for r, a, b in over:
        print(f"  !! {r * 100:5.1f}%  {a}  ~  {b}")

    print("\nbody word counts:")
    for n in sorted(words):
        print(f"  {n:42} {len(words[n]):5}")

    return 1 if over else 0

if __name__ == '__main__':
    raise SystemExit(main())
