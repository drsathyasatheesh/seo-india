# Indic Languages, Scripts and Hinglish

Load when scoring "Language and script" or running `keywords`.

## Language and script map (stable facts)

| Language | Code | Script | Notes |
|----------|------|--------|-------|
| Hindi | hi | Devanagari | Also Marathi, Konkani, Nepali, Maithili, Dogri, Bodo |
| Marathi | mr | Devanagari | Distinct from Hindi; do not reuse Hindi copy |
| Bengali | bn | Bengali-Assamese | Assamese (`as`) shares the script |
| Tamil | ta | Tamil | |
| Telugu | te | Telugu | |
| Kannada | kn | Kannada | |
| Malayalam | ml | Malayalam | |
| Gujarati | gu | Gujarati | |
| Punjabi | pa | Gurmukhi | Pakistan Punjabi uses a different script |
| Odia | or | Odia | |
| Urdu | ur | Perso-Arabic (right-to-left) | Needs `dir="rtl"` |

India's constitution lists 22 scheduled languages; this table is the commercially common subset, not the full list.

## Rules

1. **Hindi is not "India".** Hindi serves one large region. Southern and eastern
   markets usually need Tamil, Telugu, Kannada, Malayalam or Bengali, and many
   urban users read English. Choose languages by the audience's location, not by
   a pan-India default.
2. **Language codes.** Use ISO 639-1 plus region: `hi-IN`, `ta-IN`, `en-IN`.
   Validate tags with `seo-hreflang`. Add `lang` on `<html>` and on mixed-language blocks.
3. **Human review.** Raw machine translation of Indic text often reads unnaturally
   and is a spam-policy risk at scale. Require native-speaker review.
4. **Separate URLs per language** (`/hi/`, `/ta/`), each with self-referencing
   hreflang and `x-default`. Do not auto-redirect by IP.
5. **Fonts.** Check that Indic glyphs render with no empty boxes. Prefer system
   fonts or subset webfonts (Noto Sans family has Indic coverage). Use
   `font-display: swap`. Indic fonts are heavy: measure their size.
6. **Right-to-left** for Urdu: `dir="rtl"` and mirrored layout.
7. **Do not mix scripts in titles carelessly.** Truncation and wrapping differ
   from Latin text; check title and meta snippets render in the SERP.

## Search behaviour patterns

People search the same need in several forms. Cover all that matter:

| Form | Example idea | Where to use |
|------|--------------|--------------|
| English (India) | "dentist near me" | Main English pages |
| Native script | the same query typed in Devanagari or Tamil script | Native-language pages |
| Transliterated | Indic words typed in Roman letters (e.g. "kaise", "kitna") | Titles, headings, FAQ phrasing where natural |
| Hinglish | English and Hindi words mixed in one query | FAQ, blog headings, social, video titles |

Do not guess which form wins for a topic. **All four are hypotheses until real
data confirms them.** Use `seo-dataforseo`, Search Console query data, or
Google autocomplete/related searches to validate. Never state search volumes
from memory.

## Keyword output template

| Keyword | Language | Script | Form | Intent | Page type | Validated? |
|---------|----------|--------|------|--------|-----------|-----------|
| ... | hi | Latin | transliterated | informational | FAQ | no |

## Checks for existing multilingual sites

- Every language page has a translated title, meta description, H1, and schema.
- Image alt text and URLs slugs are localised (native-script slugs are allowed
  but percent-encode in links; consider Roman slugs for sharing).
- Language switcher is crawlable links, not a script-only dropdown.
- Content parity: translated pages cover the same sections as the source.
