import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from identity_visibility import *

class IdentityVisibilityTests(unittest.TestCase):
    def test_normalize(self): self.assertEqual(normalize([3,4]),(.6+0j,.8+0j))
    def test_normalize_complex(self): self.assertAlmostEqual(sum(abs(x)**2 for x in normalize([1j,2])),1)
    def test_zero_vector(self):
        with self.assertRaises(ValueError): normalize([0,0])
    def test_empty(self):
        with self.assertRaises(ValueError): normalize([])
    def test_nan(self):
        with self.assertRaises(ValueError): normalize([float('nan')])
    def test_inf(self):
        with self.assertRaises(ValueError): normalize([float('inf')])
    def test_dimension_mismatch(self):
        with self.assertRaises(ValueError): overlap([1,0],[1,0,0])
    def test_identical_overlap(self): self.assertAlmostEqual(overlap([1,0],[1,0]).real,1)
    def test_orthogonal_overlap(self): self.assertEqual(overlap([1,0],[0,1]),0)
    def test_complex_overlap(self): self.assertAlmostEqual(abs(overlap([1,0],[1j,0])),1)
    def test_visibility_same(self): self.assertEqual(visibility([1,0],[1,0]),1)
    def test_visibility_orthogonal(self): self.assertEqual(visibility([1,0],[0,1]),0)
    def test_visibility_partial(self): self.assertAlmostEqual(visibility([1,0],[1,1]),1/math.sqrt(2))
    def test_probability_constructive(self): self.assertAlmostEqual(path_probability([1,0],[1,0],0),1)
    def test_probability_destructive(self): self.assertAlmostEqual(path_probability([1,0],[1,0],math.pi),0,places=14)
    def test_probability_no_interference(self): self.assertEqual(path_probability([1,0],[0,1],0),.5)
    def test_probability_partial(self): self.assertAlmostEqual(path_probability([1,0],[1,1],0),.5*(1+1/math.sqrt(2)))
    def test_invalid_phase(self):
        with self.assertRaises(ValueError): path_probability([1],[1],float('nan'))
    def test_purity_pure(self): self.assertEqual(reduced_path_purity([1,0],[1,0]),1)
    def test_purity_mixed(self): self.assertEqual(reduced_path_purity([1,0],[0,1]),.5)
    def test_helstrom_identical(self): self.assertEqual(identity_information_bound([1,0],[1,0]),.5)
    def test_helstrom_orthogonal(self): self.assertEqual(identity_information_bound([1,0],[0,1]),1)
    def test_complementarity(self):
        v=visibility([1,0],[1,1]); distinguishability=2*identity_information_bound([1,0],[1,1])-1
        self.assertAlmostEqual(v*v+distinguishability**2,1)

if __name__=='__main__': unittest.main()
