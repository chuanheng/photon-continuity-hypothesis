"""Ten tests: v3.02-v3.11."""
import unittest
from models.identity_paper_audit_v302_v311 import calc
class TenTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=calc()
 def test_302(self):self.assertEqual(self.r['v3.02']['symmetric_rank'],3)
 def test_303(self):self.assertLess(self.r['v3.03']['inert_label_max_gap'],1e-12)
 def test_304(self):self.assertAlmostEqual(self.r['v3.04']['candidate_HOM'],.2408)
 def test_305(self):self.assertEqual(self.r['v3.05']['fisher_rank_analytic'],1)
 def test_306(self):self.assertEqual(self.r['v3.06']['candidate'],self.r['v3.06']['standard'])
 def test_307(self):self.assertEqual(self.r['v3.07']['critical_ge'],27);self.assertEqual(self.r['v3.07']['profile_KL'],0)
 def test_308(self):self.assertGreater(self.r['v3.08']['restricted_KL'],0)
 def test_309(self):self.assertLess(self.r['v3.09']['similarity_gauge_max_probability_gap'],1e-12)
 def test_310(self):self.assertAlmostEqual(self.r['v3.10']['mixed_HOM_coincidence'],.31);self.assertAlmostEqual(self.r['v3.10']['noisy_candidate'],self.r['v3.10']['noisy_standard'])
 def test_311(self):self.assertFalse(self.r['v3.11']['new_identity_prediction'])
if __name__=='__main__':unittest.main()
