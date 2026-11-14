"""v1.01 GitHub companion regression (locally tested 38-case suite in ZIP)."""
import unittest
import numpy as np
from models.hierarchical_v101 import (
 HyperGrid,generate,hyperposterior,path_draws,optical_posterior,infer,audit)
from models.latent_phase_v100 import default_setup
class BayesianHOM(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=generate(10131,2)
  cls.fit=infer(cls.r,draws=300,seed=51)
 def test_hyper_count(self):self.assertEqual(len(HyperGrid().combinations()),27)
 def test_true_hyper_on_grid(self):self.assertIn((.095,.15,0.),HyperGrid().combinations())
 def test_generate_sensor_shape(self):self.assertEqual(self.r['y'].shape,(40,2))
 def test_zero_reference(self):self.assertEqual(len(self.r['zero']),80)
 def test_true_initial_zero(self):self.assertAlmostEqual(self.r['true_path'][0],0)
 def test_optical_count(self):self.assertTrue(0<=self.r['count']<=self.r['shots'])
 def test_control_count(self):self.assertTrue(0<self.r['control0']<self.r['controls'])
 def test_control_probabilities(self):
  s=default_setup()
  self.assertTrue(0<s.intercept-s.slope<s.intercept<1)
 def test_reproducible(self):
  a=generate(77,2);b=generate(77,2)
  self.assertEqual(a['count'],b['count'])
  self.assertTrue(np.array_equal(a['y'],b['y']))
 def test_bad_repeats(self):
  with self.assertRaises(ValueError):generate(77,0)
 def test_hyper_weights(self):
  m,w=hyperposterior(self.r)
  self.assertEqual(len(m),27)
  self.assertAlmostEqual(np.sum(w),1,places=10)
 def test_hyper_support(self):
  m,w=hyperposterior(self.r)
  self.assertTrue(np.all(w>=0))
 def test_bad_sensor_shape(self):
  r=dict(self.r);r['y']=np.ones((2,2))
  with self.assertRaises(ValueError):hyperposterior(r)
 def test_gaussian_precision(self):
  m,w=hyperposterior(self.r)
  self.assertTrue(all(np.all(np.diag(v[4])>0) for v in m))
 def test_sample_attenuation(self):
  m,w=hyperposterior(self.r)
  a,h=path_draws(m,w,100,80)
  self.assertTrue(np.all((a>0)&(a<=1)))
  self.assertEqual(h.shape,(100,3))
 def test_sample_reproducibility(self):
  m,w=hyperposterior(self.r)
  a=path_draws(m,w,100,80)
  b=path_draws(m,w,100,80)
  self.assertTrue(np.array_equal(a[0],b[0]))
 def test_bad_sample_count(self):
  m,w=hyperposterior(self.r)
  with self.assertRaises(ValueError):path_draws(m,w,5,80)
 def test_posterior_grid(self):
  s=default_setup()
  r=optical_posterior(self.r,np.full(100,.8),np.full(100,s.intercept),
                      np.full(100,s.intercept-s.slope))
  self.assertTrue(0<r['ci95'][0]<r['ci95'][1]<1)
 def test_joint_interval(self):
  p=self.fit['joint']
  self.assertTrue(0<p['ci95'][0]<p['ci95'][1]<1)
 def test_plugin_interval(self):
  p=self.fit['plugin']
  self.assertTrue(0<p['ci95'][0]<p['ci95'][1]<1)
 def test_hyper_means(self):
  w,s,b=self.fit['hyper_mean']
  self.assertTrue(.065<=w<=.125 and .11<=s<=.19 and -.04<=b<=.04)
 def test_joint_sensible(self):self.assertLess(abs(self.fit['joint']['mean']-.72),.15)
 def test_audit_schema(self):
  a=audit(outer=3,repeats=(1,),draws=70)
  self.assertEqual(len(a['results']['1']['rows']),3)
 def test_audit_invalid(self):
  with self.assertRaises(ValueError):audit(outer=1)
if __name__=='__main__':unittest.main()
