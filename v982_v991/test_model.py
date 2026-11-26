import unittest
import numpy as np
from .model import B,T,MASKS,copies,run,single,unambiguous

class Leakage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_rectangle(self):
        self.assertEqual(min((6*(a@b)-a.sum()*b.sum())/8 for a in MASKS for b in MASKS),-.5)

    def test_one_station(self):
        # For a mask with k entries the summed qubit operator is
        # (k I + 3 sum(n_i).sigma)/8.
        vals=[]
        for a in MASKS:
            k=sum(a);norm=np.linalg.norm(a@T)
            vals.append(min(0,(k-3*norm)/8)+min(0,(k+3*norm)/8))
        self.assertAlmostEqual(min(vals),single())

    def test_flag_correlation(self):
        for value in self.r['correlated'].values():self.assertAlmostEqual(value,-.015)

    def test_local_marginals(self):
        a=np.array([0,0,1,1]);d=1-a
        np.testing.assert_allclose((a+1-a)/2,.5)
        self.assertEqual(np.sum(B*(np.outer(a,d)+np.outer(d,a))/2),-.5)

    def test_two_copies(self):
        self.assertAlmostEqual(copies(2),-1/6)
        self.assertLess(copies(3),copies(2))
        self.assertAlmostEqual(unambiguous(2),0)

    def test_unambiguous(self):
        self.assertAlmostEqual(unambiguous(3),2/3)
        self.assertAlmostEqual(unambiguous(4),8/9)

    def test_nonuniform(self):
        self.assertAlmostEqual(self.r['unequal']['score'],-.03/4)

    def test_trace_budget(self):
        # A joint event can change by at most sum of local preparation distances.
        self.assertAlmostEqual(np.sum(abs(B))*.003,self.r['distance_budget'])
        self.assertGreater(self.r['distance_budget'],.011625)

    def test_zero_counts(self):
        q=self.r['pilot_zero']
        self.assertAlmostEqual((1-q)**1000,.05)

    def test_martingale(self):
        n=self.r['adaptive']['trials']
        delta=.011625
        self.assertTrue(np.exp(-2*n*delta**2/144)<=.05<np.exp(-2*(n-1)*delta**2/144))
