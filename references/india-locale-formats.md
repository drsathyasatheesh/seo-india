# India Locale Formats

Load when scoring "Locale formats". Complements `seo-hreflang`'s locale-formats
reference, which has no Indian row.

## Numbers

India groups digits in a 3-then-2 pattern: the first group is thousands, later
groups are lakhs and crores.

| Value | Indian grouping | International grouping |
|-------|-----------------|------------------------|
| 1,000 | 1,000 | 1,000 |
| 100,000 | 1,00,000 (one lakh) | 100,000 |
| 10,000,000 | 1,00,00,000 (one crore) | 10,000,000 |

- Use the `en-IN` locale in code: `new Intl.NumberFormat('en-IN')`.
- Decimal separator is a period. Many Indian users also read "5 lakh" or "2 crore"
  in prose; both forms are fine in copy, but be consistent within a page.
- Indic-script digits exist (e.g. Devanagari) but Western digits are the common web norm.

## Currency

- Symbol ₹ (Unicode U+20B9). Code `INR`.
- Schema: `"priceCurrency": "INR"`, price as a plain number with no commas or symbol.
- Show ₹ in visible text; keep the machine-readable price clean.
- Check that fonts include the ₹ glyph.
- Check prices are not shown in USD to Indian visitors without INR.

## Phone

- Country code +91. Mobile numbers are 10 digits and start with 6, 7, 8 or 9.
- Display as `+91 98765 43210`; use `tel:+919876543210` in links.
- Landlines use an STD code, e.g. `011-xxxx xxxx`.
- Schema `telephone`: `"+91-98765-43210"`.

## Address

Typical structure: building or house, street or locality, **landmark**
(commonly used in Indian addresses), city, state, 6-digit PIN.

- PIN code: exactly 6 digits, no spaces. First digit indicates a region.
- India has 28 states and 8 union territories.
- Schema `PostalAddress`: `addressLocality`, `addressRegion` (state),
  `postalCode` (PIN), `addressCountry: "IN"`.
- NAP (name, address, phone) must match across site, Google Business
  Profile and directories, including landmark wording.

## Dates and time

- Date order DD/MM/YYYY (`en-IN`). Avoid ambiguous MM/DD.
- Time zone IST, UTC+05:30. India does not observe daylight saving time.
- Schema and sitemaps use ISO 8601 with offset `+05:30`.

## Tax and business identifiers

- GST: GSTIN is a 15-character identifier. Showing it supports B2B trust.
- Prices: state clearly whether inclusive of GST. Confusion hurts conversion.

## Quick checks

| Check | Pass |
|-------|------|
| Prices show ₹ and INR in schema | yes/no |
| Phone is +91 with working `tel:` link | yes/no |
| PIN code field is 6 digits | yes/no |
| Dates DD/MM/YYYY | yes/no |
| State list includes all states and UTs | yes/no |
| Large numbers use lakh/crore grouping where displayed | yes/no |
