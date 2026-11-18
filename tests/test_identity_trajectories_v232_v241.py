"""Ten regression tests for v2.32-v2.41."""
import unittest
from models.identity_trajectories_v232_v241 import run
class TestTenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_232(self):self.assertLess(self.r["v2.32"]["Kraus_completeness_error"],1e-12)
 def test_233(self):self.assertAlmostEqual(sum(self.r["v2.33"].values()),1)
 def test_234(self):self.assertLess(self.r["v2.34"]["ensemble_reconstruction_gap"],1e-12)
 def test_235(self):
  self.assertLess(self.r["v2.35"]["unconditional_gap"],1e-12)
  self.assertGreater(self.r["v2.35"]["conditional_first_branch_distance"],.2)
 def test_236(self):self.assertLess(self.r["v2.36"]["Alice_marginal_gap"],1e-12)
 def test_237(self):self.assertLess(self.r["v2.37"]["Bob_marginal_after_Alice_X_gap"],1e-12)
 def test_238(self):self.assertLess(self.r["v2.38"]["equivalent_input_ensemble_channel_gap"],1e-12)
 def test_239(self):self.assertEqual(self.r["v2.39"]["jump_count"],3593)
 def test_240(self):self.assertLess(self.r["v2.40"]["two_step_channel_trajectory_gap"],1e-12)
 def test_241(self):self.assertFalse(self.r["v2.41"]["identity_specific_prediction"])
if __name__=='__main__':unittest.main()
