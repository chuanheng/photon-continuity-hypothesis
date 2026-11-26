import unittest
import numpy as np
from numpy.testing import assert_allclose
from .model import receiver,extremum,run

class Selection(unittest.TestCase):
    def test_product_state_preparation(self):
        # Independent density-matrix calculation on three dephased Bell states.
        X=np.array([[0,1],[1,0]])
        Y=np.array([[0,-1j],[1j,0]])
        Z=np.diag([1,-1])
        observables=[np.kron(p,p.conj()) for p in (X,Y,Z)]
        coefficients=np.array([[np.trace((np.eye(4)+o)@v).real/4 for v in observables] for o in observables])
        assert_allclose(coefficients,np.eye(3))
        h,c=receiver(8)
        assert_allclose(h,.093)
        assert_allclose(c,.8)

    def test_global_bound(self):
        for k in (1,1.5,2,4,8,32):
            self.assertAlmostEqual(extremum(k),(1+3*k/(k+2))/4)
            self.assertAlmostEqual((1+receiver(k)[1].sum())/4,extremum(k))
        self.assertAlmostEqual(extremum(run()['ratio_to_fake_093_fidelity']),.93)
