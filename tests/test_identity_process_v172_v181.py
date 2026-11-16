"""v1.72-v1.81 checks. python -m unittest discover -s tests -p 'test_identity_process_v172_v181.py' -v"""
import unittest
from models.identity_process_v172_v181 import run
class TestTenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_v172(self):self.assertLess(cls_r(self,'v1.72','kraus_error'),1e-12)
 def test_v173(self):self.assertLess(cls_r(self,'v1.73','four_state_tomography_error'),1e-12)
 def test_v174(self):self.assertGreaterEqual(min(cls_r(self,'v1.74','choi_eigenvalues')),-1e-12)
 def test_v175(self):self.assertEqual(cls_r(self,'v1.75','hidden_vs_classical_KL'),0)
 def test_v176(self):self.assertGreater(abs(cls_r(self,'v1.76','static_Xplus')-cls_r(self,'v1.76','reset_Xplus')),.15)
 def test_v177(self):self.assertAlmostEqual(cls_r(self,'v1.77','echo_static_Xplus'),1,places=12)
 def test_v178(self):self.assertLess(cls_r(self,'v1.78','four_intervention_classical_gap'),1e-12)
 def test_v179(self):self.assertEqual(cls_r(self,'v1.79','count_static'),694)
 def test_v180(self):self.assertEqual(cls_r(self,'v1.80','standard_static_environment_profiled_KL'),0)
 def test_v181(self):self.assertFalse(cls_r(self,'v1.81','permanent_identity_specific_prediction'))
def cls_r(obj,section,key):return obj.r[section][key]
if __name__=='__main__':unittest.main()
