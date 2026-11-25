import unittest

from . import model


class FoilTransportTests(unittest.TestCase):
    def test_cross_sections(self):
        r=model.cross_sections()
        self.assertLess(r['sum_error'],1e-10)
        self.assertLess(abs(r['relative_total_difference']),4e-5)

    def test_primary(self):
        r=model.primary_beam()
        self.assertAlmostEqual(r['first_compton_probability'],r['analytic_first_compton'])
        self.assertAlmostEqual(r['uncollided_survival'],r['nist_survival'],places=5)

    def test_finite_geometry(self):
        r=model.boundary_escape()
        self.assertGreater(r['reference_rate_per_incident'],1.5e-6)
        self.assertLess(r['reference_rate_per_incident'],1.65e-6)
        self.assertLess(r['narrow_radius_rate'],r['reference_rate_per_incident'])
        self.assertGreater(r['wide_radius_rate'],r['reference_rate_per_incident'])

    def test_response_sensitivity(self):
        r=model.response_tail()
        self.assertGreater(r['broadened_over_core'],1e5)

    def test_polarization_aperture(self):
        r=model.polarization_aperture()
        self.assertGreater(r['polarization_ratio'],1.5)
        self.assertAlmostEqual(r['aperture_ratio'],.25,places=3)

    def test_two_integrators(self):
        r=model.independent_integrators()
        self.assertLess(r['relative_disagreement'],.005)

    def test_geometry_scenarios(self):
        r=model.geometry_error()
        self.assertLess(r['scenario_min'],r['nominal'])
        self.assertLess(r['nominal'],r['scenario_max'])

    def test_independent_background(self):
        r=model.independent_background()
        self.assertGreater(r['detector_tail_upper'],r['ordinary_two_compton_estimate'])

    def test_hidden_label(self):
        r=model.kinematic_identity()
        self.assertAlmostEqual(r['probability_sum'],1.)
        self.assertAlmostEqual(r['visible_total_variation'],0.)
        self.assertGreater(r['hidden_joint_total_variation'],.8)

    def test_feasibility(self):
        r=model.feasibility()
        self.assertEqual(r['grid_exposure'],2700000)
        self.assertGreaterEqual(r['power'],.9)
        self.assertLessEqual(r['size'],.025)
