"""26 unit tests for v0.83 from repository root:
python -m unittest discover -s tests -p 'test_calibrated_bootstrap_v083.py' -v
"""
import unittest
import numpy as np
from models.calibrated_bootstrap_v083 import (
    simulate_calibration,kalman_nll,estimate_hyperparameters,
    conditioned_photon_data,bootstrap_with_refit,
    group_bias_equivalent,random_walk,covariance_model_mismatch_example,
)
from models.count_hierarchy_v082 import simulate_data,profile_statistic

class CalibrationTest(unittest.TestCase):
    def test_length(self):
        y,u=simulate_calibration(40)
        self.assertEqual((len(y),len(u)),(40,40))
    def test_reproducibility(self):
        a,_=simulate_calibration(seed=11);b,_=simulate_calibration(seed=11)
        self.assertTrue(np.array_equal(a,b))
    def test_noise_record_nonzero(self):
        y,u=simulate_calibration(seed=13)
        self.assertGreater(np.linalg.norm(y-u),0)
    def test_invalid_rho(self):
        with self.assertRaises(ValueError):simulate_calibration(rho=1)
    def test_invalid_sigma(self):
        with self.assertRaises(ValueError):simulate_calibration(sigma=-.1)
    def test_invalid_length(self):
        with self.assertRaises(ValueError):simulate_calibration(length=2)
    def test_kalman_finite(self):
        y,_=simulate_calibration()
        self.assertTrue(np.isfinite(kalman_nll(y,.8,.12)))
    def test_kalman_invalid(self):
        with self.assertRaises(ValueError):kalman_nll(np.ones(50),1,.12)
    def test_calibration_fit_converges(self):
        y,_=simulate_calibration(140,seed=71)
        fit=estimate_hyperparameters(y)
        self.assertTrue(fit['success'])
        self.assertTrue(-.95<=fit['rho']<=.97 and .008<=fit['sigma']<=.5)
    def test_calibration_fit_reproducible(self):
        y,_=simulate_calibration(100,seed=71)
        a=estimate_hyperparameters(y);b=estimate_hyperparameters(y)
        self.assertAlmostEqual(a['rho'],b['rho'])
        self.assertAlmostEqual(a['sigma'],b['sigma'])
    def test_fitted_model_better_than_far_wrong(self):
        y,_=simulate_calibration(160,seed=20)
        fit=estimate_hyperparameters(y)
        self.assertLessEqual(fit['nll'],kalman_nll(y,-.8,.35)+1e-7)
    def test_known_sensor_noise_restriction(self):
        y,_=simulate_calibration()
        with self.assertRaises(ValueError):estimate_hyperparameters(y,readout_sd=0)

class BootstrapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cal,_=simulate_calibration(70,seed=22)
        cls.data=simulate_data(t=7,delta=0,seed=33)
        cls.result=bootstrap_with_refit(cls.data,cls.cal,replications=10,seed=44)
    def test_replicate_length(self):
        self.assertEqual(len(self.result['null_bootstrap_stats']),10)
    def test_each_hyperparameter_refit(self):
        self.assertEqual(len(self.result['refitted_hyperparameters']),10)
        self.assertGreater(np.std(np.asarray(self.result['refitted_hyperparameters'])[:,0]),1e-4)
    def test_photon_optimization_converged(self):
        self.assertEqual(self.result['both_photon_fits_converged'],10)
    def test_hyper_fit_success(self):
        self.assertTrue(self.result['all_calibration_fits_converged'])
    def test_empirical_p_resolution(self):
        self.assertIn(round(self.result['p_plus_one']*11),range(1,12))
        self.assertAlmostEqual(round(self.result['p_plus_one']*11),self.result['p_plus_one']*11)
    def test_critical_finite(self):
        self.assertTrue(np.isfinite(self.result['critical_value_95']))
    def test_invalid_bootstrap_size(self):
        with self.assertRaises(ValueError):bootstrap_with_refit(self.data,self.cal,replications=5)
    def test_input_unchanged(self):
        self.assertEqual(self.data['rho'],.8)
        self.assertEqual(self.data['sigma'],.12)
    def test_conditioned_parameters(self):
        d=conditioned_photon_data(self.data,.6,.18)
        self.assertAlmostEqual(d['rho'],.6)
        self.assertAlmostEqual(d['sigma'],.18)
    def test_exact_group_bias_degeneracy(self):
        self.assertAlmostEqual(group_bias_equivalent(.18,.07),group_bias_equivalent(0,.25))
    def test_random_walk_reproducible(self):
        a=random_walk(10,.2,seed=1);b=random_walk(10,.2,seed=1)
        self.assertTrue(np.array_equal(a,b))
    def test_random_walk_invalid(self):
        with self.assertRaises(ValueError):random_walk(0,.1)
    def test_nonstationary_example(self):
        data,bias=covariance_model_mismatch_example(8)
        self.assertEqual(data['counts'].shape,(8,2,2))
        self.assertAlmostEqual(bias,.23)
    def test_profile_nonnegative_on_mismatch(self):
        data,_=covariance_model_mismatch_example(8)
        fit=profile_statistic(data)
        self.assertGreaterEqual(fit['statistic'],0)

if __name__=='__main__':unittest.main()
