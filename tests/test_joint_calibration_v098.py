"""v0.98 GitHub companion regression (local ZIP has 34 actually executed tests)."""
import unittest
import numpy as np
from models.calibration_stress_v097 import CalibrationError,corrupted_record
from models.joint_calibration_v098 import (
 Budget,confusion,external_references,source_inverse,corrected_inference,
 one_trial,paired_audit
)
class Tests(unittest.TestCase):
 def test_confusion_identity(self):self.assertTrue(np.allclose(confusion(CalibrationError()),np.eye(5)))
 def test_confusion_stochastic(self):self.assertTrue(np.allclose(confusion(CalibrationError(pnr_triplet_to_pair=.3)).sum(axis=1),1))
 def test_confusion_probability(self):self.assertAlmostEqual(confusion(CalibrationError(pnr_triplet_to_pair=.3))[4,0],.3)
 def test_budget(self):self.assertEqual(Budget().reference_shots,13000)
 def test_invalid_budget(self):
  with self.assertRaises(ValueError):Budget(pnr_per_class=0).validate()
 def test_exact_inversion(self):
  c=confusion(CalibrationError(pnr_triplet_to_pair=.3))
  x=np.array([1000,200,300,400,100.])
  n=10000
  ref={'row0':(c[0]*n).tolist(),'row4':(c[4]*n).tolist(),'n':n}
  got,cond=source_inverse(x@c,ref)
  self.assertTrue(np.allclose(got,x))
 def test_singular_matrix(self):
  with self.assertRaises(ValueError):
   source_inverse([100,0,0,0,100],{'row0':[50,0,0,0,50],'row4':[50,0,0,0,50],'n':100})
 def test_negative_inverse(self):
  with self.assertRaises(ValueError):
   source_inverse([-1,0,0,0,100],{'row0':[100,0,0,0,0],'row4':[0,0,0,0,100],'n':100})
 def test_reference_pnr_counts(self):
  err=CalibrationError(.15,0,.3,0,-.004);r=corrupted_record(seed=9811,err=err)
  refs=external_references(r,err,Budget(),9814)
  self.assertEqual(sum(refs['row4']),1000)
 def test_reference_phase_shape(self):
  err=CalibrationError(.15,0,.3,0,-.004);r=corrupted_record(seed=9811,err=err)
  refs=external_references(r,err,Budget(),9814)
  self.assertEqual(np.asarray(refs['phase_observations']).shape,(40,4))
 def test_reference_reproducible(self):
  err=CalibrationError(.15,0,.3,0,-.004);r=corrupted_record(seed=9811,err=err)
  self.assertEqual(external_references(r,err,Budget(),9814),
                   external_references(r,err,Budget(),9814))
 def test_corrected_estimator(self):
  p=one_trial(seed=9811)
  self.assertTrue(np.isfinite(p['corrected_intrinsic']))
 def test_matched_main_seed(self):
  a=one_trial(seed=9811,budget=Budget(100,100,1,1000))
  b=one_trial(seed=9811,budget=Budget(10000,10000,20,100000))
  self.assertEqual(a['naive_intrinsic'],b['naive_intrinsic'])
 def test_paired_audit_shape(self):
  a=paired_audit(n=4,budgets=(100,1000))
  self.assertEqual(len(a['results']),2)
 def test_audit_invalid(self):
  with self.assertRaises(ValueError):paired_audit(n=1)
 def test_audit_30(self):
  a=paired_audit(n=30,budgets=(100,10000))
  self.assertTrue(a['results']['10000']['metrics']['corrected_intrinsic']['rmse']<.1)
if __name__=='__main__':unittest.main()
