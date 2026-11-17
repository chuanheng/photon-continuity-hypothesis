"""v2.12-v2.21 stage tests: python -m unittest discover -s tests -p 'test_identity_nonlinear_v212_v221.py' -v"""
import unittest,math
from models.identity_nonlinear_v212_v221 import main,evolve,distance
class TenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=main()
 def test_v212(self):self.assertFalse(self.r['v2.12']['identity_specific'])
 def test_v213(self):self.assertIn('sum',self.r['v2.13']['affine_law'])
 def test_v214(self):self.assertAlmostEqual(evolve((1,0,0))[0],.2)
 def test_v215(self):self.assertGreaterEqual(self.r['v2.15']['sampled_minimum_eigenvalue'],0)
 def test_v216(self):self.assertAlmostEqual(self.r['v2.16']['trace_distance'],.15)
 def test_v217(self):
  self.assertLess(distance(self.r['v2.17']['input_A'],self.r['v2.17']['input_B']),1e-12)
  self.assertAlmostEqual(self.r['v2.17']['P_plus_A'],.5)
  self.assertAlmostEqual(self.r['v2.17']['P_plus_B'],.4)
 def test_v218(self):self.assertGreater(self.r['v2.18']['KL_B_to_A'],.02)
 def test_v219(self):self.assertAlmostEqual(self.r['v2.19']['minimax_trace_distance'],.05)
 def test_v220(self):
  self.assertAlmostEqual(self.r['v2.20']['P_click_A'],.4365)
  self.assertAlmostEqual(self.r['v2.20']['P_click_B'],.3532)
  self.assertGreater(self.r['v2.20']['z_statistic'],3)
 def test_v221(self):self.assertFalse(self.r['v2.21']['unique_photon_identity_prediction'])
if __name__=='__main__':unittest.main()
