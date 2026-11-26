import unittest
import numpy as np
from scipy.integrate import quad
from .model import run,prob,amplitudes

class Interventions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_kick(self):
        x,y=.25,.65
        state=np.sqrt([1-x,x]); read=np.sqrt([1-y,y])
        for phi in [.2,1.3,2.8]:
            self.assertAlmostEqual(abs(read@(state*np.exp([0,1j*phi])))**2,prob(x,y,phi))

    def test_reciprocal(self):
        for x in self.r['reciprocal']['roots']:self.assertAlmostEqual(prob(x,x,np.pi),.36)
    def test_swap(self):
        self.assertAlmostEqual(prob(.25,.65,.73,.32),prob(.65,.25,.73,.32))
    def test_block(self):
        self.assertAlmostEqual(self.r['blocked_reference']['estimated_x'],.25)
    def test_complementarity(self):
        self.assertAlmostEqual(self.r['distinguishability']['quadratic_sum'],1)
    def test_eraser(self):
        self.assertAlmostEqual(self.r['eraser']['unconditional'],prob(.25,.65,.4,gamma=0))
    def test_slope(self):
        a,b=amplitudes(.25,.65);delta=1e-6
        slope=np.angle((a+b*np.exp(1j*(np.pi+delta)))/(a-b))/delta
        self.assertAlmostEqual(slope,self.r['conditional_phase']['slope'],places=8)
    def test_echo(self):
        expected=quad(lambda z:np.exp(-z*z/2)*np.cos(1.6*z)/np.sqrt(2*np.pi),-10,10)[0]
        self.assertAlmostEqual(expected,self.r['echo']['free'])
    def test_common(self):
        d=self.r['crosstalk'];self.assertAlmostEqual(d['peak'],d['minimum_common'])
        self.assertGreater(d['peak']-d['relative'],.1)
    def test_calibration(self):
        # Fringe coefficient calibrates the product of marker overlap and phase contrast.
        for p in [0.,.3,1.7,np.pi]:
            self.assertAlmostEqual(prob(.25,.65,p,gamma=.54),prob(.25,.65,p,gamma=.9*.6))
