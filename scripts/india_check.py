#!/usr/bin/env python3
"""India-readiness checker for seo-india. Stdlib only.

Usage: python3 -I india_check.py <url> [--json]
Fetches one page and reports pass/fail/na/unknown checks per audit area.
Fetched content is untrusted data: it is parsed, never executed or followed.
"""
import gzip
import json
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Linux; Android 10; Moto G) AppleWebKit/537.36 Mobile Safari/537.36 seo-india/0.1"
MAX_BYTES = 5_000_000


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=20) as r:
        raw = r.read(MAX_BYTES)
        wire = len(raw)
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return (raw if binary else raw.decode("utf-8", "ignore")), wire, r.geturl()


def types_of(node, out):
    if isinstance(node, dict):
        t = node.get("@type")
        out.extend(t if isinstance(t, list) else [t] if t else [])
        for v in node.values():
            types_of(v, out)
    elif isinstance(node, list):
        for v in node:
            types_of(v, out)


def find_key(node, key):
    if isinstance(node, dict):
        if key in node:
            return node[key]
        for v in node.values():
            r = find_key(v, key)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find_key(v, key)
            if r:
                return r
    return None


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: india_check.py <url> [--json]")
    url = sys.argv[1]
    if "://" not in url:
        url = "https://" + url
    if urllib.parse.urlparse(url).scheme not in ("http", "https"):
        sys.exit("ERROR: only http/https URLs are supported")
    try:
        html, _, final = fetch(url)
    except Exception as e:  # unreachable site: report, do not guess
        hint = " (the site may block automated requests; do not guess its content, try a browser-based check)" if "403" in str(e) or "429" in str(e) else ""
        sys.exit(f"ERROR: could not fetch {url}: {e}{hint}")

    ld_raw = re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I)
    ld, types = [], []
    for b in ld_raw:
        try:
            j = json.loads(b)
            ld.append(j)
            types_of(j, types)
        except ValueError:
            pass
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    low = text.lower()

    def has(p):
        return re.search(p, low, re.I) is not None

    local_types = {"LocalBusiness", "ProfessionalService", "Store", "Restaurant", "Dentist", "MedicalBusiness"}
    shop_links = len(re.findall(r'href="[^"]*(?:/cart|/products?/|/collections/)', html, re.I))
    if "Product" in types or has(r"\badd to cart\b|\bbuy now\b|\bcheckout\b") or shop_links >= 5 or re.search(r"add[_-]?to[_-]?cart", html, re.I):
        btype = "ecommerce"
    elif local_types & set(types) and find_key(ld, "streetAddress"):
        btype = "local"
    else:
        btype = "service"

    checks = []  # (area, name, status, note)

    def add(area, name, ok, note="", na=False, unknown=False):
        checks.append((area, name, "na" if na else "unknown" if unknown else "pass" if ok else "fail", note))

    lang = re.search(r'<html[^>]*\blang="([^"]+)"', html, re.I)
    hreflang = re.findall(r'<link[^>]+hreflang="([^"]+)"', html, re.I)
    indic = len(re.findall(r"[ऀ-ൿ]", text))
    A = "Language and script"
    code = lang.group(1).lower() if lang else ""
    add(A, "html lang is an -IN or Indic tag", code.endswith("-in") or code[:2] in "hi bn ta te mr gu kn ml pa or ur as".split(), code or "missing")
    add(A, "Indic-language content present", indic > 50, f"{indic} Indic characters")
    add(A, "hreflang present", bool(hreflang), ",".join(hreflang) or "none")

    L = "Locale formats"
    phone = re.findall(r"\+91[\s-]?\d[\d\s-]{8,12}\d", text)
    add(L, "+91 phone number visible", bool(phone), phone[0].strip() if phone else "none")
    add(L, "tel: or wa.me link", bool(re.search(r'href="(tel:|https://wa\.me/)', html)), "")
    add(L, "INR in schema or INR/₹ in text", "₹" in text or bool(re.search(r"\bINR\b|\bRs\.?\s?\d", text)) or '"INR"' in html, "", na=btype == "service" and not has(r"₹|\binr\b"), )
    add(L, "6-digit PIN code present", bool(re.search(r"\b[1-9]\d{5}\b", text)) or bool(find_key(ld, "postalCode")), "")
    add(L, "schema address has street and postalCode", bool(find_key(ld, "streetAddress") and find_key(ld, "postalCode")), "")

    P = "Mobile and device"
    srcs = sorted(set(re.findall(r'<script[^>]+src="([^"]+)"', html, re.I)))
    total = 0
    for s in srcs:
        try:
            _, w, _ = fetch(urllib.parse.urljoin(final, s), binary=True)
            total += w
        except Exception:
            pass
    add(P, "viewport meta present", bool(re.search(r'name="viewport"', html, re.I)))
    add(P, "JS transfer under 300 KB", total < 300_000, f"{total // 1024} KB over {len(srcs)} files")
    imgs = re.findall(r"<img[^>]*>", html, re.I)
    add(P, "all images have alt", all("alt=" in i for i in imgs), f"{len(imgs)} images")
    add(P, "lazy-loading used on images", not imgs or any('loading="lazy"' in i for i in imgs), "")
    add(P, "CPU-throttled lab test (Lighthouse)", False, "not run by this script", unknown=True)

    C = "Commerce trust"
    is_shop = btype == "ecommerce"
    add(C, "WhatsApp contact", bool(re.search(r"wa\.me/|\bwhatsapp\b", low)))
    for label, pat in (("UPI", r"\bupi\b"), ("COD", r"\bcod\b|cash on delivery"), ("EMI", r"\bemi\b")):
        found = has(pat)
        # Payment methods often appear only on product/checkout pages, so a miss is unknown, not fail.
        add(C, f"{label} mentioned", found, "" if found else "not on this page; check product/checkout", na=not is_shop, unknown=is_shop and not found)
    add(C, "Return/refund policy link", bool(re.search(r'href="[^"]*(refund|return)[^"]*"', html, re.I)))
    add(C, "GST / GSTIN mentioned", has(r"\bgstin?\b"))
    add(C, "Privacy policy link", bool(re.search(r'href="[^"]*privacy[^"]*"', html, re.I)))

    LO = "Local presence"
    online_only = btype == "ecommerce" and not (local_types & set(types))
    add(LO, "schema has addressLocality", bool(find_key(ld, "addressLocality")), na=online_only)
    add(LO, "schema has geo coordinates", bool(find_key(ld, "geo")), na=online_only)
    add(LO, "schema has openingHours", bool(find_key(ld, "openingHoursSpecification") or find_key(ld, "openingHours")), na=online_only)
    add(LO, "Google Business Profile verified", False, "needs live GBP data", unknown=True, na=online_only)

    S = "Structured data and basics"
    add(S, "canonical tag", bool(re.search(r'rel="canonical"', html, re.I)))
    add(S, "meta description", bool(re.search(r'name="description"', html, re.I)))
    add(S, "JSON-LD present", bool(ld), ", ".join(sorted(set(types))) or "none")
    add(S, "single H1", len(re.findall(r"<h1[\s>]", html, re.I)) == 1)

    areas = {}
    for a, n, s, note in checks:
        areas.setdefault(a, []).append((n, s, note))

    def score(rows):
        p = sum(1 for _, s, _ in rows if s == "pass")
        f = sum(1 for _, s, _ in rows if s == "fail")
        return round(100 * p / (p + f)) if p + f else None

    scores = {a: score(r) for a, r in areas.items()}
    provisional = [a for a, r in areas.items() if any(st == "unknown" for _, st, _ in r)]
    scored = [v for v in scores.values() if v is not None]
    overall = round(sum(scored) / len(scored)) if scored else None
    result = {"url": final, "business_type": btype, "overall": overall, "scores": scores, "provisional_areas": provisional,
              "checks": [dict(area=a, check=n, status=s, note=t) for a, n, s, t in checks]}
    if "--json" in sys.argv:
        print(json.dumps(result, indent=1, ensure_ascii=False))
        return
    print(f"# India check: {final}\nBusiness type (heuristic): {btype}\nOverall (scored areas only): {overall}\n")
    for a, rows in areas.items():
        tag = " (provisional: has unknown checks)" if a in provisional else ""
        print(f"## {a}: {scores[a] if scores[a] is not None else 'not scored'}{tag}")
        for n, s, t in rows:
            print(f"- [{s.upper():7}] {n}" + (f" ({t})" if t else ""))
        print()


if __name__ == "__main__":
    main()
