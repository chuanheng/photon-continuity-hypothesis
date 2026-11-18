import unittest
import numpy as np
from models.identity_label_hom_v242_v251 import run,hom
class TenTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_v242(self):self.assertAlmostEqual(self.r['v2.42']['joint_overlap'],.5184)
 def test_v243(self):self.assertLess(self.r['v2.43']['amplitude_gap'],1e-12)
 def test_v244(self):self.assertLess(self.r['v2.44']['operational_gap'],1e-12)
 def test_v245(self):self.assertLess(abs(self.r['v2.45']['single_setting_fisher_eigenvalues'][0]),1e-9)
 def test_v246(self):self.assertEqual(self.r['v2.46']['profiled_KL'],0)
 def test_v247(self):self.assertGreater(self.r['v2.47']['joint_fisher_determinant'],0)
 def test_v248(self):self.assertAlmostEqual(self.r['v2.48']['label_projector_outcome_if_accessible'],.64)
 def test_v249(self):self.assertAlmostEqual(self.r['v2.49']['slot_swap_commutator_norm'],2*np.sqrt(2))
 def test_v250(self):self.assertEqual(self.r['v2.50']['observed_coincidences'],2403)
 def test_v251(self):self.assertFalse(self.r['v2.51']['novel_photon_identity_prediction'])
if __name__=='__main__':unittest.main()
