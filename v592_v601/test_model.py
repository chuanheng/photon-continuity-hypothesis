import unittest

from . import model


class MultipleScatteringTests(unittest.TestCase):
    def test_quadrature(self):
        r=model.quadrature()
        self.assertAlmostEqual(r['conditional_probability'],.0007976882084,places=11)
        self.assertLess(r['refinement_difference'],1e-10)
        self.assertLess(r['polarization_reset_probability'],r['conditional_probability'])

    def test_aperture_scaling(self):
        r=model.aperture_scaling()
        self.assertAlmostEqual(r['half_aperture_ratio'],.25,places=3)
        self.assertGreater(r['conditional_probabilities'][-1],.003)

    def test_grazing(self):
        r=model.grazing()
        self.assertGreater(r['infinite_bound_over_naive_square'][0],7)
        self.assertLess(r['second_upper'][-1],.182)
        self.assertGreater(r['two_stage_upper'][-1],.017)

    def test_low_tail(self):
        r=model.low_tail()
        self.assertAlmostEqual(r['tail_mixture_upper'],.00012000647)
        self.assertGreater(r['inflation'],18000)

    def test_intermediate_deflection(self):
        r=model.intermediate_deflection()
        self.assertAlmostEqual(r['qualifying_loss_at_bound'],2)
        self.assertGreater(r['minimum_first_angle_deg'],29.9)
        self.assertLess(r['minimum_first_angle_deg'],r['straight_return_symmetric_angle_deg'])

    def test_thickness_series(self):
        r=model.thickness_series()
        self.assertAlmostEqual(r['central_point_gap'],0)
        self.assertAlmostEqual(r['heldout_max_gap'],.012)
        self.assertAlmostEqual(r['ordinary_linear_nuisance_refit'],0)

    def test_displacement(self):
        r=model.displacement()
        self.assertEqual(r['resolvable_at_fixed_tolerance'],[False,True,True])
        self.assertAlmostEqual(r['ideal_shift_mm'][0],.0346410162)

    def test_recoil_records(self):
        r=model.recoil_records()
        self.assertLess(r['sum_energy_error'],1e-11)
        self.assertAlmostEqual(r['net_transverse_recoil'],0)
        self.assertGreater(r['individual_transverse_recoil'],49)

    def test_repeated_limit(self):
        r=model.repeated_collision_limits()
        self.assertEqual(r['minimum_collisions_for_20kev_loss'],3)
        self.assertGreater(r['kinematic_any_direction_max_losses_kev'][-1],29)
        self.assertEqual(r['all_backscatter_exit_direction_z'][-1],1)

    def test_combined_design(self):
        r=model.combined_design()
        self.assertEqual(r['joint_rank'],3)
        self.assertGreater(r['ordinary_without_linear_floor'],.009)
        self.assertLess(r['ordinary_with_linear_refit_error'],1e-14)
