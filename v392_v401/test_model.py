import unittest
from v392_v401.model import run
class TenTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=run()
 def test_392(self):self.assertEqual(self.x['training_counts'],[2340,3803,3315,4148,477])
 def test_393(self):self.assertEqual(len(self.x['holdout_counts']),4)
 def test_394(self):self.assertGreater(max(abs(x) for x in self.x['naive_z']),2.5)
 def test_395(self):self.assertTrue(all(0<=x<=1 for x in self.x['bonferroni_p']))
 def test_396(self):self.assertEqual(len(self.x['naive_p']),4)
 def test_397(self):self.assertLess(max(abs(x) for x in self.x['fisher_adjusted_z']),2.5)
 def test_398(self):self.assertEqual(self.x['bootstrap_n'],100)
 def test_399(self):self.assertTrue(0<=self.x['bootstrap_exceedance']<=1)
 def test_400(self):self.assertEqual(self.x['standard_profile_KL'],0)
 def test_401(self):self.assertFalse(self.x['identity_unique'])
if __name__=='__main__':unittest.main()
