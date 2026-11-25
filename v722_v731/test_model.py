import math
import unittest
from .model import mu,run
r=run()
class Transport(unittest.TestCase):
    def test_geometry(self):
        self.assertEqual(r['v7.22']['active_mm'],13)
    def test_table(self):
        self.assertAlmostEqual(mu(50),5.323*3.335)
    def test_exchange(self):
        self.assertAlmostEqual(math.log(r['v7.24']['ray_cross_ratio']),.002*r['v7.23']['difference'])
    def test_inverse(self):
        self.assertAlmostEqual(r['v7.25']['required_normal_path_difference_mm']*.1*r['v7.23']['difference'],.296796,5)
    def test_angle(self):
        self.assertAlmostEqual(r['v7.26']['secant']*r['v7.26']['required_thickness_difference_mm_common_angle'],r['v7.25']['required_normal_path_difference_mm'])
    def test_transmission(self):
        t=r['v7.27']
        self.assertAlmostEqual(t['transmission_extra_path_hi']/t['transmission_extra_path_lo'],1.34554,5)
    def test_band(self):
        self.assertAlmostEqual(r['v7.28']['log_span_for_total_40um'],.02905,5)
    def test_recoil(self):
        a,b=r['v7.29']['recoil_keV']
        self.assertAlmostEqual(b-a,1.179)
    def test_gate(self):
        a,b=r['v7.30']['trigger_probabilities']
        self.assertAlmostEqual(b/a,1.34554,5)
    def test_sum(self):
        self.assertGreater(min(r['v7.30']['sum_deficits_keV']),20*.5)
