"""Ten stages v1.92-v2.01 regression tests."""
import unittest
from models.identity_synthesis_v192_v201 import run
class TenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_192(self):self.assertEqual(self.r['v1.92']['candidate_count'],8)
 def test_193(self):self.assertEqual(self.r['v1.93']['energy_deficit'],2.)
 def test_194(self):self.assertEqual(self.r['v1.94']['silent_label_KL'],0)
 def test_195(self):self.assertEqual(self.r['v1.95']['unbounded_null']['KL'],0)
 def test_196(self):self.assertGreater(self.r['v1.96']['profile_KL'],0)
 def test_197(self):self.assertLessEqual(self.r['v1.97']['type_I'],.05)
 def test_198(self):self.assertEqual(self.r['v1.98']['drift_scan'][-1]['KL'],0)
 def test_199(self):self.assertLessEqual(self.r['v1.99']['type_I'],.05/3)
 def test_200(self):self.assertEqual(self.r['v2.00']['observed_clicks'],383)
 def test_201(self):self.assertFalse(self.r['v2.01']['unique_photon_identity_prediction'])
if __name__=='__main__':unittest.main()
