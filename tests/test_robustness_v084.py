import unittest
import numpy as np
from models.robustness_v084 import (
    DEFAULT, ar1_path, estimate_ar1_sensor, poisson_counts,
    phase_differences, phase_readout_variance, gls_statistic,
    generate_experiment, bootstrap_pvalue, audit_outer
)
class ModelTests(unittest.TestCase):
    def test_ar1_length(self):
        self.assertEqual(len(ar1_path(20,.8,.1,np.random.default_rng(1))),20)
    def test_ar1_invalid(self):
        with self.assertRaises(ValueError):ar1_path(10,1,.1,np.random.default_rng(1))
    def test_ar1_reproducible(self):
        a=ar1_path(20,.8,.1,np.random.default_rng(1))
        b=ar1_path(20,.8,.1,np.random.default_rng(1))
        self.assertTrue(np.array_equal(a,b))
    def test_sensor_estimate_finite(self):
        u=ar1_path(300,.8,.1,np.random.default_rng(2))
        r,s=estimate_ar1_sensor(u)
        self.assertTrue(np.isfinite(r) and s>0)
    def test_sensor_invalid(self):
        with self.assertRaises(ValueError):estimate_ar1_sensor([1,2])
    def test_sensor_positive_variance(self):
        r,s=estimate_ar1_sensor(np.zeros(10))
        self.assertGreater(s,0)
    def test_counts_shape(self):
        c=poisson_counts(np.zeros(24),np.random.default_rng(3))
        self.assertEqual(c.shape,(24,2,2,2))
    def test_counts_nonnegative(self):
        self.assertGreaterEqual(poisson_counts(np.zeros(24),np.random.default_rng(3)).min(),0)
    def test_counts_integer(self):
        self.assertTrue(np.issubdtype(poisson_counts(np.zeros(24),np.random.default_rng(3)).dtype,np.integer))
    def test_counts_reproducible(self):
        self.assertTrue(np.array_equal(poisson_counts(np.zeros(24),np.random.default_rng(3)),poisson_counts(np.zeros(24),np.random.default_rng(3))))
    def test_phase_diff_shape(self):
        c=poisson_counts(np.zeros(24),np.random.default_rng(3))
        self.assertEqual(phase_differences(c).shape,(24,))
    def test_phase_diff_bad_shape(self):
        with self.assertRaises(ValueError):phase_differences(np.zeros((3,2,2)))
    def test_phase_diff_zero_in_expectation(self):
        c=poisson_counts(np.zeros(2000),np.random.default_rng(4))
        self.assertLess(abs(phase_differences(c).mean()),.01)
    def test_phase_diff_bias_in_expectation(self):
        c=poisson_counts(np.zeros(2000),np.random.default_rng(4),bias=.22)
        self.assertAlmostEqual(phase_differences(c).mean(),.22,delta=.02)
    def test_variance_positive(self):
        self.assertGreater(phase_readout_variance(),0)
    def test_gls_stat_positive(self):
        self.assertGreaterEqual(gls_statistic(np.ones(20)*.2,.8,.1)['stat'],0)
    def test_gls_zero(self):
        self.assertAlmostEqual(gls_statistic(np.zeros(20),.8,.1)['stat'],0)
    def test_gls_constant_estimate(self):
        self.assertAlmostEqual(gls_statistic(np.ones(20)*.2,.8,.1)['estimate'],.2)
    def test_gls_bad_rho(self):
        with self.assertRaises(ValueError):gls_statistic(np.ones(20),1.,.1)
class SimulationTests(unittest.TestCase):
    def test_stationary_experiment_shape(self):
        e=generate_experiment(np.random.default_rng(4))
        self.assertEqual(e['counts'].shape,(24,2,2,2))
    def test_walk_experiment(self):
        e=generate_experiment(np.random.default_rng(4),'random_walk')
        self.assertEqual(e['ordinary_bias'],0)
    def test_bias_experiment(self):
        e=generate_experiment(np.random.default_rng(4),'ordinary_group_bias')
        self.assertAlmostEqual(e['ordinary_bias'],.22)
    def test_unknown_scenario(self):
        with self.assertRaises(ValueError):generate_experiment(np.random.default_rng(4),'foo')
    def test_bootstrap_refits(self):
        e=generate_experiment(np.random.default_rng(4))
        b=bootstrap_pvalue(e,np.random.default_rng(5),b=19)
        self.assertEqual(b['hyperparameter_refits'],19)
        self.assertTrue(0<b['p']<=1)
    def test_bootstrap_bad_count(self):
        e=generate_experiment(np.random.default_rng(4))
        with self.assertRaises(ValueError):bootstrap_pvalue(e,np.random.default_rng(5),b=4)
    def test_audit_reproducible(self):
        a=audit_outer(outer=3,inner=9,seed=4)
        b=audit_outer(outer=3,inner=9,seed=4)
        self.assertEqual(a['scenario_results'],b['scenario_results'])
    def test_audit_counts(self):
        a=audit_outer(outer=4,inner=9,seed=4)
        for v in a['scenario_results'].values():
            self.assertEqual(v['outer_simulations'],4)
            self.assertEqual(len(v['pvalues']),4)
    def test_audit_invalid(self):
        with self.assertRaises(ValueError):audit_outer(outer=0)
    def test_nonstationary_raises_rejections_in_toy(self):
        a=audit_outer(outer=30,inner=39,seed=8401)
        r=a['scenario_results']
        self.assertGreater(r['random_walk']['false_positive_rate_if_null_held'],r['stationary']['false_positive_rate_if_null_held'])
        self.assertGreater(r['ordinary_group_bias']['false_positive_rate_if_null_held'],r['stationary']['false_positive_rate_if_null_held'])
if __name__=='__main__':unittest.main()
