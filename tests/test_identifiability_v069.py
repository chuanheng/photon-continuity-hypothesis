import unittest
import numpy as np
from models.identifiability_v069 import visibility,coincidence,kl,fit

class TestIdentifiability(unittest.TestCase):
    def test_zero(self): self.assertAlmostEqual(float(coincidence(0,.7)),0)
    def test_same_law(self): self.assertTrue(np.allclose(coincidence([.2,1],.7),coincidence([.2,1],.7,'exp')))
    def test_kl_zero(self): self.assertAlmostEqual(float(kl(.2,.2)),0)
    def test_fit(self):
        k,stat=fit([.2,.4,.7,1,1.5,2],.7,1000)
        self.assertAlmostEqual(k,.8920229,places=4)
        self.assertAlmostEqual(stat,227.41553,places=3)
    def test_single_setting(self): self.assertAlmostEqual(float(coincidence(1.5,.7)),float(coincidence(1.5,.7/1.5,'gaussian')))
if __name__=='__main__': unittest.main()
