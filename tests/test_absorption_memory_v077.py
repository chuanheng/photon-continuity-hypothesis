"""31 unit tests for v0.77, from repository root:
python -m unittest discover -s tests -p test_absorption_memory_v077.py -v
"""
import unittest
import numpy as np
from models.absorption_memory_v077 import (
    I3,I2,EA,EB,EE,H0,H1,PA,PB,PE,P1,ket_dm,absorber,storage_phase,
    protocol,optical_input,output,reduced_optical,optical_detection,
    trace_distance,optical_distinguishability,swapped_ancilla_protocol,
    memory_equivalent_output,analytic_full_absorption,occupied_e_during_storage,summary
)

class UnitarityTests(unittest.TestCase):
    def test_absorber_unitary(self):
        for th in np.linspace(-np.pi,np.pi,11):
            a=absorber(th);self.assertTrue(np.allclose(a.conj().T@a,I3))
    def test_storage_unitary(self):
        for ph in np.linspace(-3,3,11):
            u=storage_phase(ph);self.assertTrue(np.allclose(u.conj().T@u,np.eye(6)))
    def test_protocol_unitary(self):
        for ph in [0.,.3,1.,np.pi]:
            u=protocol(ph);self.assertTrue(np.allclose(u.conj().T@u,np.eye(6)))
    def test_reference_arm_untouched(self):
        self.assertTrue(np.allclose(absorber(np.pi/2)@EB,EB))
    def test_absorption_e(self):
        self.assertTrue(np.allclose(absorber(np.pi/2)@EA,-1j*EE))
    def test_absorption_no_a_at_storage(self):
        self.assertAlmostEqual(occupied_e_during_storage(0)['a'],0)
    def test_storage_e_probability(self):
        self.assertAlmostEqual(occupied_e_during_storage(1)['e'],.5)
    def test_storage_b_probability(self):
        self.assertAlmostEqual(occupied_e_during_storage(1)['b'],.5)

class OperationalTests(unittest.TestCase):
    def test_label0_identity_channel(self):
        self.assertTrue(np.allclose(output(np.pi,0),np.kron(optical_input(),H0)))
    def test_label1_pi_minus(self):
        self.assertTrue(np.allclose(reduced_optical(ket_dm(output(np.pi,1))),ket_dm((EB-EA)/np.sqrt(2))))
    def test_full_absorption_analytic(self):
        for ph in [0,.3,1,2.1,np.pi]:
            for b in [0,1]:
                self.assertTrue(np.allclose(reduced_optical(ket_dm(output(ph,b))),ket_dm(analytic_full_absorption(ph,b))))
    def test_d0(self):self.assertAlmostEqual(optical_distinguishability(0),0)
    def test_d_pi(self):self.assertAlmostEqual(optical_distinguishability(np.pi),1)
    def test_trace_distance_formula(self):
        for ph in np.linspace(0,2*np.pi,17):
            self.assertAlmostEqual(optical_distinguishability(ph),abs(np.sin(ph/2)),places=10)
    def test_plus_prob_label0(self):
        for ph in [0,.3,np.pi]:self.assertAlmostEqual(optical_detection(ph,0)['plus'],1)
    def test_plus_prob_label1(self):
        for ph in np.linspace(0,2*np.pi,11):
            self.assertAlmostEqual(optical_detection(ph,1)['plus'],(1+np.cos(ph))/2)
    def test_minus_prob_label1(self):
        for ph in np.linspace(0,2*np.pi,11):
            self.assertAlmostEqual(optical_detection(ph,1)['minus'],(1-np.cos(ph))/2)
    def test_probabilities_sum(self):
        for ph in [.1,.9,3]:
            for b in [0,1]:
                d=optical_detection(ph,b)
                self.assertAlmostEqual(d['plus']+d['minus']+d['material_excitation'],1)
    def test_intensity_same(self):
        for ph in [.0,.3,1.,np.pi]:
            a=optical_detection(ph,0);b=optical_detection(ph,1)
            for key in ['optical_a','optical_b','material_excitation']:
                self.assertAlmostEqual(a[key],b[key])
    def test_partial_absorption_diminishes_difference(self):
        self.assertLess(optical_distinguishability(np.pi,theta=.3),1)
        self.assertGreater(optical_distinguishability(np.pi,theta=.3),0)

class RepresentationTests(unittest.TestCase):
    def test_swapped_ancilla_same_system_predictions(self):
        for ph in np.linspace(0,2*np.pi,13):
            for b in (0,1):
                self.assertTrue(np.allclose(reduced_optical(ket_dm(output(ph,b))),
                                            reduced_optical(ket_dm(memory_equivalent_output(ph,b)))))
    def test_full_joint_related_by_relabel(self):
        x=np.array([[0,1],[1,0]],complex);j=np.kron(I3,x)
        for ph in [.2,1.1,np.pi]:
            for b in (0,1):
                self.assertTrue(np.allclose(memory_equivalent_output(ph,b),j@output(ph,b)))
    def test_swapped_protocol_unitary(self):
        u=swapped_ancilla_protocol(.7)
        self.assertTrue(np.allclose(u.conj().T@u,np.eye(6)))
    def test_memory_and_identity_not_distinguishable_by_optical(self):
        self.assertAlmostEqual(summary()['max_system_memory_equivalence_error'],0)
    def test_reduced_trace(self):
        rho=ket_dm(output(.4,1))
        self.assertAlmostEqual(np.trace(reduced_optical(rho)).real,1)
    def test_label_bit_validation(self):
        with self.assertRaises(ValueError):output(.1,2)
    def test_invalid_ket_validation(self):
        with self.assertRaises(ValueError):ket_dm(np.array([2,0]))
    def test_invalid_reduced_shape(self):
        with self.assertRaises(ValueError):reduced_optical(np.eye(4))
    def test_trace_distance_orthogonal(self):
        self.assertAlmostEqual(trace_distance(ket_dm(EA),ket_dm(EB)),1)
    def test_trace_distance_identical(self):
        self.assertAlmostEqual(trace_distance(ket_dm(EA),ket_dm(EA)),0)
    def test_phase_zero_retrieve(self):
        for b in (0,1):
            self.assertTrue(np.allclose(output(0,b),np.kron(optical_input(),H0 if b==0 else H1)))

if __name__=='__main__':unittest.main()
