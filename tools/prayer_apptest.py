"""Focused AppTest checks for the prayer links (one case per process, each with its own time limit).
Run from the app folder:  python tools/prayer_apptest.py      Writes tools/prayer_apptest_results.json."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CASE_CODE = r"""
import json, sys
from streamlit.testing.v1 import AppTest
app, page, cal, now, must, minlinks = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], json.loads(sys.argv[5]), int(sys.argv[6])
at = AppTest.from_file(app, default_timeout=170)
at.session_state["page"] = page
at.session_state["cal"] = cal
at.session_state["sect"] = "custom"
if now != "-":
    at.session_state["_now_override"] = now
at.run()
body = "\n".join(el.proto.body for el in at.get("html"))
errs = []
if at.exception:
    errs.append("exception: " + " | ".join(e.message[:300] for e in at.exception))
for m in must:
    if m not in body:
        errs.append("missing " + m)
n = body.count("class='gs-pr'")
if n < minlinks:
    errs.append(f"only {n} prayer links")
if "class='gs-pr'" in body and "target='_blank'" not in body:
    errs.append("links lack target=_blank")
print(json.dumps({"errs": errs, "links": n}))
"""

def cases():
    sys.path.insert(0, HERE)
    import festivals as F
    import zcalendars as zc
    from datetime import date, timedelta
    y = zc.year_containing(date(2026, 11, 16), "shahanshahi")
    fl = F.festivals_in_year(y, "shahanshahi")
    avan = next(f for f in fl if f.key == "jashan_avan").start
    gah = next(f for f in fl if f.key.startswith("gahambar_")).start
    nz = zc.navroz(y + 1, "shahanshahi")
    gatha1 = nz - timedelta(days=5)
    ff = F.festivals_in_year(zc.year_containing(date(2027, 1, 1), "fasli"), "fasli")
    adar_f = next(f for f in ff if f.key == "jashan_adar").start
    A = "https://www.avesta.org/"
    return [
        ("Prayers", "shahanshahi", "-", [A + "ka/gahs.htm#g1", A + "yasna/yasna.htm#y28", A + "kanga/Khorda_Avesta_Kanga_Gujarati.pdf"], 41),
        ("Today", "shahanshahi", f"{avan}T10:00:00+05:30", [A + "ka/niyayesh.htm#ny4", A + "ka/gahs.htm#g1", A + "ka/niyayesh.htm#ny1"], 5),
        ("Today", "shahanshahi", f"{avan}T21:30:00+05:30", [A + "ka/gahs.htm#g4", A + "yasna/yasna.htm#y57"], 4),
        ("Today", "shahanshahi", f"{gatha1}T09:00:00+05:30", [A + "yasna/yasna.htm#y28", A + "ka/a2sbe.htm"], 3),
        ("Today", "shahanshahi", f"{gah}T12:30:00+05:30", [A + "ka/a3sbe.htm"], 3),
        ("Today", "fasli", f"{adar_f}T05:00:00+05:30", [A + "ka/gahs.htm#g5", A + "ka/ka_part1.htm#hb"], 3),
        ("Today", "fasli", f"{adar_f}T10:00:00+05:30", [A + "ka/niyayesh.htm#ny5", A + "ka/gahs.htm#g1"], 3),
        ("Gahs", "shahanshahi", "-", [A + "ka/gahs.htm#g%d" % i for i in range(1, 6)], 10),
        ("Festivals", "shahanshahi", "-", ["Read ↗", A + "ka/a3sbe.htm", A + "ka/niyayesh.htm#ny3"], 10),
        ("Festivals", "bastani", "-", ["Read ↗", A + "ka/yt10sbe.htm"], 10),
        ("About", "shahanshahi", "-", ["PRAYER"], 0),
        ("Month", "kadmi", "-", [], 0),
        ("Compare", "sasanian", "-", [], 0),
    ]

def main():
    app = os.path.join(HERE, "app.py")
    out = {"runs": 0, "pass": 0, "fail": 0, "timeouts": 0, "failures": []}
    for page, cal, now, must, minl in cases():
        out["runs"] += 1
        label = f"{page}/{cal}/{now}"
        try:
            r = subprocess.run([sys.executable, "-c", CASE_CODE, app, page, cal, now, json.dumps(must), str(minl)],
                               capture_output=True, text=True, timeout=200, cwd=HERE)
            res = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {"errs": ["no output: " + r.stderr[-300:]]}
        except subprocess.TimeoutExpired:
            out["timeouts"] += 1
            res = {"errs": ["timeout (200 s)"]}
        if res["errs"]:
            out["fail"] += 1
            out["failures"].append({"run": label, "errors": res["errs"]})
        else:
            out["pass"] += 1
        print(label, "OK" if not res["errs"] else res["errs"], res.get("links", ""), flush=True)
    json.dump(out, open(os.path.join(HERE, "tools", "prayer_apptest_results.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("runs", "pass", "fail", "timeouts")}))

if __name__ == "__main__":
    main()
