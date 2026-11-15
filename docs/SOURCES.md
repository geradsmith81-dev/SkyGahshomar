# Sky Gahshomar — content sources

Modules: `sects.py`, `names.py`, `festival_history.py`, `gahs.py`. Checked by `check_content.py`.
Compiled 15 November 2026. Every module also cites its sources entry by entry; this file lists them in one
place, says how each was read, and records what could not be checked.

## How the sources were read

| Source | How it was read | Used for |
|---|---|---|
| K. F. Geldner, *Avesta* (1889–96), digitised by TITUS, Frankfurt (titus.uni-frankfurt.de, `avestt.htm`) | Full text downloaded; passages searched by script | Avestan forms of the day names (Siroza 1.1–30), Gatha names (accusatives), Gah names and companions (Siroza 1.7; Yasna 1.3–7), Ahuna Vairya, Zurvan in Siroza 1.21 |
| Zoroastrian Calendar Services, zcserv.com (Arzan Lali) | Gujarati and English year and month views for 2024, 2026 and 2028, queried directly | Gujarati roj, mah, Gatha-day and festival names; Gujarati weekday and calendar labels; ય.ઝ. |
| Persian Wikipedia: گاهشماری اوستایی نو، فهرست نام روزهای ماه، اندرگاه، گاهنبار، جشن‌های ایران باستان، تیرگان، مهرگان، فروردینگان | Wikitext downloaded via the API | Persian day, month, Gatha-day and Gah names; name-day feasts |
| Dehkhoda, *Loghatnameh*, گاهنبار (via vajehyab.com and abadis.ir) | Search extracts | Persian Gahambar names and day numbers (45, 105, 180, 210, 290, 365) |
| English Wikipedia: Zoroastrian calendar, Gahambar (Zoroastrian festivals), Gāh, Rapithwin, Sadeh, Tirgan, Mehregan, Khordad Sal, Ilm-e-Khshnoom, Irani (India), Kharshedji Rustomji Cama, Faravahar, Gabr, Mazdakism, Zurvanism, Avestan alphabet | Wikitext downloaded via the API; used as a pointer to the scholarship it cites, and checked against primary or community sources where possible | Calendar history, Fasli dates of the name-day feasts, Avestan letter table |
| Gujarati Wikipedia, પતેતી | API search extract | Pateti as the last day of the year |
| Encyclopaedia Iranica: 'Kadimi', 'Dadyseth, Dadibhai Noshirwanji', 'Kabisa', 'Kustig' | **Search-engine extracts only** — iranicaonline.org refuses automated access (Cloudflare challenge, HTTP 403). Only the sentences shown in the extracts were used | Kadmi history and percentages; 1746; kabisa as shifting the Andargah; facing the light |
| Encyclopaedia Iranica: 'Rapithwin', 'Gah', 'Gahambar', 'Nowruz i', 'Sada', 'Atas', 'Adur Gusnasp', 'Mazdak', 'Cahar-sanba-suri' | **Not read directly**; cited as background or through the Wikipedia articles that summarise them | Marked "background" or "via Wikipedia" in the modules |
| P. Niechciał, 'Calendar as an identity marker of the Zoroastrian community in Iran', *Iran and the Caucasus* 23 (2019) 35–49; and her chapter on Tehran Zoroastrians (Springer, 2022) | Chapter notes via SpringerLink extract | 1939 adoption of the Bastani calendar; sal-e dini (ZRE) in Iran |
| Heritage Institute, 'Zoroastrian Calendar' (heritageinstitute.com) | Search extract | Shahrokh and 1939; Sharifabadi Qadimi; Iranis joining Kadmi temples |
| A. A. Jafarey, 'The Precise Iranian Calendar', 'Nowruz', 'The Good Religion and the Institutionalized Zoroastrianism' (zoroastrian.org; CAIS) | Search extracts | Zarathushtrian Assembly (1990, Los Angeles), ZRE, its calendar |
| ZANC, 'About Zoroastrian Calendars' (zanc.org) | Search extract | Intercalation c. 1129; Fasli leap day |
| D. Menant, *The Parsis* (Project Gutenberg 29109) | Search extract | 1746 Kadmi adoption; kabisa dispute |
| Frashogard (frashogard.com), 'The illustrious lives of Dastur Mulla Kaus and Dastur Mulla Feroze' | Search extract | Mulla Kaus mission |
| Parsi Times (Gujarati edition): 'દરેક ગેહ માંડવાનો વખત' (2018); 'ગેહ: સુસંગતતા અને ધાર્મિક વિધિઓ' (2021); 'ખોરદાદ સાલ મુબારક!' (2021, 2022) | Search extracts | Gujarati Gah names; community Gah timetable; Khordad Sal |
| avesta.org glossary; Kersey H. Antia, 'Basic Zoroastrian Prayers' | Downloaded / extract | Rapithwin replaced by Second Havan; praying towards light |
| Dastur J. M. Jamasp-Asa, 'The Kushti ritual' (CAIS reprint) | Search extract | Facing the light; south as fallback |
| Biruni, *al-Athar al-baqiya*, tr. Sachau (1879); Ferdowsi, *Shahnameh*; Strabo 11.14.9; Athenaeus 10.434e; Herodotus 1.131; Clement, *Protrepticus* 5.65 | **Cited from standard knowledge and secondary summaries, not re-read for this task** | Festival histories; each such statement names the author it comes from |
| M. Boyce, *A Persian Stronghold of Zoroastrianism* (1977); 'Rapithwin, Nō Rūz, and the Feast of Sade' (1968); J. J. Modi, *Religious Ceremonies and Customs of the Parsees* (1922); M. C. Root, *The King and Kingship in Achaemenid Art* (1979); F. de Blois, 'The Persian calendar', *Iran* 34 (1996); R. Göbl, *Die Tonbullen vom Tacht-e Suleiman* (1976); R. G. Kent, *Old Persian* (1953) | **Background: not re-read for this task**; cited for well-known points | Marked "background" where used alone |

## Avestan script

* Strings are produced by `names.to_avestan()` from TITUS transliterations; nothing is typed in Avestan by hand.
* Letter correspondences: Unicode Avestan chart (U+10B00–U+10B35) and Hoffmann's transliteration as tabulated in Wikipedia 'Avestan alphabet'; *ii* and *uu* are two letters each, as Unicode specifies. TITUS writes ṣ̌ as š + dot below; NFC normalisation makes this identical to ṣ + caron, mapped to U+10B34.
* Word separator: U+2E31 WORD SEPARATOR MIDDLE DOT (present in Noto Sans Avestan).
* Day names are the forms of Siroza 1 (dative or genitive, as attested). Days 8, 15, 23 are identical in Avestan.
* The title 'Gahshomar' is a New Persian word; its Avestan-letter form is a Pazand-style spelling made for the app, not an Avestan word.

## Flagged forms

`names.UNCERTAIN` lists every form made for the app or doubtful (31 entries), with the reason. In short:
Gujarati forms not printed by zcserv (4 jashan names, Chaharshanbe Suri, Mah Niyayesh, Bastani, Sasanian, the
eras, Iranian place names, the title); zcserv's own possible variants (અશીશવંદ, અસફનદારમદ for day 5); descriptive
Persian for Parsi-only terms (Pateti, Muktad, Zarthost no Diso, Second Havan); the Avestan Gatha nominatives
(derived from attested accusatives) and day 27 (TITUS variant aṣ̌nō). The Persian and Gujarati names of the
communities in `sects.py` are descriptive labels made for the app.

## Verification

`check_content.py` (run 15 Nov 2026) checks that every key of the shared contract is present, that all Persian
strings use only Arabic-block letters with Persian ک/ی, Gujarati only the Gujarati block, Avestan only the Avestan
block and U+2E31, that every string is NFC, that every code point is covered by the Noto fonts used, that history
texts are 80–150 words, and that every Avestan word occurs in the TITUS text. The proof sheet
`SkyGahshomar_names_proof.png` renders every name with resvg-py 0.5.0 and Noto Sans, Noto Naskh Arabic,
Noto Sans Gujarati and Noto Sans Avestan (Google Fonts, OFL).

## Open questions for the calendar engine (not settled here)

1. Shahanshahi Navroz 2026: zcserv.com gives 15 August (Hormazd roj Fravardin 1396 on 15 Aug); other published calendars give 16 August.
2. Fasli year numbers: Wikipedia ('21 March 2000 = 1370 Y.Z.') and zcserv.com (21 March 2024 = 1393 Y.Z.) differ by one.
3. Iranian popular dates of Tirgan, Mehregan and Sadeh (13 Tir, 16 Mehr, 10 Bahman) follow the civil calendar's 31-day months (about 3 July, 8 October, 30 January); in a Bastani calendar of thirty-day months the same roj/mah fall on 1 July, 2 October and about 24 January. The engine should decide which to show for the Bastani preset.
