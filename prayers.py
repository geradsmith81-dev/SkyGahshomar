"""Official Zoroastrian prayers (Khorda Avesta and Yasna) with links to readable texts.

Every link points to Joseph H. Peterson's Avesta -- Zoroastrian Archives (avesta.org), which gives
the Avestan text with English translation (Khorda Avesta after Ervad K. E. Kanga; Yashts and Yasna
in the Sacred Books of the East translations by J. Darmesteter and L. H. Mills).  The app only
links to these pages; it copies no prayer text.  Section anchors (#g1, #ny3, #y28 ...) were checked
against the live pages in November 2026 (tools/check_prayer_links.py repeats the check).

Associations (which prayer belongs to which Gah or festival) follow the rubrics of the Khorda
Avesta as printed on avesta.org: the Gah prayer of each watch; Khorshed and Meher Niyayesh in the
three day watches; Srosh Yasht Vadi at night (Aiwisruthrem); Srosh Baj and Hoshbam at dawn
(Ushahin); the Afrinagan of the Gahambar for the six seasonal feasts; the Afrinagan of Rapithwin
for the Rapithwin festival; the Gatha of each Gatha day; and, for a name-day jashan, the Yasht or
Niyayesh of the yazata of that day (the Siroza where the Khorda Avesta has no separate Yasht).
"""
from __future__ import annotations

import names

AO = "https://www.avesta.org/"

# full books (PDF) offered on the Prayers page
BOOKS = [
    ("Khorda Avesta, English (Kanga)", AO + "kanga/ka_english_kanga_epub.pdf"),
    ("Khorda Avesta, Gujarati (Kanga) · ખોરદેહ અવેસ્તા", AO + "kanga/Khorda_Avesta_Kanga_Gujarati.pdf"),
    ("Khorda Avesta, Persian · خرده اوستا", AO + "ka/ka_persian.pdf"),
    ("Khorda Avesta contents (avesta.org)", AO + "ka/index.html"),
]
SOURCE_NOTE = ("Texts: Avesta -- Zoroastrian Archives (avesta.org, ed. Joseph H. Peterson). Khorda Avesta after "
               "Ervad K. E. Kanga; Yashts and Yasna in the Sacred Books of the East translations (J. Darmesteter, "
               "L. H. Mills), with some Gatha chapters in Bartholomae's translation (via I. J. S. Taraporewala). "
               "The links open the texts on that site in a new tab; the app does not copy them.")

GROUPS = [
    ("daily", "Daily prayers and the kusti"),
    ("gah", "The Gah prayers"),
    ("niyayesh", "Niyayeshes (litanies)"),
    ("yasht", "Yashts (hymns)"),
    ("afrinagan", "Afrinagans (blessings)"),
    ("gatha", "The Gathas of Zarathushtra"),
]

def _p(en, fa, gu, group, when, links):
    return {"en": en, "fa": fa, "gu": gu, "group": group, "when": when, "links": links}

_BI = "Avestan + English"
PRAYERS = {
    # ------------------------------------------------------------------ daily
    "ashem_vohu": _p("Ashem Vohu", "اشم وهو", "અશેમ વોહુ", "daily",
                     "The short invocation of Asha, said on its own and inside nearly every prayer.",
                     [(_BI, AO + "ka/ka_part1.htm#ashem")]),
    "yatha_ahu_vairyo": _p("Yatha Ahu Vairyo (Ahunwar)", "یتا اهو ویریو", "યથા અહુ વઈર્યો", "daily",
                           "The most sacred manthra; said on its own and inside nearly every prayer.",
                           [(_BI, AO + "ka/ka_part1.htm#ahunwar")]),
    "kem_na_mazda": _p("Kem Na Mazda", "کم نا مزدا", "કેમ ના મઝદા", "daily",
                       "Protective prayer said in the kusti ritual and at night.",
                       [(_BI, AO + "ka/ka_part1.htm#kemna")]),
    "kusti": _p("Padyab-Kusti (Nirang-i Kusti)", "نیرنگ کشتی", "નીરંગે કુસ્તી", "daily",
                "Ablution and untying and retying of the sacred cord, with Ohrmazd Khoday and Jasa me Avanghe "
                "Mazda; done on waking, before each Gah prayer and before meals.",
                [(_BI, AO + "ka/ka_part1.htm#nk"), ("The kusti ritual explained", AO + "ritual/ritualk.htm")]),
    "srosh_baj": _p("Srosh Baj", "سروش باج", "સરોશ બાજ", "daily",
                    "Said on rising at dawn and at the start of the Gah prayers and the Niyayeshes.",
                    [(_BI, AO + "ka/ka_part1.htm#srb")]),
    "hoshbam": _p("Hoshbam", "هوشبام", "હોશબામ", "daily",
                  "Prayer at dawn, at the end of the Ushahin Gah.",
                  [(_BI, AO + "ka/ka_part1.htm#hb")]),
    "doa_tandorosti": _p("Doa Tandorosti", "دعای تندرستی", "દોઆ તનદોરોસ્તી", "daily",
                         "Blessing for health, said for oneself or another.",
                         [(_BI, AO + "ka/ka_part1.htm#doatan")]),
    "patet": _p("Patet Pashemani", "پتت پشیمانی", "પતેત પશેમાની", "daily",
                "The prayer of repentance; said especially on the last day of the year (Pateti).",
                [(_BI, AO + "ka/ka_part1.htm#patet")]),
    "nam_setayeshne": _p("Doa Nam Setayeshne", "نام ستایش", "દોઆ નામ સેતાએશને", "daily",
                         "Praise of the name of Ahura Mazda, said after the Niyayeshes.",
                         [(_BI, AO + "ka/niyayesh.htm#ns")]),
    "vispa_humata": _p("Vispa Humata", "ویسپ هومت", "વીસ્પ હુમત", "daily",
                       "Short prayer of good thoughts, words and deeds.",
                       [(_BI, AO + "ka/niyayesh.htm#vh")]),
    # ------------------------------------------------------------------ Gahs
    "gah_havan": _p("Havan Gah prayer", names.GAH["havan"]["fa"], names.GAH["havan"]["gu"], "gah",
                    "Sunrise to noon (and the Second Havan of the winter half-year).",
                    [(_BI, AO + "ka/gahs.htm#g1")]),
    "gah_rapithwin": _p("Rapithwin Gah prayer", names.GAH["rapithwin"]["fa"], names.GAH["rapithwin"]["gu"], "gah",
                        "Noon to mid-afternoon in the Rapithwin season (Fravardin to Meher mah).",
                        [(_BI, AO + "ka/gahs.htm#g2")]),
    "gah_uziran": _p("Uziran Gah prayer", names.GAH["uziran"]["fa"], names.GAH["uziran"]["gu"], "gah",
                     "Mid-afternoon to sunset.", [(_BI, AO + "ka/gahs.htm#g3")]),
    "gah_aiwisruthrem": _p("Aiwisruthrem Gah prayer", names.GAH["aiwisruthrem"]["fa"],
                           names.GAH["aiwisruthrem"]["gu"], "gah",
                           "Sunset to midnight.", [(_BI, AO + "ka/gahs.htm#g4")]),
    "gah_ushahin": _p("Ushahin Gah prayer", names.GAH["ushahin"]["fa"], names.GAH["ushahin"]["gu"], "gah",
                      "Midnight to sunrise.", [(_BI, AO + "ka/gahs.htm#g5")]),
    # ------------------------------------------------------------------ Niyayeshes
    "khorshed_niyayesh": _p("Khorshed Niyayesh", "خورشید نیایش", "ખોરશેદ નીઆએશ", "niyayesh",
                            "Litany to the Sun; said in each of the three day watches (Havan, Rapithwin, Uziran).",
                            [(_BI, AO + "ka/niyayesh.htm#ny1")]),
    "meher_niyayesh": _p("Meher Niyayesh", "مهر نیایش", "મહેર નીઆએશ", "niyayesh",
                         "Litany to Mithra; said with the Khorshed Niyayesh in the day watches.",
                         [(_BI, AO + "ka/niyayesh.htm#ny2")]),
    "mah_niyayesh": _p("Mah Niyayesh (Mah Bokhtar)", names.FESTIVAL["mah_niyayesh"]["fa"],
                       names.FESTIVAL["mah_niyayesh"]["gu"], "niyayesh",
                       "Litany to the Moon; said at the new moon, the full moon and the half-moon.",
                       [(_BI, AO + "ka/niyayesh.htm#ny3")]),
    "avan_niyayesh": _p("Avan Ardvisur Niyayesh", "آبان نیایش", "આવાં અરદવીસુર નીઆએશ", "niyayesh",
                        "Litany to the Waters; said by day, especially on Avan roj and the Avan jashan.",
                        [(_BI, AO + "ka/niyayesh.htm#ny4")]),
    "atash_niyayesh": _p("Atash Niyayesh", "آتش نیایش", "આતશ નીઆએશ", "niyayesh",
                         "Litany to the Fire; said before a fire at any hour, especially on Adar roj.",
                         [(_BI, AO + "ka/niyayesh.htm#ny5")]),
    # ------------------------------------------------------------------ Yashts
    "hormazd_yasht": _p("Hormazd Yasht", "هرمزد یشت", "હોરમઝદ યશ્ત", "yasht",
                        "Hymn to Ahura Mazda (Yasht 1).", [(_BI, AO + "ka/yt1_bi.htm")]),
    "bahman_yasht": _p("Bahman Yasht", "بهمن یشت", "બેહમન યશ્ત", "yasht",
                       "The short Bahman Yasht, printed after the Hormazd Yasht.", [(_BI, AO + "ka/yt1_bi.htm")]),
    "ardibehesht_yasht": _p("Ardibehesht Yasht", "اردیبهشت یشت", "અરદીબહેસ્ત યશ્ત", "yasht",
                            "Hymn to Asha Vahishta (Yasht 3).", [(_BI, AO + "ka/yt3_bi.htm")]),
    "khordad_yasht": _p("Khordad Yasht", "خرداد یشت", "ખોરદાદ યશ્ત", "yasht",
                        "Hymn to Haurvatat (Yasht 4).", [(_BI, AO + "ka/yt4_bi.htm")]),
    "aban_yasht": _p("Aban Yasht (Ardvisur Yasht)", "آبان یشت", "આવાં યશ્ત", "yasht",
                     "Hymn to Aredvi Sura Anahita, the Waters (Yasht 5).",
                     [("English", AO + "ka/yt5sbe.htm"), ("Avestan", AO + "ka/yt5.htm")]),
    "tir_yasht": _p("Tir Yasht (Tishtar Yasht)", "تیر یشت", "તીર યશ્ત", "yasht",
                    "Hymn to Tishtrya, the star of rain (Yasht 8).",
                    [("English", AO + "ka/yt8sbe.htm"), ("Avestan", AO + "ka/yt8.htm")]),
    "meher_yasht": _p("Meher Yasht", "مهر یشت", "મહેર યશ્ત", "yasht",
                      "Hymn to Mithra (Yasht 10).",
                      [("English", AO + "ka/yt10sbe.htm"), ("Avestan", AO + "ka/yt10.htm")]),
    "srosh_yasht_hadokht": _p("Srosh Yasht Hadokht", "سروش یشت هادخت", "સરોશ યશ્ત હાદોખ્ત", "yasht",
                              "Hymn to Sraosha (Yasht 11).",
                              [("English", AO + "ka/yt11sbe.htm"), ("Avestan", AO + "ka/yt11.htm")]),
    "srosh_yasht_vadi": _p("Srosh Yasht Vadi", "سروش یشت سرشب", "સરોશ યશ્ત વાડી", "yasht",
                           "The great hymn to Sraosha (Yasna 57), said at night in the Aiwisruthrem Gah.",
                           [("English (Yasna 57)", AO + "yasna/yasna.htm#y57"), ("Avestan", AO + "ka/yt11a.htm")]),
    "farvardin_yasht": _p("Farvardin Yasht", "فروردین یشت", "ફરવરદીન યશ્ત", "yasht",
                          "Hymn to the Fravashis (Yasht 13); recited for the departed, above all at Muktad.",
                          [("English", AO + "ka/yt13sbe.htm"), ("Avestan", AO + "ka/yt13.htm")]),
    "behram_yasht": _p("Behram Yasht", "بهرام یشت", "બહેરામ યશ્ત", "yasht",
                       "Hymn to Verethraghna, victory (Yasht 14).",
                       [("English", AO + "ka/yt14sbe.htm"), ("Avestan", AO + "ka/yt14.htm")]),
    "siroza": _p("Siroza", "سی‌روزه", "સીરોઝા", "yasht",
                 "Invocations of the yazatas of all thirty days of the month.",
                 [("English", AO + "ka/s1sbe.htm"), ("Avestan", AO + "ka/s1.htm")]),
    # ------------------------------------------------------------------ Afrinagans
    "afrinagan_dahman": _p("Afrinagan Dahman", "آفرینگان دهمان", "આફરીનગાન દહમાન", "afrinagan",
                           "Blessing in memory of the departed.",
                           [("English", AO + "ka/a1sbe.htm"), ("Avestan", AO + "ka/a1.htm"),
                            ("About the Afrinagan", AO + "afrin/asb.htm")]),
    "afrinagan_gatha": _p("Afrinagan of the Gatha days", "آفرینگان گاتها", "આફરીનગાન ગાથા", "afrinagan",
                          "Blessing for the five Gatha days at the end of the year.",
                          [("English", AO + "ka/a2sbe.htm"), ("Avestan", AO + "ka/a2.htm")]),
    "afrinagan_gahambar": _p("Afrinagan of the Gahambar", "آفرینگان گاهنبار", "આફરીનગાન ગાહંબાર", "afrinagan",
                             "Blessing for the six seasonal Gahambar feasts.",
                             [("English", AO + "ka/a3sbe.htm"), ("Avestan", AO + "ka/a3.htm")]),
    "afrinagan_rapithwin": _p("Afrinagan of Rapithwin", "آفرینگان رپیتون", "આફરીનગાન રપીથ્વન", "afrinagan",
                              "Blessing for the Rapithwin festival that opens the summer.",
                              [("English", AO + "ka/a4sbe.htm"), ("Avestan", AO + "ka/a4.htm")]),
    # ------------------------------------------------------------------ Gathas (named like the Gatha days)
    "gatha_ahunavaiti": _p("Ahunavaiti Gatha (Yasna 28–34)", names.GATHA["ahunavad"]["fa"], names.GATHA["ahunavad"]["gu"],
                           "gatha", "Recited on the first Gatha day, Ahunavad.",
                           [("English", AO + "yasna/yasna.htm#y28"), ("Avestan", AO + "yasna/y28to34.htm#chap28")]),
    "gatha_ushtavaiti": _p("Ushtavaiti Gatha (Yasna 43–46)", names.GATHA["ushtavad"]["fa"], names.GATHA["ushtavad"]["gu"],
                           "gatha", "Recited on the second Gatha day, Ushtavad.",
                           [("English", AO + "yasna/yasna.htm#y43"), ("Avestan", AO + "yasna/y43to46.htm")]),
    "gatha_spentamainyu": _p("Spentamainyu Gatha (Yasna 47–50)", names.GATHA["spentomad"]["fa"], names.GATHA["spentomad"]["gu"],
                             "gatha", "Recited on the third Gatha day, Spentomad.",
                             [("English", AO + "yasna/yasna.htm#y47"), ("Avestan", AO + "yasna/y47to50.htm")]),
    "gatha_vohukhshathra": _p("Vohukhshathra Gatha (Yasna 51)", names.GATHA["vohukhshathra"]["fa"],
                              names.GATHA["vohukhshathra"]["gu"], "gatha", "Recited on the fourth Gatha day, Vohukhshathra.",
                              [("English", AO + "yasna/yasna.htm#y51"), ("Avestan", AO + "yasna/y51.htm")]),
    "gatha_vahishtoishti": _p("Vahishtoishti Gatha (Yasna 53)", names.GATHA["vahishtoisht"]["fa"],
                              names.GATHA["vahishtoisht"]["gu"], "gatha", "Recited on the fifth Gatha day, Vahishtoisht.",
                              [("English", AO + "yasna/yasna.htm#y53"), ("Avestan", AO + "yasna/y53.htm")]),
}

# which prayers belong to each Gah (kusti first, as the prayers of a watch begin with it)
GAH_PRAYERS = {
    "havan": ["kusti", "srosh_baj", "gah_havan", "khorshed_niyayesh", "meher_niyayesh"],
    "second_havan": ["kusti", "srosh_baj", "gah_havan", "khorshed_niyayesh", "meher_niyayesh"],
    "rapithwin": ["kusti", "srosh_baj", "gah_rapithwin", "khorshed_niyayesh", "meher_niyayesh"],
    "uziran": ["kusti", "srosh_baj", "gah_uziran", "khorshed_niyayesh", "meher_niyayesh"],
    "aiwisruthrem": ["kusti", "srosh_baj", "gah_aiwisruthrem", "srosh_yasht_vadi", "mah_niyayesh"],
    "ushahin": ["kusti", "srosh_baj", "gah_ushahin", "hoshbam"],
}

# readings for the festivals (name-day jashans: the Yasht or Niyayesh of the day's yazata)
FESTIVAL_PRAYERS = {
    "pateti": ["patet"],
    "muktad": ["farvardin_yasht", "afrinagan_dahman", "afrinagan_gatha"],
    "farvardigan": ["farvardin_yasht", "afrinagan_dahman"],
    "khordad_sal": ["khordad_yasht"],
    "rapithwin_jashan": ["afrinagan_rapithwin", "ardibehesht_yasht"],
    "gahambar_maidyozarem": ["afrinagan_gahambar"], "gahambar_maidyoshahem": ["afrinagan_gahambar"],
    "gahambar_paitishahem": ["afrinagan_gahambar"], "gahambar_ayathrem": ["afrinagan_gahambar"],
    "gahambar_maidyarem": ["afrinagan_gahambar"], "gahambar_hamaspathmaedem": ["afrinagan_gahambar", "afrinagan_gatha"],
    "jashan_fravardin": ["farvardin_yasht"],
    "jashan_ardibehesht": ["ardibehesht_yasht"],
    "jashan_khordad": ["khordad_yasht"],
    "jashan_tir": ["tir_yasht"], "tirgan_civil": ["tir_yasht"],
    "jashan_amardad": ["siroza"],
    "jashan_shehrevar": ["siroza"],
    "jashan_meher": ["meher_yasht", "meher_niyayesh"],
    "jashan_avan": ["avan_niyayesh", "aban_yasht"],
    "jashan_adar": ["atash_niyayesh"], "sadeh": ["atash_niyayesh"],
    "jashan_dae": ["hormazd_yasht"],
    "jashan_bahman": ["bahman_yasht"],
    "jashan_aspandarmad": ["siroza"],
    "mah_niyayesh": ["mah_niyayesh"],
    # extra jashan days (jashans.py): a fire's salgreh is kept with the Atash Niyayesh; a baj with the Afrinagan
    **{k: ["atash_niyayesh"] for k in ("salgireh_iranshah", "salgireh_iranshah_fasli", "salgireh_navsari",
                                        "salgireh_modi", "salgireh_wadiaji", "salgireh_banaji", "salgireh_anjuman",
                                        "salgireh_dadyseth", "salgireh_dadyseth_greg", "salgireh_vakil")},
    "homaji_ni_baj": ["afrinagan_dahman"], "kukadaru_baj": ["afrinagan_dahman"],
}

GATHA_DAY_PRAYERS = {
    "ahunavad": ["gatha_ahunavaiti", "afrinagan_gatha"], "ushtavad": ["gatha_ushtavaiti", "afrinagan_gatha"],
    "spentomad": ["gatha_spentamainyu", "afrinagan_gatha"], "vohukhshathra": ["gatha_vohukhshathra", "afrinagan_gatha"],
    "vahishtoisht": ["gatha_vahishtoishti", "afrinagan_gatha"], "avardad_sal_gah": ["afrinagan_gatha"],
}

# Persian and Gujarati prayer names made for this app (not copied from a source): listed on the About page
UNCERTAIN = {("PRAYER", k, f): "Prayer name made for the app from common Parsi/Iranian usage; not checked against a printed Khorda Avesta."
             for k, v in PRAYERS.items() if v["group"] not in ("gah", "gatha") and k != "mah_niyayesh"
             for f in ("fa", "gu")}


def all_urls():
    out = {u for _, u in BOOKS}
    for v in PRAYERS.values():
        out.update(u for _, u in v["links"])
    return sorted(out)
