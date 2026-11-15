"""Sky Gahshomar · گاه‌شمار آسمان — the Zoroastrian calendars (Shahanshahi, Kadmi, Fasli, Bastani, and a Sasanian
reconstruction) from NASA JPL astronomy.

Run:  streamlit run app.py --server.port 8513
"""
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import streamlit as st  # noqa: E402

st.set_page_config(page_title="Sky Gahshomar · گاه‌شمار", page_icon=os.path.join(HERE, "assets", "launcher", "icon-192.png"),
                   layout="wide", initial_sidebar_state="auto")

from zoneinfo import ZoneInfo  # noqa: E402

import device  # noqa: E402
import iran_solar as irs  # noqa: E402
import locator  # noqa: E402
import names  # noqa: E402
import pages  # noqa: E402
import places  # noqa: E402
import sects  # noqa: E402
import theme  # noqa: E402

theme.apply()

PAGES = {
    "Today": ("Today", pages.render_today),
    "Month": ("Month", pages.render_month),
    "Year": ("Year", pages.render_year),
    "Gahs": ("Gahs", pages.render_gahs),
    "Festivals": ("Festivals", pages.render_festivals),
    "Compare": ("Compare", pages.render_compare),
    "Traditions": ("Traditions", pages.render_traditions),
    "How": ("How it works", pages.render_how),
    "About": ("About", pages.render_about),
}
DEFAULT_SECT = "parsi_shahanshahi:0"


def _idx(key, options, default):
    """index= for a widget, unless a preset has already put its value in session state."""
    return {} if key in st.session_state else {"index": list(options).index(default)}


def _browser_tz():
    try:
        return st.context.timezone
    except Exception:
        return None


# ---------------------------------------------------------------------------------------------- first visit
if "cal" not in st.session_state:          # default: the Parsi Shahanshahi preset at Mumbai
    _k, _i = DEFAULT_SECT.split(":")
    pages.apply_preset(_k, int(_i))
if "place" not in st.session_state:
    st.session_state["place"] = dict(places.DEFAULT, label=places.preset_label(places.DEFAULT), src="default")
    st.session_state["place_src"] = "default"
st.session_state.setdefault("rap_auto", False)


def _on_pick():
    v = st.session_state.get("locator")
    p = v.get("pick") if hasattr(v, "get") else getattr(v, "pick", None)
    if not isinstance(p, dict) or "lat" not in p:
        return
    try:
        lat, lon = float(p["lat"]), float(p["lon"])
    except (TypeError, ValueError):
        return
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return
    if p.get("auto") and st.session_state.get("place_src") == "manual":
        return   # the user already chose a place by hand: keep it
    acc = p.get("acc") if isinstance(p.get("acc"), (int, float)) else None
    st.session_state["place"] = locator.place_from_device(lat, lon, acc, _browser_tz())
    st.session_state["place_src"] = "gps"


def _set_manual(pl: dict):
    st.session_state["place"] = dict(pl, src="manual")
    st.session_state["place_src"] = "manual"


def _cal_changed():
    """Switching to the Sasanian reconstruction selects the Bundahishn four-watch rule (and back), unless the
    user has chosen the Rapithwin practice by hand."""
    cal = st.session_state.get("cal")
    rap = st.session_state.get("rapithwin", "summer")
    if cal == "sasanian" and rap == "summer":
        st.session_state["rapithwin"] = "medieval_four"
        st.session_state["rap_auto"] = True
    elif cal != "sasanian" and st.session_state.get("rap_auto"):
        st.session_state["rapithwin"] = "summer"
        st.session_state["rap_auto"] = False
    st.session_state["sect"] = "custom"


def _custom():
    st.session_state["sect"] = "custom"
    st.session_state["rap_auto"] = False


def _sect_changed():
    v = st.session_state.get("sect")
    if v and v != "custom":
        k, i = v.split(":")
        pages.apply_preset(k, int(i))


# ---------------------------------------------------------------------------------------------- top bar
cal = st.session_state["cal"]
theme.header(calendar=cal)
phone = device.phone()
c1, c2 = (st.columns([2.6, 3.4]) if not phone else (st.container(), st.container()))
with c1:
    cal = st.radio("Calendar · " + names.TITLE["fa"], pages.CALS, key="cal", horizontal=True, format_func=pages.cal_label,
                   on_change=_cal_changed,
                   help="Every page except Compare shows only this calendar. The Sasanian calendar is a "
                        "reconstruction, shown for comparison.")
with c2:
    page = st.radio("Page", list(PAGES), key="page", horizontal=True, format_func=lambda k: PAGES[k][0],
                    label_visibility="collapsed" if not phone else "visible")

_pl = st.session_state["place"]
_how = {"gps": "from your device", "timezone": "first guess from your time zone",
        "manual": "chosen by you", "default": "starting place"}.get(st.session_state.get("place_src"), "")
locator.show(f"{_pl.get('label', _pl['name'])}  ({_how})",
             auto=st.session_state.get("place_src") == "default", on_pick=_on_pick)

# ---------------------------------------------------------------------------------------------- settings
device.switch()
panel = device.input_panel("Settings: tradition, place, festivals")
with panel:
    st.subheader("Tradition")
    opts = ["custom"] + pages.preset_options()
    if st.session_state.get("sect") not in opts:
        st.session_state["sect"] = "custom"
    st.selectbox("Community preset", opts, key="sect", on_change=_sect_changed,
                 format_func=lambda o: "Custom settings" if o == "custom" else pages.preset_label(o),
                 help="Sets the calendar, Muktad length, Rapithwin practice and era (see the Traditions page).")

    st.subheader("Your place")
    q = st.text_input("Search for a town or city", key="place_q", placeholder="e.g. Navsari, Yazd, Toronto")
    if q.strip():
        res = places.search(q)
        if res:
            pick = st.selectbox("Matches", range(len(res)), key="place_pick", format_func=lambda i: places.label(res[i]))
            if st.button("Use this place", key="place_use", width="stretch"):
                r = res[pick]
                _set_manual({"name": r["name"], "fa": "", "gu": "", "country": r["country"], "lat": r["lat"],
                             "lon": r["lon"], "tz": r["tz"], "elev": 0.0, "label": places.label(r)})
                st.rerun()
        else:
            st.caption("No town of 15,000+ people by that name. Try a nearby city, or enter coordinates below.")
    pre = st.selectbox("…or a preset", ["—"] + [p["key"] for p in places.PRESETS], key="place_preset",
                       format_func=lambda k: "—" if k == "—" else places.preset_label(places.PRESETS_BY_KEY[k]))
    if pre != "—" and st.session_state.get("_last_preset") != pre:
        st.session_state["_last_preset"] = pre
        p = dict(places.PRESETS_BY_KEY[pre])
        p["label"] = places.preset_label(p)
        _set_manual(p)
        st.rerun()
    place = st.session_state["place"]
    place.setdefault("label", place["name"])
    with st.expander("Exact coordinates"):
        lat = st.number_input("Latitude (° north, negative = south)", -89.0, 89.0, float(place["lat"]), 0.0001,
                              format="%.4f", key=f"lat_{place['name']}_{place['lat']:.4f}")
        lon = st.number_input("Longitude (° east, negative = west)", -180.0, 180.0, float(place["lon"]), 0.0001,
                              format="%.4f", key=f"lon_{place['name']}_{place['lon']:.4f}")
        place = dict(place, lat=lat, lon=lon)
        st.caption(f"Time zone: {place['tz']}")
    st.caption(f"Using: {place['label']}")

    st.subheader("Festivals and Gahs")
    st.radio("Muktad", ["ten", "parsi_18"], key="muktad", on_change=_custom, **_idx("muktad", ["ten", "parsi_18"], "ten"),
             format_func=lambda k: {"ten": "10 days (Ashtad roj of Aspandarmad to the last Gatha day)",
                                    "parsi_18": "18 days (old Parsi custom: Ashishvangh roj of Aspandarmad to Amardad "
                                                "roj of Fravardin)"}[k])
    st.radio("Rapithwin practice", ["summer", "medieval_four"], key="rapithwin", on_change=_custom,
             **_idx("rapithwin", ["summer", "medieval_four"], "summer"),
             format_func=lambda k: {"summer": "Summer rule: Rapithwin Fravardin–Meher mah, Second Havan otherwise",
                                    "medieval_four": "Bundahishn winter rule: four watches in winter"}[k])
    st.radio("Era shown", ["yz", "zre", "yz+zre"], key="era", horizontal=True, on_change=_custom,
             **_idx("era", ["yz", "zre", "yz+zre"], "yz"),
             format_func=lambda k: {"yz": "Y.Z.", "zre": "ZRE", "yz+zre": "both"}[k],
             help="Y.Z. = Yazdegerdi era (from 16 June 632). ZRE = Zarathushtrian Religious Era (Fasli and Bastani only).")
    st.selectbox("Jamshedi Navroz", ["fixed_21_march", "equinox_ist"], key="jamshedi",
                 **_idx("jamshedi", ["fixed_21_march", "equinox_ist"], "fixed_21_march"),
                 format_func=lambda k: {"fixed_21_march": "21 March (Parsi usage)",
                                        "equinox_ist": "day of the March equinox in India Standard Time"}[k],
                 help="With the Bastani calendar it is always Iran's Nowruz.")
    st.selectbox("Sadeh", ["iran", "kerman", "yazd"], key="sadeh", **_idx("sadeh", ["iran", "kerman", "yazd"], "iran"),
                 format_func=lambda k: {"iran": "Iran: civil 10 Bahman", "kerman": "Kerman: Aban roj of Bahman mah",
                                        "yazd": "Yazd: Ashtad roj of Adar mah"}[k])
    st.toggle("Show Iranian civil observances with the Parsi calendars", key="iran_civil",
              **({} if "iran_civil" in st.session_state else {"value": False}),
              help="Sadeh, Chaharshanbe Suri and the civil Tirgan (13 Tir). Always shown with the Bastani calendar.")
    st.toggle("Havan from 36 minutes before sunrise (Havan-ni-Meher)", key="havan_meher",
              **({} if "havan_meher" in st.session_state else {"value": False}))
    with st.expander("Bastani: when Nowruz begins"):
        st.selectbox("Rule", list(irs.RULES), key="bastani_rule",
                     **_idx("bastani_rule", list(irs.RULES), irs.DEFAULT_RULE), format_func=lambda k: irs.RULES[k])
    with st.expander("Sasanian reconstruction"):
        st.radio("Gatha (andargāh) days", ["after_avan", "after_aspandarmad"], key="andargah",
                 **_idx("andargah", ["after_avan", "after_aspandarmad"], "after_avan"),
                 format_func=lambda k: {"after_avan": "after Avan mah (late Sasanian, al-Biruni)",
                                        "after_aspandarmad": "after Aspandarmad (after 375 YZ / 1006 CE)"}[k])
        st.radio("Intercalation", ["none", "kabisa_120"], key="intercalation",
                 **_idx("intercalation", ["none", "kabisa_120"], "none"),
                 format_func=lambda k: {"none": "none (default)",
                                        "kabisa_120": "one month every 120 years (hypothetical model)"}[k])
        st.number_input("Phase of the 120-year cycle (years)", 0, 119, 0, 1, key="kabisa_phase",
                        help="Not documented in the sources: a free parameter of the model.")

# ---------------------------------------------------------------------------------------------- context and page
ss = st.session_state
s = {k: ss.get(k) for k in pages.SETTING_KEYS}
s.update({k: v for k, v in {"muktad": s["muktad"] or "ten", "jamshedi": s["jamshedi"] or "fixed_21_march",
                            "sadeh": s["sadeh"] or "iran", "rapithwin": s["rapithwin"] or "summer",
                            "era": s["era"] or "yz", "andargah": s["andargah"] or "after_avan",
                            "intercalation": s["intercalation"] or "none", "kabisa_phase": s["kabisa_phase"] or 0,
                            "bastani_rule": s["bastani_rule"] or irs.DEFAULT_RULE,
                            "havan_meher": bool(s["havan_meher"]), "iran_civil": bool(s["iran_civil"])}.items()})
now = datetime.now(ZoneInfo(place["tz"]))
if "_now_override" in ss:      # tests only: a fixed moment (ISO string with offset)
    now = datetime.fromisoformat(ss["_now_override"]).astimezone(ZoneInfo(place["tz"]))
ctx = {"place": place, "cal": cal, "now": now, "today": now.date(), "s": s}

PAGES[page][1](ctx)

st.html("<div class='gs-frieze' role='presentation' style='margin-top:1.2rem'></div>"
        "<div class='gs-muted' style='font-size:.8rem'>Astronomy: NASA JPL DE440s via Skyfield. Dates are computed "
        "from the published rules of each calendar; communities announce their own dates, and where a printed "
        "almanac differs, follow it. MIT License (LICENSE).</div>")
