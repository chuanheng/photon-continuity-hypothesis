import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from soft_successor_detection import *
class Tests(unittest.TestCase):
    def test_mean(self): self.assertAlmostEqual(mean_resolved_photons(.1,1,math.e),.1)
    def test_zero_beta(self): self.assertEqual(mean_resolved_photons(0,1,10),0)
    def test_threshold_above(self): self.assertEqual(mean_resolved_photons(.2,10,5),0)
    def test_standard_zero(self): self.assertEqual(standard_click_probability(0,1,10),0)
    def test_standard_poisson(self): self.assertAlmostEqual(standard_click_probability(.1,1,math.e),1-math.exp(-.1))
    def test_thinning(self): self.assertAlmostEqual(standard_click_probability(.1,1,math.e,.5),1-math.exp(-.05))
    def test_no_efficiency(self): self.assertEqual(standard_click_probability(.1,1,10,0),0)
    def test_successor_detected(self): self.assertEqual(successor_click_probability(0,1,10,2),1)
    def test_successor_missed(self): self.assertEqual(successor_click_probability(0,3,10,2),0)
    def test_partial_successor(self): self.assertAlmostEqual(successor_click_probability(0,1,10,2,.6),.6)
    def test_union(self):
        p=standard_click_probability(.1,1,math.e)
        self.assertAlmostEqual(successor_click_probability(.1,1,math.e,2,.6),p+.6*(1-p))
    def test_excess_nonnegative(self): self.assertGreaterEqual(click_excess(.1,1,10,2,.7),0)
    def test_excess_zero_below_threshold(self): self.assertEqual(click_excess(.1,3,10,2,.7),0)
    def test_beta_negative(self):
        with self.assertRaises(ValueError): mean_resolved_photons(-1,1,10)
    def test_bad_threshold(self):
        with self.assertRaises(ValueError): mean_resolved_photons(.1,0,10)
    def test_bad_efficiency(self):
        with self.assertRaises(ValueError): standard_click_probability(.1,1,10,1.1)
    def test_bad_successor(self):
        with self.assertRaises(ValueError): successor_click_probability(.1,1,10,0)
    def test_bad_successor_efficiency(self):
        with self.assertRaises(ValueError): successor_click_probability(.1,1,10,2,-.1)
    def test_monotonic_threshold(self): self.assertGreater(standard_click_probability(.1,1,10),standard_click_probability(.1,2,10))
    def test_finite_near_upper(self): self.assertGreaterEqual(standard_click_probability(.1,9.999,10),0)
if __name__=='__main__': unittest.main()
