import unittest

from . import model


class OpticalCalibrationTests(unittest.TestCase):
    def test_narrowband_paths(self):
        result = model.narrowband_paths()
        self.assertAlmostEqual(result['calibration_l2'], .05)
        self.assertGreater(result['narrow_condition'], 20*result['wide_condition'])
        self.assertGreater(result['heldout_gap'], .65)

    def test_passive_scattering(self):
        result = model.passive_scattering()
        self.assertTrue(all(power < 1 for power in result['column_power']))
        self.assertAlmostEqual(result['coherent_output_power'], 1.48)
        self.assertAlmostEqual(result['distance_to_contraction'], result['spectral_lower_bound'])
        self.assertAlmostEqual(result['passive_norm'], 1)

    def test_spectral_resolution(self):
        result = model.spectral_resolution()
        self.assertLess(result['coarse_max'], 1e-14)
        self.assertGreater(result['fine_fraction'], .90)
        self.assertLess(result['uniform_center_phase_alias'], 1e-14)
        self.assertLess(result['quadrature_at_zero'], 1e-14)

    def test_injection_crosstalk(self):
        result = model.injection_crosstalk()
        self.assertGreater(result['observed_residual'], result['independently_allowed_matrix_drift'])
        self.assertGreater(result['nominal_science_port_amplitude'], .09)
        self.assertLessEqual(result['input_error'], result['certified_input_error_bound'])
        self.assertLess(result['ordinary_drift_refit_error'], 1e-14)

    def test_switching_order(self):
        result = model.switching_order()
        self.assertAlmostEqual(result['order_difference'], .17523825403889273)
        self.assertLess(result['identical_commutator_prediction_error'], 1e-14)
        self.assertAlmostEqual(result['commuting_equal_loss_difference'], 0.)

    def test_zero_events_under_drift(self):
        result = model.zero_events_under_drift()
        self.assertAlmostEqual(result['exposure'], 44)
        self.assertGreater(result['exact_profile_upper'], 2*result['falsely_factorized_upper'])
        self.assertGreater(result['exponential_envelope_upper'], result['exact_profile_upper'])
        self.assertGreater(result['zero_probability_at_wrong_upper'], .25)

    def test_coherence_window(self):
        result = model.coherence_window()
        self.assertLess(result['endpoint_gap'], 1e-14)
        self.assertLess(result['unmonitored_coherence'], 1e-14)
        self.assertGreater(result['smooth_reference_coherence'], result['guaranteed_coherence'])
        self.assertAlmostEqual(result['midpoint_phase_error'], 2.)

    def test_shared_systematic(self):
        result = model.shared_systematic()
        self.assertGreater(result['joint_se'], result['common_offset_floor'])
        self.assertGreater(result['joint_se'], 2*result['wrongly_independent_se'])
        self.assertAlmostEqual(result['paired_contrast_se'], .06*2**.5)
        self.assertEqual(result['fixed_offset_rank'], 1)

    def test_scalar_field_gap(self):
        result = model.scalar_field_gap()
        self.assertGreater(result['momentum_mismatch'], 0.)
        self.assertGreater(result['fixed_family_global_gap'], .048)
        self.assertLess(result['free_ordinary_refit_error'], 1e-14)

    def test_frozen_design(self):
        result = model.frozen_design()
        self.assertEqual(result['rejection_count'], 20)
        self.assertLess(result['joint_false_rejection_ceiling'], .05)
        self.assertGreater(result['synthetic_science_power_at_p_003'], .99)
        self.assertLess(result['sham_upper'], result['allowed_sham_bound'])
        self.assertGreater(result['upstream_recovery_lower'], result['required_upstream_bound'])
        self.assertLess(result['weak_upstream_recovery_lower'], result['required_upstream_bound'])
