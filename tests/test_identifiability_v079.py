import unittest
import numpy as np
from models.identifiability_v079 import *

class TestDistribution(unittest.TestCase):
    def test_sum(self):
        for e in [0,.2,1]:
            for v in [0,.7,1]:
                for d in [0,.5,1]:
                    self.assertAlmostEqual(physical_prob(e,v,d,.3,.1).sum(),1)
    def test_positivity(self):
        for x in np.linspace(-4,4,21):
            self.assertGreaterEqual(physical_prob(.65,.8,.05,x,.1).min(),0)
    def test_dark_uniform(self):
        self.assertTrue(np.allclose(physical_prob(.65,.8,1,.3,.4),np.ones(3)/3))
    def test_reduction(self):
        l,a=effective(.65,.8,.05)
        for x in np.linspace(-3,3,11):
            self.assertTrue(np.allclose(physical_prob(.65,.8,.05,x,.1,.2),reduced_prob(l,a,x,.1,.2)))
    def test_wrong_eta(self):
        with self.assertRaises(ValueError):physical_prob(1.1,.5,.2,0,0)
    def test_wrong_visibility(self):
        with self.assertRaises(ValueError):physical_prob(.5,-.1,.2,0,0)
    def test_wrong_dark(self):
        with self.assertRaises(ValueError):physical_prob(.5,.1,-.2,0,0)
    def test_wrong_amplitude(self):
        with self.assertRaises(ValueError):reduced_prob(.2,.9,0,0)
    def test_kl_identity(self):
        p=physical_prob(.65,.8,.05,1,0)
        self.assertAlmostEqual(kl(p,p),0)
    def test_kl_inf(self):
        self.assertTrue(np.isinf(kl([1,0,0],[0,1,0])))

class TestIdentifiability(unittest.TestCase):
    def setUp(self):
        self.l,self.a=effective(.65,.8,.05)
        self.xs=[.15,.8,1.7,2.5]
        self.s=[(x,1) for x in self.xs]
        self.m=[(x,z) for x in self.xs for z in (0,1)]
    def test_beta_delta_reparametrization(self):
        for x in self.xs:
            self.assertTrue(np.allclose(reduced_prob(self.l,self.a,x,.13,.2,1),
                reduced_prob(self.l,self.a,x,.33,0,1)))
    def test_single_fisher_identical_columns(self):
        f=fisher_reduced(self.l,self.a,.13,.2,self.s)
        self.assertTrue(np.allclose(f[:,2],f[:,3]))
    def test_single_rank_three(self):
        f=fisher_reduced(self.l,self.a,.13,.2,self.s)
        self.assertEqual(subspace_rank(f)[0],3)
    def test_fisher_symmetric_psd(self):
        for cond in [self.s,self.m]:
            f=fisher_reduced(self.l,self.a,.13,.2,cond)
            self.assertTrue(np.allclose(f,f.T))
            self.assertGreaterEqual(np.linalg.eigvalsh(f).min(),-1e-8)
    def test_profile_flat(self):
        x=profile_same_group(self.l,self.a,.13,.2,self.s,np.linspace(-2,2,21))
        self.assertLess(np.max(abs(x)),1e-8)
    def test_profile_invalid_mixed(self):
        with self.assertRaises(ValueError):profile_same_group(self.l,self.a,.13,.2,self.m,[0])
    def test_mixed_full_rank(self):
        f=fisher_reduced(self.l,self.a,.13,.2,self.m)
        self.assertEqual(subspace_rank(f)[0],4)
    def test_intervention_breaks_exact_degeneracy(self):
        f=fisher_reduced(self.l,self.a,.13,.2,self.m)
        self.assertFalse(np.allclose(f[:,2],f[:,3]))
    def test_no_intervention_conditional_information_zero(self):
        f=fisher_reduced(self.l,self.a,.13,.2,self.s)
        self.assertAlmostEqual(conditional_identity_fisher(f),0,places=7)
    def test_mixed_conditional_information_positive(self):
        f=fisher_reduced(self.l,self.a,.13,.2,self.m)
        self.assertGreater(conditional_identity_fisher(f),0)
    def test_fisher_linear_in_trials(self):
        f=fisher_reduced(self.l,self.a,.13,.2,self.m,100)
        f2=fisher_reduced(self.l,self.a,.13,.2,self.m,1000)
        self.assertTrue(np.allclose(f2,10*f))
    def test_analytic_gradient(self):
        x,z=.4,1
        params=np.array([self.l,self.a,.13,.2]);g=grad_reduced(*params[:2],x,*params[2:],z)
        for i in range(4):
            eps=1e-6; p=params.copy();q=params.copy();p[i]+=eps;q[i]-=eps
            gp=(reduced_prob(p[0],p[1],x,p[2],p[3],z)-reduced_prob(q[0],q[1],x,q[2],q[3],z))/(2*eps)
            self.assertTrue(np.allclose(gp,g[:,i],atol=1e-8))
    def test_asimov_zero_at_truth(self):
        self.assertAlmostEqual(asimov_deviance(self.l,self.a,.13,.2,self.m,.13,.2),0)
    def test_asimov_nonzero_wrong_delta(self):
        self.assertGreater(asimov_deviance(self.l,self.a,.13,.2,self.m,.13,0),0)
    def test_summary(self):
        x=summary();self.assertEqual(x['single_group_rank'],3);self.assertEqual(x['intervention_rank'],4)

if __name__=='__main__':unittest.main()
