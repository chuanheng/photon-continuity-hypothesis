import unittest
import numpy as np
from .correlation import TARGET,observed_flags,run
from .model import mix

class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_joint(self):
        q=self.r['joint_crossing']['q']
        self.assertAlmostEqual(mix(self.r['prefix']['independent']['sectors'],.03,q),TARGET)
        self.assertTrue(.0009<q<.03)
        self.assertTrue(.09<self.r['joint_crossing']['necessary_pearson']<self.r['joint_crossing']['pearson'])

    def test_rate(self):
        e=self.r['independent_feasible_rate']
        a=(2-np.sqrt(12))/8
        self.assertAlmostEqual(2*a*e*(1-e)-.5*e**2,TARGET)

    def test_history(self):
        self.assertAlmostEqual(self.r['history_score'],-.015)
        self.assertLess(self.r['history_score'],TARGET)

    def test_monitor(self):
        q=self.r['joint_crossing']['q']
        self.assertAlmostEqual(self.r['monitor']['recovered_joint'],q)
        self.assertAlmostEqual(observed_flags(.03,q,.8,.002).sum(),1)

    def test_trials(self):
        d=self.r['finite_trials'];step=2*d['margin']**2/144
        self.assertTrue((d['N']-1)*step<np.log(20)<=d['N']*step)

    def test_material(self):
        self.assertLess(self.r['heldout']['test_input_error'],1e-14)
        self.assertLess(self.r['heldout']['max_table_error'],1e-14)
