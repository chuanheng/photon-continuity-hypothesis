"""v1.02 independently authored GitHub regression tests.
The 37 actually executed tests are from the local complete ZIP, not here.
"""
import unittest
from dataclasses import replace
import numpy as np
from models.continuous_calibration_v102 import (
 Setup,response_confusion,simulate,sensor_nll,fit_sensor,phase_draws,
 calibration_draws,forward,infer,jacobian,audit)
from models.mixed_hom_v094 import Config
from models.fock_calibration_v096 import fock_split

class CompanionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=Setup()
  cls.record=simulate(10201)
  cls.fit=infer(cls.record,draws=80,seed=111)
 def test_fock_triplet(self):self.assertTrue(np.allclose(fock_split(2,1),[.375,.125,.125,.375]))
 def test_confusion_identity(self):self.assertTrue(np.allclose(response_confusion(0,0),np.eye(5)))
 def test_confusion_rows(self):self.assertTrue(np.allclose(response_confusion().sum(axis=1),1))
 def test_confusion_triplet(self):self.assertAlmostEqual(response_confusion()[4,0],.2)
 def test_bad_confusion(self):
  with self.assertRaises(ValueError):response_confusion(.7)
 def test_source_counts(self):self.assertEqual(sum(self.record['source']),self.s.source_shots)
 def test_pnr_reference(self):self.assertEqual(sum(self.record['ref4']),self.s.pnr_standards)
 def test_sensor_shape(self):self.assertEqual(self.record['y'].shape,(40,3))
 def test_sensor_zero(self):self.assertEqual(len(self.record['z']),100)
 def test_simulate_reproducible(self):
  a=simulate(10201);self.assertTrue(np.array_equal(a['y'],self.record['y']))
 def test_optics_near_below_far(self):self.assertLess(forward(.72,.8,Config(),.065,.014)[0],forward(.72,.8,Config(),.065,.014)[1])
 def test_far_no_M_dependence(self):self.assertAlmostEqual(forward(.2,.8,Config(),.065,.014)[1],forward(.9,.8,Config(),.065,.014)[1])
 def test_hyper_bounds(self):
  h=fit_sensor(self.record['y'],self.record['z'])
  self.assertTrue(.03<h['walk_sd']<.2 and .1<h['read_sd']<.22)
 def test_bias_reasonable(self):self.assertLess(abs(self.fit['hyper_mle']['bias']-.015),.05)
 def test_nll_comparison(self):
  h=self.fit['hyper_mle'];x=[np.log(h['walk_sd']),np.log(h['read_sd']),h['bias']]
  self.assertLess(sensor_nll(x,self.record['y'],self.record['z']),
     sensor_nll([np.log(.4),np.log(.4),.2],self.record['y'],self.record['z']))
 def test_draw_positive_A(self):
  a=phase_draws(self.record['y'],self.fit['hyper_mle'],80,np.random.default_rng(1))
  self.assertTrue(np.all((a>0)&(a<=1)))
 def test_particles_count(self):
  a=calibration_draws(self.record,self.s,25,np.random.default_rng(2))
  self.assertEqual(len(a),25)
 def test_particles_physical(self):
  a=calibration_draws(self.record,self.s,25,np.random.default_rng(2))
  self.assertTrue(all(0<f<p.w11 and 0<q<1 for p,f,q in a))
 def test_posterior_ci(self):
  lo,hi=self.fit['posterior']['ci95'];self.assertTrue(0<lo<hi<1)
 def test_posterior_sensible(self):self.assertLess(abs(self.fit['posterior']['mean']-.72),.08)
 def test_hyper_not_integrated(self):self.assertFalse(self.fit['hyper_uncertainty_integrated'])
 def test_jacobian_shape(self):self.assertEqual(jacobian().shape,(2,5))
 def test_jacobian_rank(self):self.assertEqual(np.linalg.matrix_rank(jacobian()),2)
 def test_jacobian_null(self):
  j=jacobian();v=np.linalg.svd(j)[2][-1]
  self.assertLess(np.linalg.norm(j@v),1e-10)
 def test_small_audit(self):
  z=audit(outer=3,draws=40)
  self.assertEqual(len(z['rows']),3)
if __name__=='__main__':unittest.main()
