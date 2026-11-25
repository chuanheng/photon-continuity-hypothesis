import unittest
import numpy as np
from .model import run

class CrossRatio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=run()
    def test_ratio(self):
        self.assertAlmostEqual(self.r['v7.02']['cross_ratio'],1.34554,5)
    def test_gain(self):
        self.assertAlmostEqual(self.r['v7.03']['after_gains'],self.r['v7.02']['log_ratio'])
    def test_null(self):
        np.testing.assert_equal(self.r['v7.04']['contrast_times_design'],[0,0,0])
    def test_projection(self):
        r=self.r['v7.05']['cell_residuals']
        self.assertAlmostEqual(r[0]-r[1]-r[2]+r[3],self.r['v7.02']['log_ratio'])
    def test_independent(self):
        r=self.r['v7.06']
        self.assertAlmostEqual(np.linalg.norm(r['relative_stat_proxies']),r['independent_log_sd'])
    def test_paired(self):
        r=self.r['v7.07']
        self.assertLess(r['1.0'],r['0.0'])
        self.assertLess(r['0.0'],r['-1.0'])
    def test_bounds(self):
        r=self.r['v7.08']
        self.assertEqual(r['min_log_sd'],0)
        self.assertGreater(r['max_log_sd'],self.r['v7.07']['-1.0'])
    def test_narrow(self):
        self.assertAlmostEqual(self.r['v7.09']['cross_ratio_narrow'],1.41346,5)
    def test_minimax(self):
        r=self.r['v7.10']
        self.assertAlmostEqual(r['symmetric_multiplier']**4,r['one_cell_multiplier'])
    def test_interaction(self):
        self.assertLess(self.r['v7.11']['max_relative_error'],1e-12)
        self.assertAlmostEqual(self.r['v7.11']['ordinary_interaction'],self.r['v7.02']['log_ratio'])
