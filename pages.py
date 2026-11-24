"""The pages of Sky Gahshomar: Today, Month, Year, Gahs, Festivals, Compare, Traditions, How it works, About.

Every page except Compare shows only the calendar chosen in the settings; the Gregorian civil date is the
reference of every grid. All HTML goes through st.html (SVG as data-URI <img>, tables as HTML, never
st.dataframe). Names: names.py through the znames shim, shown 'English · Persian · Gujarati' (+ Avestan for
roj and Gatha day names).
"""
from __future__ import annotations

import html
import json
import os
from datetime import date, datetime, timedelta

import streamlit as st

import device
import face_light_live
import festival_history as fh
import festivals as F
import gahs as G
import jashans as JS
import prayers as PR
import iran_solar as irs
import names
import ornaments as orn
import sects
import sky_layer as sl
import theme
import zcalendars as zc
import znames as zn

HERE = os.path.dirname(os.path.abspath(__file__))
esc = html.escape
CALS = list(zc.CALENDARS)
FIRST, LAST = date(1850, 1, 2), date(2149, 12, 30)
WEEK = [6, 0, 1, 2, 3, 4, 5]          # Sunday first (theme mock-up), Python weekday numbers
IRAN_ONLY = {"sadeh", "chaharshanbe_suri", "tirgan_civil"} | JS.iran_only_keys()
MULTI = {"muktad"} | {k for k in theme.FESTIVAL_KIND if k.startswith("gahambar_")}

# Popular civil-calendar dates beside the Bastani-calendar jashans (decision 6). Only variants with a source.
CIVIL_VARIANTS = {
    "jashan_tir": ("Tirgan is kept on 13 Tir in Iran's official calendar (the 'Tirgan, civil 13 Tir' entry).",
                   "surfiran.com, 'Iranian Festivals Calendar 2026/2027'"),
    "jashan_aspandarmad": ("Sepandarmazgan is also widely kept on 5 Esfand of the civil calendar.",
                           "Persian Wikipedia, 'سپندارمذگان' (retrieved 24 Nov 2026)"),
    "jashan_meher": ("Some people still mark the older date, 16 Mehr (Meher being the 16th roj).",
                     "livingintehran.com, 'Mehregan' (10 Nov 2026); surfiran.com, 'Iranian Festivals Calendar 2026/2027'"),
}
SETTING_KEYS = ("muktad", "jamshedi", "sadeh", "rapithwin", "era", "andargah", "intercalation", "kabisa_phase",
                "bastani_rule", "havan_meher", "iran_civil")


# ---------------------------------------------------------------------------------------------- small helpers
def cal_label(k: str) -> str:
    e = names.CALENDAR[k]
    return f"{e['en']} · {e['fa']} · {e['gu']}"


def fa(t):
    return theme.fa(t)


def gu(t):
    return theme.gu(t)


def hm(t) -> str:
    return t.strftime("%H:%M") if t else "–"


def copts(ctx, cal: str) -> dict:
    s = ctx["s"]
    if cal == "sasanian":
        return {"andargah": s["andargah"], "intercalation": s["intercalation"], "kabisa_phase": int(s["kabisa_phase"])}
    if cal == "bastani":
        return {"rule": s["bastani_rule"]}
    return {}


def fkw(ctx, cal: str) -> dict:
    s = ctx["s"]
    return dict(muktad=s["muktad"], jamshedi=s["jamshedi"], sadeh=s["sadeh"], **copts(ctx, cal))


def zdate(ctx, d: date, cal: str | None = None):
    cal = cal or ctx["cal"]
    return zc.to_zdate(d, cal, **copts(ctx, cal))


def roj_entry(z) -> dict:
    return (zn.GATHA if z.is_gatha else zn.ROJ)[z.roj_key]


def cell_names(entry: dict) -> str:
    """Day names stacked for a narrow grid cell: English / Persian · Gujarati / Avestan, with a line-break
    opportunity after each Avestan word separator (U+2E31) so that long names wrap inside the cell."""
    ae = entry.get("ae") or ""
    ae_html = ""
    if ae:
        ae_html = ("<br><span class='gs-ae' lang='ae' dir='rtl'>"
                   + esc(ae).replace("\u2e31", "\u2e31<wbr>") + "</span>")
    return (f"<span class='gs-dayname'><span class='gs-en'>{esc(entry.get('en', ''))}</span><br>"
            f"{fa(entry.get('fa', ''))}{theme.SEP}{gu(entry.get('gu', ''))}{ae_html}</span>")


def mah_entry(z) -> dict | None:
    return zn.MAH[z.mah_key] if z.mah_key else None


def mah_title(mah: int, repeated: bool = False) -> str:
    if mah == zc.GATHA_MAH:
        return "Gatha days " + fa(theme.KIND_FA["gatha"])
    e = zn.MAH[zn.MAH_KEYS[mah - 1]]
    return theme.names_html(e) + (" <span class='gs-recon-tag'>repeated month (hypothetical)</span>" if repeated else "")


def era_html(z, era: str, short: bool = False) -> str:
    e = z.eras
    want = {"yz": ["YZ"], "zre": ["ZRE"], "yz+zre": ["YZ", "ZRE"]}.get(era, ["YZ"])
    parts = []
    for k in want:
        if k not in e:
            continue
        n = e[k]
        if k == "YZ":
            E = names.ERA["yz"]
            parts.append(f"{E['abbr_en']} {n}" + ("" if short else f" {fa(names.fa_num(n) + ' ' + E['abbr_fa'])} "
                                                   f"{gu(E['abbr_gu'] + ' ' + names.gu_num(n))}"))
        else:
            E = names.ERA["zre"]
            parts.append(f"ZRE {n}" + ("" if short else f" {fa(names.fa_num(n) + ' ' + E['abbr_fa'])}"))
    if not parts:   # e.g. ZRE asked for a calendar that has only YZ
        n = e.get("YZ", z.year)
        parts.append(f"Y.Z. {n}" + ("" if short else " <span class='gs-muted'>(ZRE is not defined for this calendar)</span>"))
    if "SH" in e and not short:
        parts.append(f"<span class='gs-muted'>Iranian civil year SH {e['SH']}</span>")
    return " · ".join(parts)


CUR_CAL = {"cal": None}     # set by app.py before a page is drawn (Iranian feast names in the Bastani view)


def fentry(key: str) -> dict:
    """Display names of a festival key, including the extra jashan days of jashans.py."""
    if key in JS.EXTRA:
        e = JS.EXTRA[key]
        return {"en": e["en"], "fa": e["fa"], "gu": e["gu"]}
    entry = dict(zn.FESTIVAL.get(key, {"en": key}))
    if CUR_CAL["cal"] == "bastani" and key in JS.IRAN:
        entry["en"] = JS.IRAN[key][0]
        entry["fa"] = JS.IRAN[key][1]
    return entry


def fname(key: str) -> str:
    return fentry(key)["en"]


def jnote(key: str) -> str:
    """The first sentence of what a jashan day commemorates, as a small line under its chip."""
    if key not in JS.NOTE:
        return ""
    t = JS.NOTE[key][0]
    cut = t.find(". ")
    return f"<div class='gs-jnote'>{esc(t[:cut + 1] if 0 < cut < 170 else t)}</div>"


def fchip(key: str, align_right: bool = False) -> str:
    entry = fentry(key)
    kind = theme.FESTIVAL_KIND.get(key, "civil")
    return fh.clickable(key, theme.festival_chip(key, entry, icon=(kind == "fire")), align_right)


def card(title: str, body: str) -> str:
    return f"<div class='gs-card'><h3>{title}</h3>{body}</div>"


def prayer_link(key: str, all_links: bool = False) -> str:
    """A prayer name that opens its text (avesta.org) in a new tab."""
    pr = PR.PRAYERS[key]
    links = pr["links"] if all_links else pr["links"][:1]
    if not all_links:
        return (f"<a class='gs-pr' href='{esc(links[0][1])}' target='_blank' title='{esc(pr['when'])}'>"
                f"{esc(pr['en'])}</a>")
    return " · ".join(f"<a class='gs-pr' href='{esc(u)}' target='_blank'>{esc(lab)}</a>" for lab, u in links)


def prayer_line(keys, label: str = "Read") -> str:
    keys = [k for k in keys if k in PR.PRAYERS]
    if not keys:
        return ""
    return (f"<div class='gs-prline'><span class='gs-muted'>{esc(label)}:</span> "
            + " <span class='gs-sep'>·</span> ".join(prayer_link(k) for k in keys) + " <span class='gs-muted'>↗</span></div>")


def place_tuple(place: dict) -> tuple:
    return (round(float(place["lat"]), 5), round(float(place["lon"]), 5), place["tz"],
            float(place.get("elev", 0.0) or 0.0), place.get("name", ""))


def place_of(t: tuple) -> dict:
    return {"lat": t[0], "lon": t[1], "tz": t[2], "elev": t[3], "name": t[4]}


# ---------------------------------------------------------------------------------------------- cached computations
@st.cache_data(max_entries=256, show_spinner=False)
def _fest_between(start: date, end: date, cal: str, kw: tuple) -> list:
    return F.festivals_between(start, end, cal, **dict(kw))


@st.cache_data(max_entries=64, show_spinner=False)
def _fest_year(year: int, cal: str, kw: tuple) -> list:
    return F.festivals_in_year(year, cal, **dict(kw))


def _keep(ctx, cal, f) -> bool:
    return not (f.key in IRAN_ONLY and cal != "bastani" and not ctx["s"]["iran_civil"])


def fests_between(ctx, start, end, cal=None) -> list:
    cal = cal or ctx["cal"]
    return [f for f in _fest_between(start, end, cal, tuple(sorted(fkw(ctx, cal).items()))) if _keep(ctx, cal, f)]


def fests_year(ctx, year, cal=None) -> list:
    cal = cal or ctx["cal"]
    return [f for f in _fest_year(year, cal, tuple(sorted(fkw(ctx, cal).items()))) if _keep(ctx, cal, f)]


@st.cache_data(max_entries=2048, show_spinner=False)
def _gah_day(d: date, pt: tuple, cal: str, practice: str, havan_meher: bool, opts: tuple) -> dict:
    g = sl.gahs(d, place_of(pt), cal, havan_meher=havan_meher, rapithwin=practice, **dict(opts))
    return {"gahs": [(x.key, x.start, x.end, x.note) for x in g["gahs"]], "polar": g["polar"],
            "season": g["rapithwin_season"], "sun": g["sun"]}


def gah_day(ctx, d: date) -> dict:
    s, cal = ctx["s"], ctx["cal"]
    return _gah_day(d, place_tuple(ctx["place"]), cal, s["rapithwin"], bool(s["havan_meher"]),
                    tuple(sorted(copts(ctx, cal).items())))


@st.cache_data(max_entries=64, show_spinner=False)
def _phases(start: date, end: date, tz: str) -> list:
    start, end = max(start, FIRST), min(end, LAST)      # the DE440s span
    return sl.moon_phases(start, end, tz) if start <= end else []


def moon_by_day(start: date, end: date, tz: str) -> dict:
    out = {}
    for p in _phases(start, end, tz):
        out.setdefault(p["local"].date(), []).append(p)
    return out


PHASE_GLYPH = {0: "new", 1: "first_quarter", 2: "full", 3: "last_quarter"}


def phase_line(p: dict, size: int = 14) -> str:
    mn = " · Mah Niyayesh" if p["mah_niyayesh"] else ""
    return (f"<span class='gs-line'>{theme.moon_glyph(PHASE_GLYPH[p['phase']], size)} {esc(p['name'])} "
            f"<b>{p['local']:%H:%M}</b>{mn}</span>")


def range_ok(d: date) -> bool:
    return FIRST <= d <= LAST


def month_of(ctx, d: date, cal: str | None = None):
    """(year, index, (mah, repeated, start, ndays), layout) of the Zoroastrian month containing civil date d."""
    cal = cal or ctx["cal"]
    o = copts(ctx, cal)
    y = zc.year_containing(d, cal, **o)
    lay = zc.months_of_year(y, cal, **o)
    for i, (m, rep, start, n) in enumerate(lay):
        if start <= d < start + timedelta(days=n):
            return y, i, (m, rep, start, n), lay
    return y, 0, lay[0], lay


def year_bounds(ctx, cal: str) -> tuple[int, int]:
    o = copts(ctx, cal)
    return zc.year_containing(FIRST, cal, **o) + 1, zc.year_containing(LAST, cal, **o) - 1


def cell_class(z, flist) -> list[str]:
    cls = []
    if z.is_gatha:
        cls.append("gs-gatha")
    if any(f.key.startswith("gahambar_") and f.key != "gahambar_hamaspathmaedem" for f in flist):
        cls.append("gs-gahambar")
    if any(f.key.startswith("jashan_") and f.days == 1 for f in flist):
        cls.append("gs-jashan")
    return cls


def by_day(flist, start: date, end: date) -> dict:
    out = {}
    for f in flist:
        d = max(f.start, start)
        while d <= min(f.end, end):
            out.setdefault(d, []).append(f)
            d += timedelta(days=1)
    return out


def sasanian_note(cal: str) -> str:
    if cal != "sasanian":
        return ""
    return ("<div class='gs-note'>The Sasanian calendar is a <b>reconstruction</b> for comparison (late Sasanian and "
            "early Islamic arrangement after al-Biruni), not a calendar any community keeps. See How it works.</div>")


# ---------------------------------------------------------------------------------------------- Today
def render_today(ctx):
    cal, place, now = ctx["cal"], ctx["place"], ctx["now"]
    rd = zc.roj_civil_date(now, place)
    if not range_ok(rd):
        st.html(card("Today", "<p>This date is outside 1850–2149, the range of the JPL DE440s ephemeris.</p>"))
        return
    z = zdate(ctx, rd, cal)
    re_ = roj_entry(z)
    wd = names.WEEKDAY[now.weekday()]
    if z.is_gatha:
        ndays = zc.month_days(z.year, zc.GATHA_MAH, cal, **copts(ctx, cal))
        line = f"Gatha day {z.day} of {ndays} · {era_html(z, ctx['s']['era'])}"
    else:
        line = (f"Roj {z.day} " + fa(names.fa_num(z.day)) + " " + gu(names.gu_num(z.day)) + " of mah "
                + theme.names_html(mah_entry(z)) + (" <span class='gs-recon-tag'>repeated month</span>"
                                                    if z.repeated_month else "")
                + f" · {era_html(z, ctx['s']['era'])}")
    sunrise_note = ""
    if rd != now.date():
        sunrise_note = (f"<div class='gs-muted'>Before sunrise: the roj that began at sunrise on {rd:%a %d %b} is still "
                        f"running (the Zoroastrian day begins at sunrise; Ushahin Gah belongs to it).</div>")
    body = (f"<div class='gs-big'>{theme.names_html(re_, with_ae=True)}</div>"
            f"<div style='margin:.25rem 0'>{line}</div>"
            f"<div class='gs-muted'>{esc(wd['en'])} {fa(wd['fa'])} {gu(wd['gu'])} · {now:%d %B %Y}, {now:%H:%M} "
            f"at {esc(place.get('label', place['name']))} · {theme.calendar_badge(cal)}</div>"
            f"{sunrise_note}")
    if re_.get("meaning"):
        body += f"<div class='gs-muted'>{esc(re_['meaning'])}</div>"
    if z.is_gatha:
        body += prayer_line(PR.GATHA_DAY_PRAYERS.get(z.roj_key, []), "Gatha of the day")
    st.html(card("Today", body) + sasanian_note(cal))

    # --- Gahs
    g = gah_day(ctx, rd)
    cur = None
    for k, a, b, note in g["gahs"]:
        if a <= now < b:
            cur = (k, a, b, note)
    strip = theme.gah_strip([(k, zn.GAH[k], hm(a), hm(b)) for k, a, b, _ in g["gahs"]], now_key=cur[0] if cur else None)
    gb = strip
    if cur:
        info = G.GAHS.get(cur[0], {})
        gb = (f"<div class='gs-big' style='font-size:1.2rem'>Now: {theme.names_html(zn.GAH[cur[0]], with_ae=True)}</div>"
              f"<div class='gs-muted'>{hm(cur[1])} – {hm(cur[2])}{(' · ' + esc(cur[3])) if cur[3] else ''}</div>"
              f"<div>Presiding: {esc(info.get('presiding', ''))}. {esc(info.get('prayers', ''))}</div>"
              + prayer_line(PR.GAH_PRAYERS.get(cur[0], []), "Prayers of this Gah") + strip)
    if g["polar"]:
        gb += (f"<div class='gs-note'>Polar {esc(g['polar'])}: the Sun does not {'set' if g['polar'] == 'day' else 'rise'} "
               "here today, so sunrise and sunset are taken as true noon − 6 h and + 6 h (an app convention).</div>")
    gb += ("<div class='gs-muted'>Rapithwin season: " + ("yes" if g["season"] else "no (Second Havan" +
           (", or four watches under the Bundahishn rule" if ctx["s"]["rapithwin"] == "medieval_four" else "") + ")")
           + ". Times from JPL sunrise, true noon and sunset at your place.</div>")
    st.html(card("The Gahs of this roj", gb))

    # --- festivals
    fl = fests_between(ctx, rd, rd)
    fl = [f for f in fl if f.start <= rd <= f.end]
    if fl:
        rows = []
        for f in fl:
            k = (rd - f.start).days + 1
            extra = f" <span class='gs-muted'>day {k} of {f.days}</span>" if f.days > 1 else ""
            rows.append(f"<div style='margin:.2rem 0'>{fchip(f.key)}{extra} <span class='gs-muted'>{esc(f.note)}</span>"
                        f"{jnote(f.key)}{prayer_line(PR.FESTIVAL_PRAYERS.get(f.key, []))}</div>")
        fb = "".join(rows) + "<div class='gs-muted'>Click a jashan or festival for what it commemorates, its history and sources.</div>"
    else:
        fb = "<div class='gs-muted'>No festival on this roj.</div>"
    nxt = [f for f in fests_between(ctx, rd + timedelta(days=1), min(rd + timedelta(days=60), LAST))
           if f.start > rd][:4] if rd < LAST else []
    if nxt:
        fb += "<div style='margin-top:.4rem'><b>Coming:</b> " + " ".join(
            f"{fchip(f.key)} <span class='gs-muted'>{f.start:%d %b}</span>" for f in nxt) + "</div>"
    st.html(card("Festivals", fb))

    # --- Moon and face the light
    ftl = sl.face_the_light(now, place)
    ph = _phases(rd - timedelta(days=1), rd + timedelta(days=31), place["tz"])
    nxtp = [p for p in ph if p["local"] > now]
    waxing = bool(nxtp and nxtp[0]["phase"] in (1, 2))
    illum = float(ftl["moon"].get("illumination", 0.0))
    today_mn = [p for p in ph if p["local"].date() == now.date() and p["mah_niyayesh"]]
    mb = (f"<div class='gs-moonrow'>{theme.moon(illum, waxing, 46)}<div><b>{illum * 100:.0f}% lit</b>, "
          f"{'waxing' if waxing else 'waning'}; the Moon is {abs(ftl['moon']['alt']):.0f}° "
          f"{'above' if ftl['moon']['alt'] > 0 else 'below'} the horizon.</div></div>")
    if today_mn:
        p = today_mn[0]
        mb += (f"<div class='gs-note'>{fchip('mah_niyayesh')} Today is a Mah Niyayesh day: {esc(p['name'])} at "
               f"{p['local']:%H:%M} ({esc(p['avestan'])}).</div>")
    mb += "<div class='gs-moonrow' style='margin-top:.35rem'>" + "".join(
        f"<span class='gs-ph'>{theme.moon_glyph(PHASE_GLYPH[p['phase']], 18)} {esc(p['name'])} "
        f"{p['local']:%a %d %b %H:%M}{' · <b>Mah Niyayesh</b>' if p['mah_niyayesh'] else ''}</span>" for p in nxtp[:4]) + "</div>"
    mb += prayer_line(["mah_niyayesh"])
    mb += ("<div class='gs-muted'>The Mah Niyayesh names the Moon's stations: new moon (antarə.måŋha), full moon "
           "(pərənō.måŋha) and the half-moon (vīšaptaθa). Phases from JPL DE440s, in your time zone.</div>")
    st.html(card("Moon · " + theme.names_html(zn.FESTIVAL["mah_niyayesh"]), mb))
    title = "Face the light"
    try:
        face_light_live.show(ftl, place.get("label", place["name"]), place["lat"], place["lon"], title,
                             waxing=waxing)
    except Exception as exc:   # pragma: no cover - the static drawing is still useful
        st.html(face_light_live.markup(ftl, place.get("label", ""), place["lat"], place["lon"], title)[0])
        st.caption(f"Live compass unavailable: {exc}")


# ---------------------------------------------------------------------------------------------- Month
def _set_anchor(d: date):
    st.session_state["m_anchor"] = min(max(d, FIRST), LAST)


def _goto_changed(k):
    v = st.session_state.get(k)
    if isinstance(v, date):
        _set_anchor(v)


def render_month(ctx):
    cal, today = ctx["cal"], ctx["today"]
    if "m_anchor" not in st.session_state:
        st.session_state["m_anchor"] = min(max(today, FIRST), LAST)
    anchor = st.session_state["m_anchor"]
    y, i, (m, rep, start, n), lay = month_of(ctx, anchor)
    end = start + timedelta(days=n - 1)
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1.4]) if not device.phone() else (st.container(),) * 4
    c1.button("◀ Previous", key="m_prev", width="stretch", on_click=_set_anchor, args=(start - timedelta(days=1),))
    c2.button("This month", key="m_today", width="stretch", on_click=_set_anchor, args=(today,))
    c3.button("Next ▶", key="m_next", width="stretch", on_click=_set_anchor, args=(end + timedelta(days=1),))
    gk = f"m_goto_{anchor.isoformat()}"
    c4.date_input("Go to a date", value=anchor, min_value=FIRST, max_value=LAST, key=gk, format="DD/MM/YYYY",
                  label_visibility="collapsed", on_change=_goto_changed, args=(gk,))
    z0 = zdate(ctx, start)
    st.html(f"<div class='gs-mdnav'>{mah_title(m, rep)} · {era_html(z0, ctx['s']['era'], short=True)}</div>"
            f"<div class='gs-muted'>{theme.calendar_badge(cal)} {start:%a %d %b %Y} – {end:%a %d %b %Y} · {n} days</div>"
            + sasanian_note(cal))
    days = [start + timedelta(days=k) for k in range(n)]
    fl = fests_between(ctx, start, end)
    fday = by_day(fl, start, end)
    moon = moon_by_day(start, end, ctx["place"]["tz"])

    def lines(d, align_right=False):
        out = []
        for f in fday.get(d, []):
            if f.start == d or d == start:
                out.append(fchip(f.key, align_right))
            if f.days > 1:
                out.append(f"<span class='gs-line'>{esc(fname(f.key))}: day <b>{(d - f.start).days + 1}</b>"
                           f" of {f.days}</span>")
        for p in moon.get(d, []):
            out.append(phase_line(p))
        return "".join(out)

    if device.phone():
        rows = []
        for d in days:
            z = zdate(ctx, d)
            cls = " ".join(cell_class(z, fday.get(d, [])) + (["gs-today"] if d == today else []))
            rows.append(f"<tr><td class='{cls}' style='width:38%'><span class='gs-roj'>{z.day}</span> "
                        f"<span class='gs-muted'>{d:%a %d %b}</span><span class='gs-dayname'>"
                        f"{theme.names_html(roj_entry(z), with_ae=True)}</span></td><td class='{cls}'>{lines(d)}</td></tr>")
        st.html("<table class='gs-list'>" + "".join(rows) + "</table>")
    else:
        lead = WEEK.index(start.weekday())
        cells = ["<td class='gs-empty'></td>"] * lead
        for d in days:
            z = zdate(ctx, d)
            cls = cell_class(z, fday.get(d, [])) + (["gs-today"] if d == today else [])
            col = WEEK.index(d.weekday())
            cells.append(f"<td class='{' '.join(cls)}'><span class='gs-roj'>{z.day}</span>"
                         f"<span class='gs-civ'>{d.day} {d:%b}</span>"
                         f"{cell_names(roj_entry(z))}"
                         f"{lines(d, align_right=col >= 4)}</td>")
        while len(cells) % 7:
            cells.append("<td class='gs-empty'></td>")
        head = "".join(f"<th>{esc(names.WEEKDAY[w]['en'][:3])} {fa(names.WEEKDAY[w]['fa'])}</th>" for w in WEEK)
        rows = "".join("<tr>" + "".join(cells[k:k + 7]) + "</tr>" for k in range(0, len(cells), 7))
        st.html(f"<table class='gs-grid'><tr>{head}</tr>{rows}</table>")
    st.html(theme.legend() + "<div class='gs-muted'>Each cell is a civil (Gregorian) day; the large number is the roj "
            "of the month in the chosen calendar, the small date the civil date. A roj runs from sunrise to sunrise; "
            "the cell shows the roj whose daylight falls on that civil date.</div>")


# ---------------------------------------------------------------------------------------------- Year
def _year_picker(ctx, key: str, label: str = "Year") -> int:
    cal = ctx["cal"]
    lo, hi = year_bounds(ctx, cal)
    cur = zc.year_containing(min(max(ctx["today"], FIRST), LAST), cal, **copts(ctx, cal))
    cur = min(max(cur, lo), hi)
    k = f"{key}_{cal}"
    if k in st.session_state and not lo <= st.session_state[k] <= hi:
        del st.session_state[k]
    return int(st.number_input(f"{label} ({'ZRE' if cal == 'bastani' else 'YZ'})", lo, hi,
                               st.session_state.get(k, cur), 1, key=k))


def render_year(ctx):
    cal = ctx["cal"]
    y = _year_picker(ctx, "y_year")
    o = copts(ctx, cal)
    lay = zc.months_of_year(y, cal, **o)
    nz = zc.navroz(y, cal, **o)
    L = zc.year_length(y, cal, **o)
    z0 = zc.to_zdate(nz, cal, **o)
    st.html(f"<div class='gs-mdnav'>{theme.calendar_badge(cal)} {era_html(z0, ctx['s']['era'])}</div>"
            f"<div class='gs-muted'>Navroz {nz:%a %d %b %Y} · {L} days"
            + (" (leap year: Avardad-sal-gah added)" if L == 366 else "")
            + (f" · intercalated month (hypothetical model)" if L > 366 else "") + "</div>" + sasanian_note(cal))
    today = ctx["today"]
    fl = fests_year(ctx, y)
    end = nz + timedelta(days=L - 1)
    fday = by_day(fl, nz, end)
    cols_n = 1 if device.phone() else 3
    cols = st.columns(cols_n)
    for idx, (m, rep, start, n) in enumerate(lay):
        cells = []
        for k in range(n):
            d = start + timedelta(days=k)
            z = zc.to_zdate(d, cal, **o)
            cls = cell_class(z, fday.get(d, [])) + (["gs-today"] if d == today else [])
            cells.append(f"<td class='{' '.join(cls)}' title='{esc(roj_entry(z)['en'])}, {d:%d %b %Y}'>"
                         f"<b>{z.day}</b><small>{d.day}/{d.month}</small></td>")
        rows = "".join("<tr>" + "".join(cells[r:r + 10]) + "</tr>" for r in range(0, len(cells), 10))
        mf = [f for f in fl if start <= f.start < start + timedelta(days=n)]
        chips = " ".join(fchip(f.key, align_right=(idx % cols_n) == cols_n - 1) for f in mf)
        body = (f"<div class='gs-muted'>{start:%d %b %Y} – {(start + timedelta(days=n - 1)):%d %b %Y} · {n} days</div>"
                f"<table class='gs-mini'>{rows}</table><div style='margin-top:.3rem'>{chips}</div>")
        with cols[idx % cols_n]:
            st.html(card(mah_title(m, rep), body))
    st.html(theme.legend(["new_year", "gahambar", "jashan", "gatha", "memorial", "birth", "fire", "civil"]))


# ---------------------------------------------------------------------------------------------- Gahs
def render_gahs(ctx):
    cal, place, today = ctx["cal"], ctx["place"], ctx["today"]
    _, _, (m, rep, start0, n0), _ = month_of(ctx, min(max(today, FIRST), LAST))
    start0 = min(max(start0, FIRST), LAST - timedelta(days=40))
    c1, c2 = st.columns(2)
    start = c1.date_input("From", value=start0, min_value=FIRST, max_value=LAST - timedelta(days=40), key="g_from",
                          format="DD/MM/YYYY")
    ndays = int(c2.slider("Days", 7, 40, n0, key="g_days"))
    rows, polar_any = [], False
    nowk = ctx["now"]
    for k in range(ndays):
        d = start + timedelta(days=k)
        g = gah_day(ctx, d)
        z = zdate(ctx, d)
        gd = {key: (a, b) for key, a, b, _ in g["gahs"]}
        mid = "rapithwin" if "rapithwin" in gd else ("second_havan" if "second_havan" in gd else None)
        cls = " class='gs-today-row'" if d == today else ""
        polar = g["polar"]
        polar_any = polar_any or bool(polar)
        pc = " class='gs-polar'" if polar else ""
        rows.append(
            f"<tr{cls}><td>{d:%a %d %b}</td><td>{z.day} {esc(roj_entry(z)['en'])}</td>"
            f"<td{pc}>{hm(gd['havan'][0])}</td>"
            f"<td>{hm(gd[mid][0]) + ' ' + esc(names.GAH[mid]['en']) if mid else '— (Havan continues)'}</td>"
            f"<td>{hm(gd['uziran'][0])}</td><td{pc}>{hm(gd['aiwisruthrem'][0])}</td><td>{hm(gd['ushahin'][0])}</td>"
            f"<td{pc}>{hm(gd['ushahin'][1])}</td><td>{('polar ' + esc(polar)) if polar else ''}</td></tr>")
    head = ("<tr><th>Civil date</th><th>Roj</th><th>Havan (sunrise)</th><th>Rapithwin / Second Havan (noon)</th>"
            "<th>Uziran</th><th>Aiwisruthrem (sunset)</th><th>Ushahin (midnight)</th><th>next sunrise</th><th></th></tr>")
    st.html(f"<div class='gs-muted'>{theme.calendar_badge(cal)} Start of each Gah at {esc(place.get('label', place['name']))}"
            f" ({esc(place['tz'])}).</div><div class='gs-scroll'><table class='gs-times'>{head}{''.join(rows)}</table></div>")
    if polar_any:
        st.html("<div class='gs-note'>Rows marked 'polar': the Sun does not rise or set that day here; sunrise and "
                "sunset are taken as true noon − 6 h and + 6 h (an app convention, not a priestly ruling).</div>")
    # explainer
    trs = "".join(f"<tr><td>{theme.names_html(zn.GAH[k], with_ae=True)}</td><td>{esc(G.GAHS[k]['period'])}</td>"
                  f"<td>{esc(G.GAHS[k]['presiding'])}</td><td>{esc(G.GAHS[k]['prayers'])}{prayer_line(PR.GAH_PRAYERS.get(k, []))}</td>"
                  f"<td>{esc(G.GAHS[k]['note'])}<div class='gs-src'>{esc(G.GAHS[k]['src'])}</div></td></tr>"
                  for k in G.GAH_ORDER)
    st.html(card("The five Gahs",
                 f"<table class='gs-table'><tr><th>Gah</th><th>When</th><th>Presiding</th><th>Prayers</th><th>Note</th></tr>"
                 f"{trs}</table>"))
    st.caption("Prayer names are links: they open the Avestan text and English translation on avesta.org in a new tab. "
               "The Prayers page lists them all.")
    practice = ("Summer rule (Rapithwin from Fravardin to Meher mah, Second Havan otherwise)"
                if ctx["s"]["rapithwin"] == "summer" else "Bundahishn winter rule (four watches outside the Rapithwin season)")
    st.html(card("Rapithwin", f"<p><b>Setting:</b> {esc(practice)}.</p><p>{esc(G.RAPITHWIN)}</p>"
                              f"<div class='gs-src'>{esc(G.RAPITHWIN_SRC)}</div>"
                              f"<p>{esc(G.COMMUNITY_TIMES)}</p><div class='gs-src'>{esc(G.COMMUNITY_TIMES_SRC)}</div>"))


# ---------------------------------------------------------------------------------------------- Festivals
def zlabel(z) -> str:
    return f"{esc(roj_entry(z)['en'])} roj, " + (f"{esc(zn.MAH[z.mah_key]['en'])} mah" if z.mah_key else "Gatha")


def zspan(ctx, f) -> str:
    s = zlabel(f.zstart)
    if f.days > 1:
        s += " – " + zlabel(zdate(ctx, f.end, f.cal))
    return s


def render_festivals(ctx):
    cal = ctx["cal"]
    y = _year_picker(ctx, "f_year")
    fl = fests_year(ctx, y)
    rule = ctx["s"]["bastani_rule"]
    rows = []
    for f in fl:
        civ = f"{f.start:%a %d %b %Y}" + (f" – {f.end:%a %d %b %Y}" if f.days > 1 else "")
        extra = ""
        if cal == "bastani":
            sy, sm, sd = irs.to_civil(f.start, rule)
            extra = f"<td>{sd} {esc(irs.CIVIL_MONTHS[sm - 1][0])} {sy} {fa(names.fa_num(sd) + ' ' + irs.CIVIL_MONTHS[sm - 1][1])}"
            if f.key in CIVIL_VARIANTS:
                t, src = CIVIL_VARIANTS[f.key]
                extra += f"<div class='gs-muted'>{esc(t)}</div><div class='gs-src'>{esc(src)}</div>"
            extra += "</td>"
        rd_ = ' · '.join(prayer_link(k) for k in PR.FESTIVAL_PRAYERS.get(f.key, []))
        rows.append(f"<tr><td>{fchip(f.key)}{jnote(f.key)}</td><td>{zspan(ctx, f)}</td><td>{civ}</td><td>{f.days}</td>{extra}"
                    f"<td class='gs-muted'>{esc(f.note)}</td><td>{rd_}</td></tr>")
    head = ("<tr><th>Festival</th><th>Zoroastrian date</th><th>Civil date</th><th>Days</th>"
            + ("<th>Iranian civil date</th>" if cal == "bastani" else "") + "<th>Rule</th><th>Read ↗</th></tr>")
    z0 = zc.to_zdate(zc.navroz(y, cal, **copts(ctx, cal)), cal, **copts(ctx, cal))
    st.html(f"<div class='gs-mdnav'>{theme.calendar_badge(cal)} {era_html(z0, ctx['s']['era'])}</div>"
            + sasanian_note(cal) + f"<table class='gs-table'>{head}{''.join(rows)}</table>"
            "<div class='gs-muted'>Click a jashan or festival for what it commemorates, its history and sources.</div>")
    if cal != "bastani" and not ctx["s"]["iran_civil"]:
        st.caption("Sadeh, Chaharshanbe Suri and the civil Tirgan are Iranian observances: they are listed with the "
                   "Bastani calendar, or here if you switch on 'Show Iranian civil observances' in the settings.")
    # Mah Niyayesh days of the year
    nz = zc.navroz(y, cal, **copts(ctx, cal))
    L = zc.year_length(y, cal, **copts(ctx, cal))
    ph = [p for p in _phases(nz, nz + timedelta(days=L - 1), ctx["place"]["tz"]) if p["mah_niyayesh"]]
    st.html(card("Mah Niyayesh days (new and full moons)",
                 "<div class='gs-moonrow'>" + "".join(
                     f"<span class='gs-ph'>{theme.moon_glyph(PHASE_GLYPH[p['phase']], 16)} {p['local']:%d %b %Y %H:%M}</span>"
                     for p in ph) + "</div>" + f"<div class='gs-muted'>In {esc(ctx['place']['tz'])}. {fchip('mah_niyayesh')}</div>" + prayer_line(['mah_niyayesh'])))
    if cal in fh.CAL_H:
        t, src = fh.CAL_H[cal]
        st.html(card("About this calendar · " + theme.names_html(names.CALENDAR[cal]),
                     f"<p>{esc(t)}</p><div class='gs-src'>Sources: {esc(src)}</div>"))



# ---------------------------------------------------------------------------------------------- Prayers
def render_prayers(ctx):
    st.html(card("Prayers", "<p>The official prayers of the Khorda Avesta and the Gathas. Each name and link opens the "
                 "text on avesta.org in a new tab: the Avestan text with an English translation. The app links to "
                 "these pages and does not copy them.</p>"
                 + "<div class='gs-prline'><b>Whole books:</b> " + " <span class='gs-sep'>·</span> ".join(
                     f"<a class='gs-pr' href='{esc(u)}' target='_blank'>{esc(lab)}</a>" for lab, u in PR.BOOKS) + " ↗</div>"
                 + f"<div class='gs-src'>{esc(PR.SOURCE_NOTE)}</div>"))
    for gkey, gtitle in PR.GROUPS:
        rows = "".join(
            f"<tr><td>{prayer_link(k)}<div>{theme.fa(v['fa'])} {theme.gu(v['gu'])}</div></td>"
            f"<td>{esc(v['when'])}</td><td>{prayer_link(k, all_links=True)}</td></tr>"
            for k, v in PR.PRAYERS.items() if v["group"] == gkey)
        st.html(card(esc(gtitle), "<div class='gs-scroll'><table class='gs-table'><tr><th>Prayer</th><th>When</th>"
                     f"<th>Read ↗</th></tr>{rows}</table></div>"))
    st.caption("Which prayers belong to each Gah and festival follows the rubrics of the Khorda Avesta; for a name-day "
               "jashan the app links the Yasht or Niyayesh of that day's yazata (the Siroza where there is no separate "
               "Yasht). Families and priests may follow other customs.")

# ---------------------------------------------------------------------------------------------- Compare
COMPARE_KEYS = ["navroz", "jamshedi_navroz", "khordad_sal", "farvardigan", "gahambar_maidyozarem", "jashan_tir",
                "jashan_meher", "jashan_adar", "zarthost_no_diso", "gahambar_maidyarem", "muktad", "pateti"]


def render_compare(ctx):
    today = ctx["today"]
    d = st.date_input("Civil date to compare", value=min(max(today, FIRST), LAST), min_value=FIRST, max_value=LAST,
                      key="c_date", format="DD/MM/YYYY")
    zs = {c: zdate(ctx, d, c) for c in CALS}
    ref = zs["shahanshahi"]
    rows = []
    for c in CALS:
        z = zs[c]
        dr = " gs-diff" if z.roj_key != ref.roj_key else ""
        dm = " gs-diff" if (z.mah, z.repeated_month) != (ref.mah, ref.repeated_month) else ""
        fl = [f for f in fests_between(ctx, d, d, c) if f.start <= d <= f.end]
        mah = (theme.names_html(zn.MAH[z.mah_key]) if z.mah_key else "Gatha days") + (" (repeated)" if z.repeated_month else "")
        rows.append(f"<tr><td>{theme.calendar_badge(c)}</td><td class='{dr}'>{z.day} · {theme.names_html(roj_entry(z), with_ae=True)}</td>"
                    f"<td class='{dm}'>{mah}</td><td>{era_html(z, 'yz+zre', short=True)}</td><td>{z.day_of_year}</td>"
                    f"<td>{' '.join(fchip(f.key, True) for f in fl)}</td></tr>")
    st.html(f"<div class='gs-mdnav'>{d:%A %d %B %Y}</div><table class='gs-table'><tr><th>Calendar</th><th>Roj</th>"
            f"<th>Mah</th><th>Year</th><th>Day of year</th><th>Festivals</th></tr>{''.join(rows)}</table>"
            "<div class='gs-muted'>Gold cells differ from the Shahanshahi reckoning. The Sasanian calendar is a "
            "reconstruction for comparison only.</div>")
    # where they disagree: Navroz and key festivals in this civil year
    gy = d.year
    a, b = max(date(gy, 1, 1), FIRST), min(date(gy, 12, 31), LAST)
    per = {c: {} for c in CALS}
    for c in CALS:
        for f in fests_between(ctx, a, b, c):
            if a <= f.start <= b and f.key in COMPARE_KEYS:
                per[c].setdefault(f.key, []).append(f.start)
    trs = []
    for k in COMPARE_KEYS:
        vals = [", ".join(x.strftime("%d %b") for x in per[c].get(k, [])) or "–" for c in CALS]
        diff = len(set(vals)) > 1
        trs.append(f"<tr><td>{fchip(k)}</td>" + "".join(f"<td class='{'gs-diff' if diff else ''}'>{v}</td>" for v in vals) + "</tr>")
    head = "<tr><th>Festival (first day)</th>" + "".join(f"<th>{esc(names.CALENDAR[c]['en'])}</th>" for c in CALS) + "</tr>"
    st.html(card(f"Where they disagree in {gy}", f"<div class='gs-scroll' style='max-height:none'><table class='gs-table'>"
                 f"{head}{''.join(trs)}</table></div>"))
    # explanation
    nz = {c: [x for x in per[c].get("navroz", [])] for c in CALS}
    pts = []
    pts.append("Kadmi runs exactly 30 days ahead of Shahanshahi (a Kadmi date names the next month): the Parsis of "
               "India once intercalated a month that the Iranians did not.")
    if nz["fasli"] and nz["shahanshahi"]:
        off = (nz["shahanshahi"][0] - nz["fasli"][0]).days
        pts.append(f"Fasli keeps Navroz on 21 March with a Gregorian leap day; this year the Shahanshahi Navroz comes "
                   f"{off} days after it, and the gap grows by about one day every four years.")
    if nz["bastani"] and nz["fasli"]:
        off = (nz["bastani"][0] - nz["fasli"][0]).days
        pts.append("Bastani has the same structure as Fasli but begins at Iran's Nowruz (the day of the March equinox "
                   f"before true noon at 52.5° E): this year {abs(off)} day{'s' if abs(off) != 1 else ''} "
                   f"{'before' if off < 0 else 'after'} the Fasli Navroz" + (" (the same day)." if off == 0 else "."))
    pts.append("The Sasanian reconstruction counts its years like Kadmi but puts the five Gatha (andargāh) days after "
               "Avan mah (setting), so from Adar mah onward its dates stand five days apart from Kadmi's.")
    st.html(card("Why", "<ul>" + "".join(f"<li>{esc(p)}</li>" for p in pts) + "</ul>"))


# ---------------------------------------------------------------------------------------------- Traditions
def apply_preset(sect_key: str, i: int = 0):
    """Set calendar, Muktad, Rapithwin practice and era from a community preset (button/selectbox callback)."""
    p = sects.preset(sect_key, i)
    st.session_state["cal"] = p["calendar"]
    st.session_state["muktad"] = "parsi_18" if int(p.get("muktad_days", 10)) == 18 else "ten"
    st.session_state["rapithwin"] = p.get("rapithwin", "summer")
    st.session_state["era"] = p.get("era", "yz")
    st.session_state["sect"] = f"{sect_key}:{i}"
    st.session_state["rap_auto"] = False


def preset_options() -> list[str]:
    return [f"{s['key']}:{i}" for s in sects.SECTS for i in range(len(s["uses"]))]


def preset_label(opt: str) -> str:
    k, i = opt.split(":")
    s = next(x for x in sects.SECTS if x["key"] == k)
    return f"{s['name']} — {s['uses'][int(i)][1]}"


def _diagram_svg() -> str:
    D = sects.BRANCH_DIAGRAM
    nodes = D["nodes"]
    ys = sorted({n["y"] for n in nodes})
    row = {y: r for r, y in enumerate(ys)}
    W, bw, bh, top, rowh = 1000, 176, 46, 30, 66
    x0 = 80
    lanew = (W - x0 - 20) / 5
    pos = {}
    for n in nodes:
        cx = x0 + lanew * n["lane"] + lanew / 2
        cy = top + row[n["y"]] * rowh + bh / 2
        pos[n["id"]] = (cx, cy)
    H = top + len(ys) * rowh + 10
    font = ""
    try:
        import base64
        with open(os.path.join(HERE, "assets", "fonts", "Vazirmatn-Regular-sub.woff2"), "rb") as fh_:
            font = ("<style>@font-face{font-family:'GahPersian';src:url(data:font/woff2;base64,"
                    + base64.b64encode(fh_.read()).decode("ascii") + ") format('woff2');}</style>")
    except OSError:
        pass
    out = [f"<defs>{font}<marker id='ah' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='7' markerHeight='7' "
           f"orient='auto-start-reverse'><path d='M0,0 L10,5 L0,10 z' fill='{theme.GOLD}'/></marker></defs>",
           f"<rect width='{W}' height='{H}' fill='{theme.BG}'/>"]
    for y in ys:
        cy = top + row[y] * rowh + bh / 2 + 4
        out.append(f"<text x='8' y='{cy:.0f}' font-family='Georgia,serif' font-size='12' fill='{theme.MUTED}'>{y}</text>")
    dash = {"split": "", "adopt": "stroke-dasharray='7 5'", "migrate": "stroke-dasharray='2 4'"}
    for e in D["edges"]:
        (ax, ay), (bx, by) = pos[e["from"]], pos[e["to"]]
        down = by >= ay
        sy_, ty_ = (ay + bh / 2, by - bh / 2) if down else (ay - bh / 2, by + bh / 2)
        my = (sy_ + ty_) / 2
        out.append(f"<path d='M{ax:.1f},{sy_:.1f} C{ax:.1f},{my:.1f} {bx:.1f},{my:.1f} {bx:.1f},{ty_:.1f}' fill='none' "
                   f"stroke='{theme.GOLD}' stroke-opacity='.8' stroke-width='1.6' {dash.get(e['style'], '')} marker-end='url(#ah)'/>")
        lx, ly = (ax + bx) / 2, my
        lab = esc(e.get("label", ""))
        out.append(f"<text x='{lx:.1f}' y='{ly + 4:.1f}' text-anchor='middle' font-family='Segoe UI,Arial,sans-serif' "
                   f"font-size='10.5' fill='{theme.OBS}' stroke='{theme.BG}' stroke-width='3' paint-order='stroke'>{lab}</text>")
    for n in nodes:
        cx, cy = pos[n["id"]]
        kind = n.get("kind")
        stroke = theme.GOLD if kind == "living" else (theme.MUTED if kind == "historic" else theme.GOLD_DEEP)
        da = "stroke-dasharray='4 3'" if kind == "note" else ""
        out.append(f"<rect x='{cx - bw / 2:.1f}' y='{cy - bh / 2:.1f}' width='{bw}' height='{bh}' rx='5' fill='{theme.CARD}' "
                   f"stroke='{stroke}' stroke-width='1.6' {da}/>")
        out.append(f"<text x='{cx:.1f}' y='{cy - 6:.1f}' text-anchor='middle' font-family='Georgia,serif' font-size='12' "
                   f"font-weight='700' fill='{theme.TEXT}'>{esc(n['label'])}</text>")
        out.append(f"<text x='{cx:.1f}' y='{cy + 10:.1f}' text-anchor='middle' font-family='Segoe UI,Arial,sans-serif' "
                   f"font-size='10' fill='{theme.MUTED}'>{esc(n.get('when', ''))}</text>")
        out.append(f"<text x='{cx:.1f}' y='{cy + 21:.1f}' text-anchor='middle' direction='rtl' "
                   f"font-family='GahPersian,Vazirmatn,Tahoma,sans-serif' font-size='10' fill='{theme.GOLD}'>{esc(n.get('fa', ''))}</text>")
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}' role='img' "
            f"aria-label='Branch diagram of the Zoroastrian communities and their calendars'>{''.join(out)}</svg>")


def render_traditions(ctx):
    st.html(card("Communities and their calendars",
                 "<p>Each community below keeps its days by one or more of the calendars. 'Use' sets the app's "
                 "calendar, Muktad length, Rapithwin practice and era to model that practice. Practice varies inside "
                 "every community; the presets are models, and each note says whose practice it follows.</p>"
                 f"<p class='gs-muted'>{esc(sects.MUKTAD_NOTE)} The app's 18-day option follows the engine's rule "
                 "(Ashishvangh roj of Aspandarmad to Amardad roj of Fravardin; Karanjia).</p>"))
    svg = _diagram_svg()
    st.html(f"<img class='gs-diagram' src='{orn.data_uri(svg)}' alt='Branch diagram of the Zoroastrian communities'>"
            f"<div class='gs-muted'>{esc(sects.BRANCH_DIAGRAM['caption'])}</div>")
    cur = st.session_state.get("sect", "")
    for gi, (gen, gfa, ggu) in enumerate(sects.GROUPS):
        st.html(f"<h3>{esc(gen)} {fa(gfa)} {gu(ggu)}</h3>")
        for s in [x for x in sects.SECTS if x["group"] == gen]:
            since = f" · since {esc(s['since'])}" if s.get("since") else ""
            st.html(f"<div class='gs-sect'><h4>{esc(s['name'])} {fa(s.get('fa', ''))} {gu(s.get('gu', ''))}</h4>"
                    f"<p><b>Where:</b> {esc(s.get('where', ''))}{since}</p><p>{esc(s.get('how', ''))}</p>"
                    f"<div class='gs-src'>{esc(s.get('src', ''))}</div></div>")
            cols = st.columns(max(1, len(s["uses"])))
            for i, (c, lab, p) in enumerate(s["uses"]):
                on = cur == f"{s['key']}:{i}"
                cols[i].button(("✓ " if on else "Use: ") + f"{lab}", key=f"use_{s['key']}_{i}", width="stretch",
                               on_click=apply_preset, args=(s["key"], i), type="primary" if on else "secondary",
                               help=f"Calendar {names.CALENDAR[p['calendar']]['en']}, Muktad {p['muktad_days']} days, "
                                    f"Rapithwin '{p['rapithwin']}', era {p['era'].upper()}")
    if sects.HISTORICAL:
        st.html(card("Historical movements (notes only, no preset)", "".join(
            f"<div class='gs-sect'><h4>{esc(h['name'])} {fa(h.get('fa', ''))}</h4><p class='gs-muted'>{esc(h.get('period', ''))}</p>"
            f"<p>{esc(h.get('note', ''))}</p><div class='gs-src'>{esc(h.get('src', ''))}</div></div>" for h in sects.HISTORICAL)))


# ---------------------------------------------------------------------------------------------- How it works / About
def _md(path: str) -> str:
    try:
        with open(os.path.join(HERE, path), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return f"({path} is missing)"


def render_how(ctx):
    st.markdown(_md("HOW_IT_WORKS.md"))


def render_about(ctx):
    st.html(card("About Sky Gahshomar",
                 "<p>Sky Gahshomar is the Zoroastrian sibling of Sky Luach (Jewish) and Sky Taqwim (Islamic). "
                 "Astronomy: NASA JPL DE440s through Skyfield (1850–2149). Code: MIT License (see LICENSE), "
                 "© 2026 Gerad Smith, the same licence as the sibling apps. Third-party fonts, data and models keep "
                 "their own licences (THIRD_PARTY.md below).</p>"))
    try:
        with open(os.path.join(HERE, "validation", "results.json"), encoding="utf-8") as f:
            res = json.load(f)
        st.html(card("Validation", "<p>The engine's validation (validation/validate.py; docs/VALIDATION.md) was "
                     "re-run after the names were reconciled, with the same results. Summary of the checks:</p>"
                     f"<pre style='white-space:pre-wrap;color:{theme.TEXT};font-size:.8rem'>"
                     f"{esc(json.dumps(res, indent=1)[:3000])}</pre>"))
    except (OSError, ValueError):
        pass
    rows = "".join(f"<tr><td>{esc(t)}</td><td>{esc(str(k) if k else '')}</td><td>{esc(fld)}</td><td>{esc(why)}</td></tr>"
                   for (t, k, fld), why in sorted({**names.UNCERTAIN, **PR.UNCERTAIN, **JS.UNCERTAIN}.items(), key=lambda x: (str(x[0][0]), str(x[0][1]), x[0][2])))
    st.html(card(f"Uncertain spellings ({len(names.UNCERTAIN) + len(PR.UNCERTAIN) + len(JS.UNCERTAIN)})",
                 "<p>Forms the content track could not confirm in a source, or chose between variants:</p>"
                 f"<div class='gs-scroll'><table class='gs-table'><tr><th>Table</th><th>Key</th><th>Field</th><th>Why</th></tr>"
                 f"{rows}</table></div>"))
    srows = "".join(f"<tr><td>{esc(k)}</td><td>{esc(v)}</td></tr>" for k, v in names.SOURCES.items())
    st.html(card("Sources of the names", f"<table class='gs-table'>{srows}</table>"))
    with st.expander("Sources (SOURCES.md)"):
        st.markdown(_md(os.path.join("docs", "SOURCES.md")))
    with st.expander("Name reconciliation (engine vs content spellings)"):
        st.markdown(_md(os.path.join("docs", "NAMES_RECONCILIATION.md")))
    with st.expander("Licence (LICENSE)"):
        st.code(_md("LICENSE"), language=None)
    with st.expander("Third-party material (THIRD_PARTY.md)"):
        st.markdown(_md("THIRD_PARTY.md"))
