"""v2.72-v2.81 GitHub mirror tests."""
import unittest
from models.identity_full_sequence_v272_v281 import run
class TenTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_272(self):self.assertLess(self.r['v2.72']['write_unitarity_error'],1e-12)
 def test_273(self):self.assertLess(self.r['v2.73']['reverse_trace_distance'],1e-12)
 def test_274(self):self.assertAlmostEqual(self.r['v2.74']['normalization'],1)
 def test_275(self):self.assertAlmostEqual(self.r['v2.75']['outputs']['photon_X_plus'],self.r['v2.75']['analytic_X_plus'])
 def test_276(self):self.assertGreater(self.r['v2.76']['probe_dephasing_drop'],.05)
 def test_277(self):self.assertLess(self.r['v2.77']['all_observed_fields_max_gap'],1e-12)
 def test_278(self):self.assertEqual(self.r['v2.78']['fisher_rank'],1)
 def test_279(self):self.assertLess(self.r['v2.79']['max_scan_gap'],1e-12)
 def test_280(self):self.assertEqual(self.r['v2.80']['synthetic_click_count'],7071)
 def test_281(self):self.assertFalse(self.r['v2.81']['identity_specific_prediction'])
if __name__=='__main__':unittest.main()
