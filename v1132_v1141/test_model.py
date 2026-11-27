import math
import unittest
import numpy as np
from .model import (SEED, accessible_entanglement, all_event_chsh, calibration_trial,
                    crosstalk_chsh, identifiability_audit, permutation_audit, run, sector_state)

class PhaseTests(unittest.TestCase):
    def test_single_number_twirl(self):
        for p in (0,.13,.5,1): np.testing.assert_allclose(sector_state(p,1),np.diag([1-p,p]))
    def test_activated_sector(self):
        for p in (.07,.37,.91):
            rho=sector_state(p,2); np.testing.assert_allclose(rho[1:3,1:3],np.full((2,2),p*(1-p)))
            np.testing.assert_allclose(np.diag(np.diag(rho)),sector_state(p,2,True))
    def test_phase_refit(self):
        from scipy.integrate import quad
        from scipy.stats import norm
        predicted=quad(lambda x:np.cos(x)*norm.pdf(x,scale=.8),-9,9)[0]
        self.assertAlmostEqual(predicted,run()['differential']['exchange'],places=12)
    def test_all_event_bell(self):
        value,weight,conditional=all_event_chsh(.5)
        self.assertAlmostEqual(value,1+math.sqrt(2)); self.assertEqual(weight,.5)
        self.assertAlmostEqual(conditional,2*math.sqrt(2))
    def test_multicopy_identity(self):
        for n in range(1,33): self.assertAlmostEqual(*accessible_entanglement(.37,n),places=12)
        self.assertEqual(accessible_entanglement(.37,1)[0],0)
    def test_loss_dark_is_standard_control(self):
        imperfect=all_event_chsh(.5,.82,.9,.015)[0]
        self.assertGreater(imperfect,2); self.assertLess(imperfect,all_event_chsh(.5)[0])
    def test_crosstalk(self):
        self.assertAlmostEqual(crosstalk_chsh(0)[0],2*math.sqrt(2)); self.assertEqual(crosstalk_chsh(.5)[0],2)
    def test_calibration_reproducible(self):
        a=calibration_trial(SEED); self.assertEqual(a,calibration_trial(SEED)); self.assertLess(abs(a[0]-a[1]),3*a[2])
    def test_quadratic_drift_refit(self):
        r=identifiability_audit(); self.assertGreater(r['candidate_residual_linear'],1)
        self.assertLess(r['candidate_residual_quadratic'],1e-12); self.assertEqual(r['rank_with_candidate'],3)
    def test_permutation_symmetry(self):
        r=permutation_audit(); self.assertGreater(r['labelled_swap_commutator'],1); self.assertEqual(r['symmetric_swap_commutator'],0)
