import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "models"))
import spectral_discrimination as s


class SpectralTests(unittest.TestCase):
    def test_no_extra_counts(self):
        self.assertEqual(s.expected_counts(0), s.BASELINE)

    def test_amplitude_conserves_extra_count(self):
        self.assertAlmostEqual(sum(s.expected_counts(100))-sum(s.BASELINE), 100)

    def test_asimov_zero_and_increases(self):
        self.assertAlmostEqual(s.asimov_discovery_q(0), 0)
        self.assertGreater(s.asimov_discovery_q(100), s.asimov_discovery_q(50))

    def test_invalid_amplitude(self):
        with self.assertRaises(ValueError):
            s.expected_counts(-1)

    def test_identical_shape_is_unidentifiable_with_free_scale(self):
        b = (10.0, 20.0, 30.0)
        t = (1/6, 1/3, 1/2)
        self.assertAlmostEqual(s.nuisance_degeneracy(b, t), 1.0)
        self.assertAlmostEqual(s.profiled_information_free_normalization(b, t), 0)

    def test_nonidentical_shape_retains_information(self):
        self.assertGreater(s.profiled_information_free_normalization(), 0)


if __name__ == "__main__":
    unittest.main()
