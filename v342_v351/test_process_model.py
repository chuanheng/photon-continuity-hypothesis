"""Ten tests for ten research stages; deterministic synthetic model."""
import unittest
from v342_v351.process_model import run
class TenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_v342(self):self.assertAlmostEqual(self.r['v3.42']['p_one'],.311)
 def test_v343(self):self.assertGreater(self.r['v3.43']['reset_m_effect'],.14)
 def test_v344(self):self.assertLess(self.r['v3.44']['both_reset_independent_gap'],1e-12)
 def test_v345(self):self.assertEqual(self.r['v3.45']['one_setting_rank'],1);self.assertEqual(self.r['v3.45']['three_settings_rank'],2)
 def test_v346(self):self.assertEqual(self.r['v3.46']['counts']['baseline'],[5704,1236,1186,1874])
 def test_v347(self):self.assertLess(self.r['v3.47']['imperfect_reset_m'],self.r['v3.47']['ideal_reset_m'])
 def test_v348(self):self.assertFalse(self.r['v3.48']['photon_individuality_identified'])
 def test_v349(self):self.assertEqual(self.r['v3.49']['profiled_KL'],0)
 def test_v350(self):self.assertAlmostEqual(self.r['v3.50']['norm'],1);self.assertLess(self.r['v3.50']['two_time_marginal_gap'],1e-12)
 def test_v351(self):self.assertFalse(self.r['v3.51']['unique_photon_identity_prediction'])
if __name__=='__main__':unittest.main()
