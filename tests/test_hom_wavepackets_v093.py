"""v0.93 independently authored GitHub regression suite, 40 unittest cases.
Original 40 locally executed test cases and exact bytes live in full ZIP.
"""
import unittest
import numpy as np
from scipy.integrate import quad
from models.hom_wavepackets_v093 import *
class PureTests(unittest.TestCase):
 def test_identical(self):self.assertAlmostEqual(pure_overlap(),1)
 def test_detuning(self):self.assertAlmostEqual(pure_overlap(detuning=1),.5)
 def test_linewidth(self):self.assertAlmostEqual(pure_overlap(1,2),8/9)
 def test_delay_plus(self):self.assertAlmostEqual(pure_overlap(delay=1),np.exp(-1))
 def test_delay_minus(self):self.assertAlmostEqual(pure_overlap(delay=-1),np.exp(-1))
 def test_asym_plus(self):self.assertAlmostEqual(pure_overlap(1,2,delay=1),8/9*np.exp(-1))
 def test_asym_minus(self):self.assertAlmostEqual(pure_overlap(1,2,delay=-1),8/9*np.exp(-2))
 def test_exchange(self):self.assertAlmostEqual(pure_overlap(1,2,delay=.3),pure_overlap(2,1,delay=-.3))
 def test_zero_coincidence(self):self.assertAlmostEqual(coincidence(1),0)
 def test_half_coincidence(self):self.assertAlmostEqual(coincidence(0),.5)
 def test_mid_coincidence(self):self.assertAlmostEqual(coincidence(.5),.25)
 def test_background(self):self.assertAlmostEqual(coincidence(1,.1),.05)
 def test_all_background(self):self.assertAlmostEqual(coincidence(1,1),.5)
 def test_bad_rate(self):
  with self.assertRaises(ValueError):pure_overlap(g1=0)
 def test_bad_background(self):
  with self.assertRaises(ValueError):coincidence(.4,2)
 def test_numerical_check(self):
  for a,b,w,d in [(1,1,0,0),(1,2,0,1),(.7,2,1,-.25)]:
   self.assertAlmostEqual(pure_overlap(a,b,w,d),numerical_pure_overlap(a,b,w,d),places=8)
class NoiseTests(unittest.TestCase):
 def test_time_zero(self):self.assertEqual(time_jitter_average(),1)
 def test_frequency_zero(self):self.assertEqual(spectral_jitter_average(),1)
 def test_common_time(self):self.assertEqual(time_jitter_average(onset_std=.2,correlation=1),1)
 def test_common_freq(self):self.assertEqual(spectral_jitter_average(frequency_std=.3,correlation=1),1)
 def test_correlation_time(self):self.assertGreater(time_jitter_average(onset_std=.2,correlation=.8),time_jitter_average(onset_std=.2))
 def test_correlation_freq(self):self.assertGreater(spectral_jitter_average(frequency_std=.3,correlation=.8),spectral_jitter_average(frequency_std=.3))
 def test_factor(self):
  self.assertAlmostEqual(ensemble_overlap(onset_std=.2,frequency_std=.3),
       time_jitter_average(onset_std=.2)*spectral_jitter_average(frequency_std=.3))
 def test_ensemble_independent(self):self.assertAlmostEqual(ensemble_overlap(onset_std=.2,frequency_std=.3),.708102263506253)
 def test_ensemble_correlated(self):self.assertAlmostEqual(ensemble_overlap(onset_std=.2,frequency_std=.3,arrival_correlation=.8,frequency_correlation=.8),.8769429272607854)
 def test_MC_100000(self):
  a=monte_carlo_ensemble();self.assertLess(abs(a['mean_overlap']-.708102263506253),4*a['mc_standard_error'])
 def test_MC_reproducible(self):self.assertEqual(monte_carlo_ensemble(n=100,seed=99),monte_carlo_ensemble(n=100,seed=99))
 def test_MC_invalid(self):
  with self.assertRaises(ValueError):monte_carlo_ensemble(n=5)
 def test_corr_invalid(self):
  with self.assertRaises(ValueError):spectral_jitter_average(frequency_std=.2,correlation=3)
 def test_std_invalid(self):
  with self.assertRaises(ValueError):time_jitter_average(onset_std=-1)
 def test_noise_reduces_overlap(self):self.assertLess(ensemble_overlap(onset_std=.4,frequency_std=.5),ensemble_overlap(onset_std=.2,frequency_std=.3))
class PhysicalInternalTests(unittest.TestCase):
 def test_identical_modes(self):self.assertEqual(probability_from_states([1,0],[1,0]),0)
 def test_orthogonal_modes(self):self.assertEqual(probability_from_states([1,0],[0,1]),.5)
 def test_identical_internal(self):self.assertEqual(probability_from_states([1,0],[1,0],[1,0],[1,0]),0)
 def test_orthogonal_internal(self):self.assertEqual(probability_from_states([1,0],[1,0],[1,0],[0,1]),.5)
 def test_orthogonal_modes_identical_internal(self):self.assertEqual(probability_from_states([1,0],[0,1],[1,0],[1,0]),.5)
 def test_bad_modes(self):
  with self.assertRaises(ValueError):probability_from_states([1,1],[1,0])
 def test_unpaired_internal(self):
  with self.assertRaises(ValueError):probability_from_states([1,0],[1,0],[1,0],None)
 def test_summary(self):self.assertAlmostEqual(summary()['pure_cases']['detuning_1_gamma']['ideal_coincidence'],.25)
if __name__=='__main__':unittest.main()
