import sys, pathlib, unittest
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from internal_bosons import *
class TestBosonInternal(unittest.TestCase):
    def test_swap_unitary(self):
        for d in range(2,7):
            s=swap_operator(d); self.assertTrue(np.allclose(s@s,np.eye(d*d)))
    def test_projector(self):
        for d in range(2,7):
            p=symmetric_projector(d)
            self.assertTrue(np.allclose(p@p,p)); self.assertAlmostEqual(np.trace(p).real,d*(d+1)/2)
    def test_pair(self):
        for d in range(2,7):
            for i in range(d):
                for j in range(d):
                    a=np.eye(d)[i]; b=np.eye(d)[j]; v=symmetric_pair(a,b)
                    self.assertTrue(np.allclose(swap_operator(d)@v,v))
                    self.assertAlmostEqual(np.vdot(v,v).real,1)
    def test_hom_identical(self):
        for d in range(2,7):
            for i in range(d): self.assertAlmostEqual(hom_coincidence(np.eye(d)[i],np.eye(d)[i]),0)
    def test_hom_orthogonal(self):
        for d in range(2,7):
            for i in range(d):
                for j in range(d):
                    if i!=j: self.assertAlmostEqual(hom_coincidence(np.eye(d)[i],np.eye(d)[j]),.5)
    def test_hom_partial(self):
        a=np.array([1,0])
        for theta in np.linspace(0,np.pi/2,21):
            b=np.array([np.cos(theta),np.sin(theta)])
            self.assertAlmostEqual(hom_coincidence(a,b),np.sin(theta)**2/2)
    def test_number_commutes_with_swap(self):
        for d in range(2,7):
            s=swap_operator(d)
            for i in range(d):
                n=number_operator(d,i); self.assertTrue(np.allclose(n@s,s@n))
    def test_slot_operator_not_symmetric(self):
        d=2; p=np.diag([1,0]); slot=np.kron(p,np.eye(2)); s=swap_operator(d)
        self.assertFalse(np.allclose(slot@s,s@slot))
    def test_semantic_equivalence(self):
        for x in np.linspace(0,1,101):
            result=passive_label_equivalence(float(x))
            self.assertEqual(result['ordinary_internal'],result['permanent_identity'])
    def test_invalid(self):
        with self.assertRaises(ValueError): hom_coincidence([1,0],[1,1])
        with self.assertRaises(ValueError): passive_label_equivalence(1.1)
        with self.assertRaises(ValueError): number_operator(2,2)
if __name__=='__main__': unittest.main()
