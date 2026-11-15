"""Engine-side name tables for Sky Gahshomar, built from the canonical display source names.py.

Reconciliation (app assembly, Nov 2026): the engine track shipped its own spellings here; the content
track's names.py is canonical for display (Gujarati checked against zcserv.com, Avestan against TITUS).
This module now re-exports names.py, keeping the engine's API (ROJ_KEYS, ROJ_NUMBER, display(), avestan(),
JASHAN_ROJ_FOR_MAH ...) so zcalendars, festivals and sky_layer are unchanged. Every spelling that differed
is listed in docs/NAMES_RECONCILIATION.md.

Kept from the engine track because names.py has no equivalent:
  * 'meaning' (English gloss of each roj / Gatha day) and 'fa_alt' (variant Persian spelling);
  * festival keys 'rapithwin_jashan' and 'tirgan_civil' (extra keys beyond the shared contract). Their
    Persian and Gujarati were written by the engine track and are NOT verified against a source
    (listed in names.UNCERTAIN under ('FESTIVAL', key, 'gu'/'fa')).
  * avestan(tokens): the engine's space-separated transliterator (names.to_avestan is the canonical one).
"""
from __future__ import annotations

import copy

import names as _n

_AV = {'a': 68352, 'ā': 68353, 'å': 68354, 'ā̊': 68355, 'ą': 68356, 'ą̄': 68357, 'ə': 68358, 'ə̄': 68359, 'e': 68360, 'ē': 68361, 'o': 68362, 'ō': 68363, 'i': 68364, 'ī': 68365, 'u': 68366, 'ū': 68367, 'k': 68368, 'x': 68369, 'x́': 68370, 'xᵛ': 68371, 'g': 68372, 'ġ': 68373, 'γ': 68374, 'c': 68375, 'j': 68376, 't': 68377, 'θ': 68378, 'd': 68379, 'δ': 68380, 't̰': 68381, 'p': 68382, 'f': 68383, 'b': 68384, 'β': 68385, 'ŋ': 68386, 'ŋ́': 68387, 'ŋᵛ': 68388, 'n': 68389, 'ń': 68390, 'ṇ': 68391, 'm': 68392, 'm̨': 68393, 'ẏ': 68394, 'y': 68395, 'v': 68396, 'r': 68397, 'l': 68398, 's': 68399, 'z': 68400, 'š': 68401, 'ž': 68402, 'š́': 68403, 'ṣ̌': 68404, 'h': 68405}
AVESTAN_WORD_SEPARATOR = "\u2E31"


def avestan(tokens: str) -> str:
    """'a h u r a | m a z d ā' -> Avestan script (engine transliterator). Raises KeyError on an unknown token."""
    return "".join(AVESTAN_WORD_SEPARATOR if t == "|" else chr(_AV[t]) for t in tokens.split())


ROJ_KEYS = ['hormazd', 'bahman', 'ardibehesht', 'shehrevar', 'spendarmad', 'khordad', 'amardad', 'dae_pa_adar', 'adar', 'avan', 'khorshed', 'mohor', 'tir', 'gosh', 'dae_pa_meher', 'meher', 'srosh', 'rashne', 'fravardin', 'behram', 'ram', 'govad', 'dae_pa_din', 'din', 'ashishvangh', 'ashtad', 'asman', 'zamyad', 'mareshpand', 'aneran']
GATHA_KEYS = ['ahunavad', 'ushtavad', 'spentomad', 'vohukhshathra', 'vahishtoisht', 'avardad_sal_gah']
MAH_KEYS = ['fravardin', 'ardibehesht', 'khordad', 'tir', 'amardad', 'shehrevar', 'meher', 'avan', 'adar', 'dae', 'bahman', 'aspandarmad']
GAH_KEYS = ['havan', 'second_havan', 'rapithwin', 'uziran', 'aiwisruthrem', 'ushahin']

_MEANING = {'ROJ': {'hormazd': 'Ahura Mazda, the Wise Lord', 'bahman': 'Good Mind', 'ardibehesht': 'Best Truth / Righteousness', 'shehrevar': 'Desirable Dominion', 'spendarmad': 'Holy Devotion; the Earth', 'khordad': 'Wholeness; the Waters', 'amardad': 'Immortality; the Plants', 'dae_pa_adar': 'the Creator, with Adar', 'adar': 'Fire', 'avan': 'the Waters', 'khorshed': 'the radiant Sun', 'mohor': 'the Moon', 'tir': 'Tishtrya, the star Sirius; rain', 'gosh': 'the soul of the Cow; animals', 'dae_pa_meher': 'the Creator, with Meher', 'meher': 'Mithra: covenant, light', 'srosh': 'Sraosha: obedience, hearing', 'rashne': 'Rashnu: justice', 'fravardin': 'the Fravashis (guardian spirits)', 'behram': 'Verethraghna: victory', 'ram': 'Raman: peace, joy', 'govad': 'Vata: the wind', 'dae_pa_din': 'the Creator, with Din', 'din': 'Daena: religion, conscience', 'ashishvangh': 'Ashi Vanguhi: blessing, reward', 'ashtad': 'Arshtat: rectitude', 'asman': 'the Sky', 'zamyad': 'the Earth', 'mareshpand': 'the Holy Word', 'aneran': 'Endless Lights'}, 'GATHA': {'ahunavad': 'first Gatha day (Ahunavaiti Gatha)', 'ushtavad': 'second Gatha day (Ushtavaiti Gatha)', 'spentomad': 'third Gatha day (Spenta Mainyu Gatha)', 'vohukhshathra': 'fourth Gatha day (Vohu Khshathra Gatha)', 'vahishtoisht': 'fifth Gatha day (Vahishtoishti Gatha)', 'avardad_sal_gah': "leap day of the Fasli and Bastani calendars (also 'Roz-e Vahizak')"}}
_FA_ALT = {'ROJ': {'hormazd': 'اورمزد', 'spendarmad': 'اسفند', 'khordad': 'خرداد', 'amardad': 'مرداد', 'khorshed': 'خورشید', 'behram': 'بهرام', 'ashishvangh': 'اشیشونگ', 'mareshpand': 'مهراسپند', 'aneran': 'انیران'}, 'GATHA': {'avardad_sal_gah': 'روز وهیزک'}, 'MAH': {'khordad': 'خرداد', 'amardad': 'مرداد', 'aspandarmad': 'اسفند'}}
_EXTRA_FESTIVALS = {'rapithwin_jashan': {'en': 'Rapithwin Jashan (Ardibehesht roj, Fravardin mah)', 'fa': 'جشن رپیتون', 'gu': 'રપીથવનનું જશન'}, 'tirgan_civil': {'en': 'Tirgan (Iranian civil 13 Tir)', 'fa': 'تیرگان (۱۳ تیر)', 'gu': 'તીરગાન (ઈરાની ૧૩ તીર)'}}


def _table(name: str) -> dict:
    t = copy.deepcopy(getattr(_n, name))
    for k, v in t.items():
        if isinstance(v, dict):
            v.setdefault("meaning", _MEANING.get(name, {}).get(k, ""))
            alt = _FA_ALT.get(name, {}).get(k, "")
            v.setdefault("fa_alt", "" if alt == v.get("fa") else alt)
            if v.get("ae") is None and "ae" in v:
                v["ae"] = ""
    return t


ROJ = _table("ROJ")
GATHA = _table("GATHA")
MAH = _table("MAH")
GAH = _table("GAH")
FESTIVAL = _table("FESTIVAL")
for _k, _v in _EXTRA_FESTIVALS.items():
    FESTIVAL.setdefault(_k, dict(_v))
    for _f in ("fa", "gu"):
        _n.UNCERTAIN.setdefault(("FESTIVAL", _k, _f),
                                "Engine-track spelling for an extra festival key; not checked against a source.")
CALENDAR = _table("CALENDAR")

JASHAN_ROJ_FOR_MAH = {'fravardin': 'fravardin', 'ardibehesht': 'ardibehesht', 'khordad': 'khordad', 'tir': 'tir', 'amardad': 'amardad', 'shehrevar': 'shehrevar', 'meher': 'meher', 'avan': 'avan', 'adar': 'adar', 'bahman': 'bahman', 'aspandarmad': 'spendarmad', 'dae': 'hormazd'}
ROJ_NUMBER = {k: i + 1 for i, k in enumerate(ROJ_KEYS)}
MAH_NUMBER = {k: i + 1 for i, k in enumerate(MAH_KEYS)}

assert list(ROJ) == ROJ_KEYS and list(GATHA) == GATHA_KEYS and list(MAH) == MAH_KEYS
assert set(GAH) == set(GAH_KEYS)


def display(table: dict, key: str, sep: str = " · ") -> str:
    """'English · Persian · Gujarati' for any name table entry."""
    e = table[key]
    return sep.join(x for x in (e.get("en"), e.get("fa"), e.get("gu")) if x)
