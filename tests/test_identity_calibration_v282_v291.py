"""Ten regression tests for v2.82-v2.91. No real photon experiment."""
import unittest
from models.identity_calibration_v282_v291 import run
class TestTenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_282(self):self.assertEqual(self.r['v2.82']['main_only_fisher_rank'],1)
 def test_283(self):self.assertEqual(self.r['v2.83']['rank_main_plus_two_refs'],3)
 def test_284(self):self.assertEqual(self.r['v2.84']['full_fisher_rank'],5)
 def test_285(self):self.assertEqual(self.r['v2.85']['counts'],[6947,4603,4875,49,4518])
 def test_286(self):self.assertAlmostEqual(self.r['v2.86']['coverage_95'],.953)
 def test_287(self):self.assertLess(self.r['v2.87']['estimated_s_bias'],-.01)
 def test_288(self):self.assertLess(self.r['v2.88']['max_gap'],1e-12)
 def test_289(self):self.assertGreater(self.r['v2.89']['KL_wrong_fixed_s_one'],0)
 def test_290(self):self.assertFalse(self.r['v2.90']['permanent_photon_identity_proven'])
 def test_291(self):self.assertFalse(self.r['v2.91']['unique_identity_prediction'])
if __name__=='__main__':unittest.main()
