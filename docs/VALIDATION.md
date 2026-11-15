# VALIDATION — Sky Gahshomar calendar engine

Generated from `validation/results.json` (run `python validation/validate.py`). Range checked: every civil date 1 Jan 1850 – 31 Dec 2149 (109,573 days), the span of JPL DE440s.

## Summary

| check | compared | agree | notes |
|---|---|---|---|
| A. Published dates (gazette, broadcasters, community sources) | 15 | 15 | table below |
| B. ZANC/Heritage Institute converter, shahanshahi, day by day | 109,573 | 109,573 | roj + mah identical every day |
| B. ZANC/Heritage Institute converter, kadmi, day by day | 109,573 | 109,573 | roj + mah identical every day |
| B. ZANC/Heritage Institute converter, fasli, day by day | 109,573 | 109,573 | roj + mah identical every day |
| C. Heritage Institute Fasli/Bastani perpetual grid | 363 cells | 363 | 338 cells carry a month name, all checked |
| D. Bastani Nowruz vs persiantools 6.2 | 300 years | 300 | |
| D. Bastani Nowruz vs jdatetime | 300 years | 299 | differs in [2124] (see below) |
| D. Nowruz vs Sky Taqwim's published data/seasons.csv (3 rules) | 300 years × 3 | all | 0 differences; equinox times identical (max diff 0.0 s) |
| E. Internal consistency (5 calendars + 2 Sasanian variants) | 7 × 109,573 days | all | round-trip and day-sequence failures: 0 |
| E. Festival structure | 47,838 festival instances | 47,838 | |
| F. Gah structure (6 places × 12 dates × 2 calendars) | 144 | 144 | contiguous, ordered, Rapithwin season correct |

## A. Published dates

| calendar | civil date | published as | engine | ok | source |
|---|---|---|---|---|---|
| shahanshahi | 2026-08-15 | Parsi New Year (Shahenshahi) 2026 | Hormazd roj, Fravardin mah, YZ 1396 | ✓ | Maharashtra Govt Gazette Extraordinary No.184 (8 Dec 2025), GAD notification PHD-1125/C.R.199/Japuk(29) of 5 Dec 2025, as listed on mmrda.maharashtra.gov.in/en/public-holidays (year number: aazad.com, palvkasti.com "1396 Y.Z.") |
| shahanshahi | 2025-08-15 | Navroze, Shenshai 2025 | Hormazd roj, Fravardin mah, YZ 1395 | ✓ | RE:Online festival calendar (reonline.org.uk) |
| kadmi | 2025-07-16 | Navroze, Kadmi 2025 | Hormazd roj, Fravardin mah, YZ 1395 | ✓ | RE:Online festival calendar (reonline.org.uk) |
| shahanshahi | 2023-08-16 | Navroz celebrated today | Hormazd roj, Fravardin mah, YZ 1393 | ✓ | newsonair.gov.in (All India Radio), 16 Aug 2023 |
| shahanshahi | 2020-08-06 | Muktad begins Thursday 6 Aug 2020, Roj Ashtad Mah Aspandarmad YZ 1389 | Ashtad roj, Aspandarmad mah, YZ 1389 | ✓ | avesta.org WZSE #377 (Mobed recollections, 2020) |
| shahanshahi | 2007-08-15 | First Gatha day Ahunavaiti, 15 Aug 2007 | Ahunavad Gatha, YZ 1376 | ✓ | Heritage Institute, Pateti page (photo caption) |
| fasli | 2024-03-20 | Roz-e Vahizak (leap day) 20 Mar 2024 | Avardad-sal-gah Gatha, YZ 1393 | ✓ | Parsi Khabar, "Jamshedi Navroze Mubarak 2024" |
| fasli | 2024-03-21 | Roj Hormuzd Mah Fravardin 21 Mar 2024 | Hormazd roj, Fravardin mah, YZ 1394 | ✓ | Parsi Khabar, "Jamshedi Navroze Mubarak 2024" |
| fasli | 2013-03-21 | 3751 ZRE starts March 21 2013 | Hormazd roj, Fravardin mah, YZ 1383 | ✓ | Heritage Institute calendar page 1 (Dabih Behruz system) |
| fasli | 2014-03-21 | 3752 ZRE starts March 21 2014 | Hormazd roj, Fravardin mah, YZ 1384 | ✓ | Heritage Institute calendar page 1 |
| fasli | 2015-03-21 | 3753 ZRE starts March 21 2015 | Hormazd roj, Fravardin mah, YZ 1385 | ✓ | Heritage Institute calendar page 1 |
| fasli | 2016-03-21 | 3754 ZRE starts March 21 2016 | Hormazd roj, Fravardin mah, YZ 1386 | ✓ | Heritage Institute calendar page 1 |
| fasli | 2017-03-21 | 3755 ZRE starts March 21 2017 | Hormazd roj, Fravardin mah, YZ 1387 | ✓ | Heritage Institute calendar page 1 |
| fasli | 2010-03-21 | March 21 to Dec 31 2010 fall in year 3748 | Hormazd roj, Fravardin mah, YZ 1380 | ✓ | Heritage Institute calendar page 1 |
| bastani | 2027-10-02 | Mehregan 10 Mehr 1406 = Sat 2 Oct 2027 (Mehr roj of Mehr mah) | Meher roj, Meher mah, ZRE 3765 | ✓ | surfiran.com Iranian festivals calendar 2026/2027 |

### The disputed Shahanshahi Navroz of 2026 (15 or 16 August)

**Resolved: Saturday 15 August 2026 (1 Fravardin YZ 1396).** Evidence:

1. The Government of Maharashtra's 2026 public-holiday list (Government Gazette Extraordinary No. 184 of 8 Dec 2025, General Administration Department notification of 5 Dec 2025) lists *Parsi New Year (Shahenshahi)* on 15 August 2026, the same day as Independence Day; the list is reproduced on the MMRDA government website.
2. Arithmetic: the Shahanshahi year has exactly 365 days. Navroz was 15 Aug 2025 (RE:Online); no 29 February lies between 15 Aug 2025 and 15 Aug 2026, so the next Navroz is again 15 August. It moves to 14 August only in 2028.
3. The independent ZANC converter (part B) gives 15 Aug 2026.

Several commercial websites (e.g. ganeshaspeaks, calendarr, neckbands, jikadragraphic, thecoochikoo, aazad) give Sunday 16 August 2026, and one travel site gives both dates in the same article. These pages offer no calendar reasoning; the likeliest cause is carrying over the 2020–2023 date (16 August) without the leap-year step of 2024. One also gives 16 Aug 2024, which contradicts the same arithmetic. They are recorded here as disagreeing secondary sources, not as evidence.

## B. Independent converter (ZANC / Heritage Institute)

The JavaScript converter on heritageinstitute.com (`zcalendar.js`, adapted from the Zarthoshti Anjuman of Northern California, Kainaz Amaria, CC BY-NC-SA 1.0) was downloaded and run unmodified with the `quickjs` package, one call per civil date at local noon. It is a separate implementation (anchored on 21 March 1129 and on 16 July 632), so agreement is a genuine cross-check. Its code is **not** redistributed in this package because of its non-commercial licence; `validate.py` fetches it at run time.

- Shahanshahi, Kadmi, Fasli: 0 roj/mah mismatches in 109,573 days each (its leap-day label 'Avardad-sal-Gah' maps to the engine's `avardad_sal_gah`).
- **Year numbers differ:** on 20 Aug 2026 ZANC shows YZ 1394, the engine YZ 1396. The engine is right: avesta.org (WZSE 377) dates 6 Aug 2020 to 'Roj Ashtad Mah Aspandarmad YZ 1389', so Navroz 16 Aug 2020 began YZ 1390 and 15 Aug 2026 begins YZ 1396; Parsi calendars for 2026–27 are headed 1396 Y.Z. ZANC's year counter is two years behind (its display hides the year).

## C. Heritage Institute perpetual grid

K. E. Eduljee's '365-Day Fasli-Bastani/Gregorian Perpetual Calendar Grid' (page 2) was transcribed from the page text into `validation/heritage_fasli_grid.csv`: 30 roj × 12 mah + 4 Gatha days = 364 cells, of which one (Ashtad roj, Aspandarmad mah) shows only the label 'Farvardigan/Muktad' and is not compared. All 363 remaining cells agree with Fasli YZ 1395 (21 Mar 2025 – 20 Mar 2026). The grid marks a 'Leap Year' shift from Meher roj of Aspandarmad; the engine puts that roj on 2028-02-29 in leap year YZ 1397 and the Avardad-sal-gah on 2028-03-20 — consistent. The grid's festival marks also agree: Khordad Sal 26 Mar, Farvardingan 8 Apr, Tirgan 1 Jul, Mehergan 2 Oct, Zarthost Diso 26 Dec, Maidyarem from 31 Dec, Sadeh-Iran 30 Jan, Sadeh-Kerman 24 Jan, Sadeh-Yazd 11 Dec, Hamaspathmaidyem from 16 Mar.

## D. Bastani Nowruz (Iran's official Nowruz)

Rule: day of the JPL March equinox if it precedes true solar noon on 52.5° E, otherwise the next day (Sky Taqwim rule). Table: `data/bastani_nowruz.csv`.

- persiantools 6.2 (which encodes the astronomical calendar, with ICU4X corrections after 1501 SH): 0 differences in 300 years.
- jdatetime (33-year arithmetic) and the 'mean noon' rule: 1 difference, **2124**. The JPL equinox, 2124-03-20T08:38:00 UT, falls only 8.3 s before true noon at 52.5° E (and 8.0 min after 12:00 IRST). The engine gives 20 March 2124; mean-noon/arithmetic gives 21 March. An 8-second margin is smaller than the uncertainty of ΔT a century ahead, so 2124 is **provisional** and flagged.
- It is the only year 1850–2149 with the equinox within 2 minutes of true noon.
- JPL equinox times agree with the Nowruz infobox on Wikipedia to 1.1 s (2025: 09:01:28.9 vs 09:01:30 UT) and 1.6 s (2026: 14:45:57.4 vs 14:45:59); for 2027 the engine has 20:24:41 vs Wikipedia's 20:24:18 (23 s; the Wikipedia source is not stated). None of these is near a decision boundary.

## E. Internal consistency, 1850–2149

| calendar | years | year lengths | round-trip failures | sequence failures |
|---|---|---|---|---|
| shahanshahi | 1219–1519 | 365 d × 301 | 0 | 0 |
| kadmi | 1219–1519 | 365 d × 301 | 0 | 0 |
| fasli | 1219–1519 | 365 d × 228, 366 d × 73 | 0 | 0 |
| bastani | 3587–3887 | 365 d × 228, 366 d × 73 | 0 | 0 |
| sasanian | 1219–1519 | 365 d × 301 | 0 | 0 |
| sasanian:andargah=after_aspandarmad | 1219–1519 | 365 d × 301 | 0 | 0 |
| sasanian:intercalation=kabisa_120 | 1218–1518 | 365 d × 299, 395 d × 2 | 0 | 0 |

- Kadmi date = Shahanshahi date of the civil day 30 days later: 0 failures.
- Fasli Navroz on 21 March: 0 failures in 300 years; Fasli leap year ⇔ the following February has 29 days: 0 failures (73 leap years; 1900 and 2100 correctly common).
- Bastani Mehregan (Meher roj, Meher mah) = civil 10 Mehr: 0 failures in 299 years (matches Iran's official calendar); Tir jashan = civil 10 Tir: 0 failures; Bastani leap ⇔ civil Esfand has 30 days: 0 failures.
- Festival structure (47,838 instances, all five calendars): Khordad Sal on Khordad roj of Fravardin, Zarthost no Diso on Khorshed roj of Dae, each name-day jashan on roj = mah, four Dae jashans, Gahambars of 5 days, Muktad ending on the last day of the year (Sasanian: on the last andargāh day): 0 failures.

## F. Gahs and the sunrise day

- 1 minute before sunrise on 15 Aug 2026 at Mumbai: Vahishtoisht Gatha, YZ 1395; 1 minute after: Hormazd roj, Fravardin mah, YZ 1396.
- Mumbai true noon through 2026: 12:22–12:52 IST, bracketing the fixed 12:40 used by Parsi prayer guides for the start of Rapithwin; the engine uses the true noon of the day.
- Sunrise/sunset/transit come from Skyfield on DE440s with the same horizon convention as Sky Taqwim's prayer times (validated there against JPL Horizons); they were not re-validated here against a Parsi almanac (none obtained).

## What could not be validated

- **No Parsi panchang/almanac PDF or Indian Government (central) holiday list series was obtained** for 1850–2025; only the single-year sources in table A. The day-by-day agreement with the independent ZANC converter covers the whole range, but that converter is itself a computation, not a printed almanac.
- **No Iranian Zoroastrian Anjoman gahshomar** (Tehran/Yazd/Kerman) was obtained; the Bastani structure rests on the Heritage Institute description and on the agreement of Bastani Mehregan with Iran's official 10 Mehr.
- zanc.org/zcal was not reachable from the sandbox (not on the network allowlist); the Heritage Institute hosts the same converter.
- The Sasanian reconstruction has, by its nature, no modern reference; its parameters are documented choices.
- Gujarati and Persian spellings of names (znames.py) are best-effort and should be reviewed by a Gujarati-reading Parsi priest or scholar; the Avestan script is generated from standard transliterations (Unicode U+10B00 block).
- Gah boundaries follow the published rule (true noon, noon + 3 h, sunset, solar midnight); no printed Gah timetable was compared minute by minute.


---

## App assembly checks (November 2026)

These checks were run on the assembled Streamlit app (conda env `luach`: Python 3.12, Streamlit 1.67.0, Skyfield 1.54,
pygeomag 1.1.0, quickjs 1.19.4) on Windows. Scripts are in `tools/`; results in `tools/apptest_results.json`.

### Engine after the name reconciliation
`znames.py` now re-exports the content track's `names.py` (see docs/NAMES_RECONCILIATION.md). `tests/test_engine.py`
passes (9/9) and `validation/validate.py` was re-run: `validation/results.json` is identical to the engine track's
file (no value changed), since the calendars use keys, not spellings.

### Streamlit AppTest sweep (`python tools/apptest_sweep.py`)
**1040 runs, 1040 passed, 0 failed** (200 s). Every run checks: no exception; the page's own
HTML marker; outside Compare only the chosen calendar's badge; Compare shows all five; popovers use `gs-` classes;
no inline `<svg>` passed to `st.html`; the Gahs page has the `gs-times` table with today's `gs-today-row`.

| group | runs | what |
|---|---|---|
| A default | 2 | first visit = Parsi Shahanshahi preset at Mumbai; calendar labels 'English · Persian · Gujarati' |
| B presets | 99 | all 11 community presets (sidebar) × 9 pages; calendar, Muktad, Rapithwin and era applied |
| C calendars × places | 405 | 5 calendars × 9 pages × 9 places (Mumbai, Udvada, Yazd, Karachi, London, Toronto, Los Angeles, Sydney, Tromsø 69.6° N) |
| D dates | 96 | Gatha days of each calendar, Fasli and Bastani leap days (Avardad-sal-gah), polar night and polar day at Tromsø, before sunrise, Navroz 2026, 29 Feb 2028, range edges Jan 1850 and Dec 2149, 6 pages each |
| E settings | 339 | Muktad 18, Bundahishn rule, eras, Jamshedi rule, Sadeh variants, Iranian observances, Havan-ni-Meher, phone layout (× 5 calendars × 6 pages); 3 Bastani Nowruz rules; 4 Sasanian model settings |
| F interactions | 99 | every Traditions 'Use' button; month navigation; 14 months forward in every calendar (incl. the Gatha 'month') |

Defects found and fixed during the sweep: `theme.moon()` returned inline SVG (stripped by `st.html`; now a data-URI
`<img>`); date widgets and Moon/Sun queries at the 1850/2149 range edges (now clamped to the DE440s span).

### JavaScript (`python tools/js_check.py`)
The two browser components (`face_light_live.JS`, `locator.JS`) compile as ES modules in QuickJS and run with a stub
DOM through the no-compass, lamp, iPhone (permission button) and Android (absolute orientation) branches: 10/10 ok.
The launcher's inline script and `sw.js` also parse. This is a syntax and smoke check, not a test on a phone.

### Fonts
Every Persian (42), Gujarati (55) and Avestan (54) code point used in the app's strings and documents is in the
shipped WOFF2 subsets (Vazirmatn Regular/Bold, Noto Sans Gujarati Regular/Bold, Noto Sans Avestan); no re-subset was
needed. Gujarati Bold is now embedded as well.

### Visual previews (headless Edge)
`tools/render_previews.py` writes the HTML each page passes to `st.html` (theme CSS included; Streamlit's widgets are
imitated, the live compass replaced by its static drawing). Headless Edge crashed (0xC0000005) on most full-page
renders in this sandbox, more often the longer the page, with or without the embedded fonts; each block tried rendered
on its own. The previews were therefore rendered block by block and stitched. The crash was not reproducible as a
single faulty element, so it is attributed to the sandboxed headless browser; it has not been checked in a normal
desktop browser. The previews led to two fixes: day names overflowing Month cells (now stacked, wrapping after the
Avestan word separator) and the static compass arrow (now drawn at the bearing).

### Not checked
- No live server: HTTP to localhost is blocked in this sandbox, so `streamlit run` was not opened in a browser; the
  components (automatic location, live compass on a real phone) were not exercised end to end.
- Published-date checks remain as in the engine sections above (including the open Shahanshahi Navroz 2026 item).
