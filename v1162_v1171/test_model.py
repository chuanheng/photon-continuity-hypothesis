import unittest
import numpy as np
from scipy.linalg import expm
from .model import hamiltonian, state, solve


class DimerTests(unittest.TestCase):
    def test_hopping(self):
        self.assertAlmostEqual(abs(state(0.,.001)[1])**2 / .001**2,2.,places=5)

    def test_dark(self):
        self.assertLess(solve()['dark_eigen_error'],1e-14)

    def test_splitting(self):
        self.assertAlmostEqual(solve()['pair_splitting'][0],(np.sqrt(80)-8)/2)

    def test_peak(self):
        self.assertAlmostEqual(solve()['breakup_peak'],8/80)

    def test_sign_counts(self):
        for t in np.linspace(0,2,17):
            np.testing.assert_allclose(abs(state(8,t))**2,abs(state(-8,t))**2)

    def test_phase(self):
        a,b=solve()['phase_probe']
        self.assertGreater(abs(a-b),.2)

    def test_resonance(self):
        a,b=solve()['tilt_resonance']
        self.assertGreater(b,.8)
        self.assertLess(a,.1)

    def test_loss(self):
        # Independent full master equation including the vacuum.
        from scipy.integrate import solve_ivp
        h=np.zeros((4,4));h[:3,:3]=hamiltonian(8)
        jumps=[]
        for source in (0,2):
            jump=np.zeros((4,4));jump[3,source]=np.sqrt(.18);jumps.append(jump)
        def rhs(t,flat):
            r=flat.reshape(4,4)
            dr=-1j*(h@r-r@h)
            for j in jumps:
                k=j.T@j
                dr+=j@r@j.T-(k@r+r@k)/2
            return dr.ravel()
        initial=np.diag([1.,0.,0.,0.]).astype(complex)
        r=solve_ivp(rhs,(0,.7),initial.ravel(),atol=1e-12,rtol=1e-10).y[:,-1].reshape(4,4)
        np.testing.assert_allclose(solve()['pair_loss'],[1-r[3,3].real,r[1,1].real],atol=1e-9)

    def test_shared_kerr(self):
        self.assertLess(solve()['shared_kerr'],1e-13)

    def test_readback(self):
        r=solve()['dephased_counts']
        self.assertAlmostEqual(r['return_dephased'],3/8)
        self.assertAlmostEqual(r['return_pure'],1)
