#!/usr/bin/env python3
"""Recompute the CSP meta tag in index.html from the inline <style> and <script> hashes.

Run after any edit to the inline CSS or JS:  python3 scripts/update-csp.py
CI runs it with --check and fails if the committed hashes are stale.
"""
import base64, hashlib, re, sys

PATH = "index.html"
src = open(PATH, encoding="utf-8").read()

def sha(block):
    return "'sha256-" + base64.b64encode(hashlib.sha256(block.encode("utf-8")).digest()).decode() + "'"

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
script = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
csp = ("default-src 'none'; "
       f"script-src {sha(script)}; style-src {sha(style)}; "
       "connect-src https://formsubmit.co; img-src 'none'; font-src 'none'; "
       "base-uri 'none'; form-action 'none'")
new = re.sub(r'(<meta http-equiv="Content-Security-Policy" content=")[^"]*(")', lambda m: m.group(1) + csp + m.group(2), src, count=1)

if "--check" in sys.argv:
    if new != src:
        sys.exit("CSP hashes are stale. Run: python3 scripts/update-csp.py")
    print("CSP hashes OK")
else:
    open(PATH, "w", encoding="utf-8").write(new)
    print("CSP updated")
