import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from jaynes_cummings import populations,minimum_mode_photon_probability

class JCTests(unittest.TestCase):
    def test_initial(self): self.assertEqual(populations(1,0,0),(1.,0.))
    def test_resonant_full_transfer(self):
        a,b=populations(1,0,math.pi/2)
        self.assertAlmostEqual(a,0,places=14)
        self.assertAlmostEqual(b,1,places=14)
    def test_revival(self):
        a,b=populations(1,0,math.pi)
        self.assertAlmostEqual(a,1)
        self.assertAlmostEqual(b,0)
    def test_normalization(self):
        for d in (0,0.2,3):
            for t in (0,0.5,1,10):
                a,b=populations(1,d,t)
                self.assertAlmostEqual(a+b,1)
                self.assertGreaterEqual(a,-1e-12)
                self.assertGreaterEqual(b,-1e-12)
    def test_detuned_incomplete_transfer(self):
        self.assertAlmostEqual(minimum_mode_photon_probability(1,2),0.5)
    def test_zero_coupling(self): self.assertEqual(populations(0,0,10),(1.,0.))
    def test_bad_input(self):
        with self.assertRaises(ValueError): populations(-1,0,1)
        with self.assertRaises(ValueError): populations(1,float("nan"),1)
if __name__=="__main__": unittest.main()
