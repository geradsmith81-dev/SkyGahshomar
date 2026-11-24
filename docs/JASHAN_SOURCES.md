# Jashan-day research for Sky Gahshomar: confidence and conflicts

Compiled 24 November 2026. This is a companion to `jashan_research.json`. It contains research only, no code.

## Method

- Sources were web searches, direct page fetches (Heritage Institute, Wikipedia English and Persian via the MediaWiki API) and search-result extracts. Encyclopaedia Iranica and the Great Islamic Encyclopaedia (CGIE) were read only through search extracts.
- Every Gregorian date reported by a source was checked against the calendar arithmetic. Shahenshahi uses a 365-day year with 1 Fravardin 1391 YZ = 16 Aug 2021. Kadmi = Shahenshahi + 30 days. Bastani uses 30-day months from 21 March, mapped onto the Solar Hijri 31/30-day months. Agreement is recorded in each record's `check` field.

## A. Atash Behram salgirehs (8 of 9 found)

| Fire | Roj / Mah | Kept by | Consecrated | Confidence |
|---|---|---|---|---|
| Iranshah, Udvada | Adar / Adar | Shahenshahi (a Fasli Adar/Adar salgreh is also held) | Sanjan 721 CE (90 YZ); Udvada 1742 | High |
| Navsari (Desai/Bhagarsath) | Sarosh / Ardibehesht | Shahenshahi | 2 Dec 1765, 1135 YZ | High |
| Dadyseth, Mumbai | Sarosh / Fravardin | **Kadmi** | 29 Sep 1783, 1153 YZ | High; see conflict |
| Modi, Surat | Sarosh / Ardibehesht | Shahenshahi | 19 Nov 1823, 1193 YZ | High |
| Vakil, Surat | Ardibehesht / Tir | **Kadmi** | 5 Dec 1823, 1193 YZ | High; see conflict |
| Wadiaji, Mumbai | Sarosh / Ardibehesht | Shahenshahi | 17 Nov 1830, 1200 YZ | High |
| Banaji, Mumbai | Sarosh / Khordad | Shahenshahi (date evidence) | 13 Dec 1845, 1215 YZ | High for roj/mah; see conflict |
| Anjuman, Mumbai | Ardibehesht / Ardibehesht | Shahenshahi | 17 Oct 1897, 1267 YZ | High |
| Yazd Atash Bahram | not found | | building 1313-1318 SH | Not found |

Conflicts:

- **Dadyseth.** Heritage Institute, a community PDF and Parsi Times (2024) print "Roj Govad, Mah Aspandad 1153". Encyclopaedia Iranica (citing Patell 1888) and Parsi Times (2025) give **Kadmi Sarosh/Fravardin 1153**, and only that form matches 29 Sep 1783. The Shahenshahi equivalent of that day is Sarosh/Aspandarmad, not Govad. The temple also keeps the Gregorian 29 September anniversary.
- **Vakil.** The commonly printed "Ardibehesht/Khordad" is the Shahenshahi equivalent. The Kadmi date the temple keeps is Ardibehesht/Tir (Parsi Times 2022; ahuramazda.com). A 2026 online calendar lists the Kadmi Surat Atash Behram salgreh on 16 Oct 2026, which is Kadmi Ardibehesht/Tir.
- **Banaji.** Heritage Institute labels it "Kadmi". The consecration date and reported salgreh dates (31 Oct 2021; 30 Oct 2026) match Sarosh/Khordad only in the **Shahenshahi** calendar, so the app should place it there.
- **Anjuman.** One speech gives the foundation stone as "Daepaadar roj" on 17 Oct 1897, but that date is Ardibehesht roj. The salgreh is Ardibehesht/Ardibehesht.
- **Note on Sarosh/Ardibehesht.** Navsari, Modi and Wadiaji share Sarosh roj, Ardibehesht mah. Parsi Times reports them together, so the app can show one combined chip if desired.

## B. Iranian names (12/12)

Persian names and customs come from Persian Wikipedia; the Dey dates from Amordad News. The civil equivalents of the Bastani dates were computed, and they match the civil dates Persian Wikipedia itself gives where stated (Ordibeheshtgan 2 Ordibehesht, Tirgan 10 Tir, Amordadgan 3 Mordad, Abangan 4 Aban, Azargan 3 Azar, Bahmangan 26 Dey). Amordad News confirms the four Deygan days at civil 25 Azar and 2, 9 and 17 Dey.

- **Conflict: Sepandarmazgan.** Persian Wikipedia gives civil 5 Esfand, but Bastani 5 Esfand falls on civil 29 Bahman. Both are in popular use; show the Bastani date and mention 5 Esfand.
- **Customs are one-liners.** Several rest on al-Biruni as relayed by Wikipedia, so they describe historical or general Iranian practice rather than current Zoroastrian practice. Medium confidence.

## C. Shab-e Yalda

- **Civil rule (high confidence).** The evening of 30 Azar, the night before 1 Dey (English Wikipedia).
- **Solstice.** The festival is tied to the calendar date, not the exact solstice instant. The statement that the solstice falls on 30 Azar or 1 Dey is inferred from the calendar's structure; showing the computed JPL solstice beside it is suggested.
- **Zoroastrian name.** Iranian Zoroastrians call it Jashn-e Shab-e Chelleh (Rasti almanac via Amordad News). 1 Dey was al-Biruni's Khorram-ruz / Navad-ruz.
- **Bastani clash.** In Bastani reckoning Khorram-ruz (Hormazd roj, Dae mah) falls on civil 25 Azar, about 5 days before Yalda. The app should not merge Yalda with jashan_dae.

## D. Pirs (6/6)

The primary source is CGIE "Zardoshtiyan", which gives Zoroastrian roj ranges with civil equivalents. Heritage Institute, Amordad News, Berasad, Kojaro and Safarmarket corroborate it. All dates are **Bastani roj/mah with fixed civil (Solar Hijri) equivalents**:

| Pir | Bastani | Civil | Gregorian | Days |
|---|---|---|---|---|
| Herisht | Farvardin, Amordad-Khorshed | 7-11 Farvardin | 27-31 Mar | 5 |
| Sabz (Chak Chak) | Khordad, Ashtad-Aneran | 24-28 Khordad | 14-18 Jun | 5 |
| Seti Pir | Khordad, Ashtad | 24 Khordad | 14 Jun | 1 |
| Narestaneh | Tir, Aspandarmad-Adar | 2-6 Tir | 23-27 Jun | 5 |
| Banu-Pars | Tir, Meher-Behram | 13-17 Tir | 4-8 Jul | 5 |
| Naraki | Amordad, Meher-Behram | 12-16 Mordad | 3-7 Aug | 5 |

Conflicts:

- Heritage Institute writes Pir-e Sabz as "Ashtad-Mahraspand" (4 roj) but gives 5 Gregorian days.
- One source gives Seti Pir the whole 14-18 June span.
- The figure honoured at Naraki varies by source.
- Persian Wikipedia wrongly redirects Naraki to Narestaneh.

Encyclopaedia Iranica was not retrieved, and Boyce (1977) was read only through a secondary quotation; neither is the basis for any date.

## E. Other fixed days (3)

| Day | Roj / Mah (Shahenshahi) | Confidence |
|---|---|---|
| Homaji ni Baj | Govad / Dae | High |
| Dasturji Kukadaru's birthday | Zamyad / Avan | High; Wikipedia gives 26 May vs 27 May 1831 |
| Dasturji Kukadaru's Baj | Behram / Fravardin | High; Wikipedia's "4 Jan 1900" is inconsistent with the roj/mah, 4 Oct 1900 fits |

A Mumbai blog calls Zamyad/Avan the Baj. This is outvoted by frashogard and the Zoroastrian Association of California (ZAC) calendar, and by the arithmetic on the 1831 birth date.

## Not found or not included

- Yazd Atash Bahram salgireh.
- Zarathushtra's Navjote.
- A Sanjan-arrival jashan.
- Behram roj (monthly) and the Bahman-mah nabor days (customary over the whole month): not single annual jashans.
- BPP, Jam-e-Jamshed and Parsiana calendars were not directly retrieved.
