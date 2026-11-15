"""Static HTML previews of the main pages (for headless-browser screenshots; no Streamlit server needed).

Runs the app with AppTest at a fixed moment, collects the HTML that the page passes to st.html (theme CSS,
cards, grids) and the Markdown, and writes tools/preview/<page>.html. Streamlit's own widgets are not drawn; the
live compass is replaced by its static markup (face_light_live.markup).
Usage: python tools/render_previews.py [ISO-moment] [calendar] [place-key]
"""
from __future__ import annotations

import html
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from streamlit.testing.v1 import AppTest  # noqa: E402

import face_light_live  # noqa: E402
import places  # noqa: E402
import sky_layer as sl  # noqa: E402

OUT = os.path.join(HERE, "preview")
os.makedirs(OUT, exist_ok=True)
moment = sys.argv[1] if len(sys.argv) > 1 else "2026-11-15T17:30:00+05:30"
cal = sys.argv[2] if len(sys.argv) > 2 else "shahanshahi"
pk = sys.argv[3] if len(sys.argv) > 3 else "mumbai"
pl = dict(places.PRESETS_BY_KEY[pk], label=places.preset_label(places.PRESETS_BY_KEY[pk]))

PAGE_CSS = """<style>body{margin:0;background:#0e1420;color:#f5eedf;font-family:'Segoe UI',sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:18px 22px}.block-container{padding-top:0!important}
.fake-radio{display:flex;flex-wrap:wrap;gap:.3rem .9rem;margin:.3rem 0 .6rem;font-size:.92rem}
.fake-radio span{border:1px solid rgba(236,197,102,.5);border-radius:14px;padding:.15rem .6rem}
.fake-radio span.on{background:#2c4e9e;color:#fff;border-color:#ecc566}
.md h1,.md h2,.md h3{font-family:'Palatino Linotype',Georgia,serif;color:#ecc566}.md table{border-collapse:collapse}
.md td,.md th{border-bottom:1px solid rgba(168,121,42,.4);padding:4px 6px;text-align:left}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}</style>"""


def build(page: str, width_cols: int = 3) -> str:
    at = AppTest.from_file(os.path.join(ROOT, "app.py"), default_timeout=180)
    at.session_state["place"] = dict(pl)
    at.session_state["place_src"] = "manual"
    at.session_state["_now_override"] = moment
    at.run()
    if at.session_state["cal"] != cal:
        at.radio(key="cal").set_value(cal).run()
    at.radio(key="page").set_value(page).run()
    assert not at.exception, [e.message for e in at.exception]
    cal_opts = at.radio(key="cal").options
    page_opts = at.radio(key="page").options
    head, body = [], []
    for el in at.get("html"):
        h = el.proto.body
        (head if h.lstrip().startswith("<style>") else body).append(h)
    sel_c = [o for o in cal_opts]
    cur_c = sel_c[[k for k in ["shahanshahi", "kadmi", "fasli", "bastani", "sasanian"]].index(cal)]
    radios = ("<div class='fake-radio'>" + "".join(f"<span class='{'on' if o == cur_c else ''}'>{html.escape(o)}</span>"
                                                 for o in cal_opts) + "</div>"
              "<div class='fake-radio'>" + "".join(
                  f"<span class='{'on' if o.startswith(page if page != 'How' else 'How') else ''}'>{html.escape(o)}</span>"
                  for o in page_opts) + "</div>")
    body.insert(1, radios)
    if page == "Today":
        place = at.session_state["place"]
        now = datetime.fromisoformat(moment)
        ftl = sl.face_the_light(now, place)
        body.insert(len(body) - 1, face_light_live.markup(ftl, place["label"], place["lat"], place["lon"], "Face the light")[0])
    if page == "Year":   # Streamlit columns are not in the HTML list: lay the month cards out in a grid
        cards = [b for b in body if b.startswith("<div class='gs-card'><h3>") and "gs-mini" in b]
        rest = [b for b in body if b not in cards]
        body = rest[:-2] + ["<div class='cols'>" + "".join(cards) + "</div>"] + rest[-2:]
    md = "".join(f"<div class='md'>{_md(m.value)}</div>" for m in at.markdown)
    build.blocks = {"head": PAGE_CSS + "".join(head), "blocks": body[:-1] + ([md] if md else []) + body[-1:]}
    return ("<!doctype html><html><head><meta charset='utf-8'>" + PAGE_CSS + "".join(head) + "</head><body>"
            "<div class='wrap stApp'>" + "".join(body[:-1]) + md + body[-1] + "</div></body></html>")


def _md(t: str) -> str:
    try:
        import markdown   # optional
        return markdown.markdown(t, extensions=["tables"])
    except Exception:
        return "<pre style='white-space:pre-wrap'>" + html.escape(t) + "</pre>"


if __name__ == "__main__":
    pages = sys.argv[4].split(",") if len(sys.argv) > 4 else ["Today", "Month", "Year", "Gahs", "Compare", "Traditions"]
    for pg in pages:
        fn = os.path.join(OUT, f"{pg.lower()}_{cal}_{pk}.html")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(build(pg))
        import json
        with open(fn[:-5] + ".blocks.json", "w", encoding="utf-8") as f:
            json.dump(build.blocks, f, ensure_ascii=False)
        print(fn)
