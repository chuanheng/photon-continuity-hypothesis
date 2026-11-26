import unittest
import numpy as np
from .model import B,run

class PrivateFlags(unittest.TestCase):
    def test_sync(self):
        a=np.array([1,1,0,0])
        self.assertAlmostEqual(.03*(a@B@(1-a)),run()['sync']['bound'])

    def test_incompatibility(self):
        r=run()['exclusive']
        self.assertEqual(r['single_optimal_axes'],4)
        self.assertAlmostEqual(r['clean_floor_at_saturation'],1/6)

    def test_independent(self):
        r=run()['independent']
        e=.03
        single=(2-np.sqrt(12))/8
        self.assertAlmostEqual(r['feasible'],2*e*(1-e)*single-.5*e**2)
        self.assertGreater(r['gap_to_relaxation'],0)

    def test_outer_hull(self):
        from .model import bound_independent
        for k in (24,48):
            bracket=bound_independent(0,k)
            self.assertLessEqual(bracket['lower'],0)
            self.assertAlmostEqual(bracket['upper'],0)
        b=bound_independent(.03)
        self.assertLess(b['lower'],b['upper'])
        self.assertGreater(b['lower'],-.011625+1e-6)
