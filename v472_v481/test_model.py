import unittest

from .model import modulated_rotation,pulsed_loading


class PartialTests(unittest.TestCase):
    def test_rotation(self):
        r = modulated_rotation()
        self.assertLess(r["polarization_summed_spectral_power_error"],1e-14)
        self.assertLess(r["ordinary_rotator_probability_error"],1e-14)
        self.assertGreater(r["common_phase_probability_error"],.2)

    def test_loading(self):
        r = pulsed_loading()
        matched, square = r["matched_and_square_ledgers"]
        self.assertAlmostEqual(matched[0],r["optimal_storage_probability"],places=10)
        self.assertGreater(matched[0],square[0])
        self.assertLess(r["max_ledger_error"],1e-10)
        self.assertAlmostEqual(r["steady_resonant_reflection_amplitude"],0)


from . import controls


class FieldControlTests(unittest.TestCase):
    def test_resolved_mode_recovers_arbitrary_input(self):
        result = controls.resolved_jones()
        self.assertLess(result["reduced_error"],1e-14)
        self.assertLess(result["filtered_inversion_error"],1e-14)
        self.assertLess(result["unfiltered_visibility"],.5)

    def test_depth_ratio_requires_invariant_spam(self):
        result = controls.polarization_transfer()
        self.assertLess(result["single_depth_refit"],1e-14)
        self.assertGreater(result["depth_two_gap"],.04)
        self.assertAlmostEqual(result["depth_ratio"],.7)
        self.assertLess(result["readout_drift_refit"],1e-14)

    def test_joint_multiport_bound(self):
        result = controls.multiport_reset()
        self.assertLess(result["max_port"],result["calibrated_norm"])
        self.assertGreater(result["least_exact_refit_norm"],result["calibrated_norm"])
        self.assertAlmostEqual(result["bounded_residual"],result["least_exact_refit_norm"]-.12)
        self.assertLess(result["exact_refit_error"],1e-14)

    def test_zero_quantum_capacity_with_history(self):
        result = controls.flagged_history()
        self.assertLess(result["tp_error"],1e-14)
        self.assertAlmostEqual(result["history_trace_distance"],.37)
        self.assertAlmostEqual(result["coherent_information"],-.26)
        self.assertEqual(result["quantum_capacity"],0)

    def test_transport_with_missing_outcomes(self):
        result = controls.transported_contrast()
        low,high = result["identified_interval"]
        self.assertLess(low,result["prediction"])
        self.assertGreater(high,result["prediction"])
        self.assertLess(result["lp_error"],1e-14)
        self.assertLess(result["exact_refit_error"],1e-14)

    def test_passive_remote_bands(self):
        result = controls.remote_lorentz()
        self.assertLessEqual(result["real_refit_error"],1.00001e-4)
        self.assertGreater(result["target_imaginary_peak"],0)
        self.assertLess(result["ordinary_max_imaginary"],2e-4)

    def test_storage_phase_without_optical_population(self):
        result = controls.coherent_reemission()
        self.assertLess(result["stored_arm_optical_population"],1e-14)
        self.assertLess(result["output_pop_variation"],1e-14)
        self.assertAlmostEqual(result["reference_fringe_span"],1)
        self.assertLess(result["analytic_fringe_error"],1e-14)
        self.assertLess(result["excitation_ledger_error"],1e-14)

    def test_joint_calibration_excludes_marginal_fit(self):
        result = controls.joint_quadrature()
        self.assertLess(result["max_marginal_required_power"],result["calibrated_power_bound"])
        self.assertGreater(result["minimum_shared_power"],result["calibrated_power_bound"])
        self.assertAlmostEqual(result["critical_missing_power"],.002733)
