# Sky Gahshomar engine · گاهشمار — rules, sources, API

Flat Python modules (Python 3.12; conda env `luach`). Astronomy: NASA JPL DE440s via Skyfield
(1850–2149). The ephemeris is **not** in the GitHub copy: put `de440s.bsp` in `ephem/` next to the modules, or
set `SKY_EPHEM_DIR`; otherwise it is downloaded from JPL once (on the desktop copy into
`%LOCALAPPDATA%\SkyGahshomar\ephem`, never into the program folder). The Windows desktop zip ships the file.

| module | contents |
|---|---|
| `znames.py` | name tables keyed by the shared key contract (`ROJ`, `GATHA`, `MAH`, `GAH`, `FESTIVAL`, `CALENDAR`), `display()`, `avestan()` transliterator |
| `zcalendars.py` | the five calendars: `to_zdate`, `from_zdate`, `navroz`, `year_layout`, iterators, sunrise-day helpers |
| `iran_solar.py` | Iran's official Nowruz (JPL equinox vs true noon at 52.5° E) and the Iranian civil calendar |
| `festivals.py` | festivals per calendar (`festivals_in_year`, `festivals_between`, `festivals_on`) |
| `sky_layer.py` | five Gahs, Rapithwin season, Moon phases for the Mah Niyayesh, Sun/Moon bearings |
| `sky_engine.py` | JPL astronomy (from Sky Taqwim) + `solar_day`, `sun_transits`, `sun_moon_position` |
| `data/seasons.csv` | every equinox/solstice 1850–2150, with Nowruz under three noon rules |
| `data/navroz_1850_2149.csv` | Navroz and year length for every year of every calendar |
| `data/bastani_nowruz.csv` | Bastani Nowruz 1850–2149 next to persiantools and jdatetime |
| `tests/test_engine.py` | unit tests (`python tests/test_engine.py` or pytest) |
| `validation/validate.py` | full validation, writes `validation/results.json` (see VALIDATION.md) |

## HOW IT WORKS

### 1. One structure, five calendars
Every Zoroastrian calendar has 12 months (*mah*) of 30 days. Each day (*roj*) carries the name of
one of 30 yazatas (Hormazd … Aneran), so the same roj name recurs each month. Five Gatha days
(Ahunavad … Vahishtoisht) complete the 365-day year. When the roj name equals the mah name the day is a
name-day feast (*jashan, parab*). The calendars differ only in **where the year begins**, **whether a leap
day is added**, and (in the reconstruction) **where the Gatha days stand**. Internally every date is a
Julian Day Number, so all conversions are exact integer arithmetic.

| key | year begins | leap day | era(s) | evidence |
|---|---|---|---|---|
| `shahanshahi` | Kadmi date + 30 days; Navroz 15 Aug 2025, 15 Aug 2026 | never | YZ | Maharashtra Govt Gazette 2026 holiday list (Parsi New Year (Shahenshahi) = 15 Aug 2026); All India Radio 16 Aug 2023 |
| `kadmi` | 1 Fravardin YZ 1 = 16 June 632 (Julian) = JDN 1952063, then 365 days a year; Navroz 16 Jul 2025 | never | YZ | RE:Online 2025; epoch = accession of Yazdegerd III (Wikipedia/EIr) — the count reproduces the published Kadmi Navroz exactly |
| `fasli` | 21 March | Avardad-sal-gah on 20 March before a Gregorian 29 Feb (73 times 1850–2149) | YZ (changes at 21 March), ZRE = Gregorian + 1738 | Heritage Institute (Fasli calendar of 1906; ZRE years 3751–3755 from 21 March 2013–2017); Parsi Khabar 2024 |
| `bastani` | Iran's official Nowruz: day of the March equinox if it falls before true solar noon at 52.5° E, else next day | sixth Gatha day when the next Nowruz is 366 days later | ZRE (primary), YZ, SH | Heritage Institute: Bastani = Fasli organisation brought to Iran by Kay Khosrow Shahrokh, adopted in Tehran 1939, months *different* from the civil 31/30-day months; rule for Nowruz from Sky Taqwim (Calendar Center, Univ. of Tehran) |
| `sasanian` | 1 Fravardin of the Yazdegerdi count (same as Kadmi) | none (default) | YZ | reconstruction, see §2 |

Why Kadmi is "one month ahead": the Parsis of India once intercalated a month (dated to the 1120s by the
Heritage Institute) and the Iranians did not; a Kadmi date therefore names the month that comes *after*
the Shahanshahi one on the same civil day (Adar in Shahanshahi = Dae in Kadmi). The engine models this as
Shahanshahi = Kadmi + 30 days, and Kadmi = the unbroken count from Yazdegerd III's accession.

Year numbers: YZ = years of the Yazdegerdi era; each calendar enters the new number on its own Navroz
(Fasli in March, Kadmi in July, Shahanshahi in August — palvkasti.com). Shahanshahi YZ 1396 began on
15 Aug 2026.

**Bastani vs the Zarathushtrian Assembly.** A. A. Jafarey's Zarathushtrian Assembly (California) follows
the Iranian civil months (31/30 days). The Bastani calendar of the Iranian Anjomans keeps 30-day months +
Gatha days; this is why Mehregan (Meher roj of Meher mah) is civil 10 Mehr and the Tir jashan is civil 10 Tir.
Only the Bastani form is implemented.

### 2. The Sasanian reconstruction (a comparison ideal)
Like Sky Luach's "Early Temple Period", this calendar is shown to compare, not to claim anyone keeps it.
- **Andargāh after Avan** (default). al-Biruni reports that in late Sasanian and early Islamic times the five
  epagomenal days (*andargāh*) stood after the 8th month, Ābān; they were moved back to the end of the year in
  375 YZ (1006 CE) (Encyclopaedia Iranica, "Calendars i. Pre-Islamic calendars" and "Kabisa";
  F. de Blois, "The Persian calendar", *Iran* 34, 1996, 39–54; S. H. Taqizadeh, *Old Iranian Calendars*, 1938).
  Option `andargah="after_aspandarmad"` gives the post-1006 arrangement.
- **Intercalation** (`intercalation="kabisa_120"`, off by default). al-Biruni describes a fixed year kept in
  place by intercalating one month every 120 years, the andargāh moving to the end of the intercalated
  month each time. The engine continues that model hypothetically: in YZ 120·k (+`kabisa_phase`) the month
  after the Gatha days is repeated (flag `ZDate.repeated_month`) and the Gatha days follow the repeat.
  EIr "Kabisa" concludes there was "no true intercalation, but rather a periodic readjustment", officially
  enacted only once; hence the default "none". The phase of the cycle is not documented and is a free parameter.
- Festivals: Hamaspathmaedem = the andargāh days; Muktad = the last five days of the month before them plus
  the andargāh (Biruni's Farwardajan). de Blois' hypothesis of a c. 500 CE reform moving Nowruz to 1 Ādar is
  documented here but not modelled.

### 3. The day begins at sunrise
`to_zdate(date)` gives the roj whose daylight falls on that civil date. `zdate_at(datetime, place, cal)`
applies the rule to a moment: before local sunrise the previous roj is still running (Ushahin Gah belongs to
the previous day). Sunrise = Sun's centre at −0.8333° minus the dip of the horizon (0.0347°·√elevation m).
In polar day/night, 06:00 local mean solar time (true noon − 6 h) is used.

### 4. Festivals
See the docstring of `festivals.py` for every rule and source. Summary:
name-day jashans (Dae mah has four: Hormazd, Dae-pa-Adar, Dae-pa-Meher, Dae-pa-Din); six five-day
Gahambars (Maidyozarem Ardibehesht 11–15, Maidyoshahem Tir 11–15, Paitishahem Shehrevar 26–30,
Ayathrem Meher 26–30, Maidyarem Dae 16–20, Hamaspathmaedem = Gatha days); Muktad 10 days from Ashtad
roj of Aspandarmad (11 in Fasli/Bastani leap years), `muktad="parsi_18"` for the old 18-day custom
(Ashishvangh roj of Aspandarmad – Amardad roj of Fravardin); Navroz; Pateti (last day of the year);
Jamshedi Navroz (21 March for all Parsi calendars; `jamshedi="equinox_ist"` for the equinox day in IST;
Iran's Nowruz for Bastani); Khordad Sal; Zarthost no Diso; Farvardigan; Rapithwin Jashan; Iranian Sadeh
(`sadeh="iran"` civil 10 Bahman, `"kerman"` Aban roj Bahman mah, `"yazd"` Ashtad roj Adar mah);
Chaharshanbe Suri (Tuesday evening before the last Wednesday of the Iranian year); Tirgan civil 13 Tir.

### 5. Gahs, Rapithwin, Moon and light
Havan sunrise→true noon; Rapithwin (or Second Havan) noon→noon+3 h; Uziran →sunset; Aiwisruthrem
→solar midnight; Ushahin →next sunrise. The Bombay prayer-guide times (Havan to 12:40, Rapithwin 12:40–3:40)
are Bombay's true noon and noon + 3 h (Mumbai true noon ranges 12:22–12:52 IST through the year).
Rapithwin season: Hormazd roj of Fravardin mah to Aneran roj of Meher mah; Second Havan from Hormazd roj of
Avan mah to Vahishtoisht Gatha (Khordeh Avesta, Kanga tr.), applied in the user's own calendar.
Moon: all four JPL phases; new and full moon flagged for the Mah Niyayesh (antarə.måŋha, pərənō.måŋha;
vīšaptaθa = the half-moon station). `face_the_light()` returns Sun and Moon altitude/azimuth and which
light to face (Sun by day, Moon if up at night, otherwise a lamp/fire).

## API (for the app assembler)

```python
import zcalendars as zc, festivals as F, sky_layer as sl, znames as zn, sky_engine as se
zc.CALENDARS                      # ['shahanshahi','kadmi','fasli','bastani','sasanian']
z = zc.to_zdate(date, cal, **opts)          # ZDate
z.year, z.mah (1..12, 13=Gatha), z.day, z.roj_key, z.mah_key, z.eras, z.day_of_year,
z.is_gatha, z.repeated_month, z.label(), z.roj_names(), z.mah_names()
zc.from_zdate(year, mah, day, cal, repeated=False, **opts) -> date
zc.navroz(year, cal), zc.year_containing(date, cal), zc.year_length / is_leap / year_layout
zc.year_days(year, cal), zc.month_days(year, mah, cal), zc.months_of_year(year, cal)
zc.gregorian_range(start, end, cal), zc.all_calendars(date)
zc.zdate_at(aware_datetime, place, cal), zc.roj_civil_date(aware_datetime, place)
F.festivals_in_year(year, cal, muktad='ten'|'parsi_18', jamshedi='fixed_21_march'|'equinox_ist',
                    sadeh='iran'|'kerman'|'yazd', **opts) -> [Festival(key,start,days,cal,zstart,note,names)]
F.festivals_between(start, end, cal, **kw); F.festivals_on(date, cal, **kw)
sl.gahs(date, place, cal, havan_meher=False) -> {'zdate','rapithwin_season','gahs':[Gah(key,start,end,note)],'polar','sun'}
sl.gah_at(aware_datetime, place, cal) -> (Gah, ZDate)
sl.moon_phases(start, end, tz) ; sl.face_the_light(aware_datetime, place)
zn.display(zn.ROJ, key) -> 'English · Persian · Gujarati'; zn.ROJ[key]['ae'] (Avestan script)
```
`opts`: Sasanian `andargah='after_avan'|'after_aspandarmad'`, `intercalation='none'|'kabisa_120'`,
`kabisa_phase=int`; Bastani `rule='true_noon_52.5'|'mean_noon_52.5'|'true_noon_tehran'`.
A *place* is a dict `{name, lat, lon, tz, elev?}` as in Sky Luach / Sky Taqwim (`se.UDVADA`, `se.MUMBAI`,
`se.YAZD`, `se.TEHRAN` provided).

Extra keys beyond the shared contract: festival keys `rapithwin_jashan`, `tirgan_civil`; `znames.CALENDAR`;
name fields `ae_tr` (Avestan transliteration), `meaning`, `fa_alt` (variant Persian spelling).
`farvardigan` and `jashan_fravardin` fall on the same day by definition.

Range: 1850-01-01 … 2149-12-31 for all calendars (Bastani uses arithmetic Nowruz for 1849 and 2150 only to
close the first and last years; `iran_solar.nowruz_source()` tells which).

Sources (short list): al-Bīrūnī, *Chronology of Ancient Nations* (Sachau tr. 1879) and *al-Qānūn al-Masʿūdī*;
Encyclopaedia Iranica: "Calendars i" (Panaino), "Kabisa", "Gāhānbār"; de Blois 1996; Taqizadeh 1938;
M. Boyce, "On the calendar of Zoroastrian feasts", BSOAS 33 (1970); K. E. Eduljee, Heritage Institute
Zoroastrian calendar pages 1–3; Khordeh Avesta (Kanga, English tr.); R. P. Karanjia on Muktad; Sky Taqwim
`solar_hijri_calendar.py` (Nowruz rule).
