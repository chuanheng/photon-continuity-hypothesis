import unittest
import numpy as np
from .model import moments,run
class Reuse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_fourier(self):
        z=self.r['phase_representation'];self.assertLess(z['max_error'],1e-14);self.assertAlmostEqual(z['weights_sum'],1)
    def test_moments(self):
        z=self.r['moment_bound'];a=np.arccos(z['g4'])
        self.assertAlmostEqual(np.cos(2*a),z['lower']);self.assertAlmostEqual(.875-.125,z['g4'])
    def test_floor(self):
        # Two unit deductions require an initial energy of at least two.
        self.assertEqual(sum(m>=2 for m in range(1,17))/16,self.r['boundary']['success_both'])
    def test_kerr(self):
        ratio=abs(np.sin(16*4*.035)/(16*np.sin(4*.035)))
        self.assertAlmostEqual(ratio,self.r['interposed_kerr']['visibility'])
    def test_number(self):
        self.assertAlmostEqual(self.r['number_access']['energy_TV'],.25)
        self.assertGreater(self.r['number_access']['optimal_pure_TV'],.25)
    def test_loop(self):
        z=self.r['loop'];self.assertAlmostEqual(z['phase'],1.12);self.assertAlmostEqual(z['visibility'],1)
    def test_refit(self):self.assertLess(self.r['classical_kick_fit']['complex_error'],1e-14)
    def test_ent(self):
        g=.75;a=np.array([1.,0.]);b=np.array([g,np.sqrt(1-g*g)])
        psi=np.r_[a,b]/np.sqrt(2);pt=np.outer(psi,psi).reshape(2,2,2,2).transpose(0,3,2,1).reshape(4,4)
        self.assertAlmostEqual(-min(np.linalg.eigvalsh(pt)),self.r['pump_entanglement']['negativity'])
    def test_bell(self):
        z=self.r['bell_test'];self.assertAlmostEqual(z['ideal']*z['critical_white_visibility'],2);self.assertGreater(z['ideal'],2)
    def test_twirled(self):
        L=np.r_[np.zeros(4),np.ones(16)/4];R=L[::-1]
        self.assertAlmostEqual(sum((a*a+b*b)/2 for a,b in zip(L,R)),self.r['energy_superselection']['joint_trace'])
        self.assertGreaterEqual(min(min(np.linalg.eigvalsh(np.outer([a,b],[a,b])/2)) for a,b in zip(L,R)),-1e-15)
