import unittest,numpy as np
from v372_v381.model import TRUE,probs,fit,nll,run
class TenTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.x=run()
 def test_372(self):self.assertEqual(len(probs(TRUE)),5)
 def test_373(self):self.assertEqual(self.x['counts'],[2340,3803,3315,4148,477])
 def test_374(self):self.assertLessEqual(nll(fit(np.array([2385,3754,3376,4085,527]))[1],np.array([2385,3754,3376,4085,527])),nll(TRUE,np.array([2385,3754,3376,4085,527]))+1e-4)
 def test_375(self):self.assertEqual(len(self.x['profile_grid']),18)
 def test_376(self):self.assertEqual(self.x['LR_simulations'],30)
 def test_377(self):self.assertLessEqual(self.x['LR_fraction_above_3_841'],1)
 def test_378(self):self.assertEqual(len(self.x['mle']),5)
 def test_379(self):self.assertTrue(np.all(np.isfinite(probs(TRUE))))
 def test_380(self):self.assertEqual(self.x['standard_model_profile_KL'],0)
 def test_381(self):self.assertFalse(self.x['identity_unique_prediction'])
if __name__=='__main__':unittest.main()
