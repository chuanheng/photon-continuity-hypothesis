import unittest

from . import model


class RobustDesignTests(unittest.TestCase):
    def test_optimal_design(self):
        r=model.optimal_design()
        self.assertEqual(r['pair'],[0,4])
        self.assertAlmostEqual(r['smallest_singular'],max(r['all_pair_smallest']))
        self.assertGreater(r['smallest_singular'],8*r['close_controls_scale'])

    def test_matrix_uncertainty(self):
        r=model.matrix_uncertainty()
        self.assertGreater(r['robust_sigma_min_lower'],.72)
        self.assertLess(r['actual_response_shift'],r['response_shift_bound'])
        self.assertLess(r['nominal_coefficient_bias'],r['coefficient_bias_bound'])

    def test_preparation_leakage(self):
        r=model.preparation_leakage()
        self.assertAlmostEqual(r['clean_target_click'],.676)
        self.assertAlmostEqual(r['composite_target_click'],.63856)
        self.assertAlmostEqual(r['ordinary_false_path_probability'],.13)

    def test_joint_region(self):
        r=model.joint_region()
        self.assertGreater(r['distance_lower'],.045)
        self.assertGreater(r['box_contains_projection'],.05)

    def test_helstrom(self):
        r=model.helstrom()
        self.assertAlmostEqual(r['old_population_gap'],0)
        self.assertAlmostEqual(r['projective_prediction_gap'],r['trace_distance'])
        self.assertAlmostEqual(r['minimal_error'],(1-r['trace_distance'])/2)

    def test_exact_power(self):
        r=model.exact_power()
        self.assertEqual(r['first_n'],968)
        self.assertGreaterEqual(r['power'],.90)
        self.assertLess(r['max_smaller_n_power'],.90)
        self.assertLess(r['null_probability'],.05)

    def test_correlated_repetitions(self):
        r=model.correlated_repetitions()
        self.assertGreater(r['correct_se'][-1],r['se_floor'])
        self.assertGreater(r['correct_se'][-1],6*r['naive_se'][-1])
        self.assertLess(r['power'][-1],.71)

    def test_transfer_calibration(self):
        r=model.transfer_calibration()
        self.assertGreater(r['calibrated_margin'],0)
        self.assertLess(r['unmonitored_margin'],0)
        self.assertAlmostEqual(r['ordinary_shift_exact_refit'],0)

    def test_spectral_holdout(self):
        r=model.spectral_holdout()
        self.assertAlmostEqual(r['coarse_bin_gap'],0)
        self.assertGreater(r['resolved_total_variation'],.16)
        self.assertGreater(r['bounded_centroid_first_bin_certificate'],.12)
        self.assertAlmostEqual(r['ordinary_unbounded_centroid_refit'],0)

    def test_operational_stop(self):
        r=model.operational_stop()
        self.assertAlmostEqual(r['enlarged_ordinary_gap'],0)
        self.assertAlmostEqual(r['independently_constrained_gap'],r['analytic_constrained_gap'])
        self.assertGreater(r['independently_constrained_gap'],.049)
