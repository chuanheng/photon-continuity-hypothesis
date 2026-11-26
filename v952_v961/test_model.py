import unittest
import numpy as np
from numpy.testing import assert_allclose
from .model import clicks,design,moments,ratio,run

class Photodetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.r=run()

    def test_antibunch(self):
        c=self.r['single_output']
        assert_allclose(c['events'],[1-.093*.5,.093*.3,.093*.2,0],atol=1e-14)
        self.assertTrue(0<c['keep']<1)

    def test_number_ratio(self):
        s=self.r['ratio_vs_g2']
        self.assertAlmostEqual(s['g2'],2*.005/(.093*(1+.01)))
        self.assertLess(s['click_ratio'],s['number_ratio'])

    def test_two_photon_split(self):
        assert_allclose(clicks([0,0,1]),[.25,.39,.24,.12],atol=1e-14)

    def test_indistinguishable(self):
        s=self.r['hbt_null']
        assert_allclose(clicks(s['p']),clicks(s['q']),atol=1e-13)
        self.assertGreater(s['g2_gap'],.001)
        self.assertGreater(min(s['q']),0)

    def test_scan(self):
        A=design([(.3,.2),(.15,.1)])
        self.assertEqual(np.linalg.matrix_rank(A),5)
        self.assertLess(self.r['scan']['reconstruction_error'],1e-10)

    def test_dark(self):
        d=self.r['dark']
        self.assertAlmostEqual(ratio(clicks([.907,.093],dark=d)),.005)

    def test_crosstalk(self):
        c=clicks([.907,.093])
        transfer=c[1]*self.r['crosstalk']
        c[3]+=transfer
        c[1]-=transfer
        self.assertAlmostEqual(ratio(c),.005)

    def test_lag(self):
        x=np.tile([.12,.04],100)
        self.assertAlmostEqual(np.mean(x*np.roll(x,1))/np.mean(x)**2,self.r['lag_normalization'])

    def test_busy(self):
        c=clicks([.86,.12,.02])
        def g(t): return t[3]/((t[1]+t[3])*(t[2]+t[3]))
        self.assertAlmostEqual(g(.8*c+.2*np.array([1,0,0,0]))/g(c),self.r['shared_live_enhancement'])

    def test_wavepacket(self):
        self.assertAlmostEqual(sum(self.r['envelope']['time_prob']),1)
        self.assertAlmostEqual(self.r['envelope']['hom_overlap'],.01)
