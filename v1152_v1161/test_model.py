import unittest
from .model import run
class CouplingTests(unittest.TestCase):
    def test_exchange_symmetry(self):
        r=run()['exchange_symmetry']; self.assertEqual(r['invariant_dimension'],10); self.assertGreater(r['slot_commutator'],1); self.assertEqual(r['collective_commutator'],0)
    def test_number_conservation(self):
        r=run()['number_conservation']; self.assertEqual(r['exchange_commutator'],0); self.assertGreater(r['pair_commutator'],1)

import numpy as np
from scipy.linalg import expm
from .ring import hamiltonian, probabilities, solve


class RingTests(unittest.TestCase):
    def test_tree_gauge(self):
        self.assertLess(solve()['tree_gauge'], 1e-14)

    def test_flux_spectrum(self):
        predicted = 2*np.cos((.7+2*np.pi*np.arange(3))/3)
        np.testing.assert_allclose(solve()['flux_spectrum'], np.sort(predicted))

    def test_direction(self):
        p = probabilities(hamiltonian(-.7),.83)
        self.assertAlmostEqual(solve()['direction'], p[0,1]-p[1,0])
        self.assertGreater(abs(solve()['direction']),.4)

    def test_short_time(self):
        self.assertAlmostEqual(solve()['short_time'], -2*np.sin(.7), places=5)

    def test_material_elimination(self):
        self.assertLess(solve()['material_elimination'],1e-13)

    def test_dark_leak(self):
        dark = np.array([1,0,-1])/np.sqrt(2)
        self.assertAlmostEqual(abs((expm(-.83j*hamiltonian(0))@dark)[1]),0)
        self.assertGreater(solve()['dark_leak'],.06)

    def test_efficiency(self):
        raw, calibrated = solve()['efficiency']
        self.assertGreater(raw,.07)
        self.assertLess(abs(calibrated),1e-14)

    def test_heldout(self):
        self.assertLess(solve()['heldout'],1e-14)
