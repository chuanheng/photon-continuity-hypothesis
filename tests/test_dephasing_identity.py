import sys,unittest,pathlib
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from dephasing_identity import *
class TestDephasingIdentity(unittest.TestCase):
    def test_identical(self): self.assertAlmostEqual(hom_probability([1,0],[1,0]),0)
    def test_orthogonal(self): self.assertAlmostEqual(hom_probability([1,0],[0,1]),.5)
    def test_partial(self): self.assertAlmostEqual(hom_probability([1,0],[1,1]),.25)
    def test_normalization(self): self.assertAlmostEqual(overlap_squared([2,0],[0,3]),0)
    def test_phase_damping_identity(self):
        r=np.array([[.5,.5],[.5,.5]]); self.assertTrue(np.allclose(phase_damping(r,1),r))
    def test_phase_damping_full(self):
        r=np.array([[.5,.5],[.5,.5]]); self.assertTrue(np.allclose(phase_damping(r,0),np.diag([.5,.5])))
    def test_trace_preserved(self):
        r=np.array([[.5,.5],[.5,.5]])
        for eta in np.linspace(0,1,51): self.assertAlmostEqual(np.trace(phase_damping(r,eta)).real,1)
    def test_positive(self):
        r=np.array([[.5,.5],[.5,.5]])
        for eta in np.linspace(0,1,51): self.assertGreaterEqual(np.linalg.eigvalsh(phase_damping(r,eta)).min(),-1e-12)
    def test_equivalence(self):
        for x in np.linspace(0,1,101): self.assertEqual(visibility_from_hidden_label(float(x)),visibility_from_environment_overlap(float(x)))
    def test_coincidence(self): self.assertAlmostEqual(coincidence_from_visibility(.6),.2)
    def test_kl_zero(self): self.assertAlmostEqual(binomial_kl(.2,.2),0)
    def test_kl_positive(self): self.assertGreater(binomial_kl(.2,.4),0)
    def test_llr_zero(self): self.assertAlmostEqual(expected_llr(.2,.2,1000),0)
    def test_llr_positive(self): self.assertGreater(expected_llr(.2,.4,1000),0)
    def test_invalid_eta(self):
        with self.assertRaises(ValueError): phase_damping(np.eye(2),1.1)
    def test_invalid_visibility(self):
        with self.assertRaises(ValueError): coincidence_from_visibility(-.1)
    def test_invalid_state(self):
        with self.assertRaises(ValueError): normalized([0,0])
    def test_invalid_kl(self):
        with self.assertRaises(ValueError): binomial_kl(.2,0)
if __name__=='__main__': unittest.main()
