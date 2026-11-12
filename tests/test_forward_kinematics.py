"""Run: python3 -m unittest discover -s tests -v"""
import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "models"))
import forward_kinematics as k


class ForwardKinematicsTests(unittest.TestCase):
    def test_elastic_forward_loss_zero(self):
        self.assertEqual(k.forward_energy_loss(k.ELECTRON_REST_KEV, 0), 0)

    def test_inelastic_loss_exceeds_excitation(self):
        r, u = k.PROTON_REST_KEV, 0.001
        loss = k.forward_energy_loss(r, u)
        self.assertGreater(loss, u)
        self.assertAlmostEqual(loss - u, u*u/(2*r), places=16)

    def test_invariant_conservation(self):
        self.assertAlmostEqual(k.invariant_residual(1000, 10), 0, places=10)

    def test_kinematic_threshold(self):
        with self.assertRaises(ValueError):
            k.final_photon_energy(1, 1000, 1)

    def test_compton_forward(self):
        self.assertEqual(k.compton_scattered_energy(60, 0), 60)

    def test_compton_right_angle(self):
        expected = 60 / (1 + 60 / k.ELECTRON_REST_KEV)
        self.assertAlmostEqual(k.compton_scattered_energy(60, math.pi/2), expected)


if __name__ == "__main__":
    unittest.main()
