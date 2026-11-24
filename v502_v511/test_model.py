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
