import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from soft_photon_toy import mean_count,exclusive_zero,poisson_probability,expected_radiated_energy,no_resolved_emission
class Tests(unittest.TestCase):
    def test_log(self): self.assertAlmostEqual(mean_count(.2,1,math.e),.2)
    def test_no_emission(self): self.assertAlmostEqual(exclusive_zero(.3,1,math.e),math.exp(-.3))
    def test_probability_sum(self): self.assertAlmostEqual(sum(poisson_probability(.5,.01,1,n) for n in range(50)),1,places=12)
    def test_beta_zero(self): self.assertEqual(poisson_probability(0,.01,1,0),1)
    def test_beta_zero_nonzero_n(self): self.assertEqual(poisson_probability(0,.01,1,2),0)
    def test_lower_cutoff_more_photons(self): self.assertGreater(mean_count(.1,.0001,1),mean_count(.1,.01,1))
    def test_exclusive_zero_decreases(self): self.assertLess(exclusive_zero(.1,.0001,1),exclusive_zero(.1,.01,1))
    def test_finite_energy_limit(self): self.assertAlmostEqual(expected_radiated_energy(.1,.000001,1),.0999999)
    def test_resolution(self): self.assertAlmostEqual(no_resolved_emission(.1,.1,1),.1**.1)
    def test_invalid_cutoffs(self):
        with self.assertRaises(ValueError): mean_count(.1,0,1)
    def test_invalid_beta(self):
        with self.assertRaises(ValueError): mean_count(-.1,.1,1)
    def test_invalid_n(self):
        with self.assertRaises(ValueError): poisson_probability(.1,.1,1,-1)
    def test_nan(self):
        with self.assertRaises(ValueError): mean_count(float('nan'),.1,1)
if __name__=='__main__': unittest.main()
