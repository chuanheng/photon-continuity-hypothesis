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
