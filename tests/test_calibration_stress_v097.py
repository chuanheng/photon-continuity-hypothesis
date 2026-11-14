"""v0.97 GitHub counterpart tests; the 44 actually passed local tests
are in photon_v097_complete.zip. Not yet verified in GitHub CI.
"""
import unittest
import numpy as np
from models.calibration_stress_v097 import (
 CalibrationError,SCENARIOS,pnr_confusion_matrix,corrupted_record,
 population_limit,evaluate)

class TestCalibration(unittest.TestCase):
 def test_scenarios(self):self.assertEqual(len(SCENARIOS),8)
 def test_identity_confusion(self):
  self.assertTrue(np.allclose(pnr_confusion_matrix(),np.eye(5)))
 def test_confusion_rows_sum(self):
  c=pnr_confusion_matrix(CalibrationError(pnr_triplet_to_pair=.3))
  self.assertTrue(np.allclose(c.sum(axis=1),1))
 def test_triplet_to_pair(self):
  self.assertAlmostEqual(pnr_confusion_matrix(CalibrationError(pnr_triplet_to_pair=.3))[4,0],.3)
 def test_pair_to_triplet(self):
  self.assertAlmostEqual(pnr_confusion_matrix(CalibrationError(pnr_pair_to_triplet=.05))[0,4],.05)
 def test_bad_noise(self):
  with self.assertRaises(ValueError):CalibrationError(phase_noise_sd=-.1).validate()
 def test_bad_confusion(self):
  with self.assertRaises(ValueError):CalibrationError(pnr_pair_to_triplet=2).validate()
 def test_bad_q_ref(self):
  with self.assertRaises(ValueError):corrupted_record(err=CalibrationError(q_monitor_offset=-.1))
 def test_base_record(self):
  r=corrupted_record(seed=9705)
  self.assertEqual(sum(r['source_counts']),r['source_trials'])
 def test_reproducible(self):
  self.assertEqual(corrupted_record(seed=9705),corrupted_record(seed=9705))
 def test_phase_truth(self):
  r=corrupted_record(seed=9705)
  self.assertTrue(np.allclose(r['true_phase'],r['phase_monitor']))
 def test_phase_noise(self):
  r=corrupted_record(seed=9705,err=CalibrationError(phase_noise_sd=.15))
  self.assertGreater(np.linalg.norm(np.array(r['true_phase'])-r['phase_monitor']),.1)
 def test_phase_bias(self):
  r=corrupted_record(seed=9705,err=CalibrationError(phase_bias=.1))
  self.assertTrue(np.allclose(np.array(r['phase_monitor'])-r['true_phase'],.1))
 def test_record_truth_unchanged(self):
  a=corrupted_record(seed=9705)
  b=corrupted_record(seed=9705,err=CalibrationError(pnr_triplet_to_pair=.3))
  self.assertEqual(a['near'],b['near'])
  self.assertEqual(a['far'],b['far'])
 def test_misclassified_triplets(self):
  a=corrupted_record(seed=9705)
  b=corrupted_record(seed=9705,err=CalibrationError(pnr_triplet_to_pair=.3))
  self.assertLess(b['source_counts'][-1],a['source_counts'][-1])
 def test_infinite_calibration_exact(self):
  self.assertAlmostEqual(population_limit()['estimated_intrinsic'],.72,places=11)
 def test_pnr_misclassification_bias(self):
  self.assertGreater(population_limit(CalibrationError(pnr_triplet_to_pair=.3))['estimated_intrinsic'],.72)
 def test_monitor_mismatch_sign(self):
  low=population_limit(CalibrationError(q_monitor_offset=-.004))
  high=population_limit(CalibrationError(q_monitor_offset=.004))
  self.assertLess(low['estimated_intrinsic'],high['estimated_intrinsic'])
 def test_phase_noise_targets_intrinsic(self):
  x=population_limit(CalibrationError(phase_noise_sd=.15))
  self.assertAlmostEqual(x['bias_mean'],0,places=9)
 def test_small_bootstrap(self):
  x=evaluate(outer=2,B=20,seed=9705)
  self.assertEqual(len(x['rows']),2)
 def test_bad_outer(self):
  with self.assertRaises(ValueError):evaluate(outer=0,B=20)
 def test_bad_bootstrap(self):
  with self.assertRaises(ValueError):evaluate(outer=2,B=3)
if __name__=='__main__':unittest.main()
