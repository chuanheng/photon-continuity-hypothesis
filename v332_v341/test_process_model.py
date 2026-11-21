"""Ten tests for v3.32-v3.41, all synthetic."""
import unittest
from .process_model import run
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=run()
 def test_332(self):self.assertAlmostEqual(self.x['v3.32']['single_p1'],.26)
 def test_333(self):self.assertAlmostEqual(sum(self.x['v3.33']['shared']),1)
 def test_334(self):self.assertAlmostEqual(self.x['v3.34']['fresh_disagree'],.3848)
 def test_335(self):self.assertEqual(self.x['v3.35']['profile_KL'],0)
 def test_336(self):self.assertGreater(self.x['v3.36']['KL_wrong_fresh_baseline'],.03)
 def test_337(self):self.assertEqual(self.x['v3.37']['counts'],[6000,1451,1376,1173])
 def test_338(self):self.assertGreater(self.x['v3.38']['shift'],.01)
 def test_339(self):self.assertAlmostEqual(self.x['v3.39']['fresh_reference'][3],.0676)
 def test_340(self):self.assertAlmostEqual(self.x['v3.40']['normalization'],1)
 def test_341(self):self.assertFalse(self.x['v3.41']['unique_photon_identity_prediction'])
if __name__=='__main__':unittest.main()
