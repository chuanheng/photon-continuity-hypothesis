import unittest,numpy as np
from models.process_tomography_v070 import *
class TestProcess(unittest.TestCase):
    def test_completeness(self):
        for g in np.linspace(0,1,11):
            self.assertTrue(np.allclose(sum(k.conj().T@k for k in kraus(g)),np.eye(2)))
    def test_choi(self):
        for g in np.linspace(0,1,11):
            self.assertAlmostEqual(np.trace(choi(g)).real,2)
            self.assertGreaterEqual(np.linalg.eigvalsh(choi(g)).min(),-1e-12)
    def test_reconstruct(self):
        for g in np.linspace(0,1,11):
            self.assertTrue(np.allclose(reconstruct({k:channel(v,g) for k,v in probe_states().items()}),choi(g)))
    def test_aux(self):
        for g in np.linspace(0,1,11):
            for aux in [np.diag([1,0]),np.diag([0,1]),np.eye(2)/2]:
                self.assertTrue(np.allclose(trace_aux(np.kron(channel(probe_states()['one'],g),aux)),channel(probe_states()['one'],g)))
if __name__=='__main__':unittest.main()
