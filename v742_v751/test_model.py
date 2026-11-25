import math
import unittest
from .model import evaluate
r=evaluate()
class Band(unittest.TestCase):
    def test_cells(self): self.assertEqual(r['v7.42']['monitor_cells_for_one_peak_per_line_arm_group'],16)
    def test_scale(self): self.assertAlmostEqual(*r['v7.43'].values())
    def test_integral(self): self.assertAlmostEqual(r['v7.44']['integrated_ratio'],1.345541,5)
    def test_centroids(self): self.assertTrue(all(34.5<x<36.5 for x in r['v7.45']['arm_centroids_keV']))
    def test_derivative(self): self.assertAlmostEqual(*r['v7.46'].values(),8)
    def test_tilt(self): self.assertGreater(r['v7.47']['cross_ratios'][0],r['v7.47']['cross_ratios'][2])
    def test_material(self): self.assertAlmostEqual(r['v7.48']['inverse_material_weight'],.288624,5)
    def test_direction(self): self.assertLess(r['v7.49']['linewise_direction_ratio_ranges'][0][0],1)
    def test_bounds(self):
        lo,hi=r['v7.50']['grid_cross_bounds']
        self.assertLess(lo,1);self.assertGreater(hi,1.5)
    def test_resolution(self):
        self.assertAlmostEqual(r['v7.51']['flattening_tilt_per_keV'],evaluate(4001)['v7.51']['flattening_tilt_per_keV'],4)
