"""v2.52-v2.61 ten regression tests."""
import unittest,math
from models.identity_operator_v252_v261 import run
class TestTenStages(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_252(self):self.assertEqual(self.r['v2.52']['bosonic_subspace_rank'],3);self.assertLess(self.r['v2.52']['inaccessible_label_probe_gap'],1e-12)
 def test_253(self):self.assertLess(self.r['v2.53']['coupling_commutator_fro'],1e-12);self.assertGreater(self.r['v2.53']['slot_commutator_fro'],2.8)
 def test_254(self):self.assertAlmostEqual(self.r['v2.54']['P_X_plus_00'],(1+math.sin(.8))/2)
 def test_255(self):self.assertLess(self.r['v2.55']['mixture_ensemble_gap'],1e-12)
 def test_256(self):self.assertLess(self.r['v2.56']['coherent_vs_incoherent_probe_trace_distance'],1e-12)
 def test_257(self):self.assertAlmostEqual(self.r['v2.57']['discriminating_gap'],(1-math.cos(.8))/2)
 def test_258(self):self.assertEqual(self.r['v2.58']['fisher_rank'],1)
 def test_259(self):self.assertEqual(self.r['v2.59']['X_plus_counts_00'],858);self.assertEqual(self.r['v2.59']['X_plus_counts_11'],153)
 def test_260(self):self.assertGreater(self.r['v2.60']['coupling_vs_free_probe_commutator_fro'],0)
 def test_261(self):self.assertFalse(self.r['v2.61']['novel_permanent_identity_observable'])
if __name__=='__main__':unittest.main()
