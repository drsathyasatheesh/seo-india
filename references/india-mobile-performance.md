# India Mobile and Device Performance

Load when scoring "Mobile and device performance".

## Why this differs from US advice

Measured median mobile download speeds in India have risen sharply with 5G
(Ookla reported about 131 Mbps for Aug 2025; this is a self-selected sample and
**changes over time, so re-check before quoting**). Raw bandwidth is therefore
often not the bottleneck. The common bottlenecks are:

1. **Device CPU and RAM.** A large share of users are on budget phones. Heavy
   JavaScript parses and runs slowly there. (The exact share is **unverified**;
   do not quote a figure without a source.)
2. **Data caps and cost.** Large pages and autoplay video burn limited data.
3. **Uneven coverage and network switching** outside major cities.
4. **Third-party script weight**: ads, chat widgets, tag managers.

## Test method

1. Measure with real data where possible: CrUX field data via `seo-google`,
   filtered to India if the source allows.
2. Lab-test with **CPU throttling** (for example 4x or 6x slowdown in Chrome
   DevTools or Lighthouse), not only network throttling.
3. Also run a slow-network profile to cover weak coverage.
4. Compare against Core Web Vitals thresholds (good: LCP at most 2.5 s, INP at
   most 200 ms, CLS at most 0.1; confirm current thresholds in `seo-technical`).

## Checks

| Area | What to look for |
|------|------------------|
| JavaScript | Total JS size, long tasks, hydration cost, unused code |
| Fonts | Indic webfonts can be large; subset, preload the one in use, `font-display` |
| Images | AVIF/WebP, correct sizes, lazy-load below the fold, no huge hero on mobile |
| Video | No autoplay with sound or full-size background video on mobile |
| Third parties | Count and weight of tags, widgets and chat tools; defer or remove |
| Layout shift | Reserve space for images, ads and late-loading fonts |
| Input responsiveness | Tap targets large enough, no main-thread blocking on tap |
| Offline/slow | Graceful loading state, content visible before scripts finish |
| Data use | Total transfer on first load; flag pages over a few MB on mobile |

## Findings to prioritise

1. Large JS bundles blocking interaction on throttled CPU.
2. Unoptimised Indic font files.
3. Oversized images and background video.
4. Heavy third-party tags.

## Output

Report lab results with the throttling settings used, the field data source
and date if any, and what could not be tested.
