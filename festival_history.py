"""Short histories of the festivals and calendars, opened by clicking a festival's or calendar's name.

Each entry: a few sentences of history (80-150 words) and the main sources. Titles and Persian names come
from names.py so that every page spells them the same way. Where an archaeological link is debated, the
text says so; where a custom is reported by one medieval author only, the text names him.

Abbreviations in the source lines:
  Biruni, Chronology = al-Biruni, al-Athar al-baqiya (c. 1000), tr. E. Sachau, The Chronology of Ancient
                       Nations (London, 1879)
  Boyce 1977         = M. Boyce, A Persian Stronghold of Zoroastrianism (Oxford, 1977)
  Boyce 1968         = M. Boyce, 'Rapithwin, No Ruz, and the Feast of Sade', in Pratidanam (The Hague, 1968)
  Modi 1922          = J. J. Modi, The Religious Ceremonies and Customs of the Parsees (Bombay, 1922)
  EIr                = Encyclopaedia Iranica (iranicaonline.org)
  Yt, Y, Vr, S       = Yasht, Yasna, Vispered, Siroza of the Avesta (Geldner's text, via TITUS)
"""
from __future__ import annotations

import html

from names import CALENDAR, FESTIVAL

# key -> (text, sources)
H = {
    "navroz": (
        "Navroz, 'new day', is Hormazd roj of Fravardin mah, the first day of the year. Zoroastrian "
        "tradition makes it the day of creation and an image of the final renewal, and its noon service "
        "welcomes back Rapithwin, the spirit of the summer noon, from his winter retreat beneath the earth. "
        "Because the Shahanshahi and Kadmi years have no leap day, their Navroz has drifted from spring to "
        "August and July; Fasli and Iranian Zoroastrians keep it at the March equinox. Biruni describes a "
        "Lesser Nowruz on the first day and a Greater Nowruz on the sixth. The tribute processions on the "
        "Apadana stairways at Persepolis are often presented as a New Year ceremony, but no Achaemenid text "
        "names the festival, and many archaeologists read the reliefs as a timeless image of empire rather "
        "than a record of Nowruz.",
        "Boyce 1968; Biruni, Chronology; M. C. Root, The King and Kingship in Achaemenid Art (Acta Iranica 19, "
        "1979); EIr, 'Nowruz i. In the pre-Islamic period'"),
    "pateti": (
        "Pateti takes its name from patet, the Middle Persian word for repentance and for the confessional "
        "prayer (Patet Pashemani) in which a Zoroastrian renounces sins of thought, word and deed. Parsis "
        "keep it on the last day of the year, the fifth Gatha day, Vahishtoisht, as a day of stock-taking "
        "before Navroz; Gujarati writers compare it to the last day of the Vikram year before Diwali. Older "
        "practice spread the self-examination over the last five days. Failure to keep Rapithwin is itself "
        "one of the sins named in the Middle Persian patet formularies. In popular usage 'Pateti' is often "
        "used loosely for Navroz, the following day; the app keeps the two apart. The Iranian calendars "
        "have no festival of this name.",
        "Gujarati Wikipedia, 'પતેતી'; Wikipedia, 'Zoroastrian festivals'; EIr, 'Rapithwin' (patet "
        "formularies), as summarised in Wikipedia, 'Rapithwin'; Modi 1922 (background)"),
    "jamshedi_navroz": (
        "Jamshedi Navroz is the New Year at the March equinox, named after the legendary king Jamshid. The "
        "Shahnameh tells how Jamshid, having set the world in order, had his throne raised into the air on "
        "the day of Hormazd in the month of Fravardin, and the people called that day the New Day; Biruni "
        "records the same story. Parsis of the Shahanshahi and Kadmi calendars, whose own Navroz now falls "
        "in late summer, keep 21 March as Jamshedi Navroz with prayers and a festive table, so that the "
        "spring New Year is not lost. For Fasli Parsis and Iranian Zoroastrians the two coincide. In Iran "
        "the day is Nowruz, the first day of the civil year, kept by Iranians of every faith.",
        "Ferdowsi, Shahnameh, reign of Jamshid; Biruni, Chronology; Wikipedia, 'Zoroastrian festivals'"),
    "khordad_sal": (
        "Khordad Sal is Khordad roj of Fravardin mah, the sixth day of the year, kept as the birthday of "
        "Zarathushtra. In late Sasanian reckoning this was the Greater Nowruz: Biruni reports that King "
        "Hormizd, son of Shapur, joined the days from the first to the sixth into one festival. A Middle "
        "Persian text, Mah Fravardin Roz Hordad, lists great events of the past and future said to fall on "
        "this day, from the first humans to the renewal of the world, among them events of Zarathushtra's "
        "mission. No historical record gives the prophet's birthday; the date is a theological one. Parsis "
        "visit the fire temple and hold a jashan; in Iran the day is called the birthday of Asho "
        "Zarathushtra.",
        "Biruni, Chronology; Mah Fravardin Roz Hordad (Middle Persian; ed. J. M. Jamasp-Asana, Pahlavi Texts, "
        "1897-1913); Parsi Times (Gujarati), 'ખોરદાદ સાલ મુબારક!' (2021, 2022)"),
    "zarthost_no_diso": (
        "Zarthost no Diso ('diso' is the Parsi Gujarati word for a death anniversary) is Khorshed roj of "
        "Dae mah, the eleventh day of the tenth month, kept with prayers for the fravashi of the prophet. "
        "The Pahlavi tradition says he died aged seventy-seven (Zadspram gives 77 years and 40 days), slain "
        "by a Turanian named Bradres; the Shahnameh places his death at the fire temple of Balkh during the "
        "invasion of Arjasp. The forty days do not fit the interval between Khordad Sal and 11 Dae, which "
        "has led scholars to suggest that the year once began with the month Dae. Like the birthday, the "
        "date is traditional, not historical. In the Fasli calendar it falls on 26 December.",
        "Zadspram 23.9 (as cited in Wikipedia, 'Zoroastrian calendar'); Ferdowsi, Shahnameh, reign of "
        "Goshtasp; Wikipedia, 'Zoroastrian festivals'"),
    "muktad": (
        "The Muktad, which Iranians call Farvardigan or Panjeh, are the last ten days of the year: the last "
        "five days of Aspandarmad and the five Gatha days. The Farvardin Yasht says that the fravashis of "
        "the righteous come to their homes at Hamaspathmaedaya and go about for ten nights, asking to be "
        "remembered with prayer, offerings and clothing. Parsi families set out flowers in metal vases on "
        "tables in a clean room or at the fire temple, and priests recite prayers for the departed through "
        "the days and nights; some Indian families extend the period to eighteen days. Boyce describes the "
        "same welcome in the villages of Yazd: houses cleaned, lamps lit, food offered for the returning "
        "souls. The Muktad ends at Navroz.",
        "Yt 13.49-52; Boyce 1977; Wikipedia, 'Zoroastrian festivals' (eighteen days); Modi 1922 (background)"),
    "farvardigan": (
        "Fravardin roj of Fravardin mah, the nineteenth day of the first month, is the name-day feast of the "
        "fravashis, the guardian spirits of the righteous living and dead. The winged Faravahar emblem is "
        "commonly taken today as a fravashi, although its meaning on the Achaemenid reliefs is debated. "
        "Parsis hold a jashan and visit the Towers of Silence or cemeteries to remember the dead; Iranian "
        "Zoroastrians call the day Farvardinegan and gather at their cemeteries (aramgah). It should not be "
        "confused with the ten days of Farvardigan at the end of the year, which carry the same name in "
        "Iran. The feast belongs to the series of days on which the day-name and month-name coincide, "
        "which Biruni lists one by one.",
        "Biruni, Chronology; Wikipedia, 'Zoroastrian festivals' and 'Faravahar'; Persian Wikipedia, "
        "'فروردینگان'"),
    "gahambar_maidyozarem": (
        "Maidyozarem, 'mid-spring' (Avestan maidhyoi-zaremaya, the time of fresh green), is the first of the "
        "six seasonal festivals, kept for five days, 11-15 Ardibehesht, ending on the 45th day of the year. "
        "The Pahlavi books link each Gahambar with one of the six creations, and this one with the sky. The "
        "six are named together in the Vispered and in the Afrinagan of the Gahambars. A Gahambar is a "
        "communal feast: food given by the community or by endowments is blessed with the Afrinagan and "
        "shared by rich and poor alike, and attendance was held a religious duty. In Shahanshahi and Kadmi "
        "reckoning the festival no longer falls in spring.",
        "Vr 1.2; Afrinagan-i Gahambar; Dehkhoda, 'گاهنبار'; Persian Wikipedia, 'گاهنبار'; EIr, 'Gahambar' "
        "(background); Boyce 1977"),
    "gahambar_maidyoshahem": (
        "Maidyoshahem, 'midsummer', is the second seasonal festival, kept for five days, 11-15 Tir, ending "
        "on the 105th day of the year; it was originally a feast of the summer solstice and of the hay "
        "harvest. The Pahlavi books link it with the creation of water. In the Sharifabad of the 1960s "
        "Boyce saw the Gahambar feasts still held in the village by families who had inherited the duty "
        "with land endowed for the purpose, and the whole village ate together. Parsi Gahambars in Mumbai "
        "and Navsari are likewise funded by old endowments. In the Fasli calendar the feast falls in late "
        "June and early July.",
        "Vr 1.2; Dehkhoda, 'گاهنبار'; Boyce 1977; Wikipedia, 'Gahambar'"),
    "gahambar_paitishahem": (
        "Paitishahem, 'bringing in the corn', is the third seasonal festival, kept for five days, 26-30 "
        "Shehrevar, ending on the 180th day of the year, when the grain harvest was gathered. The Pahlavi "
        "books link it with the creation of the earth. Like all Gahambars it is a feast of giving: the "
        "Persian name gahanbar is often explained as the 'time of bearing fruit', and the duty of every "
        "Zoroastrian to give food and share it at these feasts is stressed in Iranian practice, where many "
        "have left land, gardens or water rights to pay for them. Iran registered the Gahambar rites on its "
        "list of national intangible heritage.",
        "Vr 1.2; Dehkhoda, 'گاهنبار'; Persian Wikipedia, 'گاهنبار'"),
    "gahambar_ayathrem": (
        "Ayathrem, 'homecoming', is the fourth seasonal festival, kept for five days, 26-30 Meher, ending on "
        "the 210th day of the year, when the herds were brought down from the summer pastures and the "
        "seven-month Zoroastrian summer ended. The Pahlavi books link it with the creation of plants. After "
        "Ayathrem the five months of winter begin, in which Rapithwin is not invoked at noon and the "
        "Second Havan takes his place. In the old village calendar of Yazd, Boyce notes, the Gahambars were "
        "fixed points of the farming year. In the Fasli calendar Ayathrem ends in mid-October.",
        "Vr 1.2; Dehkhoda, 'گاهنبار'; Wikipedia, 'Rapithwin' (after EIr); Boyce 1977"),
    "gahambar_maidyarem": (
        "Maidyarem, 'mid-year', is the fifth seasonal festival, kept for five days, 16-20 Dae, ending on the "
        "290th day of the year, in the depth of winter. The name is usually explained as the middle of the "
        "year counted from the old autumn new year, or as the time of rest for herdsmen and farmers. The "
        "Pahlavi books link it with the creation of animals. Its timing near the winter solstice, in a "
        "calendar that kept to the seasons, made it a feast of endurance and sharing in the cold. In the "
        "Fasli calendar it ends early in January.",
        "Vr 1.2; Dehkhoda, 'گاهنبار'; Wikipedia, 'Gahambar'"),
    "gahambar_hamaspathmaedem": (
        "Hamaspathmaedem is the sixth seasonal festival, kept on the five Gatha days at the end of the year "
        "(in older practice together with the last five days of Aspandarmad). The meaning of the Avestan "
        "name hamaspathmaedaya is uncertain; it has been explained as the time when day and night are "
        "equal. The Pahlavi books link it with the creation of humankind, and it coincides with the coming "
        "of the fravashis described in the Farvardin Yasht, so that this Gahambar is also the feast of the "
        "souls of the departed. Each Gatha day is named after one of the five Gathas of Zarathushtra, which "
        "are recited in turn.",
        "Vr 1.2; Yt 13.49; Dehkhoda, 'گاهنبار'; Persian Wikipedia, 'گاهشماری اوستایی نو'"),
    "jashan_fravardin": (
        "In Parsi calendars the nineteenth day of Fravardin is printed as the Fravardian Jashan. A jashan "
        "(Middle Persian yazishn, 'worship') is the thanksgiving service held on name-days and community "
        "occasions: two or more priests sit before a fire in its vase with flowers, fruit, milk, wine or "
        "water and sweets, and recite the Afrinagan prayers of blessing, exchanging flowers at set points. "
        "On this day the Afrinagan is dedicated to the fravashis. Jashans may be held at home, in a fire "
        "temple, or in a public hall, and lay Zoroastrians may attend. The same day is Farvardinegan in Iran.",
        "Modi 1922 (background); Wikipedia, 'Gahambar' (name-day feasts); Boyce 1977"),
    "jashan_ardibehesht": (
        "Ardibehesht roj of Ardibehesht mah, the third day of the second month, is the feast of Asha "
        "Vahishta, 'Best Truth' or 'Best Order', the Amesha Spenta who guards fire. The Ashem Vohu, one of "
        "the oldest and holiest prayers, is a praise of Asha, so the feast touches every act of worship. "
        "Parsis go to the fire temples; in Iran the day is Ardibeheshtgan. Asha also presides over the noon "
        "watch: the Rapithwin Gah is under his protection, and in the Fasli calendar this feast falls on 22 "
        "April, a few weeks after Rapithwin's spring return. Nothing ties the feast to particular "
        "archaeological remains.",
        "Wikipedia, 'Gahambar' (name-day feasts; Fasli date) and 'Rapithwin'; Persian Wikipedia, 'جشن‌های "
        "ایران باستان'"),
    "jashan_khordad": (
        "Khordad roj of Khordad mah, the sixth day of the third month, is the feast of Haurvatat, "
        "'Wholeness', the Amesha Spenta who guards water. In the Gathas Haurvatat and Ameretat, 'Wholeness' "
        "and 'Immortality', are always named together, and the Pahlavi books make them guardians of water "
        "and plants. Iranian Zoroastrians kept Khordadgan by going to springs, streams and the sea shore to "
        "pray and celebrate, according to Persian accounts of the old name-day feasts. Parsis hold a jashan. "
        "In the Fasli calendar the day falls on 25 May.",
        "Wikipedia, 'Gahambar' (name-day feasts; Fasli date); Persian Wikipedia, 'جشن‌های ایران باستان'"),
    "jashan_tir": (
        "Tirgan is the feast of Tishtrya, the star Sirius, on Tir roj of Tir mah. The Tishtar Yasht tells "
        "how Tishtrya, as a white horse, fought the black horse Apaosha, demon of drought, and released the "
        "rains; it compares Tishtrya's swiftness to the arrow of Arash the archer. Biruni and Gardizi tell "
        "how Arash's arrow, shot to fix the frontier between Iran and Turan, flew from the mountains of "
        "Amol to the edge of Khorasan. Iranians still splash water and tie bands of coloured threads to the "
        "wrist, thrown into running water after ten days. The heliacal rising of Sirius in high summer may "
        "lie behind the feast. In the Fasli calendar it falls on 1 July.",
        "Yt 8; Biruni, Chronology; Gardizi, Zayn al-akhbar; Wikipedia, 'Tirgan' and 'Gahambar' (Fasli date)"),
    "jashan_amardad": (
        "Amardad roj of Amardad mah, the seventh day of the fifth month, is the feast of Ameretat, "
        "'Immortality', the Amesha Spenta who guards plants. Iranian Zoroastrian writers stress that the "
        "name is Amordad, 'deathless', not the Persian Mordad, which would mean the opposite. In Iran the "
        "day, Amordadgan, is kept with the planting of trees and a jashan; Parsis hold a jashan in honour of "
        "the plant creation. Ameretat and Haurvatat are invoked together in the Gathas and in the daily "
        "prayers. In the Fasli calendar the day falls on 25 July.",
        "Wikipedia, 'Gahambar' (name-day feasts; Fasli date); delgarm.com, 'تقویم زرتشتی' (Amordad not "
        "Mordad); Persian Wikipedia, 'جشن‌های ایران باستان'"),
    "jashan_shehrevar": (
        "Shehrevar roj of Shehrevar mah, the fourth day of the sixth month, is the feast of Khshathra "
        "Vairya, 'Desirable Dominion', the Amesha Spenta of the sky and metals in the Pahlavi books. The "
        "Ahuna Vairya prayer ends by giving the dominion to Ahura, whom the faithful make 'shepherd of the "
        "poor', and the feast has long been a day for charity to the needy. Persian writers also call it "
        "Azarjashn, a feast of fire, with fires lit as the summer ends. In the Fasli calendar it falls on "
        "21 August, near the start of the Paitishahem harvest season.",
        "Ahuna Vairya (Y 27.13, TITUS); Wikipedia, 'Gahambar' (Fasli date); Persian Wikipedia, 'جشن‌های "
        "ایران باستان' (شهریورگان یا آذرجشن)"),
    "jashan_meher": (
        "Mehergan is the feast of Mithra, god of the covenant and of light, on Meher roj of Meher mah, and "
        "was the greatest feast after Nowruz. Classical writers give early evidence: Strabo says the satrap "
        "of Armenia sent the Persian king 20,000 foals each year for the Mithrakana, and Duris of Samos "
        "(quoted by Athenaeus) that the king drank and danced only at the festival of Mithra. Under the "
        "Sasanians kings were often crowned at Mehergan or Nowruz. Biruni links the day with Fereydun's "
        "victory over Zahhak and calls it a sign of resurrection, 'because at Mihragan that which grows "
        "reaches perfection'. In the Fasli calendar it falls on 2 October.",
        "Strabo, Geography 11.14.9; Athenaeus, Deipnosophists 10.434e (Duris); Biruni, Chronology and "
        "Tafhim; Wikipedia, 'Mehregan' and 'Gahambar' (Fasli date)"),
    "jashan_avan": (
        "Avan roj of Avan mah, the tenth day of the eighth month, is the feast of the waters and of Aredvi "
        "Sura Anahita, praised in the Aban Yasht. Parsis go to the sea shore, a river or a well to recite "
        "the Ardvisur Niyayesh and offer flowers, sugar and coconut; the Gujarati name is Avan Ardvisur nu "
        "Parab. The epigraphy here is firm: Artaxerxes II (404-358 BCE) is the first Achaemenid king to "
        "invoke Anahita, with Ahuramazda and Mithra, in his inscriptions at Susa and Hamadan, and Berossus "
        "says he set up her statues in the chief cities of the empire. In the Fasli calendar the day falls "
        "on 26 October.",
        "Yt 5; Artaxerxes II inscriptions A2Sa, A2Ha (R. G. Kent, Old Persian, 1953); Berossus in Clement of "
        "Alexandria, Protrepticus 5.65; zcserv.com (Gujarati name); Wikipedia, 'Gahambar' (Fasli date)"),
    "jashan_adar": (
        "Adar roj of Adar mah, the ninth day of the ninth month, is the feast of Atar, fire, the son of Ahura "
        "Mazda. Parsis call it Atash nu Parab; the fire temples are crowded and the Atash Niyayesh is "
        "recited, with gifts of sandalwood. The archaeology of fire worship is well founded: Achaemenid "
        "royal tombs at Naqsh-e Rostam show the king before a fire altar, and at Takht-e Soleyman clay "
        "sealings naming the priests of Adur Gushnasp confirm the site of one of the three great Sasanian "
        "fires. In India the Iranshah fire, kept at Udvada since 1742, is held to descend from the fire "
        "brought by the first Parsi settlers. In the Fasli calendar the day falls on 24 November.",
        "S 1.9; EIr, 'Atas' and 'Adur Gusnasp' (background); R. Gobl, Die Tonbullen vom Tacht-e Suleiman "
        "(Berlin, 1976; background); Wikipedia, 'Gahambar' (Fasli date)"),
    "jashan_dae": (
        "The tenth month, Dae, belongs to the Creator, Ahura Mazda, who also owns four days of every month "
        "(1, 8, 15, 23). Their four meetings in Dae mah - Hormazd, Dae-pa-Adar, Dae-pa-Meher and Dae-pa-Din "
        "roj - are the Dae jashans. Biruni calls the first of Dae Khurram-ruz, 'the joyful day', and "
        "reports that the king came down from his throne, dressed in white and sat with the farmers. The "
        "four Creator days split the month into two weeks of seven days and two of eight, a division that "
        "may echo the Babylonian quarters of the month. In the Fasli calendar the first Dae jashan falls in "
        "mid-December.",
        "Biruni, Chronology; Wikipedia, 'Zoroastrian calendar' (weeks; Babylonian practice) and 'Gahambar'"),
    "jashan_bahman": (
        "Bahman roj of Bahman mah, the second day of the eleventh month, is the feast of Vohu Manah, 'Good "
        "Mind', guardian of useful animals. Many Parsis abstain from meat on Bahman roj and some through "
        "the whole month of Bahman, in honour of the animal creation. Biruni records the Iranian feast as "
        "Bahmanjana. Vohu Manah is the first of the Amesha Spentas to be created in Zoroastrian tradition "
        "and the one who welcomes the souls of the righteous after death (Vendidad 19). In the Fasli calendar the "
        "day falls on 16 January.",
        "Biruni, Chronology; Wikipedia, 'Gahambar' (name-day feasts; Fasli date); Modi 1922 (background)"),
    "jashan_aspandarmad": (
        "Aspandarmad roj of Aspandarmad mah, the fifth day of the twelfth month, is the feast of Spenta "
        "Armaiti, 'Holy Devotion', the Amesha Spenta of the earth, thought of as female. Biruni describes it "
        "as a feast of women, on which men gave gifts to their wives, and says that charms against "
        "scorpions and other noxious creatures were written on this day. In modern Iran Sepandarmazgan has "
        "been revived as a day of honour for women and mothers. Parsis hold a jashan. In the Fasli calendar "
        "the day falls on 18 February.",
        "Biruni, Chronology; Wikipedia, 'Gahambar' (Fasli date); Persian Wikipedia, 'جشن‌های ایران باستان'"),
    "sadeh": (
        "Sadeh, 'hundred', is a midwinter fire festival of Iran, on Aban roj of Bahman mah (10 Bahman), "
        "the name explained, among other ways, as a count of a hundred days and nights (fifty of each) "
        "before Nowruz. The Shahnameh tells how King Hushang struck flint against flint at a serpent and "
        "found fire, and founded Sadeh in thanks. Biruni and other medieval writers describe great "
        "bonfires, and the Ziyarid prince Mardavij held a famous Sadeh on the Zayandeh river at Isfahan in "
        "the 10th century. Zoroastrians of Kerman and Yazd kept the festival: boys gathered camel-thorn, a "
        "bonfire was lit near water, and families carried embers home. Parsi calendars do not "
        "traditionally list it.",
        "Ferdowsi, Shahnameh, reign of Hushang; Biruni, Chronology and Tafhim; Boyce 1968; Wikipedia, 'Sadeh'; "
        "zcserv.com (listed only for Fasli/Iranian users)"),
    "chaharshanbe_suri": (
        "Chaharshanbe Suri, 'festive Wednesday', is the eve of the last Wednesday before Nowruz, when "
        "Iranians light bonfires and jump over them. The Wednesday shows that in its present form it "
        "belongs to the Islamic era, since the Zoroastrian calendar has no week; folklorists connect it "
        "with older year-end fire customs and with the return of the souls at Farvardigan, but the link is "
        "argued, not documented. It is a national custom of Iran rather than a Zoroastrian holy day, and "
        "Zoroastrian calendars do not list it among the religious feasts. The app shows it only with the "
        "Iranian calendar, by the Iranian civil week.",
        "EIr, 'Cahar-sanba-suri' (background); Wikipedia, 'Chaharshanbe Suri'; zcserv.com (not listed)"),
    "mah_niyayesh": (
        "The Mah Niyayesh, the litany of the Moon, and the Mah Yasht praise Mah, 'the moon that keeps the "
        "seed of the bull'. The Yasht names three times of the moon: antare-mangha, the 'inner' or new moon; "
        "perenomangha, the full moon; and vishaptatha. Parsi practice is to recite the Mah Bokhtar Niyayesh at the new moon and the full "
        "moon, standing before the moon when it can be seen, and some recite it on the three days of the "
        "moon named in the text. Unlike the solar calendar, these days are fixed by the sky, so the app "
        "marks them from the JPL ephemeris. Moon worship among the Persians is already reported by "
        "Herodotus.",
        "Yt 7 (Mah Yasht); Mah Niyayesh (Khordeh Avesta); Herodotus 1.131; Modi 1922 (background). UNCERTAIN: "
        "the recitation days vary by community; no single rule was found."),
}

# calendar key -> (text, sources)
CAL_H = {
    "shahanshahi": (
        "The Shahanshahi ('imperial') calendar is the reckoning of most Parsis: twelve months of thirty "
        "days, each day and month named after a divine being, and five Gatha days, 365 days with no leap "
        "day. The Parsis inserted one extra month, called Aspandarmad vahizak, at some time between 1125 "
        "and 1129, following the Denkard's rule of one month in 120 years; it was never done again. Since "
        "then the year has slipped back against the seasons by a day every four years, so that Navroz now "
        "falls in August. Years are counted from the accession of Yazdegerd III, the last Sasanian king, "
        "on 16 June 632.",
        "Wikipedia, 'Zoroastrian calendar' (Denkard; intercalation c. 1125-1129); EIr, 'Kadimi'; ZANC, 'About "
        "Zoroastrian Calendars'"),
    "kadmi": (
        "The Kadmi or Qadimi ('ancient') calendar is the Iranian Zoroastrian reckoning, which never received "
        "the Parsi extra month and so runs thirty days ahead of the Shahanshahi. In 1721 the Kerman priest "
        "Jamasp Vilayati drew the Surat priests' attention to the difference, and in 1745 a Surat high "
        "priest and his community dropped a month to agree with Iran; the Kadmi movement is also dated to "
        "1746. The dispute, called the kabisa ('intercalation') controversy, divided families and fire "
        "temples for decades. Mulla Kaus, sent to Iran in 1767, returned to become the first Kadmi high "
        "priest of the Dadyseth Atash Behram in Bombay. Surat and Bharuch remained Kadmi strongholds.",
        "EIr, 'Kadimi' and 'Dadyseth, Dadibhai Noshirwanji'; D. Menant, The Parsis (Project Gutenberg 29109); "
        "Frashogard, 'The illustrious lives of Dastur Mulla Kaus and Dastur Mulla Feroze'"),
    "fasli": (
        "The Fasli ('seasonal') calendar keeps the old names and the twelve thirty-day months but fixes "
        "Navroz on the March equinox, taken as 21 March, and adds a sixth Gatha day, Avardad-sal-gah, in "
        "leap years by the Gregorian rule, so that each feast keeps its season. K. R. Cama argued for "
        "reform in the 1860s, and the Zarthosti Fasli Sal Mandal of Bombay published the calendar in 1906, "
        "modelled on the 11th-century Jalali calendar. Most Parsis rejected it, holding that a leap day "
        "breaks the rule of the Denkard; it is widely kept in North America and Britain. Its year numbers "
        "follow the Yazdegerdi era, but published Fasli tables differ by one in the year number.",
        "Wikipedia, 'Zoroastrian calendar' (Fasli section); ZANC, 'About Zoroastrian Calendars'; zcserv.com "
        "(year numbering)"),
    "bastani": (
        "The Bastani ('ancient') calendar is the religious calendar of Iranian Zoroastrians since 1939. "
        "Iran's civil calendar of 1925 kept the Zoroastrian month names and began the year at the March "
        "equinox; Keikhosrow Shahrokh, the Zoroastrian member of parliament, who had seen the Fasli reform "
        "in Bombay, promoted a matching religious calendar, and the Tehran Anjoman adopted it. The villages "
        "of Yazd were slow to follow. Its months have thirty days, so its month-days differ from the civil "
        "months of 31 days. In this app Nowruz falls on the day of the March equinox computed from the JPL "
        "ephemeris; a briefing of the Zoroastrian Trust Funds of Europe notes that Iranians keep the actual "
        "equinox day.",
        "Niechcial 2019 (Iran and the Caucasus 23); Heritage Institute, 'Zoroastrian Calendar'; Wikipedia, "
        "'Zoroastrian calendar' (ZTFE briefing)"),
    "sasanian": (
        "This calendar is a reconstruction, shown for comparison; it is not a claim about how any community "
        "counted. The Zoroastrian 365-day year of twelve thirty-day months and five extra days was probably "
        "introduced under the Achaemenids, on the Egyptian model; the earliest documents with its month "
        "names are the Parthian ostraca from Nisa (1st century BCE). For the Sasanian period the main "
        "source is Biruni, who reports that the five extra days were moved to follow the month Aban and "
        "that the year was meant to be corrected by a month every 120 years. Whether that intercalation was "
        "ever carried out is debated: some scholars think the word kabisa meant only shifting the five days.",
        "Biruni, Chronology; F. de Blois, 'The Persian calendar', Iran 34 (1996) 39-54; EIr, 'Kabisa' "
        "(A. Cristoforetti); I. M. Diakonoff and V. A. Livshits, Parthian Economic Documents from Nisa "
        "(1976-2001, background); Wikipedia, 'Zoroastrian calendar'"),
}


def title(key: str) -> tuple[str, str]:
    """(English, Persian) title of a festival or calendar key."""
    if key in FESTIVAL:
        return FESTIVAL[key]["en"], FESTIVAL[key]["fa"]
    import jashans
    if key in jashans.EXTRA:
        e = jashans.EXTRA[key]
        return e["en"], e.get("fa", "")
    if key in CALENDAR:
        return CALENDAR[key]["en"], CALENDAR[key]["fa"]
    import znames
    e = znames.FESTIVAL.get(key, {"en": key, "fa": ""})
    return e["en"], e.get("fa", "")


def _prayer_links(key: str) -> str:
    try:
        import prayers
    except ImportError:       # pragma: no cover
        return ""
    keys = [k for k in prayers.FESTIVAL_PRAYERS.get(key, []) if k in prayers.PRAYERS]
    if not keys:
        return ""
    return ("<div class='gs-pop-read'>Read: " + " · ".join(
        f"<a class='gs-pr' href='{html.escape(prayers.PRAYERS[k]['links'][0][1])}' target='_blank'>"
        f"{html.escape(prayers.PRAYERS[k]['en'])}</a>" for k in keys) + " ↗</div>")


def has_text(key: str) -> bool:
    import jashans
    return key in H or key in CAL_H or key in jashans.NOTE or key in jashans.HISTORY


def body_html(key: str) -> str:
    """Popover body: what the day commemorates (short), then its history, the prayers to read and sources."""
    import jashans
    en, fa = title(key)
    parts = [f"<div class='gs-pop-title'>{html.escape(en)} <span class='gs-fa-i' lang='fa' dir='rtl'>"
             f"{html.escape(fa)}</span></div>"]
    srcs = []
    if key in jashans.NOTE:
        note, nsrc = jashans.NOTE[key]
        parts.append(f"<div class='gs-pop-note'><b>Commemorates:</b> {html.escape(note)}</div>")
        srcs.append(nsrc)
    if key in jashans.IRAN:
        ien, ifa, icustom = jashans.IRAN[key]
        parts.append(f"<div class='gs-pop-text'><b>In Iran:</b> {html.escape(ien)} <span class='gs-fa-i' lang='fa' "
                     f"dir='rtl'>{html.escape(ifa)}</span>. {html.escape(icustom)}</div>")
        srcs.append(jashans.IRAN_SRC)
    hist = H.get(key) or CAL_H.get(key) or jashans.HISTORY.get(key)
    if hist:
        text, src = hist
        parts.append(f"<div class='gs-pop-text'>{html.escape(text)}</div>")
        srcs.append(src)
    parts.append(_prayer_links(key))
    if srcs:
        parts.append(f"<div class='gs-pop-src'>Sources: {html.escape('; '.join(srcs))}</div>")
    return "".join(parts)


def clickable(key: str, chip_html: str, align_right: bool = False) -> str:
    """Wrap a festival chip so that clicking it opens its history (no JavaScript needed)."""
    if not has_text(key):
        return chip_html
    cls = "gs-pop gs-pop-r" if align_right else "gs-pop"
    return (f"<details class='{cls}'><summary title='Click: what this day commemorates'>{chip_html}</summary>"
            f"<div class='gs-popbody'>{body_html(key)}</div></details>")
