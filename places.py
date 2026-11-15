"""Place search (GeoNames cities with 15,000+ people, via geonamescache) with time zones, and the preset places.

Adapted from Sky Taqwim (places.py). Preset coordinates: Mumbai, Udvada, Yazd and Tehran are the engine's own
reference places (sky_engine.MUMBAI etc., used in its validation); the others are the GeoNames entries
(geonamescache 3.0.2; GeoNames id in the comment). Persian and Gujarati names of the presets come from
names.PLACES (content track); places without an entry there are shown in English only.
"""
from __future__ import annotations

import unicodedata
from functools import lru_cache

import names as _names
import sky_engine as _se

_E = {"mumbai": _se.MUMBAI, "udvada": _se.UDVADA, "yazd": _se.YAZD, "tehran": _se.TEHRAN}
#        key            name            country  lat        lon         tz                      geonames id
_GN = [("navsari", "Navsari", "IN", 20.94237, 72.92467, "Asia/Kolkata"),            # 1261653
       ("surat", "Surat", "IN", 21.19594, 72.83023, "Asia/Kolkata"),                # 1255364
       ("karachi", "Karachi", "PK", 24.8608, 67.0104, "Asia/Karachi"),              # 1174872
       ("kerman", "Kerman", "IR", 30.28321, 57.07879, "Asia/Tehran"),               # 128234
       ("london", "London", "GB", 51.50853, -0.12574, "Europe/London"),             # 2643743
       ("toronto", "Toronto", "CA", 43.70643, -79.39864, "America/Toronto"),        # 6167865
       ("los_angeles", "Los Angeles", "US", 34.05223, -118.24368, "America/Los_Angeles"),  # 5368361
       ("sydney", "Sydney", "AU", -33.86785, 151.20732, "Australia/Sydney")]        # 2147714
_ORDER = ["mumbai", "udvada", "navsari", "surat", "karachi", "yazd", "kerman", "tehran",
          "london", "toronto", "los_angeles", "sydney"]
_CC = {"mumbai": "IN", "udvada": "IN", "yazd": "IR", "tehran": "IR"}
_SHORT = {"mumbai": "Mumbai", "udvada": "Udvada", "yazd": "Yazd", "tehran": "Tehran"}


def _preset(key: str) -> dict:
    if key in _E:
        e = _E[key]
        d = {"name": _SHORT[key], "country": _CC[key], "lat": e["lat"], "lon": e["lon"], "tz": e["tz"],
             "elev": e.get("elev", 0.0), "note": e["name"]}
    else:
        _, n, cc, la, lo, tz = next(x for x in _GN if x[0] == key)
        d = {"name": n, "country": cc, "lat": la, "lon": lo, "tz": tz, "elev": 0.0, "note": ""}
    nm = _names.PLACES.get(key, {})
    d.update(key=key, fa=nm.get("fa", ""), gu=nm.get("gu", ""))
    return d


PRESETS = [_preset(k) for k in _ORDER]
PRESETS_BY_KEY = {p["key"]: p for p in PRESETS}
DEFAULT = PRESETS_BY_KEY["mumbai"]


def preset_label(p: dict) -> str:
    """'English · Persian · Gujarati' where the names table has the place."""
    return " · ".join(x for x in (p["name"], p.get("fa", ""), p.get("gu", "")) if x)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


@lru_cache(maxsize=1)
def _cities() -> list[dict]:
    try:
        import geonamescache
    except ImportError:
        return []
    gc = geonamescache.GeonamesCache()
    countries = gc.get_countries()
    states = gc.get_us_states()
    out = []
    for c in gc.get_cities().values():
        cc = c["countrycode"]
        region = states.get(c.get("admin1code", ""), {}).get("name", "") if cc == "US" else ""
        out.append({"name": c["name"], "country": cc,
                    "country_name": countries.get(cc, {}).get("name", cc), "region": region,
                    "lat": float(c["latitude"]), "lon": float(c["longitude"]), "tz": c["timezone"],
                    "pop": int(c["population"]), "key": _norm(c["name"]),
                    "alt": "|" + "|".join(_norm(a) for a in c.get("alternatenames", []) if a) + "|"})
    out.sort(key=lambda r: -r["pop"])
    return out


def search(query: str, limit: int = 12) -> list[dict]:
    """Exact name matches first, then alternate names, then prefixes; larger cities first."""
    q = _norm(query)
    if not q:
        return []
    cities = _cities()
    exact = [c for c in cities if c["key"] == q]
    alt = [c for c in cities if c["key"] != q and f"|{q}|" in c["alt"]]
    pref = [c for c in cities if c["key"] != q and c["key"].startswith(q) and f"|{q}|" not in c["alt"]]
    seen, out = set(), []
    for c in exact + alt + pref:
        k = (c["name"], c["country"], round(c["lat"], 2))
        if k not in seen:
            seen.add(k)
            out.append(c)
        if len(out) >= limit:
            break
    return out


def label(p: dict) -> str:
    parts = [p["name"]]
    if p.get("region"):
        parts.append(p["region"])
    parts.append(p.get("country_name") or p.get("country", ""))
    return ", ".join(x for x in parts if x)
