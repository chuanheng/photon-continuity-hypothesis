import unittest
from .model import SEED, run


class HamiltonianAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.r = run()
    def test_v882(self): self.assertEqual(self.r["v8.82"]["energy_commutator_norm"], 0.0)
    def test_v883(self): self.assertEqual(self.r["v8.83"]["fixed_number_label_trace_distance"], 0.0)
    def test_v884(self): self.assertAlmostEqual(self.r["v8.84"]["ramsey_label_trace_distance"], self.r["v8.84"]["analytic_sin_gt"])
    def test_v885(self): self.assertLess(self.r["v8.85"]["ordinary_detuning_max_difference"], 1e-14)
    def test_v886(self):
        self.assertEqual(self.r["seed"], SEED)
        self.assertAlmostEqual(self.r["v8.86"]["random_state_norm"], 1.0)
    def test_v887(self):
        self.assertGreater(self.r["v8.87"]["asymmetric_swap_commutator_norm"], 0.0)
        self.assertEqual(self.r["v8.87"]["symmetric_swap_commutator_norm"], 0.0)
    def test_v888(self): self.assertEqual(self.r["v8.88"]["remote_change_under_label_local_unitary"], 0.0)
    def test_v889(self):
        self.assertEqual(self.r["v8.89"]["exchange_total_number_commutator_norm"], 0.0)
        self.assertAlmostEqual(self.r["v8.89"]["swap_probability"], self.r["v8.89"]["analytic_swap_probability"])
    def test_v890(self): self.assertLess(self.r["v8.90"]["standard_channel_max_difference"], 1e-14)
    def test_v891(self): self.assertEqual(self.r["v8.91"]["nine_time_candidate_ordinary_max_difference"], 0.0)


if __name__ == "__main__": unittest.main()
