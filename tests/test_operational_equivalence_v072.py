import unittest,numpy as np
from models.operational_equivalence_v072 import *
class TestOperational(unittest.TestCase):
 def test_unitary(self):
  for t in [0,.2,1,3.14]:
   u=controlled_phase(t);self.assertTrue(np.allclose(u.conj().T@u,np.eye(4)))
 def test_no_coupling(self):self.assertAlmostEqual(system_distinguishability(state(0),state(1),0),0)
 def test_direct(self):
  self.assertAlmostEqual(probability(np.kron(state(0),state(0)),np.kron(I,state(0))),1)
  self.assertAlmostEqual(probability(np.kron(state(0),state(1)),np.kron(I,state(0))),0)
 def test_coupling(self):
  for t in [.1,.5,1,1.5,2,3.14]:
   self.assertAlmostEqual(system_distinguishability(state(0),state(1),t),abs(np.sin(t)))
 def test_partial_trace(self):
  for a in [state(0),state(1),I/2]:
   self.assertTrue(np.allclose(reduced_system(np.kron(state(0),a)),state(0)))
if __name__=='__main__':unittest.main()
