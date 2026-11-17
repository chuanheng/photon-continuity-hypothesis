"""Ten tests for v2.02-v2.11 statistical calibration synthesis."""
import unittest
from models.identity_evidence_v202_v211 import run
class TestSynthesis(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_202(self):self.assertEqual(self.r['v2.02']['audited_candidate_count'],8)
 def test_203(self):self.assertEqual(self.r['v2.03']['inert_identity_kl'],0)
 def test_204(self):self.assertGreater(self.r['v2.04']['exact_power'],.999)
 def test_205(self):
  p=self.r['v2.05']['finite_references']
  self.assertLess(p['1000']['alternative']['rejection_fraction'],p['20000']['alternative']['rejection_fraction'])
 def test_206(self):
  v=self.r['v2.06']['joint_asimov']
  self.assertLess(v['1000']['expected_log_lr'],v['20000']['expected_log_lr'])
 def test_207(self):self.assertGreater(self.r['v2.07']['drift']['0.020']['rejection_fraction'],.98)
 def test_208(self):self.assertAlmostEqual(self.r['v2.08']['detected_click'],self.r['v2.08']['alternate_click'])
 def test_209(self):
  self.assertTrue(all(x['rejection_fraction']<.07 for x in self.r['v2.09']['null_rates'].values()))
 def test_210(self):self.assertGreater(self.r['v2.10']['power']['5000']['rejection_fraction'],.98)
 def test_211(self):self.assertFalse(self.r['v2.11']['identity_specific_prediction'])
if __name__=='__main__':unittest.main()
