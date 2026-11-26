import unittest
import numpy as np
from scipy.stats import poisson
from .model import analytic,gain,interval,run

class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_source(self):
        n=np.arange(32)
        self.assertAlmostEqual(poisson.pmf(n,.6)@(1-.998*.82**n),gain(.6))

    def test_alias(self):
        self.assertAlmostEqual(poisson.pmf(1,.6)*.04-poisson.pmf(2,.6)*2*.04/.6,0)

    def test_analytic(self):
        for eff in [.01,.18,.8]:
            q=gain([0,.15,.6],eff)
            self.assertLessEqual(analytic(.6,.15,*q),.002+.998*eff)

    def test_tails(self):
        vals=list(self.r['tail_relaxation'].values())
        for lo,hi in vals:self.assertTrue(lo<.18164<hi)
        self.assertGreater(vals[0][1]-vals[0][0],vals[2][1]-vals[2][0])

    def test_design(self):
        lo,hi=self.r['extra_intensity']
        self.assertTrue(lo<.18164<hi and hi-lo<.0002)

    def test_precision(self):
        lo,hi=self.r['noise_budget']
        self.assertTrue(lo<.18 and hi>.19)

    def test_leaked_setting(self):
        self.assertGreater(self.r['setting_leak']['apparent_lower'],.18164+.08)

    def test_drift(self):
        r=self.r['block_drift']
        self.assertLess(r['randomized_lower'],r['pooled_y1'])
        self.assertGreater(r['blocked_lower'],.002+.998*.30)

    def test_phase(self):
        r=self.r['phase_coherence']
        self.assertAlmostEqual(r['locked']-r['randomized'],np.exp(-.15)*np.sqrt(.15))

    def test_signed(self):
        r=self.r['cell_witness']
        self.assertTrue(r['truth']<=r['upper']<0)
