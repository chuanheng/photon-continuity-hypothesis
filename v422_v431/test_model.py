import unittest

import numpy as np
import sympy as sp

from .calibration import (
    DRIFT, distance_certificate, fit_training, memory_amplitude, probabilities,
)
from .model import run


class BatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = run()

    def test_422_controlled_equivalence_and_counterexample(self):
        result = self.results["v4.22"]
        self.assertEqual(result["equivalent"], {"basis_dimension": 4, "witness": None})
        self.assertEqual(result["changed_reset"]["witness"]["difference"], "-12/625")
        self.assertEqual(result["adaptive_total_mass"], "1")
        self.assertGreater(sp.Rational(result["adaptive_changed_total_variation"]), 0)

    def test_423_exact_rank_witness(self):
        for setting in ("controlled", "passive"):
            result = self.results["v4.23"][setting]
            self.assertEqual(result["ranks_by_depth"], [1, 2, 4])
            self.assertNotEqual(sp.Rational(result["determinant"]), 0)
        self.assertIn((("reset", 0),), self.results["v4.23"]["controlled"]["rows"])

    def test_424_positive_realization(self):
        result = self.results["v4.24"]
        self.assertEqual(result["square_rank"], result["simpler_rank"])
        self.assertEqual(result["square_nonnegative_lower"], result["square_nonnegative_upper"])
        self.assertEqual(result["square_nonnegative_lower"], 4)
        self.assertEqual(result["simpler_nonnegative_upper"], 3)

    def test_425_independent_calibration_and_missing_carrier(self):
        result = self.results["v4.25"]
        self.assertGreaterEqual(result["joint_reference_coverage"]["rate"], 0.975)
        stress = result["main_upper_envelope_coverage"]
        self.assertGreater(stress["in_budget_shared_drift"]["rate"], 0.99)
        self.assertLess(stress["unmonitored_carrier"]["rate"], 0.01)

    def test_426_quantum_and_classical_memory_comparison(self):
        result = self.results["v4.26"]
        self.assertAlmostEqual(result["quantum_success"], (1 + 1 / np.sqrt(2)) / 2)
        self.assertEqual(result["classical_one_bit_maximum"], 0.75)
        self.assertLess(result["two_bit_match_error"], 1e-14)
        for channel in ("preparation", "storage"):
            self.assertGreaterEqual(result[channel + "_choi_min_eigenvalue"], -1e-14)
            self.assertLess(result[channel + "_trace_error"], 1e-14)

    def test_427_exact_positive_distance_and_refit(self):
        result = distance_certificate()
        np.testing.assert_allclose(result["null_ceiling"], [0.528, 0.55])
        self.assertAlmostEqual(result["exact_equal_weight_kl"], 0.001057943305285672)
        np.testing.assert_allclose(probabilities(memory_amplitude(result["unrestricted_crosstalk_refit"]), 0),
                                   result["candidate"])
        self.assertLess(result["refit_max_error"], 1e-14)

    def test_428_nested_fit_and_finite_sample_rejection(self):
        interior = probabilities(0.06, 0.002)
        counts = np.array([[532, 30, 438], [599, 51, 350]])
        fit = fit_training(counts, np.full(2, 0.02), np.full(2, 0.08))
        np.testing.assert_allclose(fit[0], interior)
        np.testing.assert_allclose(fit[1], probabilities(0.08, DRIFT), atol=1e-9)
        result = self.results["v4.28"]
        for name in ("ordinary_interior", "ordinary_positive_drift_edge",
                     "ordinary_negative_drift_edge", "exact_refit_in_reference_domain"):
            self.assertLessEqual(result[name]["certified_reject"]["rate"], 0.05)
        self.assertGreater(result["ordinary_positive_drift_edge"]["naive_reject"]["rate"], 0.10)
        self.assertGreater(result["separated_positive_control"]["certified_reject"]["rate"], 0.90)

    def test_429_fixed_budget_design_and_independent_validation(self):
        result = self.results["v4.29"]
        self.assertEqual(sum(result["optimized"]), result["budget"])
        self.assertEqual(sum(result["uniform"]), result["budget"])
        self.assertGreater(result["optimized_proxy"], result["uniform_proxy"])
        for point in result["validation"].values():
            self.assertEqual(point["trials"], 4000)

    def test_430_dispersive_ordinary_refit(self):
        result = self.results["v4.30"]
        self.assertLess(result["detuning_mixture_full_reduced_state_error"], 1e-13)
        self.assertLess(result["energy_error"], 1e-13)
        self.assertEqual(result["number_commutator_norm"], 0.0)
        self.assertLess(result["min_photonic_population"], 0.05)

    def test_431_blinded_controls_and_drift(self):
        result = self.results["v4.31"]["unblinded_results"]
        self.assertLess(result["ordinary_calibrated"]["rate"], 0.05)
        self.assertGreater(result["synthetic_separation"]["rate"], 0.90)
        self.assertGreater(result["unmonitored_ordinary_drift"]["rate"], 0.90)
        self.assertLess(result["weak_separation"]["rate"], 0.50)
