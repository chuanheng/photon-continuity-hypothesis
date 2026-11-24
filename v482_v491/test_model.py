import unittest

from . import model


class OrdinaryStorageTests(unittest.TestCase):
    def test_flagged_bell(self):
        result=model.flagged_bell()
        self.assertLess(result["trace_error"],1e-14)
        self.assertGreater(result["success_fidelity"],.5)
        self.assertAlmostEqual(result["negativity"],result["unnormalized_witness"])

    def test_multipair_threshold(self):
        result=model.multipair_threshold()
        self.assertLess(result["threshold_refit_error"],1e-14)
        self.assertLess(result["refit_overlap"],1)
        self.assertGreater(result["near_four_same_port_probability"],.005)

    def test_rank_two_receiver(self):
        result=model.compressed_modes()
        self.assertAlmostEqual(result["matched_detection"],result["optimum_detection"])
        self.assertLess(result["best_random_detection"],result["optimum_detection"])
        self.assertGreater(result["all_mode_detection"],result["optimum_detection"])
        self.assertLess(result["isometry_error"],1e-14)

    def test_ramsey_refit_exposed_by_echo(self):
        result=model.echo_refit()
        self.assertGreater(min(result["white"],result["static"]),0)
        self.assertLess(result["ramsey_error"],1e-14)
        self.assertLess(result["echo_integral_error"],1e-6)
        self.assertLess(result["single_echo_gap"],1e-14)
        self.assertGreater(result["two_pulse_echo_gap"],.01)

    def test_common_reference_covariance(self):
        result=model.correlated_reference()
        self.assertLess(result["simulation_error"],.0008)
        self.assertLess(abs(result["monitor_subtracted_cross_moment"]),.0008)
        self.assertLess(result["observed_cross_moment"],0)
        self.assertGreater(result["reversed_cross_moment"],0)

    def test_thermal_count_statistics(self):
        result=model.thermal_bunching()
        self.assertLess(result["mean_refit_error"],1e-14)
        self.assertAlmostEqual(result["thermal_g2"],2.)
        self.assertAlmostEqual(result["poisson_g2"],1.)
        self.assertLess(result["optical_electronic_marginal_error"],1e-14)

    def test_anharmonic_excitation_ladder(self):
        result=model.excitation_ladder()
        self.assertGreater(result["closest_line_change"],.1)
        self.assertGreater(result["max_equal_lineweight_response_gap"],.3)
        self.assertLess(result["ordinary_nonlinear_refit_error"],1e-14)

    def test_timing_transfer_modes(self):
        result=model.jittered_delay()
        self.assertLess(result["map_svd_error"],1e-14)
        self.assertLess(result["observable_modes_at_floor"],result["bins"])
        self.assertGreater(result["observable_modes_at_floor"],1)
        self.assertLess(result["eye_column_sum_error"],1e-14)
        self.assertLess(result["split_jitter_refit_error"],1e-14)

    def test_reciprocity_counterexamples(self):
        result=model.reciprocity()
        self.assertLess(result["full_unitarity_error"],1e-14)
        self.assertAlmostEqual(result["best_reciprocal_frobenius_residual"],1/2**.5)
        self.assertGreater(result["reciprocal_uncalibrated_power_gap"],.3)

    def test_held_out_linear_program(self):
        result=model.retained_process()
        self.assertLess(result["primal_error"],1e-14)
        self.assertLess(result["dual_gap"],1e-14)
        self.assertGreaterEqual(result["dual_slack_min"],-1e-14)
        self.assertLess(result["restricted_prediction_max"],result["held_observation"])
        self.assertLess(result["extended_refit_error"],1e-14)
