import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from continuum_channels import *

class ContinuumTests(unittest.TestCase):
    def test_golden_rule(self): self.assertAlmostEqual(golden_rule_rate(2,3),24*math.pi)
    def test_complex_element(self): self.assertAlmostEqual(golden_rule_rate(3+4j,1),50*math.pi)
    def test_hbar(self): self.assertAlmostEqual(golden_rule_rate(1,1,2),math.pi)
    def test_zero_matrix_element(self): self.assertEqual(golden_rule_rate(0,1),0)
    def test_zero_density(self): self.assertEqual(golden_rule_rate(1,0),0)
    def test_equal_branch(self): self.assertEqual(branching_rates(2,2),(.5,.5))
    def test_direction_a(self): self.assertEqual(branching_rates(2,0),(1,0))
    def test_no_channels(self): self.assertEqual(branching_rates(0,0),(0,0))
    def test_branch_normalization(self): self.assertAlmostEqual(sum(branching_rates(2,3)),1)
    def test_transition_zero(self): self.assertEqual(transition_probability(1,0),0)
    def test_transition_lifetime(self): self.assertAlmostEqual(transition_probability(2,.5),1-math.exp(-1))
    def test_click_probability(self): self.assertAlmostEqual(resolved_successor_probability(2,2,1,.8),.4*(1-math.exp(-4)))
    def test_density_scaling(self): self.assertAlmostEqual(continuum_density_3d(4),2)
    def test_density_threshold(self): self.assertEqual(continuum_density_3d(0),0)
    def test_invalid_rate(self):
        with self.assertRaises(ValueError): branching_rates(-1,2)
    def test_invalid_hbar(self):
        with self.assertRaises(ValueError): golden_rule_rate(1,1,0)
    def test_invalid_efficiency(self):
        with self.assertRaises(ValueError): resolved_successor_probability(1,1,1,2)
    def test_invalid_density(self):
        with self.assertRaises(ValueError): continuum_density_3d(-1)
    def test_invalid_time(self):
        with self.assertRaises(ValueError): transition_probability(1,float('nan'))
if __name__=='__main__': unittest.main()
