"""Sanity checks for the illustrative Poisson energy-loss model.

Run: python3 -m unittest discover -s tests -v
"""
import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "models"))
import attenuation as model


class ToyModelTests(unittest.TestCase):
    def test_zero_thickness(self):
        result = model.simulate(0)
        self.assertEqual(result["toy_simulated_mean_energy_keV"], model.E0_KEV)
        self.assertEqual(result["standard_expected_uncollided_count"], model.N)

    def test_mean_energy_formula(self):
        # Statistical check: Monte Carlo agrees with the analytical expectation.
        result = model.simulate(2)
        expected = result["toy_expected_mean_energy_keV"]
        self.assertLess(abs(result["toy_simulated_mean_energy_keV"] - expected) / expected, 0.02)

    def test_positive_energy(self):
        self.assertGreater(model.E0_KEV * (1 - model.ALPHA) ** 100, 0)
        self.assertTrue(0 < model.ALPHA < 1)

    def test_nist_reference(self):
        self.assertAlmostEqual(model.MU_CM_INV, 0.7497822, places=6)


if __name__ == "__main__":
    unittest.main()
