import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from identifiability_scan import information,amplitude_for_local_snr

class Tests(unittest.TestCase):
    def test_prior_increases_information(self):
        self.assertLess(information(fractional_prior=None),information(fractional_prior=.1))
        self.assertLess(information(fractional_prior=.1),information(fractional_prior=.01))
    def test_proportional_unidentifiable(self):
        self.assertAlmostEqual(information((10.,20.,30.),(1/6,1/3,1/2)),0.,places=12)
    def test_proportional_prior_breaks_degeneracy(self):
        self.assertGreater(information((10.,20.,30.),(1/6,1/3,1/2),.05),0)
    def test_invalid(self):
        with self.assertRaises(ValueError): information(fractional_prior=0)
    def test_finite_proxy(self):
        self.assertTrue(math.isfinite(amplitude_for_local_snr(3,.03)))

if __name__=="__main__": unittest.main()
