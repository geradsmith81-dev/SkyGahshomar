"""Jashan days: a short note on what each commemorates, shown first when a festival chip is clicked.

NOTE[key] = (one or two sentences: who or what is honoured and how the day is kept, source).
The longer histories stay in festival_history.H; extra jashan days (Atash Behram salgirehs, Iranian
pilgrimages, Shab-e Yalda ...) are defined in EXTRA below and computed by extras_between().
"""
from __future__ import annotations

_B79 = "M. Boyce, Zoroastrians: Their Religious Beliefs and Practices (1979)"
_M22 = "J. J. Modi, The Religious Ceremonies and Customs of the Parsees (1922)"
_EIR = "Encyclopaedia Iranica"
_KA = "Khorda Avesta (Kanga), avesta.org"

NOTE = {
    "navroz": ("The first day of the Zoroastrian year, Hormazd roj of Fravardin mah, dedicated to Ahura Mazda and "
               "the renewal of creation. Families visit the fire temple, attend a jashan and greet one another "
               "with 'Navroz Mubarak'.", f"{_M22}; {_B79}"),
    "pateti": ("The last day of the year, a day of repentance: the Patet Pashemani is recited to review the "
               "year's thoughts, words and deeds before the New Year.", f"{_M22}; {_KA} (Patet Pashemani)"),
    "jamshedi_navroz": ("The spring-equinox New Year, linked in Iranian tradition with the legendary king Jamshid "
                        "(Yima). Parsis of every calendar keep it on 21 March with a jashan and a festive meal.",
                        f"{_M22}; Ferdowsi, Shahnameh (Jamshid)"),
    "khordad_sal": ("Khordad roj of Fravardin mah, kept as the birthday of Asho Zarathushtra. A Pahlavi text lists "
                    "many great events of sacred history on this day; Parsis hold jashans and visit the fire temple.",
                    f"{_M22}; Pahlavi 'Mah Fravardin Roj Khordad' (avesta.org)"),
    "zarthost_no_diso": ("Khorshed roj of Dae mah, the day of remembrance of Asho Zarathushtra's death, which "
                         "tradition places at Balkh. It is kept with prayers for his fravashi (Baj, Afringan, "
                         "Farokhshi) and lectures on his teaching rather than with feasting.", f"{_M22}; {_B79}"),
    "muktad": ("The days of the fravashis (Farvardegan) at the end of the year, when the souls of the departed are "
               "believed to return. Families set flowers in silver vases in a clean room or the fire temple and "
               "priests recite the Afringan, Farokhshi and Stum for each departed person.", f"{_M22}; {_B79}"),
    "farvardigan": ("Fravardin roj of Fravardin mah, honouring the fravashis of the righteous. Parsis gather at "
                    "the Doongerwadi or the aramgah for a jashan in memory of the departed.",
                    f"{_M22}; {_KA} (Farvardin Yasht)"),
    "rapithwin_jashan": ("Ardibehesht roj of Fravardin mah, when Rapithwin, the spirit of noon and of summer, "
                         "returns from beneath the earth, where he sheltered during the winter. The Rapithwin Gah "
                         "is said again from this day, with the Afrinagan of Rapithwin.",
                         "M. Boyce, 'Rapithwin, No Ruz, and the Feast of Sade' (1968); " + _KA),
    "gahambar_maidyozarem": ("The mid-spring Gahambar, linked in the Pahlavi texts with the creation of the sky. "
                             "Like every Gahambar it is a communal feast: food is shared after the Afringan and Baj.",
                             f"{_EIR}, 'Gahanbar'; Bundahishn"),
    "gahambar_maidyoshahem": ("The midsummer Gahambar, linked with the creation of water; a communal feast with "
                              "Afringan and shared meals.", f"{_EIR}, 'Gahanbar'; Bundahishn"),
    "gahambar_paitishahem": ("The harvest Gahambar, linked with the creation of the earth; a communal feast with "
                             "Afringan and shared meals.", f"{_EIR}, 'Gahanbar'; Bundahishn"),
    "gahambar_ayathrem": ("The Gahambar of the herds' return from summer pasture, linked with the creation of "
                          "plants; a communal feast.", f"{_EIR}, 'Gahanbar'; Bundahishn"),
    "gahambar_maidyarem": ("The midwinter Gahambar, linked with the creation of animals; a communal feast.",
                           f"{_EIR}, 'Gahanbar'; Bundahishn"),
    "gahambar_hamaspathmaedem": ("The Gahambar of the Gatha days at the year's end, linked with the creation of "
                                 "humankind and with the fravashis of all the departed.", f"{_EIR}, 'Gahanbar'; Bundahishn"),
    "jashan_fravardin": ("Name-day of the fravashis, the guardian spirits of the righteous: a jashan at the "
                         "Doongerwadi or the aramgah in memory of the departed.", f"{_M22}; {_KA} (Farvardin Yasht)"),
    "jashan_ardibehesht": ("Name-day of Asha Vahishta, Best Righteousness, the Amesha Spenta who guards fire. The "
                           "Ardibehesht Yasht is recited at the fire temple.", f"{_B79}; {_KA} (Ardibehesht Yasht)"),
    "jashan_khordad": ("Name-day of Haurvatat, wholeness and perfection, the Amesha Spenta who guards water.",
                       f"{_B79}; {_KA} (Khordad Yasht)"),
    "jashan_tir": ("Name-day of Tishtrya, the star Sirius who brings the rain (Tirgan). In Iran it is a summer "
                   "festival of splashing water and of the coloured band (tir-o-bad) tied on the wrist and later "
                   "thrown into running water.", f"{_KA} (Tir Yasht); {_EIR}, 'Tiragan'"),
    "jashan_amardad": ("Name-day of Ameretat, immortality, the Amesha Spenta who guards plants.",
                       f"{_B79}; {_KA} (Siroza)"),
    "jashan_shehrevar": ("Name-day of Khshathra Vairya, the desirable dominion, the Amesha Spenta who guards metals "
                         "and is linked with help for the poor.", f"{_B79}; {_KA} (Siroza)"),
    "jashan_meher": ("Name-day of Mithra, yazata of the covenant, of truth and of light (Mehergan), an autumn "
                     "feast; the Meher Niyayesh and Meher Yasht are recited.", f"{_EIR}, 'Mehragan'; {_KA} (Meher Yasht)"),
    "jashan_avan": ("Name-day of the waters and of Aredvi Sura Anahita (Avan Ardvisur nu Parab). Parsis go to the "
                    "sea, a river or a well to recite the Avan Niyayesh and offer flowers, sugar and coconut.",
                    f"{_M22}; {_KA} (Avan Niyayesh)"),
    "jashan_adar": ("Name-day of fire (Atash nu Parab). Parsis visit the fire temple to recite the Atash Niyayesh, "
                    "and the hearth at home is cleaned and honoured.", f"{_M22}; {_KA} (Atash Niyayesh)"),
    "jashan_dae": ("One of the four days of Dadvah, the Creator, in Dae mah (Hormazd, Dae-pa-Adar, Dae-pa-Meher "
                   "and Dae-pa-Din roj), dedicated to Ahura Mazda.", f"{_B79}; {_KA} (Hormazd Yasht)"),
    "jashan_bahman": ("Name-day of Vohu Manah, Good Mind, the Amesha Spenta who guards animals. Many Parsis keep "
                      "Bahman mah, or at least Bahman roj, without meat.", f"{_M22}; {_KA} (Bahman Yasht)"),
    "jashan_aspandarmad": ("Name-day of Spenta Armaiti, holy devotion, the Amesha Spenta of the earth. In Iran the "
                           "day (Sepandarmazgan) also honours women.", f"{_B79}; {_EIR}, 'Spendarmad'"),
    "sadeh": ("The midwinter fire festival, 100 days and nights after the start of winter (traditionally 50 days "
              "before Nowruz). A great bonfire is lit at sunset to drive back the cold and darkness.",
              f"{_EIR}, 'Sada'; al-Biruni, Chronology"),
    "chaharshanbe_suri": ("Iranian popular custom on the eve of the year's last Wednesday: people jump over small "
                          "bonfires. It uses the Islamic-era week, so it is a folk observance, not a Zoroastrian "
                          "rite.", f"{_EIR}, 'Cahar-sanba-suri'"),
    "tirgan_civil": ("Tirgan as kept in Iran today on 13 Tir of the civil calendar: water is splashed and the "
                     "rainbow band is thrown into running water; the day also recalls the archer Arash, whose arrow "
                     "fixed the border of Iran.", f"{_EIR}, 'Tiragan'; al-Biruni, Chronology"),
    "mah_niyayesh": ("New moon and full moon: days for the Mah Niyayesh, the litany to the Moon.", f"{_KA} (Mah Niyayesh)"),
}

# Histories for the two keys that had none (shown under the note, like festival_history.H)
HISTORY = {
    "rapithwin_jashan": (
        "In Zoroastrian teaching Rapithwin is the lord of the noon hour and of the summer half of the year. When "
        "winter comes he withdraws beneath the earth to keep the roots of plants and the springs warm, and the "
        "noon watch is then said as a second Havan. On Ardibehesht roj of Fravardin mah he returns; the Rapithwin "
        "Gah is recited again and the Afrinagan of Rapithwin is performed. Mary Boyce argued that this feast, the "
        "New Year and Sadeh belong together as a cycle marking the turn of the seasons, and that the Rapithwin "
        "feast preserves the older seasonal sense of the New Year after the calendar had drifted.",
        "M. Boyce, 'Rapithwin, No Ruz, and the Feast of Sade', in Pratidanam (1968); Bundahishn; avesta.org, "
        "Afrinagan-i Rapithwin (Khorda Avesta)"),
    "tirgan_civil": (
        "Tirgan, the feast of Tishtrya (the star Sirius) on Tir roj of Tir mah, is kept in Iran on 13 Tir of the "
        "official solar calendar, because that calendar's first six months have 31 days. Al-Biruni (c. 1000 CE) "
        "already joins two stories to it: Tishtrya's victory over the drought demon Apaosha, which brings the "
        "rain, and the archer Arash, whose arrow shot from Mount Damavand fixed the frontier between Iran and "
        "Turan. Customs include splashing water and the coloured wristband (tir-o-bad) that is worn for some "
        "days and then thrown into running water.",
        "al-Biruni, The Chronology of Ancient Nations (tr. Sachau 1879); Encyclopaedia Iranica, 'Tiragan'; "
        "Tir Yasht (Yt 8)"),
}


# ------------------------------------------------------------------------------------- extra jashan days
# Researched 24 Nov 2026 (docs/JASHAN_SOURCES.md). Each entry:
#   en, fa, gu   display names (fa/gu left empty where no sourced form exists)
#   kind         chip colour (theme.FESTIVAL_KIND)
#   rule         ("rojmah", calendar, mah_key, roj_key, days), ("civil", sh_month, sh_day, days)
#                or ("gregorian", month, day, days)
#   views        calendars whose pages show it
#   iran_only    True = an Iranian observance (shown with Bastani, or with the Parsi calendars only when
#                'Show Iranian civil observances' is on)
#   note, src    the short commemoration text and its sources
PARSI = ("shahanshahi", "kadmi", "fasli")
ALL_LIVING = ("shahanshahi", "kadmi", "fasli", "bastani")


SRC = {
    'iranshah': 'Shreeji Pak Iranshah Atashbehram Celebrates 1304th Salgreh, Parsi Times, May 2024 (https://parsi-times.com/2024/05/shreeji-pak-iranshah-atashbehram-celebrates-1304th-salgreh/); Iranshah Atash Behram Celebrates Fasli Salgreh, Parsi Times, 26 Nov 2016 (https://parsi-times.com/2016/11/iranshah-atash-behram-celebrates-fasli-salgreh/); Zoroastrian Places of Worship: Atash Bahram (K. E. Eduljee, Zoroastrian Heritage) (https://www.heritageinstitute.com/zoroastrianism/temples/atashbahram.htm); Adar Roj of Adar Mah is known as Adar nu Parab (PDF), zoroastrians.net, 2023 (https://zoroastrians.net/wp-content/uploads/2023/04/Adar-nu-Parab-Atash-nu-Varas.pdf)',
    'navsari': 'Zoroastrian Places of Worship: Atash Bahram (K. E. Eduljee, Zoroastrian Heritage) (https://www.heritageinstitute.com/zoroastrianism/temples/atashbahram.htm); Atash Behrams - India (sources: Brief History of Anjuman Atash Behram 1897-1996; M. J. Giara, Global Directory of Zoroastrian Fire Temples) (https://www.ahuramazda.com/pages/fire_temple_atash_behram_.html); Celebrating Salgrehs of Our Holy Atashbehrams On Roj-Sarosh, Mah-Ardibehesht, Parsi Times, Oct 2022 (https://parsi-times.com/2022/10/celebrating-salgrehs-of-our-holy-atashbehrams-on-roj-sarosh-mah-ardibehesht/)',
    'dadyseth': 'Dadyseth Atash Behram Celebrates Glorious 242nd Salgreh, Parsi Times, Oct 2025 (https://parsi-times.com/2025/10/dadyseth-atash-behram-celebrates-glorious-242ndsalgreh/); Dadyseth Ataš Bahrām, Encyclopaedia Iranica (citing Patell 1888, p. 86; Patell 1906, pp. 15-17); read via search-result extract only (https://www.iranicaonline.org/articles/dadyseth-atas-bahram-the-oldest-atas-bahiam-q/); Zoroastrian Places of Worship: Atash Bahram (K. E. Eduljee, Zoroastrian Heritage) (https://www.heritageinstitute.com/zoroastrianism/temples/atashbahram.htm)',
    'modi': 'Zoroastrian Places of Worship: Atash Bahram (K. E. Eduljee, Zoroastrian Heritage) (https://www.heritageinstitute.com/zoroastrianism/temples/atashbahram.htm); Celebrating Salgrehs of Our Holy Atashbehrams On Roj-Sarosh, Mah-Ardibehesht, Parsi Times, Oct 2022 (https://parsi-times.com/2022/10/celebrating-salgrehs-of-our-holy-atashbehrams-on-roj-sarosh-mah-ardibehesht/)',
    'vakil': 'The Glorious Seth Pestonji Kalabhai Vakil Kadmi Atash Behram, Parsi Times, Oct 2022 (https://parsi-times.com/2022/10/the-glorious-seth-pestonji-kalabhai-vakil-kadmi-atash-behram/); Atash Behrams - India (sources: Brief History of Anjuman Atash Behram 1897-1996; M. J. Giara, Global Directory of Zoroastrian Fire Temples) (https://www.ahuramazda.com/pages/fire_temple_atash_behram_.html)',
    'wadiaji': 'Zoroastrian Places of Worship: Atash Bahram (K. E. Eduljee, Zoroastrian Heritage) (https://www.heritageinstitute.com/zoroastrianism/temples/atashbahram.htm); Wadiaji Atash Behram Celebrates 188th Salgreh, Parsi Times, 7 Oct 2017 (https://parsi-times.com/2017/10/wadiaji-atash-behram-celebrates-188th-salgreh/); Celebrating Salgrehs of Our Holy Atashbehrams On Roj-Sarosh, Mah-Ardibehesht, Parsi Times, Oct 2022 (https://parsi-times.com/2022/10/celebrating-salgrehs-of-our-holy-atashbehrams-on-roj-sarosh-mah-ardibehesht/)',
    'banaji': 'Banaji Atashbehram Celebrates Glorious 177th Salgreh, Parsi Times, 6 Nov 2021 (https://parsi-times.com/2021/11/banaji-atashbehram-celebrates-glorious-177th-salgreh/); Parsi Calendar 2026-27 (Shahenshahi with Kadmi/Fasli; salgreh list) (https://palvkasti.com/parsi-calendar)',
    'anjuman': 'Anjuman AtashBehram Celebrates Glorious 128th Salgreh, Parsi Times, Sep 2025 (https://parsi-times.com/2025/09/anjuman-atashbehram-celebrates-glorious-128th-salgreh/); Anjuman Atash Behram Celebrates 120th Salgreh, Parsi Times, 23 Sep 2017 (https://parsi-times.com/2017/09/anjuman-atash-behram-celebrates-120th-salgreh/); Zoroastrian Places of Worship: Atash Bahram (K. E. Eduljee, Zoroastrian Heritage) (https://www.heritageinstitute.com/zoroastrianism/temples/atashbahram.htm)',
    'homaji': "Significance of Homaji's Baj, Parsi Times, 3 Jun 2023 (https://parsi-times.com/2023/06/significance-of-homajis-baj/); Weekly Zoroastrian Scripture Extract #369: Homaji ni Baj (avesta.org) (https://www.avesta.org/wzse/wzse369.pdf)",
    'kukadaru': 'Death Anniversary of Dastur Kukadaru, frashogard.com (2007) (https://www.frashogard.com/category/famous-parsis/zarathushtrian-miracles/page/3/); Zoroastrian Association of California newsletter, Jan 2024 (event calendar) (https://zacla.org/wp-content/uploads/2024/01/ZAC-2024-Jan-NL.pdf); Jamshedji Sorab Kukadaru, English Wikipedia (https://en.wikipedia.org/wiki/Jamshedji_Sorab_Kukadaru)',
    'pirs': "زردشتیان (Zardoshtiyan), Dāyerat-ol-Ma'āref-e Bozorg-e Eslāmi / Center for the Great Islamic Encyclopaedia (cgie.org.ir), read via search extract (https://www.cgie.org.ir/fa/article/246854/زردشتیان?entryviewid=246857); Pilgrimage in Zoroastrianism: The Six Pirs and Pilgrimage Calendar (K. E. Eduljee, Zoroastrian Heritage) (http://www.heritageinstitute.com/zoroastrianism/worship/pilgrimage.htm); Mary Boyce, A Persian Stronghold of Zoroastrianism (Oxford: Clarendon Press, 1977), quoted (not read directly) at tenets.parsizoroastrianism.com 'Zarathustri Pilgrimage Sites In Iran' (http://tenets.parsizoroastrianism.com/ZarathustriPilgrimageSitesInIran.html)",
    'sabz': "زردشتیان (Zardoshtiyan), Dāyerat-ol-Ma'āref-e Bozorg-e Eslāmi / Center for the Great Islamic Encyclopaedia (cgie.org.ir), read via search extract (https://www.cgie.org.ir/fa/article/246854/زردشتیان?entryviewid=246857); Pir-e Sabz / Chak-Chak (Zoroastrian Heritage) (https://www.heritageinstitute.com/zoroastrianism/worship/piresabz.htm); Chak Chak, Yazd, English Wikipedia (https://en.wikipedia.org/wiki/Chak_Chak,_Yazd); Zoroastrians Flock to Sacred Temple for Annual Pilgrimage, Parsi Khabar, 2017 (https://parsikhabar.net/iran/zoroastrians-flock-to-sacred-temple-for-annual-pilgrimage/15483/)",
    'narestaneh': "زردشتیان (Zardoshtiyan), Dāyerat-ol-Ma'āref-e Bozorg-e Eslāmi / Center for the Great Islamic Encyclopaedia (cgie.org.ir), read via search extract (https://www.cgie.org.ir/fa/article/246854/زردشتیان?entryviewid=246857); نیایش همگانی زرتشتیان در پیر نارستانه؛ نگین کوه دربید, Amordad News (https://amordadnews.com/11134/); Pilgrimage in Zoroastrianism: The Six Pirs and Pilgrimage Calendar (K. E. Eduljee, Zoroastrian Heritage) (http://www.heritageinstitute.com/zoroastrianism/worship/pilgrimage.htm)",
    'naraki': "زردشتیان (Zardoshtiyan), Dāyerat-ol-Ma'āref-e Bozorg-e Eslāmi / Center for the Great Islamic Encyclopaedia (cgie.org.ir), read via search extract (https://www.cgie.org.ir/fa/article/246854/زردشتیان?entryviewid=246857); دانستنی\u200cهایی درباره\u200cی پیر نارکی, Amordad News (https://amordadnews.com/7438/); Pilgrimage in Zoroastrianism: The Six Pirs and Pilgrimage Calendar (K. E. Eduljee, Zoroastrian Heritage) (http://www.heritageinstitute.com/zoroastrianism/worship/pilgrimage.htm)",
    'yalda': 'Yalda Night, English Wikipedia (retrieved 2026-11-24) (https://en.wikipedia.org/wiki/Yalda_Night); نماوای نیایش اورمزدیشت به خجستگی جشن\u200cهای چهارگانه دیگان, Amordad News (https://amordadnews.com/101595/); خرم\u200cروز (Deygan), Persian Wikipedia (https://fa.wikipedia.org/wiki/خرم\u200cروز)',
    'fawiki': 'Persian Wikipedia articles: فروردینگان، اردیبهشتگان، خردادگان، تیرگان، امردادگان، شهریورگان، مهرگان، آبانگان، آذرگان، خرم\u200cروز (دیگان)، بهمنگان، سپندارمذگان (retrieved via MediaWiki API 2026-11-24) (https://fa.wikipedia.org/wiki/سپندارمذگان (and sibling titles))',
}


def _x(en, kind, rule, views, note, src, fa="", gu="", iran_only=False, when=""):
    return {"en": en, "fa": fa, "gu": gu, "kind": kind, "rule": rule, "views": views, "iran_only": iran_only,
            "note": note, "src": src, "when": when}


EXTRA = {
    "salgireh_iranshah": _x(
        "Iranshah Atash Behram salgreh (Udvada)", "salgireh", ("rojmah", "shahanshahi", "adar", "adar", 1), PARSI,
        "Anniversary of the enthronement of the Iranshah, the oldest Atash Behram in India: first enthroned at "
        "Sanjan by the early Parsi settlers (traditionally 721 CE) and kept at Udvada since 1741-42. It falls on "
        "the Adar parab and is kept with a jashan by the Vada Dasturjis.", SRC["iranshah"],
        when="Adar roj, Adar mah (Shahanshahi)"),
    "salgireh_iranshah_fasli": _x(
        "Iranshah Atash Behram Fasli salgreh", "salgireh", ("rojmah", "fasli", "adar", "adar", 1), ("fasli",),
        "A second salgreh of the Iranshah is held on Adar roj of Adar mah in the Fasli calendar (24 November); "
        "some Fasli Parsis regard it as the true anniversary.", SRC["iranshah"], when="Adar roj, Adar mah (Fasli)"),
    "salgireh_navsari": _x(
        "Navsari Atash Behram salgreh", "salgireh", ("rojmah", "shahanshahi", "ardibehesht", "srosh", 1), PARSI,
        "Anniversary of the Navsari (Desai) Atash Behram, consecrated in 1765 (YZ 1135) by the Bhagarsath "
        "Anjuman; kept with a jashan and a flag (zando) procession through Navsari.", SRC["navsari"],
        when="Srosh roj, Ardibehesht mah (Shahanshahi)"),
    "salgireh_modi": _x(
        "Modi Atash Behram salgreh (Surat)", "salgireh", ("rojmah", "shahanshahi", "ardibehesht", "srosh", 1), PARSI,
        "Anniversary of Surat's Shahanshahi Atash Behram of Seth Dadabhai Naoshirwanji Modi, consecrated in 1823 "
        "(YZ 1193); kept with a machi in the Havan Gah and a flag procession.", SRC["modi"],
        when="Srosh roj, Ardibehesht mah (Shahanshahi)"),
    "salgireh_wadiaji": _x(
        "Wadiaji Atash Behram salgreh (Mumbai)", "salgireh", ("rojmah", "shahanshahi", "ardibehesht", "srosh", 1), PARSI,
        "Anniversary of the Wadiaji Atash Behram on Princess Street, Mumbai, consecrated in 1830 (YZ 1200) under "
        "Dasturji Jamshedji Edulji Jamaspasa; kept with a machi and jashans.", SRC["wadiaji"],
        when="Srosh roj, Ardibehesht mah (Shahanshahi)"),
    "salgireh_banaji": _x(
        "Banaji Atash Behram salgreh (Mumbai)", "salgireh", ("rojmah", "shahanshahi", "khordad", "srosh", 1), PARSI,
        "Anniversary of the Banaji Atash Behram at Thakurdwar, Mumbai, consecrated in 1845 (YZ 1215); kept with a "
        "morning jashan and humbandagi. Some lists label it Kadmi, but its dates follow the Shahanshahi reckoning.",
        SRC["banaji"], when="Srosh roj, Khordad mah (Shahanshahi)"),
    "salgireh_anjuman": _x(
        "Anjuman Atash Behram salgreh (Mumbai)", "salgireh", ("rojmah", "shahanshahi", "ardibehesht", "ardibehesht", 1), PARSI,
        "Anniversary of the Anjuman Atash Behram at Dhobi Talao, Mumbai, the youngest Atash Behram in India, "
        "enthroned in 1897 (YZ 1267); it falls on the Ardibehesht parab.", SRC["anjuman"],
        when="Ardibehesht roj, Ardibehesht mah (Shahanshahi)"),
    "salgireh_dadyseth": _x(
        "Dadyseth Atash Behram salgreh (Mumbai, Kadmi)", "salgireh", ("rojmah", "kadmi", "fravardin", "srosh", 1), PARSI,
        "Anniversary of the Dadyseth Atash Behram at Fanaswadi, Mumbai, the city's oldest, consecrated on "
        "29 September 1783 (YZ 1153) and kept by the Kadmi reckoning. Some printed lists give Govad roj, Aspandarmad "
        "mah, which does not match the consecration date; the temple also marks 29 September.", SRC["dadyseth"],
        when="Srosh roj, Fravardin mah (Kadmi)"),
    "salgireh_dadyseth_greg": _x(
        "Dadyseth Atash Behram anniversary (29 September)", "salgireh", ("gregorian", 9, 29, 1), PARSI,
        "The Dadyseth Atash Behram also marks the Gregorian anniversary of its consecration on 29 September 1783, "
        "besides its Kadmi roj-mah salgreh.", SRC["dadyseth"], when="29 September (Gregorian)"),
    "salgireh_vakil": _x(
        "Vakil Kadmi Atash Behram salgreh (Surat)", "salgireh", ("rojmah", "kadmi", "tir", "ardibehesht", 1), PARSI,
        "Anniversary of Surat's Kadmi Atash Behram of Seth Pestonji Kalabhai Vakil, consecrated in 1823 (YZ 1193) "
        "after a court case (1819-22) brought to stop a Kadmi Atash Behram being built.", SRC["vakil"],
        when="Ardibehesht roj, Tir mah (Kadmi)"),
    "homaji_ni_baj": _x(
        "Homaji ni Baj", "memorial", ("rojmah", "shahanshahi", "dae", "govad", 1), PARSI,
        "Death anniversary of Behdin Homaji Jamshed of Bharuch, hanged in Bombay in 1783 on false testimony during "
        "the calendar (Kabiseh) controversy. He is remembered as the patron of the falsely accused, with jashan "
        "and baj prayers.", SRC["homaji"], when="Govad roj, Dae mah (Shahanshahi)"),
    "kukadaru_birthday": _x(
        "Birthday of Dasturji Kukadaru", "memorial", ("rojmah", "shahanshahi", "avan", "zamyad", 1), PARSI,
        "Birth anniversary (1831) of Dasturji Jamshedji Sorab Kukadaru, the Bombay priest revered for his "
        "asceticism and reputed miracles, whose portrait hangs in most Atash Behrams and agiaries.", SRC["kukadaru"],
        when="Zamyad roj, Avan mah (Shahanshahi)"),
    "kukadaru_baj": _x(
        "Baj of Dasturji Kukadaru", "memorial", ("rojmah", "shahanshahi", "fravardin", "behram", 1), PARSI,
        "Death anniversary (1900) of Dasturji Kukadaru, kept with baj prayers and jashans.", SRC["kukadaru"],
        when="Behram roj, Fravardin mah (Shahanshahi)"),
    "pir_herisht": _x(
        "Pir-e Herisht pilgrimage", "pilgrimage", ("rojmah", "bastani", "fravardin", "amardad", 5), ALL_LIVING,
        "Pilgrimage to the shrine near Sharifabad (Yazd) dedicated to Morvarid, a lady-in-waiting of the fleeing "
        "Sasanian royal household, who in the legend appeared to a child and asked for the shrine.",
        SRC["pirs"], fa="پیر هریشت", iran_only=True, when="Amardad to Khorshed roj, Fravardin mah (civil 7-11 Farvardin)"),
    "pir_sabz": _x(
        "Pir-e Sabz (Chak Chak) pilgrimage", "pilgrimage", ("rojmah", "bastani", "khordad", "ashtad", 5), ALL_LIVING,
        "The great pilgrimage to the mountain grotto of Chak Chak near Ardakan, where in the legend princess "
        "Nikbanu, daughter of Yazdegerd III, was sheltered from the Arab army when the mountain opened in answer to "
        "her prayer; the dripping spring is the mountain's tears for her.", SRC["sabz"], fa="پیر سبز (چک‌چک)",
        iran_only=True, when="Ashtad to Aneran roj, Khordad mah (civil 24-28 Khordad, about 14-18 June)"),
    "pir_seti": _x(
        "Seti Pir", "pilgrimage", ("rojmah", "bastani", "khordad", "ashtad", 1), ALL_LIVING,
        "The underground shrine at Maryamabad (Yazd) dedicated to queen Hastbadan, wife of Yazdegerd III; often "
        "visited on the first day of the Pir-e Sabz pilgrimage.", SRC["pirs"], fa="ستی پیر", iran_only=True,
        when="Ashtad roj, Khordad mah (civil 24 Khordad)"),
    "pir_narestaneh": _x(
        "Pir-e Narestaneh pilgrimage", "pilgrimage", ("rojmah", "bastani", "tir", "spendarmad", 5), ALL_LIVING,
        "Pilgrimage to the shrine in the Kharanaq hills about 40 km from Yazd, associated with prince Ardeshir of "
        "the fleeing royal household.", SRC["narestaneh"], fa="پیر نارستانه", iran_only=True,
        when="Spendarmad to Adar roj, Tir mah (civil 2-6 Tir)"),
    "pir_banu": _x(
        "Pir-e Banu (Banu-Pars) pilgrimage", "pilgrimage", ("rojmah", "bastani", "tir", "meher", 5), ALL_LIVING,
        "Pilgrimage to the hillside shrine near Zarju (Ardakan), where in the legend princess Banu-Pars vanished "
        "into the mountain while fleeing the Arabs; a cleft in the rock marks the spot.", SRC["pirs"],
        fa="پیر بانو", iran_only=True, when="Meher to Behram roj, Tir mah (civil 13-17 Tir)"),
    "pir_naraki": _x(
        "Pir-e Naraki pilgrimage", "pilgrimage", ("rojmah", "bastani", "amardad", "meher", 5), ALL_LIVING,
        "Pilgrimage to the shrine in the Naraki hills near Mehriz, south of Yazd, associated in different tellings "
        "with Nazbanu, daughter of the Sasanian governor of Pars, or a daughter of Yazdegerd III.",
        SRC["naraki"], fa="پیر نارکی", iran_only=True, when="Meher to Behram roj, Amardad mah (civil 12-16 Mordad)"),
    "shab_e_yalda": _x(
        "Shab-e Yalda (Shab-e Chelleh)", "civil", ("civil", 9, 30, 1), ALL_LIVING,
        "The longest night of the year, kept on the evening of 30 Azar of the Iranian civil calendar (about "
        "21 December). Families stay awake together with pomegranates, watermelon and poetry; Iranian "
        "Zoroastrians call it Jashn-e Shab-e Chelleh. The next day, 1 Dey, al-Biruni's Khorram-ruz, is close to "
        "the Bastani Dae jashan of Hormazd roj.", SRC["yalda"], fa="شب یلدا", iran_only=True,
        when="evening of 30 Azar (Iranian civil)"),
}

# Iranian names of the name-day feasts (shown in the popover; used as the chip label in the Bastani calendar)
IRAN = {
    'jashan_fravardin': ('Farvardingan', 'فروردینگان', 'A feast of remembrance of the departed; since Zoroastrianism has no mourning rites of the usual kind, the souls of the dead are included in the rejoicing.'),
    'jashan_ardibehesht': ('Ordibeheshtgan', 'اردیبهشتگان', 'A fire feast; white clothing is worn as a sign of purity, and because it falls when flowers bloom it is also called Golestan-jashn, the feast of flowers.'),
    'jashan_khordad': ('Khordadgan', 'خردادگان', "Kept in honour of water and prosperity; Persian Wikipedia notes a survival in the 'Shast-o-Sheshi' rite of Sian village (Isfahan)."),
    'jashan_tir': ('Tirgan', 'تیرگان', "In honour of Tishtrya, the rain-bringing star: water-splashing, the fal-e kuzeh (jar augury) and the rainbow 'tir-o-bad' wrist-band."),
    'jashan_amardad': ('Amordadgan', 'امردادگان', 'Honours Amordad (immortality), guardian of plants; people traditionally went out to gardens and fields.'),
    'jashan_shehrevar': ('Shahrivargan', 'شهریورگان', "Today Zoroastrians treat it as Father's Day; historically a household fire feast."),
    'jashan_meher': ('Mehregan', 'مهرگان', 'Feast of Mehr (Mithra), regarded as the second-greatest Iranian festival after Nowruz and tied to the autumn equinox.'),
    'jashan_avan': ('Abangan', 'آبانگان', 'Honours Aban / Aredvi Sura Anahita, the waters; Persian Wikipedia describes it as kept in praise of the flowing waters.'),
    'jashan_adar': ('Azargan', 'آذرگان', 'The fire feast: fires are kindled and fire temples visited (al-Biruni via Persian Wikipedia).'),
    'jashan_dae': ('Deygan', 'دیگان', 'Four days named for the Creator (Dadar); al-Biruni says that on Khorram-ruz the king came down from his throne, dressed in white and sat with farmers. Zoroastrians gather at their places of worship on all four days.'),
    'jashan_bahman': ('Bahmangan', 'بهمنگان', 'Honours Vohu Manah (good mind), protector of useful animals; Zoroastrians abstain from slaughtering and eating them, and milk or egg is placed on the ritual spread.'),
    'jashan_aspandarmad': ('Sepandarmazgan', 'سپندارمذگان', "A day honouring women, the earth and fertility (love for 'woman, earth and generation'); al-Biruni records gifts exchanged between men and women."),
}
IRAN_SRC = 'Persian Wikipedia articles: فروردینگان، اردیبهشتگان، خردادگان، تیرگان، امردادگان، شهریورگان، مهرگان، آبانگان، آذرگان، خرم\u200cروز (دیگان)، بهمنگان، سپندارمذگان (retrieved via MediaWiki API 2026-11-24) (https://fa.wikipedia.org/wiki/سپندارمذگان (and sibling titles)); Zoroastrian festivals, English Wikipedia'


def extras_between(start, end, cal: str, **opts) -> list:
    """Extra jashan days of EXTRA that overlap [start, end], for the pages of calendar `cal`."""
    import festivals as F
    import iran_solar
    import zcalendars as zc
    import znames as zn
    o = {k: v for k, v in opts.items() if k in ("andargah", "intercalation", "kabisa_phase", "rule")}
    out = []
    for key, e in EXTRA.items():
        if cal not in e["views"]:
            continue
        rule = e["rule"]
        starts = []
        if rule[0] == "rojmah":
            _, sc, mk, rk, days = rule
            so = o if sc == cal else {}
            try:
                y0, y1 = zc.year_containing(start, sc, **so) - 1, zc.year_containing(end, sc, **so) + 1
            except ValueError:
                continue
            for y in range(y0, y1 + 1):
                try:
                    starts.append(zc.from_zdate(y, zn.MAH_NUMBER[mk], zn.ROJ_NUMBER[rk], sc, **so))
                except ValueError:
                    continue
        elif rule[0] == "gregorian":
            _, gm, gd, days = rule
            from datetime import date as _date
            starts = [_date(gy, gm, gd) for gy in range(start.year, end.year + 1)]
        else:
            _, sm, sd, days = rule
            for sy in range(start.year - 622, end.year - 620):
                try:
                    starts.append(iran_solar.from_civil(sy, sm, sd, o.get("rule", iran_solar.DEFAULT_RULE)))
                except ValueError:
                    continue
        for d in starts:
            if d <= end and d + __import__("datetime").timedelta(days=days - 1) >= start:
                try:
                    z = zc.to_zdate(d, cal, **o)
                except ValueError:
                    continue
                out.append(F.Festival(key, d, days, cal, z, e["when"], {"en": e["en"], "fa": e["fa"], "gu": e["gu"]}))
    return out


def iran_only_keys() -> set:
    return {k for k, e in EXTRA.items() if e["iran_only"]}


# make the extra days known to the rest of the app (chip names, notes, colours)
for _k, _e in EXTRA.items():
    NOTE[_k] = (_e["note"], _e["src"])


# Names made for the app (listed on the About page with the other unconfirmed spellings)
UNCERTAIN = {
    ("JASHAN", "salgireh", "fa"): "Persian legend label 'سالگرد آتش بهرام' made for the app.",
    ("JASHAN", "pilgrimage", "fa"): "Persian legend label 'زیارت پیر' made for the app.",
    **{("JASHAN", k, "fa/gu"): "No sourced Persian or Gujarati form; shown in English only."
       for k, e in EXTRA.items() if not e["fa"]},
}
