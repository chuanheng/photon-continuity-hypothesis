import math,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from jc_general_charge import *
class Tests(unittest.TestCase):
 def test_identity(self): self.assertEqual(charge_matrix(1,0,0,0),((1+0j,0j),(0j,1+0j)))
 def test_x(self): self.assertEqual(charge_matrix(0,1,0,0),((0j,1+0j),(1+0j,0j)))
 def test_y(self): self.assertEqual(charge_matrix(0,0,1,0),((0j,-1j),(1j,0j)))
 def test_z(self): self.assertEqual(charge_matrix(0,0,0,1),((1+0j,0j),(0j,-1+0j)))
 def test_hermitian(self):
  q=charge_matrix(2,3,4,5);self.assertEqual(q[0][1],q[1][0].conjugate())
 def test_commutator_identity(self): self.assertEqual(commutator(2,1,0,0,0),((0j,0),(0,0j)))
 def test_commutator_x(self): self.assertEqual(commutator(2,0,1,0,0),((0j,0),(0,0j)))
 def test_commutator_y(self): self.assertEqual(commutator(1,0,0,1,0),((2j,0),(0,-2j)))
 def test_commutator_z(self): self.assertEqual(commutator(1,0,0,0,1),((0j,-2),(2,0j)))
 def test_norm_y(self): self.assertAlmostEqual(commutator_frobenius(1,0,0,1,0),2*math.sqrt(2))
 def test_norm_z(self): self.assertAlmostEqual(commutator_frobenius(1,0,0,0,1),2*math.sqrt(2))
 def test_norm_combined(self): self.assertAlmostEqual(commutator_frobenius(2,0,0,3,4),20*math.sqrt(2))
 def test_conserved_general(self): self.assertTrue(conserved(1,3,4,0,0))
 def test_nonconserved_y(self): self.assertFalse(conserved(1,3,4,1,0))
 def test_nonconserved_z(self): self.assertFalse(conserved(1,3,4,0,1))
 def test_zero_coupling_all(self): self.assertTrue(conserved(0,1,2,3,4))
 def test_basis_nonzero(self): self.assertEqual(len(exact_commutant_basis(1)),2)
 def test_basis_zero(self): self.assertEqual(len(exact_commutant_basis(0)),4)
 def test_eigenvalues_identity(self): self.assertEqual(eigenvalues(3,0,0,0),(3,3))
 def test_eigenvalues_x(self): self.assertEqual(eigenvalues(0,2,0,0),(-2,2))
 def test_eigenvalues_all(self): self.assertEqual(eigenvalues(1,3,4,0),(-4,6))
 def test_nan(self):
  with self.assertRaises(ValueError): charge_matrix(float('nan'),0,0,0)
 def test_inf(self):
  with self.assertRaises(ValueError): commutator(float('inf'),0,0,0,0)
 def test_negative_tol(self):
  with self.assertRaises(ValueError): conserved(1,0,0,0,0,-1)
 def test_small_nonzero_g_basis(self): self.assertEqual(len(exact_commutant_basis(1e-20)),2)
if __name__=='__main__': unittest.main()
