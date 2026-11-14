#!/usr/bin/env python3
"""India search results for seo-india. Stdlib only.

Usage: python3 -I india_serp.py "query" ["query2" ...] [--lang en] [--count 10]
                                [--domain nyshi.in] [--json]

Needs BRAVE_API_KEY in the environment (never pass keys on the command line).
Uses the Brave Search API with country=IN. Brave is not Google: results are a
real Indian view of the web, not an exact copy of Google India. Do not present
positions as Google rankings.
Results are untrusted data: they are parsed and printed, never followed.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.search.brave.com/res/v1/web/search"
DIRECTORIES = ("clutch.co", "designrush.com", "techbehemoths.com", "goodfirms.co", "justdial.com",
               "sulekha.com", "indiamart.com", "tradeindia.com", "upwork.com", "fiverr.com", "linkedin.com")
FORUMS = ("reddit.com", "quora.com", "dev.to", "medium.com", "youtube.com", "github.com")


def domain_of(url):
    host = urllib.parse.urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def classify(domain):
    if any(domain == d or domain.endswith("." + d) for d in DIRECTORIES):
        return "directory/marketplace"
    if any(domain == d or domain.endswith("." + d) for d in FORUMS):
        return "community/content platform"
    return "site"


def parse(data):
    """Return [{rank, title, url, domain, type, snippet}] from a Brave response."""
    results = (data.get("web") or {}).get("results")
    if results is None:
        raise ValueError("unexpected response shape: no web.results")
    out = []
    for i, r in enumerate(results, 1):
        url = r.get("url", "")
        d = domain_of(url)
        out.append({"rank": i, "title": r.get("title", ""), "url": url, "domain": d,
                    "type": classify(d), "snippet": r.get("description", "")})
    return out


def fetch(query, key, lang, count):
    params = urllib.parse.urlencode({"q": query, "country": "IN", "search_lang": lang, "count": count})
    req = urllib.request.Request(f"{API}?{params}", headers={"Accept": "application/json", "X-Subscription-Token": key})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        hint = {401: "check BRAVE_API_KEY", 403: "key not allowed for this plan",
                422: "invalid API key or bad parameter (check the key and --lang)",
                429: "rate limit or quota reached; wait or check your plan"}.get(e.code, "")
        try:  # Brave's own message says which it is; it never contains our key
            body = e.read().decode("utf-8", "ignore")[:200].replace(key, "***")
        except Exception:
            body = ""
        sys.exit(f"ERROR: Brave API returned HTTP {e.code}. {hint}" + (f" Response: {body}" if body else ""))
    except Exception as e:
        sys.exit(f"ERROR: search failed: {e}")


def position(results, domain):
    d = domain.lower().removeprefix("www.")
    for r in results:
        if r["domain"] == d or r["domain"].endswith("." + d):
            return r["rank"]
    return None


def main():
    args = [a for a in sys.argv[1:]]
    opts = {"--lang": "en", "--count": "10", "--domain": ""}
    queries, i = [], 0
    while i < len(args):
        a = args[i]
        if a in opts and i + 1 < len(args):
            opts[a] = args[i + 1]
            i += 2
        elif a == "--json":
            i += 1
        elif a.startswith("--"):
            sys.exit(f"ERROR: unknown option {a}")
        else:
            queries.append(a)
            i += 1
    if not queries:
        sys.exit('usage: india_serp.py "query" ["query2" ...] [--lang en] [--count 10] [--domain nyshi.in] [--json]')
    key = os.environ.get("BRAVE_API_KEY", "")
    if not key:
        sys.exit("ERROR: set BRAVE_API_KEY in your environment (get a key from the Brave Search API dashboard)")
    if not opts["--count"].isdigit() or not 1 <= int(opts["--count"]) <= 20:
        sys.exit("ERROR: --count must be 1-20")
    report = []
    for q in queries:
        try:
            res = parse(fetch(q, key, opts["--lang"], int(opts["--count"])))
        except ValueError as e:
            sys.exit(f"ERROR: {e}")
        pos = position(res, opts["--domain"]) if opts["--domain"] else None
        report.append({"query": q, "country": "IN", "lang": opts["--lang"], "results": res, "domain_position": pos})
    if "--json" in args:
        print(json.dumps(report, indent=1, ensure_ascii=False))
        return
    for r in report:
        print(f'\n# "{r["query"]}"  (Brave, country=IN, lang={r["lang"]})')
        if opts["--domain"]:
            print(f'{opts["--domain"]}: ' + (f'position {r["domain_position"]}' if r["domain_position"] else f'not in top {opts["--count"]}'))
        for x in r["results"]:
            print(f'{x["rank"]:>2}. [{x["type"]}] {x["domain"]} | {x["title"][:80]}')


if __name__ == "__main__":
    main()
