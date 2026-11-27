import unittest
import numpy as np
from .model import run,branch,V,A
class Loss(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_kl(self):np.testing.assert_allclose((A@V).T@(A@V),2*np.eye(2))
    def test_single(self):np.testing.assert_allclose(self.r['finite_single']['prob'],[2*.2*.8**3,2*.2*.8])
    def test_null(self):self.assertAlmostEqual(-self.r['vacuum_record']['difference'],(1-.8**2)**2/2)
    def test_filter(self):
        b=branch(1,.8);s=min(np.linalg.svd(b,compute_uv=False))
        np.testing.assert_allclose(s*np.linalg.pinv(b)@b,s*np.eye(2))
    def test_odd(self):self.assertAlmostEqual(self.r['odd_alias']['three_fraction'],.0064/self.r['odd_alias']['prob'])
    def test_false(self):self.assertLess(self.r['wrong_flag']['single_fraction'],1-self.r['odd_alias']['three_fraction'])
    def test_two(self):self.assertGreater(self.r['double_jump']['overlap_with_code'],.1)
    def test_bath(self):
        p=np.array([np.diag(branch(k,.8).T@branch(k,.8)) for k in range(5)])
        np.testing.assert_allclose(p.sum(axis=0),1);self.assertAlmostEqual(max(np.where(p[:,0]>p[:,1],p[:,0]-p[:,1],0).sum(),0),self.r['emitted_info']['count_tv'])
    def test_time(self):
        from scipy.integrate import quad
        self.assertAlmostEqual(quad(lambda t:np.cos(1.4*(t-.4)),0,.8)[0]/.8,self.r['timing']['unknown_visibility'])
    def test_energy(self):
        W=A@V/np.sqrt(2);np.testing.assert_allclose(np.diag(W.T@np.diag(np.arange(5))@W),[3,1])
