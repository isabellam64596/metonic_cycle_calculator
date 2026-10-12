import unittest
from datetime import date

from metonic_cycle_calculator import (
    GOLDEN_NUMBER,
    PASCHAL_FULL_MOON_DATES,
    MetonicCycleCalculator,
    InvalidYearError,
)


class TestGoldenNumber(unittest.TestCase):
    def setUp(self):
        self.calc = MetonicCycleCalculator()

    def test_known_golden_numbers(self):
        # 2024: 2024 % 19 = 10, +1 = 11
        self.assertEqual(self.calc.golden_number(2024), 11)
        # 2025: 2025 % 19 = 11, +1 = 12
        self.assertEqual(self.calc.golden_number(2025), 12)

    def test_golden_number_range(self):
        for y in range(1900, 2200):
            gn = self.calc.golden_number(y)
            self.assertGreaterEqual(gn, 1)
            self.assertLessEqual(gn, 19)

    def test_year_at_boundary_min(self):
        self.assertEqual(self.calc.golden_number(1900), 1)

    def test_year_at_boundary_max(self):
        # 2199 % 19 = 14, +1 = 15
        self.assertEqual(self.calc.golden_number(2199), 15)

    def test_year_below_range_raises(self):
        with self.assertRaises(InvalidYearError):
            self.calc.golden_number(1899)

    def test_year_above_range_raises(self):
        with self.assertRaises(InvalidYearError):
            self.calc.golden_number(2200)


class TestPaschalFullMoon(unittest.TestCase):
    def setUp(self):
        self.calc = MetonicCycleCalculator()

    def test_2024_paschal_full_moon(self):
        # Golden number 11 -> March 25
        self.assertEqual(
            self.calc.paschal_full_moon(2024),
            date(2024, 3, 25),
        )

    def test_returns_date_object(self):
        result = self.calc.paschal_full_moon(2020)
        self.assertIsInstance(result, date)

    def test_all_golden_numbers_give_valid_dates(self):
        for gn in range(1, 20):
            # Find a year in range with this golden number.
            year = 1900 + (gn - 1)
            if year > 2199:
                year -= 19
            d = self.calc.paschal_full_moon(year)
            # Confirm month is March or April (the only legal months
            # for a Paschal full moon).
            self.assertIn(d.month, (3, 4))

    def test_march_dates_have_valid_days(self):
        calc = MetonicCycleCalculator()
        for gn in range(1, 20):
            year = 1900 + gn - 1
            if year > 2199:
                year -= 19
            d = calc.paschal_full_moon(year)
            if d.month == 3:
                self.assertGreaterEqual(d.day, 21)
                self.assertLessEqual(d.day, 31)

    def test_april_dates_have_valid_days(self):
        calc = MetonicCycleCalculator()
        for gn in range(1, 20):
            year = 1900 + gn - 1
            if year > 2199:
                year -= 19
            d = calc.paschal_full_moon(year)
            if d.month == 4:
                self.assertGreaterEqual(d.day, 1)
                self.assertLessEqual(d.day, 19)

    def test_paschal_full_moon_out_of_range_raises(self):
        with self.assertRaises(InvalidYearError):
            self.calc.paschal_full_moon(1899)


class TestCycleForYear(unittest.TestCase):
    def setUp(self):
        self.calc = MetonicCycleCalculator()

    def test_keys(self):
        result = self.calc.cycle_for_year(2024)
        expected_keys = {"year", "golden_number", "paschal_full_moon", "cycle_start_year"}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_values_consistent(self):
        result = self.calc.cycle_for_year(2024)
        self.assertEqual(result["year"], 2024)
        self.assertEqual(result["golden_number"], 11)
        self.assertEqual(result["paschal_full_moon"], date(2024, 3, 25))

    def test_cycle_start_year(self):
        # Golden number 1 means the year IS the cycle start.
        result = self.calc.cycle_for_year(1900)
        self.assertEqual(result["cycle_start_year"], 1900)

    def test_cycle_start_year_offset(self):
        # 2024 has golden number 11, so cycle started at 2024 - 10 = 2014
        result = self.calc.cycle_for_year(2024)
        self.assertEqual(result["cycle_start_year"], 2014)


class TestModuleConstants(unittest.TestCase):
    def test_golden_number_constant(self):
        self.assertEqual(GOLDEN_NUMBER, tuple(range(1, 20)))
        self.assertEqual(len(GOLDEN_NUMBER), 19)

    def test_paschal_full_moon_dates_length(self):
        self.assertEqual(len(PASCHAL_FULL_MOON_DATES), 20)

    def test_paschal_full_moon_dates_entries_are_tuples(self):
        for entry in PASCHAL_FULL_MOON_DATES[1:]:
            self.assertIsInstance(entry, tuple)
            self.assertEqual(len(entry), 2)


if __name__ == "__main__":
    unittest.main()
