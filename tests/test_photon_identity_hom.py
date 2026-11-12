import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from photon_identity_hom import coincidence_probability,bunching_probability,gaussian_delay_coincidence

class TestHOM(unittest.TestCase):
    def test_identical(self): self.assertEqual(coincidence_probability(1),0)
    def test_distinguishable(self): self.assertEqual(coincidence_probability(0),.5)
    def test_partial(self): self.assertEqual(coincidence_probability(.5),.25)
    def test_bunching(self): self.assertEqual(bunching_probability(1),1)
    def test_normalization(self):
        for x in (0,.1,.5,.9,1): self.assertAlmostEqual(coincidence_probability(x)+bunching_probability(x),1)
    def test_zero_delay(self): self.assertEqual(gaussian_delay_coincidence(0,1),0)
    def test_symmetric_delay(self): self.assertEqual(gaussian_delay_coincidence(-1,2),gaussian_delay_coincidence(1,2))
    def test_large_delay(self): self.assertAlmostEqual(gaussian_delay_coincidence(100,1),.5)
    def test_invalid_overlap(self):
        for x in (-.1,1.1,float('nan')):
            with self.assertRaises(ValueError): coincidence_probability(x)
    def test_invalid_coherence(self):
        with self.assertRaises(ValueError): gaussian_delay_coincidence(1,0)
    def test_invalid_delay(self):
        with self.assertRaises(ValueError): gaussian_delay_coincidence(float('inf'),1)
    def test_monotonic_delay(self): self.assertLess(gaussian_delay_coincidence(.2,1),gaussian_delay_coincidence(1,1))
if __name__=='__main__': unittest.main()
