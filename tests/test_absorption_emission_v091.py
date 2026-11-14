"""v0.91 GitHub regression tests for standard JC-mode transfer (supplemental
to 49/49 executed local ZIP tests; remote CI has not been run).
"""
import unittest
import numpy as np
from models.absorption_emission_v091 import *
class Coupling(unittest.TestCase):
 def test_a_hermitian(self):self.assertTrue(np.allclose(coupling('a'),coupling('a').conj().T))
 def test_b_hermitian(self):self.assertTrue(np.allclose(coupling('b'),coupling('b').conj().T))
 def test_a_unitary(self):self.assertTrue(np.allclose(pulse('a').conj().T@pulse('a'),I))
 def test_b_unitary(self):self.assertTrue(np.allclose(pulse('b').conj().T@pulse('b'),I))
 def test_pulse_area(self):self.assertTrue(np.allclose(pulse('a',g=1),pulse('a',g=3)))
 def test_idle(self):self.assertTrue(np.allclose(pulse('a',area=0),I))
 def test_invalid_g(self):
  with self.assertRaises(ValueError):coupling(g=0)
 def test_invalid_mode(self):
  with self.assertRaises(ValueError):coupling('z')
 def test_excitation_conserved_a(self):
  self.assertLess(np.linalg.norm(commutator(coupling('a'),N_EXCITATION)),1e-12)
 def test_excitation_conserved_b(self):
  self.assertLess(np.linalg.norm(commutator(coupling('b'),N_EXCITATION)),1e-12)
 def test_photon_not_conserved_a(self):
  self.assertGreater(np.linalg.norm(commutator(coupling('a'),N_PHOTON)),1)
 def test_photon_not_conserved_b(self):
  self.assertGreater(np.linalg.norm(commutator(coupling('b'),N_PHOTON)),1)
class Evolution(unittest.TestCase):
 def setUp(self):self.tr=trajectory()
 def test_initial(self):self.assertTrue(np.allclose(self.tr['input'],A))
 def test_absorbed(self):self.assertTrue(np.allclose(self.tr['stored'],-1j*E))
 def test_emitted(self):self.assertTrue(np.allclose(self.tr['output'],-B))
 def test_input_photon(self):self.assertEqual(observables(self.tr['input'])['photon_count'],1)
 def test_stored_photon_zero(self):self.assertAlmostEqual(observables(self.tr['stored'])['photon_count'],0)
 def test_reemitted_photon_one(self):self.assertAlmostEqual(observables(self.tr['output'])['photon_count'],1)
 def test_excitation_conserved(self):
  for state in self.tr.values():self.assertAlmostEqual(observables(state)['excitation_count'],1)
 def test_mode_a_empty_after(self):self.assertAlmostEqual(observables(self.tr['output'])['P_a'],0)
 def test_mode_b_full_after(self):self.assertAlmostEqual(observables(self.tr['output'])['P_b'],1)
 def test_atom_full_when_stored(self):self.assertAlmostEqual(observables(self.tr['stored'])['P_e'],1)
 def test_absorb_quarter(self):self.assertAlmostEqual(observables(trajectory(absorption=np.pi/6)['stored'])['P_e'],.25)
 def test_emit_half(self):self.assertAlmostEqual(observables(trajectory(emission=np.pi/4)['output'])['P_b'],.5)
 def test_norm_preserved(self):
  for state in self.tr.values():self.assertAlmostEqual(np.vdot(state,state).real,1)
 def test_bad_shape(self):
  with self.assertRaises(ValueError):expectation([1,0],N_A)
class FullSpace(unittest.TestCase):
 def setUp(self):self.ops=full_fock_operators()
 def test_dim(self):self.assertEqual(self.ops['Nexc'].shape,(8,8))
 def test_ha_hermitian(self):self.assertTrue(np.allclose(self.ops['ha'],self.ops['ha'].conj().T))
 def test_hb_hermitian(self):self.assertTrue(np.allclose(self.ops['hb'],self.ops['hb'].conj().T))
 def test_conserved_a(self):self.assertTrue(np.allclose(commutator(self.ops['ha'],self.ops['Nexc']),0))
 def test_conserved_b(self):self.assertTrue(np.allclose(commutator(self.ops['hb'],self.ops['Nexc']),0))
 def test_photons_vary(self):self.assertGreater(np.linalg.norm(commutator(self.ops['ha'],self.ops['na']+self.ops['nb'])),1)
class Damping(unittest.TestCase):
 def test_kraus_complete(self):
  for angle in (0,.3,np.pi/4,np.pi/2):
   k0,k1=damped_emission_kraus(angle)
   self.assertTrue(np.allclose(k0.conj().T@k0+k1.conj().T@k1,np.eye(2)))
 def test_excited_half(self):self.assertTrue(np.allclose(atom_emission_channel(np.diag([0,1]),np.pi/4),np.eye(2)/2))
 def test_excited_all(self):self.assertTrue(np.allclose(atom_emission_channel(np.diag([0,1]),np.pi/2),np.diag([1,0])))
 def test_ground_idle(self):self.assertTrue(np.allclose(atom_emission_channel(np.diag([1,0]),.8),np.diag([1,0])))
 def test_coherence(self):self.assertAlmostEqual(atom_emission_channel(np.ones((2,2))/2,np.pi/3)[0,1].real,.25)
 def test_trace(self):self.assertAlmostEqual(np.trace(atom_emission_channel(np.eye(2)/2,.3)).real,1)
 def test_invalid(self):
  with self.assertRaises(ValueError):atom_emission_channel(np.eye(3),.3)
class Ancillary(unittest.TestCase):
 def test_tag0(self):self.assertTrue(np.allclose(spectator_label_probability([1,0]),[0,0,1]))
 def test_tag1(self):self.assertTrue(np.allclose(spectator_label_probability([0,1]),[0,0,1]))
 def test_tag_plus(self):self.assertTrue(np.allclose(spectator_label_probability([1/np.sqrt(2)]*2),[0,0,1]))
 def test_tag_random(self):
  r=np.random.default_rng(91)
  for _ in range(10):
   a=r.normal(size=3)+1j*r.normal(size=3);a/=np.linalg.norm(a)
   self.assertTrue(np.allclose(spectator_label_probability(a),[0,0,1]))
 def test_tag_invalid(self):
  with self.assertRaises(ValueError):spectator_label_probability([1,1])
 def test_reference(self):
  a=coherent_transfer_reference()
  self.assertTrue(np.allclose(a['output'],a['expected']))
 def test_reference_norm(self):self.assertAlmostEqual(np.vdot(coherent_transfer_reference()['output'],coherent_transfer_reference()['output']).real,1)
 def test_reference_invalid(self):
  with self.assertRaises(ValueError):coherent_transfer_reference(2,0)
 def test_summary(self):
  d=summary();self.assertEqual(d['version'],'v0.91')
  self.assertAlmostEqual(d['stages']['stored']['photon_count'],0)
if __name__=='__main__':unittest.main()
