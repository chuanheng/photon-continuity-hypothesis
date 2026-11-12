import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from photoionization_threshold import ionization_threshold,max_successor_energy,successor_is_kinematically_allowed

class ThresholdTests(unittest.TestCase):
    M=10_000_000.0
    I=0.0136 # keV
    ion=9_999_489.0146
    electron=510.999
    def test_standard_threshold_recoil(self):
        t=ionization_threshold(self.M,self.ion,self.electron)
        self.assertGreater(t,(self.ion+self.electron)-self.M)
    def test_successor_adds_energy(self):
        t=ionization_threshold(self.M,self.ion,self.electron)
        self.assertAlmostEqual(ionization_threshold(self.M,self.ion,self.electron,.001)-t,.001)
    def test_threshold_closed(self):
        self.assertFalse(successor_is_kinematically_allowed(.01,self.M,self.ion,self.electron,.001))
    def test_threshold_open(self):
        self.assertTrue(successor_is_kinematically_allowed(.02,self.M,self.ion,self.electron,.001))
    def test_zero_successor_not_strict(self):
        self.assertFalse(successor_is_kinematically_allowed(.02,self.M,self.ion,self.electron,0))
    def test_max_residual(self):
        self.assertAlmostEqual(max_successor_energy(.02,self.M,self.ion,self.electron),.02-ionization_threshold(self.M,self.ion,self.electron))
    def test_bad_mass(self):
        with self.assertRaises(ValueError): ionization_threshold(-1,1,1)
    def test_exothermic_rejected(self):
        with self.assertRaises(ValueError): ionization_threshold(100,50,1)
    def test_bad_successor(self):
        with self.assertRaises(ValueError): ionization_threshold(100,100,1,-.01)
    def test_nonfinite(self):
        with self.assertRaises(ValueError): ionization_threshold(float('nan'),100,1)

if __name__=='__main__': unittest.main()
