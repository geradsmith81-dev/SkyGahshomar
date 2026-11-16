# Sky Gahshomar · گاه‌شمار آسمان

The Zoroastrian calendars, from NASA JPL astronomy (DE440s via Skyfield, 1850–2149): **Shahanshahi, Kadmi, Fasli and
the Iranian Bastani**, plus a **Sasanian reconstruction** shown for comparison only. The Zoroastrian sibling of
[Sky Luach](https://github.com/geradsmith81-dev/sky-luach) (Jewish) and [Sky Taqwim](https://github.com/geradsmith81-dev/sky-taqwim) (Islamic).

- **Pages:** Today (roj · mah · year, the current Gah, festivals with their histories, the Moon and the Mah Niyayesh,
  and a live *Face the light* compass toward the Sun or the Moon), Month, Year, Gahs (timetable), Prayers (the official prayers as links to their texts), Festivals, Compare
  (the only page that shows all five calendars side by side), Traditions (communities with *Use* presets), How it
  works, About.
- **Names** in English · Persian · Gujarati, with Avestan script for the roj and Gatha day names (`names.py`).
- **Location** found automatically (the browser asks once), or chosen from presets (Mumbai, Udvada, Navsari, Surat,
  Karachi, Yazd, Kerman, Tehran, London, Toronto, Los Angeles, Sydney) or any town of 15,000+ people.
- Default: the Parsi Shahanshahi preset at Mumbai.

See [HOW_IT_WORKS.md](HOW_IT_WORKS.md) for the rules and sources, [docs/VALIDATION.md](docs/VALIDATION.md) for the
checks, and [docs/NAMES_RECONCILIATION.md](docs/NAMES_RECONCILIATION.md) for the spellings.

## Run it on a computer (Windows)

Double-click **Start app.bat** (first run installs the components into `.venv`, 2–5 minutes). The app opens at
http://localhost:8513. **Create desktop icon.bat** puts a Sky Gahshomar icon on the Desktop and in the Start menu.
The NASA JPL file `ephem/de440s.bsp` (32.7 MB) must be in the `ephem` folder; if it is missing it is copied from
`C:\AfterglowApp\ephem` when present, or downloaded once from JPL.

Or, with Python 3.12:

```
pip install -r requirements.txt
streamlit run app.py --server.port 8513
```

## Put it online (GitHub + Streamlit Community Cloud)

1. Create a public repository `sky-gahshomar` and upload everything in this folder (keep the folders), **without**
   `ephem/de440s.bsp` (GitHub's web upload limit is 25 MB; the app downloads it on its first start).
2. If the hidden `.streamlit` folder was skipped, create `.streamlit/config.toml` and paste the contents of
   `config.toml for GitHub (paste).txt`.
3. At https://share.streamlit.io choose **Create app**, the repository, branch `main`, file `app.py`, and under
   **Advanced settings** Python **3.12**.

## Tests

- `python tools/check_prayer_links.py` checks every prayer link (needs internet).
- `python tools/prayer_apptest.py` runs focused headless checks of the prayer links.


```
pip install -r requirements-validation.txt
python tests/test_engine.py            # engine unit tests
python validation/validate.py          # full engine validation (writes validation/results.json)
python tools/apptest_sweep.py          # Streamlit AppTest sweep of every page, calendar, preset and several places
python tools/js_check.py               # syntax and smoke check of the two browser components (quickjs)
```

## License

MIT License, copyright (c) 2026 Gerad Smith. See [LICENSE](LICENSE). Fonts (SIL OFL 1.1), the JPL ephemeris and
WMM2025 (public domain), pygeomag (MIT) and GeoNames data keep their own terms: see [THIRD_PARTY.md](THIRD_PARTY.md).
