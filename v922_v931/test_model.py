import unittest
from scipy.stats import poisson
from .model import run

class SixStates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = run()

    def test_v922(self):
        self.assertAlmostEqual(self.r['single'], 0.6666666666666666, delta=1e-12)

    def test_v923(self):
        self.assertAlmostEqual(self.r['two'], 0.75, delta=1e-12)

    def test_v924(self):
        self.assertAlmostEqual(self.r['isotropy_error'], 0, delta=1e-12)

    def test_v925(self):
        self.assertAlmostEqual(self.r['three'], 0.8333333333333334, delta=1e-12)

    def test_v926(self):
        self.assertAlmostEqual(self.r['povm3'], 0.8333333333333334, delta=1e-12)

    def test_v927(self):
        self.assertAlmostEqual(self.r['axis'], 0.6666666666666666, delta=1e-12)

    def test_v928(self):
        self.assertAlmostEqual(self.r['upper'], .855983611849195)

    def test_v929(self):
        self.assertAlmostEqual(self.r['upper']-self.r['lower'], poisson.sf(3,1)/(.093*6))

    def test_v930(self):
        self.assertGreater(self.r['upper_low'],self.r['upper'])
        self.assertLess(self.r['upper_high'],self.r['upper'])

    def test_v931(self):
        self.assertAlmostEqual(self.r['margin'], .074016388150805)
