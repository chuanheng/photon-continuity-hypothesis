"""v0.95 GitHub counterpart regression: 24 lightweight tests.
The actual locally executed full package has 30/30 passing tests.
"""
import unittest
import numpy as np
from models.mixed_hom_v094 import Config,estimate_records,parametric_bootstrap
from models.robustness_v095 import (Stress,triplet_coincidence,correlated_click,
    drifted_overlap,stressed_probabilities,simulate_stressed,audit_one,audit_all)
class TestPhysics(unittest.TestCase):
 def setUp(self):self.p=Config()
 def test_base_near(self):
  a,b=stressed_probabilities(self.p,Stress(),[.72]*40)
  self.assertAlmostEqual(a[0],.08557754880720003)
 def test_base_far(self):
  a,b=stressed_probabilities(self.p,Stress(),[.72]*40)
  self.assertAlmostEqual(b,.24821511250800002)
 def test_noise_adds(self):self.assertAlmostEqual(correlated_click(.2,.1),.28)
 def test_triplet_bounded(self):self.assertTrue(0<triplet_coincidence(self.p)<1)
 def test_noise_near(self):
  a,b=stressed_probabilities(self.p,Stress(correlated_live_click=.014),[.72]*40)
  self.assertGreater(a[0],.08557754880720003)
 def test_triplet_near(self):
  a,b=stressed_probabilities(self.p,Stress(triple_fraction=.065),[.72]*40)
  self.assertGreater(a[0],.08557754880720003)
 def test_negative_click_rejected(self):
  with self.assertRaises(ValueError):Stress(correlated_live_click=-1).validate()
 def test_large_triplet_rejected(self):
  with self.assertRaises(ValueError):Stress(triple_fraction=.9).validate()
 def test_negative_drift_rejected(self):
  with self.assertRaises(ValueError):Stress(mode_random_walk_step=-.1).validate()
 def test_invalid_modes_rejected(self):
  with self.assertRaises(ValueError):stressed_probabilities(self.p,Stress(),[.5,1.5])
 def test_low_pair_fraction_rejected(self):
  from dataclasses import replace
  with self.assertRaises(ValueError):
   stressed_probabilities(replace(self.p,w11=.01),Stress(triple_fraction=.06),[.5,.5])
 def test_zero_drift(self):
  self.assertTrue(np.allclose(drifted_overlap(self.p,0,np.random.default_rng(5)),.72))
 def test_random_walk_bounded(self):
  x=drifted_overlap(self.p,.1,np.random.default_rng(5))
  self.assertTrue(np.all((x>0)&(x<=.72)))
 def test_random_walk_repeated(self):
  self.assertTrue(np.array_equal(drifted_overlap(self.p,.1,np.random.default_rng(5)),drifted_overlap(self.p,.1,np.random.default_rng(5))))
class TestStatistics(unittest.TestCase):
 def setUp(self):self.p=Config()
 def test_synthetic_record(self):
  r=simulate_stressed(self.p,Stress(),seed=5)
  self.assertTrue(0<=r['near']<=r['shots'])
 def test_synthetic_reproducible(self):
  self.assertEqual(simulate_stressed(self.p,Stress(),seed=5),simulate_stressed(self.p,Stress(),seed=5))
 def test_source_calibrations_normalized(self):
  r=simulate_stressed(self.p,Stress(),seed=5)
  self.assertEqual(sum(r['source_counts']),r['source_trials'])
 def test_misspecification_blind_calibration(self):
  a=simulate_stressed(self.p,Stress(),seed=5)
  b=simulate_stressed(self.p,Stress(.014,.065,.095),seed=5)
  self.assertEqual(a['source_counts'],b['source_counts'])
  self.assertEqual(a['dark_counts'],b['dark_counts'])
 def test_estimator_exists(self):
  e=estimate_records(simulate_stressed(self.p,Stress(),seed=5))
  self.assertTrue(np.isfinite(e['overlap']))
 def test_bootstrap_refit(self):
  a=simulate_stressed(self.p,Stress(),seed=5)
  b=parametric_bootstrap(a,replications=20,seed=5)
  self.assertTrue(b['refitted_calibrations_each_replication'])
 def test_bias_direction_combined(self):
  a=simulate_stressed(self.p,Stress(.014,.065,.095),seed=17)
  self.assertLess(estimate_records(a)['overlap'],.72)
 def test_stress_changes_mode_estimand(self):
  a=simulate_stressed(self.p,Stress(mode_random_walk_step=.095),seed=17)
  self.assertLess(a['true_mean_mode_overlap'],.72)
 def test_audit_small(self):
  a=audit_one(Stress(),outer=3,inner=20,seed=5)
  self.assertEqual(len(a['rows']),3)
 def test_audit_size_rejected(self):
  with self.assertRaises(ValueError):audit_one(Stress(),outer=0,inner=20)
if __name__=='__main__':unittest.main()
