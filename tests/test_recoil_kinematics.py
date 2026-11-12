import math
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from recoil_kinematics import outgoing_energy, recoil_energy, invariant_residual

class RecoilTests(unittest.TestCase):
    def test_forward_exact(self):
        self.assertAlmostEqual(outgoing_energy(60,40,25_000_000), 20-40**2/(2*25_000_000))
    def test_zero_excitation_compton(self):
        r=511
        self.assertAlmostEqual(outgoing_energy(100,0,r,math.pi),100/(1+200/r))
    def test_angle_dependence(self):
        self.assertGreater(outgoing_energy(60,40,25_000_000,0), outgoing_energy(60,40,25_000_000,math.pi))
    def test_recoil_positive(self):
        self.assertGreater(recoil_energy(60,40,25_000_000),0)
    def test_conservation(self):
        self.assertLess(abs(invariant_residual(60,40,25_000_000,math.pi/3)),.1)
    def test_no_positive_successor(self):
        with self.assertRaises(ValueError): outgoing_energy(40,40,25_000_000)
    def test_invalid(self):
        with self.assertRaises(ValueError): outgoing_energy(60,40,-1)
        with self.assertRaises(ValueError): outgoing_energy(60,40,25_000_000,-.1)

if __name__=='__main__': unittest.main()
