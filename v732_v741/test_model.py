import math
import unittest
from .model import run
r=run()
class Normalization(unittest.TestCase):
    def test_rates(self):
        for y in r['v7.32']['per_flux_rates']: self.assertAlmostEqual(y,.2)
    def test_matching(self):
        self.assertAlmostEqual(r['v7.33']['matched_log_cross'],0)
    def test_path(self):
        self.assertAlmostEqual(r['v7.34']['net_log_cross']/.001,-.792782,5)
    def test_weighted(self):
        self.assertGreater(r['v7.35']['weighted_ratio_low'],r['v7.35']['weighted_ratio_high'])
    def test_bound(self):
        self.assertLess(abs(r['v7.35']['single_arm_log_residual']),r['v7.36']['one_arm_log_bound'])
    def test_background(self):
        self.assertAlmostEqual(math.log1p(r['v7.37']['one_cell_background_fraction']),-r['v7.37']['normalized_log_bias'])
    def test_pooling(self):
        self.assertAlmostEqual(r['v7.38']['pooled_ratio']-r['v7.38']['equal_block_mean'],1/15)
    def test_covariance(self):
        self.assertAlmostEqual(r['v7.39']['independent_log_variance']-r['v7.39']['subset_log_variance'],.002)
    def test_monitor(self):
        self.assertAlmostEqual(-math.log(r['v7.40']['monitor_low']),r['v7.40']['equal_signal_log_ratio'])
    def test_decomposition(self):
        self.assertAlmostEqual(r['v7.41']['raw_log_cross'],r['v7.41']['monitor_log_cross'])
