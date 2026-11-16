# How Sky Gahshomar works

Sky Gahshomar (Persian گاه‌شمار, 'time-reckoner') shows the Zoroastrian calendars from NASA JPL DE440s astronomy
(1850–2149). Pages other than **Compare** show only the calendar chosen in the settings; the Gregorian civil date is
the reference of every grid.

### 1. One structure, five calendars
Every Zoroastrian calendar has 12 months (*mah*) of 30 days. Each day (*roj*) carries the name of
one of 30 yazatas (Hormazd … Aneran), so the same roj name recurs each month. Five Gatha days
(Ahunavad … Vahishtoisht) complete the 365-day year. When the roj name equals the mah name the day is a
name-day feast (*jashan, parab*). The calendars differ only in **where the year begins**, **whether a leap
day is added**, and (in the reconstruction) **where the Gatha days stand**. Internally every date is a
Julian Day Number, so all conversions are exact integer arithmetic.

| key | year begins | leap day | era(s) | evidence |
|---|---|---|---|---|
| `shahanshahi` | Kadmi date + 30 days; Navroz 15 Aug 2025, 15 Aug 2026 | never | YZ | Maharashtra Govt Gazette 2026 holiday list (Parsi New Year (Shahenshahi) = 15 Aug 2026); All India Radio 16 Aug 2023 |
| `kadmi` | 1 Fravardin YZ 1 = 16 June 632 (Julian) = JDN 1952063, then 365 days a year; Navroz 16 Jul 2025 | never | YZ | RE:Online 2025; epoch = accession of Yazdegerd III (Wikipedia/EIr) — the count reproduces the published Kadmi Navroz exactly |
| `fasli` | 21 March | Avardad-sal-gah on 20 March before a Gregorian 29 Feb (73 times 1850–2149) | YZ (changes at 21 March), ZRE = Gregorian + 1738 | Heritage Institute (Fasli calendar of 1906; ZRE years 3751–3755 from 21 March 2013–2017); Parsi Khabar 2024 |
| `bastani` | Iran's official Nowruz: day of the March equinox if it falls before true solar noon at 52.5° E, else next day | sixth Gatha day when the next Nowruz is 366 days later | ZRE (primary), YZ, SH | Heritage Institute: Bastani = Fasli organisation brought to Iran by Kay Khosrow Shahrokh, adopted in Tehran 1939, months *different* from the civil 31/30-day months; rule for Nowruz from Sky Taqwim (Calendar Center, Univ. of Tehran) |
| `sasanian` | 1 Fravardin of the Yazdegerdi count (same as Kadmi) | none (default) | YZ | reconstruction, see §2 |

Why Kadmi is "one month ahead": the Parsis of India once intercalated a month (dated to the 1120s by the
Heritage Institute) and the Iranians did not; a Kadmi date therefore names the month that comes *after*
the Shahanshahi one on the same civil day (Adar in Shahanshahi = Dae in Kadmi). The engine models this as
Shahanshahi = Kadmi + 30 days, and Kadmi = the unbroken count from Yazdegerd III's accession.

Year numbers: YZ = years of the Yazdegerdi era; each calendar enters the new number on its own Navroz
(Fasli in March, Kadmi in July, Shahanshahi in August — palvkasti.com). Shahanshahi YZ 1396 began on
15 Aug 2026.

**Bastani vs the Zarathushtrian Assembly.** A. A. Jafarey's Zarathushtrian Assembly (California) follows
the Iranian civil months (31/30 days). The Bastani calendar of the Iranian Anjomans keeps 30-day months +
Gatha days; this is why Mehregan (Meher roj of Meher mah) is civil 10 Mehr and the Tir jashan is civil 10 Tir.
Only the Bastani form is implemented.

### 2. The Sasanian reconstruction (a comparison ideal)
Like Sky Luach's "Early Temple Period", this calendar is shown to compare, not to claim anyone keeps it.
- **Andargāh after Avan** (default). al-Biruni reports that in late Sasanian and early Islamic times the five
  epagomenal days (*andargāh*) stood after the 8th month, Ābān; they were moved back to the end of the year in
  375 YZ (1006 CE) (Encyclopaedia Iranica, "Calendars i. Pre-Islamic calendars" and "Kabisa";
  F. de Blois, "The Persian calendar", *Iran* 34, 1996, 39–54; S. H. Taqizadeh, *Old Iranian Calendars*, 1938).
  Option `andargah="after_aspandarmad"` gives the post-1006 arrangement.
- **Intercalation** (`intercalation="kabisa_120"`, off by default). al-Biruni describes a fixed year kept in
  place by intercalating one month every 120 years, the andargāh moving to the end of the intercalated
  month each time. The engine continues that model hypothetically: in YZ 120·k (+`kabisa_phase`) the month
  after the Gatha days is repeated (flag `ZDate.repeated_month`) and the Gatha days follow the repeat.
  EIr "Kabisa" concludes there was "no true intercalation, but rather a periodic readjustment", officially
  enacted only once; hence the default "none". The phase of the cycle is not documented and is a free parameter.
- Festivals: Hamaspathmaedem = the andargāh days; Muktad = the last five days of the month before them plus
  the andargāh (Biruni's Farwardajan). de Blois' hypothesis of a c. 500 CE reform moving Nowruz to 1 Ādar is
  documented here but not modelled.

### 3. The day begins at sunrise
`to_zdate(date)` gives the roj whose daylight falls on that civil date. `zdate_at(datetime, place, cal)`
applies the rule to a moment: before local sunrise the previous roj is still running (Ushahin Gah belongs to
the previous day). Sunrise = Sun's centre at −0.8333° minus the dip of the horizon (0.0347°·√elevation m).
In polar day/night, 06:00 local mean solar time (true noon − 6 h) is used.

### 4. Festivals
See the docstring of `festivals.py` for every rule and source. Summary:
name-day jashans (Dae mah has four: Hormazd, Dae-pa-Adar, Dae-pa-Meher, Dae-pa-Din); six five-day
Gahambars (Maidyozarem Ardibehesht 11–15, Maidyoshahem Tir 11–15, Paitishahem Shehrevar 26–30,
Ayathrem Meher 26–30, Maidyarem Dae 16–20, Hamaspathmaedem = Gatha days); Muktad 10 days from Ashtad
roj of Aspandarmad (11 in Fasli/Bastani leap years), `muktad="parsi_18"` for the old 18-day custom
(Ashishvangh roj of Aspandarmad – Amardad roj of Fravardin); Navroz; Pateti (last day of the year);
Jamshedi Navroz (21 March for all Parsi calendars; `jamshedi="equinox_ist"` for the equinox day in IST;
Iran's Nowruz for Bastani); Khordad Sal; Zarthost no Diso; Farvardigan; Rapithwin Jashan; Iranian Sadeh
(`sadeh="iran"` civil 10 Bahman, `"kerman"` Aban roj Bahman mah, `"yazd"` Ashtad roj Adar mah);
Chaharshanbe Suri (Tuesday evening before the last Wednesday of the Iranian year); Tirgan civil 13 Tir.

### 5. Gahs, Rapithwin, Moon and light
Havan sunrise→true noon; Rapithwin (or Second Havan) noon→noon+3 h; Uziran →sunset; Aiwisruthrem
→solar midnight; Ushahin →next sunrise. The Bombay prayer-guide times (Havan to 12:40, Rapithwin 12:40–3:40)
are Bombay's true noon and noon + 3 h (Mumbai true noon ranges 12:22–12:52 IST through the year).
Rapithwin season: Hormazd roj of Fravardin mah to Aneran roj of Meher mah; Second Havan from Hormazd roj of
Avan mah to Vahishtoisht Gatha (Khordeh Avesta, Kanga tr.), applied in the user's own calendar.
Moon: all four JPL phases; new and full moon flagged for the Mah Niyayesh (antarə.måŋha, pərənō.måŋha;
vīšaptaθa = the half-moon station). `face_the_light()` returns Sun and Moon altitude/azimuth and which
light to face (Sun by day, Moon if up at night, otherwise a lamp/fire).

### 6. Year numbers shown (decision for the app)
Sources disagree on the Fasli year number: Wikipedia gives 21 March 2000 = 1370 YZ, while zcserv gives
21 March 2024 = 1393 YZ. The app follows the engine (ENGINE_NOTES): the Fasli calendar **enters the new YZ number
on its own Navroz, 21 March**, with YZ = Gregorian year − 630 from 21 March; so 21 March 2024 = **Fasli YZ 1394**
(validated against Parsi Khabar, 'Jamshedi Navroze Mubarak 2024': Roj Hormuzd Mah Fravardin 21 Mar 2024, and
consistent with Wikipedia's 1370 for 2000). zcserv's 1393 equals the Shahanshahi/Kadmi number still running on that
day (those calendars reach 1394 only at their own Navroz in July/August 2024); that is a likely explanation of
the difference, not a confirmed one. ZRE = Gregorian year + 1738,
changing on 21 March (Fasli) or at Iran's Nowruz (Bastani). The 'Era' setting chooses YZ, ZRE or both; the
Shahanshahi, Kadmi and Sasanian calendars have only YZ, so ZRE is not shown for them. For Bastani the Iranian civil
(Solar Hijri, SH) year is shown as well.

### 7. The Gahs, step by step
The day begins at sunrise. Every time below is computed for the chosen place from JPL sunrise, true (solar) noon,
sunset and solar midnight, so the clock times change with the place and the season.

| Gah | when | presiding | prayers |
|---|---|---|---|
| Havan | Sunrise to noon | Mithra, with Raman (Ram Khvastra) | Havan Gah prayer; Khorshed and Meher Niyayesh (said in each of the three day watches); most priestly rites, including the Yasna, are performed in this watch. |
| Rapithwin | Noon to mid-afternoon (about 3 p.m.), in the seven summer months only | Asha Vahishta (Ardibehesht), with Atar, fire | Rapithwin Gah prayer; Khorshed and Meher Niyayesh. |
| Second Havan | Noon to mid-afternoon in the five winter months and the Gatha days | Mithra, as in the morning Havan | Havan Gah prayer said a second time; Khorshed and Meher Niyayesh. |
| Uziran | Mid-afternoon to sunset | Berezat Ahura Napat Apam (Burz Yazad), with the waters | Uziran Gah prayer; Khorshed and Meher Niyayesh (the last of the day). |
| Aiwisruthrem | Sunset to midnight | The fravashis of the righteous | Aiwisruthrem Gah prayer; Mah Niyayesh may be said when the moon is up. |
| Ushahin | Midnight to dawn | Sraosha (Srosh), with Rashnu and Arshtat | Ushahin Gah prayer; Srosh is invoked as guardian of the night against the demons of darkness. |

**Rapithwin practice** (setting; preset key `rapithwin` of the Traditions presets):
- *Summer rule* (`summer`, default): Rapithwin Gah from Hormazd roj of Fravardin mah to Aneran roj of Meher mah;
  Second Havan in its place in the other five months and the Gatha days (Khordeh Avesta, Kanga tr.). It is
  applied in the calendar you chose, so Shahanshahi and Kadmi users' Rapithwin returns in August/July.
- *Bundahishn winter rule* (`medieval_four`): outside the Rapithwin season there are only four watches, the
  morning Havan running on until Uziran. It is offered for the Sasanian model and is selected automatically when
  you switch to the Sasanian calendar (you can change it).

Rapithwin is the spirit of the noon heat and lord of the summer. In Zoroastrian teaching the sun stood still at noon before evil entered the world, Ohrmazd performed the sacrifice of creation in Rapithwin's hour, and the final restoration will also be completed at noon. The Zoroastrian summer lasts seven months, from Navroz to the end of the Ayathrem Gahambar (30 Meher); for the five winter months Rapithwin withdraws under the earth to keep the springs and the roots of plants warm, and he is not invoked at noon: the Second Havan replaces his watch. At noon on Navroz (Hormazd roj of Fravardin mah) he is welcomed back with a jashan, a Yasna and the Afrinagan of Rapithwin; Boyce noted that in this ceremony the officiating priest faces west, whereas at other jashans he faces east. Failure to keep Rapithwin is listed as a sin in the Middle Persian confessions (patet). In the Fasli and Bastani calendars Rapithwin returns at the spring equinox; in the Shahanshahi and Kadmi calendars the 'summer' months have drifted, so Rapithwin now returns in August and July. The Bundahishn describes an older winter rule with only four watches, the morning Havan running on until Uziran; the app offers this as the 'medieval_four' setting, used for the Sasanian reconstruction.

*Sources:* Wikipedia, 'Rapithwin' (summary of EIr, 'Rapithwin', and M. Boyce, 'Rapithwin, No Ruz, and the Feast of Sade', 1968); Wikipedia, 'Zoroastrian calendar' (Bundahishn winter rule); Parsi Times (Gujarati), 'દરેક ગેહ માંડવાનો વખત' (2018: Rapithwin begins at noon on Hormazd roj of Fravardin mah)

**Community timetables.** Parsi timetables do not all follow the plain astronomical rule. A Parsi Times guide (2018) counts the Havan watch from 36 minutes before sunrise and the Aiwisruthrem watch from 72 minutes after sunset, and gives local-time rules for when each Gah may be begun. Iranian calendars print the watches in clock times. The app uses the astronomical events and says so; a user who follows a priest's timetable should follow the timetable.

*Sources:* Parsi Times (Gujarati), 'દરેક ગેહ માંડવાનો વખત', July 2018. UNCERTAIN: one community guide.

**Far north and far south.** If sunset comes less than 3 hours after noon, the Rapithwin/Second Havan watch ends
half-way between noon and sunset. In polar day or polar night, when the Sun does not rise or set, sunrise and sunset
are replaced by true noon − 6 h and + 6 h, and the rows are marked 'polar'. These are the app's conventions, not
rulings of any priestly authority.

### 8. Facing the light
Zoroastrians pray standing, facing a source of light, which stands for the light of Ahura Mazda and of Asha. Encyclopaedia Iranica's account of the kusti ritual gives the rule: while untying and tying the sacred cord, face east from dawn to midday and west until sunset, that is, toward the sun; at night, face an oil lamp, a fire, the moon or the stars. When there is no light at all, face south, held to be the direction of Ahura Mazda's heavenly abode. Dastur Jamaspji Jamasp-Asa's description of the same ritual adds that one should face south at midday, even when the sun is to the north. North is avoided because the Vendidad makes it the region from which Angra Mainyu and the demons rush forth. In a fire temple the worshipper faces the sacred fire. The compass page shows the bearing of the Sun by day and of the Moon at night, with south as the fallback, from the JPL ephemeris.

*Sources:* EIr, 'Kustig' (read via search extract); Dastur J. M. Jamasp-Asa, 'The Kushti ritual' (reprinted by CAIS); Vendidad 19.1; Wikipedia, 'Zoroastrian prayer' (after Boyce 1996, p. 258); Kersey H. Antia, 'Basic Zoroastrian Prayers' (avesta.org: 'During the day, pray facing the sun and at night, facing a light')

The Today page's live compass points to the Sun when it is above the horizon, to the Moon when it is up at night,
and otherwise asks you to face a lamp or a fire. On phones the dial turns with the device (iPhone/iPad after you tap
'Turn on the live compass' and allow Motion & Orientation; Android automatically). The phone's magnetic heading is
corrected to true north with the World Magnetic Model 2025 (pygeomag). Nothing leaves your browser.

### 9. Iranian festivals in the Bastani calendar
With the Bastani calendar the app shows each jashan on its Bastani date: Mehregan = Meher roj of Meher mah = civil
**10 Mehr**, the Tir jashan = civil **10 Tir** (checked for every year 1850–2149 in the validation). Popular
civil-calendar variants are noted beside them: **Tirgan on 13 Tir**, the date kept in Iran's official calendar, and
**Mehregan on 16 Mehr**, an older date some people still mark (surfiran.com, 'Iranian Festivals Calendar
2026/2027'; livingintehran.com, 'Mehregan', 10 Nov 2026). Sadeh, Chaharshanbe Suri and the civil Tirgan are Iranian
observances; they are shown with the Bastani calendar, and with the Parsi calendars only if you switch on 'Show
Iranian civil observances'.

### 9a. Prayers (links to the texts)
Prayer names in the app are links. They open the prayer on **avesta.org** (Avesta -- Zoroastrian Archives, edited by
Joseph H. Peterson) in a new tab, with the Avestan text and an English translation. The Khorda Avesta follows Ervad
K. E. Kanga; the Yashts and the Yasna use the Sacred Books of the East translations (J. Darmesteter, L. H. Mills), with
some Gatha chapters in Bartholomae's translation (via I. J. S. Taraporewala). The app only links to these pages and
copies no prayer text. The **Prayers** page lists all 41 prayers by group and links the whole Khorda Avesta in
English, Gujarati and Persian (PDF).

Where the links appear, and which prayers are linked, follows the rubrics of the Khorda Avesta:
- **Today, the current Gah:** the kusti, the Srosh Baj and the Gah prayer. In the three day watches (Havan or Second
  Havan, Rapithwin, Uziran) also the Khorshed and Meher Niyayesh. In Aiwisruthrem also the Srosh Yasht Vadi and the
  Mah Niyayesh, and in Ushahin also the Hoshbam.
- **Gatha days:** the Gatha of the day (Ahunavaiti, Ushtavaiti, Spentamainyu, Vohukhshathra, Vahishtoishti) and the
  Afrinagan of the Gatha days.
- **Festivals (Today and the Festivals page):**
  - Pateti: the Patet Pashemani.
  - Muktad and Farvardigan: the Farvardin Yasht and the Afrinagans.
  - The Gahambars: the Afrinagan of the Gahambar.
  - The Rapithwin festival: the Afrinagan of Rapithwin.
  - Each name-day jashan: the Yasht or Niyayesh of that day's yazata, e.g. Avan Niyayesh and Aban Yasht for the Avan
    jashan, Atash Niyayesh for Adar. Where the Khorda Avesta has no separate Yasht (Amardad, Shehrevar,
    Aspandarmad), the Siroza is linked.
- **The Moon:** the Mah Niyayesh on the Today page and in the list of Mah Niyayesh days.

Families and priests may follow other customs. The Persian and Gujarati prayer names were made for the app; they are
listed with the other unconfirmed spellings on the About page. `tools/check_prayer_links.py` re-checks that every link
loads and every section anchor exists (63 links, 0 problems in November 2026).

### 10. Caveats
- The **Sasanian calendar is a reconstruction**, shown for comparison like Sky Luach's 'Early Temple Period'; no
  community keeps it, and its options (andargāh position, 120-year intercalation and its phase) are scholarly
  models, not a record of practice.
- Dates are computed. Communities announce their own dates; where a printed almanac (panchang) differs, follow it.
  The open check of Shahanshahi Navroz 2026 (15 vs 16 August in published lists) is described in VALIDATION.md.
- The **18-day Muktad** follows the engine's rule (Ashishvangh roj of Aspandarmad to Amardad roj of Fravardin;
  Karanjia, avesta.org). The Traditions notes add that the starting day varies by family.
- Persian, Gujarati and Avestan spellings come from names.py; forms that could not be confirmed are listed on the
  About page.
