#!/usr/bin/env python3
"""
Phase B — one standardised trust block at the bottom of every page.

What it replaces: the BBB seal currently sits in an <iframe> on 23 pages,
unlinked on 22 of them. An iframe means a third-party document load, no alt
text, and a fixed pixel box that cannot respond. Anthony supplied the static
seal image, so this swaps in a plain <img> inside a real link to his profile —
one request, lazy-loaded, proper alt text, and it scales.

What it adds: the NAP line (name / locality / phone, matching the schema
exactly and carrying no street address, because this is a service-area
business) and links to all five profiles. Nextdoor especially — his strongest
local channel, previously not linked anywhere on the site.

Social links are text pills rather than icons. Brand glyphs drawn from memory
tend to come out subtly wrong, and a wrong logo is worse than a clear word.
"""
import os
import re

ROOT = "/home/user/Ateam/website"

BBB_PROFILE = ("https://www.bbb.org/us/oh/tipp-city/profile/window-cleaning/"
               "a-team-contracting-0322-1440107933")
GBP = "https://g.page/r/CdoEOEshw5VUEAE/"

PROFILES = [
    ("Google", GBP),
    ("Facebook", "https://www.facebook.com/Ateamcontractings/"),
    ("Nextdoor", "https://nextdoor.com/page/a-team-contracting-services"),
    ("Yelp", "https://www.yelp.com/biz/a-team-contracting-tipp-city"),
    ("BBB", BBB_PROFILE),
]

TRUST = """  <div class="footer-trust">
    <p class="footer-nap"><strong>A-Team Contracting</strong> &middot; Tipp City, OH &middot; <a href="tel:+19379392936">(937) 939-2936</a></p>
    <ul class="footer-social">
%s
    </ul>
    <a class="footer-seal" href="%s/#sealclick" target="_blank" rel="noopener nofollow">
      <img src="https://seal-dayton.bbb.org/seals/blue-seal-293-61-whitetxt-bbb-1440107933.png" width="293" height="61" loading="lazy" alt="A-Team Contracting is BBB Accredited with an A+ Rating">
    </a>
  </div>
""" % (
    "\n".join(
        '      <li><a href="%s" target="_blank" rel="noopener" aria-label="A-Team Contracting on %s">%s</a></li>'
        % (url, name, name)
        for name, url in PROFILES
    ),
    BBB_PROFILE,
)

CSS = """
/* FOOTER TRUST — NAP, profile links and the BBB seal. Identical sitewide.
   No street address: A-Team is a service-area business, so the visible NAP
   matches the schema, which carries locality/region/postal only. */
.footer-trust{border-top:1px solid rgba(255,255,255,.12);margin-top:1.5rem;padding-top:1.5rem;text-align:center}
.footer-nap{font-size:.86rem;color:rgba(255,255,255,.8);margin-bottom:1rem;line-height:1.7}
.footer-nap strong{color:#fff}
.footer-nap a{color:var(--orange-on-dark);font-weight:700}
.footer-social{list-style:none;display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin:0 0 1.25rem;padding:0}
.footer-social li{margin:0}
.footer-social a{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.04em;color:rgba(255,255,255,.85);border:1px solid rgba(255,255,255,.25);border-radius:99px;padding:.4rem .9rem;transition:background .15s,border-color .15s,color .15s}
.footer-social a:hover{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.55);color:#fff}
/* The seal is a 293x61 white-text PNG, sized down for a footer. width/height
   are on the img so it reserves space and does not shift layout on load. */
.footer-seal{display:inline-block;line-height:0}
.footer-seal img{width:200px;height:auto;max-width:100%}
"""

# Any element (div or a) whose only real content is the old seal iframe.
OLD_SEAL = re.compile(
    r'\n\s*<(div|a)\b[^>]*>\s*<iframe[^>]*seal-dayton[^>]*>\s*</iframe>\s*</\1>', re.S)


def process(path):
    html = open(path, encoding="utf-8").read()
    before = html
    notes = []

    n = len(OLD_SEAL.findall(html))
    if n:
        html = OLD_SEAL.sub("", html)
        notes.append("-%d iframe seal" % n)

    if "footer-trust" not in html and "</footer>" in html:
        # Sits after the closing .container so it spans the footer's full width.
        html = html.replace("</footer>", TRUST + "</footer>", 1)
        notes.append("+trust block")

    if html != before:
        open(path, "w", encoding="utf-8").write(html)
    return notes


def main():
    files = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d != "node_modules"]
        if "index.html" in fn:
            files.append(os.path.join(dp, "index.html"))

    for p in sorted(files):
        rel = os.path.relpath(os.path.dirname(p), ROOT)
        rel = "/" if rel == "." else "/" + rel + "/"
        print("  %-46s %s" % (rel, ", ".join(process(p)) or "-"))

    # Shared stylesheet for the 25 pages that link it.
    css = os.path.join(ROOT, "css", "site.css")
    s = open(css, encoding="utf-8").read()
    if "footer-trust" not in s:
        open(css, "w", encoding="utf-8").write(s.rstrip() + "\n" + CSS)
        print("\n  css/site.css  +footer-trust rules")

    # The homepage carries its own inline CSS and does not link site.css.
    home = os.path.join(ROOT, "index.html")
    s = open(home, encoding="utf-8").read()
    if ".footer-trust{" not in s:
        s = s.replace("\n/* FOOTER */", CSS + "\n/* FOOTER */", 1)
        open(home, "w", encoding="utf-8").write(s)
        print("  index.html    +footer-trust rules (inline <style>)")


if __name__ == "__main__":
    main()
