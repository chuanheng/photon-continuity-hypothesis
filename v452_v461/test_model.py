import unittest

from . import model


class OpticalTests(unittest.TestCase):
    def test_efficiency(self):
        r = model.efficiency_product()
        self.assertEqual((r["no_calibration_rank"], r["calibrated_rank"]), (1, 2))
        self.assertLess(r["refit_max_error"], 1e-14)
        self.assertAlmostEqual(r["source_interval"][0], .252/.37)
        self.assertAlmostEqual(r["source_interval"][1], .72)

    def test_dead_time(self):
        r = model.dead_time()
        self.assertAlmostEqual(r["simulated_rate"], r["stationary_rate"], delta=.002)
        for k, (simulation, theory) in r["lag_covariance_simulation_and_theory"].items():
            self.assertAlmostEqual(simulation, theory, delta=.002)
            self.assertGreater(simulation*(-1)**int(k), 0)

    def test_afterpulse(self):
        r = model.afterpulse_probe()
        self.assertLess(r["passive_max_error"], 1e-14)
        self.assertAlmostEqual(r["second_detector_contrast"], .97*.16*.55)
        self.assertAlmostEqual(r["transfer_needed_to_refit"], .088)

    def test_thermal_loss(self):
        r = model.thermal_loss()
        self.assertAlmostEqual(r["equivalent_source_mean"], .44)
        self.assertLess(r["pmf_max_error"], 1e-14)
        self.assertAlmostEqual(r["click_probability"], .44/1.44)
        self.assertLess(r["bath_tail_bound"], 1e-18)

    def test_coherent_storage(self):
        r = model.coherent_storage()
        self.assertAlmostEqual(r["min_output_population"], 1)
        for key in ("max_capture_error", "phase_transfer_error", "excitation_error"):
            self.assertLess(r[key], 1e-14)

    def test_temporal_gate(self):
        r = model.temporal_gate()
        self.assertAlmostEqual(r["full_overlap_squared"], r["full_overlap_exact"], delta=.00024)
        self.assertAlmostEqual(r["conditional_overlap_squared"], 1)
        self.assertAlmostEqual(r["acceptance_ratio"], r["full_overlap_exact"])
        self.assertLess(r["acceptances"][0], r["acceptances"][1])

    def test_gaussian_cp(self):
        r = model.gaussian_cp()
        self.assertAlmostEqual(r["cp_min_eigenvalue"], -.03)
        self.assertLess(r["vacuum_output_variance"], .5)
        self.assertAlmostEqual(r["ordinary_refit_error"], 0)

    def test_phase_reference(self):
        r = model.phase_reference()
        self.assertAlmostEqual(r["shared_visibility"], 1)
        self.assertLess(r["independent_visibility"], 1e-14)
        self.assertLess(r["population_error"], 1e-14)

    def test_missing_bounds(self):
        r = model.missing_bounds()
        self.assertAlmostEqual(r["sharp_contrast_interval"][0], -.348)
        self.assertAlmostEqual(r["sharp_contrast_interval"][1], .552)
        self.assertTrue(all(0 <= p <= 1 for p in r["equal_marginal_refit"]))
        self.assertAlmostEqual(r["ordinary_refit_error"], 0)

    def test_sidebands(self):
        r = model.driven_sidebands()
        self.assertLess(r["sum_loss"], 1e-14)
        self.assertLess(r["bessel_max_error"], 1e-14)
        self.assertGreater(r["biased_mean_order"], .38)
        self.assertLess(abs(r["calibrated_mean_order"]), 1e-14)
