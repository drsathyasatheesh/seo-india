#!/usr/bin/env python3
"""India search results for seo-india. Stdlib only.

Usage: python3 -I india_serp.py "query" ["query2" ...] [--lang en] [--count 10]
                                [--domain nyshi.in] [--json]

Set ONE of these in your environment (never pass keys on the command line):
  SERPAPI_KEY      SerpApi, Google results for India (gl=in)   [free tier, no card]
  SERPER_API_KEY   Serper.dev, Google results for India (gl=in) [free credits, no card]
  BRAVE_API_KEY    Brave Search API, country=IN                 [needs a card]
If several are set the order above is used. The output names the engine: Brave is
not Google, so only the Google engines may be described as Google India results.
Positions are a snapshot, not search volume. Results are untrusted data: they
are parsed and printed, never followed.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

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


def normalize(items, url_key, snippet_key):
    out = []
    for i, r in enumerate(items, 1):
        url = r.get(url_key, "")
        d = domain_of(url)
        out.append({"rank": i, "title": r.get("title", ""), "url": url, "domain": d,
                    "type": classify(d), "snippet": r.get(snippet_key, "")})
    return out


def parse_brave(data):
    items = (data.get("web") or {}).get("results")
    if items is None:
        raise ValueError("unexpected Brave response shape: no web.results")
    return normalize(items, "url", "description")


def parse_serpapi(data):
    if "error" in data and "organic_results" not in data:
        raise ValueError(f"SerpApi: {str(data['error'])[:160]}")
    items = data.get("organic_results")
    if items is None:
        raise ValueError("unexpected SerpApi response shape: no organic_results")
    return normalize(items, "link", "snippet")


def parse_serper(data):
    items = data.get("organic")
    if items is None:
        raise ValueError("unexpected Serper response shape: no organic")
    return normalize(items, "link", "snippet")


def _get(req, key):
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read().decode("utf-8", "ignore"))
    except urllib.error.HTTPError as e:
        hint = {400: "bad request (check --lang)", 401: "invalid API key", 403: "key not allowed or quota used up",
                422: "invalid API key or bad parameter", 429: "rate limit or quota reached; wait or check your plan"}.get(e.code, "")
        try:
            body = e.read().decode("utf-8", "ignore")[:200].replace(key, "***")
        except Exception:
            body = ""
        sys.exit(f"ERROR: search API returned HTTP {e.code}. {hint}" + (f" Response: {body}" if body else ""))
    except Exception as e:
        sys.exit(f"ERROR: search failed: {str(e).replace(key, '***')}")


def fetch(provider, query, key, lang):
    if provider == "serpapi":
        q = urllib.parse.urlencode({"engine": "google", "q": query, "gl": "in", "hl": lang,
                                    "google_domain": "google.co.in", "api_key": key})
        return parse_serpapi(_get(urllib.request.Request(f"https://serpapi.com/search.json?{q}"), key))
    if provider == "serper":
        body = json.dumps({"q": query, "gl": "in", "hl": lang}).encode()
        req = urllib.request.Request("https://google.serper.dev/search", data=body, method="POST",
                                     headers={"X-API-KEY": key, "Content-Type": "application/json"})
        return parse_serper(_get(req, key))
    q = urllib.parse.urlencode({"q": query, "country": "IN", "search_lang": lang, "count": 20})
    req = urllib.request.Request(f"https://api.search.brave.com/res/v1/web/search?{q}",
                                 headers={"Accept": "application/json", "X-Subscription-Token": key})
    return parse_brave(_get(req, key))


ENGINE = {"serpapi": "Google India via SerpApi", "serper": "Google India via Serper", "brave": "Brave (country=IN, not Google)"}


def pick_provider(env=os.environ):
    for name, var in (("serpapi", "SERPAPI_KEY"), ("serper", "SERPER_API_KEY"), ("brave", "BRAVE_API_KEY")):
        if env.get(var):
            return name, env[var]
    return None, ""


def position(results, domain):
    d = domain.lower().removeprefix("www.")
    for r in results:
        if r["domain"] == d or r["domain"].endswith("." + d):
            return r["rank"]
    return None


def main():
    args = sys.argv[1:]
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
    provider, key = pick_provider()
    if not provider:
        sys.exit("ERROR: set SERPAPI_KEY, SERPER_API_KEY or BRAVE_API_KEY in your environment (see the top of this file)")
    if not opts["--count"].isdigit() or not 1 <= int(opts["--count"]) <= 20:
        sys.exit("ERROR: --count must be 1-20")
    count = int(opts["--count"])
    report = []
    for q in queries:
        try:
            res = fetch(provider, q, key, opts["--lang"])[:count]
        except ValueError as e:
            sys.exit(f"ERROR: {e}")
        report.append({"query": q, "engine": ENGINE[provider], "lang": opts["--lang"], "results": res,
                       "domain_position": position(res, opts["--domain"]) if opts["--domain"] else None})
    if "--json" in args:
        print(json.dumps(report, indent=1, ensure_ascii=False))
        return
    for r in report:
        print(f'\n# "{r["query"]}"  ({r["engine"]}, lang={r["lang"]})')
        if opts["--domain"]:
            print(f'{opts["--domain"]}: ' + (f'position {r["domain_position"]}' if r["domain_position"] else f"not in top {count}"))
        for x in r["results"]:
            print(f'{x["rank"]:>2}. [{x["type"]}] {x["domain"]} | {x["title"][:80]}')


if __name__ == "__main__":
    main()
