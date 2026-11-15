"""Tests for the Sky Gahshomar engine. Run from the engine folder:  python -m pytest tests
(or without pytest:  python tests/test_engine.py). Needs ephem/de440s.bsp or SKY_EPHEM_DIR."""
import os
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import festivals as F  # noqa: E402
import iran_solar as ir  # noqa: E402
import sky_engine as se  # noqa: E402
import sky_layer as sl  # noqa: E402
import zcalendars as zc  # noqa: E402
import znames as zn  # noqa: E402


def test_published_navroz():
    assert zc.navroz(1396, "shahanshahi") == date(2026, 8, 15)      # Maharashtra gazette 2026
    assert zc.navroz(1395, "shahanshahi") == date(2025, 8, 15)
    assert zc.navroz(1395, "kadmi") == date(2025, 7, 16)
    assert zc.to_zdate(date(2023, 8, 16), "shahanshahi").day_of_year == 1
    z = zc.to_zdate(date(2020, 8, 6), "shahanshahi")
    assert (z.year, z.mah_key, z.roj_key) == (1389, "aspandarmad", "ashtad")


def test_epoch():
    assert zc.YZ_EPOCH_JDN == zc.julian_to_jdn(632, 6, 16)
    assert zc.to_zdate(zc.from_jdn(zc.YZ_EPOCH_JDN), "kadmi").label() == "Hormazd roj, Fravardin mah, YZ 1"


def test_fasli_and_zre():
    assert zc.to_zdate(date(2024, 3, 20), "fasli").roj_key == "avardad_sal_gah"
    z = zc.to_zdate(date(2024, 3, 21), "fasli")
    assert (z.mah, z.day, z.eras["ZRE"], z.eras["YZ"]) == (1, 1, 3762, 1394)
    assert zc.to_zdate(date(2013, 3, 21), "fasli").eras["ZRE"] == 3751
    assert not zc.is_leap(1394, "fasli") and zc.is_leap(1393, "fasli")


def test_bastani():
    assert zc.navroz(3763, "bastani") == date(2025, 3, 21) == ir.nowruz(2025)
    assert zc.navroz(3762, "bastani") == date(2024, 3, 20)
    mg = zc.from_zdate(3765, 7, 16, "bastani")
    assert mg == date(2027, 10, 2) and ir.to_civil(mg) == (1406, 7, 10)


def test_sasanian():
    lay = zc.year_layout(1396, "sasanian")
    assert [m for m, _, _ in lay][:10] == [1, 2, 3, 4, 5, 6, 7, 8, 13, 9]
    assert zc.year_length(1320, "sasanian", intercalation="kabisa_120") == 395
    for o in ({}, {"andargah": "after_aspandarmad"}, {"intercalation": "kabisa_120"}):
        d = date(2000, 1, 1)
        for i in range(0, 4000, 7):
            z = zc.to_zdate(d + timedelta(days=i), "sasanian", **o)
            assert zc.from_zdate(z.year, z.mah, z.day, "sasanian", repeated=z.repeated_month, **o) == d + timedelta(days=i)


def test_roundtrip_all():
    for cal in zc.CALENDARS:
        d = date(2023, 1, 1)
        while d < date(2029, 1, 1):
            z = zc.to_zdate(d, cal)
            assert zc.from_zdate(z.year, z.mah, z.day, cal) == d
            d += timedelta(days=1)


def test_festivals():
    fs = {f.key: f for f in F.festivals_in_year(1396, "shahanshahi")}
    assert fs["navroz"].start == date(2026, 8, 15)
    assert fs["muktad"].days == 10 and fs["muktad"].end == date(2027, 8, 14)
    assert fs["khordad_sal"].start == date(2026, 8, 20)
    f18 = {f.key: f for f in F.festivals_in_year(1395, "shahanshahi", muktad="parsi_18")}
    assert f18["muktad"].days == 18
    fa = {f.key: f for f in F.festivals_in_year(1395, "fasli")}
    assert fa["jashan_meher"].start == date(2025, 10, 2)
    assert fa["zarthost_no_diso"].start == date(2025, 12, 26)
    assert fa["sadeh"].start == date(2026, 1, 30)
    assert fa["chaharshanbe_suri"].start == date(2026, 3, 17)


def test_gahs_and_sunrise():
    g = sl.gahs(date(2026, 8, 15), se.MUMBAI, "shahanshahi")
    keys = [x.key for x in g["gahs"]]
    assert keys == ["havan", "rapithwin", "uziran", "aiwisruthrem", "ushahin"]
    g2 = sl.gahs(date(2026, 1, 15), se.MUMBAI, "fasli")
    assert g2["gahs"][1].key == "second_havan"
    sd = se.solar_day(se.MUMBAI, date(2026, 8, 15))
    assert zc.zdate_at(sd["sunrise"] - timedelta(minutes=1), se.MUMBAI, "shahanshahi").roj_key == "vahishtoisht"
    assert zc.zdate_at(sd["sunrise"] + timedelta(minutes=1), se.MUMBAI, "shahanshahi").roj_key == "hormazd"


def test_names():
    for k in zn.ROJ_KEYS:
        assert zn.ROJ[k]["ae"] and zn.ROJ[k]["fa"] and zn.ROJ[k]["gu"]
    assert len(zn.MAH) == 12 and len(zn.GATHA) == 6 and len(zn.GAH) == 6
    assert zn.display(zn.MAH, "meher") == "Meher · مهر · મેહેર"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
