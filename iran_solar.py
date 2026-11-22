"""
Iran's official Nowruz day and the Iranian civil (solar Hijri) calendar, from NASA JPL astronomy.

The Bastani calendar of the Iranian Zoroastrians begins its year on Iran's official Nowruz.
The rule (taken over from Sky Taqwim's solar_hijri_calendar.py): the year begins on the day of the
March equinox if the equinox falls before noon, otherwise on the next day. "Noon" is, by default,
true (apparent) solar noon on the 52.5 E meridian (the meridian of Iran Standard Time), as reckoned
by the Calendar Center of the Institute of Geophysics, University of Tehran ("true_noon_52.5").
Alternatives for comparison: "mean_noon_52.5" (12:00 IRST = 08:30 UT) and "true_noon_tehran".

The civil calendar (law of 31 March 1925): Farvardin..Shahrivar 31 days, Mehr..Bahman 30,
Esfand 29 or 30. It is used here only for Iranian festivals defined by civil dates (Sadeh on
10 Bahman, Tirgan on 13 Tir, Chaharshanbe Suri) and for the 'SH' era label.

Precomputed table: data/seasons.csv (every equinox/solstice 1850-2150 with the Nowruz date under
each rule). It is rebuilt from the ephemeris if missing (about 5 s).
"""
from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache

import pandas as pd

import sky_engine as se

HERE = os.path.dirname(os.path.abspath(__file__))
SEASONS_FILE = os.path.join(HERE, "data", "seasons.csv")      # shipped with the app
# rebuilt here if the shipped table is missing (desktop copy: %LOCALAPPDATA%\\SkyGahshomar\\data, never the program folder)
SEASONS_REBUILT = os.path.join(se._fallback_dir("data"), "seasons.csv")
IRST = timezone(timedelta(hours=3, minutes=30))
RULES = {
    "true_noon_52.5": "Equinox before true solar noon on the 52.5 E meridian (Calendar Center, Univ. of Tehran)",
    "mean_noon_52.5": "Equinox before 12:00 Iran Standard Time (mean noon at 52.5 E)",
    "true_noon_tehran": "Equinox before true solar noon in Tehran (51.39 E)",
}
DEFAULT_RULE = "true_noon_52.5"
CIVIL_MONTHS = [("Farvardin", "فروردین"), ("Ordibehesht", "اردیبهشت"), ("Khordad", "خرداد"), ("Tir", "تیر"),
                ("Mordad", "مرداد"), ("Shahrivar", "شهریور"), ("Mehr", "مهر"), ("Aban", "آبان"),
                ("Azar", "آذر"), ("Dey", "دی"), ("Bahman", "بهمن"), ("Esfand", "اسفند")]


def _apparent_noon_utc(d: date, lon: float, lat: float = 35.7) -> datetime:
    from skyfield import almanac
    ts, eph, earth, sun, moon = se.bodies()
    topos = se._observer(lat, lon)
    start = datetime(d.year, d.month, d.day, tzinfo=IRST).astimezone(timezone.utc)
    t, y = almanac.find_discrete(ts.from_datetime(start), ts.from_datetime(start + timedelta(days=1)),
                                 almanac.meridian_transits(eph, sun, topos))
    return [ti.utc_datetime() for ti, yi in zip(t, y) if yi == 1][0]


def build_seasons(start: date = date(1850, 1, 1), end: date = date(2150, 1, 10)) -> None:
    rows = []
    for t, k in se.seasons(start, end):
        row = {"utc": t.isoformat(), "kind": k, "name": se.SEASON_NAMES[k]}
        if k == 0:
            d = t.astimezone(IRST).date()
            n525, nteh = _apparent_noon_utc(d, 52.5), _apparent_noon_utc(d, 51.389)
            nmean = datetime(d.year, d.month, d.day, 12, tzinfo=IRST).astimezone(timezone.utc)
            row.update({"irst_date": d.isoformat(), "true_noon_52.5_utc": n525.isoformat(),
                        "true_noon_tehran_utc": nteh.isoformat(), "mean_noon_52.5_utc": nmean.isoformat()})
            for rule, noon in (("true_noon_52.5", n525), ("mean_noon_52.5", nmean), ("true_noon_tehran", nteh)):
                row[f"nowruz_{rule}"] = (d if t < noon else d + timedelta(days=1)).isoformat()
        rows.append(row)
    os.makedirs(os.path.dirname(SEASONS_REBUILT), exist_ok=True)
    pd.DataFrame(rows).to_csv(SEASONS_REBUILT, index=False)


@lru_cache(maxsize=1)
def season_table() -> pd.DataFrame:
    path = SEASONS_FILE if os.path.exists(SEASONS_FILE) else SEASONS_REBUILT
    if not os.path.exists(path):
        build_seasons()
    df = pd.read_csv(path)
    df["utc"] = pd.to_datetime(df["utc"], utc=True, format="ISO8601")
    return df


@lru_cache(maxsize=3)
def nowruz_dates(rule: str = DEFAULT_RULE) -> dict:
    """Gregorian year -> civil date of Iran's Nowruz (1 Farvardin)."""
    if rule not in RULES:
        raise ValueError(f"rule must be one of {list(RULES)}")
    df = season_table()
    out = {}
    for _, r in df[df["kind"] == 0].iterrows():
        d = date.fromisoformat(r[f"nowruz_{rule}"])
        out[d.year] = d
    return out


# The ephemeris (1849-12-26 .. 2150-01-22) contains no March equinox for 1849 or 2150. To close the
# Bastani years that start in March 1849 and March 2149, these two Nowruz dates are taken from the
# arithmetic Persian calendar (persiantools 6.2 and jdatetime agree: 1 Farvardin 1228 = 21 Mar 1849,
# 1 Farvardin 1529 = 21 Mar 2150). They are flagged by nowruz_source().
EDGE_NOWRUZ = {1849: date(1849, 3, 21), 2150: date(2150, 3, 21)}


def nowruz(gyear: int, rule: str = DEFAULT_RULE) -> date:
    try:
        return nowruz_dates(rule)[gyear]
    except KeyError:
        if gyear in EDGE_NOWRUZ:
            return EDGE_NOWRUZ[gyear]
        raise ValueError(f"Nowruz {gyear} is outside the ephemeris table (1849-2150)") from None


def nowruz_source(gyear: int, rule: str = DEFAULT_RULE) -> str:
    return "jpl" if gyear in nowruz_dates(rule) else ("arithmetic" if gyear in EDGE_NOWRUZ else "none")


def march_equinox_utc(gyear: int) -> datetime:
    df = season_table()
    sel = df[(df["kind"] == 0) & (df["utc"].dt.year == gyear)]
    if sel.empty:
        raise ValueError(f"no March equinox for {gyear} in the table")
    return sel["utc"].iloc[0].to_pydatetime()


def to_civil(d: date, rule: str = DEFAULT_RULE) -> tuple[int, int, int]:
    """Gregorian date -> Iranian civil (solar Hijri) (year, month, day)."""
    nz = nowruz(d.year, rule)
    if d < nz:
        nz = nowruz(d.year - 1, rule)
    n = (d - nz).days
    sh = nz.year - 621
    m = n // 31 + 1 if n < 186 else 7 + (n - 186) // 30
    day = n - 31 * (m - 1) + 1 if m <= 6 else n - 186 - 30 * (m - 7) + 1
    if m > 12:  # Esfand 30
        m, day = 12, n - 336 + 1
    return sh, m, day


def from_civil(sh_year: int, month: int, day: int, rule: str = DEFAULT_RULE) -> date:
    nz = nowruz(sh_year + 621, rule)
    off = 31 * (month - 1) if month <= 7 else 186 + 30 * (month - 7)
    return nz + timedelta(days=off + day - 1)
