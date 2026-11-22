import json, pathlib, unittest
from heat_air_stress.scoring import (heat_index_c, heat_level, air_level_from_pm25, air_level_from_aqi,
                                     combine, stress, safer_hours, runs)
from heat_air_stress.advice import build_advice

SAMPLES = json.loads((pathlib.Path(__file__).resolve().parent.parent / "data" / "sample_days.json").read_text(encoding="utf-8"))


class TestHeatIndex(unittest.TestCase):
    def test_cool_day_close_to_air_temp(self):
        self.assertAlmostEqual(heat_index_c(27, 40), 26.5, delta=1.5)
    def test_nws_reference_80F_40pct(self):          # NWS table: 80F at 40% RH is about 80F (26.7C)
        self.assertAlmostEqual(heat_index_c(26.7, 40), 26.7, delta=1.0)
    def test_humidity_raises_heat_index(self):
        self.assertGreater(heat_index_c(35, 70), heat_index_c(35, 30))
    def test_temperature_raises_heat_index(self):
        self.assertGreater(heat_index_c(40, 40), heat_index_c(34, 40))


class TestLevels(unittest.TestCase):
    def test_heat_boundaries(self):
        self.assertEqual([heat_level(x) for x in (31.9, 32, 38.9, 39, 50.9, 51)], [0, 1, 1, 2, 2, 3])
    def test_imd_override(self):
        self.assertEqual(heat_level(30, "orange"), 2)
        self.assertEqual(heat_level(30, "red"), 3)
        self.assertEqual(heat_level(45, "yellow"), 2)
    def test_pm25_boundaries(self):
        self.assertEqual([air_level_from_pm25(x) for x in (60, 61, 90, 91, 120, 121)], [0, 1, 1, 2, 2, 3])
    def test_aqi_boundaries(self):
        self.assertEqual([air_level_from_aqi(x) for x in (100, 101, 200, 201, 300, 301)], [0, 1, 1, 2, 2, 3])


class TestCombine(unittest.TestCase):
    def test_base_is_max(self):
        self.assertEqual(combine(1, 0, "street_vendor"), 1)
        self.assertEqual(combine(0, 2, "street_vendor"), 2)
    def test_interaction_rule(self):
        self.assertEqual(combine(2, 2, "street_vendor"), 3)
        self.assertEqual(combine(1, 2, "street_vendor"), 2)   # only one is High: no uplift
    def test_exertion_uplift(self):
        self.assertEqual(combine(1, 0, "delivery_rider"), 2)
        self.assertEqual(combine(0, 0, "delivery_rider"), 0)  # no uplift when Low
    def test_cap_at_three(self):
        self.assertEqual(combine(3, 3, "construction"), 3)


class TestSafeHours(unittest.TestCase):
    def test_summer_day_has_early_safer_window(self):
        r = safer_hours(SAMPLES["summer_heatwave"], "street_vendor")
        self.assertIn(6, r["best_work_hours"])
        self.assertTrue(r["rest_hours"])
        self.assertTrue(all(12 <= h <= 21 or h >= 10 for h in r["rest_hours"]))
    def test_smog_all_day_has_no_safer_window(self):
        r = safer_hours(SAMPLES["winter_smog"], "street_vendor")
        self.assertEqual(r["best_work_hours"], [])
    def test_mild_day_flags_no_rest(self):
        r = safer_hours(SAMPLES["mild_day"], "delivery_rider")
        self.assertEqual(r["rest_hours"], [])
    def test_runs_groups_contiguous_hours(self):
        self.assertEqual(runs([6, 7, 8, 12, 13, 20]), [(6, 9), (12, 14), (20, 21)])


class TestAdvice(unittest.TestCase):
    def test_both_languages_nonempty_all_levels(self):
        for lang in ("en", "hi"):
            for s in range(4):
                r = {"score": s, "heat_level": s, "air_level": s}
                self.assertTrue(build_advice(r, lang))
    def test_severe_includes_medical_help_line(self):
        r = stress(45, 15, 150, "delivery_rider")
        self.assertEqual(r["score"], 3)
        self.assertEqual(len(build_advice(r, "en")), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
