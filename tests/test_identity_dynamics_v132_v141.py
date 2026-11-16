"""Ten regression checks for v1.32-v1.41."""
import unittest
from models.identity_dynamics_v132_v141 import *
class TenRoundTests(unittest.TestCase):
    def test_v132(self):
        self.assertAlmostEqual(survival(0,DELTA,4),1)
    def test_v133(self):
        self.assertEqual(run()['v1.33']['spectator_effect'],0)
    def test_v134(self):
        self.assertGreater(run()['v1.34']['max_probability_difference'],.15)
    def test_v135(self):
        self.assertLess(channel_gap(),1e-12)
    def test_v136(self):
        self.assertEqual(run()['v1.36']['excitation_commutator_norm'],0)
    def test_v137(self):
        self.assertEqual(run()['v1.37']['forbidden_N1_to_N2_amplitude'],0)
    def test_v138(self):
        self.assertGreater(detuning_scan()[1],.05)
    def test_v139(self):
        self.assertGreater(run()['v1.39']['sum_kl_ideal'],.4)
    def test_v140(self):
        a=run()
        self.assertLess(a['v1.40']['sum_kl_detected'],a['v1.39']['sum_kl_ideal'])
    def test_v141(self):
        self.assertEqual(run()['v1.41']['minimum_kl_with_static_detuning_noise'],0)
if __name__=='__main__':unittest.main()
