"""Offline test for india_serp.py parsing. Run: python3 -I scripts/test_india_serp.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import india_serp as s

brave = {"web": {"results": [
    {"title": "Top Web Developers in Bengaluru", "url": "https://clutch.co/in/web-developers/bengaluru", "description": "list"},
    {"title": "OneCity", "url": "https://www.onecity.co.in/website-development-company-bangalore", "description": "agency"},
    {"title": "NYSHI guide", "url": "https://www.nyshi.in/guides/x", "description": "ours"}]}}
serpapi = {"organic_results": [
    {"position": 1, "title": "A", "link": "https://www.justdial.com/x", "snippet": "a"},
    {"position": 2, "title": "NYSHI", "link": "https://www.nyshi.in/", "snippet": "b"}]}
serper = {"organic": [
    {"position": 1, "title": "A", "link": "https://dev.to/x", "snippet": "a"},
    {"position": 2, "title": "NYSHI", "link": "https://nyshi.in/guides/y", "snippet": "b"}]}

b, a, p = s.parse_brave(brave), s.parse_serpapi(serpapi), s.parse_serper(serper)
assert [x["rank"] for x in b] == [1, 2, 3]
assert b[0]["type"] == "directory/marketplace" and b[1]["type"] == "site"
assert b[1]["domain"] == "onecity.co.in"                      # www. stripped
assert s.position(b, "nyshi.in") == 3 and s.position(b, "www.nyshi.in") == 3
assert s.position(b, "example.com") is None
assert a[0]["type"] == "directory/marketplace" and s.position(a, "nyshi.in") == 2
assert p[0]["type"] == "community/content platform" and s.position(p, "nyshi.in") == 2
assert s.classify("sub.upwork.com") == "directory/marketplace"
assert s.classify("notclutch.co") == "site"                   # no false suffix match
for fn, bad in ((s.parse_brave, {}), (s.parse_serpapi, {}), (s.parse_serper, {})):
    try:
        fn(bad)
        raise SystemExit("expected ValueError")
    except ValueError:
        pass
try:
    s.parse_serpapi({"error": "Invalid API key"})
    raise SystemExit("expected ValueError")
except ValueError as e:
    assert "Invalid API key" in str(e)
assert s.pick_provider({"SERPER_API_KEY": "k"}) == ("serper", "k")
assert s.pick_provider({"SERPAPI_KEY": "a", "BRAVE_API_KEY": "b"})[0] == "serpapi"   # Google engines first
assert s.pick_provider({}) == (None, "")
print("ok")
