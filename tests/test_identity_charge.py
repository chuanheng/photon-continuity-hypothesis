import sys,unittest,pathlib
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from identity_charge import *
class TestIdentity(unittest.TestCase):
 def test_01(self): self.assertEqual(hamiltonian().shape,(4,4))
 def test_02(self): self.assertEqual(charge().shape,(4,4))
 def test_03(self): self.assertTrue(np.allclose(hamiltonian(.3,.4),hamiltonian(.3,.4).conj().T))
 def test_04(self): self.assertTrue(np.allclose(charge(),charge().conj().T))
 def test_05(self): self.assertTrue(np.allclose(charge()@charge(),np.eye(4)))
 def test_06(self): self.assertTrue(np.allclose(commutator(hamiltonian(.3,.4),charge()),0))
 def test_07(self): self.assertTrue(np.allclose(commutator(hamiltonian(.3,0),charge()),0))
 def test_08(self): self.assertTrue(np.allclose(commutator(hamiltonian(0,.4),charge()),0))
 def test_09(self): self.assertTrue(np.allclose(evolution(hamiltonian(.3,.4),.7).conj().T@evolution(hamiltonian(.3,.4),.7),np.eye(4)))
 def test_10(self): self.assertTrue(np.allclose(evolution(hamiltonian(.3,.4),0),np.eye(4)))
 def test_11(self): self.assertTrue(np.allclose(commutator(evolution(hamiltonian(.3,.4),.7),charge()),0))
 def test_12(self): self.assertTrue(np.allclose(np.sort(np.linalg.eigvalsh(hamiltonian(.3,.4))),[-.5,-.5,.5,.5]))
 def test_13(self): self.assertAlmostEqual(jc_probability(1,0,np.pi/2),1)
 def test_14(self): self.assertAlmostEqual(jc_probability(1,0,0),0)
 def test_15(self): self.assertAlmostEqual(jc_probability(0,1,1),0)
 def test_16(self): self.assertAlmostEqual(jc_probability(1,1,0),0)
 def test_17(self): self.assertAlmostEqual(jc_probability(1,1,.5,1),jc_probability(1,1,.5,-1))
 def test_18(self): self.assertLess(jc_probability(1,1,np.pi/2),1)
 def test_19(self): self.assertGreaterEqual(jc_probability(1,1,.5),0)
 def test_20(self): self.assertLessEqual(jc_probability(1,1,.5),1)
 def test_21(self): self.assertAlmostEqual(jc_probability(1,0,.2),np.sin(.2)**2)
 def test_22(self): self.assertTrue(np.allclose(reduced_jc(np.diag([1,0,0,0])),np.diag([1,0])))
 def test_23(self): self.assertTrue(np.allclose(reduced_jc(np.diag([0,1,0,0])),np.diag([1,0])))
 def test_24(self): self.assertTrue(np.allclose(reduced_jc(np.diag([0,0,1,0])),np.diag([0,1])))
 def test_25(self): self.assertAlmostEqual(physical_expectation(np.diag([1,0,0,0]),Z),1)
 def test_26(self): self.assertAlmostEqual(physical_expectation(np.diag([0,1,0,0]),Z),1)
 def test_27(self): self.assertAlmostEqual(physical_expectation(np.diag([0,0,1,0]),Z),-1)
 def test_28(self):
  with self.assertRaises(ValueError): reduced_jc(np.eye(2))
 def test_29(self):
  with self.assertRaises(ValueError): physical_expectation(np.eye(4),np.eye(4))
 def test_30(self):
  with self.assertRaises(ValueError): hamiltonian(float('nan'))
 def test_31(self):
  with self.assertRaises(ValueError): evolution(hamiltonian(),float('inf'))
 def test_32(self):
  with self.assertRaises(ValueError): jc_probability(1,1,1,0)
 def test_33(self): self.assertTrue(np.allclose(np.linalg.eigvalsh(hamiltonian(0,0)),0))
 def test_34(self): self.assertTrue(np.allclose(commutator(hamiltonian(.3,.4),hamiltonian(.3,.4)),0))
 def test_35(self): self.assertAlmostEqual(jc_probability(0,0,1),0)
if __name__=='__main__': unittest.main()
