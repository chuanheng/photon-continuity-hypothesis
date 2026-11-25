import unittest

from . import model


class MetalControlsTests(unittest.TestCase):
    def test_ledger(self):
        r = model.ledger()
        self.assertAlmostEqual(r['closure'],1.)
        self.assertAlmostEqual(r['unmeasured_energy'],.098)
        self.assertAlmostEqual(r['nist_60kev_primary_survival'],.9277379199)

    def test_aperture(self):
        r = model.aperture()
        self.assertAlmostEqual(r['single_aperture_flat_refit'],r['ordinary_transmission'][1])
        self.assertGreater(r['wider_aperture_gap'],.027)

    def test_film(self):
        r = model.film()
        self.assertLess(r['independently_integrated_closure_error'],1e-8)
        self.assertGreater(r['transmission_range'],.018)

    def test_calorimetry(self):
        r = model.calorimetry()
        self.assertEqual(r['correlated_max_closure_error'],0)
        self.assertEqual(r['swapped_same_marginal_max_error'],18)
        self.assertEqual(r['linked_covariance'],-r['swapped_covariance'])

    def test_scattering(self):
        r = model.scattering_tail()
        self.assertLess(r['single_loss_in_3deg_kev'],.01)
        self.assertAlmostEqual(r['two_scatter_loss_kev'],6.3047285464)
        self.assertAlmostEqual(r['total_recoil_momentum_kev_over_c'][-1],r['two_scatter_loss_kev'])
        self.assertLess(r['gaussian_single_false_tail_upper'],1e-8)

    def test_common_material(self):
        r = model.common_material()
        self.assertAlmostEqual(r['recovered_shared_scale'],1.04)
        self.assertLess(r['homogeneous_heldout_error'],1e-14)
        self.assertGreater(r['mismatched_heldout_error'],.025)

    def test_redistribution(self):
        r = model.redistribution()
        self.assertAlmostEqual(r['ordinary_max'],.078)
        self.assertAlmostEqual(r['monitor_load'],.048)
        self.assertAlmostEqual(r['wider_ordinary_exact_refit_error'],0.)

    def test_rare_counts(self):
        r = model.rare_counts()
        self.assertEqual(r['required_shots'],23706)
        self.assertGreaterEqual(r['heldout_power'],.9)
        self.assertLess(r['lower_n_max_power'],.9)
        self.assertLess(r['worst_case_null_tail'],.025)

    def test_collinear_recoil(self):
        r = model.collinear_recoil()
        self.assertGreater(r['target_mass_increase_kev'],5.9)
        self.assertLess(r['free_recoil_kinetic_kev'],.04)
        self.assertAlmostEqual(r['energy_closure_with_excitation'],0.)

    def test_joint_gate(self):
        r = model.joint_gate()
        self.assertAlmostEqual(r['third_bin_gap_with_calibration_radius'],.025)
        self.assertAlmostEqual(r['expanded_ordinary_refit'],0.)
