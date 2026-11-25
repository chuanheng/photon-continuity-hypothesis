import unittest

from . import model


class JointCalibrationTests(unittest.TestCase):
    def test_shared_leakage(self):
        result = model.shared_leakage()
        self.assertGreater(result["shared_residual"], .1)
        self.assertLess(result["projected_residual_dot"], 1e-14)
        self.assertLess(result["per_setting_max_amplitude"], result["per_setting_bound"])
        self.assertLess(result["per_setting_refit_error"], 1e-14)

    def test_calibration_ellipse(self):
        result = model.calibration_ellipse()
        self.assertAlmostEqual(result["global_distance"], .04)
        self.assertAlmostEqual(result["attainable_residual"], .04)
        self.assertLess(result["sampled_support"], result["support"]+1e-14)
        self.assertLess(result["observed_norm"], result["circular_outer_radius"])

    def test_reference_slope(self):
        result = model.reference_slope()
        self.assertGreater(result["calibrated_endpoint_gap"], .35)
        self.assertLess(result["free_reference_refit_error"], 1e-14)

    def test_nuisance_contrast(self):
        result = model.nuisance_contrast()
        self.assertAlmostEqual(result["null_response"], 0)
        self.assertAlmostEqual(result["signal_response"], .16)
        self.assertLess(result["curvature_refit_error"], 1e-14)

    def test_selection_error(self):
        result = model.selection_error()
        self.assertGreater(result["uncorrected_family_error"], .64)
        self.assertAlmostEqual(result["corrected_family_error"], .05)
        self.assertGreater(result["bonferroni_cutoff"], result["independent_adjusted_cutoff"])

    def test_reference_blocks(self):
        result = model.reference_blocks()
        self.assertLess(result["naive_coverage"], .5)
        self.assertAlmostEqual(result["valid_coverage"], .95, delta=.02)
        self.assertAlmostEqual(result["paired_coverage"], .95, delta=.02)

    def test_signed_power(self):
        result = model.signed_power()
        self.assertAlmostEqual(result["size"], .05)
        self.assertAlmostEqual(result["positive_power"], result["negative_power"])
        self.assertGreaterEqual(result["positive_power"], .9)
        self.assertLess(result["previous_count_power"], .9)

    def test_candidate_intersection(self):
        result = model.candidate_intersection()
        self.assertAlmostEqual(result["global_gaps"][0], 0)
        self.assertAlmostEqual(result["global_gaps"][1], .04)
        self.assertLess(result["overlap_point"], result["null_radius"])
        self.assertLess(result["distance_to_alternative_center"], result["alternative_radius"])

    def test_calibration_priority(self):
        result = model.calibration_priority()
        self.assertAlmostEqual(result["chosen_margin"], max(result["margins"]))
        self.assertLessEqual(result["intervention_cost"][result["chosen_index"]], result["budget"])

    def test_injection_recovery(self):
        result = model.injection_recovery()
        self.assertLess(result["sham_false_positive"], .01)
        self.assertGreater(result["full_chain_recovery"], .65)
        self.assertGreater(result["downstream_recovery"]-result["full_chain_recovery"], .15)
