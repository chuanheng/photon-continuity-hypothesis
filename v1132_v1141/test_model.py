import unittest
import numpy as np
from .model import run, sector_state


class PhaseTests(unittest.TestCase):
    def test_single_number_twirl(self):
        for p in (0, .13, .5, 1):
            np.testing.assert_allclose(sector_state(p, 1), np.diag([1-p, p]))

    def test_activated_sector(self):
        for p in (.07, .37, .91):
            rho = sector_state(p, 2)
            np.testing.assert_allclose(rho[1:3, 1:3], np.full((2, 2), p*(1-p)))
            np.testing.assert_allclose(np.diag(np.diag(rho)), sector_state(p, 2, independent=True))

    def test_phase_refit(self):
        from scipy.integrate import quad
        from scipy.stats import norm
        predicted = quad(lambda x: np.cos(x)*norm.pdf(x, scale=.8), -9, 9)[0]
        values = run()['differential']
        self.assertAlmostEqual(predicted, values['exchange'], places=12)
        self.assertAlmostEqual(predicted, 1-2*values['equivalent_flip_probability'], places=12)
