# seo-india

A Claude Code skill that audits and plans SEO for the Indian market.

It adds the India-specific layer that general SEO tools skip:

- Indic languages, scripts, transliterated and Hinglish search
- Indian formats: ₹, lakh/crore, +91, 6-digit PIN codes, IST
- Low-end-device performance (CPU and JavaScript, not just bandwidth)
- Trust signals Indian customers look for: UPI, COD, EMI, WhatsApp, GST
- Local SEO for Indian cities and directories
- AI-search visibility checks for Indic languages

## Install

Copy this folder to `~/.claude/skills/seo-india/` and restart Claude Code.

## Use

```
/seo-india audit https://example.in
/seo-india keywords "wedding photographer"
/seo-india local "Dental clinic, Koramangala, Bangalore"
/seo-india commerce https://shop.example.in
```

Or run the fact checker directly (Python 3, no installs):

```
python3 -I scripts/india_check.py https://example.in
python3 -I scripts/india_check.py https://example.in --json
```

## What it does and does not do

- It checks what is visible on the public page: language, formats, schema,
  contact and trust signals, JavaScript weight, images.
- It does **not** invent search volumes or rankings. Keyword plans are marked
  unvalidated unless a real data source (for example DataForSEO or Search
  Console) is connected.
- It reads one page per run; it does not crawl a whole site.
- Sites that block automated requests (HTTP 403/429) cannot be read.
- Publishers and news sites are treated as `service`; there is no publisher mode yet.
- It does not run CPU-throttled Lighthouse or check Google Business Profile
  by itself; those items are reported as "unknown".
- Fast-changing facts (AI feature languages, UPI figures, platform shares) must
  be re-verified before you quote them to a client.

## Layout

```
SKILL.md              commands, workflow, scoring rules
scripts/india_check.py  fact checker
references/           language, formats, culture, mobile, commerce, local
LICENSE.txt           MIT
```

## Works alongside

`seo-hreflang`, `seo-schema`, `seo-technical`, `seo-local`, `seo-ecommerce`,
`seo-geo`, `seo-dataforseo`, `seo-google`. These are separate tools by other
authors and are not included here.

## License

MIT. Free to use, modify and share. See `LICENSE.txt`.

## Built by NYSHI

NYSHI builds websites, SEO, WhatsApp automation and Google Business Profile
setups for Indian businesses: https://nyshi.in , team@nyshi.in

## Paid extras (planned, not built yet)

The core audit stays free. Possible paid add-ons, only built if there is demand:
multi-page crawler, client-ready report templates, validated Indic keyword
data, and monthly fact updates. Email team@nyshi.in to say which you would use.
