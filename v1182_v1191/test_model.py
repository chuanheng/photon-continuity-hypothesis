import unittest
import numpy as np
from scipy.stats import binom
from .model import run


class ReferenceTests(unittest.TestCase):
    def test_passive_preparation(self):
        np.testing.assert_allclose(run()['reachable'],((1+np.array([1,-1])*np.sin(.66))/2)**2)

    def test_relative_twirl(self):
        relative,common=run()['twirls']
        self.assertAlmostEqual(relative,(1+np.sin(.66)**2/2)/4)
        self.assertAlmostEqual(common,run()['reachable'][0])

    def test_spectral_overlap(self):
        a,b=run()['orthogonal_ports']
        self.assertAlmostEqual(a,b)
        self.assertAlmostEqual(a,1.49*np.cos(.66)**2/4)

    def test_exact_tail(self):
        r=run()['count_test']; hi,lo=run()['reachable']
        self.assertLessEqual(r['worst_false_positive'],.01)
        self.assertGreater(binom.sf(r['threshold']-2,r['n'],lo+.05),.01)
        self.assertGreater(r['minimum_power'],.99)
