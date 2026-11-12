"""Run with: python3 -m unittest discover -s tests -v"""
import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "models"))
import standard_baseline as baseline


class BaselineTests(unittest.TestCase):
    def test_nist_coefficient(self):
        self.assertAlmostEqual(baseline.AL_LINEAR_ATTENUATION_CM_INV, 0.7497822)

    def test_zero_thickness(self):
        self.assertEqual(baseline.uncollided_fraction(0), 1)

    def test_monotonic(self):
        self.assertGreater(baseline.uncollided_fraction(1), baseline.uncollided_fraction(2))

    def test_exponential_composition(self):
        self.assertAlmostEqual(baseline.uncollided_fraction(2), baseline.uncollided_fraction(1)**2)

    def test_negative_thickness(self):
        with self.assertRaises(ValueError):
            baseline.uncollided_fraction(-1)


if __name__ == "__main__":
    unittest.main()
