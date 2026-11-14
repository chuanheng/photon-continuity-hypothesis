"""v1.00 companion regression tests. Actual complete 27-test local suite is in ZIP.
No claim that this separately authored GitHub suite has passed CI.
"""
import unittest
import numpy as np
from models.latent_phase_v100 import (Setup,default_setup,optical_calibration,
  generate,smooth,sample_paths,attenuation,posterior_grid,infer,audit)
class LatentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=default_setup();cls.r=generate(1001,2,cls.s)
 def test_calibration(self):self.assertTrue(0<self.s.intercept-self.s.slope<self.s.intercept<1)
 def test_invalid_setup(self):
  with self.assertRaises(ValueError):Setup(intercept=.1,slope=.2)
 def test_generation_seed(self):self.assertTrue(np.array_equal(self.r['true_u'],generate(1001,2,self.s)['true_u']))
 def test_initial_phase(self):self.assertEqual(self.r['true_u'][0],0)
 def test_y_shape(self):self.assertEqual(self.r['y'].shape,(40,2))
 def test_count_range(self):self.assertTrue(0<=self.r['near_count']<=self.s.near_shots)
 def test_A_bounds(self):self.assertTrue(0<self.r['A_true']<=1)
 def test_invalid_repeats(self):
  with self.assertRaises(ValueError):generate(1,0,self.s)
 def test_smoother_boundary(self):
  m=smooth(self.r['y'],self.s)
  self.assertEqual(m['mean'][0],0);self.assertEqual(m['variance'][0],0)
 def test_smoother_spd(self):
  self.assertGreater(np.linalg.eigvalsh(smooth(self.r['y'],self.s)['cov_unknown']).min(),0)
 def test_smoother_shape(self):
  with self.assertRaises(ValueError):smooth(np.zeros((4,4)),self.s)
 def test_more_reads_less_uncertainty(self):
  a=smooth(generate(44,1,self.s)['y'],self.s)
  b=smooth(generate(44,20,self.s)['y'],self.s)
  self.assertLess(np.mean(b['variance'][1:]),np.mean(a['variance'][1:]))
 def test_sample_shape(self):self.assertEqual(sample_paths(smooth(self.r['y'],self.s),100,9).shape,(100,40))
 def test_sample_initial(self):self.assertTrue(np.all(sample_paths(smooth(self.r['y'],self.s),100,9)[:,0]==0))
 def test_sample_reproducible(self):
  a=smooth(self.r['y'],self.s)
  self.assertTrue(np.array_equal(sample_paths(a,100,9),sample_paths(a,100,9)))
 def test_sample_variance(self):
  m=smooth(self.r['y'],self.s);v=sample_paths(m,8000,11)
  self.assertAlmostEqual(np.var(v[:,15],ddof=1),m['variance'][15],delta=.0002)
 def test_attenuation_zero(self):self.assertAlmostEqual(attenuation(np.zeros((3,40))).mean(),1)
 def test_attenuation_positive(self):
  a=sample_paths(smooth(self.r['y'],self.s),100,9)
  self.assertTrue(np.all(attenuation(a)>0))
 def test_posterior_normalized(self):
  p=posterior_grid(self.r['near_count'],self.s.near_shots,np.ones(80)*.8,self.s)
  self.assertAlmostEqual(sum(p['weight']),1)
 def test_credible_interval_bounds(self):
  p=posterior_grid(self.r['near_count'],self.s.near_shots,np.ones(80)*.8,self.s)
  self.assertTrue(0<p['ci95'][0]<p['ci95'][1]<1)
 def test_latent_wider(self):
  p=infer(self.r,self.s,draws=400,seed=8)
  a,b=p['plugin']['ci95'],p['latent']['ci95']
  self.assertGreater(b[1]-b[0],a[1]-a[0])
 def test_audit_small(self):
  a=audit(outer=2,repeats=(1,),draws=60)
  self.assertEqual(a['results']['1']['runs'],2)
if __name__=='__main__':unittest.main()
