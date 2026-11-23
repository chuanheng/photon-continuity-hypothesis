import unittest

from .model import modulated_rotation,pulsed_loading


class PartialTests(unittest.TestCase):
    def test_rotation(self):
        r = modulated_rotation()
        self.assertLess(r["polarization_summed_spectral_power_error"],1e-14)
        self.assertLess(r["ordinary_rotator_probability_error"],1e-14)
        self.assertGreater(r["common_phase_probability_error"],.2)

    def test_loading(self):
        r = pulsed_loading()
        matched, square = r["matched_and_square_ledgers"]
        self.assertAlmostEqual(matched[0],r["optimal_storage_probability"],places=10)
        self.assertGreater(matched[0],square[0])
        self.assertLess(r["max_ledger_error"],1e-10)
        self.assertAlmostEqual(r["steady_resonant_reflection_amplitude"],0)
