import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from hydrogen_coulomb_cross_section import *

class CoulombTests(unittest.TestCase):
    def test_threshold_benchmark(self): self.assertAlmostEqual(threshold_cross_section_cm2()/1e-18,6.3043181,places=5)
    def test_threshold_exact(self): self.assertEqual(cross_section_cm2(IONIZATION_EV),threshold_cross_section_cm2())
    def test_below_threshold(self): self.assertEqual(cross_section_cm2(10),0)
    def test_zero_energy(self): self.assertEqual(cross_section_cm2(0),0)
    def test_near_threshold(self): self.assertAlmostEqual(cross_section_cm2(IONIZATION_EV*(1+1e-8))/threshold_cross_section_cm2(),1,places=6)
    def test_positive(self): self.assertGreater(cross_section_cm2(20),0)
    def test_decreasing_20_40(self): self.assertGreater(cross_section_cm2(20),cross_section_cm2(40))
    def test_decreasing_40_100(self): self.assertGreater(cross_section_cm2(40),cross_section_cm2(100))
    def test_units(self): self.assertAlmostEqual(cross_section_megabarn(IONIZATION_EV),6.3043181,places=5)
    def test_finite_very_high(self): self.assertTrue(math.isfinite(cross_section_cm2(1e8)))
    def test_large_energy_suppression(self): self.assertLess(cross_section_cm2(1e6),cross_section_cm2(1e3))
    def test_threshold_formula(self): self.assertAlmostEqual(threshold_cross_section_cm2(),(512*math.pi**2/3)*ALPHA*BOHR_RADIUS_CM**2*math.exp(-4))
    def test_nan(self):
        with self.assertRaises(ValueError): cross_section_cm2(float('nan'))
    def test_infinity(self):
        with self.assertRaises(ValueError): cross_section_cm2(float('inf'))
    def test_negative(self):
        with self.assertRaises(ValueError): cross_section_cm2(-1)
    def test_shape_at_2x(self): self.assertGreater(cross_section_megabarn(IONIZATION_EV*2),0)
    def test_nonnegative_grid(self):
        for e in (0,10,IONIZATION_EV,15,20,30,50,100,1000): self.assertGreaterEqual(cross_section_cm2(e),0)
    def test_threshold_continuity(self):
        for epsilon in (1e-5,1e-6):
            self.assertLess(abs(cross_section_cm2(IONIZATION_EV*(1+epsilon))/threshold_cross_section_cm2()-1),1e-3)
if __name__=='__main__': unittest.main()
