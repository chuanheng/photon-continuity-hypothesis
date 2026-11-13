import unittest
import numpy as np
from models.loss_dephasing_v078 import (
    state, probabilities, memory_probabilities, total_variation,
    kl_divergence, expected_llr, sample_counts,
    log_likelihood_ratio, fisher_phase, summary)

class TestChannel(unittest.TestCase):
    def test_trace(self):
        for eta in [0,.2,.8,1]:
            for v in [0,.5,1]:
                self.assertAlmostEqual(np.trace(state(eta,v,.4)).real,1)
    def test_hermitian(self):
        rho=state(.6,.7,1.4)
        self.assertTrue(np.allclose(rho,rho.conj().T))
    def test_positive(self):
        for v in np.linspace(0,1,11):
            self.assertGreaterEqual(np.linalg.eigvalsh(state(.7,v,.5)).min(),-1e-12)
    def test_eta_zero_vacuum(self):
        self.assertTrue(np.allclose(probabilities(0,.5,.6),[1,0,0]))
    def test_visibility_zero(self):
        self.assertTrue(np.allclose(probabilities(.8,0,.4),[.2,.4,.4]))
    def test_plus_phase_zero(self):
        self.assertTrue(np.allclose(probabilities(1,1,0),[0,1,0]))
    def test_minus_phase_pi(self):
        self.assertTrue(np.allclose(probabilities(1,1,np.pi),[0,0,1]))
    def test_prob_sum(self):
        for phi in np.linspace(-4,4,19):
            self.assertAlmostEqual(probabilities(.6,.7,phi).sum(),1)
    def test_formula(self):
        eta,v,phi=.7,.5,1.
        self.assertTrue(np.allclose(probabilities(eta,v,phi),
            [1-eta,eta*(1+v*np.cos(phi))/2,eta*(1-v*np.cos(phi))/2]))
    def test_invalid_eta(self):
        with self.assertRaises(ValueError):state(-.1,.5,.1)
    def test_invalid_visibility(self):
        with self.assertRaises(ValueError):state(.5,1.1,.1)

class TestInference(unittest.TestCase):
    def setUp(self):
        self.p=probabilities(.65,.8,np.pi/2)
        self.q=probabilities(.65,.8,np.pi/2+.2)
    def test_equivalent_memory(self):
        self.assertTrue(np.array_equal(self.p,memory_probabilities(.65,.8,np.pi/2)))
    def test_zero_tv(self):
        self.assertEqual(total_variation(self.p,self.p),0)
    def test_zero_kl(self):
        self.assertEqual(kl_divergence(self.p,self.p),0)
    def test_kl_positive_phase_offset(self):
        self.assertGreater(kl_divergence(self.q,self.p),0)
    def test_gibbs_inequality(self):
        for phi in np.linspace(.2,2,9):
            self.assertGreaterEqual(kl_divergence(probabilities(.65,.8,phi),self.p),-1e-12)
    def test_kl_infinite_unsupported(self):
        self.assertTrue(np.isinf(kl_divergence(np.array([.5,.5,0]),np.array([1,0,0]))))
    def test_llr_expectation(self):
        self.assertAlmostEqual(expected_llr(1000,self.q,self.p),1000*kl_divergence(self.q,self.p))
    def test_llr_identical_zero(self):
        self.assertEqual(log_likelihood_ratio([100,200,300],self.p,self.p),0)
    def test_same_model_any_n_indistinguishable(self):
        for n in [1,100,10_000_000]:
            self.assertEqual(expected_llr(n,self.p,self.p),0)
    def test_sampling_determinism(self):
        self.assertTrue(np.array_equal(sample_counts(100,self.q,seed=1),sample_counts(100,self.q,seed=1)))
    def test_counts_sum(self):
        self.assertEqual(sample_counts(1243,self.q).sum(),1243)
    def test_bad_counts(self):
        with self.assertRaises(ValueError):sample_counts(-1,self.p)
    def test_fisher_midfringe(self):
        eta,v=.65,.8
        self.assertAlmostEqual(fisher_phase(eta,v,np.pi/2),eta*v*v)
    def test_fisher_zero_visibility(self):
        self.assertEqual(fisher_phase(.8,0,np.pi/2),0)
    def test_kl_matches_quadratic_approx_small_offset(self):
        delta=1e-4
        q=probabilities(.65,.8,np.pi/2+delta)
        kl=kl_divergence(q,self.p)
        self.assertAlmostEqual(2*kl/delta**2,fisher_phase(.65,.8,np.pi/2),places=4)
    def test_summary(self):
        s=summary()
        self.assertEqual(s['identity_vs_memory_kl'],0)
        self.assertGreater(s['expected_twice_llr_n1000'],0)
        self.assertEqual(sum(s['simulated_counts_alternative']),1000)

if __name__=='__main__':unittest.main()
