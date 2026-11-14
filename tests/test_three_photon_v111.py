"""Tests for v1.11: python -m unittest discover -s tests -p 'test_three_photon_v111.py' -v"""
import unittest
import numpy as np
from models.three_photon_v111 import (THETA,distribution,main_info,ref_info,
    eta_info,eps_info,metrics,allocations,BASE)
class V111Tests(unittest.TestCase):
    def test_probabilities(self):
        p=distribution(THETA)
        self.assertEqual(len(p),20)
        self.assertTrue(np.all(p>0))
        self.assertAlmostEqual(p.sum(),1,places=11)
    def test_joint_fisher_psd(self):
        for matrix in [main_info(),ref_info(),eta_info(),eps_info()]:
            self.assertTrue(np.allclose(matrix,matrix.T,atol=1e-9))
            self.assertGreater(np.linalg.eigvalsh(matrix).min(),-1e-8)
        self.assertEqual(np.linalg.matrix_rank(main_info(),tol=1e-8),6)
    def test_finite_baseline(self):
        self.assertAlmostEqual(metrics(BASE)['sd_phi'],.33409740738,places=7)
    def test_more_information_improves(self):
        baseline=metrics(BASE)['sd_phi']
        for inc in [(10000,0,0,0),(0,10000,0,0),(0,0,10000,0),(0,0,0,10000)]:
            alloc=tuple(a+b for a,b in zip(BASE,inc))
            self.assertLess(metrics(alloc)['sd_phi'],baseline)
    def test_best_1000_step_grid(self):
        arr=allocations(10000,BASE,1000)
        self.assertEqual(len(arr),286)
        self.assertEqual(min(arr,key=lambda t:t[1]['sd_phi'])[0],(10000,0,0,0))
    def test_calibration_information_sparsity(self):
        self.assertEqual(np.count_nonzero(ref_info()),1)
        self.assertEqual(np.count_nonzero(eta_info()),3)
        self.assertEqual(np.count_nonzero(eps_info()),1)
if __name__=='__main__':unittest.main()
