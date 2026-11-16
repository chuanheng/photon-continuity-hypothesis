"""v0.96 independent GitHub regression tests; full tested 44 cases in ZIP."""
import unittest
import numpy as np
from models.mixed_hom_v094 import Config
from models.fock_calibration_v096 import *

class Fock(unittest.TestCase):
 def test_vacuum(self):self.assertTrue(np.allclose(fock_split(0,0),[1]))
 def test_one(self):self.assertTrue(np.allclose(fock_split(1,0),[.5,.5]))
 def test_HOM_11(self):self.assertTrue(np.allclose(fock_split(1,1),[.5,0,.5]))
 def test_two_same_input(self):self.assertTrue(np.allclose(fock_split(2,0),[.25,.5,.25]))
 def test_21(self):self.assertTrue(np.allclose(fock_split(2,1),[3/8,1/8,1/8,3/8]))
 def test_12(self):self.assertTrue(np.allclose(fock_split(1,2),[3/8,1/8,1/8,3/8]))
 def test_30(self):self.assertTrue(np.allclose(fock_split(3,0),[1/8,3/8,3/8,1/8]))
 def test_generic_four(self):self.assertAlmostEqual(fock_split(2,2).sum(),1)
 def test_generic_eight(self):self.assertAlmostEqual(fock_split(4,4).sum(),1)
 def test_invalid_fock(self):
  with self.assertRaises(ValueError):fock_split(-1,2)
 def test_triplet_lossless(self):
  p=Config(eta_a=1,eta_b=1,dark_a=0,dark_b=0)
  self.assertAlmostEqual(triple_click(p,True),.25)
  self.assertAlmostEqual(triple_click(p,False),.75)
 def test_click_three(self):self.assertEqual(n_click(3,1,0),1)
 def test_two_different_distributions(self):
  self.assertGreater(np.linalg.norm(fock_split(2,1)-distinguishable_split_three()),.3)
 def test_triplet_detector_realistic(self):self.assertLess(triple_click(Config(),True),triple_click(Config(),False))

class Identification(unittest.TestCase):
 def setUp(self):self.r=synthetic_record(seed=9601)
 def test_record_reproducible(self):self.assertEqual(self.r,synthetic_record(seed=9601))
 def test_40_phase_blocks(self):self.assertEqual(len(self.r['phase_monitor']),40)
 def test_source_class_sum(self):self.assertEqual(sum(self.r['source_counts']),self.r['source_trials'])
 def test_true_phase_averaging(self):self.assertAlmostEqual(self.r['true_mean'],.5566398361798411)
 def test_calibration_mean(self):self.assertLess(abs(infer(self.r)['mean_overlap']-self.r['true_mean']),.05)
 def test_calibration_intrinsic(self):self.assertLess(abs(infer(self.r)['intrinsic_overlap']-.72),.06)
 def test_naive_bias(self):self.assertLess(naive_old_estimator(self.r),infer(self.r)['intrinsic_overlap'])
 def test_sensor_relation(self):
  e=infer(self.r)
  self.assertAlmostEqual(e['mean_overlap'],e['intrinsic_overlap']*e['drift_factor'])
 def test_monitored_q(self):self.assertLess(abs(infer(self.r)['online_click']-.014),.007)
 def test_monitored_triplets(self):self.assertLess(abs(infer(self.r)['triplet']-.065),.006)
 def test_identification_rank(self):self.assertEqual(np.linalg.matrix_rank(optical_jacobian()),2)
 def test_identification_null_direction(self):
  j=optical_jacobian();v=np.linalg.svd(j)[2][-1]
  self.assertLess(np.linalg.norm(j@v),1e-9)
 def test_bootstrap(self):
  x=parametric_bootstrap(self.r,24,seed=9602)
  self.assertTrue(x['intrinsic_ci'][0]<.72<x['intrinsic_ci'][1])
  self.assertTrue(x['conditioned_exact_phase_monitor'])
 def test_bootstrap_invalid(self):
  with self.assertRaises(ValueError):parametric_bootstrap(self.r,3)
 def test_background_increases_probability(self):
  p=Config()
  self.assertTrue(np.all(optical_probs(p,.065,.014,.55)>optical_probs(p,.065,0,.55)))
 def test_physical_probability(self):
  x=optical_probs(Config(),.065,.014,.55)
  self.assertTrue(np.all((x>0)&(x<1)))
 def test_bad_fraction(self):
  with self.assertRaises(ValueError):optical_probs(Config(),1,0,.5)
if __name__=='__main__':unittest.main()
