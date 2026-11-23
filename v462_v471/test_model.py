import unittest

from .controls import (allpass_delay, bell_bounds, environment_eraser, finite_reference,
                       heldout_design, joint_null, rotating_wave)
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


class FurtherTests(unittest.TestCase):
    def test_rotating_wave(self):
        r = rotating_wave()
        self.assertLess(r["rwa_formula_error"], 1e-12)
        self.assertLess(r["cutoff_errors"][1], .0001)
        self.assertGreater(r["rwa_gaps"][1], 10*r["rwa_gaps"][0])

    def test_bell(self):
        r = bell_bounds()
        self.assertLess(r["max_chsh"][0], 2)
        self.assertGreater(r["max_chsh"][1], 2)
        self.assertLess(r["explicit_setting_max_error"], 1e-14)

    def test_eraser(self):
        r = environment_eraser()
        self.assertAlmostEqual(r["conditional_visibility"], .76)
        self.assertLess(r["conditional_error"], 1e-14)
        self.assertLess(r["unconditional_error"], 1e-14)

    def test_delay(self):
        r = allpass_delay()
        self.assertLess(r["intensity_error"], 1e-14)
        self.assertAlmostEqual(r["center_group_delay"], 2/.74, delta=5e-7)
        self.assertLess(r["finite_difference_max_error"], 5e-7)
        self.assertLess(r["untracked_reference_error"], 1e-11)

    def test_reference(self):
        r = finite_reference()
        for levels, measured, uniform, bound in r["results"]:
            self.assertAlmostEqual(measured,bound)
            if levels >= 4:
                self.assertGreater(measured,uniform)

    def test_joint_null(self):
        r = joint_null()
        self.assertAlmostEqual(r["distance"][0],r["small_cap_dual_bound"])
        self.assertAlmostEqual(r["distance"][1],0)
        self.assertLessEqual(sum(r["fits"][0][:2]),.22+1e-12)

    def test_heldout(self):
        r = heldout_design()
        self.assertLess(r["exact_boundary_size"],r["nominal_size_bound"])
        self.assertAlmostEqual(r["exact_power"],r["simulated_power"],delta=.001)
        self.assertGreater(r["exact_power"],.99)
        self.assertLess(r["nearby_power_at_0p355"],.9)
