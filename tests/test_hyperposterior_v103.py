"""v1.03 GitHub companion regression. The actual 38 locally passed tests
are included in photon_v103_complete.zip; this counterpart has 23 tests.
"""
import unittest
import numpy as np
from models.hyperposterior_v103 import (
 BOUNDS,sensor_log_posterior,hyper_mle,numerical_hessian,
 sample_hyper,calibrated_optical_grid,infer,audit)
from models.continuous_calibration_v102 import Setup,simulate,calibration_draws

class HyperTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=Setup();cls.rec=simulate(103007,cls.s)
 def test_baseline_sensor_shape(self):self.assertEqual(self.rec['y'].shape,(40,3))
 def test_initial_phase(self):self.assertEqual(self.rec['true_path'][0],0)
 def test_mle_shape(self):self.assertEqual(hyper_mle(self.rec).shape,(3,))
 def test_mle_bounded(self):
  x=hyper_mle(self.rec)
  self.assertTrue(np.all((x>BOUNDS[:,0])&(x<BOUNDS[:,1])))
 def test_prior_rejects(self):self.assertEqual(sensor_log_posterior([0,0,0],self.rec),-np.inf)
 def test_hessian_symmetric(self):
  a=numerical_hessian(hyper_mle(self.rec),self.rec)
  self.assertTrue(np.allclose(a,a.T))
 def test_sample_shapes(self):
  z=sample_hyper(self.rec,80,103)
  self.assertEqual(z['theta'].shape,(80,3))
 def test_ess(self):
  z=sample_hyper(self.rec,80,103)
  self.assertTrue(1<z['ess']<=80+1e-7)
 def test_sample_normalized(self):
  z=sample_hyper(self.rec,80,103)
  self.assertAlmostEqual(z['weights'].sum(),1)
 def test_sample_bounds(self):
  z=sample_hyper(self.rec,80,103)
  self.assertTrue(np.all((z['theta']>BOUNDS[:,0])&(z['theta']<BOUNDS[:,1])))
 def test_sample_reproducible(self):
  a=sample_hyper(self.rec,80,103);b=sample_hyper(self.rec,80,103)
  self.assertTrue(np.array_equal(a['theta'],b['theta']))
 def test_bad_sample_count(self):
  with self.assertRaises(ValueError):sample_hyper(self.rec,4,103)
 def test_sample_bad_scale(self):
  with self.assertRaises(ValueError):sample_hyper(self.rec,20,103,0)
 def test_true_mode(self):self.assertEqual(self.s.M,.72)

class OpticalTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=Setup();cls.rec=simulate(103008,cls.s)
  cls.particles=calibration_draws(cls.rec,cls.s,40,np.random.default_rng(1))
 def test_weights_not_normalized(self):
  with self.assertRaises(ValueError):
   calibrated_optical_grid(self.rec,self.s,np.full(40,.8),self.particles,np.ones(40))
 def test_valid_interval(self):
  z=calibrated_optical_grid(self.rec,self.s,np.full(40,.8),self.particles,np.ones(40)/40)
  self.assertTrue(0<z['ci95'][0]<z['ci95'][1]<1)
 def test_valid_mean(self):
  z=calibrated_optical_grid(self.rec,self.s,np.full(40,.8),self.particles,np.ones(40)/40)
  self.assertTrue(0<z['mean']<1)
 def test_importance_weights_affect(self):
  a=np.linspace(.5,.95,40)
  b=np.exp(np.linspace(-3,3,40));b/=b.sum()
  v=calibrated_optical_grid(self.rec,self.s,a,self.particles,np.ones(40)/40)
  w=calibrated_optical_grid(self.rec,self.s,a,self.particles,b)
  self.assertGreater(abs(v['mean']-w['mean']),1e-5)
 def test_infer_flags(self):
  a=infer(self.rec,self.s,draws=60,seed=19)
  self.assertTrue(a['hyper_uncertainty_integrated'] and a['calibration_nuisance_sampled'])
 def test_infer_reproducible(self):
  a=infer(self.rec,self.s,draws=60,seed=19)
  b=infer(self.rec,self.s,draws=60,seed=19)
  self.assertAlmostEqual(a['joint']['mean'],b['joint']['mean'])
 def test_infer_interval(self):
  a=infer(self.rec,self.s,draws=60,seed=19)
  self.assertTrue(0<a['joint']['ci95'][0]<a['joint']['ci95'][1]<1)
 def test_audit_smoke(self):
  a=audit(2,draws=40,seed=103000)
  self.assertEqual(len(a['rows']),2)
 def test_audit_ess(self):
  a=audit(2,draws=40,seed=103000)
  self.assertTrue(a['median_hyper_ess']>1)

if __name__=='__main__':unittest.main()
