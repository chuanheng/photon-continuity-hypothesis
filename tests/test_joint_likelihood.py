import math,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from joint_likelihood import *
class Tests(unittest.TestCase):
 def test_normalize(self): self.assertEqual(normalized_bins([2,2]),(.5,.5))
 def test_normalize_zero(self):
  with self.assertRaises(ValueError): normalized_bins([0,0])
 def test_negative_weight(self):
  with self.assertRaises(ValueError): normalized_bins([1,-1])
 def test_nan_weight(self):
  with self.assertRaises(ValueError): normalized_bins([1,float('nan')])
 def test_identity_response(self): self.assertEqual(observed_bins([2,1],[[1,0],[0,1]]),(2/3,1/3))
 def test_mixing_response(self): self.assertEqual(observed_bins([1,0],[[.8,.2],[.2,.8]]),(.8,.2))
 def test_invalid_response_shape(self):
  with self.assertRaises(ValueError): observed_bins([1,1],[[1]])
 def test_invalid_response_sum(self):
  with self.assertRaises(ValueError): observed_bins([1,1],[[.5,.5],[.2,.2]])
 def test_invalid_response_negative(self):
  with self.assertRaises(ValueError): observed_bins([1,1],[[1,-1],[0,2]])
 def test_equal_hypotheses(self): self.assertAlmostEqual(log_likelihood_ratio([4,6],[.5,.5],[.5,.5]),0)
 def test_h1_favored(self): self.assertGreater(log_likelihood_ratio([8,2],[.5,.5],[.8,.2]),0)
 def test_h0_favored(self): self.assertLess(log_likelihood_ratio([2,8],[.5,.5],[.8,.2]),0)
 def test_zero_counts(self): self.assertEqual(log_likelihood_ratio([0,0],[.5,.5],[.8,.2]),0)
 def test_zero_h0(self): self.assertEqual(log_likelihood_ratio([1,0],[0,1],[.5,.5]),math.inf)
 def test_zero_h1(self): self.assertEqual(log_likelihood_ratio([1,0],[.5,.5],[0,1]),-math.inf)
 def test_both_impossible(self):
  with self.assertRaises(ValueError): log_likelihood_ratio([1,0],[0,1],[0,1])
 def test_bad_counts(self):
  with self.assertRaises(ValueError): log_likelihood_ratio([1.5,2],[.5,.5],[.5,.5])
 def test_kl_equal(self): self.assertAlmostEqual(kl_divergence([.5,.5],[.5,.5]),0)
 def test_kl_positive(self): self.assertGreater(kl_divergence([.8,.2],[.5,.5]),0)
 def test_kl_infinite(self): self.assertEqual(kl_divergence([1,1],[1,0]),math.inf)
 def test_kl_expected_llr(self): self.assertAlmostEqual(kl_divergence([.8,.2],[.5,.5]),.8*math.log(1.6)+.2*math.log(.4))
if __name__=='__main__': unittest.main()
