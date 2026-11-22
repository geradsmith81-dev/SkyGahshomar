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

Download `SkyGahshomar_desktop.zip` from the release, check it against `SHA256SUMS.txt`
(`Get-FileHash SkyGahshomar_desktop.zip -Algorithm SHA256`), unzip it anywhere and double-click **Start app.bat**.
The first run installs the tested, checksum-verified components into `.venv` (2–5 minutes, Python 3.12 or newer;
tested with 3.15) and puts a Sky Gahshomar icon on the Desktop and in the Start menu (**Create desktop icon.bat**
makes it again). The app then opens in its own window at http://localhost:8513, with no console window; it stops
about 90 seconds after its window is closed, or at once with **Quit Sky Gahshomar** at the bottom of the page.
**Share on this network.bat** opens it to phones and other computers on the same network, behind a new password each
time. The NASA JPL file `ephem/de440s.bsp` (32.7 MB) ships with the desktop copy. See `READ ME FIRST.txt` in that zip.

## Run locally

Install the exact, checksum-verified versions the app was tested with (Python 3.12 or newer):

```
python -m venv .venv
.venv\Scripts\python -m pip install --require-hashes --only-binary ":all:" -r requirements.txt
.venv\Scripts\python -m streamlit run app.py --server.address 127.0.0.1
```

`requirements.in` lists the direct components; `requirements.txt` is the full lock with SHA-256
hashes (generated with `uv pip compile requirements.in --universal --python-version 3.12
--generate-hashes --only-binary :all:`). The same lock serves Streamlit Community Cloud.

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

## Security and privacy

- The Windows desktop copy of Sky Gahshomar listens on this computer only (127.0.0.1). "Share on this network.bat" can open it to the local network, protected by a new password each time; only the person at the computer sees the Quit button.
- The desktop copy keeps its logs (and, only if a shipped data file is missing, a rebuilt copy of it) in `%LOCALAPPDATA%\SkyGahshomar`, checks its program files against `MANIFEST.sha256` at every start, and each release publishes SHA-256 checksums of its zips in `SHA256SUMS.txt`.
- All components are pinned to exact versions and installed with `--require-hashes`.
- The desktop-only code (`desktop.py`) does nothing on a hosted copy: no Quit button is shown there.
- Sky Gahshomar stores no personal data. Your place (from the browser or typed in) is used only in the current session and never written to disk.
