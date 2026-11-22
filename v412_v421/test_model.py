import unittest
from v412_v421.model import run
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_412(self):self.assertAlmostEqual(sum(self.r['one_time']),1)
 def test_413(self):self.assertEqual(self.r['hankel_shapes']['3'],[15,15])
 def test_414(self):self.assertEqual(self.r['theoretical_ranks']['3'],4)
 def test_415(self):self.assertLess(self.r['theoretical_singular_first5'][4],1e-12)
 def test_416(self):self.assertGreater(self.r['best_rank2_residual'],.03)
 def test_417(self):self.assertGreater(self.r['naive_rank_at_1e_minus_4'],4)
 def test_418(self):self.assertEqual(self.r['null_n'],60)
 def test_419(self):self.assertGreater(self.r['observed_fifth'],0)
 def test_420(self):self.assertEqual(self.r['theoretical_ranks']['4'],4)
 def test_421(self):self.assertFalse(self.r['identity_unique'])
if __name__=='__main__':unittest.main()
