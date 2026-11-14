"""v1.06 GitHub companion regression checks.
The 43 tests actually executed are in photon_v106_complete.zip.
No remote CI success is claimed.
"""
import unittest
import numpy as np
from models.continuous_partial_v106 import (
    FULL,DIST,LO,HI,Setting,triplet_probabilities,optical,make_record,
    sensor_loglike,phase_posterior_sample,hyper_samples,infer,small_audit)

class ThreeBosonPhysics(unittest.TestCase):
    def test_full_bosonic(self):
        self.assertTrue(np.allclose(triplet_probabilities(1),[.375,.125,.125,.375]))
    def test_distinguishable(self):
        self.assertTrue(np.allclose(triplet_probabilities(0),[.125,.375,.375,.125]))
    def test_halfway(self):
        self.assertTrue(np.allclose(triplet_probabilities(.5),[.25,.25,.25,.25]))
    def test_normalization(self):
        for rho in np.linspace(0,1,11):
            self.assertAlmostEqual(sum(triplet_probabilities(rho)),1)
    def test_invalid_rho(self):
        with self.assertRaises(ValueError):triplet_probabilities(2)
    def test_near_rho_effect(self):
        a,b=optical(.72,.8,.14,.014,.74,.68,.002,.003,1)
        c,d=optical(.72,.8,.14,.014,.74,.68,.002,.003,0)
        self.assertLess(float(a),float(c))
        self.assertAlmostEqual(float(b),float(d))
    def test_far_mode_invariant(self):
        a=optical(.1,.5,.14,.014,.74,.68,.002,.003,.5)[1]
        b=optical(.9,.9,.14,.014,.74,.68,.002,.003,.5)[1]
        self.assertAlmostEqual(float(a),float(b))
    def test_local_nonidentifiability(self):
        def f(m,r):return np.array(optical(m,.8,.14,.014,.74,.68,.002,.003,r),float).reshape(2)
        h=1e-5
        J=np.column_stack(((f(.72+h,.4)-f(.72-h,.4))/(2*h),
                           (f(.72,.4+h)-f(.72,.4-h))/(2*h)))
        self.assertEqual(np.linalg.matrix_rank(J),1)

class ContinuousSensor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.record,cls.truth=make_record(seed=10601)
    def test_shape(self):self.assertEqual(self.record['y'].shape,(24,2))
    def test_zero_shape(self):self.assertEqual(self.record['zero'].shape,(40,))
    def test_attenuation_bounds(self):self.assertTrue(0<self.truth['A']<=1)
    def test_exact_initial_phase(self):self.assertEqual(self.truth['M'],.72)
    def test_reproducible_data(self):
        a,b=make_record(seed=10601)
        self.assertTrue(np.array_equal(a['y'],self.record['y']))
    def test_loglike_finite(self):
        x=np.array([np.log(.095),np.log(.15),.015])
        self.assertTrue(np.isfinite(sensor_loglike(x,self.record['y'],self.record['zero'])))
    def test_prior_rejects_outside(self):
        self.assertEqual(sensor_loglike(LO-1,self.record['y'],self.record['zero']),-np.inf)
    def test_hyperposterior_normalized(self):
        a,w,ess=hyper_samples(self.record,60,seed=9)
        self.assertAlmostEqual(float(sum(w)),1)
        self.assertTrue(1<ess<=60+1e-7)
    def test_hyperposterior_in_support(self):
        a,w,ess=hyper_samples(self.record,60,seed=9)
        self.assertTrue(np.all((a>LO)&(a<HI)))
    def test_phase_attenuation_sampled(self):
        t=np.array([np.log(.095),np.log(.15),.015])
        v=phase_posterior_sample(self.record['y'],t,np.random.default_rng(1))
        self.assertTrue(0<v<=1)
    def test_monte_carlo_seed_repeat(self):
        a=infer(self.record,rho=1,n=60,seed=30)
        b=infer(self.record,rho=1,n=60,seed=30)
        self.assertEqual(a['mean'],b['mean'])
    def test_valid_credible_interval(self):
        a=infer(self.record,rho=1,n=60,seed=30)
        self.assertTrue(0<a['ci95'][0]<a['ci95'][1]<1)
    def test_model_comparison(self):
        a=infer(self.record,rho=1,n=60,seed=30)
        b=infer(self.record,rho=.1,n=60,seed=30)
        self.assertNotAlmostEqual(a['mean'],b['mean'],places=3)
    def test_small_audit(self):
        z=small_audit(n=2,particles=45)
        self.assertEqual(len(z),5)

if __name__=="__main__":unittest.main()
