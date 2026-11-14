"""v0.88: 25 mathematical checks."""
import unittest
import numpy as np
from models.originality_process_v088 import *
class OneStep(unittest.TestCase):
 def test_trace_preserving(self):self.assertAlmostEqual(np.trace(channel(P0)).real,1)
 def test_one_step_mixed(self):self.assertTrue(np.allclose(channel(P0),I/2))
 def test_unital(self):self.assertTrue(np.allclose(channel(I/2),I/2))
 def test_hermitian(self):
  rho=density(np.array([1,1j])/np.sqrt(2));self.assertTrue(np.allclose(channel(rho),channel(rho).conj().T))
 def test_idempotent(self):self.assertTrue(np.allclose(channel(channel(P0)),channel(P0)))
 def test_state_validation(self):
  with self.assertRaises(ValueError):density(np.array([2,0]))
 def test_matrix_validation(self):
  with self.assertRaises(ValueError):channel(np.eye(3))
 def test_trace_distance_zero(self):self.assertEqual(trace_distance(P0,P0),0)
 def test_trace_distance_orthogonal(self):self.assertAlmostEqual(trace_distance(P0,P1),1)
 def test_channel_kraus_sum(self):
  a=I/np.sqrt(2);b=X/np.sqrt(2)
  self.assertTrue(np.allclose(a.conj().T@a+b.conj().T@b,I))
class MultiStep(unittest.TestCase):
 def test_fixed_id_output(self):self.assertTrue(np.allclose(two_step(P0,I,True),P0))
 def test_fresh_id_output(self):self.assertTrue(np.allclose(two_step(P0,I,False),I/2))
 def test_fixed_X_output(self):self.assertTrue(np.allclose(two_step(P0,X,True),P1))
 def test_fresh_X_output(self):self.assertTrue(np.allclose(two_step(P0,X,False),I/2))
 def test_fixed_Z_output(self):self.assertTrue(np.allclose(two_step(P0,Z,True),P0))
 def test_fresh_Z_output(self):self.assertTrue(np.allclose(two_step(P0,Z,False),I/2))
 def test_max_distance_half(self):self.assertAlmostEqual(distinguishability(I)['trace_distance'],.5)
 def test_guess_success_three_quarters(self):self.assertAlmostEqual(distinguishability()['optimal_equal_prior_success'],.75)
 def test_probs(self):
  x=distinguishability();self.assertEqual(x['fixed_output_prob_zero'],1);self.assertAlmostEqual(x['fresh_output_prob_zero'],.5)
 def test_trace_preservation_two(self):
  for rho in (P0,P1,I/2):
   for correlated in (True,False):self.assertAlmostEqual(np.trace(two_step(rho,I,correlated)).real,1)
 def test_nonunitary_rejected(self):
  with self.assertRaises(ValueError):two_step(P0,2*I)
 def test_bad_state_rejected(self):
  with self.assertRaises(ValueError):two_step(np.eye(3))
 def test_equal_on_mixed_input(self):self.assertTrue(np.allclose(two_step(I/2,I,True),two_step(I/2,I,False)))
 def test_pure_both(self):
  for correlated in (True,False):self.assertGreaterEqual(np.linalg.eigvalsh(two_step(P0,I,correlated)).min(),-1e-12)
 def test_summary(self):self.assertAlmostEqual(state_readout_vs_process_readout()['two_step_identity_intervention']['trace_distance'],.5)
if __name__=='__main__':unittest.main()
