import unittest

import numpy as np

from .model import run


class MatchedDesign(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = run()

    def test_v862(self):
        self.assertAlmostEqual(self.results["v8.62"]["contrast_standard_deviation"], 0.08)

    def test_v863(self):
        self.assertAlmostEqual(self.results["v8.63"]["worst_case_contrast_sd"], 0.2)

    def test_v864(self):
        np.testing.assert_allclose(
            self.results["v8.64"]["main_effect_calibration_contrast_sensitivity"], 0
        )

    def test_v865(self):
        self.assertEqual(self.results["v8.65"]["science_plus_reference_rank"], 2)

    def test_v866(self):
        self.assertAlmostEqual(self.results["v8.66"]["recovered_candidate"],
                               self.results["v8.67"]["true_candidate"])

    def test_v867(self):
        self.assertGreater(self.results["v8.67"]["apparent_candidate"],
                           self.results["v8.67"]["true_candidate"])

    def test_v868(self):
        self.assertEqual(self.results["v8.68"]["abba_drift_moments_orders_0_to_3"][:2], [0, 0])

    def test_v869(self):
        self.assertGreater(self.results["v8.69"]["variance_reduction_fraction"], 0.5)

    def test_v870(self):
        self.assertGreater(self.results["v8.70"]["required_science_exposure_multiplier"], 20)

    def test_v871(self):
        self.assertEqual(self.results["v8.71"]["protocol_rank"], 3)
