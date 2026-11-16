"""Headless Streamlit AppTest sweep of Sky Gahshomar.

Run from the app folder:  python tools/apptest_sweep.py  [--quick]
Writes tools/apptest_results.json. Every run checks: no exception; the page's own marker is in the HTML; outside
Compare only the chosen calendar's badge appears; popovers use the gs- classes; no '<svg' is passed to st.html
(Streamlit strips inline SVG); the Gahs page has a gs-times table (and a gs-today-row when today is in it).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import traceback
from datetime import date, datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APP = os.path.join(ROOT, "app.py")
sys.path.insert(0, ROOT)

from streamlit.testing.v1 import AppTest  # noqa: E402

import places  # noqa: E402
import sects  # noqa: E402
import zcalendars as zc  # noqa: E402

CALS = list(zc.CALENDARS)
PAGES = ["Today", "Month", "Year", "Gahs", "Prayers", "Festivals", "Compare", "Traditions", "How", "About"]
MARK = {"Prayers": "gs-pr", "Today": "gs-gahs", "Month": "gs-grid", "Year": "gs-mini", "Gahs": "gs-times", "Festivals": "gs-table",
        "Compare": "gs-table", "Traditions": "gs-diagram", "How": None, "About": "Uncertain spellings"}
TROMSO = {"name": "Tromsø", "fa": "", "gu": "", "country": "NO", "lat": 69.6489, "lon": 18.95508, "tz": "Europe/Oslo",
          "elev": 0.0, "label": "Tromsø, Norway (high latitude)"}          # GeoNames 3133895
PL = {k: dict(places.PRESETS_BY_KEY[k], label=places.preset_label(places.PRESETS_BY_KEY[k]))
      for k in ("mumbai", "udvada", "yazd", "karachi", "london", "toronto", "los_angeles", "sydney")}
PL["tromso"] = TROMSO

results = {"runs": 0, "pass": 0, "fail": 0, "failures": [], "groups": {}}


def htmls(at) -> list[str]:
    return [el.proto.body for el in at.get("html")]


def md_text(at) -> str:
    return "\n".join(m.value for m in at.markdown)


def check(at, page: str, cal: str, label: str, extra=None):
    """Run the standard checks on an AppTest that has just run; record pass/fail."""
    results["runs"] += 1
    grp = label.split(":")[0]
    g = results["groups"].setdefault(grp, {"runs": 0, "pass": 0})
    g["runs"] += 1
    errs = []
    if at.exception:
        errs.append("exception: " + " | ".join(e.message[:400] for e in at.exception))
    H = htmls(at)
    body = "\n".join(H)
    for h in H:
        if h.lstrip().startswith("<style>"):
            continue
        if "<svg" in h:
            errs.append("inline <svg> passed to st.html (Streamlit strips it)")
            break
    mk = MARK.get(page)
    if page == "Month" and "gs-list" in body:
        mk = "gs-list"
    if mk and mk not in body:
        errs.append(f"marker {mk!r} missing")
    if page == "How" and "How Sky Gahshomar works" not in md_text(at):
        errs.append("HOW_IT_WORKS.md not rendered")
    if "sg-pop" in body:
        errs.append("sg-pop class present")
    badges = set(re.findall(r"gs-cal-([a-z]+)'", body))
    if page not in ("Compare", "Traditions", "How", "About"):
        other = badges - {cal}
        if other:
            errs.append(f"other calendars shown outside Compare: {sorted(other)}")
        if page in ("Today", "Month", "Year", "Gahs", "Festivals") and cal not in badges:
            errs.append("chosen calendar badge missing")
    if page == "Compare" and badges != set(CALS):
        errs.append(f"Compare shows {sorted(badges)}")
    if at.session_state["cal"] != cal:
        errs.append(f"calendar state {at.session_state['cal']} != {cal}")
    if extra:
        try:
            e = extra(at, body)
            if e:
                errs.append(e)
        except Exception as exc:     # a failing check is a failure, not a crash of the sweep
            errs.append(f"check error {exc!r}")
    if errs:
        results["fail"] += 1
        results["failures"].append({"run": label, "errors": errs})
    else:
        results["pass"] += 1
        g["pass"] += 1


def new_app(place=None, now=None, state=None):
    at = AppTest.from_file(APP, default_timeout=180)
    if place is not None:
        at.session_state["place"] = dict(place)
        at.session_state["place_src"] = "manual"
    if now is not None:
        at.session_state["_now_override"] = now
    for k, v in (state or {}).items():
        at.session_state[k] = v
    at.run()
    return at


def goto(at, page):
    at.radio(key="page").set_value(page).run()


def set_cal(at, cal):
    if at.session_state["cal"] != cal:
        at.radio(key="cal").set_value(cal).run()


def main(quick=False):
    t0 = time.time()
    # A. default first visit: Parsi Shahanshahi preset at Mumbai
    at = new_app()
    ok = (at.session_state["cal"] == "shahanshahi" and at.session_state["sect"] == "parsi_shahanshahi:0"
          and at.session_state["place"]["name"] == "Mumbai" and at.session_state["muktad"] == "ten")
    check(at, "Today", "shahanshahi", "A_default:Today",
          extra=lambda a, b: None if ok else "default is not Parsi Shahanshahi at Mumbai")
    labels = at.radio(key="cal").options
    check(at, "Today", "shahanshahi", "A_default:labels",
          extra=lambda a, b: None if labels == [f"{n['en']} · {n['fa']} · {n['gu']}" for n in
                                                (__import__('names').CALENDAR[c] for c in CALS)] else f"labels {labels}")

    # B. every community preset (sidebar selectbox) x every page
    opts = [f"{s['key']}:{i}" for s in sects.SECTS for i in range(len(s["uses"]))]
    for o in opts:
        at = new_app()
        at.selectbox(key="sect").set_value(o).run()
        k, i = o.split(":")
        p = sects.preset(k, int(i))
        want_m = "parsi_18" if p["muktad_days"] == 18 else "ten"
        for pg in PAGES:
            goto(at, pg)
            check(at, pg, p["calendar"], f"B_preset:{o}:{pg}",
                  extra=lambda a, b, p=p, want_m=want_m: None if (a.session_state["muktad"] == want_m and
                                                                  a.session_state["rapithwin"] == p["rapithwin"] and
                                                                  a.session_state["era"] == p["era"]) else "preset not applied")

    # C. every calendar x every page x places (incl. high latitude)
    plist = list(PL) if not quick else ["mumbai", "tromso"]
    for pk in plist:
        at = new_app(place=PL[pk])
        for cal in CALS:
            set_cal(at, cal)
            for pg in PAGES:
                goto(at, pg)

                def gah_extra(a, b, pg=pg):
                    if pg == "Gahs" and "gs-today-row" not in b:
                        return "today row missing on Gahs page"
                    if pg == "Today" and cal == "sasanian" and a.session_state["rapithwin"] != "medieval_four":
                        return "Sasanian did not select the Bundahishn rule"
                    return None
                check(at, pg, cal, f"C_cal_place:{pk}:{cal}:{pg}", extra=gah_extra)

    # D. dated cases: Gatha periods, leap days, polar day/night, before sunrise, range edges
    dcases = []
    for cal in CALS:
        y = zc.year_containing(date(2026, 11, 15), cal)
        g1 = zc.from_zdate(y, 13, 1, cal)
        dcases.append((f"gatha_{cal}", cal, "mumbai", datetime(g1.year, g1.month, g1.day, 10, 0) + timedelta(days=2), "Gatha"))
    for cal in ("fasli", "bastani"):
        for y in range(zc.year_containing(date(2026, 1, 1), cal), zc.year_containing(date(2040, 1, 1), cal)):
            if zc.year_length(y, cal) == 366:
                d = zc.from_zdate(y, 13, 6, cal)
                dcases.append((f"leapday_{cal}_{d}", cal, "yazd" if cal == "bastani" else "mumbai",
                               datetime(d.year, d.month, d.day, 12, 0), "Avardad"))
                break
    dcases += [("polar_night", "fasli", "tromso", datetime(2026, 12, 15, 12, 0), "Polar night"),
               ("polar_day", "shahanshahi", "tromso", datetime(2026, 6, 21, 12, 0), "Polar day"),
               ("before_sunrise", "shahanshahi", "mumbai", datetime(2026, 8, 15, 5, 0), "Before sunrise"),
               ("navroz_2026", "shahanshahi", "mumbai", datetime(2026, 8, 15, 9, 0), "Navroz"),
               ("leap_feb29_2028", "fasli", "london", datetime(2028, 2, 29, 9, 0), None),
               ("edge_1850", "kadmi", "mumbai", datetime(1850, 1, 10, 9, 0), None),
               ("edge_2149", "bastani", "tehran", datetime(2149, 12, 20, 9, 0), None),
               ("sydney_winter", "bastani", "sydney", datetime(2027, 6, 21, 13, 0), None),
               ("la_night", "kadmi", "los_angeles", datetime(2026, 11, 15, 23, 30), None)]
    for name, cal, pk, dt, want in dcases:
        pl = PL.get(pk) or dict(places.PRESETS_BY_KEY[pk], label=pk)
        from zoneinfo import ZoneInfo
        iso = dt.replace(tzinfo=ZoneInfo(pl["tz"])).isoformat()
        at = new_app(place=pl, now=iso)
        set_cal(at, cal)
        for pg in ["Today", "Month", "Year", "Gahs", "Festivals", "Compare"]:
            goto(at, pg)

            def dextra(a, b, pg=pg, want=want):
                if pg == "Today" and want and want not in b:
                    return f"expected {want!r} on Today"
                return None
            check(at, pg, cal, f"D_dates:{name}:{pg}", extra=dextra)

    # E. settings variants
    variants = [("muktad", "parsi_18", "radio"), ("rapithwin", "medieval_four", "radio"), ("era", "zre", "radio"),
                ("era", "yz+zre", "radio"), ("jamshedi", "equinox_ist", "selectbox"), ("sadeh", "kerman", "selectbox"),
                ("sadeh", "yazd", "selectbox"), ("iran_civil", True, "toggle"), ("havan_meher", True, "toggle"),
                ("phone_layout", True, "toggle")]
    for key, val, kind in variants:
        for cal in CALS:
            at = new_app()
            set_cal(at, cal)
            getattr(at, kind)(key=key).set_value(val).run()
            for pg in ["Today", "Month", "Year", "Gahs", "Festivals", "Compare"]:
                goto(at, pg)
                check(at, pg, cal, f"E_settings:{key}={val}:{cal}:{pg}",
                      extra=lambda a, b, key=key, val=val: None if a.session_state[key] == val else f"{key} not kept")
    # Bastani rules and Sasanian model options
    import iran_solar as irs
    for rule in irs.RULES:
        at = new_app(place=PL["yazd"])
        set_cal(at, "bastani")
        at.selectbox(key="bastani_rule").set_value(rule).run()
        for pg in ["Today", "Month", "Year", "Festivals", "Compare"]:
            goto(at, pg)
            check(at, pg, "bastani", f"E_bastani:{rule}:{pg}",
                  extra=lambda a, b, pg=pg: None if pg != "Festivals" or "Iranian civil date" in b else "civil column missing")
    for andargah, inter, phase in [("after_aspandarmad", "none", 0), ("after_avan", "kabisa_120", 0),
                                   ("after_avan", "kabisa_120", 37), ("after_aspandarmad", "kabisa_120", 100)]:
        at = new_app()
        set_cal(at, "sasanian")
        at.radio(key="andargah").set_value(andargah).run()
        at.radio(key="intercalation").set_value(inter).run()
        at.number_input(key="kabisa_phase").set_value(phase).run()
        for pg in ["Today", "Month", "Year", "Gahs", "Festivals", "Compare"]:
            goto(at, pg)
            check(at, pg, "sasanian", f"E_sasanian:{andargah}:{inter}:{phase}:{pg}",
                  extra=lambda a, b: None if "reconstruction" in b else "reconstruction label missing")

    # F. interactions: Traditions 'Use' buttons, month navigation, popovers
    at = new_app()
    goto(at, "Traditions")
    for s in sects.SECTS:
        for i, (c, lab, p) in enumerate(s["uses"]):
            at.button(key=f"use_{s['key']}_{i}").click().run()
            check(at, "Traditions", p["calendar"], f"F_use:{s['key']}:{i}",
                  extra=lambda a, b, s=s, i=i: None if a.session_state["sect"] == f"{s['key']}:{i}" else "sect not set")
    at = new_app()
    goto(at, "Month")
    for b_ in ["m_next", "m_next", "m_prev", "m_today", "m_prev", "m_prev"] * (1 if quick else 3):
        at.button(key=b_).click().run()
        check(at, "Month", "shahanshahi", f"F_month_nav:{b_}")
    for cal in CALS:          # walk a whole year of months, incl. the Gatha 'month'
        at = new_app()
        set_cal(at, cal)
        goto(at, "Month")
        for k in range(14):
            at.button(key="m_next").click().run()
            check(at, "Month", cal, f"F_month_walk:{cal}:{k}")
    results["seconds"] = round(time.time() - t0, 1)


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    try:
        main(quick)
    except Exception:
        results["crash"] = traceback.format_exc()
    with open(os.path.join(HERE, "apptest_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, ensure_ascii=False)
    print(json.dumps({k: results[k] for k in ("runs", "pass", "fail")}), "crash" in results)
    for x in results["failures"][:25]:
        print(x)
    if "crash" in results:
        print(results["crash"][-3000:])
