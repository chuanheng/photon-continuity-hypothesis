import unittest
import numpy as np
from models.fair_composite_null_v085 import *

class DriftTests(unittest.TestCase):
    def test_ar1_reproducibility(self): self.assertTrue(np.array_equal(latent_drift(24,seed=5),latent_drift(24,seed=5)))
    def test_walk_reproducibility(self): self.assertTrue(np.array_equal(latent_drift(24,'random_walk',seed=5),latent_drift(24,'random_walk',seed=5)))
    def test_piecewise_changes(self): self.assertGreater(latent_drift(100,'piecewise',seed=5)[50:].mean(),latent_drift(100,'piecewise',seed=5)[:50].mean())
    def test_invalid_drift(self):
        with self.assertRaises(ValueError):latent_drift(10,'not_a_model')
    def test_invalid_size(self):
        with self.assertRaises(ValueError):latent_drift(1)
    def test_invalid_rho(self):
        with self.assertRaises(ValueError):latent_drift(10,rho=1.)

class CountTests(unittest.TestCase):
    def setUp(self):self.u=latent_drift(24,'ar1',seed=6)
    def test_shape(self):self.assertEqual(poisson_means(self.u).shape,(24,2,2,2))
    def test_positivity(self):self.assertGreater(poisson_means(self.u).min(),0)
    def test_sample_reproducible(self):
        a=poisson_means(self.u);self.assertTrue(np.array_equal(sample_counts(a,seed=6),sample_counts(a,seed=6)))
    def test_sample_integer(self):self.assertTrue(np.issubdtype(sample_counts(poisson_means(self.u)).dtype,np.integer))
    def test_bad_signature(self):
        with self.assertRaises(ValueError):poisson_means(self.u,signature=np.ones(5))
    def test_bad_eta(self):
        with self.assertRaises(ValueError):poisson_means(self.u,cfg={**DEFAULT,'eta':1.5})
    def test_bad_likelihood_shape(self):
        with self.assertRaises(ValueError):poisson_log_likelihood(np.ones(4),np.ones(5))
    def test_kl_self_zero(self):
        p=poisson_means(self.u);self.assertAlmostEqual(poisson_kl(p,p),0,places=10)
    def test_kl_nonnegative(self):
        a=poisson_means(self.u,ordinary_bias=.1);b=poisson_means(self.u,ordinary_bias=.2)
        self.assertGreater(poisson_kl(a,b),0)

class StructuralTests(unittest.TestCase):
    def setUp(self):self.u=latent_drift(24,'ar1',seed=8)
    def test_equal_ar1(self): self.assert_equivalence(self.u)
    def test_equal_walk(self): self.assert_equivalence(latent_drift(24,'random_walk',seed=8))
    def test_equal_piecewise(self):self.assert_equivalence(latent_drift(24,'piecewise',seed=8))
    def assert_equivalence(self,u):
        p=poisson_means(u,.11,.2);z=exact_null_relabel(u,.11,.2)
        q=poisson_means(z['latent_drift'],z['ordinary_bias'],z['identity_delta'])
        self.assertTrue(np.allclose(p,q,atol=1e-12,rtol=1e-14))
    def test_exact_joint_loglikelihood(self):
        p=poisson_means(self.u,.11,.2);q=poisson_means(self.u,.31,0.)
        self.assertAlmostEqual(poisson_log_likelihood(sample_counts(p),p),poisson_log_likelihood(sample_counts(p),q))
    def test_exact_kl(self):self.assertAlmostEqual(poisson_kl(poisson_means(self.u,.11,.2),poisson_means(self.u,.31)),0)
    def test_nonconstant_signature_not_constant_bias(self):
        with self.assertRaises(ValueError):exact_null_relabel(self.u,.11,.2,np.linspace(-1,1,len(self.u)))
    def test_constant_signature_relabel(self):
        t=exact_null_relabel(self.u,.11,.2,np.ones(len(self.u))*2)
        self.assertAlmostEqual(t['ordinary_bias'],.51)
    def test_fisher_rank_one(self):self.assertEqual(np.linalg.matrix_rank(fisher_bias_delta(self.u,.11,.2)),1)
    def test_fisher_null_vector(self):
        f=fisher_bias_delta(self.u,.11,.2);self.assertTrue(np.allclose(f@np.array([1.,-1.]),0))
    def test_calibration_lifts_rank(self):self.assertEqual(np.linalg.matrix_rank(calibrated_fisher(self.u,.11,.2,.05)),2)
    def test_calibration_independent_reproducible(self):self.assertEqual(independent_bias_calibration(.11,seed=5),independent_bias_calibration(.11,seed=5))
    def test_bad_calibration_sd(self):
        with self.assertRaises(ValueError):calibrated_fisher(self.u,.11,.2,0)
    def test_design_constant_rank_one(self):self.assertEqual(np.linalg.matrix_rank(nuisance_design(24)),1)
    def test_design_varying_rank_two(self):self.assertEqual(np.linalg.matrix_rank(nuisance_design(24,np.linspace(-1,1,24))),2)
    def test_time_bias_mimics_signature(self):
        self.assertEqual(np.linalg.matrix_rank(nuisance_design(24,np.linspace(-1,1,24),True)),24)
    def test_summary(self):
        s=summary();self.assertEqual(s['constant_signature_rank'],1)
        for k in ('ar1','random_walk','piecewise'):
            self.assertAlmostEqual(s['poisson_kl'][k],0)

if __name__=='__main__':unittest.main()
