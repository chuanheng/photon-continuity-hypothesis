import unittest
from itertools import combinations

import numpy as np

import process_model as m


class ProcessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.values = {key: value for _, key, value in m.results()}

    def test_v322_tomography(self):
        self.assertLess(self.values['tensor_contraction_error'], 1e-12)
        tensor = m.response_tensor(m.pauli_state(1), [m.SWAP, m.CNOT_E])
        self.assertEqual(tensor.shape, (4,)*5)
        self.assertAlmostEqual(m.contract(tensor, [(m.ZERO, m.I)]*2, m.I), 1)

    def test_v323_causal_break(self):
        self.assertAlmostEqual(m.causal_gap(m.SWAP), 1)
        self.assertAlmostEqual(m.causal_gap(np.eye(4)), 0)

    def test_v324_three_time_marginals(self):
        a, b = m.parity_table(True), m.parity_table(False)
        for pair in combinations(range(3), 2):
            self.assertEqual(m.marginal(a, pair), m.marginal(b, pair))
        self.assertAlmostEqual(self.values['triple_tv'], 0.5)

    def test_v325_bell_coherence(self):
        self.assertAlmostEqual(m.coherence_readout(1, m.PLUS), 0.5)
        self.assertAlmostEqual(m.coherence_readout(-1, m.PLUS), 0)
        self.assertAlmostEqual(self.values['bell_z_branch_gap'], 0)

    def test_v326_phase_echo(self):
        self.assertAlmostEqual(self.values['shared_phase_echo'], 1)
        self.assertAlmostEqual(self.values['fresh_phase_echo'], 0.5)
        np.testing.assert_allclose((m.PLUS + m.Z @ m.PLUS @ m.Z)/2, m.I/2)

    def test_v327_silent_label(self):
        self.assertAlmostEqual(self.values['silent_label_tensor_gap'], 0)

    def test_v328_correlation_erasure(self):
        rho = m.pauli_state(1).reshape(2,2,2,2)
        np.testing.assert_allclose(np.trace(rho, axis1=0, axis2=2), m.I/2)
        np.testing.assert_allclose(np.trace(rho, axis1=1, axis2=3), m.I/2)
        self.assertAlmostEqual(self.values['correlated_vs_product_tensor_gap'], 0.25)

    def test_v329_fair_baseline(self):
        self.assertAlmostEqual(self.values['memoryless_mean_kl'], 0.192744757021758)
        self.assertAlmostEqual(self.values['shared_memory_mean_kl'], 0)

    def test_v330_calibration_profile(self):
        self.assertAlmostEqual(self.values['nominal_residual'], 0.05)
        self.assertAlmostEqual(self.values['profiled_residual'], 0)

    def test_v331_causal_prefix(self):
        self.assertLess(self.values['causal_prefix_error'], 1e-12)
        rho = m.pauli_state(1)
        for first_effect in m.BASIS:
            gates = [m.SWAP, m.CNOT_E]
            prefix = [(m.PLUS, first_effect)]
            expected = m.probability(rho, gates[:1], prefix, m.I)
            for future_effect in m.BASIS:
                branches = [future_effect, m.I - future_effect]
                actual = sum(m.probability(rho, gates, prefix + [(m.ZERO, e)], m.I) for e in branches)
                self.assertAlmostEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
