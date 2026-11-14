import unittest
import numpy as np
from models.process_access_v089 import *

class TestBasic(unittest.TestCase):
    def test_kets_normalized(self):self.assertTrue(all(np.isclose(np.vdot(x,x),1) for x in KETS))
    def test_kraus_cp_trace_nonincreasing(self):
        for p in range(4):
            for e in range(4):
                k=kraus(p,e)
                self.assertGreaterEqual(np.linalg.eigvalsh(I-k.conj().T@k).min(),-1e-12)
    def test_instrument_projector(self):self.assertTrue(np.allclose(instrument_outcome(P0,kraus(0,0)),P0))
    def test_instrument_impossible_outcome(self):self.assertTrue(np.allclose(instrument_outcome(P0,kraus(0,1)),np.zeros((2,2))))
    def test_one_step_channel(self):self.assertTrue(np.allclose(single_step(P0),I/2))
    def test_one_step_trace(self):self.assertAlmostEqual(np.trace(single_step(P1)).real,1)
    def test_two_step_fixed(self):self.assertTrue(np.allclose(no_intervention(correlated=True),P0))
    def test_two_step_fresh(self):self.assertTrue(np.allclose(no_intervention(correlated=False),I/2))
    def test_distance(self):self.assertAlmostEqual(trace_distance(P0,I/2),.5)
    def test_zero_distance(self):self.assertAlmostEqual(trace_distance(P0,P0),0)
    def test_wrong_shape(self):
        with self.assertRaises(ValueError):process_output(np.eye(3))
    def test_output_psd(self):
        for correlated in (True,False):
            for p in range(4):
                for e in range(4):
                    self.assertGreaterEqual(np.linalg.eigvalsh(process_output(kraus(p,e),correlated)).min(),-1e-12)
    def test_output_trace(self):
        for correlated in (True,False):
            self.assertAlmostEqual(np.trace(process_output(I,correlated)).real,1)
class TestCausalBreak(unittest.TestCase):
    def test_reset_outcome0_probability(self):self.assertAlmostEqual(outcome_reset(0,0,True)[0],.5)
    def test_reset_outcome1_probability(self):self.assertAlmostEqual(outcome_reset(1,0,True)[0],.5)
    def test_reset_outcome0_correlated_future(self):self.assertTrue(np.allclose(outcome_reset(0,0,True)[1],P0))
    def test_reset_outcome1_correlated_future(self):self.assertTrue(np.allclose(outcome_reset(1,0,True)[1],P1))
    def test_reset_fresh_future(self):
        for e in [0,1]:self.assertTrue(np.allclose(outcome_reset(e,0,False)[1],I/2))
    def test_reset_conditioned_norm(self):
        for e in [0,1]:
            for correlated in [True,False]:
                self.assertAlmostEqual(np.trace(outcome_reset(e,0,correlated)[1]).real,1)
    def test_causal_break_checks_past(self):
        self.assertAlmostEqual(trace_distance(outcome_reset(0,0,True)[1],outcome_reset(1,0,True)[1]),1)
    def test_fresh_no_memory(self):
        self.assertAlmostEqual(trace_distance(outcome_reset(0,0,False)[1],outcome_reset(1,0,False)[1]),0)
class TestTomography(unittest.TestCase):
    def test_4_final_effects_span(self):self.assertEqual(informational_completeness()['final_effect_span_rank'],4)
    def test_16_cp_instruments_span(self):self.assertEqual(informational_completeness()['instrument_choi_span_rank'],16)
    def test_joint_span_64(self):self.assertEqual(informational_completeness()['joint_linear_span_rank'],64)
    def test_signature_length(self):self.assertEqual(len(tomography_signature()),64)
    def test_signature_nonnegative(self):self.assertGreaterEqual(tomography_signature().min(),-1e-12)
    def test_signature_le_one(self):self.assertLessEqual(tomography_signature().max(),1+1e-12)
    def test_relabel_same_fixed(self):self.assertTrue(np.allclose(tomography_signature(True),tomography_signature(True,True)))
    def test_relabel_same_fresh(self):self.assertTrue(np.allclose(tomography_signature(False),tomography_signature(False,True)))
    def test_relabel_same_random_instruments(self):
        rng=np.random.default_rng(89)
        for correlated in [True,False]:
            for _ in range(20):
                k=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2))
                k=k/np.linalg.norm(k,2)
                self.assertTrue(np.allclose(process_output(k,correlated),process_output(k,correlated,True)))
    def test_fixed_fresh_different_signature(self):
        self.assertGreater(np.linalg.norm(tomography_signature(True)-tomography_signature(False)),.1)
    def test_random_inputs_differ_under_memory(self):
        self.assertFalse(np.allclose(process_output(I,True),process_output(I,False)))
    def test_summary(self):
        s=summary()
        self.assertEqual(s['tomography']['number_observables'],64)
        self.assertLess(s['tomography']['max_label_rewrite_error'],1e-12)
        self.assertGreater(s['tomography']['max_fixed_vs_fresh_probability_difference'],0)

if __name__=='__main__':unittest.main()
