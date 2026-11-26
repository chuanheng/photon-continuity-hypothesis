import unittest
import numpy as np
from .model import run,pair_table,Z,SIGNS,M
class Times(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_lg(self):
        self.assertAlmostEqual(self.r['leggett']['K'],1.5)
        self.assertEqual(max(np.array([1,1,-1])@M),1)
    def test_insert(self):
        self.assertAlmostEqual(Z.diagonal()@np.array(self.r['insertion']['with_meter'])@Z.diagonal(),.25)
    def test_nsit(self):
        self.assertLess(self.r['nsit']['single_max'],1e-14)
        self.assertAlmostEqual(self.r['nsit']['pair_tv'],.375)
    def test_signed_mass(self):
        self.assertAlmostEqual(self.r['signed_mass'],.125)
    def test_noise(self):
        v=self.r['phase_noise']['threshold']
        self.assertAlmostEqual(2*v*np.cos(np.pi/3)-v*v*np.cos(2*np.pi/3),1)
    def test_unsharp(self):self.assertAlmostEqual(self.r['unsharp']['pair'],.8**2/2)
    def test_offset(self):self.assertAlmostEqual(self.r['asymmetric']['measured'],.07**2+.8**2/2)
    def test_selection(self):
        np.testing.assert_allclose(self.r['selection']['acceptance'],8/9)
        self.assertAlmostEqual((2/3)/(8/9),.75)
    def test_classical_meter(self):
        for k,A in enumerate(self.r['classical_meter'],1):
            np.testing.assert_allclose(A,(1+np.outer([1,-1],[1,-1])*np.cos(k*np.pi/3))/2)
    def test_invasiveness(self):
        f=self.r['invasive_fraction'];self.assertAlmostEqual((1-f)/3+f,.5)
