"""GitHub v1.07 companion regression tests; exact 44 executed tests in ZIP."""
import unittest
import numpy as np
from models.gram_v107 import gram,gram_states,split_three,restricted_rho,triad_phase,gram_phase_demo
from models.rho_reference_v107 import (pair_prob,ref_counts,rho_reference,
    main_record,fit,paired_demo,optical)
class GramTests(unittest.TestCase):
 def test_photons_identical(self):
  v=[1,0,0]
  self.assertTrue(np.allclose(split_three([v,v,v]),[3/8,1/8,1/8,3/8]))
 def test_orthogonal_third(self):
  self.assertTrue(np.allclose(split_three([[1,0,0],[1,0,0],[0,1,0]]),[1/8,3/8,3/8,1/8]))
 def test_rho_intermediate(self):
  for rho in [0,.1,.5,.9,1]:
   phi=np.array([1.,0.,0.])
   psi=np.array([np.sqrt(rho),np.sqrt(1-rho),0.])
   self.assertTrue(np.allclose(split_three([phi,phi,psi]),restricted_rho(rho)))
 def test_gram_reconstruction(self):
  r=.5
  G=np.array([[1,r,r],[r,1,1j*r],[r,-1j*r,1]],complex)
  self.assertTrue(np.allclose(gram(gram_states(G)),G))
 def test_gram_phase_counterexample(self):
  p=gram_phase_demo()
  self.assertTrue(p['magnitudes_same'])
  self.assertTrue(np.allclose(p['distribution_0'],[.2,.3,.3,.2]))
  self.assertTrue(np.allclose(p['distribution_pi2'],[.175,.325,.325,.175]))
 def test_bad_gram(self):
  with self.assertRaises(ValueError):gram_states(np.array([[1,2,0],[2,1,0],[0,0,1]]))
 def test_bad_rho(self):
  with self.assertRaises(ValueError):restricted_rho(-.1)
 def test_three_states_normalized(self):
  r=np.random.default_rng(42)
  for _ in range(10):
   v=r.normal(size=(3,3))+1j*r.normal(size=(3,3))
   v/=np.linalg.norm(v,axis=1,keepdims=True)
   self.assertAlmostEqual(split_three(v).sum(),1)
 def test_initial_photon_permutation(self):
  v=np.array([[1.,0.],[1.,0.],[.5,np.sqrt(.75)]])
  self.assertTrue(np.allclose(split_three(v,(0,0,1)),split_three(v,(1,1,0))))
class RhoTests(unittest.TestCase):
 def test_pair_extremes(self):
  self.assertEqual(pair_prob(0),.5);self.assertEqual(pair_prob(1),0)
 def test_reference_reproducible(self):
  self.assertEqual(ref_counts(.1,1000,9),ref_counts(.1,1000,9))
 def test_uniform_reference_prior(self):
  r=rho_reference({'shots':0,'coincidences':0})
  self.assertAlmostEqual(r['mean'],.5)
 def test_reference_narrows(self):
  a=rho_reference(ref_counts(.1,100,9))
  b=rho_reference(ref_counts(.1,10000,9))
  self.assertLess(b['ci95'][1]-b['ci95'][0],a['ci95'][1]-a['ci95'][0])
 def test_rho_reference_probability(self):
  a=rho_reference(ref_counts(.1,10000,9))
  self.assertLess(abs(a['mean']-.1),.04)
 def test_reject_bad_count(self):
  with self.assertRaises(ValueError):rho_reference({'shots':20,'coincidences':21})
 def test_reject_bad_shots(self):
  with self.assertRaises(ValueError):ref_counts(.1,-1)
 def test_far_independent_rho(self):
  a=optical(.72,.1)[1];b=optical(.72,1)[1]
  self.assertAlmostEqual(float(a),float(b))
 def test_main_reproducible(self):
  self.assertEqual(main_record(19),main_record(19))
 def test_fit_interval(self):
  a=fit(main_record(19),ref_counts(.1,1000,20))
  self.assertTrue(0<a['M_ci95'][0]<a['M_ci95'][1]<1)
 def test_oracle_fixed(self):
  a=fit(main_record(19),ref_counts(.1,1000,20),oracle_rho=.1)
  self.assertAlmostEqual(a['rho_mean'],.1)
 def test_wrong_rho_bias(self):
  obs=main_record(19)
  a=fit(obs,ref_counts(.1,1000,20),oracle_rho=1)
  b=fit(obs,ref_counts(.1,1000,20),oracle_rho=.1)
  self.assertGreater(b['M_mean']-a['M_mean'],.1)
 def test_paired_demo(self):
  x=paired_demo(n=2)
  self.assertEqual(x['ref_100']['n'],2)
  self.assertEqual(len(x),6)
if __name__=='__main__':unittest.main()
