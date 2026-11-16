"""Colours, fonts and ornament for a theme drawn from Achaemenid art (Persia, 6th-4th centuries BCE).

Palette: the glazed-brick friezes of Susa (the 'Archers' and the winged-disc panels: turquoise, ochre-yellow,
white and brown glazes), lapis lazuli, the gold of the Oxus Treasure, and the grey limestone and polished dark
'black' stone of Persepolis. The ground is a night sky over dark stone. Ornaments (Faravahar, Persepolis
rosette, lotus-and-bud frieze, bull and griffin capitals, fire altar, Gah icons, Moon): see ornaments.py.

Every text colour has at least 7:1 contrast (WCAG AAA) on its background (computed, sRGB relative luminance):
  text colour            BG     CARD  SIDEBAR  GATHA_BG JASHAN_BG GAHAMBAR_BG  HOVER  TODAY_ROW
  TEXT   #f5eedf       16.0    14.0    15.1     12.2     12.7      13.2       11.1    10.3
  MUTED  #d9d0bf       12.0    10.6    11.4      9.2      9.6      10.0        8.4     7.8
  GOLD   #ecc566       11.2     9.8    10.6      8.6      8.9       9.3        7.8     7.3
  LINK   #a9d6f5       12.0    10.5    11.3      9.2      9.5       9.9        8.3     7.8
  OBS    #9fe5d6       12.9    11.3    12.2      9.9     10.3      10.6        9.0     8.3
  chips (INK #0e1420 on pastel): new_year 12.2, gahambar 11.5, jashan 11.7, gatha 12.5, memorial 12.0,
     birth 13.5, fire 11.5, moon 12.7, civil 14.0, reconstruction 13.2
  INK on GOLD 11.2; white on LAPIS (buttons) 7.8; white on LAPIS_HOVER 9.9; white on TURQ_DEEP 7.3;
  white on TODAY_ROW 11.9.  Lowest of all: 7.3:1.
FORCE_CSS sets both the text and the background colour of every Streamlit surface, so these pairs hold
whether the browser, the phone or Streamlit's own menu is in light or dark mode.
"""
import base64
import html
import os

import streamlit as st

import names as _names
import ornaments as orn

HERE = os.path.dirname(os.path.abspath(__file__))

BG = "#0e1420"          # night over Persepolis black stone
CARD = "#18212f"        # dark stone panel
SIDEBAR = "#121a27"
GATHA_BG = "#0c3033"    # deep turquoise glaze: the five Gatha (epagomenal) days
JASHAN_BG = "#1b2550"   # deep lapis: jashan days (day name = month name)
GAHAMBAR_BG = "#2e2410"  # deep ochre: the Gahambar seasonal feasts
HOVER = "#25324a"
TODAY_ROW = "#26365a"
TEXT = "#f5eedf"        # limestone ivory
MUTED = "#d9d0bf"
GOLD = "#ecc566"        # Oxus gold
LINK = "#a9d6f5"        # pale lapis
OBS = "#9fe5d6"         # pale turquoise glaze: astronomical / observed values
INK = "#0e1420"         # dark ink for chips
GOLD_DEEP = orn.GOLD_DEEP
TURQUOISE = orn.TURQUOISE
OCHRE = orn.OCHRE
LAPIS = orn.LAPIS       # buttons (white text 7.8:1)
LAPIS_HOVER = "#233f86"
TURQ_DEEP = "#11615e"   # carries white text (7.3:1)
CARNELIAN = orn.CARNELIAN

# Festival kinds: dark ink on pastel chips.
CHIP = {
    "new_year": "#f0cf72", "gahambar": "#e9c88f", "jashan": "#bccff4", "gatha": "#a6e0da",
    "memorial": "#cdd0d9", "birth": "#c6e6b6", "fire": "#f4c3a0", "moon": "#d8d2f2", "civil": "#e9e0c9",
    "recon": "#e4d9c2",
}
KIND_LABEL = {
    "new_year": "New Year", "gahambar": "Gahambar (seasonal feast)", "jashan": "Jashan (name-day feast)",
    "gatha": "Gatha days / Muktad", "memorial": "Remembrance", "birth": "Birth of Zarathushtra",
    "fire": "Fire festival", "moon": "Mah Niyayesh (Moon prayer)", "civil": "Civil calendar",
    "recon": "Reconstruction",
}
KIND_FA = {
    "new_year": "نوروز", "gahambar": "گاهنبار", "jashan": "جشن", "gatha": "گاتها", "memorial": "یادبود",
    "birth": "زادروز", "fire": "جشن آتش", "moon": "ماه نیایش", "civil": "گاه‌شماری رسمی", "recon": "بازسازی",
}
# Festival key (shared contract) -> chip kind.
FESTIVAL_KIND = {
    "navroz": "new_year", "pateti": "new_year", "jamshedi_navroz": "new_year",
    "khordad_sal": "birth", "zarthost_no_diso": "memorial", "muktad": "gatha", "farvardigan": "memorial",
    **{k: "gahambar" for k in ("gahambar_maidyozarem", "gahambar_maidyoshahem", "gahambar_paitishahem",
                               "gahambar_ayathrem", "gahambar_maidyarem", "gahambar_hamaspathmaedem")},
    **{f"jashan_{m}": "jashan" for m in ("fravardin", "ardibehesht", "khordad", "tir", "amardad", "shehrevar",
                                         "meher", "avan", "adar", "dae", "bahman", "aspandarmad")},
    "sadeh": "fire", "chaharshanbe_suri": "fire", "mah_niyayesh": "moon",
    "rapithwin_jashan": "jashan", "tirgan_civil": "civil",   # extra engine keys
}
# Default calendar labels for the badge (the names module may pass its own). Gujarati: Parsi usage for the
# three Parsi calendars; 'Bastani' and 'Sasanian' in Gujarati are transliterations.
# Calendar labels come from names.CALENDAR, the canonical display source (app assembly, Nov 2026; the theme
# track's own labels differed for Kadmi, Fasli Gujarati, Bastani and Sasanian Gujarati).
CAL_LABEL = {k: dict(v) for k, v in _names.CALENDAR.items()}
RECONSTRUCTED = {"sasanian"}

# Title. Avestan: gāhšumār letter by letter (GE AA HE SHE U ME AA RE), a modern Pazand-style transliteration
# of New Persian gāh-šomār, not an attested Avestan word.
TITLE_EN = "Sky Gahshomar"
TITLE_AE = "\U00010B14\U00010B01\U00010B35\U00010B31\U00010B0E\U00010B28\U00010B01\U00010B2D"
TITLE_FA = "گاه‌شمار آسمان"
TITLE_GU = "ગાહશુમાર"
SUBTITLE = "the Zoroastrian calendars, Shahanshahi, Kadmi, Fasli and Bastani, from NASA JPL astronomy"

FONTS = (   # family, file in assets/fonts, weight, unicode-range
    ("GahAvestan", "NotoSansAvestan-Regular-sub.woff2", 400, "U+10B00-10B3F, U+2E31, U+200C-200F"),
    ("GahPersian", "Vazirmatn-Regular-sub.woff2", 400,
     "U+0600-06FF, U+200C-200F, U+FB50-FDFF, U+FE70-FEFF, U+00AB, U+00BB"),
    ("GahPersian", "Vazirmatn-Bold-sub.woff2", 700,
     "U+0600-06FF, U+200C-200F, U+FB50-FDFF, U+FE70-FEFF, U+00AB, U+00BB"),
    ("GahGujarati", "NotoSansGujarati-Regular-sub.woff2", 400, "U+0A80-0AFF, U+0964-0965, U+200C-200D, U+25CC"),
    ("GahGujarati", "NotoSansGujarati-Bold-sub.woff2", 700, "U+0A80-0AFF, U+0964-0965, U+200C-200D, U+25CC"),
)


def _font_face() -> str:
    """Embed the subset fonts (assets/fonts, about 78 kB of woff2) as data URIs. If a file is missing, the
    stacks below fall back to the system's fonts for that script."""
    out = []
    for family, fname, weight, urange in FONTS:
        path = os.path.join(HERE, "assets", "fonts", fname)
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
        except OSError:
            continue
        out.append(f"@font-face {{ font-family: '{family}'; src: url(data:font/woff2;base64,{b64}) format('woff2'); "
                   f"font-weight: {weight}; font-style: normal; font-display: swap; unicode-range: {urange}; }}")
    return "\n".join(out)


ROSETTE_BAND = orn.data_uri(orn.rosette_band_tile_svg())
LOTUS_BAND = orn.data_uri(orn.lotus_frieze_tile_svg())
ROSETTE = orn.data_uri(orn.rosette_svg(40))
ROSETTE_INK = orn.data_uri(orn.rosette_svg(40, petal=INK, center=TURQUOISE, ring=INK))
CAPITAL_BULL = orn.data_uri(orn.capital_svg(124, "bull"))
CAPITAL_GRIFFIN = orn.data_uri(orn.capital_svg(124, "griffin"))
FIRE = orn.data_uri(orn.fire_altar_svg(40))

SERIF = "'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, 'Times New Roman', serif"
PERSIAN = "'GahPersian', 'Vazirmatn', 'Noto Naskh Arabic', 'Segoe UI', 'Tahoma', sans-serif"
GUJARATI = "'GahGujarati', 'Noto Sans Gujarati', 'Nirmala UI', 'Shruti', sans-serif"
AVESTAN = "'GahAvestan', 'Noto Sans Avestan', 'Segoe UI Historic', sans-serif"

CSS = f"""
<style>
{_font_face()}
.block-container, [data-testid="stMainBlockContainer"] {{ padding-top: 4.6rem; }}
[data-testid="stAppViewContainer"] {{ background:
   radial-gradient(ellipse at 50% -10%, rgba(44,78,158,.36), rgba(0,0,0,0) 58%), {BG}; }}
[data-testid="stSidebar"] {{ background: {SIDEBAR}; border-right: 1px solid rgba(236,197,102,.30); }}
h1, h2, h3, h4 {{ font-family: {SERIF}; color: {GOLD}; }}
.gs-head {{ display:flex; align-items:center; gap: 14px; margin: .4rem 0 .2rem 0; }}
.gs-head img {{ flex: 0 0 auto; }}
.gs-title {{ font-family: {SERIF}; font-size: 2.05rem; font-weight: 700; color: {GOLD}; line-height:1.15; }}
.gs-title .gs-ae {{ font-size: 1.7rem; margin-left: .45rem; }}
.gs-title .gs-fa {{ font-size: 1.5rem; font-weight: 700; margin-left: .35rem; }}
.gs-title .gs-gu {{ font-size: 1.25rem; margin-left: .35rem; }}
.gs-sub {{ color: {MUTED}; margin-bottom: 0.4rem; font-size: .95rem; }}
.gs-frieze {{ height: 34px; background-image: url("{ROSETTE_BAND}"); background-repeat: repeat-x;
             background-size: auto 34px; margin: .25rem 0 .7rem 0; }}
.gs-lotus {{ height: 34px; background-image: url("{LOTUS_BAND}"); background-repeat: repeat-x;
            background-size: auto 34px; margin: .4rem 0 .6rem 0; }}
.gs-divider {{ display: flex; align-items: center; gap: .6rem; margin: .8rem 0; }}
.gs-divider::before, .gs-divider::after {{ content: ""; flex: 1 1 auto; height: 5px;
   border-top: 2px solid {GOLD}; border-bottom: 1px solid {GOLD}; }}
.gs-divider img {{ flex: 0 0 auto; height: 38px; width: auto; }}
/* the three scripts. Persian and Avestan are right-to-left; each run is isolated so that the
   'English · Persian · Gujarati' order holds inside left-to-right text */
.gs-fa {{ font-family: {PERSIAN}; direction: rtl; unicode-bidi: isolate; color: {GOLD}; line-height: 1.5; }}
.gs-gu {{ font-family: {GUJARATI}; unicode-bidi: isolate; color: {TEXT}; line-height: 1.5; }}
.gs-ae {{ font-family: {AVESTAN}; direction: rtl; unicode-bidi: isolate; color: {GOLD}; font-size: 1.15em;
         line-height: 1.4; }}
.gs-sep {{ color: {MUTED}; padding: 0 .25em; }}
.gs-names {{ color: {TEXT}; }}
.gs-card {{ background: {CARD}; border: 1px solid {GOLD_DEEP}; outline: 1px solid rgba(236,197,102,.35);
           outline-offset: -5px; border-radius: 4px; padding: .95rem 1.15rem; margin-bottom: .8rem; color: {TEXT}; }}
.gs-card h3 {{ font-family: {SERIF}; color: {GOLD}; margin: 0 0 .4rem 0; font-size: 1.08rem; font-weight: 700;
              padding-left: 27px; background: url("{ROSETTE}") no-repeat left center; background-size: 19px 19px; }}
.gs-big {{ font-family: {SERIF}; font-size: 1.55rem; font-weight: 700; color: {TEXT}; line-height: 1.25; }}
.gs-big .gs-fa {{ font-size: 1.3rem; }} .gs-big .gs-ae {{ font-size: 1.45rem; }}
.gs-muted {{ color: {MUTED}; font-size: .92rem; }}
.gs-obs {{ color: {OBS}; }}
.gs-grid {{ width: 100%; border-collapse: separate; border-spacing: 4px; table-layout: fixed; }}
.gs-grid th {{ font-family: {SERIF}; color: {GOLD}; font-weight: 700; font-size: .9rem; padding: 2px 4px; text-align: left;
              border-bottom: 2px solid {GOLD_DEEP}; }}
.gs-grid td {{ background: {CARD}; border-radius: 3px; vertical-align: top; padding: 5px 6px;
              height: 108px; color: {TEXT}; border: 1px solid rgba(168,121,42,.55); }}
.gs-grid td.gs-empty {{ background: transparent; border: none; }}
.gs-grid td.gs-gatha {{ background: {GATHA_BG}; border-color: rgba(86,199,192,.85); }}
.gs-grid td.gs-jashan {{ background: {JASHAN_BG}; box-shadow: inset 0 3px 0 rgba(236,197,102,.75); }}
.gs-grid td.gs-gahambar {{ background: {GAHAMBAR_BG}; border-color: rgba(212,154,54,.9); }}
.gs-grid td.gs-today {{ border: 2px solid {GOLD}; }}
.gs-roj {{ font-weight: 700; font-size: 1.05rem; color: {TEXT}; }}
.gs-civ {{ float: right; text-align: right; font-size: .78rem; color: {MUTED}; }}
.gs-dayname {{ display: block; font-size: .8rem; color: {TEXT}; margin-top: 1px; }}
.gs-dayname .gs-ae {{ font-size: .95rem; }}
.gs-other {{ font-size: .74rem; color: {OBS}; display: block; margin-top: 1px; }}
.gs-chip {{ display: inline-block; color: {INK}; border-radius: 3px; padding: 1px 6px; margin: 2px 2px 0 0;
           font-size: .76rem; font-weight: 600; line-height: 1.45; border: 1px solid rgba(14,20,32,.35); }}
.gs-chip .gs-fa, .gs-chip .gs-gu, .gs-chip .gs-ae {{ color: {INK}; font-weight: 600; font-size: .95rem; line-height: 1.2; }}
.gs-chip .gs-sep {{ color: {INK}; }}
.gs-chip img {{ width: 13px; height: 13px; vertical-align: -2px; margin-right: 3px; }}
.gs-line {{ font-size: .76rem; color: {MUTED}; display: block; margin-top: 2px; }}
.gs-line b {{ color: {TEXT}; }}
.gs-list {{ width: 100%; border-collapse: collapse; }}
.gs-list td {{ border-bottom: 1px solid rgba(168,121,42,.45); padding: 7px 4px; vertical-align: top; color: {TEXT}; }}
.gs-list td.gs-gatha {{ background: {GATHA_BG}; }}
.gs-list td.gs-jashan {{ background: {JASHAN_BG}; }}
.gs-list td.gs-gahambar {{ background: {GAHAMBAR_BG}; }}
.gs-list td.gs-today {{ outline: 2px solid {GOLD}; }}
.gs-legend span {{ margin-right: 6px; }}
.gs-table {{ width: 100%; border-collapse: collapse; font-size: .93rem; }}
.gs-table th {{ font-family: {SERIF}; color: {GOLD}; text-align: left; border-bottom: 2px solid {GOLD_DEEP}; padding: 5px 6px; }}
.gs-table td {{ color: {TEXT}; border-bottom: 1px solid rgba(168,121,42,.40); padding: 5px 6px; vertical-align: top; }}
.gs-table td.gs-diff {{ color: {GOLD}; font-weight: 700; }}
/* calendar badge; the reconstructed (Sasanian) calendar is marked with a dashed border and a label */
.gs-cal {{ display: inline-flex; align-items: center; gap: .4rem; background: {CARD}; color: {TEXT};
          border: 1px solid {GOLD}; border-radius: 999px; padding: .12rem .7rem .12rem .45rem;
          font-family: {SERIF}; font-size: .9rem; font-weight: 700; vertical-align: middle; }}
.gs-cal::before {{ content: ""; width: 15px; height: 15px; background: url("{ROSETTE}") no-repeat center;
                  background-size: 15px 15px; }}
.gs-cal .gs-fa, .gs-cal .gs-gu {{ font-weight: 400; }}
.gs-cal.gs-recon {{ border-style: dashed; }}
.gs-recon-tag {{ display: inline-block; background: {CHIP['recon']}; color: {INK}; border-radius: 3px;
                padding: 0 5px; font-size: .74rem; font-weight: 700; margin-left: .2rem; }}
/* the five Gahs of the day */
.gs-gahs {{ display: flex; flex-wrap: wrap; gap: .4rem; margin: .3rem 0 .6rem 0; }}
.gs-gah {{ display: flex; align-items: center; gap: .4rem; background: {CARD}; color: {TEXT};
          border: 1px solid rgba(168,121,42,.55); border-radius: 6px; padding: .3rem .55rem; font-size: .88rem; }}
.gs-gah img {{ width: 26px; height: 26px; }}
.gs-gah b {{ color: {GOLD}; }}
.gs-gah small {{ color: {MUTED}; display: block; }}
.gs-gah.gs-now {{ border: 2px solid {GOLD}; background: {HOVER}; }}
.gs-pop {{ display: inline-block; position: relative; vertical-align: top; }}
.gs-pop > summary {{ list-style: none; cursor: pointer; display: inline; }}
.gs-pop > summary::-webkit-details-marker {{ display: none; }}
.gs-pop > summary .gs-chip {{ text-decoration: underline dotted rgba(14,20,32,.6); text-underline-offset: 2px; }}
.gs-pop[open] > summary .gs-chip {{ outline: 2px solid {GOLD}; }}
.gs-popbody {{ position: absolute; z-index: 1000; left: 0; top: calc(100% + 4px); width: 340px; max-width: 80vw;
              background: {CARD}; color: {TEXT}; border: 1px solid {GOLD}; border-radius: 6px; padding: .7rem .85rem;
              box-shadow: 0 8px 24px rgba(0,0,0,.65); font-size: .86rem; line-height: 1.45; text-align: left;
              white-space: normal; font-weight: 400; }}
.gs-pop-r .gs-popbody {{ left: auto; right: 0; }}
.gs-pop-title {{ font-family: {SERIF}; color: {GOLD}; font-weight: 700; font-size: 1rem; margin-bottom: .3rem; }}
.gs-pop-text {{ color: {TEXT}; }}
.gs-pop-src {{ color: {MUTED}; font-size: .78rem; margin-top: .45rem; font-style: italic; }}
.gs-scroll {{ overflow-x: auto; -webkit-overflow-scrolling: touch; max-height: 70vh; overflow-y: auto;
              border: 1px solid {GOLD_DEEP}; border-radius: 6px; background: {CARD}; }}
.gs-times {{ width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; white-space: nowrap; }}
.gs-times th {{ position: sticky; top: 0; background: {SIDEBAR}; color: {GOLD}; z-index: 1; }}
.gs-times th, .gs-times td {{ padding: .3rem .55rem; text-align: left; border-bottom: 1px solid rgba(236,197,102,.18); color: {TEXT}; }}
.gs-times tr.gs-today-row td {{ background: {TODAY_ROW}; color: #ffffff; font-weight: 700; }}
.gs-moon, .gs-icon {{ display: inline-block; vertical-align: middle; line-height: 0; }}
.gs-fa-i {{ font-family: {PERSIAN}; direction: rtl; unicode-bidi: isolate; color: {GOLD}; font-weight: 400; }}
.gs-pop-title .gs-fa-i {{ font-size: .95em; margin-left: .3em; }}
.gs-sect {{ background: {CARD}; border: 1px solid rgba(168,121,42,.55); border-radius: 6px; padding: .7rem .9rem; margin: .5rem 0; color: {TEXT}; }}
.gs-sect h4 {{ margin: 0 0 .25rem 0; font-size: 1.05rem; }}
.gs-sect p {{ margin: .25rem 0; font-size: .92rem; }}
.gs-src {{ color: {MUTED}; font-size: .8rem; font-style: italic; }}
.gs-diagram {{ width: 100%; max-width: 980px; height: auto; display: block; margin: .4rem 0; }}
.gs-mini {{ width: 100%; border-collapse: separate; border-spacing: 2px; table-layout: fixed; font-size: .76rem; }}
.gs-mini td {{ background: {CARD}; color: {TEXT}; text-align: center; padding: 2px 1px; border-radius: 2px; border: 1px solid rgba(168,121,42,.35); }}
.gs-mini td small {{ display: block; color: {MUTED}; font-size: .68rem; }}
.gs-mini td.gs-gatha {{ background: {GATHA_BG}; }} .gs-mini td.gs-jashan {{ background: {JASHAN_BG}; }}
.gs-mini td.gs-gahambar {{ background: {GAHAMBAR_BG}; }} .gs-mini td.gs-today {{ outline: 2px solid {GOLD}; }}
.gs-note {{ background: {CARD}; border-left: 3px solid {GOLD}; padding: .45rem .7rem; margin: .4rem 0; color: {TEXT}; font-size: .9rem; }}
.gs-moonrow {{ display: flex; flex-wrap: wrap; gap: .3rem .9rem; align-items: center; }}
.gs-moonrow span.gs-ph {{ display: inline-flex; align-items: center; gap: .3rem; }}
.gs-mdnav {{ font-family: {SERIF}; color: {GOLD}; font-size: 1.15rem; font-weight: 700; margin: .3rem 0; }}
.gs-times td.gs-polar {{ color: {OBS}; }}
.gs-grid td {{ overflow: hidden; overflow-wrap: anywhere; }}
.gs-grid .gs-dayname {{ line-height: 1.3; }}
.gs-grid .gs-dayname .gs-ae {{ font-size: .9rem; overflow-wrap: anywhere; }}
a {{ color: {LINK}; }}
.gs-pr {{ color: {LINK}; text-decoration: underline dotted; text-underline-offset: 3px; }}
.gs-pr:hover {{ color: {GOLD}; }}
.gs-prline {{ margin: .25rem 0; font-size: .92rem; line-height: 1.6; }}
@media (pointer: coarse) {{
  .gs-grid td {{ height: auto; min-height: 80px; }}
  div[data-testid="stRadio"] label {{ padding: 6px 4px; }}
  button {{ min-height: 44px; }}
}}
@media (max-width: 640px) {{
  .gs-popbody {{ position: static; width: auto; max-width: none; margin-top: 4px; }}
  .gs-title {{ font-size: 1.5rem; }} .gs-title .gs-ae {{ font-size: 1.3rem; }} .gs-title .gs-fa {{ font-size: 1.2rem; }}
  .gs-title .gs-gu {{ display: none; }}
  .gs-big {{ font-size: 1.28rem; }}
  .gs-head img {{ width: 64px; height: auto; }}
  .gs-grid td {{ padding: 3px 3px; }}
}}
</style>
"""

# The location button (locator.py: use as its component CSS). All three class prefixes are styled, so the
# button looks right whether the component's JavaScript names its elements gs-loc-*, tq-loc-* or sl-loc-*.
_PIN = orn.data_uri(orn.rosette_svg(32, petal=GOLD, center="#ffffff", ring=GOLD))
LOCATOR_CSS = f"""
.gs-loc, .tq-loc, .sl-loc {{ display:flex; flex-wrap:wrap; align-items:center; gap:.5rem .8rem; margin:.1rem 0 .5rem 0;
          font-family: {SERIF}; }}
.gs-loc-btn, .tq-loc-btn, .sl-loc-btn {{ background:{LAPIS}; color:#ffffff; border:1px solid {GOLD}; border-radius:6px;
              padding:.35rem .8rem .35rem 2rem; font-weight:700; font-size:.92rem; cursor:pointer; min-height:36px;
              background-image:url("{_PIN}"); background-repeat:no-repeat; background-position:.55rem center;
              background-size:16px 16px; }}
.gs-loc-btn:hover, .tq-loc-btn:hover, .sl-loc-btn:hover {{ background-color:{LAPIS_HOVER}; }}
.gs-loc-btn:focus-visible, .tq-loc-btn:focus-visible, .sl-loc-btn:focus-visible {{ outline:2px solid {GOLD}; outline-offset:2px; }}
.gs-loc-place, .tq-loc-place, .sl-loc-place {{ color:{TEXT}; font-size:.95rem; }}
.gs-loc-status, .tq-loc-status, .sl-loc-status {{ color:{MUTED}; font-size:.88rem; }}
.gs-loc-status a, .tq-loc-status a, .sl-loc-status a {{ color:{LINK}; }}
@media (pointer: coarse) {{ .gs-loc-btn, .tq-loc-btn, .sl-loc-btn {{ min-height:44px; }} }}
"""

# The live 'Face the light' compass (face_light_live.py). Written page-wide by apply() as well, because a
# component's own css= was not applied on Streamlit Community Cloud (Sky Taqwim, qibla_live.py).
COMPASS_CSS = f"""
.gs-ql {{ display: flex; flex-wrap: wrap; gap: 1rem; align-items: flex-start; }}
.gs-ql-wrap {{ position: relative; padding-top: 14px; flex: 0 0 auto; }}
.gs-ql-lubber {{ position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: 0; height: 0;
                border-left: 9px solid transparent; border-right: 9px solid transparent; border-top: 13px solid {CARNELIAN}; }}
.gs-ql-stage {{ position: relative; border-radius: 50%; transition: box-shadow .25s; }}
.gs-ql-stage.gs-ql-on {{ box-shadow: 0 0 0 4px {OBS}, 0 0 18px 4px rgba(159,229,214,.55); }}
.gs-ql-dial, .gs-ql-arrow {{ position: absolute; inset: 0; will-change: transform; transform-origin: 50% 50%; }}
.gs-ql-dial svg, .gs-ql-arrow svg {{ width: 100% !important; height: 100% !important; max-width: none !important; display: block; }}
.gs-ql-info {{ flex: 1 1 13rem; min-width: 12rem; color: {TEXT}; }}
.gs-ql-deg {{ font-family: {SERIF}; font-size: 1.35rem; font-weight: 700; color: {GOLD}; }}
.gs-ql-text {{ color: {TEXT}; font-size: .92rem; margin-top: .2rem; }}
.gs-ql-btn {{ display: none; margin-top: .55rem; background: {LAPIS}; color: #ffffff; border: 1px solid {GOLD};
             border-radius: 6px; padding: .45rem .9rem; font: 700 .95rem {SERIF}; min-height: 44px; cursor: pointer; }}
.gs-ql-btn:focus-visible {{ outline: 2px solid {GOLD}; outline-offset: 2px; }}
.gs-ql-status {{ margin-top: .45rem; color: {TEXT}; font-size: .95rem; font-weight: 600; min-height: 1.3em; }}
.gs-ql-status.gs-ql-good {{ color: {OBS}; }}
.gs-ql-status.gs-ql-warn {{ color: {GOLD}; }}
.gs-ql-tab {{ display: none; margin-top: .4rem; color: {LINK}; font-size: .92rem; }}
"""


# Streamlit's own widgets, text and menus. These rules set the colours directly, so the app reads the same
# (ivory and gold on night stone) whether the browser, the phone or Streamlit's menu is in light or dark mode,
# and even if .streamlit/config.toml is missing. Every pair here is at least 7:1 (WCAG AAA).
FORCE_CSS = f"""
<style>
:root {{ color-scheme: dark; }}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stBottom"] > div {{ color: {TEXT}; }}
.stApp {{ background-color: {BG}; }}
[data-testid="stHeader"] {{ background: rgba(14,20,32,.92); color: {TEXT}; }}
[data-testid="stHeader"] button, [data-testid="stHeader"] a, [data-testid="stToolbar"] *,
[data-testid="stSidebarCollapseButton"] *, [data-testid="stExpandSidebarButton"] *, [data-testid="stSidebarCollapsedControl"] * {{
  color: {TEXT} !important; fill: currentColor; }}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {{ background-color: {SIDEBAR} !important; color: {TEXT}; }}
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
[data-testid="stText"], [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p, label, legend,
[data-testid="stRadio"] label, [data-testid="stRadio"] p, [data-testid="stCheckbox"] p, [data-testid="stToggle"] p,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] p {{ color: {TEXT} !important; }}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p, .stCaption, small,
[data-testid="stWidgetLabel"] [data-testid="stTooltipIcon"] {{ color: {MUTED} !important; }}
[data-testid="stMarkdownContainer"] a, [data-testid="stCaptionContainer"] a {{ color: {LINK} !important; }}
[data-testid="stMarkdownContainer"] code {{ background: {CARD}; color: {GOLD}; }}
h1, h2, h3, h4, h5, h6, [data-testid="stHeading"] * {{ color: {GOLD} !important; }}
/* text boxes, number boxes, select boxes and their menus */
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"], [data-baseweb="select"] > div,
[data-testid="stNumberInputContainer"], [data-testid="stDateInput"] [data-baseweb="input"] {{
  background-color: {CARD} !important; border-color: rgba(236,197,102,.55) !important; color: {TEXT} !important; }}
[data-baseweb="input"] input, [data-baseweb="base-input"] input, textarea, [data-baseweb="select"] input,
[data-baseweb="select"] div, [data-baseweb="select"] span {{ color: {TEXT} !important; -webkit-text-fill-color: {TEXT}; background-color: transparent; }}
input::placeholder, textarea::placeholder {{ color: {MUTED} !important; -webkit-text-fill-color: {MUTED}; opacity: 1; }}
[data-baseweb="select"] svg, [data-testid="stNumberInputContainer"] svg {{ color: {TEXT} !important; fill: currentColor; }}
[data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"] {{ background: {CARD} !important; color: {TEXT} !important; }}
[data-baseweb="popover"] > div, [data-baseweb="popover"] ul, [data-baseweb="menu"], [role="listbox"] {{
  background-color: {CARD} !important; color: {TEXT} !important; border-color: {GOLD_DEEP} !important; }}
[data-baseweb="popover"] li, [role="option"] {{ color: {TEXT} !important; background-color: {CARD}; }}
[data-baseweb="popover"] li:hover, [role="option"]:hover, [role="option"][aria-selected="true"] {{ background-color: {HOVER} !important; }}
[data-baseweb="tag"] {{ background-color: {LAPIS} !important; color: #ffffff !important; }}
[data-baseweb="tag"] * {{ color: #ffffff !important; }}
[data-baseweb="calendar"], [data-baseweb="calendar"] * {{ background-color: {CARD}; color: {TEXT}; }}
[data-baseweb="tooltip"], [data-baseweb="tooltip"] * {{ background-color: {CARD} !important; color: {TEXT} !important; }}
/* buttons */
[data-testid^="stBaseButton-secondary"], [data-testid="stDownloadButton"] button, .stButton > button {{
  background-color: {CARD} !important; color: {TEXT} !important; border: 1px solid {GOLD} !important; }}
[data-testid^="stBaseButton-secondary"]:hover, [data-testid="stDownloadButton"] button:hover, .stButton > button:hover {{
  background-color: {HOVER} !important; color: #ffffff !important; }}
[data-testid^="stBaseButton-primary"] {{ background-color: {LAPIS} !important; color: #ffffff !important; border: 1px solid {GOLD} !important; }}
[data-testid^="stBaseButton-primary"]:hover {{ background-color: {LAPIS_HOVER} !important; }}
[data-testid^="stBaseButton"] p {{ color: inherit !important; }}
/* radio dots, check boxes and toggles stay visible on the dark ground */
[data-testid="stRadio"] [role="radio"] > div:first-child, [data-baseweb="radio"] > div:first-child {{ border-color: {GOLD} !important; }}
[data-baseweb="checkbox"] [role="checkbox"], [data-baseweb="checkbox"] > div:first-child {{ border-color: {GOLD} !important; }}
/* expanders, tabs, alerts, tables */
[data-testid="stExpander"] details, [data-testid="stExpander"] > details {{ background-color: {CARD} !important;
  border-color: rgba(236,197,102,.45) !important; color: {TEXT} !important; }}
[data-testid="stExpander"] summary, [data-testid="stExpander"] summary * {{ color: {GOLD} !important; background-color: transparent; }}
[data-testid="stExpander"] summary:hover {{ background-color: {HOVER} !important; }}
[data-baseweb="tab"], [data-baseweb="tab"] p {{ color: {TEXT} !important; }}
[data-baseweb="tab"][aria-selected="true"], [data-baseweb="tab"][aria-selected="true"] p {{ color: {GOLD} !important; }}
[data-testid="stAlertContainer"], [data-testid="stAlert"] > div {{ background-color: {CARD} !important; color: {TEXT} !important;
  border: 1px solid {GOLD_DEEP}; }}
[data-testid="stAlertContainer"] *, [data-testid="stAlert"] * {{ color: {TEXT} !important; }}
[data-testid="stTable"] table, [data-testid="stTable"] th, [data-testid="stTable"] td {{ color: {TEXT} !important;
  background-color: {CARD} !important; border-color: rgba(236,197,102,.3) !important; }}
[data-testid="stTable"] th {{ color: {GOLD} !important; }}
[data-testid="stSpinner"], [data-testid="stSpinner"] * {{ color: {TEXT} !important; }}
[data-testid="stToast"] {{ background-color: {CARD} !important; color: {TEXT} !important; }}
hr {{ border-color: rgba(236,197,102,.35) !important; }}
</style>
"""


def apply():
    st.html(CSS)
    st.html(FORCE_CSS)
    # the components' stylesheet, page-wide as well (a component's own css= was not applied on Streamlit Cloud)
    st.html("<style>" + COMPASS_CSS + LOCATOR_CSS + "</style>")


# --------------------------------------------------------------------------------------------- text helpers
def fa(text: str) -> str:
    return f"<span class='gs-fa' lang='fa' dir='rtl'>{html.escape(text)}</span>" if text else ""


def gu(text: str) -> str:
    return f"<span class='gs-gu' lang='gu'>{html.escape(text)}</span>" if text else ""


def ae(text: str) -> str:
    return f"<span class='gs-ae' lang='ae' dir='rtl'>{html.escape(text)}</span>" if text else ""


SEP = "<span class='gs-sep' aria-hidden='true'>·</span>"


def names_html(entry: dict, with_ae: bool = False, sep: str = SEP) -> str:
    """'English · Persian · Gujarati' for a name-table entry ({en, fa, gu[, ae]}); with_ae=True adds the
    Avestan script after the Gujarati (for roj and gatha day names)."""
    parts = [f"<span class='gs-en'>{html.escape(entry.get('en', ''))}</span>" if entry.get("en") else "",
             fa(entry.get("fa", "")), gu(entry.get("gu", ""))]
    if with_ae:
        parts.append(ae(entry.get("ae", "")))
    return f"<span class='gs-names'>{sep.join(p for p in parts if p)}</span>"


def calendar_badge(key: str, label: dict | None = None) -> str:
    """A badge naming the calendar in use. The reconstructed Sasanian calendar gets a dashed border and a
    'reconstruction' tag."""
    lab = label or CAL_LABEL.get(key, CAL_LABEL["shahanshahi"])
    rec = key in RECONSTRUCTED
    cls = "gs-cal gs-recon" if rec else "gs-cal"
    tag = "<span class='gs-recon-tag'>reconstruction</span>" if rec else ""
    title = ("A reconstruction for comparison, not a calendar in use" if rec
             else "Days, months and festivals follow this calendar")
    return (f"<span class='{cls} gs-cal-{html.escape(key)}' title='{title}'>{html.escape(lab.get('en', key))} "
            f"{fa(lab.get('fa', ''))} {gu(lab.get('gu', ''))}{tag}</span>")


def header(subtitle: str = "", calendar: str | None = None):
    emblem = orn.data_uri(orn.faravahar_svg(120))
    sub = html.escape(subtitle or SUBTITLE)
    badge = f" {calendar_badge(calendar)}" if calendar else ""
    st.html(f"<div class='gs-head'><img src='{emblem}' width='120' height='59' alt='Faravahar'>"
            f"<div><div class='gs-title'>{TITLE_EN} "
            f"<span class='gs-ae' lang='ae' dir='rtl' title='gāhšumār in Avestan letters'>{TITLE_AE}</span> "
            f"<span class='gs-fa' lang='fa' dir='rtl' title='Gāh-shomār-e āsmān: the calendar of the sky'>{TITLE_FA}</span> "
            f"<span class='gs-gu' lang='gu'>{TITLE_GU}</span>"
            f"</div><div class='gs-sub'>{sub}{badge}</div></div></div>"
            f"<div class='gs-frieze' role='presentation'></div>")


def chip(kind: str, text: str, fa_text: str = "", gu_text: str = "", icon: bool = False) -> str:
    """A festival chip (dark ink on a pastel colour of its kind). icon=True puts the fire altar in front."""
    inner = (f"<img src='{FIRE}' alt=''>" if icon else "") + html.escape(text)
    if fa_text:
        inner += SEP + fa(fa_text)
    if gu_text:
        inner += SEP + gu(gu_text)
    return f"<span class='gs-chip gs-chip-{html.escape(kind)}' style='background:{CHIP.get(kind, CHIP['civil'])}'>{inner}</span>"


def festival_chip(festival_key: str, entry: dict, icon: bool = False) -> str:
    """A chip for a festival from the shared contract, coloured by FESTIVAL_KIND."""
    return chip(FESTIVAL_KIND.get(festival_key, "civil"), entry.get("en", festival_key), entry.get("fa", ""),
                entry.get("gu", ""), icon)


def legend(kinds=None) -> str:
    ks = [k for k in KIND_LABEL if kinds is None or k in kinds]
    return "<div class='gs-legend'>" + "".join(chip(k, KIND_LABEL[k], KIND_FA.get(k, "")) for k in ks) + "</div>"


def moon(illum: float, waxing: bool, size: int = 22, tilt: float = 0.0) -> str:
    # a data-URI <img>: st.html strips inline <svg> (app assembly fix; the theme track returned inline SVG)
    alt = f"Moon {illum * 100:.0f}% lit, {'waxing' if waxing else 'waning'}"
    return f"<span class='gs-moon'>{_img(orn.moon_phase_svg(illum, waxing, size, tilt), size, alt)}</span>"


def _img(svg: str, size: int, alt: str = "") -> str:
    return f"<img class='gs-icon' src='{orn.data_uri(svg)}' width='{size}' height='{size}' alt='{html.escape(alt)}'>"


def moon_glyph(phase: str, size: int = 22) -> str:
    """'new', 'first_quarter', 'full' or 'last_quarter' as an <img> (for Mah Niyayesh days)."""
    return _img(orn.moon_glyph_svg(phase, size), size, f"{phase.replace('_', ' ')} Moon")


def gah_icon(key: str, size: int = 26) -> str:
    return _img(orn.gah_icon_svg(key, size), size, key)


def fire_icon(size: int = 18) -> str:
    return _img(orn.fire_altar_svg(size), size, "fire altar")


def gah_strip(gahs, now_key: str | None = None) -> str:
    """The Gahs of the day as a row of boxes. gahs: iterable of (key, name_entry, start_text, end_text);
    now_key marks the current Gah."""
    out = []
    for key, entry, start, end in gahs:
        cls = "gs-gah gs-now" if key == now_key else "gs-gah"
        out.append(f"<div class='{cls}'>{gah_icon(key)}<div><b>{html.escape(entry.get('en', key))}</b> "
                   f"{fa(entry.get('fa', ''))}<small>{html.escape(start)} – {html.escape(end)}</small></div></div>")
    return "<div class='gs-gahs'>" + "".join(out) + "</div>"


def divider(kind: str = "bull") -> str:
    src = CAPITAL_GRIFFIN if kind == "griffin" else CAPITAL_BULL
    return f"<div class='gs-divider' role='presentation'><img src='{src}' alt=''></div>"


def lotus_frieze() -> str:
    return "<div class='gs-lotus' role='presentation'></div>"
