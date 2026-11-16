"""v0.92 regression tests for published GitHub model.
The original locally executed 46-case suite is in photon_v092_complete.zip.
"""
import unittest
import numpy as np
from scipy.integrate import quad
from models.wigner_weisskopf_v092 import *

class AnalyticChecks(unittest.TestCase):
 def test_initial(self):self.assertAlmostEqual(atomic_amplitude(0),1)
 def test_exponential(self):self.assertAlmostEqual(excited_population(1),np.exp(-1))
 def test_half_life(self):self.assertAlmostEqual(excited_population(np.log(2)),.5)
 def test_lamb_shift(self):self.assertAlmostEqual(abs(atomic_amplitude(2,lamb_shift=.5)),np.exp(-1))
 def test_negative_time(self):
  with self.assertRaises(ValueError):atomic_amplitude(-1)
 def test_gamma_zero(self):
  with self.assertRaises(ValueError):atomic_amplitude(1,0)
 def test_cdf(self):self.assertAlmostEqual(emission_probability_by(1),1-np.exp(-1))
 def test_density_norm(self):self.assertAlmostEqual(quad(lambda t:detection_density(t),0,np.inf)[0],1)
 def test_time_mode_causal(self):self.assertEqual(time_mode(-.2),0)
 def test_time_mode_norm(self):self.assertAlmostEqual(quad(lambda t:abs(time_mode(t))**2,0,np.inf)[0],1)
 def test_spectrum_norm(self):self.assertAlmostEqual(quad(lambda d:spectrum(d),-np.inf,np.inf)[0],1)
 def test_spectrum_peak(self):self.assertAlmostEqual(spectrum(0),2/np.pi)
 def test_spectrum_halfmax(self):self.assertAlmostEqual(spectrum(.5),spectrum(0)/2)
 def test_frequency_symmetry(self):self.assertAlmostEqual(spectrum(-2),spectrum(2))
 def test_spectral_amplitude(self):
  d=np.linspace(-3,3,25)
  self.assertTrue(np.allclose(abs(spectral_amplitude(d))**2,spectrum(d)))
 def test_spectral_bad_gamma(self):
  with self.assertRaises(ValueError):spectrum(0,gamma=0)
 def test_overlap_identical(self):self.assertAlmostEqual(overlap_probability(1,1),1)
 def test_overlap_frequency(self):self.assertAlmostEqual(overlap_probability(1,1,1),.5)
 def test_overlap_width(self):self.assertAlmostEqual(overlap_probability(1,2),8/9)
 def test_overlap_delay(self):self.assertAlmostEqual(overlap_probability(1,1,onset_difference=1),np.exp(-1))
 def test_overlap_negative_delay(self):self.assertAlmostEqual(overlap_probability(1,1,onset_difference=-1),np.exp(-1))
 def test_overlap_invalid(self):
  with self.assertRaises(ValueError):pulse_overlap(0,1)
 def test_markov_population_plus_field(self):
  t=np.linspace(0,3,20)
  self.assertTrue(np.allclose(excited_population(t)+emission_probability_by(t),1))

class FiniteModes(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.times=np.linspace(0,8,81)
  cls.o=finite_evolution(cls.times)
 def test_h_hermitian(self):
  h,_,_=finite_reservoir()
  self.assertLess(np.linalg.norm((h-h.getH()).toarray()),1e-12)
 def test_dimensions(self):self.assertEqual(len(self.o['mode_detunings']),401)
 def test_initial(self):self.assertAlmostEqual(self.o['atomic_population'][0],1)
 def test_initial_field(self):self.assertAlmostEqual(self.o['field_population'][0],0)
 def test_unitary(self):self.assertLess(np.max(abs(self.o['total_norm']-1)),1e-10)
 def test_excitation_conservation(self):
  self.assertTrue(np.allclose(self.o['atomic_population']+self.o['field_population'],1,atol=1e-10))
 def test_markov_near_two(self):self.assertLess(abs(self.o['atomic_population'][20]-np.exp(-2)),.003)
 def test_markov_from_half(self):
  mask=self.times>=.5
  self.assertLess(np.max(abs(self.o['atomic_population'][mask]-np.exp(-self.times[mask]))),.04)
 def test_emission_complete_by_eight(self):self.assertLess(self.o['atomic_population'][-1],.001)
 def test_mode_norm_at_end(self):
  self.assertAlmostEqual(sum(abs(self.o['mode_amplitudes_at_end'])**2),self.o['field_population'][-1])
 def test_positive_couplings(self):self.assertTrue(np.all(self.o['couplings']>0))
 def test_curvature(self):
  s=finite_evolution(np.array([0,.001,.002]),modes=101)
  c=finite_early_curvature(modes=101)
  self.assertAlmostEqual((1-s['atomic_population'][1])/1e-6,c,delta=.03)
 def test_bad_even_modes(self):
  with self.assertRaises(ValueError):finite_reservoir(modes=10)
 def test_bad_bandwidth(self):
  with self.assertRaises(ValueError):finite_reservoir(bandwidth=0)
 def test_bad_time_grid(self):
  with self.assertRaises(ValueError):finite_evolution([0,.1,.3])
 def test_summary(self):
  d=compact_summary()
  self.assertEqual(d['version'],'v0.92')
  self.assertLess(d['max_norm_error'],1e-10)
 def test_early_unitary_slope(self):
  s=finite_evolution(np.array([0,1e-5,2e-5]),modes=101)
  self.assertLess((1-s['atomic_population'][1])/1e-5,1e-3)

# Parallel parameterized checks: explicit independent assertions.
def generate_cases():
 def mk_overlap_shift(delta):
  def run(self):self.assertAlmostEqual(overlap_probability(1,1,delta),1/(1+delta*delta))
  return run
 for i,delta in enumerate([.05,.1,.2,.3,.6,.8,1.2,1.5,2]):
  setattr(AnalyticChecks,'test_overlap_frequency_grid_'+str(i),mk_overlap_shift(delta))
generate_cases()

if __name__=='__main__':unittest.main()
