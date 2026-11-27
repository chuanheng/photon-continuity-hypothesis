import unittest
import numpy as np
from .model import run,encoded,overlap
class Reference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_energy(self):
        self.assertEqual(self.r['conservation']['energy_defect'],0);self.assertLess(self.r['conservation']['gram_error'],1e-14)
    def test_choi(self):
        bell=np.zeros((2,5));bell[0,[0,4]]=.5;bell[1,2]=1/np.sqrt(2)
        for amp,f in [(np.array([1.]),.625),(np.ones(16)/4,.90625)]:
            out=np.einsum('rb,snb->rsn',np.eye(2)/np.sqrt(2),encoded(amp))
            self.assertAlmostEqual(np.linalg.norm(np.einsum('rs,rsn->n',bell,out))**2,f)
    def test_translate(self):self.assertAlmostEqual(*self.r['energy_shift'].values())
    def test_opt(self):self.assertAlmostEqual(self.r['optimized']['max_g4'],np.cos(np.pi/5))
    def test_worst(self):
        u=np.linspace(0,1,501)/2
        self.assertAlmostEqual(min(1-2*u*(1-u)*.25),self.r['worst_input']['worst'])
    def test_phase(self):
        a=np.exp(1j*.08*np.arange(16))/4
        self.assertAlmostEqual(overlap(a,4).real,self.r['phase_drift']['known_offset_g'])
    def test_which(self):
        d=self.r['which_shift'];self.assertAlmostEqual(d['overlap']**2+d['trace_distance']**2,1)
    def test_eraser(self):self.assertAlmostEqual(self.r['eraser']['accept'],.875)
    def test_reuse(self):self.assertAlmostEqual(self.r['reuse']['shared_g8'],8/16)
    def test_population(self):
        for amp in [np.array([1.]),np.ones(16)/4]:
            v=encoded(amp)[:,:,0];np.testing.assert_allclose(np.diag(v@v.conj().T),[.5,0,0,0,.5])
