import unittest
import numpy as np
from .selection import axes,paired,run,selected

class SelectionAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_outcomes(self):
        # Isotropized X/Y/Z measure-prepare: favourable mass 2/3.
        h=.093
        good,bad=8*3*h/17,3*h/17
        self.assertAlmostEqual((2*good+bad)/3,h)
        self.assertAlmostEqual((1+3*selected(good,bad,1/3))/4,31/34)

    def test_one_arm(self):
        r=np.ones(3)/np.sqrt(3)
        self.assertAlmostEqual((1+r.sum())/4,self.r['single_arm'])
        self.assertLessEqual(abs(r.sum()),np.sqrt(3)+1e-14)

    def test_timing(self):
        self.assertGreater(paired(.5),.999)
        self.assertAlmostEqual(paired(6),.25,places=8)

    def test_early(self):
        h=.093
        self.assertAlmostEqual((.02+(h-.02)/2)/h,self.r['apparent_early'])

    def test_axes(self):
        u,s,v=np.linalg.svd(axes(np.pi/12))
        self.assertAlmostEqual(u[:,0]@axes(np.pi/12)@v[0],np.sqrt(1+np.sin(np.pi/12)))

    def test_source(self):
        for u,v in [(.8,.75),(.6,1)]:
            rho=np.diag([(1+3*u)/4]+[(1-u)/4]*3)
            self.assertAlmostEqual((v*rho+(1-v)*np.eye(4)/4)[0,0],.7)

    def test_bypass(self):
        self.assertAlmostEqual(self.r['bypass']['bell_return'],1)
        self.assertEqual(self.r['bypass']['stored_signal_excited'],0)

    def test_unconditional(self):
        # A separable isotropic source can keep just agreeing outcomes.
        self.assertAlmostEqual((1+1/3)/2,self.r['all_trials']['min_efficiency'])
        self.assertGreater(3*(2*.67-1),1)
