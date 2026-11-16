import unittest
import numpy as np
from models.gauge_redundancy_v074 import (
    I, X, Y, Z, K0, K1, I8, G_L, G_R, GAUGE_GROUP, P_PHYSICAL,
    PHYSICAL_BASIS, O_LEFT_CHARGE, O_HOP, kron3, density, commutator,
    is_gauge_invariant, physical_projector, physical_projection, twirl,
    physical_weight, compress, encode_logical, expectation,
    ancilla_extension, restricted_label_expectation,
    extended_gauge_invariant_label_z, summary,
)

class GaugeConstraintsTests(unittest.TestCase):
    def test_generators_commute(self):
        self.assertTrue(np.allclose(commutator(G_L, G_R), 0))

    def test_generators_hermitian(self):
        for g in (G_L, G_R):
            self.assertTrue(np.allclose(g, g.conj().T))

    def test_generators_square_identity(self):
        for g in (G_L, G_R):
            self.assertTrue(np.allclose(g @ g, I8))

    def test_projector_hermitian(self):
        self.assertTrue(np.allclose(P_PHYSICAL, P_PHYSICAL.conj().T))

    def test_projector_idempotent(self):
        self.assertTrue(np.allclose(P_PHYSICAL @ P_PHYSICAL, P_PHYSICAL))

    def test_physical_dimension_two(self):
        self.assertEqual(np.linalg.matrix_rank(physical_projector()), 2)

    def test_basis_orthonormal(self):
        self.assertTrue(np.allclose(PHYSICAL_BASIS.conj().T @ PHYSICAL_BASIS, np.eye(2)))

    def test_basis_spans_physical_projector(self):
        self.assertTrue(np.allclose(PHYSICAL_BASIS @ PHYSICAL_BASIS.conj().T, P_PHYSICAL))

    def test_basis_gauss_law(self):
        for g in (G_L, G_R):
            self.assertTrue(np.allclose(g @ PHYSICAL_BASIS, PHYSICAL_BASIS))

    def test_gauge_group_four_distinct(self):
        self.assertEqual(len(GAUGE_GROUP), 4)
        for i in range(4):
            for j in range(i+1, 4):
                self.assertFalse(np.allclose(GAUGE_GROUP[i], GAUGE_GROUP[j]))

class ObservableTests(unittest.TestCase):
    def test_left_charge_invariant(self):
        self.assertTrue(is_gauge_invariant(O_LEFT_CHARGE))

    def test_hopping_invariant(self):
        self.assertTrue(is_gauge_invariant(O_HOP))

    def test_link_z_not_invariant(self):
        self.assertFalse(is_gauge_invariant(kron3(I, Z, I)))

    def test_logical_z(self):
        self.assertTrue(np.allclose(compress(O_LEFT_CHARGE), Z))

    def test_logical_x(self):
        self.assertTrue(np.allclose(compress(O_HOP), X))

    def test_logical_y_from_operator_product(self):
        self.assertTrue(np.allclose(compress(1j * O_HOP @ O_LEFT_CHARGE), Y))

    def test_gauss_invariant_states_still_distinguishable(self):
        a = encode_logical(density(K0))
        b = encode_logical(density(K1))
        self.assertAlmostEqual(expectation(a, O_LEFT_CHARGE).real, 1)
        self.assertAlmostEqual(expectation(b, O_LEFT_CHARGE).real, -1)

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            is_gauge_invariant(np.eye(2))

class TwirlingTests(unittest.TestCase):
    def setUp(self):
        self.bare = density(kron3(K0, K0, K0))

    def test_twirl_trace_preserving(self):
        self.assertAlmostEqual(np.trace(twirl(self.bare)).real, 1)

    def test_twirl_positive(self):
        self.assertGreaterEqual(np.min(np.linalg.eigvalsh(twirl(self.bare))), -1e-12)

    def test_twirl_idempotent(self):
        self.assertTrue(np.allclose(twirl(twirl(self.bare)), twirl(self.bare)))

    def test_twirl_invariant_under_group(self):
        for g in GAUGE_GROUP:
            self.assertTrue(np.allclose(twirl(g @ self.bare @ g), twirl(self.bare)))

    def test_twirl_same_invariant_expectations(self):
        for obs in [P_PHYSICAL, O_LEFT_CHARGE, O_HOP]:
            self.assertAlmostEqual(expectation(self.bare, obs).real,
                                   expectation(twirl(self.bare), obs).real)

    def test_twirl_does_not_enforce_gauss_law(self):
        self.assertAlmostEqual(physical_weight(twirl(self.bare)), 0.5)
        self.assertFalse(np.allclose(twirl(self.bare),
                                     physical_projection(self.bare)[0]))

    def test_postselected_projector_physical(self):
        projected, weight = physical_projection(self.bare)
        self.assertAlmostEqual(weight, 0.5)
        self.assertAlmostEqual(physical_weight(projected), 1.0)

    def test_projection_zero_weight_raises(self):
        sector_projection = (I8 - G_L) @ (I8 + G_R) / 4
        v = np.linalg.eigh(sector_projection)[1][:, -1]
        with self.assertRaises(ValueError):
            physical_projection(density(v))

class IdentityAncillaTests(unittest.TestCase):
    def setUp(self):
        self.logical = density((K0 + K1) / np.sqrt(2))
        self.a = ancilla_extension(self.logical, 0)
        self.b = ancilla_extension(self.logical, 1)

    def test_joint_states_are_distinct(self):
        self.assertAlmostEqual(np.trace(self.a @ self.b).real, 0)

    def test_restricted_measurements_equal(self):
        for obs in [I8, P_PHYSICAL, O_LEFT_CHARGE, O_HOP, G_L, G_R]:
            self.assertAlmostEqual(
                restricted_label_expectation(self.a, obs).real,
                restricted_label_expectation(self.b, obs).real,
            )

    def test_label_measurement_distinguishes(self):
        obs, gl, gr = extended_gauge_invariant_label_z()
        self.assertAlmostEqual(expectation(self.a, obs).real, +1)
        self.assertAlmostEqual(expectation(self.b, obs).real, -1)

    def test_label_observable_commutes_with_gauss(self):
        obs, gl, gr = extended_gauge_invariant_label_z()
        self.assertTrue(np.allclose(commutator(obs, gl), 0))
        self.assertTrue(np.allclose(commutator(obs, gr), 0))

    def test_invalid_label(self):
        with self.assertRaises(ValueError):
            ancilla_extension(self.logical, 2)

class SummaryTests(unittest.TestCase):
    def test_summary(self):
        r = summary()
        self.assertEqual(r['extended_hilbert_dimension'], 8)
        self.assertEqual(r['physical_hilbert_dimension'], 2)
        self.assertAlmostEqual(r['bare_physical_weight'], 0.5)
        self.assertAlmostEqual(r['gauge_related_bare_overlap'], 0)

    def test_invalid_density(self):
        with self.assertRaises(ValueError):
            density(np.array([2., 0.]))

if __name__ == '__main__':
    unittest.main()
