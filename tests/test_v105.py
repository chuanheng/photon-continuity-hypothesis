"""v1.05 independent GitHub regression suite.
Actual 40 successful local tests are preserved in photon_v105_complete.zip.
"""
import unittest
import numpy as np
from models.full_sbc_v105 import (HYPER,generate,conditional_phase,calibrate,
    infer,clicks,ranks,audit,M,R)
from models.robust_sensor_v105 import (sensor_data,fit_predict,audit as sensor_audit)

class Optics(unittest.TestCase):
 def test_ideal_HOM_dip(self):
  a=clicks(.1,.8,.05,.01,.75,.7,.001,.002)[0]
  b=clicks(.9,.8,.05,.01,.75,.7,.001,.002)[0]
  self.assertGreater(a,b)
 def test_far_independent_of_overlap(self):
  a=clicks(.1,.8,.05,.01,.75,.7,.001,.002)[1]
  b=clicks(.9,.8,.05,.01,.75,.7,.001,.002)[1]
  self.assertAlmostEqual(a,b)
 def test_extra_correlated_clicks(self):
  a=clicks(.5,.8,.05,0,.75,.7,.001,.002)[0]
  b=clicks(.5,.8,.05,.1,.75,.7,.001,.002)[0]
  self.assertGreater(b,a)
 def test_optical_bounds(self):
  a,b=clicks(np.linspace(.01,.99,40),1,.05,.01,.75,.7,.001,.002)
  self.assertTrue(np.all((a>0)&(a<1)))
  self.assertTrue(np.all((b>0)&(b<1)))
 def test_vectorized(self):
  x,y=clicks(np.array([.1,.5]),1,.05,.01,.75,.7,.001,.002)
  self.assertEqual(x.shape,(2,));self.assertEqual(y.shape,(2,))

class PriorSBC(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record,cls.truth=generate(10577)
  cls.fit=infer(cls.record,n=700,draws=49,seed=10578)
 def test_generated_true_M(self):self.assertTrue(0<self.truth['M']<1)
 def test_generated_prior_r(self):self.assertTrue(0<self.truth['r']<1)
 def test_generated_sensor_shape(self):self.assertEqual(self.record['y'].shape,(24,2))
 def test_generate_reproducible(self):
  a,b=generate(10577)
  self.assertEqual(a['near'],self.record['near'])
  self.assertAlmostEqual(b['M'],self.truth['M'])
 def test_sensor_posterior_normalized(self):
  hp,_=conditional_phase(self.record)
  self.assertAlmostEqual(np.sum(hp),1)
 def test_hyper_count(self):self.assertEqual(len(HYPER),27)
 def test_source_grid_count(self):self.assertEqual(len(R),151)
 def test_overlap_grid_count(self):self.assertEqual(len(M),161)
 def test_calibration_draws_shape(self):
  q,e=calibrate(self.record,150,np.random.default_rng(3))
  self.assertEqual(len(e),150)
  self.assertTrue(np.all((q['r']>0)&(q['r']<1)))
 def test_importance_ess(self):
  self.assertTrue(1<self.fit['ess']<=700)
 def test_credible_interval(self):
  lo,hi=self.fit['M95']
  self.assertTrue(0<lo<hi<1)
 def test_posterior_sample_shape(self):
  self.assertEqual(len(self.fit['draws']['M']),49)
 def test_reproducible_posterior(self):
  v=infer(self.record,n=700,draws=49,seed=10578)
  self.assertEqual(self.fit['Mmean'],v['Mmean'])
 def test_rank_range(self):
  g=np.random.default_rng(9)
  d=ranks(self.truth,self.fit['draws'],g)
  self.assertEqual(len(d),12)
  self.assertTrue(all(0<=v<=49 for v in d.values()))
 def test_prior_sbc_smoke(self):
  a=audit(n=6,particles=350,draws=19,seed=8)
  self.assertEqual(len(a['ranks']['M']),6)
  self.assertEqual(len(a['rank_tests']),12)

class SensorValidation(unittest.TestCase):
 def test_clean_flags(self):
  a,b,c,d=sensor_data(5,contamination=0)
  self.assertEqual(c.sum()+d.sum(),0)
 def test_contamination_in_both(self):
  a,b,c,d=sensor_data(5,contamination=.2)
  self.assertGreater(c.sum(),0);self.assertGreater(d.sum(),0)
 def test_seed_repeat(self):
  a=sensor_data(5);b=sensor_data(5)
  self.assertTrue(np.array_equal(a[0],b[0]))
 def test_score_finite(self):
  a,b,_,_=sensor_data(5)
  q=fit_predict(a,b)
  self.assertTrue(np.isfinite(q['student_minus_normal']))
 def test_outlier_student_better(self):
  a,b,_,_=sensor_data(5)
  a=a.copy();b=b.copy();a[0]=4;b[0]=4
  self.assertGreater(fit_predict(a,b)['student_minus_normal'],0)
 def test_robust_audit_small(self):
  z=sensor_audit(3)
  self.assertEqual(z['0.08']['n'],3)
 def test_training_short(self):
  with self.assertRaises(ValueError):fit_predict([1,2],[1,2,3,4,5])
if __name__=='__main__':unittest.main()
