import unittest

from .model import SEED, run


class IdentityLabelAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = run()

    def test_v872(self): self.assertEqual((self.r["v8.72"]["global_trace_distance"], self.r["v8.72"]["accessible_trace_distance"]), (1.0, 0.0))
    def test_v873(self): self.assertEqual(self.r["v8.73"]["label_only_accessible_change"], 0.0)
    def test_v874(self):
        self.assertEqual(self.r["seed"], SEED)
        self.assertLess(self.r["v8.74"]["random_factorized_accessible_distance"], 1e-14)
        self.assertLess(self.r["v8.74"]["unitarity_error"], 1e-14)
    def test_v875(self):
        self.assertAlmostEqual(self.r["v8.75"]["coupled_accessible_trace_distance"], 1.0)
        self.assertEqual(self.r["v8.75"]["coupling_unitarity_error"], 0.0)
    def test_v876(self): self.assertEqual(self.r["v8.76"]["candidate_ordinary_max_difference"], 0.0)
    def test_v877(self): self.assertEqual((self.r["v8.77"]["labeled_assignment_distance"], self.r["v8.77"]["accessible_occupation_distance"]), (1.0, 0.0))
    def test_v878(self):
        self.assertEqual(self.r["v8.78"]["replacement_output_distance"], 0.0)
        self.assertEqual(self.r["v8.78"]["choi_rank"], 2)
        self.assertAlmostEqual(self.r["v8.78"]["choi_trace"], 1.0)
    def test_v879(self): self.assertEqual((self.r["v8.79"]["candidate_vs_ordinary_memory_tv"], self.r["v8.79"]["candidate_vs_memoryless_tv"]), (0.0, 0.5))
    def test_v880(self): self.assertEqual(self.r["v8.80"]["finite_control_max_difference"], 0.0)
    def test_v881(self):
        self.assertGreater(self.r["v8.81"]["restricted_ordinary_distance"], 0.0)
        self.assertLess(self.r["v8.81"]["expanded_ordinary_distance"], 1e-14)


if __name__ == "__main__":
    unittest.main()
