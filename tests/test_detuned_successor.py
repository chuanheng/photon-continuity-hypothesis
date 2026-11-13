import math
import pathlib
import sys
import unittest
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from detuned_successor import detunings,hamiltonian,evolve,probabilities

class Tests(unittest.TestCase):
    def test_detunings(self): self.assertEqual(detunings(10,2,8,10),(0,0))
    def test_distinct_states(self): self.assertEqual(detunings(10,2,8,8),(0,-2))
    def test_hermitian(self):
        h=hamiltonian(1,2,3,-4)
        self.assertTrue(np.allclose(h,h.conj().T))
    def test_initial(self): self.assertTrue(np.allclose(evolve(1,1,2,3,0),[1,0,0]))
    def test_norm(self):
        for t in (0,.1,1,10): self.assertAlmostEqual(sum(probabilities(1,.7,.3,-.4,t)),1,places=12)
    def test_absorption_forbidden_when_g_zero(self):
        for t in (.1,1,5): self.assertAlmostEqual(probabilities(1,0,.5,0,t)[2],0,places=12)
    def test_successor_forbidden_when_kappa_zero(self):
        self.assertAlmostEqual(probabilities(0,1,0,.5,2)[1],0,places=12)
    def test_no_coupling(self): self.assertTrue(np.allclose(probabilities(0,0,1,2,100),[1,0,0]))
    def test_resonant_analytic(self):
        p=probabilities(1,1,0,0,math.pi/(2*math.sqrt(2)))
        self.assertAlmostEqual(p[0],0,places=12)
        self.assertAlmostEqual(p[1],.5,places=12)
        self.assertAlmostEqual(p[2],.5,places=12)
    def test_off_resonance_suppression(self):
        k,d=1,6
        t=math.pi/math.sqrt(d*d+4*k*k)
        self.assertAlmostEqual(probabilities(k,0,d,0,t)[1],4*k*k/(d*d+4*k*k),places=12)
    def test_energy_expectation_conserved(self):
        h=hamiltonian(1,.7,.3,-.4)
        for t in (.1,1,10):
            psi=evolve(1,.7,.3,-.4,t)
            self.assertAlmostEqual(float(np.vdot(psi,h@psi).real),0,places=12)
    def test_invalid_energy(self):
        with self.assertRaises(ValueError): detunings(10,0,8,10)
    def test_invalid_coupling(self):
        with self.assertRaises(ValueError): hamiltonian(-1,0,0,0)
    def test_invalid_time(self):
        with self.assertRaises(ValueError): evolve(1,0,0,0,-1)
    def test_nan(self):
        with self.assertRaises(ValueError): hamiltonian(1,0,float("nan"),0)

if __name__=="__main__": unittest.main()
