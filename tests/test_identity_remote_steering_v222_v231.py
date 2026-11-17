"""Tests for v2.22-v2.31 Bell steering and nonlinear branch response."""
import unittest
from models.identity_remote_steering_v222_v231 import run
class TenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_222(self):self.assertAlmostEqual(self.r['v2.22']['Bell_norm'],1)
 def test_223(self):self.assertLess(self.r['v2.23']['A_POVM_error'],1e-12)
 def test_224(self):self.assertLess(self.r['v2.24']['B_POVM_error'],1e-12)
 def test_225(self):self.assertLess(self.r['v2.25']['unconditioned_trace_distance'],1e-12)
 def test_226(self):self.assertAlmostEqual(self.r['v2.26']['difference'],.1)
 def test_227(self):self.assertGreater(self.r['v2.27']['KL'],.02)
 def test_228(self):self.assertEqual(self.r['v2.28']['critical_at_most'],473)
 def test_229(self):
  for x in self.r['v2.29']['lambda_scan']:self.assertAlmostEqual(x['pB'],.5-x['lambda']/4)
 def test_230(self):self.assertAlmostEqual(self.r['v2.30']['shared_affine_minimax_distance'],.05)
 def test_231(self):self.assertFalse(self.r['v2.31']['identity_specific_prediction'])
if __name__=='__main__':unittest.main()
