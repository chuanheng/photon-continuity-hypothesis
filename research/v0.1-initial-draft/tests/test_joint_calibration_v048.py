import unittest, math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from models.joint_calibration import *
class ModelTests(unittest.TestCase):
 def setUp(self): self.d=Design()
 def test_defaults_valid(self): self.d.validate()
 def test_means_default(self): self.assertEqual(means(self.d),(11.,9.,7.,5.))
 def test_zero_exposure(self): self.assertEqual(means(Design(t=0)),(0.,)*4)
 def test_scaled_exposure(self): self.assertEqual(means(Design(t=2)),(22.,18.,14.,10.))
 def test_eta_scaling(self): self.assertEqual(means(self.d,eta=2),(21.,17.,13.,9.))
 def test_beta_scaling(self): self.assertEqual(means(self.d,beta=2),(12.,10.,8.,6.))
 def test_eps_template(self): self.assertEqual(means(self.d,eps=1),(11.,9.,10.,5.))
 def test_negative_eta(self):
  with self.assertRaises(ValueError): means(self.d,eta=-1)
 def test_negative_beta(self):
  with self.assertRaises(ValueError): means(self.d,beta=-1)
 def test_negative_eps(self):
  with self.assertRaises(ValueError): means(self.d,eps=-1)
 def test_invalid_exposure(self):
  with self.assertRaises(ValueError): Design(t=-1).validate()
 def test_nan_template(self):
  with self.assertRaises(ValueError): Design(s=(float('nan'),)*4).validate()
 def test_mismatched_templates(self):
  with self.assertRaises(ValueError): Design(s=(1,),b=(1,2),h=(1,)).validate()
 def test_zero_signal_template(self):
  with self.assertRaises(ValueError): Design(s=(0,)*4).validate()
 def test_lp_zero_count_zero_mean(self): self.assertEqual(loglike(self.d,Data((0,)*4,0,0),1,1,0),-232.)
 def test_lp_positive_count_zero_mean(self): self.assertEqual(loglike(self.d,Data((1,0,0,0),0,0),0,0,0),-math.inf)
 def test_negative_parameter_likelihood(self): self.assertEqual(loglike(self.d,Data((0,)*4,0,0),-1,1,0),-math.inf)
 def test_fit_boundary_eps(self): self.assertGreaterEqual(fit(self.d,Data((11,9,7,5),100,100))[1][2],0)
 def test_fit_returns_finite(self): self.assertTrue(math.isfinite(fit(self.d,Data((11,9,7,5),100,100))[0]))
 def test_q_nonnegative(self): self.assertGreaterEqual(q_stat(self.d,Data((12,9,12,5),100,100)),0)
 def test_q_reproducible(self):
  y=generate(self.d,seed=8); self.assertEqual(q_stat(self.d,y),q_stat(self.d,y))
 def test_generate_reproducible(self): self.assertEqual(generate(self.d,seed=7),generate(self.d,seed=7))
 def test_generate_zero_mu(self): self.assertEqual(poisson(__import__('random').Random(1),0),0)
 def test_poisson_reject_negative(self):
  with self.assertRaises(ValueError): poisson(__import__('random').Random(1),-1)
 def test_bootstrap_reject_small_null(self):
  with self.assertRaises(ValueError): bootstrap(self.d,n_null=2)
 def test_bootstrap_reject_alpha(self):
  with self.assertRaises(ValueError): bootstrap(self.d,alpha=1)
 def test_bootstrap_shape(self):
  r=bootstrap(self.d,n_null=20,n_alt=5,seed=1); self.assertEqual((r['n_null'],r['n_alt']),(20,5))
 def test_bootstrap_range(self):
  r=bootstrap(self.d,n_null=20,n_alt=5,seed=1); self.assertTrue(0<=r['power']<=1 and 0<=r['fpr']<=1)
 def test_calibration_zero_valid(self): Design(k_eta=0,k_beta=0).validate()
 def test_calibration_negative_invalid(self):
  with self.assertRaises(ValueError): Design(k_eta=-1).validate()
 def test_h_equal_s_nonident_no_cal(self):
  d=Design(h=(10.,8.,6.,4.),k_eta=0,k_beta=100); y=Data((15,12,9,6),0,100)
  # Under proportional templates, science identifies eta+eps only; equality of fitted optima.
  self.assertLess(abs(fit(d,y,True)[0]-fit(d,y,False)[0]),1e-7)
 def test_wilson_bounds(self):
  lo,hi=wilson(5,100); self.assertLess(lo,.05); self.assertGreater(hi,.05)
 def test_wilson_all_zero(self): self.assertEqual(wilson(0,100)[0],0)
 def test_wilson_invalid_n(self):
  with self.assertRaises(ValueError): wilson(0,0)
 def test_alt_fit_not_worse(self):
  y=Data((11,9,16,5),100,100); self.assertGreaterEqual(fit(self.d,y,True)[0],fit(self.d,y,False)[0]-1e-9)
if __name__=='__main__': unittest.main()
