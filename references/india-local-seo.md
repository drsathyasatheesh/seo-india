# India Local SEO

Load when scoring "Local presence" or running `local`. Use with `seo-local` and
`seo-maps` for the generic method; this file covers India specifics.

## Google Business Profile

- Claim and verify the profile; Google is by far the dominant search engine in
  India (about 98% share per StatCounter, Oct 2026), so GBP is the main local surface.
- Use an Indian-format address with landmark and PIN. Keep it identical everywhere.
- Primary category accurate; add secondary categories honestly.
- Add the +91 number, hours (IST, include festival-day changes), photos, services
  and products.
- WhatsApp and appointment links where available.
- Reply to reviews in the reviewer's language when possible.
- Service-area businesses: list the areas actually served; do not hide the
  address if customers visit.

## City, locality and PIN-code pages

- Create a page per **real** service location or service area with unique content:
  local landmarks, local team, local reviews, local pricing or availability.
- Do not mass-produce near-identical city pages that swap only the city name; that
  is thin content and a spam risk. Use `seo-programmatic` quality gates.
- Tier-2 and tier-3 cities are often less competitive and worth targeting
  if the business can really serve them. **Verify demand per city with real keyword data.**

## NAP and directories

Consistency matters across: website, GBP, social profiles, and directories.
Commonly relevant Indian directories include Justdial, Sulekha, IndiaMART
(B2B), TradeIndia (B2B) and category sites (health, education, real estate,
travel). **Check which are active and relevant for the specific category
before recommending; directory importance varies.**

## Reviews

- Encourage reviews on Google first. Offer a short link or QR that opens the review form.
- Never buy, gate or fake reviews.
- Monitor for reviews in regional languages and respond appropriately.

## Schema

`LocalBusiness` (or a specific subtype) with `PostalAddress` (state in
`addressRegion`, PIN in `postalCode`, `addressCountry: "IN"`), `telephone`,
`openingHoursSpecification`, `geo`, `areaServed`, `sameAs`. Validate with
`seo-schema`.

## Language for local

- Provide key local pages in the local language of the city (for example
  Tamil for Chennai, Marathi for Pune) where the audience is likely to search
  in it. Validate with real query data first.
- Use transliterated place names and local spellings (for example Bengaluru /
  Bangalore, Mumbai / Bombay); cover both when both are searched.

## Output

Local score 0-100 with: GBP completeness, NAP consistency, location-page quality,
directory coverage, review profile, and a ranked action list. State which items
needed live data you could not access.
