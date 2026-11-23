import unittest

from .extensions import (bypass_cuts, clustered_phase, distance_profile, exchange_modes,
                         history_cp, probe_rank, selection_control, spectral_refit)
from .model import constrained_refit, witness


class PhaseTests(unittest.TestCase):
    def test_442_noncommuting_control(self):
        result = witness()
        self.assertLess(result["max_formula_error"], 1e-14)
        self.assertAlmostEqual(result["x_readout_total_variation_pi_over_2"], 0.5)

    def test_443_calibration_and_exact_ordinary_refit(self):
        result = constrained_refit()
        self.assertAlmostEqual(result["calibrated_solution"][2], 0.24)
        self.assertAlmostEqual(result["ordinary_coherent_solution"][0], 0.5)
        self.assertAlmostEqual(result["ordinary_coherent_solution"][2], 0.0)


class ExtensionTests(unittest.TestCase):
    def test_444_probe(self):
        r = probe_rank()
        self.assertEqual((r["signal_rank"], r["joint_rank"]), (3, 4))
        self.assertLess(r["null_error"], 1e-14)
        self.assertGreater(r["joint_sigma_min"], .7)

    def test_445_fourth_path(self):
        r = bypass_cuts()
        self.assertLess(r["formula_error"], 1e-12)
        self.assertAlmostEqual(r["uncalibrated_upper"][-1], 1)
        self.assertAlmostEqual(r["fourth_path_calibrated_upper"][-1], .025)

    def test_446_sessions(self):
        r = clustered_phase()
        self.assertGreater(r["naive_rejection"], .60)
        self.assertTrue(.03 < r["cluster_rejection"] < .07)
        self.assertTrue(.03 < r["holdout_rejection"] < .07)
        self.assertAlmostEqual(r["simulated_mean_variance"]/r["theoretical_mean_variance"],
                               1, delta=.08)

    def test_447_refit(self):
        r = spectral_refit()
        self.assertLess(r["ordinary_max_error"], 1e-11)
        self.assertGreater(r["frozen_max_error"], .1)

    def test_448_modes(self):
        r = exchange_modes()
        self.assertLess(r["formula_error"], 1e-14)
        self.assertLess(r["common_rotation_error"], 1e-14)
        self.assertGreater(r["mode_resolved_max_contrast"], .3)
        self.assertEqual(r["bunched_projector_rank"], 36)
        self.assertEqual(r["bunched_projector_dimension"], 36)

    def test_449_cp(self):
        r = history_cp()
        for case in r["parameters"]:
            self.assertLess(case["tp_error"], 1e-14)
            self.assertLess(case["pauli_formula_error"], 1e-14)
            self.assertAlmostEqual(case["min_choi"], min(0, (1-abs(case["c"]))/2))
        self.assertGreater(r["parameters"][2]["x_plus_probability"], 1)
        self.assertLess(r["causal_prefix_error"], 1e-14)

    def test_450_profile(self):
        r = distance_profile()
        self.assertLess(r["formula_error"], 1e-12)
        self.assertAlmostEqual(r["binary_tv_at_first_cap"], .07)
        self.assertAlmostEqual(r["expectation_linf"][-1], 0)

    def test_451_heralding(self):
        r = selection_control()
        self.assertAlmostEqual(r["accepted_contrast"], .8)
        self.assertEqual(r["accepted_rate"], [.5, .5])
        self.assertLess(r["all_trial_contrast"], 1e-14)
