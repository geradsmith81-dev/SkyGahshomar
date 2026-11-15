# Name reconciliation: engine `znames.py` vs content `names.py`

Decision: `names.py` (content track) is the canonical display source. `znames.py` is now a thin shim that
re-exports it (keeping the engine API). The engine spellings listed below were **dropped**; the app shows the
`names.py` form. Engine-only data kept: `meaning`, `fa_alt`, festival keys `rapithwin_jashan`, `tirgan_civil`.

174 field differences across 74 entries.

Avestan note: the engine wrote bare stems (e.g. *ahura mazdā*); names.py writes the genitive/dative forms used in
the Siroza day dedications and checked against TITUS (e.g. *ahurahe mazdā̊*), so most Avestan rows differ by design.

| table | key | field | names.py (shown) | engine znames (dropped) |
|---|---|---|---|---|
| ROJ | adar | ae | '𐬁𐬚𐬭𐬋' | '𐬁𐬙𐬀𐬭' |
| ROJ | adar | ae_tr | 'āϑrō' | 'ā t a r' |
| ROJ | amardad | ae | '𐬀𐬨𐬆𐬭𐬆𐬙𐬀𐬙𐬁𐬙𐬋' | '𐬀𐬨𐬆𐬭𐬆𐬙𐬁𐬙' |
| ROJ | amardad | ae_tr | 'amərətatātō' | 'a m ə r ə t ā t' |
| ROJ | aneran | fa | 'انیران' | 'انارام' |
| ROJ | aneran | gu | 'અનેરાંન' | 'અનેરાન' |
| ROJ | aneran | ae | '𐬀𐬥𐬀𐬖𐬭𐬀𐬥𐬄𐬨⸱𐬭𐬀𐬊𐬗𐬀𐬢𐬵𐬄𐬨' | '𐬀𐬥𐬀𐬖𐬭𐬀⸱𐬭𐬀𐬊𐬗𐬂' |
| ROJ | aneran | ae_tr | 'anaγranąm raocaŋhąm' | 'a n a γ r a |
| ROJ | ardibehesht | gu | 'અરદીબેહેશત' | 'અરદીબહેસ્ત' |
| ROJ | ardibehesht | ae | '𐬀𐬴𐬀𐬵𐬈⸱𐬬𐬀𐬵𐬌𐬱𐬙𐬀𐬵𐬈' | '𐬀𐬱𐬀⸱𐬬𐬀𐬵𐬌𐬱𐬙𐬀' |
| ROJ | ardibehesht | ae_tr | 'aṣ̌ahe vahištahe' | 'a š a |
| ROJ | ashishvangh | gu | 'અશીશવંદ' | 'અશીશવંઘ' |
| ROJ | ashishvangh | ae | '𐬀𐬴𐬋𐬌𐬱⸱𐬬𐬀𐬢𐬵𐬎𐬌𐬌𐬃' | '𐬀𐬴𐬌⸱𐬬𐬀𐬢𐬎𐬵𐬍' |
| ROJ | ashishvangh | ae_tr | 'aṣ̌ōiš vaŋhuiiā̊' | 'a ṣ̌ i |
| ROJ | ashtad | gu | 'આશતાદ' | 'આસ્તાદ' |
| ROJ | ashtad | ae | '𐬀𐬭𐬱𐬙𐬁𐬙𐬋' | '𐬀𐬭𐬱𐬙𐬁𐬙' |
| ROJ | ashtad | ae_tr | 'arštātō' | 'a r š t ā t' |
| ROJ | asman | ae | '𐬀𐬴𐬥𐬋' | '𐬀𐬯𐬨𐬀𐬥' |
| ROJ | asman | ae_tr | 'aṣ̌nō' | 'a s m a n' |
| ROJ | avan | ae | '𐬀𐬞𐬄𐬨⸱𐬬𐬀𐬢𐬎𐬵𐬍𐬥𐬄𐬨' | '𐬁𐬞𐬋' |
| ROJ | avan | ae_tr | 'apąm vaŋuhīnąm' | 'ā p ō' |
| ROJ | bahman | gu | 'બેહમન' | 'બહમન' |
| ROJ | bahman | ae | '𐬬𐬀𐬢𐬵𐬀𐬎𐬎𐬈⸱𐬨𐬀𐬥𐬀𐬢𐬵𐬈' | '𐬬𐬊𐬵𐬎⸱𐬨𐬀𐬥𐬀𐬵' |
| ROJ | bahman | ae_tr | 'vaŋhauue manaŋhe' | 'v o h u |
| ROJ | behram | gu | 'બેહેરાંમ' | 'બહેરામ' |
| ROJ | behram | ae | '𐬬𐬆𐬭𐬆𐬚𐬭𐬀𐬖𐬥𐬀𐬵𐬈' | '𐬬𐬆𐬭𐬆𐬚𐬭𐬀𐬖𐬥𐬀' |
| ROJ | behram | ae_tr | 'vərəϑraγnahe' | 'v ə r ə θ r a γ n a' |
| ROJ | dae_pa_adar | fa | 'دی به آذر' | 'دی\u200cبه\u200cآذر' |
| ROJ | dae_pa_adar | gu | 'દએ પ આદર' | 'દએપઆદર' |
| ROJ | dae_pa_adar | ae | '𐬛𐬀𐬚𐬎𐬴𐬋⸱𐬀𐬵𐬎𐬭𐬀𐬵𐬈⸱𐬨𐬀𐬰𐬛𐬃' | '𐬛𐬀𐬜𐬎𐬎𐬂' |
| ROJ | dae_pa_adar | ae_tr | 'daϑuṣ̌ō ahurahe mazdā̊' | 'd a δ u u å' |
| ROJ | dae_pa_din | fa | 'دی به دین' | 'دی\u200cبه\u200cدین' |
| ROJ | dae_pa_din | gu | 'દએ પ દીન' | 'દએપદીન' |
| ROJ | dae_pa_din | ae | '𐬛𐬀𐬚𐬎𐬴𐬋⸱𐬀𐬵𐬎𐬭𐬀𐬵𐬈⸱𐬨𐬀𐬰𐬛𐬃' | '𐬛𐬀𐬜𐬎𐬎𐬂' |
| ROJ | dae_pa_din | ae_tr | 'daϑuṣ̌ō ahurahe mazdā̊' | 'd a δ u u å' |
| ROJ | dae_pa_meher | fa | 'دی به مهر' | 'دی\u200cبه\u200cمهر' |
| ROJ | dae_pa_meher | gu | 'દએ પ મેહેર' | 'દએપમેહેર' |
| ROJ | dae_pa_meher | ae | '𐬛𐬀𐬚𐬎𐬴𐬋⸱𐬀𐬵𐬎𐬭𐬀𐬵𐬈⸱𐬨𐬀𐬰𐬛𐬃' | '𐬛𐬀𐬜𐬎𐬎𐬂' |
| ROJ | dae_pa_meher | ae_tr | 'daϑuṣ̌ō ahurahe mazdā̊' | 'd a δ u u å' |
| ROJ | din | ae | '𐬛𐬀𐬉𐬥𐬀𐬌𐬌𐬃⸱𐬬𐬀𐬢𐬵𐬎𐬌𐬌𐬃' | '𐬛𐬀𐬉𐬥𐬁' |
| ROJ | din | ae_tr | 'daēnaiiā̊ vaŋhuiiā̊' | 'd a ē n ā' |
| ROJ | fravardin | ae | '𐬟𐬭𐬀𐬎𐬎𐬀𐬴𐬌𐬥𐬄𐬨' | '𐬟𐬭𐬀𐬎𐬎𐬀𐬴𐬌' |
| ROJ | fravardin | ae_tr | 'frauuaṣ̌inąm' | 'f r a u u a ṣ̌ i' |
| ROJ | gosh | ae | '𐬔𐬇𐬎𐬱⸱𐬎𐬭𐬎𐬥𐬈' | '𐬔𐬆𐬎𐬱' |
| ROJ | gosh | ae_tr | 'gə̄uš urune' | 'g ə u š' |
| ROJ | govad | ae | '𐬬𐬁𐬙𐬀𐬵𐬈' | '𐬬𐬁𐬙𐬀' |
| ROJ | govad | ae_tr | 'vātahe' | 'v ā t a' |
| ROJ | hormazd | gu | 'હોરમજદ' | 'હોરમઝદ' |
| ROJ | hormazd | ae | '𐬀𐬵𐬎𐬭𐬀𐬵𐬈⸱𐬨𐬀𐬰𐬛𐬃' | '𐬀𐬵𐬎𐬭𐬀⸱𐬨𐬀𐬰𐬛𐬁' |
| ROJ | hormazd | ae_tr | 'ahurahe mazdā̊' | 'a h u r a |
| ROJ | khordad | fa | 'خرداد' | 'خورداد' |
| ROJ | khordad | ae | '𐬵𐬀𐬎𐬭𐬎𐬎𐬀𐬙𐬁𐬙𐬋' | '𐬵𐬀𐬎𐬭𐬎𐬎𐬀𐬙𐬁𐬙' |
| ROJ | khordad | ae_tr | 'hauruuatātō' | 'h a u r u u a t ā t' |
| ROJ | khorshed | ae | '𐬵𐬎𐬎𐬀𐬭𐬆𐬑𐬴𐬀𐬉𐬙𐬀𐬵𐬈' | '𐬵𐬎𐬎𐬀𐬭𐬆⸱𐬑𐬱𐬀𐬉𐬙𐬀' |
| ROJ | khorshed | ae_tr | 'huuarəxṣ̌aētahe' | 'h u u a r ə |
| ROJ | mareshpand | fa | 'مهراسپند' | 'مانتره\u200cسپند' |
| ROJ | mareshpand | gu | 'મારેસપંદ' | 'મારેસ્પંદ' |
| ROJ | mareshpand | ae | '𐬨𐬄𐬚𐬭𐬀𐬵𐬈⸱𐬯𐬞𐬆𐬧𐬙𐬀𐬵𐬈' | '𐬨𐬄𐬚𐬭𐬀⸱𐬯𐬞𐬆𐬧𐬙𐬀' |
| ROJ | mareshpand | ae_tr | 'mąϑrahe spəṇtahe' | 'm ą θ r a |
| ROJ | meher | ae | '𐬨𐬌𐬚𐬭𐬀𐬵𐬈' | '𐬨𐬌𐬚𐬭𐬀' |
| ROJ | meher | ae_tr | 'miϑrahe' | 'm i θ r a' |
| ROJ | mohor | ae | '𐬨𐬄𐬢𐬵𐬀𐬵𐬈' | '𐬨𐬂𐬢𐬵𐬀' |
| ROJ | mohor | ae_tr | 'mąŋhahe' | 'm å ŋ h a' |
| ROJ | ram | gu | 'રાંમ' | 'રામ' |
| ROJ | ram | ae | '𐬭𐬁𐬨𐬀𐬥𐬋⸱𐬓𐬁𐬯𐬙𐬭𐬀𐬵𐬈' | '𐬭𐬁𐬨𐬀𐬥' |
| ROJ | ram | ae_tr | 'rāmanō xᵛāstrahe' | 'r ā m a n' |
| ROJ | rashne | gu | 'રશ્ને' | 'રશને' |
| ROJ | rashne | ae | '𐬭𐬀𐬴𐬥𐬀𐬊𐬱' | '𐬭𐬀𐬱𐬥𐬎' |
| ROJ | rashne | ae_tr | 'raṣ̌naoš' | 'r a š n u' |
| ROJ | shehrevar | gu | 'શેહેરેવર' | 'શહેરેવર' |
| ROJ | shehrevar | ae | '𐬑𐬴𐬀𐬚𐬭𐬀𐬵𐬈⸱𐬬𐬀𐬌𐬭𐬌𐬌𐬈𐬵𐬈' | '𐬑𐬱𐬀𐬚𐬭𐬀⸱𐬬𐬀𐬌𐬭𐬌𐬌𐬀' |
| ROJ | shehrevar | ae_tr | 'xṣ̌aϑrahe vairiiehe' | 'x š a θ r a |
| ROJ | spendarmad | gu | 'અસફનદારમદ' | 'સ્પેંદારમદ' |
| ROJ | spendarmad | ae | '𐬯𐬞𐬆𐬧𐬙𐬀𐬌𐬌𐬃⸱𐬬𐬀𐬢𐬵𐬎𐬌𐬌𐬃⸱𐬁𐬭𐬨𐬀𐬙𐬋𐬌𐬱' | '𐬯𐬞𐬆𐬧𐬙𐬁⸱𐬁𐬭𐬨𐬀𐬌𐬙𐬌' |
| ROJ | spendarmad | ae_tr | 'spəṇtaiiā̊ vaŋhuiiā̊ ārmatōiš' | 's p ə ṇ t ā |
| ROJ | srosh | ae | '𐬯𐬭𐬀𐬊𐬴𐬀𐬵𐬈' | '𐬯𐬭𐬀𐬊𐬱𐬀' |
| ROJ | srosh | ae_tr | 'sraoṣ̌ahe' | 's r a o š a' |
| ROJ | tir | ae | '𐬙𐬌𐬱𐬙𐬭𐬌𐬌𐬈𐬵𐬈' | '𐬙𐬌𐬱𐬙𐬭𐬌𐬌𐬀' |
| ROJ | tir | ae_tr | 'tištriiehe' | 't i š t r i i a' |
| ROJ | zamyad | gu | 'જમીઆદ' | 'જમીયાદ' |
| ROJ | zamyad | ae | '𐬰𐬆𐬨𐬋' | '𐬰𐬀𐬨' |
| ROJ | zamyad | ae_tr | 'zəmō' | 'z a m' |
| GATHA | ahunavad | fa | 'اهنودگاه' | 'اهنود' |
| GATHA | ahunavad | ae_tr | 'ahunauuaitī' | 'a h u n a u u a i t ī' |
| GATHA | avardad_sal_gah | fa | 'اورداد' | 'اورداد سال\u200cگاه' |
| GATHA | avardad_sal_gah | gu | 'આવરદાદ સાલ' | 'અવરદાદ સાલ ગાહ' |
| GATHA | avardad_sal_gah | ae | None | '' |
| GATHA | avardad_sal_gah | ae_tr | None | '' |
| GATHA | spentomad | fa | 'سپنتمدگاه' | 'سپنتمد' |
| GATHA | spentomad | gu | 'સપેનતોમદ' | 'સ્પેન્તોમદ' |
| GATHA | spentomad | ae | '𐬯𐬞𐬆𐬧𐬙𐬁⸱𐬨𐬀𐬌𐬥𐬌𐬌𐬏' | '𐬯𐬞𐬆𐬧𐬙𐬁⸱𐬨𐬀𐬌𐬥𐬌𐬌𐬎' |
| GATHA | spentomad | ae_tr | 'spəṇtā.mainiiū' | 's p ə ṇ t ā |
| GATHA | ushtavad | fa | 'اشتودگاه' | 'اشتود' |
| GATHA | ushtavad | gu | 'ઉશતવદ' | 'ઉસ્તવદ' |
| GATHA | ushtavad | ae_tr | 'uštauuaitī' | 'u š t a u u a i t ī' |
| GATHA | vahishtoisht | fa | 'وهیشتواشت\u200cگاه' | 'وهشتوایشت' |
| GATHA | vahishtoisht | gu | 'વહીશતોઈશત' | 'વહીસ્તોઇસ્ત' |
| GATHA | vahishtoisht | ae | '𐬬𐬀𐬵𐬌𐬱𐬙𐬋𐬌𐬱𐬙𐬍' | '𐬬𐬀𐬵𐬌𐬱𐬙𐬋𐬌𐬱𐬙𐬌' |
| GATHA | vahishtoisht | ae_tr | 'vahištōištī' | 'v a h i š t ō i š t i' |
| GATHA | vohukhshathra | fa | 'وهوخشترگاه' | 'وهوخشتر' |
| GATHA | vohukhshathra | gu | 'વોહુખષથર' | 'વોહુક્ષથ્ર' |
| GATHA | vohukhshathra | ae | '𐬬𐬊𐬵𐬎𐬑𐬴𐬀𐬚𐬭𐬁' | '𐬬𐬊𐬵𐬎⸱𐬑𐬱𐬀𐬚𐬭𐬁' |
| GATHA | vohukhshathra | ae_tr | 'vohuxṣ̌aϑrā' | 'v o h u |
| MAH | ardibehesht | gu | 'અરદીબેહેશત' | 'અરદીબહેસ્ત' |
| MAH | aspandarmad | gu | 'અસફનદારમદ' | 'અસ્પંદાર્મદ' |
| MAH | bahman | gu | 'બેહમન' | 'બહમન' |
| MAH | khordad | fa | 'خرداد' | 'خورداد' |
| MAH | shehrevar | gu | 'શેહેરેવર' | 'શહેરેવર' |
| GAH | aiwisruthrem | en | 'Aiwisruthrem' | 'Aiwisruthrem Gah' |
| GAH | aiwisruthrem | fa | 'اویسروترمگاه' | 'گاه اویسروترم' |
| GAH | aiwisruthrem | gu | 'અઈવીસ્ત્રુથ્રેમ ગેહ' | 'અઇવીસરુથ્રેમ ગેહ' |
| GAH | aiwisruthrem | ae | '𐬀𐬌𐬡𐬌𐬯𐬭𐬏𐬚𐬭𐬌𐬨𐬁𐬌' | '𐬀𐬌𐬡𐬌𐬯𐬭𐬎𐬚𐬭𐬌𐬨𐬀' |
| GAH | aiwisruthrem | ae_tr | 'aiβisrūϑrimāi' | 'aiβisruθrima' |
| GAH | havan | en | 'Havan' | 'Havan Gah' |
| GAH | havan | fa | 'هاونگاه' | 'گاه هاون' |
| GAH | havan | ae | '𐬵𐬁𐬎𐬎𐬀𐬥𐬇𐬈' | '𐬵𐬁𐬎𐬎𐬀𐬥𐬌' |
| GAH | havan | ae_tr | 'hāuuanə̄e' | 'hāuuani' |
| GAH | rapithwin | en | 'Rapithwin' | 'Rapithwin Gah' |
| GAH | rapithwin | fa | 'رپیتونیگاه' | 'گاه رپیتون' |
| GAH | rapithwin | gu | 'રપિથ્વન ગેહ' | 'રપીથવન ગેહ' |
| GAH | rapithwin | ae | '𐬭𐬀𐬞𐬌𐬚𐬡𐬌𐬥𐬁𐬌' | '𐬭𐬀𐬞𐬌𐬚𐬡𐬌𐬥𐬀' |
| GAH | rapithwin | ae_tr | 'rapiϑβināi' | 'rapiθβina' |
| GAH | second_havan | en | 'Second Havan' | 'Second Havan Gah' |
| GAH | second_havan | fa | 'هاونگاه دوم' | 'هاون دوم' |
| GAH | second_havan | ae | '𐬵𐬁𐬎𐬎𐬀𐬥𐬇𐬈' | '𐬵𐬁𐬎𐬎𐬀𐬥𐬌' |
| GAH | second_havan | ae_tr | 'hāuuanə̄e' | 'hāuuani' |
| GAH | ushahin | en | 'Ushahin' | 'Ushahin Gah' |
| GAH | ushahin | fa | 'اوشهنگاه' | 'گاه اشهین' |
| GAH | ushahin | ae | '𐬎𐬴𐬀𐬵𐬌𐬥𐬁𐬌' | '𐬎𐬱𐬀𐬵𐬌𐬥𐬀' |
| GAH | ushahin | ae_tr | 'uṣ̌ahināi' | 'ušahina' |
| GAH | uziran | en | 'Uziran' | 'Uziran Gah' |
| GAH | uziran | fa | 'ازیرنیگاه' | 'گاه ازیرن' |
| GAH | uziran | ae | '𐬎𐬰𐬀𐬌𐬌𐬈𐬌𐬭𐬌𐬥𐬁𐬌' | '𐬎𐬰𐬀𐬪𐬈𐬌𐬭𐬌𐬥𐬀' |
| GAH | uziran | ae_tr | 'uzaiieirināi' | 'uzaẏeirina' |
| FESTIVAL | farvardigan | en | 'Farvardinegan (19 Fravardin)' | 'Farvardigan (Fravardin roj, Fravardin mah)' |
| FESTIVAL | farvardigan | gu | 'જશને ફરવરદીગન' | 'ફરવરદીનગાન' |
| FESTIVAL | gahambar_ayathrem | gu | 'અયાથરેમ ગહમ્બાર' | 'અયાથ્રેમ ગાહમ્બાર' |
| FESTIVAL | gahambar_hamaspathmaedem | gu | 'હમાસ્પાથેમેદાયેમ ગહમ્બાર' | 'હમસ્પથમએદમ ગાહમ્બાર' |
| FESTIVAL | gahambar_maidyarem | gu | 'મૈધ્યરેમ ગહમ્બાર' | 'મઇદ્યારેમ ગાહમ્બાર' |
| FESTIVAL | gahambar_maidyoshahem | fa | 'گاهنبار میدیوشم' | 'گاهنبار میدیوشهیم' |
| FESTIVAL | gahambar_maidyoshahem | gu | 'મૈધ્યોશેમ ગહમ્બાર' | 'મઇદ્યોશહેમ ગાહમ્બાર' |
| FESTIVAL | gahambar_maidyozarem | gu | 'મૈધ્યોઝરેમ ગહમ્બાર' | 'મઇદ્યોઝરેમ ગાહમ્બાર' |
| FESTIVAL | gahambar_paitishahem | fa | 'گاهنبار پتیه\u200cشهیم' | 'گاهنبار پیته\u200cشهیم' |
| FESTIVAL | gahambar_paitishahem | gu | 'પૈતિશેમ ગહમ્બાર' | 'પઇતીશહેમ ગાહમ્બાર' |
| FESTIVAL | jamshedi_navroz | gu | 'જમ્શેદી નવરોઝ' | 'જમશેદી નવરોઝ' |
| FESTIVAL | jashan_adar | en | 'Adar Jashan (Atash nu Parab)' | 'Adar Jashan (Adar parab)' |
| FESTIVAL | jashan_adar | gu | 'આતશ નુ પરબ' | 'આદર જશન' |
| FESTIVAL | jashan_amardad | gu | 'જશને અમરદાદગન' | 'અમરદાદ જશન' |
| FESTIVAL | jashan_ardibehesht | gu | 'જશને અરદિબેહેશતગન' | 'અરદીબહેસ્ત જશન' |
| FESTIVAL | jashan_aspandarmad | gu | 'જશને અસફનદારમદગન' | 'અસ્પંદાર્મદ જશન' |
| FESTIVAL | jashan_avan | en | 'Avan Ardvisur Parab' | 'Avan Jashan (Avan Ardvisur parab)' |
| FESTIVAL | jashan_avan | gu | 'આવાં અર્દાવીસૂર નુ પરબ' | 'આવાં જશન' |
| FESTIVAL | jashan_bahman | gu | 'જશને બેહમનગન' | 'બહમન જશન' |
| FESTIVAL | jashan_dae | en | 'Dae Jashans' | 'Dae Jashan' |
| FESTIVAL | jashan_dae | gu | 'દએ માહ નુ જશન' | 'દએ જશન' |
| FESTIVAL | jashan_fravardin | en | 'Fravardin Jashan' | 'Fravardin Jashan (Farvardinegan)' |
| FESTIVAL | jashan_fravardin | fa | 'جشن فروردینگان' | 'فروردینگان' |
| FESTIVAL | jashan_fravardin | gu | 'ફરવરદીઆન જશન' | 'ફરવરદીન જશન' |
| FESTIVAL | jashan_khordad | gu | 'જશને ખોરદાદગન' | 'ખોરદાદ જશન' |
| FESTIVAL | jashan_meher | en | 'Mehergan' | 'Meher Jashan (Mehergan)' |
| FESTIVAL | jashan_meher | gu | 'જશને મેહેરગન' | 'મેહેર જશન (મેહેરગાન)' |
| FESTIVAL | jashan_shehrevar | gu | 'જશને શેહેરેવરગન' | 'શહેરેવર જશન' |
| FESTIVAL | jashan_tir | en | 'Tirgan' | 'Tir Jashan (Tirgan)' |
| FESTIVAL | jashan_tir | gu | 'જશને તીરગન' | 'તીર જશન (તીરગાન)' |
| FESTIVAL | mah_niyayesh | en | 'Mah Niyayesh (moon prayer)' | 'Mah Niyayesh (Moon prayer)' |
| FESTIVAL | mah_niyayesh | gu | 'માહ બોખતાર નિયાએશ' | 'માહ બોખતાર નીઆએશ' |
| FESTIVAL | muktad | en | 'Muktad (Farvardigan days)' | 'Muktad (Farvardegan days)' |
| FESTIVAL | muktad | gu | 'મુકતાદ' | 'મુક્તાદ' |
| FESTIVAL | pateti | fa | 'پتت' | 'پتتی' |
| FESTIVAL | sadeh | fa | 'جشن سده' | 'سده' |
| FESTIVAL | sadeh | gu | 'જશને સદેહ' | 'સદેહ' |
| FESTIVAL | zarthost_no_diso | gu | 'ઝર્થોસ્ત નો દિસો' | 'જરથોસ્તનો દીસો' |
| CALENDAR | bastani | en | 'Bastani (Iranian)' | 'Bastani (Iranian Zoroastrian)' |
| CALENDAR | fasli | gu | 'ફસલિ' | 'ફસલી' |

Extra festival keys present only in the engine (kept, spellings unverified, flagged in `names.UNCERTAIN`):

- `rapithwin_jashan`: Rapithwin Jashan (Ardibehesht roj, Fravardin mah) · جشن رپیتون · રપીથવનનું જશન
- `tirgan_civil`: Tirgan (Iranian civil 13 Tir) · تیرگان (۱۳ تیر) · તીરગાન (ઈરાની ૧૩ તીર)