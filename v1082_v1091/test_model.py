import unittest
import numpy as np
from .model import branches,run,bell_pt,success
class Flags(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_choi(self):
        z=self.r['choi'];np.testing.assert_allclose(z['pt_min'],[.1,1/6],atol=1e-14)
        np.testing.assert_allclose(branches().sum(axis=1),[5/8,3/8])
    def test_success(self):
        self.assertAlmostEqual(self.r['single_use']['with_flag'],.625)
        self.assertAlmostEqual(self.r['single_use']['ignored'],.5)
    def test_flip(self):
        e=self.r['noisy_flag']['error']
        self.assertAlmostEqual(self.r['noisy_flag']['success'],.5+.125*abs(1-2*e))
    def test_root(self):
        v=self.r['noise_boundary']['vcrit'];a=(1+3*v)/4;b=(1-v)/4
        self.assertAlmostEqual(2*(a*a+3*b*b),1-6*b*b)
        self.assertLess(v,np.sqrt(1/3))
    def test_memory(self):
        self.assertAlmostEqual(self.r['shared_boundary']['wcrit'],1/9)
        z=self.r['shared_boundary'];self.assertLess(z['plus_pt'],0);self.assertGreater(z['serial_pt'],0)
