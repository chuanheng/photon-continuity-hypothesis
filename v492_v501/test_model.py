import unittest
from . import model


class CarrierCriteriaTests(unittest.TestCase):
    def test_phase_reference(self):
        result=model.phase_reference()
        self.assertAlmostEqual(result["independent_distance"],0)
        self.assertAlmostEqual(result["single_mode_distinguishability"],0)
        self.assertAlmostEqual(result["common_distance"],.5)
        self.assertAlmostEqual(result["beam_splitter_probability_gap"],.5)
        self.assertLess(result["gaussian_mc_error"],.001)

    def test_thermal_reset(self):
        result=model.thermal_reset()
        self.assertGreater(result["heat"],0)
        self.assertGreater(result["landauer_excess"],0)
        self.assertLess(result["ledger_error"],1e-14)
        self.assertLess(result["identity_error"],1e-14)

    def test_triad_bunching(self):
        result=model.triad_bunching()
        self.assertGreater(result["triad_gap"],.008)
        self.assertLess(result["max_tensor_formula_error"],1e-14)
        self.assertAlmostEqual(result["triad_gap"],4*.38**3/27)

    def test_coupled_internal_mode(self):
        result=model.coupled_internal_mode()
        self.assertGreater(result["cross_mode_probability"],.3)
        self.assertLess(result["normal_mode_fit_error"],1e-14)
        self.assertLess(result["two_boson_count_fit_error"],1e-14)
        self.assertLess(result["residual_material_population"],1e-14)
        self.assertLess(result["joint_unitarity_error"],1e-14)

    def test_boosted_dwell(self):
        result=model.boosted_dwell()
        self.assertLess(result["invariant_phase_error"],1e-13)
        self.assertLess(result["proper_time_error"],1e-13)
        self.assertGreater(result["naive_max_phase_error"],1)

    def test_finite_clock(self):
        result=model.finite_clock()
        self.assertLess(result["tightness_error"],1e-14)
        self.assertGreater(result["tight_visibility"],result["flat_visibility"])
        self.assertLess(result["tight_visibility"],1)

    def test_reverse_loss(self):
        result=model.reverse_loss()
        self.assertLess(result["reference_error"],1e-14)
        self.assertLess(result["recovery_tp_error"],1e-14)
        self.assertLess(result["post_recovery_trace_distance"],result["post_loss_trace_distance"])

    def test_common_controller(self):
        result=model.common_controller()
        self.assertAlmostEqual(result["branch_mutual_information"],0.)
        self.assertGreater(result["conditional_mutual_information"],.5)
        self.assertLess(result["entropy_formula_error"],1e-14)

    def test_band_completion(self):
        result=model.band_completion()
        self.assertEqual(result["null_dimension"],3)
        self.assertLess(result["in_band_refit_error"],1e-14)
        self.assertAlmostEqual(result["omitted_band_energy"],1)
        self.assertLess(result["full_energy_error"],1e-14)

    def test_sourced_scalar(self):
        result=model.sourced_scalar()
        self.assertEqual(result["plane_wave_source"],0)
        self.assertEqual(result["standing_antinode_source"],-8)
        self.assertLess(result["ordinary_gapped_refit_error"],1e-14)
        self.assertLess(result["far_near_scaled_ratio"],.2)
