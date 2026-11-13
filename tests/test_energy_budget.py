import pathlib,sys,unittest,math
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from energy_budget import *
class TestEnergyBudget(unittest.TestCase):
    def test_excess(self): self.assertAlmostEqual(excess_energy(20,13.606),6.394)
    def test_threshold(self): self.assertEqual(excess_energy(13.606,13.606),0)
    def test_below_threshold(self): self.assertLess(excess_energy(10,13.606),0)
    def test_successor_cost(self): self.assertAlmostEqual(remaining_kinetic(20,2,0,13.606),4.394)
    def test_other_radiation_cost(self): self.assertAlmostEqual(remaining_kinetic(20,2,1,13.606),3.394)
    def test_allowed(self): self.assertTrue(energetically_allowed(20,2,0,13.606))
    def test_forbidden(self): self.assertFalse(energetically_allowed(20,7,0,13.606))
    def test_boundary(self): self.assertTrue(energetically_allowed(20,6.394,0,13.606))
    def test_electron_recoil(self): self.assertAlmostEqual(electron_kinetic_from_recoil(20,2,.1,0,13.606),4.294)
    def test_excess_recoil(self):
        with self.assertRaises(ValueError): electron_kinetic_from_recoil(20,2,5,0,13.606)
    def test_max_successor(self): self.assertAlmostEqual(max_successor_energy(20,.1,1,13.606),5.294)
    def test_max_below_threshold(self): self.assertEqual(max_successor_energy(10,0,0,13.606),0)
    def test_negative_successor(self):
        with self.assertRaises(ValueError): remaining_kinetic(20,-1)
    def test_negative_recoil(self):
        with self.assertRaises(ValueError): electron_kinetic_from_recoil(20,1,-1)
    def test_negative_other_radiation(self):
        with self.assertRaises(ValueError): remaining_kinetic(20,1,-1)
    def test_nan(self):
        with self.assertRaises(ValueError): excess_energy(float('nan'))
    def test_infinite(self):
        with self.assertRaises(ValueError): max_successor_energy(float('inf'))
    def test_invalid_ionization(self):
        with self.assertRaises(ValueError): excess_energy(20,0)
    def test_invalid_incident(self):
        with self.assertRaises(ValueError): excess_energy(-1)
    def test_energy_balance(self):
        e=electron_kinetic_from_recoil(20,2,.1,1,13.606)
        self.assertAlmostEqual(13.606+e+.1+2+1,20)
if __name__=='__main__': unittest.main()
