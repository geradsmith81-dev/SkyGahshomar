"""
Festivals and holy days for each calendar of Sky Gahshomar.

festivals_in_year(year, cal, **opts)  -> list[Festival] for one Zoroastrian year of that calendar
festivals_between(start, end, cal, **opts) -> list[Festival] whose first day falls in [start, end]

Rules (month/day positions are applied inside each calendar, so a Shahanshahi Khordad Sal falls in
August and a Fasli one on 26 March):
* Name-day jashans (parab): the roj whose name equals the mah name - Fravardin 19, Ardibehesht 3,
  Khordad 6, Tir 13, Amardad 7, Shehrevar 4, Meher 16, Avan 10, Adar 9, Bahman 2, Aspandarmad 5
  (Spendarmad roj); Dae mah has four Dae jashans: Hormazd 1, Dae-pa-Adar 8, Dae-pa-Meher 15,
  Dae-pa-Din 23 (returned as four 'jashan_dae' entries).
* The six Gahambars, five days each (Encyclopaedia Iranica 'Gāhānbār'; Heritage Institute grid):
  Maidyozarem Ardibehesht 11-15, Maidyoshahem Tir 11-15, Paitishahem Shehrevar 26-30,
  Ayathrem Meher 26-30, Maidyarem Dae 16-20, Hamaspathmaedem the five Gatha days.
  (Fasli/Bastani leap years: the Avardad-sal-gah is not counted in the Gahambar.)
* Muktad / Farvardegan days: Ashtad roj of Aspandarmad mah to the last day of the year (10 days;
  11 in a Fasli/Bastani leap year). muktad='parsi_18' gives the old Parsi 18-day custom, from
  Ashishvangh roj of Aspandarmad to Amardad roj of Fravardin (Karanjia; avesta.org 'Making Muktad
  More Meaningful': 18 days since at least the 15th century, reduced to 10 in the 1970s).
* Farvardigan: Fravardin roj of Fravardin mah (same day as jashan_fravardin).
* Navroz: 1 Fravardin. Pateti: the last day of the year (the day before Navroz).
* Jamshedi Navroz: 21 March for Parsis of every calendar (Fasli New Year; Parsi Khabar 2024:
  '21st March is Roj Hormuzd of Mah Fravardin'); for Bastani it is Iran's Nowruz.
  jamshedi='equinox_ist' instead gives the civil date of the March equinox in India Standard Time
  (some Indian sources, e.g. greetings on 20 March 2025, use the equinox day).
* Khordad Sal: Khordad roj of Fravardin mah. Zarthost no Diso: Khorshed roj of Dae mah.
* Rapithwin Jashan (extra key): Ardibehesht roj of Fravardin mah, the consecration of Rapithwin.
* Sadeh: sadeh='iran' (default) 10 Bahman of the Iranian civil calendar (Jan 29-31; the date now
  observed in Iran, Heritage Institute grid 'Sadeh-Iran'); 'kerman' Aban roj of Bahman mah;
  'yazd' Ashtad roj of Adar mah (farsinet / Heritage Institute grid). Not a Parsi observance.
* Chaharshanbe Suri: the evening (Tuesday) before the last Wednesday before Iran's Nowruz.
* Tirgan (civil, extra key 'tirgan_civil'): 13 Tir of the Iranian civil calendar; the Zoroastrian
  Tir jashan (Tir roj of Tir mah) falls on civil 10 Tir in the Bastani calendar. Mehergan in the
  Bastani calendar coincides with civil 10 Mehr, the date of Iran's official calendar.
* Sasanian reconstruction: Hamaspathmaedem = the andargāh days after Avan, and the Muktad = the last
  five days of the month before them + andargāh (al-Biruni's Farwardajan). de Blois' hypothesis
  that a c. 500 CE reform moved Nowruz to 1 Adar is documented, not modelled.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

import znames as zn
import zcalendars as zc

GATHA = zc.GATHA_MAH


@dataclass
class Festival:
    key: str
    start: date
    days: int
    cal: str
    zstart: "zc.ZDate"
    note: str = ""
    names: dict = field(default_factory=dict)

    @property
    def end(self) -> date:
        return self.start + timedelta(days=self.days - 1)

    def label(self) -> str:
        if self.key not in zn.FESTIVAL:          # extra jashan days (jashans.py)
            return self.names.get("en", self.key)
        return zn.display(zn.FESTIVAL, self.key)


def _f(key, start, days, cal, note="", **opts):
    return Festival(key, start, days, cal, zc.to_zdate(start, cal, **opts), note, zn.FESTIVAL[key])


def _d(year, mah, day, cal, **opts):
    return zc.from_zdate(year, mah, day, cal, **opts)


def _gatha_start(year, cal, **opts):
    return _d(year, GATHA, 1, cal, **opts)


def _cal_opts(opts):
    return {k: v for k, v in opts.items() if k in ("andargah", "intercalation", "kabisa_phase", "rule")}


def festivals_in_year(year: int, cal: str, muktad: str = "ten", jamshedi: str = "fixed_21_march",
                      sadeh: str = "iran", jashan_days: bool = True, **opts) -> list:
    """All festivals of one Zoroastrian year (year = YZ, or ZRE for Bastani), sorted by date."""
    o = _cal_opts(opts)
    M = zn.MAH_NUMBER
    R = zn.ROJ_NUMBER
    out = []
    n_year = zc.year_length(year, cal, **o)
    nz = zc.navroz(year, cal, **o)
    last = nz + timedelta(days=n_year - 1)
    leap = cal in ("fasli", "bastani") and n_year == 366

    out.append(_f("navroz", nz, 1, cal, "1 Fravardin, Hormazd roj", **o))
    out.append(_f("pateti", last, 1, cal,
                  "last day of the year" + (" (Avardad-sal-gah in this leap year)" if leap else ""), **o))
    out.append(_f("khordad_sal", _d(year, 1, R["khordad"], cal, **o), 1, cal, "Khordad roj, Fravardin mah", **o))
    out.append(_f("rapithwin_jashan", _d(year, 1, R["ardibehesht"], cal, **o), 1, cal,
                  "Ardibehesht roj, Fravardin mah: consecration of Rapithwin", **o))
    out.append(_f("farvardigan", _d(year, 1, R["fravardin"], cal, **o), 1, cal, "Fravardin roj, Fravardin mah", **o))
    out.append(_f("zarthost_no_diso", _d(year, M["dae"], R["khorshed"], cal, **o), 1, cal, "Khorshed roj, Dae mah", **o))

    # name-day jashans
    for mk, rk in zn.JASHAN_ROJ_FOR_MAH.items():
        if mk == "dae":
            for r in ("hormazd", "dae_pa_adar", "dae_pa_meher", "dae_pa_din"):
                out.append(_f("jashan_dae", _d(year, M["dae"], R[r], cal, **o), 1, cal,
                              f"{zn.ROJ[r]['en']} roj, Dae mah", **o))
            continue
        out.append(_f(f"jashan_{mk}", _d(year, M[mk], R[rk], cal, **o), 1, cal,
                      f"{zn.ROJ[rk]['en']} roj, {zn.MAH[mk]['en']} mah", **o))

    # gahambars
    for key, mk, d0 in (("gahambar_maidyozarem", "ardibehesht", 11), ("gahambar_maidyoshahem", "tir", 11),
                        ("gahambar_paitishahem", "shehrevar", 26), ("gahambar_ayathrem", "meher", 26),
                        ("gahambar_maidyarem", "dae", 16)):
        out.append(_f(key, _d(year, M[mk], d0, cal, **o), 5, cal,
                      f"{zn.ROJ_KEYS[d0 - 1].replace('_', '-').title()} to {zn.ROJ_KEYS[d0 + 3].replace('_', '-').title()} roj, "
                      f"{zn.MAH[mk]['en']} mah", **o))
    g1 = _gatha_start(year, cal, **o)
    out.append(_f("gahambar_hamaspathmaedem", g1, 5, cal, "the five Gatha days"
                  + (" (after Avan in the Sasanian reconstruction)" if cal == "sasanian" and o.get("andargah", "after_avan") == "after_avan" else ""), **o))

    # muktad
    if cal == "sasanian":
        # month that precedes the andargah in this year's layout
        lay = zc.year_layout(year, cal, **o)
        i = [k for k, (m, _, _) in enumerate(lay) if m == GATHA][0]
        pm, _, prep = lay[i - 1]
        s = zc.from_zdate(year, pm, 26, cal, repeated=prep, **o)
        out.append(_f("muktad", s, 10, cal, "Ashtad to Aneran roj of the month before the andargāh + the five "
                      "andargāh days (al-Biruni's Farwardajan)", **o))
    else:
        s = _d(year, M["aspandarmad"], R["ashtad"], cal, **o)
        if muktad == "parsi_18":
            s = s - timedelta(days=1)
            end = zc.from_zdate(year + 1, 1, R["amardad"], cal, **o)
            out.append(_f("muktad", s, (end - s).days + 1, cal,
                          "Parsi 18-day custom: Ashishvangh roj of Aspandarmad to Amardad roj of Fravardin", **o))
        else:
            out.append(_f("muktad", s, (last - s).days + 1, cal,
                          "Ashtad roj of Aspandarmad to the last Gatha day" + (" incl. Avardad-sal-gah" if leap else ""), **o))

    # Jamshedi Navroz in the civil year of this calendar year's spring
    out.extend(_jamshedi_for_year(year, cal, jamshedi, o, nz, last))
    out.extend(_iranian_civil(year, cal, sadeh, o, nz, last))
    if jashan_days:
        import jashans      # extra jashan days: Atash Behram salgirehs, Pir pilgrimages, Yalda ...
        out.extend(f for f in jashans.extras_between(nz, last, cal, **o) if nz <= f.start <= last)
    return sorted(out, key=lambda f: (f.start, f.key))


def _jamshedi_date(gyear: int, cal: str, mode: str, o: dict) -> date:
    if cal == "bastani":
        import iran_solar
        return iran_solar.nowruz(gyear, o.get("rule", iran_solar.DEFAULT_RULE))
    if mode == "equinox_ist":
        import iran_solar
        from datetime import timezone
        ist = timezone(timedelta(hours=5, minutes=30))
        return iran_solar.march_equinox_utc(gyear).astimezone(ist).date()
    return date(gyear, 3, 21)


def _jamshedi_for_year(year, cal, mode, o, nz, last):
    out = []
    for gy in range(nz.year, last.year + 1):
        try:
            d = _jamshedi_date(gy, cal, mode, o)
        except ValueError:
            continue
        if nz <= d <= last:
            note = ("21 March, kept by Parsis of every calendar" if mode != "equinox_ist" else
                    "day of the March equinox in India Standard Time") if cal != "bastani" else "Iran's Nowruz"
            out.append(_f("jamshedi_navroz", d, 1, cal, note, **o))
    return out


def _iranian_civil(year, cal, sadeh_mode, o, nz, last):
    import iran_solar
    rule = o.get("rule", iran_solar.DEFAULT_RULE)
    out = []
    M, R = zn.MAH_NUMBER, zn.ROJ_NUMBER
    parsi = cal in ("shahanshahi", "kadmi")
    tag = " Iranian observance, not a Parsi one." if parsi else ""
    # Sadeh
    if sadeh_mode == "kerman":
        out.append(_f("sadeh", _d(year, M["bahman"], R["avan"], cal, **o), 1, cal,
                      "Aban roj, Bahman mah (Kerman tradition)." + tag, **o))
    elif sadeh_mode == "yazd":
        out.append(_f("sadeh", _d(year, M["adar"], R["ashtad"], cal, **o), 1, cal,
                      "Ashtad roj, Adar mah (Yazd tradition)." + tag, **o))
    for gy in range(nz.year, last.year + 1):
        try:
            if sadeh_mode == "iran":
                d = iran_solar.from_civil(gy - 622, 11, 10, rule)   # Bahman of SH year begun in gy-1
                if nz <= d <= last:
                    out.append(_f("sadeh", d, 1, cal, "10 Bahman of the Iranian civil calendar (evening bonfire)." + tag, **o))
            # Chaharshanbe Suri before Nowruz of civil year starting in gy
            n = iran_solar.nowruz(gy, rule)
            wed = n - timedelta(days=1)
            while wed.weekday() != 2:
                wed -= timedelta(days=1)
            cs = wed - timedelta(days=1)
            if nz <= cs <= last:
                out.append(_f("chaharshanbe_suri", cs, 1, cal,
                              "Tuesday evening before the last Wednesday of the Iranian year." + tag, **o))
            tc = iran_solar.from_civil(gy - 621, 4, 13, rule)
            if nz <= tc <= last:
                out.append(_f("tirgan_civil", tc, 1, cal, "13 Tir of the Iranian civil calendar." + tag, **o))
        except ValueError:
            continue
    return out


def festivals_between(start: date, end: date, cal: str, **kw) -> list:
    """Festivals whose first day lies in [start, end] (multi-day festivals overlapping the start
    are included too)."""
    o = _cal_opts(kw)
    y0 = zc.year_containing(start, cal, **o) - 1
    y1 = zc.year_containing(end, cal, **o)
    out = []
    for y in range(y0, y1 + 1):
        try:
            for f in festivals_in_year(y, cal, **kw):
                if f.end >= start and f.start <= end:
                    out.append(f)
        except ValueError:      # outside the Bastani table
            continue
    seen, uniq = set(), []
    for f in sorted(out, key=lambda f: (f.start, f.key)):
        k = (f.key, f.start)
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    return uniq


def festivals_on(d: date, cal: str, **kw) -> list:
    return [f for f in festivals_between(d - timedelta(days=20), d, cal, **kw) if f.start <= d <= f.end]
