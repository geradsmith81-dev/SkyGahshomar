"""
The five Zoroastrian calendars of Sky Gahshomar behind one API.

All arithmetic is done on Julian Day Numbers (JDN, integer days; JDN 2451545 = 1 Jan 2000).
Every calendar has twelve months (mah) of 30 days named after yazatas, each day (roj) named after
one of 30 yazatas, plus the five Gatha (epagomenal) days; the calendars differ in where the year
begins, whether a leap day exists, and (Sasanian) where the Gatha days stand.

  shahanshahi  Parsi 'imperial' calendar. 365 days, never a leap day. Yazdegerdi era (YZ).
               1 Fravardin YZ 1395 = 15 Aug 2025; YZ 1396 = 15 Aug 2026 (Maharashtra Government
               Gazette holiday list 2026, GAD notification of 5 Dec 2025, as reproduced by MMRDA).
  kadmi        Qadimi calendar (Surat 1745; Yazd). Same structure, one month (30 days) ahead of
               Shahanshahi: Navroz 16 Jul 2025 (RE:Online). It is the unbroken 365-day count from
               1 Fravardin YZ 1 = 16 June 632 (Julian) = JDN 1952063, the accession of Yazdegerd III;
               the Shahanshahi count is the same plus one intercalated month (Heritage Institute:
               'missed adjustment ... in the 1120s').
  fasli        Seasonal calendar of the Zarthosti Fasili Sal Mandal (Bombay, 1906): 1 Fravardin =
               21 March; in years whose following February has 29 days a sixth Gatha day,
               Avardad-sal-gah, falls on 20 March. Eras: YZ (changes on 21 March: 2026 -> 1396) and
               ZRE (Zarathushtrian Religious Era, from the equinox of 1737 BCE: ZRE = Gregorian + 1738;
               3751 ZRE began 21 Mar 2013, Heritage Institute).
  bastani      Iranian Zoroastrian 'Bastani' calendar (introduced by Kay Khosrow Shahrokh, adopted in
               Tehran 1939): Fasli structure (12 x 30 days + 5 Gatha days + leap day) but the year
               begins on Iran's official Nowruz (iran_solar: March equinox before true noon at
               52.5 E). Eras: ZRE (primary), YZ, and the civil SH year.
  sasanian     RECONSTRUCTION, a comparison ideal - not a claim about anyone's practice. The 365-day
               Yazdegerdi count (same days as Kadmi) with the five Gatha days (andargāh) placed after
               the 8th month, Avan, as al-Biruni reports for the late Sasanian and early Islamic
               period (Āthār; Qānūn; Encyclopaedia Iranica 'Calendars i' and 'Kabisa'; de Blois,
               'The Persian calendar', Iran 34, 1996). Options:
                 andargah='after_avan' (default) | 'after_aspandarmad' (position after the reform
                   of 375 YZ = 1006 CE);
                 intercalation='none' (default) | 'kabisa_120' (Biruni's model of one month every 120
                   years, continued hypothetically: in YZ 120k the month after the Gatha days is
                   repeated and the Gatha days move to the end of the repeat; kabisa_phase shifts
                   the cycle). EIr 'Kabisa' doubts that this ever operated regularly.

ZDate.mah is 1..12 for months and 13 for the Gatha days (also for the Sasanian andargāh, which
stands after Avan); ZDate.day is 1..30, or 1..6 in the Gatha period (6 = Avardad-sal-gah).

The Zoroastrian day begins at sunrise: to_zdate() takes the civil date whose daylight the roj
covers; zdate_at(datetime, place, cal) applies the sunrise rule to a moment in time.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from functools import lru_cache

import znames as zn

CALENDARS = ["shahanshahi", "kadmi", "fasli", "bastani", "sasanian"]
GATHA_MAH = 13
YZ_EPOCH_JDN = 1952063          # 16 June 632 Julian = 1 Fravardin YZ 1 (Kadmi / pure count)
SHAHANSHAHI_OFFSET = 30         # Shahanshahi dates lie 30 days after the Kadmi dates of the same name
ZRE_OFFSET = 1738               # ZRE year = Gregorian year of its 21 March / Nowruz + 1738
YZ_FASLI_OFFSET = 630           # Fasli/Bastani YZ year = Gregorian year of its Nowruz - 630
SH_OFFSET = 621                 # Iranian civil year = Gregorian year of its Nowruz - 621
DEFAULTS = {"sasanian": {"andargah": "after_avan", "intercalation": "none", "kabisa_phase": 0},
            "bastani": {"rule": "true_noon_52.5"}}


def jdn(d: date) -> int:
    return d.toordinal() + 1721425


def from_jdn(n: int) -> date:
    return date.fromordinal(n - 1721425)


def julian_to_jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    y2, m2 = y + 4800 - a, m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - 32083


@dataclass(frozen=True)
class ZDate:
    cal: str
    year: int                       # primary era year (YZ; ZRE for Bastani)
    mah: int                        # 1..12, 13 = Gatha days
    day: int                        # 1..30 or 1..6
    roj_key: str                    # roj key, or Gatha-day key in the Gatha period
    mah_key: str | None             # None in the Gatha period
    gregorian: date
    eras: dict = field(default_factory=dict, compare=False)
    day_of_year: int = 0            # 1-based position in the year
    repeated_month: bool = False    # Sasanian kabisa model: the second (intercalated) copy of a month

    @property
    def is_gatha(self) -> bool:
        return self.mah == GATHA_MAH

    @property
    def jdn(self) -> int:
        return jdn(self.gregorian)

    def roj_names(self) -> dict:
        return (zn.GATHA if self.is_gatha else zn.ROJ)[self.roj_key]

    def mah_names(self) -> dict | None:
        return zn.MAH[self.mah_key] if self.mah_key else None

    def label(self, sep: str = " · ") -> str:
        """e.g. 'Hormazd roj, Fravardin mah, YZ 1396' (English)."""
        era = "ZRE" if self.cal == "bastani" else "YZ"
        if self.is_gatha:
            return f"{zn.GATHA[self.roj_key]['en']} Gatha, YZ {self.eras.get('YZ', self.year)}" if era == "YZ" \
                else f"{zn.GATHA[self.roj_key]['en']} Gatha, ZRE {self.year}"
        rep = " (repeated)" if self.repeated_month else ""
        return f"{zn.ROJ[self.roj_key]['en']} roj, {zn.MAH[self.mah_key]['en']}{rep} mah, {era} {self.year}"


# ----------------------------------------------------------------------------------------------
# year layouts: list of (mah, n_days, repeated_flag)
# ----------------------------------------------------------------------------------------------
_STD = tuple((m, 30, False) for m in range(1, 13))


def _std_layout(n_gatha: int):
    return _STD + ((GATHA_MAH, n_gatha, False),)


def _opts(cal: str, opts: dict) -> dict:
    o = dict(DEFAULTS.get(cal, {}))
    o.update({k: v for k, v in opts.items() if v is not None})
    if cal == "sasanian":
        if o["andargah"] not in ("after_avan", "after_aspandarmad"):
            raise ValueError("andargah must be 'after_avan' or 'after_aspandarmad'")
        if o["intercalation"] not in ("none", "kabisa_120"):
            raise ValueError("intercalation must be 'none' or 'kabisa_120'")
    return o


# --- Sasanian kabisa model -------------------------------------------------------------------
def _kabisa_years_before(y: int, phase: int) -> int:
    """Number of kabisa years among YZ 1 .. y-1 (kabisa years: YZ = 120k + phase, k >= 1)."""
    return max(0, (y - 1 - phase) // 120) if y - 1 - phase >= 120 else 0


def _is_kabisa(y: int, phase: int) -> bool:
    return y - phase >= 120 and (y - phase) % 120 == 0


def _sasanian_layout(y: int, o: dict):
    if o["intercalation"] == "none":
        pos = 8 if o["andargah"] == "after_avan" else 12
        months = [(m, 30, False) for m in range(1, 13)]
        months.insert(pos, (GATHA_MAH, 5, False))
        return tuple(months)
    phase = int(o.get("kabisa_phase", 0))
    k = _kabisa_years_before(y, phase)
    start_pos = 8 if o["andargah"] == "after_avan" else 12
    pos = (start_pos - 1 + k) % 12 + 1          # month after which the Gatha days stand this year
    months = [(m, 30, False) for m in range(1, 13)]
    if _is_kabisa(y, phase):
        rep = pos % 12 + 1                      # month repeated; Gatha days follow the repeat
        i = rep                                 # index after month `rep`
        months.insert(i, (rep, 30, True))
        months.insert(i + 1, (GATHA_MAH, 5, False))
    else:
        months.insert(pos, (GATHA_MAH, 5, False))
    return tuple(months)


# ----------------------------------------------------------------------------------------------
# year starts
# ----------------------------------------------------------------------------------------------
def year_start_jdn(year: int, cal: str, **opts) -> int:
    """JDN of 1 Fravardin of `year` (YZ for shahanshahi/kadmi/sasanian/fasli; ZRE for bastani)."""
    o = _opts(cal, opts)
    if cal == "kadmi":
        return YZ_EPOCH_JDN + 365 * (year - 1)
    if cal == "shahanshahi":
        return YZ_EPOCH_JDN + SHAHANSHAHI_OFFSET + 365 * (year - 1)
    if cal == "sasanian":
        extra = 30 * _kabisa_years_before(year, int(o.get("kabisa_phase", 0))) if o["intercalation"] == "kabisa_120" else 0
        return YZ_EPOCH_JDN + 365 * (year - 1) + extra
    if cal == "fasli":
        return jdn(date(year + YZ_FASLI_OFFSET, 3, 21))
    if cal == "bastani":
        import iran_solar
        return jdn(iran_solar.nowruz(year - ZRE_OFFSET, o["rule"]))
    raise ValueError(f"unknown calendar {cal!r}; use one of {CALENDARS}")


def year_layout(year: int, cal: str, **opts):
    o = _opts(cal, opts)
    if cal in ("shahanshahi", "kadmi"):
        return _std_layout(5)
    if cal == "sasanian":
        return _sasanian_layout(year, o)
    n = year_start_jdn(year + 1, cal, **opts) - year_start_jdn(year, cal, **opts)
    if n not in (365, 366):
        raise RuntimeError(f"{cal} year {year} has {n} days")
    return _std_layout(n - 360)


def year_length(year: int, cal: str, **opts) -> int:
    return sum(n for _, n, _ in year_layout(year, cal, **opts))


def is_leap(year: int, cal: str, **opts) -> bool:
    return year_length(year, cal, **opts) > 365


def _year_of_jdn(n: int, cal: str, **opts) -> int:
    o = _opts(cal, opts)
    if cal == "kadmi":
        return (n - YZ_EPOCH_JDN) // 365 + 1
    if cal == "shahanshahi":
        return (n - YZ_EPOCH_JDN - SHAHANSHAHI_OFFSET) // 365 + 1
    if cal == "sasanian":
        y = (n - YZ_EPOCH_JDN) // 365 + 1
        if o["intercalation"] == "kabisa_120":
            while year_start_jdn(y, cal, **opts) > n:
                y -= 1
            while year_start_jdn(y + 1, cal, **opts) <= n:
                y += 1
        return y
    d = from_jdn(n)
    off = YZ_FASLI_OFFSET if cal == "fasli" else -ZRE_OFFSET
    y = d.year - off
    if year_start_jdn(y, cal, **opts) > n:
        y -= 1
    return y


def _eras(cal: str, year: int, start: date) -> dict:
    if cal in ("shahanshahi", "kadmi", "sasanian"):
        return {"YZ": year}
    if cal == "fasli":
        return {"YZ": year, "ZRE": start.year + ZRE_OFFSET}
    return {"ZRE": year, "YZ": start.year - YZ_FASLI_OFFSET, "SH": start.year - SH_OFFSET}


# ----------------------------------------------------------------------------------------------
# conversions
# ----------------------------------------------------------------------------------------------
def to_zdate(d: date, cal: str, **opts) -> ZDate:
    """Civil (Gregorian) date -> ZDate. The roj is the one whose daylight falls on date d."""
    n = jdn(d)
    y = _year_of_jdn(n, cal, **opts)
    start = year_start_jdn(y, cal, **opts)
    off = n - start
    pos = off
    for mah, nd, rep in year_layout(y, cal, **opts):
        if pos < nd:
            day = pos + 1
            if mah == GATHA_MAH:
                rk, mk = zn.GATHA_KEYS[day - 1], None
            else:
                rk, mk = zn.ROJ_KEYS[day - 1], zn.MAH_KEYS[mah - 1]
            return ZDate(cal, y, mah, day, rk, mk, d, _eras(cal, y, from_jdn(start)), off + 1, rep)
        pos -= nd
    raise RuntimeError("date not placed in year layout")  # pragma: no cover


def from_zdate(year: int, mah: int, day: int, cal: str, repeated: bool = False, **opts) -> date:
    """(year, mah 1..12 or 13 for Gatha, day) -> civil date. For the Sasanian kabisa model pass
    repeated=True for the intercalated copy of a month."""
    off = 0
    for m, nd, rep in year_layout(year, cal, **opts):
        if m == mah and rep == repeated:
            if not 1 <= day <= nd:
                raise ValueError(f"day {day} out of range 1..{nd} for mah {mah} of {cal} {year}")
            return from_jdn(year_start_jdn(year, cal, **opts) + off + day - 1)
        off += nd
    raise ValueError(f"mah {mah} (repeated={repeated}) does not occur in {cal} year {year}")


def navroz(year: int, cal: str, **opts) -> date:
    return from_jdn(year_start_jdn(year, cal, **opts))


def year_containing(d: date, cal: str, **opts) -> int:
    return _year_of_jdn(jdn(d), cal, **opts)


def year_days(year: int, cal: str, **opts):
    """Iterator over the ZDates of one year."""
    s = year_start_jdn(year, cal, **opts)
    for i in range(year_length(year, cal, **opts)):
        yield to_zdate(from_jdn(s + i), cal, **opts)


def month_days(year: int, mah: int, cal: str, repeated: bool = False, **opts) -> list:
    first = from_zdate(year, mah, 1, cal, repeated=repeated, **opts)
    n = next(nd for m, nd, rep in year_layout(year, cal, **opts) if m == mah and rep == repeated)
    return [to_zdate(first + timedelta(days=i), cal, **opts) for i in range(n)]


def months_of_year(year: int, cal: str, **opts) -> list:
    """[(mah, repeated, first civil date, n_days), ...] in calendar order."""
    s, out, off = year_start_jdn(year, cal, **opts), [], 0
    for m, nd, rep in year_layout(year, cal, **opts):
        out.append((m, rep, from_jdn(s + off), nd))
        off += nd
    return out


def gregorian_range(start: date, end: date, cal: str, **opts):
    """Iterator over ZDates for every civil date start..end inclusive."""
    d = start
    while d <= end:
        yield to_zdate(d, cal, **opts)
        d += timedelta(days=1)


# ----------------------------------------------------------------------------------------------
# the day begins at sunrise
# ----------------------------------------------------------------------------------------------
def roj_civil_date(when: datetime, place: dict) -> date:
    """Civil date whose roj is in force at the tz-aware moment `when` at `place`: the roj begins at
    sunrise, so before local sunrise the previous date's roj still runs (Ushahin Gah belongs to
    the previous day). In polar night/day the civil date's 06:00 local mean solar time is used."""
    import sky_engine as se
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(place["tz"])
    local = when.astimezone(tz)
    sd = se.solar_day(place, local.date())
    start = sd["sunrise"]
    if start is None:   # polar: use local mean 06:00 (noon - 6 h)
        start = sd["noon"] - timedelta(hours=6)
    return local.date() if local >= start else local.date() - timedelta(days=1)


def zdate_at(when: datetime, place: dict, cal: str, **opts) -> ZDate:
    """ZDate in force at a tz-aware moment and place (day begins at sunrise)."""
    return to_zdate(roj_civil_date(when, place), cal, **opts)


def all_calendars(d: date, **opts_by_cal) -> dict:
    """{cal: ZDate} for one civil date; opts_by_cal = {'sasanian': {...}, 'bastani': {...}}."""
    return {c: to_zdate(d, c, **opts_by_cal.get(c, {})) for c in CALENDARS}
