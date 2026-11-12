import pathlib,sys,unittest
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from rabi_spectrum import build,spectrum,convergence
class Tests(unittest.TestCase):
 def test_shape_h(self): self.assertEqual(build(4)[0].shape,(8,8))
 def test_shape_parity(self): self.assertEqual(build(4)[1].shape,(8,8))
 def test_shape_probe(self): self.assertEqual(build(4)[2].shape,(8,8))
 def test_hermitian_h(self):
  h,_,_=build(5);self.assertTrue(np.allclose(h,h.T.conj()))
 def test_parity_square(self):
  _,p,_=build(5);self.assertTrue(np.allclose(p@p,np.eye(10)))
 def test_h_parity_commute(self):
  h,p,_=build(6);self.assertLess(np.linalg.norm(h@p-p@h),1e-12)
 def test_probe_odd(self):
  _,p,x=build(6);self.assertLess(np.linalg.norm(p@x@p+x),1e-12)
 def test_energies_sorted(self):
  e,_,_,_=spectrum(6);self.assertTrue(np.all(np.diff(e)>=0))
 def test_eigenstate_parities(self):
  _,_,_,p=spectrum(6);self.assertTrue(np.allclose(np.abs(p),1))
 def test_signs(self):
  _,s,_,_=spectrum(6);self.assertTrue(set(s).issubset({-1,1}))
 def test_strength_nonnegative(self): self.assertTrue(np.all(spectrum(5)[2]>=0))
 def test_strength_symmetric(self):
  s=spectrum(5)[2];self.assertTrue(np.allclose(s,s.T))
 def test_same_parity_forbidden(self):
  _,p,s,_=spectrum(7);self.assertLess(np.max(np.abs(s[p[:,None]==p[None,:]])),1e-20)
 def test_opposite_parity_allowed(self):
  _,p,s,_=spectrum(7);self.assertGreater(np.max(s[p[:,None]!=p[None,:]]),0.1)
 def test_zero_coupling(self):
  e,_,_,_=spectrum(4,coupling=0);self.assertAlmostEqual(e[0],-.5)
 def test_omega(self): self.assertEqual(len(spectrum(4,omega=2)[0]),8)
 def test_omega0(self): self.assertEqual(len(spectrum(4,omega0=2)[0]),8)
 def test_cutoff_two(self): self.assertEqual(len(spectrum(2)[0]),4)
 def test_bad_cutoff(self):
  with self.assertRaises(ValueError): build(1)
 def test_bool_cutoff(self):
  with self.assertRaises(ValueError): build(True)
 def test_bad_g(self):
  with self.assertRaises(ValueError): build(4,coupling=float('nan'))
 def test_bad_omega(self):
  with self.assertRaises(ValueError): build(4,omega=float('inf'))
 def test_convergence_reference(self): self.assertEqual(convergence([4,6,8],levels=3)[-1][1],0)
 def test_convergence_length(self): self.assertEqual(len(convergence([4,6,8])),3)
 def test_convergence_nonnegative(self): self.assertTrue(all(err>=0 for _,err in convergence([4,6,8])))
 def test_convergence_invalid(self):
  with self.assertRaises(ValueError): convergence([4])
 def test_convergence_bad_levels(self):
  with self.assertRaises(ValueError): convergence([4,6],levels=9)
 def test_strong_coupling(self): self.assertTrue(np.all(np.isfinite(spectrum(8,coupling=1)[0])))
 def test_probe_diagonal_zero(self): self.assertLess(np.max(np.abs(np.diag(spectrum(7)[2]))),1e-20)
 def test_finite_norm(self): self.assertTrue(np.isfinite(np.linalg.norm(spectrum(8)[2])))
if __name__=='__main__': unittest.main()
