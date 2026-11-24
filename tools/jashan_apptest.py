"""Focused AppTest checks for the jashan days (one case per process, each with its own time limit).
Run from the app folder:  python tools/jashan_apptest.py      Writes tools/jashan_apptest_results.json."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CASE_CODE = r"""
import json, sys
from streamlit.testing.v1 import AppTest
app, page, cal, now, must, minlinks = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], json.loads(sys.argv[5]), int(sys.argv[6])
state = json.loads(sys.argv[7]) if len(sys.argv) > 7 else {}
at = AppTest.from_file(app, default_timeout=170)
at.session_state["page"] = page
at.session_state["cal"] = cal
at.session_state["sect"] = "custom"
for k, v in state.items():
    at.session_state[k] = v
if now != "-":
    at.session_state["_now_override"] = now
at.run()
body = "\n".join(el.proto.body for el in at.get("html"))
errs = []
if at.exception:
    errs.append("exception: " + " | ".join(e.message[:300] for e in at.exception))
for m in must:
    if m.startswith("!"):
        if m[1:] in body:
            errs.append("should not show " + m[1:])
    elif m not in body:
        errs.append("missing " + m)
n = body.count("gs-pop-note")
if n < minlinks:
    errs.append(f"only {n} commemoration notes")
print(json.dumps({"errs": errs, "links": n}))
"""


def cases():
    # (page, calendar, moment, strings that must / must not (!) appear, min commemoration notes, extra state)
    M = "_now_override"
    return [
        ("Today", "shahanshahi", "2026-09-30T10:00:00+05:30",
         ["Navsari Atash Behram salgreh", "Modi Atash Behram salgreh", "Wadiaji Atash Behram salgreh",
          "gs-jnote", "Commemorates:", "ka/niyayesh.htm#ny5"], 3, {}),
        ("Month", "shahanshahi", "2026-09-30T10:00:00+05:30",
         ["Navsari Atash Behram salgreh", "Dadyseth Atash Behram anniversary", "Ardibehesht Jashan", "!Pir-e"], 5, {}),
        ("Month", "kadmi", "2026-08-01T10:00:00+05:30", ["Dadyseth Atash Behram salgreh (Mumbai, Kadmi)"], 1, {}),
        ("Month", "kadmi", "2026-10-16T10:00:00+05:30", ["Vakil Kadmi Atash Behram salgreh"], 1, {}),
        ("Month", "fasli", "2026-11-24T10:00:00+05:30", ["Iranshah Atash Behram Fasli salgreh"], 1, {}),
        ("Month", "bastani", "2027-06-14T10:00:00+03:30", ["Pir-e Sabz (Chak Chak) pilgrimage", "Seti Pir", "!Navsari Atash Behram", "!Iranshah Atash Behram"], 2,
         {"place": {"name": "Yazd", "lat": 31.8974, "lon": 54.3569, "tz": "Asia/Tehran", "label": "Yazd"}, "place_src": "manual"}),
        ("Festivals", "bastani", "-", ["Mehregan", "Abangan", "Sepandarmazgan", "Shab-e Yalda", "Pir-e Naraki", "In Iran:", "5 Esfand"], 20, {}),
        ("Festivals", "shahanshahi", "-", ["Homaji ni Baj", "Kukadaru", "Iranshah Atash Behram salgreh", "!Pir-e Sabz", "!Shab-e Yalda"], 30, {}),
        ("Festivals", "sasanian", "-", ["!salgreh", "!Pir-e"], 5, {}),
        ("Today", "shahanshahi", "2026-12-21T19:00:00+05:30", ["!Shab-e Yalda"], 0, {}),
        ("About", "shahanshahi", "-", ["JASHAN"], 0, {}),
        ("Festivals", "shahanshahi", "-", ["Pir-e Sabz (Chak Chak) pilgrimage", "Shab-e Yalda"], 30, {"iran_civil": True}),
    ]

def main():
    app = os.path.join(HERE, "app.py")
    out = {"runs": 0, "pass": 0, "fail": 0, "timeouts": 0, "failures": []}
    for page, cal, now, must, minn, state in cases():
        out["runs"] += 1
        label = f"{page}/{cal}/{now}"
        try:
            r = subprocess.run([sys.executable, "-c", CASE_CODE, app, page, cal, now, json.dumps(must), str(minn), json.dumps(state)],
                               capture_output=True, text=True, timeout=200, cwd=HERE)
            res = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {"errs": ["no output: " + r.stderr[-400:]]}
        except subprocess.TimeoutExpired:
            out["timeouts"] += 1
            res = {"errs": ["timeout (200 s)"]}
        if res["errs"]:
            out["fail"] += 1
            out["failures"].append({"run": label, "errors": res["errs"]})
        else:
            out["pass"] += 1
        print(label, "OK" if not res["errs"] else res["errs"], res.get("links", ""), flush=True)
    json.dump(out, open(os.path.join(HERE, "tools", "jashan_apptest_results.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("runs", "pass", "fail", "timeouts")}))

if __name__ == "__main__":
    main()
