import unittest

import numpy as np

from .model import calibration_design, quantum_break


class CheckpointTests(unittest.TestCase):
    def test_432_approximate_break_and_unreset_environment(self):
        result = quantum_break()
        p = np.array(result["leakage"])
        np.testing.assert_allclose(result["bell_distance"], 3 * p / 4, atol=1e-14)
        np.testing.assert_allclose(result["unassisted_optimal_distance"], p / 2)
        self.assertEqual(result["local_distance_after_reset"], 0.0)
        self.assertEqual(result["distance_after_ordinary_swap"], 1.0)

    def test_433_incomplete_calibration_of_quantum_memory(self):
        result = calibration_design()
        self.assertEqual(result["z_only_design_rank"], 2)
        self.assertEqual(result["four_state_design_rank"], 4)
        np.testing.assert_allclose(result["distance_by_calibration_input"], [0, 0, 0.5, 0.5])
        self.assertAlmostEqual(result["bell_distance"], 0.5)
        np.testing.assert_allclose(result["minimum_choi_ppt_eigenvalues"], [-0.5, 0], atol=1e-14)
        self.assertGreaterEqual(min(result["minimum_choi_eigenvalues"]), -1e-14)
        self.assertLess(max(result["choi_trace_errors"]), 1e-14)

    def test_434_ordinary_factorial_interaction(self):
        from .controls import factorial
        result = factorial()
        self.assertAlmostEqual(result["ordinary_interaction"], 0.072)
        self.assertAlmostEqual(result["with_additive_drift"], 0.072)
        self.assertAlmostEqual(result["with_aliased_drift"]-0.072, result["drift_bias_bound"])

    def test_435_ordinary_route_swap(self):
        from .controls import route_swap
        result = route_swap()
        np.testing.assert_allclose(result["read_probabilities"], [[0.5184, 0.09], [0.2916, 0.16]])
        self.assertEqual(result["basis_relabel_error"], 0)

    def test_436_non_diagonal_memory_witness(self):
        from .controls import dimension_witness
        result = dimension_witness()
        self.assertEqual(result["full_rank"], 4)
        self.assertEqual(result["z_only_rank"], 2)
        self.assertAlmostEqual(result["rank_four_minor"], 0.25)

    def test_437_correlated_counts(self):
        from .controls import correlated_trials
        result = correlated_trials()
        self.assertGreater(result["actual_size_using_iid"], 0.30)
        self.assertLess(result["block_bound_actual_size"], 0.05)

    def test_438_calibrated_spectral_refit(self):
        from .controls import spectral_refit
        result = spectral_refit()
        self.assertTrue(result["total_feasible"])
        self.assertEqual(result["spectrum_solver_status"], 2)
        self.assertAlmostEqual(result["calibrated_middle_ceiling"], 0.2775)
        self.assertLess(result["free_background_residual"], 1e-12)

    def test_439_bosonic_projection(self):
        from .controls import bosonic_operator
        result = bosonic_operator()
        self.assertEqual(result["symmetric_dimension"], 3)
        self.assertLess(result["slot_difference_norm"], 1e-12)
        self.assertEqual(result["collective_eigenvalues"], [-2.0, 0.0, 2.0])

    def test_440_ordinary_environment_refit(self):
        from .controls import ordinary_dilation
        result = ordinary_dilation()
        self.assertEqual(result["trajectories_checked"], 121)
        self.assertLess(result["max_reduced_difference"], 1e-12)
        self.assertAlmostEqual(result["addressable_environment_x_difference"], 1.0)

    def test_441_calibration_and_separation_gates(self):
        from .controls import decision_gates
        result = decision_gates()
        self.assertEqual(result["decisions"], ["insufficient_separation", "reject_scoped_family",
                                               "calibration_inconclusive"])
