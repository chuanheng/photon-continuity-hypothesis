import math
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'models'))
from interference_absorption import effective_absorption, populations, first_transfer_absorption_fraction


class InterferenceTests(unittest.TestCase):
    def test_exact_cancellation(self):
        self.assertLess(abs(effective_absorption(1, 1, math.pi)), 1e-12)

    def test_constructive(self):
        self.assertAlmostEqual(abs(effective_absorption(1, 1, 0)), 2)

    def test_unequal_paths_cannot_cancel(self):
        self.assertAlmostEqual(abs(effective_absorption(1, .8, math.pi)), .2)

    def test_phase_error_restores_absorption(self):
        self.assertGreater(first_transfer_absorption_fraction(1, 1, 1, math.pi+.1), 0)

    def test_exact_cancellation_zero_absorption(self):
        self.assertLess(first_transfer_absorption_fraction(1, 1, 1, math.pi), 1e-25)

    def test_normalization(self):
        for phase in (0, .1, math.pi, math.pi+.2):
            for t in (0, .1, 1., 3.):
                p = populations(1, 1, .8, phase, t)
                self.assertAlmostEqual(sum(p), 1., places=12)
                self.assertTrue(all(-1e-12 <= x <= 1+1e-12 for x in p))

    def test_no_coupling(self):
        self.assertEqual(populations(0, 0, 0, 0, 1), (1., 0., 0.))

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError): effective_absorption(-1, 1, 0)
        with self.assertRaises(ValueError): populations(1, 1, 1, 0, -1)
        with self.assertRaises(ValueError): first_transfer_absorption_fraction(0, 0, 0, 0)

    def test_small_phase_error_quadratic(self):
        e = 1e-3
        p = first_transfer_absorption_fraction(1, 1, 1, math.pi+e)
        self.assertAlmostEqual(p/e**2, 1, places=5)

if __name__ == '__main__':
    unittest.main()
