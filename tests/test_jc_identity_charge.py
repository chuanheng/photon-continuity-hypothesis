import math,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from jc_identity_charge import *
class TestJCIdentityCharge(unittest.TestCase):
 def test_commutator_equal(self): self.assertEqual(commutator(2,1,1),((0.,0.),(-0.,0.)))
 def test_commutator_unequal(self): self.assertEqual(commutator(2,1,0),((0.,-2),(2,0.)))
 def test_commutator_antisymmetric(self):
  c=commutator(3,2,5);self.assertEqual(c[0][1],-c[1][0])
 def test_commutator_norm(self): self.assertAlmostEqual(commutator_norm(2,1,0),2*math.sqrt(2))
 def test_equal_charge_conserved(self): self.assertTrue(is_conserved(2,1,1))
 def test_unequal_charge_not_conserved(self): self.assertFalse(is_conserved(2,1,0))
 def test_zero_coupling_conserved(self): self.assertTrue(is_conserved(0,1,0))
 def test_zero_time_photon(self): self.assertEqual(photon_probability(1,0),1)
 def test_absorption(self): self.assertAlmostEqual(photon_probability(1,math.pi/2),0,places=14)
 def test_absorption_atom(self): self.assertAlmostEqual(atomic_excitation_probability(1,math.pi/2),1)
 def test_total_excitation(self):
  for t in (0,.2,.7,1.5,2.3): self.assertAlmostEqual(photon_probability(1,t)+atomic_excitation_probability(1,t),1)
 def test_identity_charge_constant(self):
  for t in (0,.2,1.,math.pi/2): self.assertAlmostEqual(charge_expectation(1,t,1,1),1)
 def test_photon_number_not_constant(self): self.assertNotAlmostEqual(charge_expectation(1,.7,1,0),1)
 def test_atom_number_changes(self): self.assertGreater(charge_expectation(1,.7,0,1),0)
 def test_charge_variance_equal(self): self.assertEqual(charge_variance(1,.5,1,1),0)
 def test_charge_variance_unequal(self): self.assertGreater(charge_variance(1,.5,1,0),0)
 def test_charge_variance_zero_at_absorption(self): self.assertAlmostEqual(charge_variance(1,math.pi/2,1,0),0,places=14)
 def test_negative_g_symmetric(self): self.assertAlmostEqual(photon_probability(-1,.4),photon_probability(1,.4))
 def test_nan_g(self):
  with self.assertRaises(ValueError): commutator(float('nan'),1,1)
 def test_inf_charge(self):
  with self.assertRaises(ValueError): charge_expectation(1,1,float('inf'),1)
 def test_nan_time(self):
  with self.assertRaises(ValueError): photon_probability(1,float('nan'))
 def test_negative_tolerance(self):
  with self.assertRaises(ValueError): is_conserved(1,1,1,-1)
 def test_small_g(self): self.assertTrue(is_conserved(1e-15,1,0,tol=1e-12))
 def test_zero_charge(self): self.assertTrue(is_conserved(2,0,0))
if __name__=='__main__': unittest.main()
