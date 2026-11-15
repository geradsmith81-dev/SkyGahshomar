"""Checks for the Sky Gahshomar content modules.  Run:  python check_content.py [fonts_dir] [titus_text]

fonts_dir  : folder with the Noto fonts (optional; skips the font-coverage check if absent)
titus_text : plain-text dump of TITUS avestt.htm (optional; skips the attestation check if absent)
"""
from __future__ import annotations

import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import festival_history as fh  # noqa: E402
import gahs  # noqa: E402
import names  # noqa: E402
import sects  # noqa: E402

ROJ_KEYS = ("hormazd bahman ardibehesht shehrevar spendarmad khordad amardad dae_pa_adar adar avan khorshed "
            "mohor tir gosh dae_pa_meher meher srosh rashne fravardin behram ram govad dae_pa_din din "
            "ashishvangh ashtad asman zamyad mareshpand aneran").split()
GATHA_KEYS = "ahunavad ushtavad spentomad vohukhshathra vahishtoisht avardad_sal_gah".split()
MAH_KEYS = "fravardin ardibehesht khordad tir amardad shehrevar meher avan adar dae bahman aspandarmad".split()
GAH_KEYS = "ushahin havan second_havan rapithwin uziran aiwisruthrem".split()
FEST_KEYS = ("navroz pateti jamshedi_navroz khordad_sal zarthost_no_diso muktad farvardigan gahambar_maidyozarem "
             "gahambar_maidyoshahem gahambar_paitishahem gahambar_ayathrem gahambar_maidyarem "
             "gahambar_hamaspathmaedem jashan_fravardin jashan_ardibehesht jashan_khordad jashan_tir "
             "jashan_amardad jashan_shehrevar jashan_meher jashan_avan jashan_adar jashan_dae jashan_bahman "
             "jashan_aspandarmad sadeh chaharshanbe_suri mah_niyayesh").split()
CAL_KEYS = "shahanshahi kadmi fasli bastani sasanian".split()

OK_FA = lambda c: 0x0600 <= ord(c) <= 0x06FF or c in " ()\u200c/-·."
OK_GU = lambda c: 0x0A80 <= ord(c) <= 0x0AFF or c in " ()/.-"
OK_AE = lambda c: 0x10B00 <= ord(c) <= 0x10B3F or c == "\u2E31"


def main() -> int:
    errs: list[str] = []
    # 1. keys
    for tbl, keys, nm in ((names.ROJ, ROJ_KEYS, "ROJ"), (names.GATHA, GATHA_KEYS, "GATHA"), (names.MAH, MAH_KEYS, "MAH"),
                          (names.GAH, GAH_KEYS, "GAH"), (names.FESTIVAL, FEST_KEYS, "FESTIVAL"),
                          (names.CALENDAR, CAL_KEYS, "CALENDAR")):
        if list(tbl) != keys:
            errs.append(f"{nm}: keys differ from contract: {set(keys) ^ set(tbl)}")
    for k in FEST_KEYS:
        if k not in fh.H:
            errs.append(f"history missing: {k}")
    for k in CAL_KEYS:
        if k not in fh.CAL_H:
            errs.append(f"calendar history missing: {k}")
    if list(gahs.GAHS) != ["havan", "rapithwin", "second_havan", "uziran", "aiwisruthrem", "ushahin"]:
        errs.append("gahs: unexpected keys")
    for s in sects.SECTS:
        for cal, _, p in s["uses"]:
            if cal not in CAL_KEYS or p["calendar"] != cal:
                errs.append(f"sect {s['key']}: bad calendar {cal}")
    # 2. scripts and NFC
    n = {"fa": 0, "gu": 0, "ae": 0}
    for tname, tbl in names.all_tables().items():
        for key, e in tbl.items():
            for f, ok in (("fa", OK_FA), ("gu", OK_GU), ("ae", OK_AE)):
                s = e.get(f)
                if not s:
                    continue
                n[f] += 1
                if unicodedata.normalize("NFC", s) != s:
                    errs.append(f"{tname}.{key}.{f} not NFC")
                for c in s:
                    if not ok(c):
                        errs.append(f"{tname}.{key}.{f}: U+{ord(c):04X} outside script")
                    if f == "fa" and c in "كيى":
                        errs.append(f"{tname}.{key}.fa: Arabic kaf/yeh")
    # 3. history lengths
    for k, (text, src) in {**fh.H, **fh.CAL_H}.items():
        w = len(text.split())
        if not 80 <= w <= 150:
            errs.append(f"history {k}: {w} words")
        if not src.strip():
            errs.append(f"history {k}: no sources")
    # 4. fonts (optional)
    fonts = sys.argv[1] if len(sys.argv) > 1 else None
    if fonts and os.path.isdir(fonts):
        from fontTools.ttLib import TTFont
        cmap = set()
        for f in os.listdir(fonts):
            if f.lower().endswith((".ttf", ".otf")):
                cmap |= set(TTFont(os.path.join(fonts, f)).getBestCmap())
        for tname, tbl in names.all_tables().items():
            for key, e in tbl.items():
                for f in ("fa", "gu", "ae"):
                    for c in e.get(f) or "":
                        if not c.isspace() and c != "\u200c" and ord(c) not in cmap:
                            errs.append(f"{tname}.{key}.{f}: U+{ord(c):04X} not in fonts")
    # 5. TITUS attestation (optional)
    titus = sys.argv[2] if len(sys.argv) > 2 else None
    if titus and os.path.isfile(titus):
        t = open(titus, encoding="utf-8").read().replace(" \u030a", "\u030a").replace("x v ", "x\u1d5b")
        t = " " + unicodedata.normalize("NFC", t).replace(".", " ") + " "
        derived = {"ahunauuaitī", "uštauuaitī", "vohuxṣ̌aϑrā", "vahištōištī"}
        for tbl in (names.ROJ, names.MAH, names.GAH):
            for key, e in tbl.items():
                for wd in (e.get("ae_tr") or "").replace(".", " ").split():
                    wd = unicodedata.normalize("NFC", wd)
                    if wd not in derived and f" {wd} " not in t:
                        errs.append(f"{key}: '{wd}' not found in TITUS text")
    print(f"strings checked: fa={n['fa']} gu={n['gu']} ae={n['ae']}; histories={len(fh.H) + len(fh.CAL_H)}; "
          f"communities={len(sects.SECTS)}; uncertain forms flagged={len(names.UNCERTAIN)}")
    print("OK" if not errs else "\n".join(errs))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
