import math
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'models'))
from absorption_reemission import populations, field_number_expectation, excitation_expectation, survival_amplitude, return_fidelity

class AbsorptionReemissionTests(unittest.TestCase):
    def test_initial(self): self.assertEqual(populations(1, 0), (1, 0))
    def test_full_absorption(self):
        p = populations(2, math.pi/4)
        self.assertAlmostEqual(p[0], 0, places=14)
        self.assertAlmostEqual(p[1], 1, places=14)
    def test_revival(self):
        p = populations(2, math.pi/2)
        self.assertAlmostEqual(p[0], 1, places=14)
        self.assertAlmostEqual(p[1], 0, places=14)
    def test_normalization(self):
        for g in (0, .2, 1, 3):
            for t in (0, .1, 1, 3, 10):
                self.assertAlmostEqual(sum(populations(g,t)), 1)
    def test_excitation_conservation(self):
        for t in (0, .2, .7, 2): self.assertAlmostEqual(excitation_expectation(1,t), 1)
    def test_field_number_changes(self):
        self.assertAlmostEqual(field_number_expectation(1, math.pi/2), 0, places=14)
    def test_fidelity_initial(self): self.assertEqual(return_fidelity(1,0),1)
    def test_fidelity_absorbed(self): self.assertAlmostEqual(return_fidelity(1,math.pi/2),0,places=14)
    def test_amplitude_sign(self): self.assertAlmostEqual(survival_amplitude(1,math.pi),-1)
    def test_no_coupling(self): self.assertEqual(populations(0,100),(1,0))
    def test_invalid_negative(self):
        with self.assertRaises(ValueError): populations(-1,1)
    def test_invalid_nan(self):
        with self.assertRaises(ValueError): populations(float('nan'),1)
    def test_invalid_time(self):
        with self.assertRaises(ValueError): populations(1,-1)

if __name__=='__main__': unittest.main()
