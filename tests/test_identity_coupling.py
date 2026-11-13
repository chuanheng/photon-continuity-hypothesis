import math,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from identity_coupling import *
class Tests(unittest.TestCase):
 def test_zero_coupling_visibility(self): self.assertEqual(visibility(0,100),1)
 def test_zero_time_visibility(self): self.assertEqual(visibility(1,0),1)
 def test_visibility_zero(self): self.assertAlmostEqual(visibility(1,math.pi/4),0,places=14)
 def test_visibility_revives(self): self.assertAlmostEqual(visibility(1,math.pi/2),1)
 def test_purity_initial(self): self.assertEqual(purity(1,0),1)
 def test_purity_entangled(self): self.assertAlmostEqual(purity(1,math.pi/4),.5)
 def test_purity_bounds(self): self.assertTrue(.5<=purity(.7,1)<=1)
 def test_probability_initial(self): self.assertEqual(x_plus_probability(1,0),1)
 def test_probability_min(self): self.assertAlmostEqual(x_plus_probability(1,math.pi/2),0)
 def test_probability_half(self): self.assertAlmostEqual(x_plus_probability(1,math.pi/4),.5)
 def test_reduced_trace(self):
  r=reduced_system(.7,.3);self.assertAlmostEqual(r[0][0].real+r[1][1].real,1)
 def test_reduced_hermitian(self):
  r=reduced_system(.7,.3);self.assertEqual(r[0][1],r[1][0].conjugate())
 def test_reduced_coherence(self): self.assertAlmostEqual(reduced_system(1,math.pi/4)[0][1].real,0,places=14)
 def test_negative_time(self):
  with self.assertRaises(ValueError): visibility(1,-1)
 def test_zero_hbar(self):
  with self.assertRaises(ValueError): visibility(1,1,0)
 def test_nan(self):
  with self.assertRaises(ValueError): visibility(float('nan'),1)
 def test_infinite(self):
  with self.assertRaises(ValueError): purity(float('inf'),1)
 def test_uncoupled_plus(self):
  rho=((.5,.5),(.5,.5));self.assertAlmostEqual(uncoupled_probability(rho,rho),1)
 def test_uncoupled_mixed(self):
  rho=((.5,0),(0,.5)); proj=((1,0),(0,0));self.assertAlmostEqual(uncoupled_probability(rho,proj),.5)
 def test_uncoupled_identity(self):
  rho=((.6,0),(0,.4));ident=((1,0),(0,1));self.assertAlmostEqual(uncoupled_probability(rho,ident),1)
 def test_uncoupled_invalid(self):
  with self.assertRaises(ValueError): uncoupled_probability(((1,),),((1,0),(0,1)))
 def test_hbar_scaling(self): self.assertAlmostEqual(visibility(2,1,2),visibility(1,1,1))
 def test_sign_symmetry(self): self.assertAlmostEqual(visibility(-1,.3),visibility(1,.3))
if __name__=='__main__': unittest.main()
