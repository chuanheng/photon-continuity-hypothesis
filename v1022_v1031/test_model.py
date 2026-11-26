import unittest
import numpy as np
from numpy.testing import assert_allclose
from scipy.stats import poisson
from .model import run,no_click,invert

class Calibration(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.r=run()

    def test_single(self):self.assertAlmostEqual(self.r['single']['raw'],.48)
    def test_poisson(self):
        n=np.arange(30)
        assert_allclose(poisson.pmf(n,.55)@(.52*.65)**n,no_click(.55,.48,.35,'poisson')[2])
        assert_allclose(self.r['multipair']['corrected'],[.55,.48,.35])
    def test_alias(self):
        self.assertLess(self.r['law_alias']['max_error'],1e-14)
        self.assertGreater(abs(self.r['law_alias']['thermal'][1]-.48),.02)
    def test_holdout(self):self.assertGreater(self.r['power_holdout']['max_gap'],.005)
    def test_blank(self):
        self.assertAlmostEqual(self.r['correlated_blank']['correct'],.48)
        self.assertGreater(abs(self.r['correlated_blank']['factorized']-.48),.005)
    def test_spectrum(self):self.assertAlmostEqual(self.r['mode_bias']['heralded'],.35)
    def test_window(self):
        from scipy.integrate import quad
        self.assertAlmostEqual(self.r['timing'][0],.48*quad(lambda x:np.exp(-x*x/1.28)/(.8*np.sqrt(2*np.pi)),-.5,.5)[0])
    def test_live(self):self.assertAlmostEqual(self.r['live_flags']['independent'],.48*.8*.8/.8)
    def test_plane(self):
        lo,hi=self.r['plane']['eta_interval'];self.assertTrue(lo<.48/.9<hi)
    def test_filters(self):
        assert_allclose(self.r['transfer']['two_filters'],[.3,.8])
        self.assertAlmostEqual(self.r['transfer']['target'],.6)
