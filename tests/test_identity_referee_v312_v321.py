"""Ten stage tests for adversarial peer review v3.12-v3.21."""
import unittest
from models.identity_referee_v312_v321 import calc
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=calc()
 def test_312(self):self.assertFalse(self.r['v3.12']['claim_originality_proven'])
 def test_313(self):self.assertLess(self.r['v3.13']['closed_CPTP_ensemble_gap'],1e-12)
 def test_314(self):
  self.assertAlmostEqual(self.r['v3.14']['same_initial_reduced_gap'],0)
  self.assertAlmostEqual(self.r['v3.14']['feedback_output_gap'],1)
 def test_315(self):self.assertAlmostEqual(self.r['v3.15']['setting_dependent_channel_gap'],.5)
 def test_316(self):self.assertLess(self.r['v3.16']['same_CPTP_ensemble_gap'],1e-12)
 def test_317(self):self.assertAlmostEqual(self.r['v3.17']['mixed_HOM'],.31)
 def test_318(self):self.assertAlmostEqual(self.r['v3.18']['noisy_candidate_p'],self.r['v3.18']['noisy_standard_p'])
 def test_319(self):self.assertEqual(self.r['v3.19']['critical_ge'],27)
 def test_320(self):self.assertLess(self.r['v3.20']['gauge_probability_gap'],1e-12)
 def test_321(self):self.assertFalse(self.r['v3.21']['originality_established'])
if __name__=='__main__':unittest.main()
