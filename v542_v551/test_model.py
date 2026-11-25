import unittest

from . import model


class CalibrationTests(unittest.TestCase):
    def test_probe_angle(self):
        r = model.probe_angle()
        self.assertGreater(r['common_angle_gap'], .57)
        self.assertAlmostEqual(r['independently_profiled_gap'],r['numerical_independent_gap'])
        self.assertLess(r['independently_profiled_gap'],r['common_angle_gap'])
        self.assertAlmostEqual(r['uncalibrated_perpendicular_gap'],0)

    def test_hidden_fragment(self):
        r = model.hidden_fragment()
        self.assertAlmostEqual(r['visible_trace_distance'],0)
        self.assertAlmostEqual(r['coherent_parities'][0]-r['coherent_parities'][1],2)

    def test_phase_reference(self):
        r = model.phase_reference()
        self.assertAlmostEqual(r['estimate'],.18)
        self.assertGreater(r['interval'][0],0)
        self.assertGreater(r['joint_standard_error'],r['falsely_fixed_reference_se'])
        self.assertAlmostEqual(r['untracked_reference_refit_error'],0)

    def test_multi_pair_limit(self):
        r = model.multi_pair_limit()
        self.assertGreater(r['multi_pair_upper'],55/2000)
        self.assertGreater(r['certified_gap'],.024)
        self.assertAlmostEqual(r['worst_case_mixture_at_10_percent'],.775)

    def test_setting_dependent_flags(self):
        r = model.setting_dependent_flags()
        self.assertEqual(r['basis_success_rates'],[.5,.5])
        self.assertEqual(r['conditioned_correct_rate'],1)
        self.assertEqual(r['all_trials_score'],.5)

    def test_pt_confidence(self):
        r = model.pt_confidence()
        self.assertAlmostEqual(r['true_pt_minimum'],-.1175)
        self.assertLess(r['eigenvalue_upper'],0)
        self.assertGreater(r['estimated_pt_minimum']+r['weaker_triangle_radius'],0)

    def test_cross_calibration(self):
        r = model.cross_calibration()
        self.assertAlmostEqual(r['residual'],.04)
        self.assertGreater(r['valid_margin'],.03)
        self.assertAlmostEqual(r['falsely_ignored_readout_residual'],0)
        self.assertAlmostEqual(r['untracked_pulse_exact_refit_error'],0)

    def test_temporal_rank(self):
        r = model.temporal_rank()
        self.assertGreater(r['certified_gap'],.036)
        self.assertLess(r['without_control_singular'][1],1e-14)

    def test_conserved_label(self):
        r = model.conserved_label()
        self.assertAlmostEqual(r['allowed_charge_commutator'],0)
        self.assertGreater(r['wrong_charge_commutator'],1)
        self.assertEqual(r['stored_optical_population'],0)
        self.assertEqual(r['stored_charge'],1)
        self.assertEqual(r['ordinary_port_refit_error'],0)

    def test_blind_holdout(self):
        r = model.blind_holdout()
        self.assertGreater(r['exclusion_margin'],.024)
        self.assertLess(abs(r['matched_ordinary_contrast']),r['validated_ordinary_radius'])
