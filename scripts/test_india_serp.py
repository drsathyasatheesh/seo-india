"""Offline test for india_serp.py parsing. Run: python3 -I scripts/test_india_serp.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import india_serp as s

fake = {"web": {"results": [
    {"title": "Top Web Developers in Bengaluru", "url": "https://clutch.co/in/web-developers/bengaluru", "description": "list"},
    {"title": "OneCity", "url": "https://www.onecity.co.in/website-development-company-bangalore", "description": "agency"},
    {"title": "NYSHI guide", "url": "https://www.nyshi.in/guides/x", "description": "ours"},
]}}
r = s.parse(fake)
assert [x["rank"] for x in r] == [1, 2, 3]
assert r[0]["type"] == "directory/marketplace" and r[1]["type"] == "site"
assert r[1]["domain"] == "onecity.co.in"            # www. stripped
assert s.position(r, "nyshi.in") == 3 and s.position(r, "www.nyshi.in") == 3
assert s.position(r, "example.com") is None
assert s.classify("sub.upwork.com") == "directory/marketplace"
assert s.classify("notclutch.co") == "site"          # no false suffix match
try:
    s.parse({})
    raise SystemExit("expected ValueError")
except ValueError:
    pass
print("ok")
