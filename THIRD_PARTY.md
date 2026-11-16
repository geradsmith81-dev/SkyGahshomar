# Third-party material

Sky Gahshomar's own code is under the MIT License (see [LICENSE](LICENSE)), the same licence and copyright holder
as its sibling apps Sky Luach and Sky Taqwim. The material below keeps its own licence.

## Linked texts (not included)

- **Prayer texts** are not part of the app. Prayer names link to Avesta -- Zoroastrian Archives
  (https://www.avesta.org/, ed. Joseph H. Peterson), which hosts the Avestan texts and translations (Kanga's Khorda
  Avesta; Darmesteter and Mills, Sacred Books of the East). Their copyright and terms are those of that site.

## Data and models

- **NASA JPL DE440s** planetary ephemeris (`ephem/de440s.bsp`, not in the GitHub repository; downloaded from
  ssd.jpl.nasa.gov on first run if missing). A work of the US government (NASA/JPL-Caltech), no copyright in the US.
- **World Magnetic Model 2025** (`wmm/WMM_2025.COF`; NOAA NCEI and the British Geological Survey). A US government
  work, public domain. Used through the **pygeomag** package (MIT licence, https://github.com/boxpet/pygeomag) for the
  magnetic declination of the live 'Face the light' compass. The file is the copy distributed with pygeomag 1.1.0.
- **GeoNames** city list through the **geonamescache** package (MIT licence; GeoNames data CC BY 4.0,
  https://www.geonames.org) for the place search and the automatic place name.
- `data/seasons.csv` (equinoxes and solstices 1850–2150) is computed by this app's own engine from DE440s; the
  Bastani Nowruz rule follows Sky Taqwim (MIT, same author).

## Validation-only material (not used by the app)

- The **ZANC / Heritage Institute JavaScript converter** (`zcalendar.js`, Kainaz Amaria / Zarthoshti Anjuman of
  Northern California, CC BY-NC-SA 1.0) is used only by `validation/validate.py`, which downloads it at run time.
  **No code from it is shipped** in this package, and no code in Sky Gahshomar is adapted from it.
- `validation/heritage_fasli_grid.csv` and `validation/published_dates.csv` record dates (facts) read from the
  published sources named in each row (Heritage Institute calendar pages, government gazettes, press reports), for
  comparison only.
- `persiantools` (MIT) and `jdatetime` (Python Software Foundation licence) are optional cross-checks in validation.

## Software used by the app

Streamlit (Apache-2.0), Skyfield (MIT), NumPy (BSD-3-Clause, with bundled parts under 0BSD, MIT, Zlib, CC0), pandas (BSD-3-Clause), pygeomag (MIT),
geonamescache (MIT), tzdata (Apache-2.0). They are installed from PyPI (requirements.txt), not shipped here.

## Code adapted from the sibling apps

`locator.py`, `device.py`, `places.py` and `face_light_live.py` are adapted from Sky Taqwim
(https://github.com/geradsmith81-dev/sky-taqwim, MIT, © 2026 Gerad Smith); `sky_engine.py` likewise.

## Fonts (assets/fonts/)

All three are licensed under the **SIL Open Font License, Version 1.1** (licence texts alongside the font files).
None of the three licences declares a Reserved Font Name, so the subset files may keep their family names.
The subsets were made with fontTools 4.68.0 (`pyftsubset` options: all OpenType layout features kept,
hinting dropped); `.woff2` files are embedded in the app's CSS as data URIs (theme.py), `.ttf` files are for rendering SVG text
with resvg. A subset is a Modified Version under the OFL; it is distributed under the same licence.

| Font | Version | Copyright | Source | Subset to | Files |
|---|---|---|---|---|---|
| Noto Sans Avestan Regular | 2.003 | © 2022 The Noto Project Authors | https://github.com/notofonts/avestan (file from notofonts.github.io) | Avestan block U+10B00–10B3F, U+2E31, U+00B7, space, ZWNJ/ZWJ, bidi marks | NotoSansAvestan-Regular-sub.woff2 / .ttf, OFL-NotoSansAvestan.txt |
| Vazirmatn Regular and Bold | 33.003 | © 2015 The Vazirmatn Project Authors | https://github.com/rastikerdar/vazirmatn | Arabic script for Persian U+0600–06FF, presentation forms U+FB50–FDFF and U+FE70–FEFF, « », U+00B7 | Vazirmatn-Regular-sub / Vazirmatn-Bold-sub (.woff2 / .ttf), OFL-Vazirmatn.txt |
| Noto Sans Gujarati Regular and Bold | 2.106 | © 2022 The Noto Project Authors | https://github.com/notofonts/gujarati (file from notofonts.github.io) | Gujarati block U+0A80–0AFF, danda U+0964–0965, U+25CC | NotoSansGujarati-Regular-sub / -Bold-sub (.woff2 / .ttf), OFL-NotoSansGujarati.txt |

Embedded in the CSS: Avestan, Vazirmatn Regular and Bold, Gujarati Regular (78,564 bytes of woff2 in total). Gujarati Bold is supplied for SVG and
future use but is not embedded; the browser makes bold Gujarati from the Regular weight.

## Artwork (ornaments.py, assets/svg, icons)

All SVG art in ornaments.py is original, drawn from simple geometry in code for this app. Nothing is traced from photographs or copied from
existing drawings. The motifs follow Achaemenid monuments that are themselves in the public domain: the winged figure over the Behistun inscription
and on the Persepolis doorways and tombs (Faravahar), the Persepolis twelve-petalled rosette and lotus-and-bud friezes, the double-protome bull
and griffin capitals, the stepped fire altar of the Naqsh-e Rostam tomb reliefs, and the colours of the Susa glazed-brick friezes. The icons
(gahshomar_icon.ico, launcher PNGs) are rendered from these SVGs with resvg (resvg-py, MIT/Apache-2.0) and Pillow (MIT-CMU licence).
