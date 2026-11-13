import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from hydrogen_photoionization import *

class TestHydrogen(unittest.TestCase):
    def test_phi_zero(self): self.assertAlmostEqual(phi_1s((0,0,0)),FOURIER_NORM)
    def test_phi_decay(self): self.assertAlmostEqual(phi_1s((0,0,1)),FOURIER_NORM/4)
    def test_phi_rotation(self): self.assertAlmostEqual(phi_1s((1,0,0)),phi_1s((0,0,1)))
    def test_dipole_zero_momentum(self): self.assertEqual(dipole_z((0,0,0)),0)
    def test_dipole_transverse_zero(self): self.assertEqual(dipole_z((1,0,0)),0)
    def test_dipole_nonzero(self): self.assertGreater(dipole_strength((0,0,1)),0)
    def test_dipole_odd(self): self.assertEqual(dipole_z((0,0,-1)),-dipole_z((0,0,1)))
    def test_strength_even(self): self.assertEqual(dipole_strength((0,0,-1)),dipole_strength((0,0,1)))
    def test_dipole_analytic(self): self.assertAlmostEqual(dipole_strength((0,0,1)),(4*FOURIER_NORM)**2/64)
    def test_angle_integral(self): self.assertAlmostEqual(angle_integrated_strength(1),(4*math.pi/3)*(4*FOURIER_NORM)**2/64)
    def test_angle_zero(self): self.assertEqual(angle_integrated_strength(0),0)
    def test_radial(self): self.assertAlmostEqual(radial_strength_density(2),4*angle_integrated_strength(2))
    def test_threshold(self): self.assertEqual(kinetic_momentum(.5),0)
    def test_above_threshold(self): self.assertAlmostEqual(kinetic_momentum(1),1)
    def test_below_threshold(self):
        with self.assertRaises(ValueError): kinetic_momentum(.4)
    def test_invalid_momentum(self):
        with self.assertRaises(ValueError): dipole_z((1,2))
    def test_nonfinite(self):
        with self.assertRaises(ValueError): phi_1s((0,0,float('nan')))
    def test_invalid_radial(self):
        with self.assertRaises(ValueError): radial_strength_density(-1)

if __name__=='__main__': unittest.main()
