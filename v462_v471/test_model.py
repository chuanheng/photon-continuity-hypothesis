import unittest

from .model import cavity_ledger, gauge_probe, rotation_fit


class PreliminaryTests(unittest.TestCase):
    def test_gauge(self):
        r = gauge_probe()
        self.assertLess(r["field_max_gauge_error"], 1e-14)
        self.assertLess(r["conserved_current_max_gauge_error"], 1e-14)
        self.assertAlmostEqual(r["bare_timelike_current_min_change"], .7)

    def test_rotation(self):
        r = rotation_fit()
        self.assertLess(r["eikonal_max_error_rad"], 1e-7)
        bound = r["certified_calibrated_lower_bound_rad"]
        self.assertGreater(bound, .006)
        self.assertGreaterEqual(r["calibrated_max_residual_rad"], bound-1e-11)
        self.assertLess(r["free_offset_max_residual_rad"], 1e-7)

    def test_cavity(self):
        r = cavity_ledger()
        self.assertLess(r["ledger_max_error"], 1e-14)
        self.assertLess(r["ode_closed_form_error"], 1e-10)
        stored, measured, internal = r["final_probabilities_stored_out_internal"]
        self.assertAlmostEqual(measured/(1-stored), .7)
        self.assertAlmostEqual(internal/(1-stored), .3)
