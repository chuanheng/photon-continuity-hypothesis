import math
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'models'))
from photon_detection import (signal_click_probability, no_click_probability,
                              any_click_probability, first_signal_click_density, fock_g2_zero)

class DetectionTests(unittest.TestCase):
    def test_zero_time(self): self.assertEqual(signal_click_probability(2, 0, .7), 0)
    def test_zero_efficiency(self): self.assertEqual(signal_click_probability(2, 10, 0), 0)
    def test_long_time(self): self.assertAlmostEqual(signal_click_probability(1, 100, .6), .6)
    def test_one_lifetime(self): self.assertAlmostEqual(signal_click_probability(2, .5, .8), .8*(1-math.exp(-1)))
    def test_no_click(self): self.assertAlmostEqual(no_click_probability(1, 100, .6), .4)
    def test_dark_only(self): self.assertAlmostEqual(no_click_probability(0, 2, .7, .3), math.exp(-.6))
    def test_dark_and_signal(self): self.assertAlmostEqual(no_click_probability(1, 2, .5, .1), math.exp(-.2)*(1-.5*(1-math.exp(-2))))
    def test_complement(self): self.assertAlmostEqual(any_click_probability(1, 2, .5, .1)+no_click_probability(1, 2, .5, .1),1)
    def test_click_density(self): self.assertAlmostEqual(first_signal_click_density(2, 0, .7),1.4)
    def test_single_photon_antibunching(self): self.assertEqual(fock_g2_zero(1),0)
    def test_two_photon(self): self.assertEqual(fock_g2_zero(2),.5)
    def test_invalid_efficiency(self):
        with self.assertRaises(ValueError): signal_click_probability(1, 2, 1.1)
    def test_invalid_dark_rate(self):
        with self.assertRaises(ValueError): no_click_probability(1, 2, .5, -.1)
    def test_invalid_time(self):
        with self.assertRaises(ValueError): no_click_probability(1, float('nan'), .5)
    def test_invalid_number(self):
        with self.assertRaises(ValueError): fock_g2_zero(0)

if __name__ == '__main__': unittest.main()
