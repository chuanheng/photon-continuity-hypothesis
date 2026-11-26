import unittest
import numpy as np
from numpy.testing import assert_allclose
from scipy.stats import poisson
from .model import PHASE, discrete, finite, jitter, overlap, receiver, run

class Physics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=run()

    def test_phase_projection(self):
        g=overlap()
        for k in (1,2,4):
            roots=np.exp(2j*np.pi*np.arange(k)/k)
            blocks=[sum(np.exp(root*g-1)*root**(-s) for root in roots)/k for s in range(k)]
            self.assertAlmostEqual(discrete(k),sum(min(np.linalg.eigvalsh(b)) for b in blocks))

    def test_joint_sector(self):
        g=overlap()
        n=4
        from math import comb
        assert_allclose(((2+g)/3)**n,sum(comb(n,j)*2**(n-j)*g**j for j in range(n+1))/3**n,atol=1e-14)
        self.assertLess(abs(finite(2)-finite(2,cutoff=60)),1e-13)

    def test_common_phase(self):
        self.assertAlmostEqual(finite(2),finite(2,phases=PHASE+1.73))
        self.assertAlmostEqual(finite(0),discrete(25))

    def test_jitter(self):
        from scipy.integrate import quad_vec
        t=quad_vec(lambda x:np.exp(-x*x/2)/np.sqrt(2*np.pi)*receiver(.2*x),-10,10)[0]
        self.assertAlmostEqual((t*abs(overlap())**2).sum()/t.sum(),jitter(.2)['fidelity'])

    def test_plates(self):
        assert_allclose(self.r['plate_ray_fidelity'],1,atol=1e-14)
        self.assertLess(self.r['plate_usd'],.093)

    def test_mode_filter(self):
        x=self.r['mode_match_required']
        self.assertLess(finite(2*(x-.001)),.093)
        self.assertGreater(finite(2*(x+.001)),.093)

    def test_signal_loss(self):
        self.assertAlmostEqual(finite(2,self.r['signal_transmission_required']),.093)

    def test_accidentals(self):
        b=self.r['false_herald_fraction']
        self.assertAlmostEqual((((1-b)*np.eye(6)+b/6)*abs(overlap())**2).sum()/6,.93)

    def test_phase_witness(self):
        c,g,b=self.r['matched_first_harmonic']
        self.assertAlmostEqual(np.cos(2*np.arccos(c)),b)
        self.assertGreater(abs(g-b),.02)

    def test_ref_budget(self):
        a,b=self.r['shared_pulse_rates']
        self.assertGreater(a,.093)
        self.assertLess(b,.093)
