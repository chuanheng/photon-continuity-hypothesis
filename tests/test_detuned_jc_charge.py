import math,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from detuned_jc_charge import *
class Tests(unittest.TestCase):
 def test_identity(self): self.assertTrue(conserved(2,3,1,0,0,0))
 def test_hamiltonian(self): self.assertTrue(conserved(2,3,0,3,0,1))
 def test_resonant_x(self): self.assertTrue(conserved(0,2,0,1,0,0))
 def test_resonant_z(self): self.assertFalse(conserved(0,2,0,0,0,1))
 def test_detuned_z(self): self.assertTrue(conserved(2,0,0,0,0,1))
 def test_detuned_x(self): self.assertFalse(conserved(2,0,0,1,0,0))
 def test_y_never_nontrivial(self): self.assertFalse(conserved(2,3,0,0,1,0))
 def test_zero_all(self): self.assertTrue(conserved(0,0,2,3,4,5))
 def test_coeff_x(self): self.assertEqual(commutator_coefficients(2,3,0,0,1,0)[0],-1)
 def test_coeff_y(self): self.assertEqual(commutator_coefficients(2,3,0,1,0,0)[1],1)
 def test_coeff_z(self): self.assertEqual(commutator_coefficients(2,3,0,0,1,0)[2],3)
 def test_coeff_d(self): self.assertEqual(commutator_coefficients(2,3,0,0,0,1)[1],-3)
 def test_norm_zero(self): self.assertEqual(commutator_norm(2,3,0,3,0,1),0)
 def test_norm_y(self): self.assertAlmostEqual(commutator_norm(0,1,0,0,1,0),2*math.sqrt(2))
 def test_basis_generic(self): self.assertEqual(len(fixed_commutant_basis(2,3)),2)
 def test_basis_zero(self): self.assertEqual(len(fixed_commutant_basis(0,0)),4)
 def test_basis_valid(self):
  for a,b,c,d in fixed_commutant_basis(2,3): self.assertTrue(conserved(2,3,a,b,c,d))
 def test_common_independent(self): self.assertEqual(len(common_commutant_basis([(0,1),(2,1)])),1)
 def test_common_parallel(self): self.assertEqual(len(common_commutant_basis([(2,1),(4,2)])),2)
 def test_common_zero_ignored(self): self.assertEqual(len(common_commutant_basis([(0,0),(2,1)])),2)
 def test_common_all_zero(self): self.assertEqual(len(common_commutant_basis([(0,0),(0,0)])),4)
 def test_common_empty(self):
  with self.assertRaises(ValueError): common_commutant_basis([])
 def test_eigenvalues(self): self.assertEqual(eigenvalues(6,4),(-5,5))
 def test_eigenvalues_zero(self): self.assertEqual(eigenvalues(0,0),(0,0))
 def test_nan(self):
  with self.assertRaises(ValueError): fixed_commutant_basis(float('nan'),1)
 def test_inf(self):
  with self.assertRaises(ValueError): conserved(0,float('inf'),0,0,0,0)
 def test_negative_tolerance(self):
  with self.assertRaises(ValueError): conserved(1,1,0,0,0,0,-1)
 def test_single_common(self): self.assertEqual(len(common_commutant_basis([(1,1)])),2)
 def test_common_multiple_independent(self): self.assertEqual(len(common_commutant_basis([(2,1),(4,2),(3,1)])),1)
 def test_near_parallel_exact(self): self.assertEqual(len(common_commutant_basis([(2,1),(2+1e-8,1)])),1)
if __name__=='__main__': unittest.main()
