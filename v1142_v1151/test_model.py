import unittest
import numpy as np
from .model import (SEED, calibrated_distance, convex_refit, cross_kerr_channel,
                    finite_power, hidden_and_classical_histories, hom_coincidence,
                    reset_witness, silent_label_theorem, swap_storage_fidelity)

class IdentityAuditTests(unittest.TestCase):
    def test_hom(self):
        self.assertEqual(hom_coincidence(1),0); self.assertEqual(hom_coincidence(0),.5)
    def test_swap_storage(self):
        rho=np.array([[.5,.5j],[-.5j,.5]],complex); self.assertAlmostEqual(swap_storage_fidelity(rho),1)
    def test_history_equivalence(self): self.assertLess(hidden_and_classical_histories()[0],1e-14)
    def test_static_memory(self):
        static,reset,_=reset_witness(); self.assertNotAlmostEqual(static,reset)
    def test_system_break_not_environment_break(self):
        static,reset,system=reset_witness(); self.assertEqual(static,system); self.assertNotEqual(reset,system)
    def test_cross_kerr_cp(self):
        _,eigs=cross_kerr_channel(); self.assertGreaterEqual(min(eigs),-1e-14)
    def test_convex_refit(self): self.assertLess(convex_refit()[0],1e-14)
    def test_calibration_family_dependence(self):
        restricted,expanded=calibrated_distance(); self.assertGreater(restricted,.01); self.assertLess(expanded,1e-14)
    def test_finite_power_reproducible(self):
        a=finite_power(SEED); self.assertEqual(a,finite_power(SEED)); self.assertLess(a[0],.1); self.assertGreater(a[1],.5)
    def test_silent_label(self): self.assertLess(silent_label_theorem(),1e-14)
