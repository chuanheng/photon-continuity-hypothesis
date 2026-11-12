import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from three_state_survival import survival_populations,forbidden_channel_population,energy_bookkeeping

class ThreeStateTests(unittest.TestCase):
    def test_initial(self):
        self.assertEqual(survival_populations(1,0,0),(1.,0.,0.))
    def test_full_transfer_to_low_mode(self):
        high,low,vac=survival_populations(1,0,math.pi/2)
        self.assertAlmostEqual(high,0,places=14)
        self.assertAlmostEqual(low,1,places=14)
        self.assertEqual(vac,0)
    def test_normalization(self):
        for d in (0,.1,3):
            for t in (0,.1,1,10):
                self.assertAlmostEqual(sum(survival_populations(1,d,t)),1)
    def test_detuned_incomplete(self):
        self.assertAlmostEqual(survival_populations(1,2,math.pi/(2*math.sqrt(2)))[1],.5)
    def test_standard_absorption_contrast(self):
        self.assertAlmostEqual(forbidden_channel_population(1,math.pi/2),1)
    def test_energy_matching(self):
        self.assertAlmostEqual(energy_bookkeeping(60,.001,59.999),0,places=10)
    def test_invalid(self):
        with self.assertRaises(ValueError): survival_populations(-1,0,1)
        with self.assertRaises(ValueError): energy_bookkeeping(60,0,59)

if __name__=="__main__": unittest.main()
