"""Check every prayer link in prayers.py: the page must load (HTTP 200) and any #anchor must exist.
Run: python tools/check_prayer_links.py   (needs internet access to www.avesta.org)"""
import os, re, sys
import requests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import prayers  # noqa: E402

def main():
    cache, bad, n = {}, [], 0
    for url in prayers.all_urls():
        n += 1
        page, _, frag = url.partition("#")
        if page not in cache:
            if page.endswith(".pdf"):
                r = requests.head(page, timeout=60, allow_redirects=True)
                cache[page] = (r.status_code, "")
            else:
                r = requests.get(page, timeout=60)
                r.encoding = r.apparent_encoding
                cache[page] = (r.status_code, r.text)
        status, text = cache[page]
        if status != 200:
            bad.append((url, f"HTTP {status}"))
        elif frag and not re.search(r'(?i)(?:id|name)\s*=\s*["\']?%s(?:["\'\s>])' % re.escape(frag), text):
            bad.append((url, "anchor not found"))
    print(f"{n} links checked, {len(bad)} problems")
    for u, why in bad:
        print("  ", why, u)
    return 1 if bad else 0

if __name__ == "__main__":
    raise SystemExit(main())
