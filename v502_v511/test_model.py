import unittest
from . import model


class SourceControlsTests(unittest.TestCase):
    def test_two_beam_source(self):
        result=model.two_beam_source()
        self.assertLess(result["kinematic_error"],1e-14)
        self.assertLess(result["mass_shell_error"],1e-14)
        self.assertAlmostEqual(result["collinear_source"],0)
        self.assertAlmostEqual(result["counterpropagating_source"],-8)
        self.assertAlmostEqual(result["orthogonal_max_source"],0)
        self.assertLess(result["ordinary_angular_refit_error"],1e-14)

    def test_finite_converter(self):
        result=model.finite_converter()
        self.assertLess(result["uniform_normalized_power"],1e-28)
        self.assertAlmostEqual(result["switched_normalized_power"],4/3.141592653589793**2)
        self.assertLess(result["uniform_quadrature_error"],1e-14)
        self.assertLess(result["switched_quadrature_error"],1e-14)

    def test_clipped_readout(self):
        result=model.clipped_readout()
        self.assertGreater(result["fisher_ratio_mu_20"],.99)
        self.assertLess(result["fisher_ratio_mu_80"],.01)
        self.assertLess(result["derivative_check_error"],1e-8)
        self.assertLess(result["leakage_refit_error"],1e-12)


class DeviceControlsTests(unittest.TestCase):
    def test_propagation_planes(self):
        result = model.controls.propagation_planes()
        self.assertLess(result["single_plane_error"], 1e-14)
        self.assertGreater(result["margin"], .06)
        self.assertLess(result["aliased_plane_error"], 1e-14)
        self.assertLess(result["ordinary_two_path_error"], 1e-14)

    def test_chopping_parity(self):
        result = model.controls.chopping_parity()
        self.assertAlmostEqual(result["odd_harmonics"][0], .504)
        self.assertAlmostEqual(result["odd_harmonics"][1], 0)
        self.assertAlmostEqual(result["even_harmonics"][1], .063)
        self.assertLess(result["ordinary_mixer_error"], 1e-14)

    def test_reset_logs(self):
        result = model.controls.reset_logs()
        self.assertEqual(result["final_energies"], [.5, .5])
        self.assertEqual(result["final_quadratures"], [1., 0.])
        self.assertAlmostEqual(result["initial_quadrature"], -1.)

    def test_zero_event_limit(self):
        result = model.controls.zero_event_limit()
        self.assertAlmostEqual(result["efficiency_lower"]**60, .025)
        self.assertAlmostEqual((1-result["observed_event_upper"])**2000, .025)
        self.assertAlmostEqual(result["joint_coverage_lower"], .95)
        self.assertGreater(result["independent_cluster_upper"], 80*result["observed_event_upper"])

    def test_lifetime_mixture(self):
        result = model.controls.lifetime_mixture()
        self.assertAlmostEqual(sum(result["bins"]), 1.)
        self.assertGreater(result["early_hazard"], result["late_hazard"])
        self.assertLess(result["max_hazard_slope"], 0.)
        self.assertLess(result["detector_latency_refit_error"], 1e-14)

    def test_memory_dimension(self):
        result = model.controls.memory_dimension()
        self.assertEqual(result["certified_rank"], 3)
        self.assertGreater(result["singular_values"][2], result["operator_radius"])
        self.assertLess(result["ordinary_three_pole_error"], 1e-14)

    def test_preregistered_disk(self):
        result = model.controls.preregistered_disk()
        self.assertAlmostEqual(result["global_distance"], .06)
        self.assertAlmostEqual(result["nearest_point_residual"], .06)
        self.assertGreaterEqual(result["grid_distance"], result["global_distance"])
        self.assertLess(result["reopened_port_refit_error"], 1e-14)
