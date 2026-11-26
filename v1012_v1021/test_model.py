import unittest
import numpy as np
from scipy.integrate import quad
from scipy.stats import poisson
from .model import gains,mixed,run

class DoubleSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_joint_kernel(self):
        n=np.arange(22)
        Y=.002+.5*np.outer(1-.4**n,1-.6**n)
        self.assertAlmostEqual(poisson.pmf(n,.35)@Y@poisson.pmf(n,.08),gains([(.35,.08)])[0])

    def test_alias(self):
        a,b=.35,.08
        actual=poisson.pmf(1,a)*poisson.pmf(1,b)-poisson.pmf(0,a)*poisson.pmf(2,b)-poisson.pmf(2,a)*poisson.pmf(0,b)
        self.assertAlmostEqual(actual*.1,self.r['diagonal_alias']['off_axis'])

    def test_vacuum(self):
        self.assertTrue(mixed(.08)>mixed(.04)>.122)
        self.assertLess(mixed(.08)-.122,self.r['vacuum_rails']['remainder'])

    def test_extrap(self):
        z=self.r['extrapolation']
        self.assertTrue(z['lower']<.122<z['upper'])
        self.assertLess(z['upper']-z['lower'],.002)

    def test_crossed(self):
        z=self.r['rectangular_scan'];lo,hi=z['rich']
        self.assertTrue(lo<.122<hi and hi-lo<.0003)
        self.assertEqual(z['diagonal'][0],0)

    def test_uncertainty(self):
        lo,hi=self.r['joint_error'];self.assertTrue(lo<.112 and hi>.135)

    def test_pump(self):
        z=self.r['shared_pump'];self.assertGreater(z['shared']-z['independent'],.007)

    def test_phase(self):
        click=quad(lambda x:-np.expm1(-.35*(1-np.cos(x))),0,2*np.pi)[0]/(2*np.pi)
        self.assertAlmostEqual(click,self.r['phase_lock']['independent'])

    def test_gauge(self):
        for x in [.1,.4,1]:
            self.assertAlmostEqual(np.exp(-.8*.6*x),np.exp(-.96*.5*x))
        self.assertAlmostEqual(np.diff(self.r['attenuation_gauge']['one_photon_yields'])[0],-.02)

    def test_score(self):
        z=self.r['signed_joint'];self.assertTrue(z['truth']<=z['upper']<0)
