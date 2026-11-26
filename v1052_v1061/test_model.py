import unittest
import numpy as np
from .model import run

class Spectator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_alias(self):
        self.assertEqual(*self.r['alias']['clicks'])
        self.assertNotEqual(*self.r['alias']['occupancies'])

    def test_spectral(self):
        z=self.r['spectral']
        for l,h in zip(z['individual_lower'],z['individual_upper']):self.assertTrue(l<=.65<=h)

    def test_joint(self):
        z=self.r['joint'];lo,hi=z['interval'];l,h=z['intersection']
        self.assertTrue(l<lo<hi<h)
        for x in [lo,hi]:
            u=(np.array(self.r['spectral']['measured'])-x*np.array([.65,.60])-(1-x)*.32)/((1-x)*.18)
            self.assertAlmostEqual(u@u,1)

    def test_pulse(self):
        self.assertAlmostEqual(self.r['angle_error']['worst_population_bias'],.08*np.sin(.06)/.32)

    def test_weight(self):
        self.assertAlmostEqual(.53*1+.47*(-1),self.r['unequal_duty']['raw_max_bias']*.32/.08)
