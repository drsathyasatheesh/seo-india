# seo-india: the India layer for your SEO workflow

A skill for Claude Code that audits a website for the Indian market and tells you what to fix first.

## The problem
General SEO tools assume English, desktop, card payments and US conventions. Indian customers search in many languages, pay by UPI, contact on WhatsApp, and browse on phones of every price range.

## What seo-india checks
- **Language and script:** Indic pages, valid language tags, hreflang, Indic-script presence
- **Indian formats:** ₹/INR, +91 numbers, 6-digit PIN codes, address and schema fields
- **Phone performance:** JavaScript weight, images, lazy-loading, with guidance for CPU-throttled testing
- **Trust signals:** WhatsApp contact, refund and privacy pages, GST mention, UPI/COD/EMI for shops
- **Local presence:** city-level schema, opening hours, geo data
- **Keyword planning:** English-India, native-script, transliterated and Hinglish variants
- **Cultural fit checklist** and seasonal planning prompts

## How it works
1. A built-in checker reads the page and reports pass, fail, N/A or unknown per check.
2. It adapts to the business type: online shop, local business or service.
3. Claude adds judgement: language quality, culture, next steps, a ranked fix list.

## Honest limits
- It reads public pages. It does not invent search volumes or rankings. Keyword plans stay unvalidated unless you connect a data source.
- It checks the page you give it. It does not crawl a whole site.
- It cannot read sites that block automated requests.
- CPU-throttled Lighthouse and Google Business Profile checks are reported as "unknown", not guessed.
- Facts that change (AI-search languages, UPI figures) must be re-verified before quoting to clients.

## Requirements
Claude Code. Python 3 for the checker (no extra packages).

## Licensing
Single-user commercial license: one named person per license; client work is allowed; resale and sharing are not.

## Pricing
[Set price]

## Contact
team@nyshi.in
