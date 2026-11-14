"""Independent GitHub v1.04 companion test cases.
The 34/34 actually executed tests are in the downloadable exact local ZIP.
"""
import unittest
import numpy as np
from models.validation_v104 import posterior_optical,exact_submodel_sbc,heldout_predictive,ppc_audit,proposal_audit
from models.continuous_calibration_v102 import simulate,Setup
class RestrictedSBC(unittest.TestCase):
 def test_posterior_norm(self):
  a,w,q=posterior_optical(50);self.assertAlmostEqual(w.sum(),1)
 def test_grid(self):
  a,w,q=posterior_optical(50);self.assertEqual(len(a),801)
 def test_quantiles(self):
  a,w,q=posterior_optical(50);self.assertTrue(0<q[0]<q[1]<q[2]<1)
 def test_count_ordering(self):
  g,a,q=posterior_optical(40);g,b,q=posterior_optical(80)
  self.assertGreater(g@a,g@b)
 def test_bad_count(self):
  with self.assertRaises(ValueError):posterior_optical(-1)
 def test_sbc_reproducible(self):
  a=exact_submodel_sbc(30,49,3);b=exact_submodel_sbc(30,49,3)
  self.assertEqual(a['ranks'],b['ranks'])
 def test_sbc_rank_range(self):
  a=exact_submodel_sbc(30,49,3);self.assertTrue(all(0<=v<=49 for v in a['ranks']))
 def test_sbc_hist_count(self):
  a=exact_submodel_sbc(30,49,3);self.assertEqual(sum(a['rank_histogram']),30)
 def test_sbc_probability(self):
  a=exact_submodel_sbc(30,49,3);self.assertTrue(0<=a['rank_uniformity_p']<=1)
 def test_sbc_bad_draws(self):
  with self.assertRaises(ValueError):exact_submodel_sbc(30,3,3)
class PredictiveChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rec=simulate(1041,Setup())
 def test_holdout_count(self):
  a=heldout_predictive(self.rec,draws=20,reps=30)
  self.assertEqual(a['n_holdout'],30)
 def test_holdout_p_range(self):
  a=heldout_predictive(self.rec,draws=20,reps=30)
  self.assertTrue(0<=a['predictive_probability_ge_observed']<=1)
 def test_holdout_repeatable(self):
  a=heldout_predictive(self.rec,seed=3,draws=20,reps=30)
  b=heldout_predictive(self.rec,seed=3,draws=20,reps=30)
  self.assertEqual(a,b)
 def test_heldout_bad(self):
  with self.assertRaises(ValueError):heldout_predictive(self.rec,ntrain=100)
 def test_extreme_holdout(self):
  a=heldout_predictive(self.rec,seed=3,draws=30,reps=60)
  r=dict(self.rec);z=self.rec['z'].copy();z[70:]+=10;r['z']=z
  b=heldout_predictive(r,seed=3,draws=30,reps=60)
  self.assertLess(b['predictive_probability_ge_observed'],a['predictive_probability_ge_observed'])
 def test_ppc_scenarios(self):
  z=ppc_audit(3,seed=3);self.assertEqual(len(z),2)
 def test_ppc_inputs(self):
  with self.assertRaises(ValueError):ppc_audit(0)
class ProposalDiagnostics(unittest.TestCase):
 def test_sensitivity(self):
  a=proposal_audit(2,draws=20,seed=4,scales=(.8,1.4))
  self.assertEqual(len(a['rows']),2)
 def test_sensitivity_ess_bounds(self):
  a=proposal_audit(2,draws=20,seed=4,scales=(.8,1.4))
  self.assertTrue(all(0<v['min_ESS']<=20 for v in a['summary'].values()))
 def test_scale_not_full_SBC(self):
  a=proposal_audit(2,draws=20,seed=4,scales=(.8,1.4))
  self.assertEqual(a['n'],2)
if __name__=='__main__':unittest.main()
