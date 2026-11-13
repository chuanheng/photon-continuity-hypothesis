import unittest,numpy as np
from models.superselection_v073 import *
class Tests(unittest.TestCase):
 def test_restricted(self):self.assertAlmostEqual(operational_distance(phase_state(0),phase_state(np.pi),[0,1]),0)
 def test_unrestricted(self):self.assertAlmostEqual(operational_distance(phase_state(0),phase_state(np.pi),[0,0]),1)
 def test_full(self):self.assertAlmostEqual(trace_distance(phase_state(0),phase_state(np.pi)),1)
 def test_allowed(self):self.assertTrue(allowed(np.diag([1,2]),[0,1]))
 def test_forbidden(self):self.assertFalse(allowed(np.array([[0,1],[1,0]]),[0,1]))
 def test_idempotence(self):
  r=phase_state(.5);self.assertTrue(np.allclose(dephase(dephase(r,[0,1]),[0,1]),dephase(r,[0,1])))
if __name__=='__main__':unittest.main()
