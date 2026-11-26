import unittest

import numpy as np

from .model import run


class IndependentCalibration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = run()

    def test_v852(self):
        self.assertAlmostEqual(self.results["v8.52"]["cross_ratio"], 1.34554098)

    def test_v853(self):
        self.assertAlmostEqual(self.results["v8.53"]["min_linf_log_bias"] * 4,
                               self.results["v8.52"]["log_cross_ratio"])

    def test_v854(self):
        self.assertAlmostEqual(self.results["v8.54"]["min_l2_log_bias"] * 2,
                               self.results["v8.52"]["log_cross_ratio"])

    def test_v855(self):
        gram = np.array(self.results["v8.55"]["mode_gram"])
        np.testing.assert_allclose(gram, 4 * np.eye(4))

    def test_v856(self):
        self.assertAlmostEqual(self.results["v8.56"]["post_refit_contrast"], 0)

    def test_v857(self):
        self.assertLess(self.results["v8.57"]["per_cell_independent_log_sd_limit_95pct"], 0.08)

    def test_v858(self):
        self.assertGreater(self.results["v8.58"]["poisson_counts_per_cell_95pct"], 100)

    def test_v859(self):
        self.assertLess(self.results["v8.59"]["observed_z_proxy"], 1)

    def test_v860(self):
        self.assertEqual(self.results["v8.60"]["candidate_ordinary_rank"], 1)

    def test_v861(self):
        self.assertGreater(self.results["v8.61"]["two_sided_95pct_half_width"],
                           self.results["v8.52"]["log_cross_ratio"])
