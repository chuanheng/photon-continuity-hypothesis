import unittest
from scipy.stats import binom
from .model import run

class Bounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run()

    def test_v902(self):
        self.assertAlmostEqual(self.result['classical'], 0.75, delta=1e-12)

    def test_v903(self):
        self.assertAlmostEqual(self.result['qubit'], 0.8535533905932737, delta=1e-12)

    def test_v904(self):
        self.assertAlmostEqual(self.result['biased_classical'], 0.9, delta=1e-12)

    def test_v905(self):
        self.assertAlmostEqual(self.result['tilted'], 0.8415063509461097, delta=1e-12)

    def test_v906(self):
        self.assertAlmostEqual(self.result['dephase'], 0.7795084971874737, delta=1e-12)

    def test_v907(self):
        self.assertAlmostEqual(self.result['damping'], 0.756124969497314, delta=1e-12)

    def test_v908(self):
        self.assertAlmostEqual(self.result['postselected'], 1, delta=1e-12)

    def test_v909(self):
        self.assertAlmostEqual(self.result['leak_fraction'], 0.41421356237309515, delta=1e-12)

    def test_v910(self):
        k = self.result['critical']
        self.assertGreater(binom.sf(k-2,200,.75), .01)
        self.assertLessEqual(self.result['alpha'], .01)
        self.assertGreater(self.result['power'], .8)

    def test_v911(self):
        self.assertAlmostEqual(self.result['swap_error'], 0, delta=1e-12)
