import unittest

from .model import constrained_refit, witness


class PhaseTests(unittest.TestCase):
    def test_442_noncommuting_control(self):
        result = witness()
        self.assertLess(result["max_formula_error"], 1e-14)
        self.assertAlmostEqual(result["x_readout_total_variation_pi_over_2"], 0.5)

    def test_443_calibration_and_exact_ordinary_refit(self):
        result = constrained_refit()
        self.assertAlmostEqual(result["calibrated_solution"][2], 0.24)
        self.assertAlmostEqual(result["ordinary_coherent_solution"][0], 0.5)
        self.assertAlmostEqual(result["ordinary_coherent_solution"][2], 0.0)
