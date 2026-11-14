"""v0.99 GitHub companion regression tests.
31/31 actually passed local tests are contained in the downloadable ZIP.
These independently authored tests are NOT claimed to have run in CI.
"""
import unittest
import numpy as np
from models.joint_uncertainty_v099 import (
 Design,fitted,replicate,joint_interval,one_dataset,audit)
from models.calibration_stress_v097 import corrupted_record,CalibrationError
from models.joint_calibration_v098 import external_references

class JointTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.error=CalibrationError(.15,0,.3,0,-.004)
  cls.rec=corrupted_record(seed=99101,err=cls.error)
  cls.ref=external_references(cls.rec,cls.error,Design(1000,2).budget(),99104)
 def test_budget(self):self.assertEqual(Design(1000,2).shots,13000)
 def test_repeat_budget(self):self.assertEqual(Design(10000,20).budget().phase_repeats,20)
 def test_source_fit(self):self.assertAlmostEqual(sum(fitted(self.rec,self.ref)['w']),1)
 def test_positive_noise(self):self.assertGreater(fitted(self.rec,self.ref)['phase_sd'],0)
 def test_phase_blocks(self):self.assertEqual(len(fitted(self.rec,self.ref)['phase']),40)
 def test_replication_reproducible(self):
  a,b=replicate(self.rec,self.ref,9,1000)
  c,d=replicate(self.rec,self.ref,9,1000)
  self.assertEqual(a,c);self.assertEqual(b,d)
 def test_replication_source_conserved(self):
  a,b=replicate(self.rec,self.ref,9,1000)
  self.assertEqual(sum(a['source_counts']),a['source_trials'])
 def test_replication_PNR_standard(self):
  a,b=replicate(self.rec,self.ref,9,1000)
  self.assertEqual(sum(b['row4']),b['n'])
 def test_replication_phase(self):
  a,b=replicate(self.rec,self.ref,9,1000)
  self.assertEqual(np.asarray(b['phase_observations']).shape,(40,2))
 def test_replication_online(self):
  a,b=replicate(self.rec,self.ref,9,1000)
  self.assertTrue(0<=b['online_count']<=b['online_trials'])
 def test_interval_shape(self):
  a=joint_interval(self.rec,self.ref,20,seed=999,nphase=1000)
  self.assertEqual(len(a['intrinsic_ci']),2)
 def test_interval_positive_width(self):
  a=joint_interval(self.rec,self.ref,20,seed=999,nphase=1000)
  self.assertGreater(a['intrinsic_ci'][1],a['intrinsic_ci'][0])
 def test_interval_counts(self):
  a=joint_interval(self.rec,self.ref,20,seed=999,nphase=1000)
  self.assertEqual(a['valid']+a['invalid'],20)
 def test_interval_reject_small(self):
  with self.assertRaises(ValueError):joint_interval(self.rec,self.ref,B=5)
 def test_one_dataset_truth(self):
  a=one_dataset(n=1000,B=20,seed=99101)
  self.assertEqual(a['intrinsic_truth'],.72)
 def test_small_audit(self):
  a=audit(outer=3,B=20,budgets=(100,))
  self.assertEqual(a['budgets']['100']['outer_valid']+a['budgets']['100']['outer_invalid'],3)
 def test_audit_bad_outer(self):
  with self.assertRaises(ValueError):audit(outer=1,B=20)
 def test_not_full_latent_model(self):
  a=joint_interval(self.rec,self.ref,20,seed=999,nphase=1000)
  self.assertTrue(a['fixed_plugin_true_phase'])
if __name__=='__main__':unittest.main()
