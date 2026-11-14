"""Regression tests for v1.09 (Python standard library)."""
import unittest
import math
from models.three_photon_v109 import (
    probabilities, coarse_distribution, max_abs_delta,
    kl, fisher_multinomial, OCCS,
)

class FourierTritterTests(unittest.TestCase):
    def test_normalization_positivity(self):
        for r in [0, .1, .3, .5]:
            for phase in [0, math.pi/3, math.pi, -math.pi/3]:
                p = probabilities(r,phase)
                self.assertEqual(len(p),10)
                self.assertAlmostEqual(sum(p),1,places=11)
                self.assertTrue(all(x>=0 for x in p))

    def test_classical_limit(self):
        p=probabilities(0,0)
        self.assertAlmostEqual(p[OCCS.index((0,0,0))],1/27)
        self.assertAlmostEqual(p[OCCS.index((0,1,2))],2/9)

    def test_full_output_distinguishes_phase_sign(self):
        pos=probabilities(.3,math.pi/3)
        neg=probabilities(.3,-math.pi/3)
        self.assertGreater(max_abs_delta(pos,neg),.008)
        self.assertGreater(kl(pos,neg),.002)

    def test_coarse_output_sign_ambiguity(self):
        pos=coarse_distribution(probabilities(.3,math.pi/3))
        neg=coarse_distribution(probabilities(.3,-math.pi/3))
        for x,y in zip(pos,neg):
            self.assertAlmostEqual(x,y,places=12)

    def test_phase_irrelevant_at_zero_overlap(self):
        self.assertLess(max_abs_delta(probabilities(0,0),probabilities(0,math.pi/3)),1e-12)

    def test_local_fisher_positive(self):
        a,b,c,det=fisher_multinomial(.3,math.pi/3)
        self.assertGreater(det,0)
        self.assertAlmostEqual(det,.0008443203043,places=8)

if __name__=="__main__":
    unittest.main()
