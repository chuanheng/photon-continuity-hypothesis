import unittest
import numpy as np
from models.correlated_drift_v081 import *

class TestCovariance(unittest.TestCase):
    def test_symmetric(self):self.assertTrue(np.allclose(ar1_cov(20,.8,.2),ar1_cov(20,.8,.2).T))
    def test_positive(self):self.assertGreater(np.linalg.eigvalsh(residual_cov(40,.9,.1,.02)).min(),0)
    def test_stationary_variance(self):self.assertAlmostEqual(ar1_cov(10,.8,.2)[0,0],.2**2/(1-.8**2))
    def test_lag_covariance(self):self.assertAlmostEqual(ar1_cov(10,.8,.2)[0,4]/ar1_cov(10,.8,.2)[0,0],.8**4)
    def test_zero_drift_diagonal(self):self.assertTrue(np.allclose(residual_cov(10,.8,0,.1),.01*np.eye(10)))
    def test_invalid_rho(self):
        with self.assertRaises(ValueError):ar1_cov(10,1,.1)
    def test_invalid_sigma(self):
        with self.assertRaises(ValueError):ar1_cov(10,.8,-.1)
    def test_invalid_n(self):
        with self.assertRaises(ValueError):ar1_cov(0,.5,.1)
    def test_readout_negative(self):
        with self.assertRaises(ValueError):residual_cov(10,.5,.1,-.1)

class TestGLS(unittest.TestCase):
    def test_weights_sum(self):self.assertAlmostEqual(gls_weights(residual_cov(20,.9,.1,.05))[0].sum(),1)
    def test_white_noise_weights(self):
        w,v=gls_weights(.01*np.eye(10));self.assertTrue(np.allclose(w,.1));self.assertAlmostEqual(v,.001)
    def test_shape_validation(self):
        with self.assertRaises(ValueError):gls_weights(np.ones((3,2)))
    def test_constant_estimate(self):
        c=residual_cov(20,.8,.1,.05);self.assertAlmostEqual(score(np.ones(20)*.3,c)['delta_hat'],.3)
    def test_zero_residual(self):self.assertEqual(score(np.zeros(10),np.eye(10))['llr'],0)
    def test_size_mismatch(self):
        with self.assertRaises(ValueError):score(np.ones(5),np.eye(6))
    def test_correlated_se_greater_than_naive(self):
        c=residual_cov(80,.92,.09,.05)
        self.assertGreater(score(np.zeros(80),c)['standard_error'],.05/np.sqrt(80))
    def test_reproducible_sequence(self):
        a,_=gaussian_phase_records(12,seed=3);b,_=gaussian_phase_records(12,seed=3)
        self.assertTrue(np.array_equal(a,b))

class TestBootstrap(unittest.TestCase):
    def test_bootstrap_positive(self):self.assertGreater(bootstrap_threshold(np.eye(10),B=500)[0],0)
    def test_bootstrap_near_chisquare_threshold(self):
        q,_=bootstrap_threshold(np.eye(12),B=3000,seed=12)
        self.assertLess(abs(q-3.8414588),.45)
    def test_bad_bootstrap(self):
        with self.assertRaises(ValueError):bootstrap_threshold(np.eye(10),B=4)
    def test_null_naive_false_positives(self):
        r=monte_carlo(n_sim=350)
        self.assertGreater(r['naive_rejection_rate'],.4)
    def test_null_corrected_rate(self):
        r=monte_carlo(n_sim=350)
        self.assertLess(abs(r['correlated_rejection_rate']-.05),.055)
    def test_signal_increases_power(self):
        null=monte_carlo(n_sim=350,delta=0)
        alt=monte_carlo(n_sim=350,delta=.15)
        self.assertGreater(alt['correlated_rejection_rate'],null['correlated_rejection_rate'])
    def test_gaussian_interferometer_probability(self):
        p=phase_fringe_prob(.3);self.assertAlmostEqual(p.sum(),1)
    def test_invalid_fringe(self):
        with self.assertRaises(ValueError):phase_fringe_prob(.3,visibility=1.4)
    def test_exact_reparametrization(self):
        self.assertAlmostEqual(confounding_with_group_bias(.2,.1),confounding_with_group_bias(0,.3))
    def test_summary(self):
        s=summary();self.assertEqual(s['n'],80);self.assertGreater(s['null_rejection']['naive_rejection_rate'],s['null_rejection']['correlated_rejection_rate'])

if __name__=='__main__':unittest.main()
