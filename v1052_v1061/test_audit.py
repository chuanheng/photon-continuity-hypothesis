import unittest
import numpy as np
from .audit import run

class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_rotation(self):
        np.testing.assert_allclose(self.r['mixing']['bias'],[-np.sin(.16)/2,np.sin(.16)/2])

    def test_angle(self):
        lo,hi=self.r['axis_interval']
        for x in (lo,hi):self.assertAlmostEqual(abs(np.arccos(np.sqrt(x))-np.arccos(np.sqrt(.62))),.08)

    def test_holdout(self):
        d=self.r['third_effect'];x=d['center_occupation']
        v=np.array(self.r['prefix']['spectral']['measured'])-.32-x*np.array([.33,.28])
        for y in d['range']:
            self.assertAlmostEqual((v@v+(y-.32)**2)/(.18*(1-x))**2,1)

    def test_schedule(self):
        self.assertGreater(self.r['schedule']['blocked_norm'],1)
        self.assertLess(self.r['schedule']['blind_norm'],1)

    def test_refit(self):
        d=self.r['conditional_probe']
        self.assertGreater(d['largest_deviation'],.4)
        self.assertLess(d['max_error'],1e-14)
