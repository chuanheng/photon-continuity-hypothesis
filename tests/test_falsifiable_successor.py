import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from falsifiable_successor import branch_probabilities,successor_click_probability,binomial_log_likelihood,log_likelihood_ratio

class TestSuccessor(unittest.TestCase):
    def test_direction_a_branch(self): self.assertEqual(branch_probabilities(1,0),(1,0))
    def test_absorption_branch(self): self.assertEqual(branch_probabilities(0,1),(0,1))
    def test_equal_branch(self): self.assertAlmostEqual(branch_probabilities(1,1)[0],.5)
    def test_normalization(self): self.assertAlmostEqual(sum(branch_probabilities(3,4)),1)
    def test_direction_a_click(self): self.assertEqual(successor_click_probability(1,0,.8,2,1),.8)
    def test_reference_click(self): self.assertAlmostEqual(successor_click_probability(1,1,.8,2,1),.4)
    def test_below_threshold(self): self.assertEqual(successor_click_probability(1,0,.8,.1,1),0)
    def test_threshold_boundary(self): self.assertEqual(successor_click_probability(1,0,.8,1,1),.8)
    def test_zero_efficiency(self): self.assertEqual(successor_click_probability(1,0,0,2,1),0)
    def test_binomial_half(self): self.assertAlmostEqual(binomial_log_likelihood(1,2,.5),math.log(.5))
    def test_binomial_impossible(self): self.assertEqual(binomial_log_likelihood(1,2,0),-math.inf)
    def test_likelihood_prefers_a(self): self.assertGreater(log_likelihood_ratio(80,100,.8,.4),0)
    def test_likelihood_prefers_reference(self): self.assertLess(log_likelihood_ratio(40,100,.8,.4),0)
    def test_invalid_coupling(self):
        with self.assertRaises(ValueError): branch_probabilities(0,0)
    def test_invalid_energy(self):
        with self.assertRaises(ValueError): successor_click_probability(1,0,.5,0,1)
    def test_invalid_count(self):
        with self.assertRaises(ValueError): binomial_log_likelihood(3,2,.5)
    def test_invalid_probability(self):
        with self.assertRaises(ValueError): binomial_log_likelihood(1,2,1.1)

if __name__=="__main__": unittest.main()
