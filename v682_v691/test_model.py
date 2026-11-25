import unittest
import numpy as np
from .model import run

class Curves(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = run()
    def test_impulse(self):
        self.assertAlmostEqual(self.r['v6.82'][0]*1e31,1.21433,4)
    def test_born(self):
        self.assertTrue(np.all(np.array(self.r['v6.83'])>self.r['v6.82']))
    def test_first_line(self):
        self.assertGreater(self.r['v6.84'][0],10*self.r['v6.84'][1])
    def test_second_line(self):
        self.assertLess(self.r['v6.85'][0],self.r['v6.85'][1])
    def test_free_scale(self):
        self.assertGreater(self.r['v6.86'][0]['scale'],2)
    def test_bounded_scale(self):
        np.testing.assert_allclose([x['scale'] for x in self.r['v6.87']],[1.09,.91])
    def test_transfer(self):
        self.assertGreater(self.r['v6.88'][0],self.r['v6.85'][0])
    def test_pixels(self):
        a,b=self.r['v6.89'];self.assertGreater(a[0],b[1])
    def test_leave_one_out(self):
        original=np.sum(np.array([self.r['v6.84'],self.r['v6.85']]),axis=0)
        self.assertAlmostEqual(sum(self.r['v6.90']),7*(original[0]-original[1]))
    def test_interpolation(self):
        self.assertGreater(self.r['v6.91']['log_interpolation'],1)
        self.assertLess(self.r['v6.91']['profile_score'],min(x['score'] for x in self.r['v6.86']))
