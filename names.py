"""Names in English, Persian and Gujarati (and Avestan script for the day names and Gatha days).

Display format: 'English · Persian · Gujarati'  (see fmt()).

Every table records where its spellings come from (SOURCES[table]); single forms that were made for the
app rather than copied from a source, or that are doubtful, are listed in UNCERTAIN with the reason.

Avestan
-------
Avestan-script strings are not typed by hand. Each entry carries 'ae_tr', a transliteration copied from
the Geldner text of the Avesta as digitised by the TITUS project (Frankfurt), and 'ae' is produced from it
by to_avestan() using the Unicode Avestan block (U+10B00-U+10B3F) and the letter correspondences of the
Unicode chart and Hoffmann's transliteration (ii and uu are written as two letters, as Unicode specifies).
Words are separated by U+2E31 WORD SEPARATOR MIDDLE DOT, the Avestan word dot.

The day names use the forms of Siroza 1, where each day's being is named in turn in the dative or
genitive ('to/of X'): this is how the days are named in the Avesta itself; no nominative list exists.
Days 8, 15 and 23 are all 'daϑuṣ̌ō ahurahe mazdā̊' (of the Creator, Ahura Mazda) in the Avesta; the
Middle Persian names Dae-pa-Adar, Dae-pa-Meher, Dae-pa-Din that tell them apart have no Avestan form.
"""
from __future__ import annotations

import unicodedata

# ------------------------------------------------------------------------------------------ Avestan
_AE_MAP = [  # longest tokens first; keys are NFC
    ("ā̊", "\U00010B03"), ("å", "\U00010B02"), ("ą̇", "\U00010B05"), ("ą", "\U00010B04"),
    ("ə̄", "\U00010B07"), ("ə", "\U00010B06"), ("ā", "\U00010B01"), ("a", "\U00010B00"),
    ("ē", "\U00010B09"), ("e", "\U00010B08"), ("ō", "\U00010B0B"), ("o", "\U00010B0A"),
    ("ī", "\U00010B0D"), ("i", "\U00010B0C"), ("ū", "\U00010B0F"), ("u", "\U00010B0E"),
    ("xᵛ", "\U00010B13"), ("x́", "\U00010B12"), ("x", "\U00010B11"), ("k", "\U00010B10"),
    ("ġ", "\U00010B15"), ("γ", "\U00010B16"), ("g", "\U00010B14"), ("c", "\U00010B17"),
    ("j", "\U00010B18"), ("t̰", "\U00010B1D"), ("ϑ", "\U00010B1A"), ("θ", "\U00010B1A"),
    ("t", "\U00010B19"), ("δ", "\U00010B1C"), ("d", "\U00010B1B"), ("p", "\U00010B1E"),
    ("f", "\U00010B1F"), ("β", "\U00010B21"), ("b", "\U00010B20"), ("ŋᵛ", "\U00010B24"),
    ("ŋ́", "\U00010B23"), ("ŋ", "\U00010B22"), ("ń", "\U00010B26"), ("ṇ", "\U00010B27"),
    ("n", "\U00010B25"), ("m̨", "\U00010B29"), ("m", "\U00010B28"), ("ẏ", "\U00010B2A"),
    ("y", "\U00010B2B"), ("v", "\U00010B2C"), ("r", "\U00010B2D"), ("l", "\U00010B2E"),
    ("s", "\U00010B2F"), ("z", "\U00010B30"), ("ṣ̌", "\U00010B34"), ("š́", "\U00010B33"),
    ("š", "\U00010B31"), ("ž", "\U00010B32"), ("h", "\U00010B35"),
    (" ", "\u2E31"), (".", "\u2E31"),
]
_AE_MAP = [(unicodedata.normalize("NFC", k), v) for k, v in _AE_MAP]
_AE_MAP.sort(key=lambda kv: -len(kv[0]))


def to_avestan(translit: str) -> str:
    """Hoffmann/TITUS transliteration -> Avestan script. Raises ValueError on an unknown letter."""
    s = unicodedata.normalize("NFC", translit)
    out, i = [], 0
    while i < len(s):
        for k, v in _AE_MAP:
            if s.startswith(k, i):
                out.append(v)
                i += len(k)
                break
        else:
            raise ValueError(f"no Avestan letter for {s[i]!r} in {translit!r}")
    return "".join(out)


# ------------------------------------------------------------------------------------------ numerals
_GU_DIGITS = str.maketrans("0123456789", "૦૧૨૩૪૫૬૭૮૯")
_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def gu_num(n) -> str:
    """Gujarati digits (U+0AE6-U+0AEF), as printed in Parsi Gujarati calendars."""
    return str(n).translate(_GU_DIGITS)


def fa_num(n) -> str:
    """Extended Arabic-Indic (Persian) digits (U+06F0-U+06F9)."""
    return str(n).translate(_FA_DIGITS)


def fmt(entry: dict, sep: str = " · ") -> str:
    """'English · Persian · Gujarati' (empty parts dropped)."""
    return sep.join(p for p in (entry.get("en"), entry.get("fa"), entry.get("gu")) if p)


# ------------------------------------------------------------------------------------------ title
TITLE = {
    "en": "Sky Gahshomar",
    "fa": "گاهشمار",
    "gu": "ગાહશુમાર",
    # Pazand-style spelling of the Persian word in Avestan letters (the script was used for Middle and
    # New Persian 'Pazand' texts). 'Gahshomar' is a New Persian word; it has no Avestan original.
    "ae_tr": "gāhšumār",
}

# ------------------------------------------------------------------------------------------ roj (days)
# en: Parsi spellings as used in the shared key contract (Shahanshahi/Kadmi usage).
# fa: Iranian Zoroastrian forms, from the Persian Wikipedia table 'گاهشماری اوستایی نو' (after Biruni and
#     Dehkhoda) and the Zoroastrian Association of Germany's calendar page.
# gu: Zoroastrian Calendar Services, Gujarati year view 2026 (zcserv.com, Arzan Lali), read 15 Nov 2026.
# ae_tr: Siroza 1.1-30, Geldner's text via TITUS.
ROJ = {
    "hormazd":      {"n": 1,  "en": "Hormazd",      "fa": "هرمزد",      "gu": "હોરમજદ",     "ae_tr": "ahurahe mazdā̊",            "yazata": "Ahura Mazda"},
    "bahman":       {"n": 2,  "en": "Bahman",       "fa": "بهمن",       "gu": "બેહમન",      "ae_tr": "vaŋhauue manaŋhe",          "yazata": "Vohu Manah (Good Mind)"},
    "ardibehesht":  {"n": 3,  "en": "Ardibehesht",  "fa": "اردیبهشت",   "gu": "અરદીબેહેશત",  "ae_tr": "aṣ̌ahe vahištahe",          "yazata": "Asha Vahishta (Best Truth)"},
    "shehrevar":    {"n": 4,  "en": "Shehrevar",    "fa": "شهریور",     "gu": "શેહેરેવર",    "ae_tr": "xṣ̌aϑrahe vairiiehe",        "yazata": "Khshathra Vairya (Desirable Dominion)"},
    "spendarmad":   {"n": 5,  "en": "Spendarmad",   "fa": "سپندارمذ",   "gu": "અસફનદારમદ",  "ae_tr": "spəṇtaiiā̊ vaŋhuiiā̊ ārmatōiš", "yazata": "Spenta Armaiti (Holy Devotion)"},
    "khordad":      {"n": 6,  "en": "Khordad",      "fa": "خرداد",      "gu": "ખોરદાદ",     "ae_tr": "hauruuatātō",               "yazata": "Haurvatat (Wholeness)"},
    "amardad":      {"n": 7,  "en": "Amardad",      "fa": "امرداد",     "gu": "અમરદાદ",     "ae_tr": "amərətatātō",               "yazata": "Ameretat (Immortality)"},
    "dae_pa_adar":  {"n": 8,  "en": "Dae-pa-Adar",  "fa": "دی به آذر",  "gu": "દએ પ આદર",   "ae_tr": "daϑuṣ̌ō ahurahe mazdā̊",     "yazata": "Ahura Mazda the Creator"},
    "adar":         {"n": 9,  "en": "Adar",         "fa": "آذر",        "gu": "આદર",        "ae_tr": "āϑrō",                      "yazata": "Atar (Fire)"},
    "avan":         {"n": 10, "en": "Avan",         "fa": "آبان",       "gu": "આવાં",        "ae_tr": "apąm vaŋuhīnąm",            "yazata": "the Waters"},
    "khorshed":     {"n": 11, "en": "Khorshed",     "fa": "خور",        "gu": "ખોરશેદ",     "ae_tr": "huuarəxṣ̌aētahe",            "yazata": "Hvare Khshaeta (the Sun)"},
    "mohor":        {"n": 12, "en": "Mohor",        "fa": "ماه",        "gu": "મોહોર",      "ae_tr": "mąŋhahe",                   "yazata": "Mah (the Moon)"},
    "tir":          {"n": 13, "en": "Tir",          "fa": "تیر",        "gu": "તીર",        "ae_tr": "tištriiehe",                "yazata": "Tishtrya (Sirius)"},
    "gosh":         {"n": 14, "en": "Gosh",         "fa": "گوش",        "gu": "ગોશ",        "ae_tr": "gə̄uš urune",                "yazata": "Geush Urvan (Soul of the Cow)"},
    "dae_pa_meher": {"n": 15, "en": "Dae-pa-Meher", "fa": "دی به مهر",  "gu": "દએ પ મેહેર",  "ae_tr": "daϑuṣ̌ō ahurahe mazdā̊",     "yazata": "Ahura Mazda the Creator"},
    "meher":        {"n": 16, "en": "Meher",        "fa": "مهر",        "gu": "મેહેર",       "ae_tr": "miϑrahe",                   "yazata": "Mithra"},
    "srosh":        {"n": 17, "en": "Srosh",        "fa": "سروش",       "gu": "સરોશ",       "ae_tr": "sraoṣ̌ahe",                  "yazata": "Sraosha (Hearkening)"},
    "rashne":       {"n": 18, "en": "Rashne",       "fa": "رشن",        "gu": "રશ્ને",       "ae_tr": "raṣ̌naoš",                   "yazata": "Rashnu (Justice)"},
    "fravardin":    {"n": 19, "en": "Fravardin",    "fa": "فروردین",    "gu": "ફરવરદીન",    "ae_tr": "frauuaṣ̌inąm",               "yazata": "the Fravashis"},
    "behram":       {"n": 20, "en": "Behram",       "fa": "ورهرام",     "gu": "બેહેરાંમ",    "ae_tr": "vərəϑraγnahe",              "yazata": "Verethraghna (Victory)"},
    "ram":          {"n": 21, "en": "Ram",          "fa": "رام",        "gu": "રાંમ",        "ae_tr": "rāmanō xᵛāstrahe",          "yazata": "Raman (Peace)"},
    "govad":        {"n": 22, "en": "Govad",        "fa": "باد",        "gu": "ગોવાદ",      "ae_tr": "vātahe",                    "yazata": "Vata (Wind)"},
    "dae_pa_din":   {"n": 23, "en": "Dae-pa-Din",   "fa": "دی به دین",  "gu": "દએ પ દીન",   "ae_tr": "daϑuṣ̌ō ahurahe mazdā̊",     "yazata": "Ahura Mazda the Creator"},
    "din":          {"n": 24, "en": "Din",          "fa": "دین",        "gu": "દીન",        "ae_tr": "daēnaiiā̊ vaŋhuiiā̊",        "yazata": "Daena (Religion, Conscience)"},
    "ashishvangh":  {"n": 25, "en": "Ashishvangh",  "fa": "ارد",        "gu": "અશીશવંદ",    "ae_tr": "aṣ̌ōiš vaŋhuiiā̊",           "yazata": "Ashi (Reward)"},
    "ashtad":       {"n": 26, "en": "Ashtad",       "fa": "اشتاد",      "gu": "આશતાદ",      "ae_tr": "arštātō",                   "yazata": "Arshtat (Rectitude)"},
    "asman":        {"n": 27, "en": "Asman",        "fa": "آسمان",      "gu": "આસમાન",      "ae_tr": "aṣ̌nō",                      "yazata": "Asman (Sky)"},
    "zamyad":       {"n": 28, "en": "Zamyad",       "fa": "زامیاد",     "gu": "જમીઆદ",      "ae_tr": "zəmō",                      "yazata": "Zam (Earth)"},
    "mareshpand":   {"n": 29, "en": "Mareshpand",   "fa": "مهراسپند",   "gu": "મારેસપંદ",    "ae_tr": "mąϑrahe spəṇtahe",          "yazata": "Manthra Spenta (Holy Word)"},
    "aneran":       {"n": 30, "en": "Aneran",       "fa": "انیران",     "gu": "અનેરાંન",     "ae_tr": "anaγranąm raocaŋhąm",       "yazata": "Anaghra Raocha (Endless Lights)"},
}

# ------------------------------------------------------------------------------------------ Gatha days
# fa: Persian Wikipedia 'گاهشماری اوستایی نو' (اندرگاهان); leap day 'اورداد' from 'فهرست نام روزهای ماه'.
# gu: zcserv.com Gujarati month views (March 2024 and 2028 for the leap day).
# ae_tr: names of the five Gathas, nominative, from the accusatives attested in the Avesta
#        (ahunauuaitīm, uštauuaitīm, spəṇtā.mainiiūm, vohuxṣ̌aϑrąm, vahištōištīm gāϑąm; TITUS).
GATHA = {
    "ahunavad":        {"n": 1, "en": "Ahunavad",        "fa": "اهنودگاه",       "gu": "અહુનવદ",      "ae_tr": "ahunauuaitī"},
    "ushtavad":        {"n": 2, "en": "Ushtavad",        "fa": "اشتودگاه",       "gu": "ઉશતવદ",       "ae_tr": "uštauuaitī"},
    "spentomad":       {"n": 3, "en": "Spentomad",       "fa": "سپنتمدگاه",      "gu": "સપેનતોમદ",    "ae_tr": "spəṇtā.mainiiū"},
    "vohukhshathra":   {"n": 4, "en": "Vohukhshathra",   "fa": "وهوخشترگاه",     "gu": "વોહુખષથર",    "ae_tr": "vohuxṣ̌aϑrā"},
    "vahishtoisht":    {"n": 5, "en": "Vahishtoisht",    "fa": "وهیشتواشت‌گاه",  "gu": "વહીશતોઈશત",   "ae_tr": "vahištōištī"},
    "avardad_sal_gah": {"n": 6, "en": "Avardad-sal-gah", "fa": "اورداد",         "gu": "આવરદાદ સાલ",  "ae_tr": None},
}

# ------------------------------------------------------------------------------------------ mah (months)
# fa: Persian Wikipedia 'گاهشماری اوستایی نو' month table; gu: zcserv.com Gujarati year view headers.
# ae_tr (optional): the Old Iranian genitive month names listed in Wikipedia 'Zoroastrian calendar'
#        (after Encyclopaedia Iranica), spelled as the same words appear in the TITUS Siroza text.
MAH = {
    "fravardin":   {"n": 1,  "en": "Fravardin",   "fa": "فروردین",   "gu": "ફરવરદીન",   "ae_tr": "frauuaṣ̌inąm"},
    "ardibehesht": {"n": 2,  "en": "Ardibehesht", "fa": "اردیبهشت",  "gu": "અરદીબેહેશત", "ae_tr": "aṣ̌ahe vahištahe"},
    "khordad":     {"n": 3,  "en": "Khordad",     "fa": "خرداد",     "gu": "ખોરદાદ",    "ae_tr": "hauruuatātō"},
    "tir":         {"n": 4,  "en": "Tir",         "fa": "تیر",       "gu": "તીર",       "ae_tr": "tištriiehe"},
    "amardad":     {"n": 5,  "en": "Amardad",     "fa": "امرداد",    "gu": "અમરદાદ",    "ae_tr": "amərətatātō"},
    "shehrevar":   {"n": 6,  "en": "Shehrevar",   "fa": "شهریور",    "gu": "શેહેરેવર",   "ae_tr": "xṣ̌aϑrahe vairiiehe"},
    "meher":       {"n": 7,  "en": "Meher",       "fa": "مهر",       "gu": "મેહેર",      "ae_tr": "miϑrahe"},
    "avan":        {"n": 8,  "en": "Avan",        "fa": "آبان",      "gu": "આવાં",       "ae_tr": "apąm"},
    "adar":        {"n": 9,  "en": "Adar",        "fa": "آذر",       "gu": "આદર",       "ae_tr": "āϑrō"},
    "dae":         {"n": 10, "en": "Dae",         "fa": "دی",        "gu": "દએ",        "ae_tr": "daϑuṣ̌ō"},
    "bahman":      {"n": 11, "en": "Bahman",      "fa": "بهمن",      "gu": "બેહમન",     "ae_tr": "vaŋhə̄uš manaŋhō"},
    "aspandarmad": {"n": 12, "en": "Aspandarmad", "fa": "سپندارمذ",  "gu": "અસફનદારમદ", "ae_tr": "spəṇtaiiā̊ ārmatōiš"},
}

# ------------------------------------------------------------------------------------------ gahs
# fa: Persian Wikipedia 'گاهشماری اوستایی نو' (شبانه روز); 'second_havan' is a descriptive form.
# gu: Parsi Times, 'દરેક ગેહ માંડવાનો વખત' (July 2018), which uses all six names.
# ae_tr: dative forms of the Gah prayers and Yasna 1 ('to X'), TITUS: hāuuanə̄e, rapiϑβināi,
#        uzaiieirināi, aiβisrūϑrimāi, uṣ̌ahināi.
GAH = {
    "ushahin":      {"en": "Ushahin",      "fa": "اوشهنگاه",      "gu": "ઉશહીન ગેહ",          "ae_tr": "uṣ̌ahināi"},
    "havan":        {"en": "Havan",        "fa": "هاونگاه",       "gu": "હાવન ગેહ",           "ae_tr": "hāuuanə̄e"},
    "second_havan": {"en": "Second Havan", "fa": "هاونگاه دوم",   "gu": "બીજી હાવન ગેહ",      "ae_tr": "hāuuanə̄e"},
    "rapithwin":    {"en": "Rapithwin",    "fa": "رپیتونیگاه",    "gu": "રપિથ્વન ગેહ",        "ae_tr": "rapiϑβināi"},
    "uziran":       {"en": "Uziran",       "fa": "ازیرنیگاه",     "gu": "ઉજીરન ગેહ",          "ae_tr": "uzaiieirināi"},
    "aiwisruthrem": {"en": "Aiwisruthrem", "fa": "اویسروترمگاه",  "gu": "અઈવીસ્ત્રુથ્રેમ ગેહ", "ae_tr": "aiβisrūϑrimāi"},
}

# ------------------------------------------------------------------------------------------ festivals
# gu: zcserv.com special-event names (Gujarati), 2026 month views, unless listed in UNCERTAIN.
# fa: Dehkhoda (via vajehyab.com) for the Gahambar names; Persian Wikipedia 'جشن‌های ایران باستان' and
#     'گاهشماری اوستایی نو' for the name-day feasts; others as noted in UNCERTAIN.
FESTIVAL = {
    "navroz":               {"en": "Navroz (New Year)",            "fa": "نوروز",                 "gu": "નવરોઝ"},
    "pateti":               {"en": "Pateti",                       "fa": "پتت",                   "gu": "પતેતી"},
    "jamshedi_navroz":      {"en": "Jamshedi Navroz",              "fa": "نوروز جمشیدی",          "gu": "જમ્શેદી નવરોઝ"},
    "khordad_sal":          {"en": "Khordad Sal",                  "fa": "خوردادسال",             "gu": "ખોરદાદ સાલ"},
    "zarthost_no_diso":     {"en": "Zarthost no Diso",             "fa": "درگذشت اشو زرتشت",      "gu": "ઝર્થોસ્ત નો દિસો"},
    "muktad":               {"en": "Muktad (Farvardigan days)",    "fa": "فروردگان (پنجه)",       "gu": "મુકતાદ"},
    "farvardigan":          {"en": "Farvardinegan (19 Fravardin)", "fa": "فروردینگان",            "gu": "જશને ફરવરદીગન"},
    "gahambar_maidyozarem": {"en": "Maidyozarem Gahambar",         "fa": "گاهنبار میدیوزرم",      "gu": "મૈધ્યોઝરેમ ગહમ્બાર"},
    "gahambar_maidyoshahem": {"en": "Maidyoshahem Gahambar",       "fa": "گاهنبار میدیوشم",       "gu": "મૈધ્યોશેમ ગહમ્બાર"},
    "gahambar_paitishahem": {"en": "Paitishahem Gahambar",         "fa": "گاهنبار پتیه‌شهیم",     "gu": "પૈતિશેમ ગહમ્બાર"},
    "gahambar_ayathrem":    {"en": "Ayathrem Gahambar",            "fa": "گاهنبار ایاسرم",        "gu": "અયાથરેમ ગહમ્બાર"},
    "gahambar_maidyarem":   {"en": "Maidyarem Gahambar",           "fa": "گاهنبار میدیارم",       "gu": "મૈધ્યરેમ ગહમ્બાર"},
    "gahambar_hamaspathmaedem": {"en": "Hamaspathmaedem Gahambar", "fa": "گاهنبار همسپتمدم",      "gu": "હમાસ્પાથેમેદાયેમ ગહમ્બાર"},
    "jashan_fravardin":     {"en": "Fravardin Jashan",             "fa": "جشن فروردینگان",        "gu": "ફરવરદીઆન જશન"},
    "jashan_ardibehesht":   {"en": "Ardibehesht Jashan",           "fa": "اردیبهشتگان",           "gu": "જશને અરદિબેહેશતગન"},
    "jashan_khordad":       {"en": "Khordad Jashan",               "fa": "خوردادگان",             "gu": "જશને ખોરદાદગન"},
    "jashan_tir":           {"en": "Tirgan",                       "fa": "تیرگان",                "gu": "જશને તીરગન"},
    "jashan_amardad":       {"en": "Amardad Jashan",               "fa": "امردادگان",             "gu": "જશને અમરદાદગન"},
    "jashan_shehrevar":     {"en": "Shehrevar Jashan",             "fa": "شهریورگان",             "gu": "જશને શેહેરેવરગન"},
    "jashan_meher":         {"en": "Mehergan",                     "fa": "مهرگان",                "gu": "જશને મેહેરગન"},
    "jashan_avan":          {"en": "Avan Ardvisur Parab",          "fa": "آبانگان",               "gu": "આવાં અર્દાવીસૂર નુ પરબ"},
    "jashan_adar":          {"en": "Adar Jashan (Atash nu Parab)", "fa": "آذرگان",                "gu": "આતશ નુ પરબ"},
    "jashan_dae":           {"en": "Dae Jashans",                  "fa": "دیگان",                 "gu": "દએ માહ નુ જશન"},
    "jashan_bahman":        {"en": "Bahman Jashan",                "fa": "بهمنگان",               "gu": "જશને બેહમનગન"},
    "jashan_aspandarmad":   {"en": "Aspandarmad Jashan",           "fa": "سپندارمذگان",           "gu": "જશને અસફનદારમદગન"},
    "sadeh":                {"en": "Sadeh",                        "fa": "جشن سده",               "gu": "જશને સદેહ"},
    "chaharshanbe_suri":    {"en": "Chaharshanbe Suri",            "fa": "چهارشنبه‌سوری",          "gu": "ચહારશંબે સૂરી"},
    "mah_niyayesh":         {"en": "Mah Niyayesh (moon prayer)",   "fa": "ماه نیایش",             "gu": "માહ બોખતાર નિયાએશ"},
}

# ------------------------------------------------------------------------------------------ calendars, eras
CALENDAR = {
    "shahanshahi": {"en": "Shahanshahi", "fa": "شاهنشاهی", "gu": "શહેનશાહી"},
    "kadmi":       {"en": "Kadmi (Qadimi)", "fa": "قدیمی", "gu": "કદમી"},
    "fasli":       {"en": "Fasli", "fa": "فصلی", "gu": "ફસલિ"},
    "bastani":     {"en": "Bastani (Iranian)", "fa": "باستانی", "gu": "બાસ્તાની"},
    "sasanian":    {"en": "Sasanian (reconstruction)", "fa": "ساسانی (بازسازی)", "gu": "સાસાની (પુનર્રચના)"},
}

ERA = {
    "yz":  {"en": "Yazdegerdi era", "abbr_en": "Y.Z.", "fa": "یزدگردی", "abbr_fa": "یزدگردی",
            "gu": "યઝદેજરદી", "abbr_gu": "ય.ઝ.",
            "epoch": "16 June 632 CE (Julian), accession of Yazdegerd III"},
    "zre": {"en": "Zarathushtrian Religious Era", "abbr_en": "ZRE", "fa": "سال دینی زرتشتی",
            "abbr_fa": "دینی", "gu": "જરથોસ્તી દીની સાલ", "abbr_gu": "ZRE",
            "epoch": "March equinox of 1738 BCE (year 3738 began in 2000 CE)"},
}

# Python weekday(): 0 = Monday. The Zoroastrian calendar itself has no week; Parsis use the Gujarati
# weekday names and Iranians the Persian ones.
WEEKDAY = {
    0: {"en": "Monday",    "fa": "دوشنبه",   "gu": "સોમવાર"},
    1: {"en": "Tuesday",   "fa": "سه‌شنبه",   "gu": "મંગળવાર"},
    2: {"en": "Wednesday", "fa": "چهارشنبه", "gu": "બુધવાર"},
    3: {"en": "Thursday",  "fa": "پنجشنبه",  "gu": "ગુરુવાર"},
    4: {"en": "Friday",    "fa": "جمعه",     "gu": "શુક્રવાર"},
    5: {"en": "Saturday",  "fa": "شنبه",     "gu": "શનિવાર"},
    6: {"en": "Sunday",    "fa": "یکشنبه",   "gu": "રવિવાર"},
}

# ------------------------------------------------------------------------------------------ places
PLACES = {
    "yazd":        {"en": "Yazd",        "fa": "یزد",          "gu": "યઝદ"},
    "kerman":      {"en": "Kerman",      "fa": "کرمان",        "gu": "કરમાન"},
    "sharifabad":  {"en": "Sharifabad",  "fa": "شریف‌آباد",     "gu": "શરીફાબાદ"},
    "tehran":      {"en": "Tehran",      "fa": "تهران",        "gu": "તેહરાન"},
    "persepolis":  {"en": "Persepolis",  "fa": "تخت جمشید",    "gu": "પર્સેપોલિસ"},
    "chak_chak":   {"en": "Chak Chak (Pir-e Sabz)", "fa": "چک‌چک (پیر سبز)", "gu": "પિર એ સબ્ઝ"},
    "surat":       {"en": "Surat",       "fa": "سورت",         "gu": "સુરત"},
    "navsari":     {"en": "Navsari",     "fa": "نوساری",       "gu": "નવસારી"},
    "udvada":      {"en": "Udvada",      "fa": "اودوادا",      "gu": "ઉદવાડા"},
    "bharuch":     {"en": "Bharuch",     "fa": "بهروچ",        "gu": "ભરૂચ"},
    "sanjan":      {"en": "Sanjan",      "fa": "سنجان",        "gu": "સંજાણ"},
    "mumbai":      {"en": "Mumbai",      "fa": "بمبئی",        "gu": "મુંબઈ"},
    "karachi":     {"en": "Karachi",     "fa": "کراچی",        "gu": "કરાચી"},
}

# ------------------------------------------------------------------------------------------ sources
SOURCES = {
    "ROJ.en": "Shared key contract (Parsi spellings); cf. zcserv.com English view (which writes Ava, Aspandard).",
    "ROJ.fa": "Persian Wikipedia, 'گاهشماری اوستایی نو' and 'فهرست نام روزهای ماه' (Biruni/Dehkhoda forms); "
              "Anjoman-e Zartoshtian-e Alman, 'تقویم زرتشتی' (zoroastrian.de).",
    "ROJ.gu": "Zoroastrian Calendar Services (zcserv.com), Gujarati year view 2026, read 15 Nov 2026.",
    "ROJ.ae": "Siroza 1.1-30 in K. F. Geldner, Avesta (1889-96), digitised by TITUS (titus.uni-frankfurt.de).",
    "GATHA.fa": "Persian Wikipedia, 'گاهشماری اوستایی نو' (اندرگاهان) and 'فهرست نام روزهای ماه' (اورداد).",
    "GATHA.gu": "zcserv.com Gujarati month views, March 2024 and March 2028 (leap years).",
    "GATHA.ae": "Gatha names attested in the accusative in the Avesta (TITUS); nominatives by regular morphology.",
    "MAH.fa": "Persian Wikipedia, 'گاهشماری اوستایی نو', month table.",
    "MAH.gu": "zcserv.com Gujarati year view 2026, month headers.",
    "MAH.ae": "Wikipedia, 'Zoroastrian calendar', Avestan month names (after Encyclopaedia Iranica), in TITUS spelling.",
    "GAH.fa": "Persian Wikipedia, 'گاهشماری اوستایی نو'.",
    "GAH.gu": "Parsi Times (Gujarati edition), 'દરેક ગેહ માંડવાનો વખત', July 2018.",
    "GAH.ae": "Gah prayers / Yasna 1 dative forms, TITUS.",
    "FESTIVAL.gu": "zcserv.com Gujarati special-event names (2026 month views), except entries in UNCERTAIN.",
    "FESTIVAL.fa": "Dehkhoda, 'گاهنبار' (Gahambar names); Persian Wikipedia, 'جشن‌های ایران باستان', 'تیرگان', "
                   "'مهرگان', 'فروردینگان' (name-day feasts).",
    "CALENDAR": "zcserv.com Gujarati labels (શહેનશાહી, કદમી, ફસલિ); Persian names are the standard Persian words.",
    "ERA": "Wikipedia, 'Zoroastrian calendar' (epochs); zcserv.com (ય.ઝ.); Niechcial 2019 (سال دینی).",
    "WEEKDAY": "Standard Persian and Gujarati weekday names; Gujarati forms as printed by zcserv.com day view.",
    "PLACES": "Standard Persian and Gujarati spellings of the place names; see UNCERTAIN for transliterations.",
    "TITLE": "گاهشمار: Dehkhoda / Persian usage ('calendar', lit. 'time-reckoner').",
}

# (table, key, field): reason
UNCERTAIN = {
    ("TITLE", None, "gu"): "Gujarati transliteration made for the app; no source spelling found.",
    ("TITLE", None, "ae_tr"): "Pazand-style spelling made for the app; not an Avestan word.",
    ("ROJ", "spendarmad", "gu"): "zcserv writes અસફનદારમદ (Asfandarmad) for both day 5 and month 12; other Parsi "
                                 "texts write સ્પેન્દારમદ for the day. Kept as in the source.",
    ("ROJ", "ashishvangh", "gu"): "zcserv writes અશીશવંદ (-vand); the English form Ashishvangh suggests -વંઘ. Kept as "
                                  "in the source; may be a typing variant there.",
    ("ROJ", "khordad", "fa"): "Iranian Zoroastrian usage also writes خورداد.",
    ("ROJ", "behram", "fa"): "ورهرام is the Zoroastrian form; general Persian writes بهرام.",
    ("ROJ", "aneran", "fa"): "Also written انارام; the Persian Wikipedia list gives انارام, the calendar table انیران.",
    ("ROJ", "mareshpand", "fa"): "Also مانتره سپند.",
    ("ROJ", "asman", "ae_tr"): "TITUS gives aṣ̌nō with a variant note at Siroza 1.27; Siroza 2.27 has asmanəm.",
    ("ROJ", "*", "ae_tr"): "Siroza 1 names the beings in mixed cases (dative vaŋhauue manaŋhe for day 2, "
                           "genitive elsewhere); forms are as attested, trimmed to the name and one epithet.",
    ("GATHA", "avardad_sal_gah", "ae_tr"): "No Avestan name: a 20th-century Fasli leap day.",
    ("GATHA", "avardad_sal_gah", "gu"): "zcserv shows આવરદાદ સાલ; the full name is Avardad-sal-gah.",
    ("GATHA", "*", "ae_tr"): "Nominatives derived from attested accusatives (regular morphology), not attested as such.",
    ("MAH", "*", "ae_tr"): "Optional; Old Iranian month names are not listed together in the Avesta.",
    ("GAH", "second_havan", "fa"): "Descriptive Persian made for the app.",
    ("FESTIVAL", "pateti", "fa"): "پتت is the Persian word for the repentance prayer; Pateti is a Parsi festival name "
                                  "with no Iranian equivalent.",
    ("FESTIVAL", "zarthost_no_diso", "fa"): "Descriptive Persian ('death of Asho Zarathushtra'); Iranian calendars "
                                            "use similar wording.",
    ("FESTIVAL", "muktad", "fa"): "Muktad is a Parsi term; Iranians call these days فروردگان or پنجه.",
    ("FESTIVAL", "khordad_sal", "fa"): "Iranian calendars often write زادروز اشو زرتشت instead.",
    ("FESTIVAL", "jashan_khordad", "gu"): "Made on zcserv's 'જશને …ગન' pattern; not printed by zcserv.",
    ("FESTIVAL", "jashan_amardad", "gu"): "Made on zcserv's 'જશને …ગન' pattern; not printed by zcserv.",
    ("FESTIVAL", "jashan_shehrevar", "gu"): "Made on zcserv's 'જશને …ગન' pattern; not printed by zcserv.",
    ("FESTIVAL", "jashan_aspandarmad", "gu"): "Made on zcserv's 'જશને …ગન' pattern; not printed by zcserv.",
    ("FESTIVAL", "chaharshanbe_suri", "gu"): "Gujarati transliteration made for the app.",
    ("FESTIVAL", "mah_niyayesh", "gu"): "Parsi name of the prayer (Mah Bokhtar Niyayesh) transliterated for the app.",
    ("CALENDAR", "bastani", "gu"): "Transliteration made for the app.",
    ("CALENDAR", "sasanian", "gu"): "Transliteration made for the app.",
    ("CALENDAR", "fasli", "gu"): "zcserv writes ફસલિ; ફસલી is also common.",
    ("ERA", "yz", "gu"): "Full Gujarati name made for the app; the abbreviation ય.ઝ. is zcserv's.",
    ("ERA", "zre", "gu"): "Made for the app.",
    ("PLACES", "*", "gu"): "Iranian place names in Gujarati, and Indian ones in Persian, are transliterations made "
                           "for the app; the Indian names in Gujarati are their standard spellings.",
}

# ------------------------------------------------------------------------------------------ build Avestan
for _tbl in (ROJ, GATHA, MAH, GAH):
    for _e in _tbl.values():
        _e["ae"] = to_avestan(_e["ae_tr"]) if _e.get("ae_tr") else None
TITLE["ae"] = to_avestan(TITLE["ae_tr"])


def roj_name(key: str) -> str:
    return fmt(ROJ[key])


def mah_name(key: str) -> str:
    return fmt(MAH[key])


def all_tables() -> dict[str, dict]:
    return {"ROJ": ROJ, "GATHA": GATHA, "MAH": MAH, "GAH": GAH, "FESTIVAL": FESTIVAL,
            "CALENDAR": CALENDAR, "ERA": ERA, "WEEKDAY": WEEKDAY, "PLACES": PLACES, "TITLE": {"title": TITLE}}
