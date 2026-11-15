"""Zoroastrian communities and the calendars by which each keeps its days.

Each entry gives the calendars a community uses, with a preset of the app's settings that models its
practice (calendar, length of the Muktad, Rapithwin practice, era shown). Practice varies inside every
community and changes over time; the presets are models, and the notes say whose practice they follow.
Historical movements (Zurvanism, Mazdakism) and the term "Gabar" are notes only, with no preset: no
living community keeps a calendar under those names.

Sources: the works named in each entry were read (in full, or in the passage cited) when this list was
made (November 2026) unless marked "background" in SOURCES.md. Encyclopaedia Iranica articles were read
through search-engine extracts (the site refuses automated access); that limit is recorded in SOURCES.md.

Calendar keys (shared contract): shahanshahi, kadmi, fasli, bastani, sasanian.
Preset keys:
  calendar     one of the calendar keys
  muktad_days  10 (last five days of Aspandarmad + five Gatha days) or 18 (extended Muktad kept by some
               Indian families; counted back from the last Gatha day, see MUKTAD_NOTE)
  rapithwin    "summer"        Rapithwin Gah from Hormazd roj of Fravardin mah to Aneran roj of Meher mah;
                               Second Havan in its place for the other five months and the Gatha days
               "medieval_four" the Bundahishn's winter rule: no Rapithwin and no Second Havan in the five
                               winter months; Havan runs on until Uzerin (used only for the Sasanian model)
  era          "yz" (Yazdegerdi, from 16 June 632), "zre" (Zarathushtrian Religious Era, 1738 BCE),
               or "yz+zre" (both shown)
"""
from __future__ import annotations

GROUPS = [
    ("Parsis (India and Pakistan)", "پارسیان", "પારસી"),
    ("Zoroastrians of Iran", "زرتشتیان ایران", "ઈરાની જરથોસ્તી"),
    ("Movements and diaspora", "جنبش‌ها و پراکندگان", "ચળવળો અને પરદેશ વસતા"),
]

# The 18-day Muktad: the extension is attested (Wikipedia, "Zoroastrian festivals", which notes that among
# Indian Zoroastrians "an extended mukhtad of eighteen days is also observed"); the exact first day varies
# by family and is therefore a user setting, not a rule. 18 days ending on the last Gatha day begin on
# roj 18 (Rashne) of Aspandarmad mah when counted back from the 5th Gatha day.
MUKTAD_NOTE = ("Ten days is the common reckoning: the last five days of Aspandarmad mah and the five Gatha "
               "days. Some Indian families keep an extended Muktad of eighteen days; the starting day "
               "varies by family, so the app treats 18 as a setting counted back from the last Gatha day.")

SECTS = [
    # --------------------------------------------------------------------------- Parsis
    {"key": "parsi_shahanshahi", "name": "Parsi Shahanshahi (Shenshai)", "fa": "پارسیان شاهنشاهی",
     "gu": "શહેનશાહી પારસી", "group": "Parsis (India and Pakistan)", "parent": None,
     "where": "India (Mumbai, Gujarat), Pakistan (Karachi), and the Parsi diaspora",
     "how": "The majority of Parsis keep the Shahanshahi reckoning: twelve months of thirty days and five "
            "Gatha days, with no leap day. Its year runs one month behind the Iranian (Kadmi) reckoning "
            "because the Parsis inserted a thirteenth month once, between 1125 and 1129, and never again. "
            "Navroz therefore moves one day earlier in the Gregorian year every four years; for 2026 "
            "zcserv.com gives 15 August, though other published calendars give 16 August (to be settled by "
            "the app's validation). Years are counted from the accession of Yazdegerd III (Y.Z.). Rapithwin is "
            "recited in the seven 'summer' months of the calendar, which no longer fall in summer.",
     "uses": [("shahanshahi", "Shahanshahi reckoning, Y.Z. years",
               {"calendar": "shahanshahi", "muktad_days": 10, "rapithwin": "summer", "era": "yz"}),
              ("shahanshahi", "Shahanshahi with the extended 18-day Muktad",
               {"calendar": "shahanshahi", "muktad_days": 18, "rapithwin": "summer", "era": "yz"})],
     "src": "Encyclopaedia Iranica, 'Kadimi' (Shenshahis as 'the majority of traditionalist Parsis'); "
            "Wikipedia, 'Zoroastrian calendar' (intercalation of c. 1125-1129) and 'Parsis'; "
            "Zoroastrian Calendar Services (zcserv.com), year view 2026"},
    {"key": "parsi_kadmi", "name": "Parsi Kadmi (Qadimi)", "fa": "پارسیان قدیمی", "gu": "કદમી પારસી",
     "group": "Parsis (India and Pakistan)", "parent": "parsi_shahanshahi", "since": "1745/46",
     "where": "Surat and Bharuch (historic strongholds), Mumbai (Dadyseth Atash Behram), and abroad",
     "how": "In 1721 the Kerman priest Jamasp Vilayati, visiting Surat, noticed that the Parsi calendar ran "
            "a month behind the Iranian one. In 1745 a Surat high priest and his followers dropped a month "
            "to agree with Iran; other accounts give 1746. Mulla Kaus, sent to Iran in 1767 to study the "
            "question, later became the first Kadmi dastur of the Dadyseth Atash Behram in Bombay. The "
            "Kadmi calendar is the Iranian 'Qadimi' reckoning: the same rules as the Shahanshahi, one month "
            "ahead. About 15 percent of Parsis followed it early in the 20th century, 7 percent by the early "
            "1970s.",
     "uses": [("kadmi", "Kadmi reckoning, Y.Z. years",
               {"calendar": "kadmi", "muktad_days": 10, "rapithwin": "summer", "era": "yz"})],
     "src": "Encyclopaedia Iranica, 'Kadimi' (1721 visit; 1745 adjustment; Mulla Kaus; percentages after "
            "Bajan and Kulke) and 'Dadyseth, Dadibhai Noshirwanji' (Kadmi movement 'started in Surat in "
            "1746'); D. Menant, Les Parsis (1898; Eng. tr. 'The Parsis', Project Gutenberg 29109)"},
    {"key": "fasli_parsi", "name": "Fasli Parsis", "fa": "پارسیان فصلی", "gu": "ફસલી પારસી",
     "group": "Parsis (India and Pakistan)", "parent": "parsi_shahanshahi", "since": "1906",
     "where": "A minority in India and Pakistan; widespread in North America and Britain",
     "how": "K. R. Cama (1831-1909) argued in the 1860s that both Parsi calendars had lost the seasons. "
            "In 1906 the Zarthosti Fasli Sal Mandal in Bombay published a seasonal calendar: Navroz fixed on "
            "the March equinox (21 March), and a sixth Gatha day, Avardad-sal-gah, added in leap years so "
            "that the year keeps step with the Gregorian. Few Parsis adopted it, many holding that a leap "
            "day contradicts the Denkard; it is widely used outside India. Fasli Parsis count Y.Z. years; "
            "some also show the Zarathushtrian Religious Era.",
     "uses": [("fasli", "Fasli: Navroz on 21 March, Gregorian leap rule",
               {"calendar": "fasli", "muktad_days": 10, "rapithwin": "summer", "era": "yz"})],
     "src": "Wikipedia, 'Zoroastrian calendar' (Fasli section) and 'Kharshedji Rustomji Cama'; ZANC, "
            "'About Zoroastrian Calendars' (zanc.org); A. A. Jafarey, 'The Precise Iranian Calendar' "
            "(zoroastrian.org)"},
    {"key": "khshnoom", "name": "Ilm-e Khshnoom", "fa": "علم خشنوم", "gu": "ઇલ્મે ખ્શ્નૂમ",
     "group": "Movements and diaspora", "parent": "parsi_shahanshahi", "since": "early 1900s",
     "where": "A small circle of Parsis in Mumbai (Behram Baug) and elsewhere",
     "how": "A mystical school founded by Behramshah Nowroji Shroff (d. 1927), who taught that he had "
            "learned an esoteric Zoroastrianism from the hidden Saheb-e-Dilan; it was spread from about "
            "1909 by Phiroze Masani's journal Frashogard. Its followers are strict traditionalists in ritual "
            "and keep the Shahanshahi calendar of the Parsi majority. The preset is that calendar; the "
            "school's distinctive teachings (reincarnation, vegetarianism) do not change the dates.",
     "uses": [("shahanshahi", "Shahanshahi reckoning (as kept by the Parsi majority)",
               {"calendar": "shahanshahi", "muktad_days": 10, "rapithwin": "summer", "era": "yz"})],
     "src": "Wikipedia, 'Ilm-e-Khshnoom'; Frashogard (frashogard.com), which dates events by Shahenshahi "
            "roj and mah. UNCERTAIN: no doctrinal statement on the calendar was found; the Shahanshahi "
            "preset rests on the movement's own publications using Shahenshahi dates."},
    # --------------------------------------------------------------------------- Iran
    {"key": "iranian_bastani", "name": "Iranian Zoroastrians (Bastani)", "fa": "زرتشتیان ایران (گاهشماری باستانی)",
     "gu": "ઈરાની જરથોસ્તી (બાસ્તાની)", "group": "Zoroastrians of Iran", "parent": "iranian_qadimi",
     "since": "1939",
     "where": "Tehran, Yazd, Kerman, and the Iranian Zoroastrian diaspora",
     "how": "Iran's civil calendar of 1925 kept the Zoroastrian month names and began the year at the "
            "March equinox. Keikhosrow Shahrokh, the Zoroastrian member of parliament, promoted a matching "
            "religious calendar, called Bastani ('ancient'), and in 1939 the community adopted it; Tehran "
            "took it up quickly, the conservative villages of Yazd slowly. Nowruz is kept on the day of "
            "the equinox. Since the 1990s Iranian Zoroastrians also count a 'religious year' (sal-e dini) "
            "from 1738 BCE, the era the Zarathushtrian Assembly calls ZRE.",
     "uses": [("bastani", "Bastani: Nowruz on the day of the March equinox",
               {"calendar": "bastani", "muktad_days": 10, "rapithwin": "summer", "era": "yz+zre"})],
     "src": "P. Niechcial, 'Calendar as an identity marker of the Zoroastrian community in Iran', Iran and "
            "the Caucasus 23 (2019) 35-49, and the same author's chapter on Tehran Zoroastrians (Springer, "
            "2022), note on the 1939 adoption and sal-e dini; Heritage Institute, 'Zoroastrian Calendar' "
            "(Shahrokh; 1939); Zoroastrian Trust Funds of Europe briefing quoted in Wikipedia, 'Zoroastrian "
            "calendar'"},
    {"key": "iranian_qadimi", "name": "Yazdi and Sharifabadi Qadimi traditionalists",
     "fa": "زرتشتیان سنت‌گرای یزد و شریف‌آباد (قدیمی)", "gu": "યઝદ અને શરીફાબાદના કદીમી",
     "group": "Zoroastrians of Iran", "parent": None,
     "where": "Villages of the Yazd plain, above all Sharifabad-e Ardakan",
     "how": "The Qadimi ('old') reckoning is the calendar Iranian Zoroastrians kept through the Islamic "
            "centuries, without any intercalation; it is the calendar the Parsi Kadmis adopted. When "
            "Tehran took up the Bastani calendar in 1939, many orthodox villagers of Yazd, above all at "
            "Sharifabad, kept the Qadimi calendar for their religious year. Mary Boyce's fieldwork there "
            "(1963-64) describes the feasts and the ten-day Farvardigan by this reckoning.",
     "uses": [("kadmi", "Qadimi reckoning (identical to the Parsi Kadmi count)",
               {"calendar": "kadmi", "muktad_days": 10, "rapithwin": "summer", "era": "yz"})],
     "src": "M. Boyce, A Persian Stronghold of Zoroastrianism (Oxford, 1977); Heritage Institute, "
            "'Zoroastrian Calendar' ('the Sharifabadi Yazdis continued to use the Qadimi calendar'); "
            "Wikipedia, 'Zoroastrian calendar' (Fasli section). Present-day extent of Qadimi use in Yazd is "
            "not documented in the sources read; treat it as historical-to-recent."},
    {"key": "iranis_india", "name": "Iranis in India", "fa": "ایرانیان (زرتشتیان ایرانی‌تبار هند)",
     "gu": "ઈરાની", "group": "Zoroastrians of Iran", "parent": "iranian_qadimi",
     "since": "19th-20th c. migration",
     "where": "Mumbai, Pune, Hyderabad and other Indian cities",
     "how": "Descendants of Zoroastrians who left Qajar Iran, mostly from Yazd and Kerman, in the 19th and "
            "early 20th centuries. They had kept the Qadimi calendar in Iran and by and large joined the "
            "Kadmi fire temples already founded in India. Many also mark Nowruz at the March equinox as "
            "Iranians do. Two presets are offered.",
     "uses": [("kadmi", "Kadmi temples (the Qadimi reckoning brought from Iran)",
               {"calendar": "kadmi", "muktad_days": 10, "rapithwin": "summer", "era": "yz"}),
              ("bastani", "Iranian Nowruz at the equinox",
               {"calendar": "bastani", "muktad_days": 10, "rapithwin": "summer", "era": "yz+zre"})],
     "src": "Wikipedia, 'Irani (India)'; Heritage Institute, 'Zoroastrian Calendar' (Qajar-era migrants "
            "'by-and-large joined the Kadmi denomination'); Times of India (Mumbai), 'Irani New Year to be "
            "celebrated today and tomorrow' (2017), cited by Wikipedia 'Indian New Year's days'"},
    # --------------------------------------------------------------------------- movements, diaspora
    {"key": "reformist_zre", "name": "Reformist and diaspora groups using ZRE (e.g. Zarathushtrian Assembly)",
     "fa": "گروه‌های اصلاح‌گرا و برون‌مرزی (مانند انجمن زرتشتی کالیفرنیا)", "gu": "સુધારાવાદી અને પરદેશી સમુદાયો",
     "group": "Movements and diaspora", "parent": "iranian_bastani", "since": "1990",
     "where": "North America (founded in Los Angeles), Europe, Iran",
     "how": "The Zarathushtrian Assembly, founded in Los Angeles in 1990 by Ali A. Jafarey and others, "
            "teaches a Gathas-centred religion open to converts. It follows the precise Iranian solar "
            "calendar, with Nowruz at the moment of the March equinox, and counts years in the "
            "Zarathushtrian Religious Era (ZRE) from the equinox of 1738 BCE (year 3738 began in 2000). "
            "Many diaspora associations print both Shahanshahi and Fasli dates; the Zoroastrian Trust "
            "Funds of Europe marks both.",
     "uses": [("bastani", "Nowruz at the equinox, ZRE years",
               {"calendar": "bastani", "muktad_days": 10, "rapithwin": "summer", "era": "zre"}),
              ("fasli", "Fasli calendar (21 March), ZRE years",
               {"calendar": "fasli", "muktad_days": 10, "rapithwin": "summer", "era": "zre"})],
     "src": "A. A. Jafarey, 'The Precise Iranian Calendar, made simple' and 'The Good Religion and the "
            "Institutionalized Zoroastrianism' (zoroastrian.org; CAIS); Wikipedia, 'Zoroastrian calendar' "
            "(ZRE; ZTFE practice)"},
]

# Historical currents and terms: notes only, no presets.
HISTORICAL = [
    {"key": "zurvanism", "name": "Zurvanism", "fa": "زروانی‌گری", "period": "Achaemenid to Sasanian era",
     "note": "A theological current, not a separate church, that made Zurvan (Time) the father of both "
             "Ohrmazd and Ahriman. Greek writers (Eudemus, quoted by Damascius) knew of it, and Armenian "
             "and Syriac Christian polemic of the 5th century attributes it to Sasanian Zoroastrians. It "
             "had no calendar of its own: Zurvanites worshipped by the same 365-day Zoroastrian year. "
             "Zurvan is invoked in the Siroza (1.21) among the companions of Vayu.",
     "src": "R. C. Zaehner, Zurvan: A Zoroastrian Dilemma (Oxford, 1955), background; Siroza 1.21 "
            "(Geldner, via TITUS); Wikipedia, 'Zurvanism'"},
    {"key": "mazdakism", "name": "Mazdakism", "fa": "مزدکیان", "period": "late 5th-early 6th century",
     "note": "A religious and social movement of the reign of Kavad I, led by Mazdak, preaching common "
             "ownership and non-violence; it was suppressed with great bloodshed under Khosrow I (c. 528). "
             "Later Islamic-era writers report survivals in Iran. Nothing indicates a calendar of its own.",
     "src": "Encyclopaedia Iranica, 'Mazdak' (background); Wikipedia, 'Mazdakism'"},
    {"key": "gabar", "name": "Gabar (Gabr)", "fa": "گبر", "period": "Islamic period",
     "note": "Not a sect: a Persian word for a Zoroastrian, probably from an Aramaic ideogram for 'man', "
             "which became a slur; the community's own name is Zartoshti or Behdin. It appears in the app "
             "only to explain old sources and place names (e.g. 'Gabristan').",
     "src": "Wikipedia, 'Gabr' (after Encyclopaedia Iranica, 'Gabr')"},
]

CAL_ORDER = [
    ("shahanshahi", "Shahanshahi (Parsi majority)"),
    ("kadmi", "Kadmi / Qadimi (Iranian old reckoning)"),
    ("fasli", "Fasli (21 March, Gregorian leap day)"),
    ("bastani", "Bastani (Iran, Nowruz at the equinox)"),
    ("sasanian", "Sasanian (reconstruction, for comparison)"),
]

# ------------------------------------------------------------------------------------------------
# Branch diagram for the Traditions page (the app draws it as SVG).
# Lanes are columns left to right; 'y' is a sort year (negative = BCE) for vertical placement only.
# kind: "historic" (no living community), "living" (has a preset), "note" (historical current).
# Edge style: "split" (solid: a community separated), "adopt" (dashed: took up another's reckoning),
# "migrate" (dotted: people moved).
BRANCH_DIAGRAM = {
    "nodes": [
        {"id": "sasanian", "label": "Sasanian Zoroastrianism", "fa": "دین ساسانی", "when": "224-651",
         "y": 224, "lane": 2, "kind": "historic"},
        {"id": "zurvanism", "label": "Zurvanite current", "fa": "زروانی‌گری", "when": "to 7th c.",
         "y": 400, "lane": 0, "kind": "note"},
        {"id": "mazdakism", "label": "Mazdakite movement", "fa": "مزدکیان", "when": "c. 490-530",
         "y": 500, "lane": 4, "kind": "note"},
        {"id": "iranian_qadimi", "label": "Zoroastrians of Iran (Qadimi)", "fa": "زرتشتیان ایران (قدیمی)",
         "when": "651-", "y": 651, "lane": 3, "kind": "living"},
        {"id": "parsis", "label": "Parsis settle in Gujarat", "fa": "پارسیان در گجرات",
         "when": "8th-10th c. (traditional; debated)", "y": 900, "lane": 1, "kind": "historic"},
        {"id": "parsi_shahanshahi", "label": "Shahanshahi Parsis", "fa": "پارسیان شاهنشاهی",
         "when": "month added c. 1125-1129", "y": 1127, "lane": 1, "kind": "living"},
        {"id": "parsi_kadmi", "label": "Kadmi Parsis", "fa": "پارسیان قدیمی", "when": "1745/46",
         "y": 1745, "lane": 2, "kind": "living"},
        {"id": "iranis_india", "label": "Iranis in India", "fa": "ایرانیان هند", "when": "19th-20th c.",
         "y": 1850, "lane": 3, "kind": "living"},
        {"id": "fasli_parsi", "label": "Fasli Parsis", "fa": "پارسیان فصلی", "when": "1906",
         "y": 1906, "lane": 0, "kind": "living"},
        {"id": "khshnoom", "label": "Ilm-e Khshnoom", "fa": "علم خشنوم", "when": "early 1900s",
         "y": 1909, "lane": 1, "kind": "living"},
        {"id": "iranian_bastani", "label": "Iranian Bastani", "fa": "گاهشماری باستانی", "when": "1939",
         "y": 1939, "lane": 4, "kind": "living"},
        {"id": "reformist_zre", "label": "Zarathushtrian Assembly (ZRE)", "fa": "انجمن زرتشتی (سال دینی)",
         "when": "1990", "y": 1990, "lane": 4, "kind": "living"},
    ],
    "edges": [
        {"from": "sasanian", "to": "zurvanism", "style": "split", "label": "theological current"},
        {"from": "sasanian", "to": "mazdakism", "style": "split", "label": "suppressed c. 528"},
        {"from": "sasanian", "to": "iranian_qadimi", "style": "split", "label": "after 651"},
        {"from": "iranian_qadimi", "to": "parsis", "style": "migrate", "label": "emigration (Qissa-i Sanjan)"},
        {"from": "parsis", "to": "parsi_shahanshahi", "style": "split", "label": "one month intercalated"},
        {"from": "parsi_shahanshahi", "to": "parsi_kadmi", "style": "split", "label": "drops a month, Surat"},
        {"from": "iranian_qadimi", "to": "parsi_kadmi", "style": "adopt", "label": "Iranian reckoning adopted"},
        {"from": "iranian_qadimi", "to": "iranis_india", "style": "migrate", "label": "Qajar-era emigration"},
        {"from": "iranis_india", "to": "parsi_kadmi", "style": "adopt", "label": "join Kadmi temples"},
        {"from": "parsi_shahanshahi", "to": "fasli_parsi", "style": "split", "label": "Fasli Sal Mandal, Bombay"},
        {"from": "parsi_shahanshahi", "to": "khshnoom", "style": "split", "label": "B. N. Shroff"},
        {"from": "iranian_qadimi", "to": "iranian_bastani", "style": "split", "label": "Tehran Anjoman"},
        {"from": "fasli_parsi", "to": "iranian_bastani", "style": "adopt", "label": "Fasli model (Shahrokh)"},
        {"from": "iranian_bastani", "to": "reformist_zre", "style": "split", "label": "Los Angeles"},
    ],
    "caption": ("Who separated from whom, and when. Solid lines: a community separated over the calendar "
                "or doctrine. Dashed: a community adopted another's reckoning. Dotted: migration. The date "
                "of the Parsi settlement in Gujarat rests on the Qissa-i Sanjan (1599/1600) and is debated."),
}


def by_calendar() -> dict[str, list[tuple[dict, str, dict]]]:
    """Communities grouped by the calendar of each preset, in CAL_ORDER."""
    out = {k: [] for k, _ in CAL_ORDER}
    for s in SECTS:
        for cal, label, preset in s["uses"]:
            out.setdefault(cal, []).append((s, label, preset))
    return out


def preset(sect_key: str, index: int = 0) -> dict:
    """The settings preset of a community (first preset by default)."""
    for s in SECTS:
        if s["key"] == sect_key:
            return dict(s["uses"][index][2])
    raise KeyError(sect_key)
