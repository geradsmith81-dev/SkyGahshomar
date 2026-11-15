"""
Validation of the Sky Gahshomar engine. Run from the engine folder:

    python validation/validate.py            (writes validation/results.json and CSV files)

Parts
  A  published dates (validation/published_dates.csv, each row with its source)
  B  independent converter: the ZANC / Heritage Institute JavaScript converter (zcalendar.js,
     Kainaz Amaria, CC BY-NC-SA 1.0), downloaded at run time and run with the 'quickjs' package,
     compared day by day 1850-2149 for Shahanshahi, Kadmi and Fasli. Skipped if offline or if
     quickjs is missing (the script is not redistributed here because of its licence).
  C  Heritage Institute 365-day Fasli/Bastani perpetual grid (K. E. Eduljee), transcribed in
     validation/heritage_fasli_grid.csv
  D  Bastani Nowruz vs persiantools / jdatetime and vs Sky Taqwim's published data/seasons.csv
  E  internal consistency over every civil date 1850-01-01 .. 2149-12-31
  F  Gahs and sunrise-day rule (structural checks for sample places)
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import pandas as pd  # noqa: E402

import festivals as F  # noqa: E402
import iran_solar as ir  # noqa: E402
import sky_engine as se  # noqa: E402
import sky_layer as sl  # noqa: E402
import zcalendars as zc  # noqa: E402
import znames as zn  # noqa: E402

START, END = date(1850, 1, 1), date(2149, 12, 31)
RESULTS = {}


def part_a():
    df = pd.read_csv(os.path.join(HERE, "published_dates.csv"))
    rows = []
    for _, r in df.iterrows():
        d = date.fromisoformat(r["gregorian"])
        z = zc.to_zdate(d, r["cal"])
        if r["mah"] == 13:
            got = (z.mah, z.day)
            exp = (13, int(r["day"]))
        else:
            got = (z.mah, z.day)
            exp = (int(r["mah"]), int(r["day"]))
        ok = got == exp and (pd.isna(r["year"]) or int(r["year"]) == z.eras.get(r["era"], z.year))
        rows.append({**r.to_dict(), "engine": z.label(), "engine_era_year": z.eras.get(r["era"]), "match": ok})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(HERE, "result_published.csv"), index=False)
    RESULTS["A_published"] = {"n": len(out), "match": int(out["match"].sum()),
                              "mismatch_rows": out[~out["match"]].to_dict("records")}


ZANC_URL = "http://www.heritageinstitute.com/zoroastrianism/calendar/js/"
ZANC_ROJ = ["Hormazd", "Bahman", "Ardibehesht", "Shehrevar", "Aspandard", "Khordad", "Amardad", "Dae-Pa-Adar",
            "Adar", "Avan", "Khorshed", "Mohor", "Tir", "Gosh", "Dae-Pa-Meher", "Meher", "Srosh", "Rashne",
            "Fravardin", "Behram", "Ram", "Govad", "Dae-Pa-Din", "Din", "Ashishvangh", "Ashtad", "Asman",
            "Zamyad", "Mareshpand", "Aneran"]
ZANC_MAH = ["Fravardin", "Ardibehesht", "Khordad", "Tir", "Amardad", "Shehrevar", "Meher", "Avan", "Adar", "Dae",
            "Bahman", "Aspandard"]
ZANC_G = ["Ahunavaiti", "Ushtavaiti", "Spentamainyu", "Vohuxshathra", "Vahishtoishti", "Avardad-sal-Gah"]


def part_b():
    try:
        import urllib.request
        import quickjs
        get = lambda f: urllib.request.urlopen(ZANC_URL + f, timeout=30).read().decode("latin-1")
        ctx = quickjs.Context()
        ctx.eval("var Prototype={Version:'1.5'};var Class={create:function(){return function(){"
                 "this.initialize.apply(this,arguments);}}};Object.extend=function(d,s){for(var k in s){d[k]=s[k];}return d;};")
        ctx.eval(get("inc/date_ext.js"))
        ctx.eval(get("zcalendar.js"))
        ctx.eval("""function run(cal,y0,y1){var C=ZCalendar[cal];var out=[];var d=new Date(y0,0,1,12,0,0);
          var end=new Date(y1,11,31,12,0,0);while(d<=end){var c=C.convertDateToRoj(d);out.push(c.roj+'|'+c.mah);
          d=new Date(d.getFullYear(),d.getMonth(),d.getDate()+1,12,0,0);}return out.join(';');}""")
    except Exception as exc:   # offline or quickjs missing
        RESULTS["B_zanc"] = {"skipped": str(exc)}
        return
    out = {}
    for jcal, cal in (("Shenshai", "shahanshahi"), ("Kadmi", "kadmi"), ("Fasli", "fasli")):
        toks = ctx.eval(f"run('{jcal}',{START.year},{END.year})").split(";")
        bad = []
        for i, tok in enumerate(toks):
            d = START + timedelta(days=i)
            z = zc.to_zdate(d, cal)
            e = (ZANC_G[z.day - 1] + "|") if z.is_gatha else ZANC_ROJ[z.day - 1] + "|" + ZANC_MAH[z.mah - 1]
            if tok != e:
                bad.append((d.isoformat(), tok, e))
        yz = ctx.eval(f"var c=ZCalendar.{jcal}.convertDateToRoj(new Date(2026,7,20,12));c.yzYear")
        out[cal] = {"days": len(toks), "mismatch": len(bad), "first_mismatches": bad[:5],
                    "zanc_yz_on_2026_08_20": yz, "engine_yz_on_2026_08_20": zc.to_zdate(date(2026, 8, 20), cal).eras.get("YZ")}
    RESULTS["B_zanc"] = out


def part_c():
    g = pd.read_csv(os.path.join(HERE, "heritage_fasli_grid.csv"))
    rows = []
    for _, r in g.iterrows():
        if pd.isna(r["grid_day"]):
            continue
        if int(r["mah"]) == 13:
            d = zc.from_zdate(1395, 13, int(r["roj"]), "fasli")
        else:
            d = zc.from_zdate(1395, int(r["mah"]), int(r["roj"]), "fasli")
        month_ok = pd.isna(r["grid_month"]) or d.month == int(r["grid_month"])
        rows.append({"roj": r["roj"], "mah": r["mah"], "grid_month": r["grid_month"], "grid_day": int(r["grid_day"]),
                     "engine": d.isoformat(), "match": d.day == int(r["grid_day"]) and month_ok})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, "result_heritage_grid.csv"), index=False)
    leap = zc.from_zdate(1397, 12, 16, "fasli")   # grid note: 'Leap Year' shift begins at Meher roj, Aspandarmad
    RESULTS["C_heritage_grid"] = {"n": len(df), "match": int(df["match"].sum()),
                                  "with_month_name": int(df["grid_month"].notna().sum()),
                                  "leap_shift_check": {"meher_roj_aspandarmad_YZ1397": leap.isoformat(),
                                                       "avardad_sal_gah_YZ1397": zc.from_zdate(1397, 13, 6, "fasli").isoformat()}}


def part_d():
    rows = []
    try:
        from persiantools.jdatetime import JalaliDate
    except ImportError:
        JalaliDate = None
    try:
        import jdatetime
    except ImportError:
        jdatetime = None
    for gy in range(1850, 2150):
        e = ir.nowruz(gy)
        row = {"gregorian_year": gy, "engine_true_noon_52.5": e, "mean_noon_52.5": ir.nowruz(gy, "mean_noon_52.5"),
               "true_noon_tehran": ir.nowruz(gy, "true_noon_tehran"),
               "equinox_utc": ir.march_equinox_utc(gy).isoformat()}
        if JalaliDate:
            row["persiantools"] = JalaliDate(gy - 621, 1, 1).to_gregorian()
        if jdatetime:
            row["jdatetime"] = jdatetime.date(gy - 621, 1, 1).togregorian()
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(ROOT, "data", "bastani_nowruz.csv"), index=False)
    res = {}
    for c in ("persiantools", "jdatetime", "mean_noon_52.5", "true_noon_tehran"):
        if c in df:
            diff = df[df[c] != df["engine_true_noon_52.5"]]
            res[c] = {"n": len(df), "differ": len(diff), "years": [int(x) for x in diff["gregorian_year"]]}
    # Sky Taqwim's published seasons.csv
    try:
        import urllib.request
        import io
        b = urllib.request.urlopen("https://raw.githubusercontent.com/geradsmith81-dev/sky-taqwim/main/data/seasons.csv",
                                   timeout=30).read()
        t = pd.read_csv(io.BytesIO(b))
        m = pd.read_csv(ir.SEASONS_FILE)
        t0, m0 = t[t.kind == 0].reset_index(drop=True), m[m.kind == 0].reset_index(drop=True)
        res["sky_taqwim_seasons_csv"] = {r: int((t0[f"nowruz_{r}"] != m0[f"nowruz_{r}"]).sum()) for r in ir.RULES}
        res["sky_taqwim_seasons_csv"]["n"] = len(t0)
        dt = (pd.to_datetime(t["utc"], format="ISO8601") - pd.to_datetime(m["utc"], format="ISO8601")).abs().max()
        res["sky_taqwim_seasons_csv"]["max_abs_time_diff_s"] = float(dt.total_seconds())
    except Exception as exc:
        res["sky_taqwim_seasons_csv"] = {"skipped": str(exc)}
    # closest calls (equinox within 2 minutes of true noon at 52.5 E)
    s = ir.season_table()
    eq = s[s.kind == 0].copy()
    eq["margin_s"] = (pd.to_datetime(eq["true_noon_52.5_utc"], format="ISO8601") - eq["utc"]).dt.total_seconds()
    close = eq[eq["margin_s"].abs() < 120]
    res["equinox_within_2_min_of_true_noon"] = [{"year": int(u.year), "equinox_utc": u.isoformat(),
                                                 "margin_s": round(float(mg), 1)} for u, mg in zip(close["utc"], close["margin_s"])]
    RESULTS["D_bastani_nowruz"] = res


def _consecutive(cal, **opts):
    n_bad = 0
    prev = None
    rt_bad = 0
    d = START
    while d <= END:
        z = zc.to_zdate(d, cal, **opts)
        if zc.from_zdate(z.year, z.mah, z.day, cal, repeated=z.repeated_month, **opts) != d:
            rt_bad += 1
        if prev is not None:
            ok = (z.year == prev.year and z.day_of_year == prev.day_of_year + 1) or \
                 (z.year == prev.year + 1 and z.day_of_year == 1)
            n_bad += not ok
        prev = z
        d += timedelta(days=1)
    return rt_bad, n_bad


def part_e():
    res = {}
    configs = [("shahanshahi", {}), ("kadmi", {}), ("fasli", {}), ("bastani", {}), ("sasanian", {}),
               ("sasanian", {"andargah": "after_aspandarmad"}), ("sasanian", {"intercalation": "kabisa_120"})]
    days = (END - START).days + 1
    for cal, o in configs:
        rt, cons = _consecutive(cal, **o)
        y0, y1 = zc.year_containing(START, cal, **o), zc.year_containing(END, cal, **o)
        lengths = {}
        for y in range(y0, y1 + 1):
            n = zc.year_length(y, cal, **o)
            lengths[n] = lengths.get(n, 0) + 1
        res[cal + ("" if not o else ":" + ",".join(f"{k}={v}" for k, v in o.items()))] = {
            "days": days, "roundtrip_fail": rt, "sequence_fail": cons, "year_lengths": lengths, "years": [y0, y1]}
    # Kadmi = Shahanshahi shifted by 30 days
    bad = 0
    d = START
    while d <= END - timedelta(days=30):
        a, b = zc.to_zdate(d, "kadmi"), zc.to_zdate(d + timedelta(days=30), "shahanshahi")
        bad += (a.year, a.mah, a.day) != (b.year, b.mah, b.day)
        d += timedelta(days=1)
    res["kadmi_equals_shahanshahi_plus_30"] = {"fail": bad}
    # Fasli rules
    fz = [zc.navroz(y, "fasli") for y in range(1220, 1520)]
    res["fasli_navroz_21_march"] = {"n": len(fz), "fail": sum(1 for x in fz if (x.month, x.day) != (3, 21))}
    fl = [y for y in range(1220, 1519) if zc.is_leap(y, "fasli") != _greg_leap(y + 631)]
    res["fasli_leap_iff_next_feb29"] = {"fail": len(fl)}
    # Bastani: Mehregan = civil 10 Mehr, Tir jashan = civil 10 Tir, leap iff civil Esfand has 30 days
    mf, tf, lf = [], [], []
    for zy in range(3588, 3887):
        mg = zc.from_zdate(zy, 7, 16, "bastani")
        tg = zc.from_zdate(zy, 4, 13, "bastani")
        if ir.to_civil(mg)[1:] != (7, 10):
            mf.append(zy)
        if ir.to_civil(tg)[1:] != (4, 10):
            tf.append(zy)
        last = zc.navroz(zy + 1, "bastani") - timedelta(days=1)
        if zc.is_leap(zy, "bastani") != (ir.to_civil(last)[2] == 30):
            lf.append(zy)
    res["bastani_mehregan_is_civil_10_mehr"] = {"n": 299, "fail": len(mf)}
    res["bastani_tir_jashan_is_civil_10_tir"] = {"n": 299, "fail": len(tf)}
    res["bastani_leap_iff_civil_esfand_30"] = {"n": 299, "fail": len(lf)}
    # festivals: structural checks per year
    fbad, fcount = [], 0
    for cal in ("shahanshahi", "kadmi", "fasli", "bastani", "sasanian"):
        y0, y1 = zc.year_containing(START, cal) + 1, zc.year_containing(END, cal) - 1
        for y in range(y0, y1 + 1):
            fs = F.festivals_in_year(y, cal)
            fcount += len(fs)
            k = {f.key: f for f in fs}
            z = k["khordad_sal"].zstart
            if (z.mah, z.roj_key) != (1, "khordad"):
                fbad.append((cal, y, "khordad_sal"))
            if (k["zarthost_no_diso"].zstart.mah, k["zarthost_no_diso"].zstart.roj_key) != (10, "khorshed"):
                fbad.append((cal, y, "zarthost_no_diso"))
            muktad_end = (zc.from_zdate(y, zc.GATHA_MAH, 5, cal) if cal == "sasanian"
                          else zc.navroz(y + 1, cal) - timedelta(days=1))   # Sasanian: end of the andargah
            if k["muktad"].end != muktad_end:
                fbad.append((cal, y, "muktad_end"))
            if sum(1 for f in fs if f.key == "jashan_dae") != 4:
                fbad.append((cal, y, "dae_jashans"))
            for f in fs:
                if f.key.startswith("jashan_") and f.key != "jashan_dae":
                    if zn.JASHAN_ROJ_FOR_MAH[f.key[7:]] != f.zstart.roj_key or zn.MAH_KEYS[f.zstart.mah - 1] != f.key[7:]:
                        fbad.append((cal, y, f.key))
                if f.key.startswith("gahambar_") and f.days != 5:
                    fbad.append((cal, y, f.key))
    res["festival_structure"] = {"festivals_checked": fcount, "fail": len(fbad), "examples": fbad[:5]}
    RESULTS["E_internal"] = res


def _greg_leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def part_f():
    places = [se.UDVADA, se.MUMBAI, se.YAZD, se.TEHRAN,
              {"name": "Toronto", "lat": 43.65, "lon": -79.38, "tz": "America/Toronto"},
              {"name": "Tromso", "lat": 69.65, "lon": 18.96, "tz": "Europe/Oslo"}]
    dates = [date(2026, m, 15) for m in range(1, 13)]
    bad, n = [], 0
    for p in places:
        for d in dates:
            for cal in ("shahanshahi", "fasli"):
                g = sl.gahs(d, p, cal)
                gs = g["gahs"]
                n += 1
                cont = all(gs[i].end == gs[i + 1].start for i in range(4)) and all(x.start < x.end for x in gs)
                season_ok = (gs[1].key == "rapithwin") == (not g["zdate"].is_gatha and g["zdate"].mah <= 7)
                if not (cont and season_ok):
                    bad.append((p["name"], d.isoformat(), cal))
    # sunrise-day rule
    tz = ZoneInfo("Asia/Kolkata")
    sd = se.solar_day(se.MUMBAI, date(2026, 8, 15))
    before = zc.zdate_at(sd["sunrise"] - timedelta(minutes=1), se.MUMBAI, "shahanshahi")
    after = zc.zdate_at(sd["sunrise"] + timedelta(minutes=1), se.MUMBAI, "shahanshahi")
    # Mumbai true noon over a year vs the 12:40 used in Parsi prayer guides
    noons = [se.solar_day(se.MUMBAI, date(2026, 1, 1) + timedelta(days=i))["noon"] for i in range(0, 365, 5)]
    mins = [x.hour * 60 + x.minute + x.second / 60 for x in noons]
    RESULTS["F_gahs"] = {"place_days": n, "fail": len(bad), "examples": bad[:5],
                         "sunrise_rule": {"1_min_before_sunrise_15_aug_2026": before.label(),
                                          "1_min_after": after.label()},
                         "mumbai_true_noon_range_IST": [f"{int(min(mins)//60)}:{int(min(mins)%60):02d}",
                                                        f"{int(max(mins)//60)}:{int(max(mins)%60):02d}"]}


if __name__ == "__main__":
    for p in (part_a, part_b, part_c, part_d, part_e, part_f):
        p()
        print(p.__name__, "done")
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf8") as fh:
        json.dump(RESULTS, fh, indent=1, default=str, ensure_ascii=False)
    print(json.dumps(RESULTS, indent=1, default=str, ensure_ascii=False)[:4000])
