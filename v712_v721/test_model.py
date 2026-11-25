import math
import unittest
from .model import run
r=run()
class Calibration(unittest.TestCase):
    def test_windows(self):
        self.assertAlmostEqual(r['v7.12']['recoil_windows_keV'][0][1],20.112)
    def test_common(self):
        self.assertAlmostEqual(r['v7.13']['common_efficiency_product'],.9114)
    def test_one_anchor(self):
        self.assertEqual(r['v7.14']['ordinary_log_gains'][2],0)
    def test_two_anchors(self):
        a,b,c,d=r['v7.15']['ordinary_log_gains']
        self.assertEqual((c,d),(0,0))
        self.assertAlmostEqual(a-b,.296796,5)
    def test_bound(self):
        self.assertAlmostEqual(r['v7.16']['required_log_slope_abs']*1.179,.296796,5)
    def test_counts(self):
        self.assertEqual(r['v7.17']['equal_reference_counts_per_cell'],1600)
    def test_noise(self):
        self.assertAlmostEqual(r['v7.18']['combined_log_sd']**2-r['v7.18']['science_log_sd']**2,.0025)
    def test_exposure(self):
        m=r['v7.19']['science_exposure_multiplier']
        self.assertAlmostEqual(math.hypot(r['v7.18']['science_log_sd']/math.sqrt(m),.05),r['v7.19']['target_total_log_sd'])
    def test_drift(self):
        self.assertEqual(r['v7.20']['abba_drift_moments'],[0,0,2])
    def test_swap(self):
        self.assertAlmostEqual(r['v7.21']['swap_odd_if_stable']-r['v7.21']['odd_null_reference_corrected'],.1)
