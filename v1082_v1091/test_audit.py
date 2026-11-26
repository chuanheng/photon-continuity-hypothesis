import unittest
import numpy as np
from .audit import run
from .model import bell_pt
class JointNoise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_joint(self):
        p=self.r['profile'];self.assertLess(p['pt_range'][0],0);self.assertGreater(p['pt_range'][1],0)
        for x in p['examples']:np.testing.assert_allclose(np.sum(x,axis=0),.25);np.testing.assert_allclose(np.sum(x,axis=1),.25)
    def test_flag(self):
        z=self.r['flag'];self.assertLess(z['true_pt'],0);self.assertGreater(z['read_pt'],0);self.assertLess(z['false_plus_threshold'],.14)
    def test_drift(self):
        z=self.r['drift'];self.assertGreater(z['block_min'][0],0);self.assertLess(z['block_min'][1],0);self.assertGreater(z['herald_weight'],.5)
    def test_margin(self):self.assertAlmostEqual(self.r['audit_margin']['robust_slack'],.006875)
    def test_heldout(self):self.assertLess(self.r['heldout']['max_error'],1e-14)
