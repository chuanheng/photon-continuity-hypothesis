"""29 checks for the v0.82 raw count and bootstrap model."""
import unittest
import numpy as np
from models.count_hierarchy_v082 import (
    DEFAULT,phase_covariance,source_means,simulate_data,poisson_nll,fit,
    profile_statistic,parametric_bootstrap,group_offset_degeneracy
)

class TestPoissonModel(unittest.TestCase):
    def test_covariance_symmetry(self):
        c=phase_covariance(8);self.assertTrue(np.allclose(c,c.T))
    def test_covariance_positive(self):self.assertGreater(np.linalg.eigvalsh(phase_covariance(8)).min(),0)
    def test_covariance_negative_rho(self):self.assertGreater(np.linalg.eigvalsh(phase_covariance(8,-.7)).min(),0)
    def test_bad_rho(self):
        with self.assertRaises(ValueError):phase_covariance(5,1.0)
    def test_bad_t(self):
        with self.assertRaises(ValueError):phase_covariance(1)
    def test_bad_sigma(self):
        with self.assertRaises(ValueError):phase_covariance(5,sigma=0)
    def test_means_shape(self):
        self.assertEqual(source_means(np.arange(8),np.zeros(8),.7,.6,.8,.1,.2).shape,(8,2,2))
    def test_mean_positive(self):
        self.assertGreater(source_means(np.arange(8),np.zeros(8),.7,.6,.8,.1,.2).min(),0)
    def test_mean_group_delta_zero(self):
        m=source_means(np.arange(8),np.zeros(8),.7,.6,.8,.1,0)
        self.assertTrue(np.allclose(m[:,0],m[:,1]))
    def test_mean_port_sum(self):
        m=source_means(np.arange(8),np.zeros(8),.7,.6,.8,.1,.2)
        self.assertTrue(np.allclose(m.sum(axis=-1),80*.7+2*.8))
    def test_invalid_means(self):
        with self.assertRaises(ValueError):source_means(np.arange(3),np.zeros(4),.7,.6,.8,.1,.2)
    def test_simulation_integer_counts(self):
        d=simulate_data(seed=2);self.assertTrue(np.issubdtype(d['counts'].dtype,np.integer))
    def test_simulation_counts_positive(self):
        d=simulate_data(seed=2);self.assertGreaterEqual(d['counts'].min(),0)
    def test_simulation_reproducible(self):
        d=simulate_data(seed=2);e=simulate_data(seed=2)
        self.assertTrue(np.array_equal(d['counts'],e['counts']))
    def test_simulation_control(self):
        d=simulate_data(seed=2,delta=0);self.assertEqual(len(d['x']),10)
    def test_poisson_nll_finite(self):
        self.assertTrue(np.isfinite(poisson_nll(np.array([1,3]),np.array([1.,2.]))))
    def test_poisson_nll_invalid(self):
        self.assertEqual(poisson_nll(np.array([1]),np.array([0.])),np.inf)

class TestEstimation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=simulate_data(seed=7,delta=.2,t=8)
        cls.null=fit(cls.data,False)
        cls.alt=fit(cls.data,True)
    def test_null_finite(self):self.assertTrue(np.isfinite(self.null['objective']))
    def test_alt_finite(self):self.assertTrue(np.isfinite(self.alt['objective']))
    def test_alt_likelihood_not_worse(self):self.assertLessEqual(self.alt['objective'],self.null['objective']+1e-4)
    def test_valid_fit_eta(self):self.assertTrue(0<self.alt['parameters'][0]<1)
    def test_valid_fit_visibility(self):self.assertTrue(0<self.alt['parameters'][1]<1)
    def test_valid_fit_dark(self):self.assertGreater(self.alt['parameters'][2],0)
    def test_stat_nonnegative(self):self.assertGreaterEqual(profile_statistic(self.data)['statistic'],0)
    def test_background_data_shape(self):self.assertEqual(self.data['dark_counts'].shape,(8,2))
    def test_ar1_latent_length(self):self.assertEqual(len(self.alt['parameters']),5+8)
    def test_group_offset_exact(self):
        self.assertAlmostEqual(group_offset_degeneracy(.2,.3,.4),group_offset_degeneracy(.2,.7,0))
    def test_bootstrap_short_run(self):
        b=parametric_bootstrap(self.data,replications=10,seed=4)
        self.assertEqual(len(b['null_stats']),10)
        self.assertTrue(0<b['empirical_p_plus_one']<=1)
    def test_bootstrap_deterministic(self):
        a=parametric_bootstrap(self.data,replications=10,seed=3)
        b=parametric_bootstrap(self.data,replications=10,seed=3)
        self.assertTrue(np.allclose(a['null_stats'],b['null_stats']))

if __name__=='__main__':unittest.main()
