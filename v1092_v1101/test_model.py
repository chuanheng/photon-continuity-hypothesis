import unittest
import numpy as np
from .model import run,damping,I,X,Z,fidelity
class Feedback(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_map(self):
        z=self.r['order_flag'];self.assertAlmostEqual(z['posterior_F'],.375);self.assertAlmostEqual(z['full_tag'],1)
    def test_parity(self):
        self.assertAlmostEqual(self.r['parity_only']['Fe'],fidelity([I/np.sqrt(2),Z/np.sqrt(2)]))
    def test_markers(self):
        a=np.array([1,0]);b=np.array([.6,.8]);D=np.outer(a,a)-np.outer(b,b)
        self.assertAlmostEqual(.5+np.sum(abs(np.linalg.eigvalsh(D)))/4,self.r['imperfect_marker']['optimal_Fe'])
    def test_usd(self):
        self.assertAlmostEqual(self.r['unambiguous']['accepted'],min(np.linalg.eigvalsh([[1,.6],[.6,1]])))
    def test_repeats(self):
        z=self.r['repeat_read'];self.assertAlmostEqual(z['conditional_independent']*z['accepted_independent'],.0225)
    def test_instrument(self):
        self.assertAlmostEqual(self.r['basis_choice']['projective_Fe'],.5)
    def test_damping(self):
        K,J=damping(.36);self.assertAlmostEqual(fidelity([K,X@J]),self.r['nonunital']['best_count_unitary_Fe'])
    def test_reversal(self):
        r=self.r['heralded_inverse'];self.assertAlmostEqual(r['success'],.64);self.assertLess(r['reverse_error'],1e-14)
    def test_missing(self):self.assertAlmostEqual(self.r['missing_tags']['F'],.72+.28/4)
    def test_holdout(self):
        plus=np.ones(2)/np.sqrt(2);p=.24
        self.assertAlmostEqual((1-p)+p*abs(plus@Z@plus)**2,self.r['heldout']['Z_noise_x'])
