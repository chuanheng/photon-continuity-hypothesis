"""Ten tests for v1.82-v1.91. Requires numpy/scipy."""
import unittest
from models.identity_channel_audit_v182_v191 import run
class V182V191Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_v182(self):self.assertEqual(self.r['v1.82']['spectator_label_accessible_gap'],0)
 def test_v183(self):self.assertLess(self.r['v1.83']['different_kraus_sets_same_channel_gap'],1e-12)
 def test_v184(self):self.assertLess(self.r['v1.84']['kraus_completeness_error'],1e-12)
 def test_v185(self):self.assertLess(max(self.r['v1.85'].values()),1e-12)
 def test_v186(self):self.assertAlmostEqual(self.r['v1.86']['unitality_trace_distance'],.18)
 def test_v187(self):self.assertGreater(self.r['v1.87']['KL'],0)
 def test_v188(self):self.assertLess(self.r['v1.88']['expected_LLR_5_event_proxy'],200)
 def test_v189(self):
  self.assertLessEqual(self.r['v1.89']['actual_type_I'],.05)
  self.assertGreater(self.r['v1.89']['exact_power'],.99)
  self.assertEqual(self.r['v1.89']['seeded_ground_count'],140)
 def test_v190(self):self.assertEqual(self.r['v1.90']['profile_KL'],0)
 def test_v191(self):self.assertFalse(self.r['v1.91']['unique_identity_prediction'])
if __name__=='__main__':unittest.main()
