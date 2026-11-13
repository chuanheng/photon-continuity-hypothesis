import math,pathlib,random,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from monte_carlo_power import *
class Tests(unittest.TestCase):
 def test_normalize(self): self.assertEqual(probabilities([2,2]),(.5,.5))
 def test_zero_weights(self):
  with self.assertRaises(ValueError): probabilities([0,0])
 def test_negative_weights(self):
  with self.assertRaises(ValueError): probabilities([1,-1])
 def test_nan_weights(self):
  with self.assertRaises(ValueError): probabilities([float('nan'),1])
 def test_identity_response(self): self.assertEqual(detector_response([.7,.3],[[1,0],[0,1]]),(.7,.3))
 def test_blind_response(self): self.assertEqual(detector_response([.7,.3],[[.5,.5],[.5,.5]]),(.5,.5))
 def test_response_bad_column(self):
  with self.assertRaises(ValueError): detector_response([.7,.3],[[.4,.4],[.4,.4]])
 def test_response_bad_shape(self):
  with self.assertRaises(ValueError): detector_response([.7,.3],[[1]])
 def test_llr_zero(self): self.assertEqual(log_likelihood_ratio([1,2],[.5,.5],[.5,.5]),0)
 def test_llr_h1(self): self.assertGreater(log_likelihood_ratio([9,1],[.5,.5],[.9,.1]),0)
 def test_llr_h0(self): self.assertLess(log_likelihood_ratio([1,9],[.5,.5],[.9,.1]),0)
 def test_llr_inf(self): self.assertEqual(log_likelihood_ratio([1,0],[0,1],[.5,.5]),math.inf)
 def test_llr_bad_count(self):
  with self.assertRaises(ValueError): log_likelihood_ratio([1.2,2],[.5,.5],[.5,.5])
 def test_sample_size(self): self.assertEqual(sum(sample_counts([.2,.8],100,random.Random(1))),100)
 def test_sample_repeat(self): self.assertEqual(sample_counts([.2,.8],100,random.Random(5)),sample_counts([.2,.8],100,random.Random(5)))
 def test_sample_zero(self): self.assertEqual(sample_counts([.2,.8],0,random.Random(5)),(0,0))
 def test_sample_negative(self):
  with self.assertRaises(ValueError): sample_counts([.2,.8],-1,random.Random(5))
 def test_reproducible(self): self.assertEqual(simulate_power([.7,.2,.1],[.6,.25,.15],30,100,seed=7),simulate_power([.7,.2,.1],[.6,.25,.15],30,100,seed=7))
 def test_calibration(self): self.assertLessEqual(simulate_power([.7,.2,.1],[.6,.25,.15],30,1000)['false_positive_rate'],.05)
 def test_identical(self): self.assertEqual(simulate_power([.7,.3],[.7,.3],30,100)['power'],0)
 def test_alpha(self):
  with self.assertRaises(ValueError): simulate_power([.7,.3],[.6,.4],30,100,alpha=1)
 def test_repetitions(self):
  with self.assertRaises(ValueError): simulate_power([.7,.3],[.6,.4],30,10)
 def test_size(self):
  with self.assertRaises(ValueError): simulate_power([.7,.3],[.6,.4],0,100)
if __name__=='__main__': unittest.main()
