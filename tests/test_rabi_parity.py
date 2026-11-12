import pathlib,sys,unittest
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from rabi_parity import *
class RabiParityTests(unittest.TestCase):
 def setUp(self): self.H,self.N,self.P=operators(6,g=.3)
 def test_shapes(self): self.assertEqual(self.H.shape,(12,12))
 def test_hermitian_h(self): self.assertTrue(np.allclose(self.H,self.H.T.conj()))
 def test_hermitian_n(self): self.assertTrue(np.allclose(self.N,self.N.T.conj()))
 def test_hermitian_p(self): self.assertTrue(np.allclose(self.P,self.P.T.conj()))
 def test_parity_square(self): self.assertTrue(np.allclose(self.P@self.P,np.eye(12)))
 def test_parity_eigenvalues(self): self.assertEqual(set(np.diag(self.P)),{-1.,1.})
 def test_parity_conserved(self): self.assertLess(norm(commutator(self.H,self.P)),1e-12)
 def test_number_not_conserved(self): self.assertGreater(norm(commutator(self.H,self.N)),.1)
 def test_zero_coupling_number(self):
  h,n,p=operators(6,g=0);self.assertEqual(norm(commutator(h,n)),0)
 def test_zero_coupling_parity(self):
  h,n,p=operators(6,g=0);self.assertEqual(norm(commutator(h,p)),0)
 def test_ground_one_parity(self): self.assertEqual(self.P[1,1],1)
 def test_excited_zero_parity(self): self.assertEqual(self.P[6,6],1)
 def test_ground_three_parity(self): self.assertEqual(self.P[3,3],1)
 def test_excited_two_parity(self): self.assertEqual(self.P[8,8],1)
 def test_ground_zero_parity(self): self.assertEqual(self.P[0,0],-1)
 def test_excited_one_parity(self): self.assertEqual(self.P[7,7],-1)
 def test_jc_transition(self): self.assertAlmostEqual(transition(self.H,0,1,1,0,6),.3)
 def test_counterrotating_transition(self): self.assertAlmostEqual(transition(self.H,0,0,1,1,6),.3)
 def test_forbidden_parity_transition(self): self.assertEqual(transition(self.H,0,0,1,0,6),0)
 def test_counterrotating_sqrt2(self): self.assertAlmostEqual(transition(self.H,0,1,1,2,6),.3*np.sqrt(2))
 def test_cutoff_2(self): self.assertEqual(operators(2)[0].shape,(4,4))
 def test_cutoff_1(self):
  with self.assertRaises(ValueError): operators(1)
 def test_cutoff_float(self):
  with self.assertRaises(ValueError): operators(2.5)
 def test_nonfinite_g(self):
  with self.assertRaises(ValueError): operators(3,g=float('nan'))
 def test_nonfinite_omega(self):
  with self.assertRaises(ValueError): operators(3,omega=float('inf'))
 def test_bad_basis(self):
  with self.assertRaises(ValueError): transition(self.H,0,6,1,0,6)
 def test_norm_zero(self): self.assertEqual(norm(commutator(self.P,self.P)),0)
 def test_omega_zero(self):
  h,n,p=operators(4,omega=0,omega0=0,g=.2);self.assertLess(norm(commutator(h,p)),1e-12)
 def test_multiple_cutoffs(self):
  for k in (2,3,5,8):
   h,n,p=operators(k,g=.4);self.assertLess(norm(commutator(h,p)),1e-12)
 def test_energy_eigenvalues_real(self): self.assertTrue(np.all(np.isreal(np.linalg.eigvalsh(self.H))))
if __name__=='__main__': unittest.main()
