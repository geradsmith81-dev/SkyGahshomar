"""The five Gahs (watches of the day), the Rapithwin custom, and the note on facing the light.

The Zoroastrian day begins at sunrise (Bundahishn 25): the Ushahin watch after midnight belongs to the
day before. Each Gah has its own prayer in the Khordeh Avesta, recited after the kusti prayers, and its
own presiding beings, named in Siroza 1.7 and Yasna 1.3-7 (Geldner's text, via TITUS); the 'companions'
(hamkar) are the lesser ratus named with each Gah in the same passages.

Time rules (for the engine): 'start'/'end' use these events, computed for the observer from the JPL
ephemeris: sunrise, sunset, solar_noon (Sun's upper transit), solar_noon+3h, solar_midnight (lower transit).
The three-hour Rapithwin follows the common definition 'noon to 3 p.m.' (avesta.org Khorda Avesta;
Encyclopaedia Iranica via Wikipedia 'Gah'), taken here in apparent solar time; community timetables differ
(see COMMUNITY_TIMES).
"""
from __future__ import annotations

GAH_ORDER = ["havan", "rapithwin", "second_havan", "uziran", "aiwisruthrem", "ushahin"]

GAHS = {
    "havan": {
        "start": "sunrise", "end": "solar_noon",
        "period": "Sunrise to noon",
        "presiding": "Mithra, with Raman (Ram Khvastra)",
        "companions": "Savanghi and Visya",
        "prayers": "Havan Gah prayer; Khorshed and Meher Niyayesh (said in each of the three day watches); "
                   "most priestly rites, including the Yasna, are performed in this watch.",
        "note": "Avestan havani is the time of pressing the haoma, the start of the morning liturgy.",
        "src": "S 1.7; Y 1.3; Wikipedia, 'Gah' (table after EIr); Parsi Times (Gujarati), 'ગેહ: સુસંગતતા અને "
               "ધાર્મિક વિધિઓ' (2021)",
    },
    "rapithwin": {
        "start": "solar_noon", "end": "solar_noon+3h", "season": "summer",
        "period": "Noon to mid-afternoon (about 3 p.m.), in the seven summer months only",
        "presiding": "Asha Vahishta (Ardibehesht), with Atar, fire",
        "companions": "Fradat-fshu and Zantuma",
        "prayers": "Rapithwin Gah prayer; Khorshed and Meher Niyayesh.",
        "note": "Rapithwin is the spirit of the noon heat and of the summer; the watch is kept from Hormazd "
                "roj of Fravardin mah to Aneran roj of Meher mah. See RAPITHWIN.",
        "src": "S 1.7; Y 1.4; Wikipedia, 'Rapithwin' (after EIr, 'Rapithwin', M. Boyce)",
    },
    "second_havan": {
        "start": "solar_noon", "end": "solar_noon+3h", "season": "winter",
        "period": "Noon to mid-afternoon in the five winter months and the Gatha days",
        "presiding": "Mithra, as in the morning Havan",
        "companions": "Savanghi and Visya",
        "prayers": "Havan Gah prayer said a second time; Khorshed and Meher Niyayesh.",
        "note": "While Rapithwin is below the earth, Mithra keeps his part of the day, which is therefore "
                "called the Second Havan.",
        "src": "Wikipedia, 'Rapithwin' (after EIr); avesta.org glossary, 'Rapithwin' ('replaced by a second "
               "Hawan' for five months)",
    },
    "uziran": {
        "start": "solar_noon+3h", "end": "sunset",
        "period": "Mid-afternoon to sunset",
        "presiding": "Berezat Ahura Napat Apam (Burz Yazad), with the waters",
        "companions": "Fradat-vira and Dakhyuma",
        "prayers": "Uziran Gah prayer; Khorshed and Meher Niyayesh (the last of the day).",
        "note": "Avestan uzayeirina, the time of the day's 'going out'. Apam Napat, 'son of the waters', "
                "is one of the old Ahuras, with Mithra.",
        "src": "S 1.7; Y 1.5; Wikipedia, 'Gah' and 'Rapithwin'",
    },
    "aiwisruthrem": {
        "start": "sunset", "end": "solar_midnight",
        "period": "Sunset to midnight",
        "presiding": "The fravashis of the righteous",
        "companions": "Aibigaya; Fradat-vispam-hujyati and Zarathushtrotema",
        "prayers": "Aiwisruthrem Gah prayer; Mah Niyayesh may be said when the moon is up.",
        "note": "The name is often explained as the time when the chants are heard (Avestan aibi-sru-). "
                "The Siroza also names here the women and heroic sons of the righteous and the 'good dwelling' "
                "of the year (yairya hushiti).",
        "src": "S 1.7; Y 1.6; Wikipedia, 'Gah'",
    },
    "ushahin": {
        "start": "solar_midnight", "end": "sunrise",
        "period": "Midnight to dawn",
        "presiding": "Sraosha (Srosh), with Rashnu and Arshtat",
        "companions": "Berejya and Nmanya",
        "prayers": "Ushahin Gah prayer; Srosh is invoked as guardian of the night against the demons of "
                   "darkness.",
        "note": "Ushahin belongs to the previous day, since the day begins at sunrise.",
        "src": "S 1.7; Y 1.7; Bundahishn 25 (day begins at sunrise), as cited in Wikipedia, 'Zoroastrian "
               "calendar'",
    },
}

RAPITHWIN = (
    "Rapithwin is the spirit of the noon heat and lord of the summer. In Zoroastrian teaching the sun stood "
    "still at noon before evil entered the world, Ohrmazd performed the sacrifice of creation in Rapithwin's "
    "hour, and the final restoration will also be completed at noon. The Zoroastrian summer lasts seven "
    "months, from Navroz to the end of the Ayathrem Gahambar (30 Meher); for the five winter months "
    "Rapithwin withdraws under the earth to keep the springs and the roots of plants warm, and he is not "
    "invoked at noon: the Second Havan replaces his watch. At noon on Navroz (Hormazd roj of Fravardin mah) "
    "he is welcomed back with a jashan, a Yasna and the Afrinagan of Rapithwin; Boyce noted that in this "
    "ceremony the officiating priest faces west, whereas at other jashans he faces east. Failure to keep "
    "Rapithwin is listed as a sin in the Middle Persian confessions (patet). In the Fasli and Bastani "
    "calendars Rapithwin returns at the spring equinox; in the Shahanshahi and Kadmi calendars the "
    "'summer' months have drifted, so Rapithwin now returns in August and July. The Bundahishn describes an "
    "older winter rule with only four watches, the morning Havan running on until Uziran; the app offers "
    "this as the 'medieval_four' setting, used for the Sasanian reconstruction."
)
RAPITHWIN_SRC = ("Wikipedia, 'Rapithwin' (summary of EIr, 'Rapithwin', and M. Boyce, 'Rapithwin, No Ruz, and "
                 "the Feast of Sade', 1968); Wikipedia, 'Zoroastrian calendar' (Bundahishn winter rule); "
                 "Parsi Times (Gujarati), 'દરેક ગેહ માંડવાનો વખત' (2018: Rapithwin begins at noon on Hormazd "
                 "roj of Fravardin mah)")

# Community timetables differ from the astronomical definitions above. Recorded, not used by default.
COMMUNITY_TIMES = (
    "Parsi timetables do not all follow the plain astronomical rule. A Parsi Times guide (2018) counts the "
    "Havan watch from 36 minutes before sunrise and the Aiwisruthrem watch from 72 minutes after sunset, "
    "and gives local-time rules for when each Gah may be begun. Iranian calendars print the watches in "
    "clock times. The app uses the astronomical events and says so; a user who follows a priest's "
    "timetable should follow the timetable."
)
COMMUNITY_TIMES_SRC = "Parsi Times (Gujarati), 'દરેક ગેહ માંડવાનો વખત', July 2018. UNCERTAIN: one community guide."

FACING_LIGHT = (
    "Zoroastrians pray standing, facing a source of light, which stands for the light of Ahura Mazda and of "
    "Asha. Encyclopaedia Iranica's account of the kusti ritual gives the rule: while untying and tying the "
    "sacred cord, face east from dawn to midday and west until sunset, that is, toward the sun; at night, "
    "face an oil lamp, a fire, the moon or the stars. When there is no light at all, face south, held to "
    "be the direction of Ahura Mazda's heavenly abode. Dastur Jamaspji Jamasp-Asa's description of the "
    "same ritual adds that one should face south at midday, even when the sun is to the north. North is "
    "avoided because the Vendidad makes it the region from which Angra Mainyu and the demons rush forth. "
    "In a fire temple the worshipper faces the sacred fire. The compass page shows the bearing of the Sun "
    "by day and of the Moon at night, with south as the fallback, from the JPL ephemeris."
)
FACING_LIGHT_SRC = ("EIr, 'Kustig' (read via search extract); Dastur J. M. Jamasp-Asa, 'The Kushti ritual' "
                    "(reprinted by CAIS); Vendidad 19.1; Wikipedia, 'Zoroastrian prayer' (after Boyce 1996, "
                    "p. 258); Kersey H. Antia, 'Basic Zoroastrian Prayers' (avesta.org: 'During the day, pray "
                    "facing the sun and at night, facing a light')")


def gah_for(season: str) -> list[str]:
    """Gah keys of one day in order, for season 'summer' or 'winter' (Second Havan replaces Rapithwin)."""
    mid = "rapithwin" if season == "summer" else "second_havan"
    return ["havan", mid, "uziran", "aiwisruthrem", "ushahin"]
