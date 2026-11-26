import unittest
import numpy as np
from scipy.integrate import quad
from .model import run

class Monitoring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_click(self):self.assertAlmostEqual(self.r['external_click']['recovered'],.25)
    def test_uncertainty(self):
        lo,hi=self.r['calibration_interval'];self.assertTrue(lo<.25<hi)
    def test_tight(self):
        q=self.r['coherent_leak']['p']
        for x in self.r['coherent_leak']['range']:
            self.assertAlmostEqual(abs(q-.04-.32*x),.16*np.sqrt(x*(1-x)))
    def test_phase(self):self.assertAlmostEqual(self.r['phase_cycle']['inferred'],.25)
    def test_return(self):self.assertAlmostEqual(self.r['environment_return']['recorded'],.52)
    def test_missed(self):
        z=self.r['null_backaction'];self.assertLess(z['missed_monitor_material'],z['ideal_no_jump'])
    def test_taps(self):self.assertAlmostEqual(self.r['two_taps']['extraction'],.4)
    def test_zeno(self):
        v=self.r['zeno'];self.assertTrue(all(np.diff(v)>0));self.assertAlmostEqual(v[1],.25)
    def test_residence(self):
        z=self.r['residence'];self.assertAlmostEqual(z['derivative'],quad(lambda t:np.sin(t)**2,0,1.4)[0],places=8)
    def test_records(self):
        z=self.r['hidden_records'];self.assertAlmostEqual(z['sum'],1);self.assertLess(z['max_error'],1e-14)
