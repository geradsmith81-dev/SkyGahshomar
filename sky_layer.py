"""
The sky layer of Sky Gahshomar: the five Gahs, the Rapithwin season, Moon phases for the Mah
Niyayesh, and the bearings of the Sun and the Moon for a 'face the light' compass.

Gahs (watches of the Zoroastrian day, which begins at sunrise), from JPL sunrise, true noon,
sunset and solar midnight at the chosen place:
  Havan         sunrise -> true noon
  Rapithwin     true noon -> true noon + 3 h      (in the Rapithwin season)
  Second Havan  the same interval outside the Rapithwin season
  Uziran        true noon + 3 h -> sunset
  Aiwisruthrem  sunset -> solar midnight
  Ushahin       solar midnight -> next sunrise (still part of the same roj)
Parsi prayer guides give the Bombay times as Havan from sunrise to about 12:40 and Rapithwin
12:40-3:40 pm (Bhadha, 'Time for reciting prayers in each Geh'; 'A guide to our prayers',
zoroastrians.net); 12:40 is Bombay's true noon, so the clock times are true noon and noon + 3 h.
If sunset comes less than 3 h after noon (high latitudes in winter), the Rapithwin/Second-Havan
watch ends half-way between noon and sunset. Polar day/night: sunrise/sunset are replaced by
true noon -/+ 6 h and flagged.
Optional havan_meher=True starts Havan 36 minutes before sunrise ('Havan-ni-Meher', Bhadha).

Rapithwin practice (app assembly, Nov 2026; preset key 'rapithwin' of sects.py):
  rapithwin='summer'         (default) Rapithwin in Fravardin..Meher mah, Second Havan otherwise, as above.
  rapithwin='medieval_four'  the Bundahishn's winter rule (gahs.RAPITHWIN; Wikipedia 'Zoroastrian
                             calendar'): outside the Rapithwin season there are only four watches, the
                             morning Havan running on until Uziran (no Second Havan). The summer months are
                             unchanged. sects.py uses it only for the Sasanian reconstruction.

Rapithwin season: Rapithwin Gah is recited from Hormazd roj of Fravardin mah to Aneran roj of Meher
mah (seven months); from Hormazd roj of Avan mah to the Vahishtoisht Gatha the Second Havan is
recited instead (Khordeh Avesta, Kanga tr.: 'from Roz Hormazd Month Awan up to Gatha Vahishtoisht
Rapithwan Gah is not recited, but in its stead there is Second Havan'). The rule is applied to the
date in the user's own calendar, as Shahanshahi and Kadmi users do: their Rapithwin season starts
with their own Navroz (August/July), not at the spring equinox. The Fasli/Bastani leap day and the
Sasanian andargāh days (after Avan) fall in the Second-Havan half.

Mah Niyayesh (litany to the Moon) names the Moon's three stations: antarə.måŋha (new moon),
pərənō.måŋha (full moon) and vīšaptaθa (the intermediate, half-moon station). moon_phases()
returns all four principal phases from JPL; new and full moons are flagged as the Mah Niyayesh days.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

import sky_engine as se
import zcalendars as zc
import znames as zn

RAPITHWIN_HOURS = 3.0


def rapithwin_season(z: "zc.ZDate") -> bool:
    """True if Rapithwin Gah is recited on this roj (Fravardin..Meher mah), False for Second Havan."""
    return (not z.is_gatha) and 1 <= z.mah <= 7


@dataclass
class Gah:
    key: str
    start: datetime
    end: datetime
    note: str = ""

    def names(self) -> dict:
        return zn.GAH[self.key]


RAPITHWIN_PRACTICES = ("summer", "medieval_four")


def gahs(d: date, place: dict, cal: str = "shahanshahi", havan_meher: bool = False,
         rapithwin: str = "summer", **opts) -> dict:
    """The five Gahs of the roj that begins at sunrise on civil date d.
    Returns {'zdate': ZDate, 'rapithwin_season': bool, 'gahs': [Gah, ...], 'polar': None|'day'|'night',
             'sun': solar_day dict}."""
    z = zc.to_zdate(d, cal, **opts)
    sd = se.solar_day(place, d)
    noon = sd["noon"]
    sunrise, sunset, midnight, nxt = sd["sunrise"], sd["sunset"], sd["midnight"], sd["next_sunrise"]
    polar = sd["polar"]
    if sunrise is None or sunset is None:
        sunrise = noon - timedelta(hours=6)
        sunset = noon + timedelta(hours=6)
        nd = se.solar_day(place, d + timedelta(days=1))
        nxt = (nd["sunrise"] or nd["noon"] - timedelta(hours=6))
        midnight = midnight or noon + timedelta(hours=12)
    r_end = noon + timedelta(hours=RAPITHWIN_HOURS)
    note = ""
    if r_end >= sunset:
        r_end = noon + (sunset - noon) / 2
        note = "shortened: sunset less than 3 h after noon"
    season = rapithwin_season(z)
    mid = "rapithwin" if season else "second_havan"
    havan_start = sunrise - timedelta(minutes=36) if havan_meher else sunrise
    if rapithwin not in RAPITHWIN_PRACTICES:
        raise ValueError(f"rapithwin must be one of {RAPITHWIN_PRACTICES}")
    hnote = "from 36 min before sunrise (Havan-ni-Meher)" if havan_meher else ""
    if rapithwin == "medieval_four" and not season:
        hnote = (hnote + "; " if hnote else "") + "runs on until Uziran (Bundahishn winter rule: four watches)"
        out = [Gah("havan", havan_start, r_end, hnote)]
    else:
        out = [Gah("havan", havan_start, noon, hnote), Gah(mid, noon, r_end, note)]
    out += [
        Gah("uziran", r_end, sunset),
        Gah("aiwisruthrem", sunset, midnight),
        Gah("ushahin", midnight, nxt, "belongs to the same roj; the next roj begins at sunrise")]
    return {"zdate": z, "rapithwin_season": season, "gahs": out, "polar": polar, "sun": sd,
            "practice": rapithwin}


def gah_at(when: datetime, place: dict, cal: str = "shahanshahi", **opts) -> tuple:
    """(Gah, ZDate) in force at the tz-aware moment `when`."""
    d = zc.roj_civil_date(when, place)
    g = gahs(d, place, cal, **opts)
    for x in g["gahs"]:
        if x.start <= when < x.end:
            return x, g["zdate"]
    return g["gahs"][-1], g["zdate"]


PHASE_NAMES = {0: "New moon", 1: "First quarter", 2: "Full moon", 3: "Last quarter"}
PHASE_AVESTAN = {0: "antarə.måŋha", 1: "vīšaptaθa", 2: "pərənō.måŋha", 3: "vīšaptaθa"}


def moon_phases(start: date, end: date, tz: str = "UTC") -> list:
    """[{'utc', 'local', 'phase' 0..3, 'name', 'avestan', 'mah_niyayesh' bool}] from JPL."""
    from zoneinfo import ZoneInfo
    z = ZoneInfo(tz)
    out = []
    for t, p in se.moon_phase_events(start, end + timedelta(days=1)):
        out.append({"utc": t, "local": t.astimezone(z), "phase": p, "name": PHASE_NAMES[p],
                    "avestan": PHASE_AVESTAN[p], "mah_niyayesh": p in (0, 2)})
    return out


POINTS_16 = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def compass_point(b: float) -> str:
    return POINTS_16[int((b % 360) / 22.5 + 0.5) % 16]


def face_the_light(when: datetime, place: dict) -> dict:
    """Sun and Moon positions and which light to face. Zoroastrians pray facing a source of light:
    the Sun by day, the Moon by night when it is up, otherwise a lamp or fire. Returns
    {'sun': {...alt, az, point}, 'moon': {...alt, az, point, illumination}, 'face': 'sun'|'moon'|'lamp',
     'bearing': azimuth or None}. Altitudes include refraction; 'up' means the upper limb is above
    the sea-level horizon (-0.83 deg for the Sun, -0.3 deg roughly for the Moon's centre)."""
    utc = when.astimezone(timezone.utc)
    p = se.sun_moon_position(place["lat"], place["lon"], utc, place.get("elev", 0.0) or 0.0)
    for k in ("sun", "moon"):
        p[k]["point"] = compass_point(p[k]["az"])
    sun_up = p["sun"]["alt"] > -0.8333
    moon_up = p["moon"]["alt"] > -0.3
    face = "sun" if sun_up else ("moon" if moon_up else "lamp")
    p["face"] = face
    p["bearing"] = p[face]["az"] if face != "lamp" else None
    return p
