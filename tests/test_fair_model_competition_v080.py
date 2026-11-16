import unittest
import numpy as np
from models.fair_model_competition_v080 import *

class ProbabilityTests(unittest.TestCase):
    def test_positive_and_normalized(self):
        for kind,z,x in settings(True):
            p=probabilities(TRUE,x,z,kind)
            self.assertTrue(np.all(p>0));self.assertAlmostEqual(p.sum(),1)
    def test_calibration_ignores_identity_delta(self):
        for z in (0,1):
            self.assertTrue(np.allclose(probabilities(TRUE,1,z,'cal'),
                probabilities(np.r_[TRUE[:4],-.6],1,z,'cal')))
    def test_switch_off_ignores_delta(self):
        for kind in ('test','cal'):
            self.assertTrue(np.allclose(probabilities(TRUE,1,0,kind),
                probabilities(np.r_[TRUE[:4],-.6],1,0,kind)))
    def test_test_only_degenerate(self):
        t=TRUE.copy();t[3]+=t[4];t[4]=0
        for kind,z,x in settings(False):
            self.assertTrue(np.allclose(probabilities(TRUE,x,z,kind), probabilities(t,x,z,kind)))
    def test_calibration_breaks_degeneracy(self):
        t=TRUE.copy();t[3]+=t[4];t[4]=0
        self.assertTrue(any(np.linalg.norm(probabilities(TRUE,x,z,kind)-probabilities(t,x,z,kind))>1e-5
                            for kind,z,x in settings(True)))
    def test_invalid_probability_params(self):
        t=TRUE.copy();t[0]=-.1
        with self.assertRaises(ValueError): probabilities(t,0,0,'test')
    def test_invalid_amplitude(self):
        t=TRUE.copy();t[1]=.9
        with self.assertRaises(ValueError): probabilities(t,0,0,'test')
    def test_invalid_setting(self):
        with self.assertRaises(ValueError): probabilities(TRUE,0,2,'test')
    def test_invalid_kind(self):
        with self.assertRaises(ValueError): probabilities(TRUE,0,1,'unknown')
    def test_kl_identical(self):
        p=probabilities(TRUE,.4,1,'test');self.assertAlmostEqual(kl(p,p),0)
    def test_kl_positive(self):
        p=probabilities(TRUE,.4,1,'test');q=probabilities(TRUE,.9,1,'test');self.assertGreater(kl(p,q),0)
    def test_kl_infinite(self):
        self.assertTrue(np.isinf(kl([1,0,0],[0,1,0])))

class InformationTests(unittest.TestCase):
    def test_gradient_finite_difference(self):
        for kind,z,x in settings(True):
            g=gradient(TRUE,x,z,kind)
            for j in range(5):
                h=1e-6;a=TRUE.copy();b=TRUE.copy();a[j]+=h;b[j]-=h
                fd=(probabilities(a,x,z,kind)-probabilities(b,x,z,kind))/(2*h)
                self.assertTrue(np.allclose(g[:,j],fd,atol=1e-8))
    def test_fisher_symmetric(self):
        for cal in (False,True):
            f=fisher(TRUE,cal);self.assertTrue(np.allclose(f,f.T))
    def test_fisher_psd(self):
        for cal in (False,True):
            self.assertGreaterEqual(np.linalg.eigvalsh(fisher(TRUE,cal)).min(),-1e-7)
    def test_test_only_rank_four(self):
        self.assertEqual(numerical_rank(fisher(TRUE,False))[0],4)
    def test_joint_rank_five(self):
        self.assertEqual(numerical_rank(fisher(TRUE,True))[0],5)
    def test_test_only_kappa_delta_identical(self):
        f=fisher(TRUE,False);self.assertTrue(np.allclose(f[:,3],f[:,4]))
    def test_joint_different_columns(self):
        f=fisher(TRUE,True);self.assertFalse(np.allclose(f[:,3],f[:,4]))
    def test_test_only_conditional_delta_zero(self):
        self.assertAlmostEqual(schur_delta_info(fisher(TRUE,False)),0,places=6)
    def test_joint_conditional_delta_positive(self):
        self.assertGreater(schur_delta_info(fisher(TRUE,True)),10)
    def test_fisher_scales_with_samples(self):
        self.assertTrue(np.allclose(fisher(TRUE,True,1000),10*fisher(TRUE,True,100)))

class ModelSelectionTests(unittest.TestCase):
    def test_deviance_self_zero(self):
        self.assertAlmostEqual(asimov_deviance(TRUE,TRUE),0,places=8)
    def test_test_only_profile_zero(self):
        self.assertLess(abs(profile_delta_null(TRUE,False)['deviance']),1e-7)
    def test_joint_profile_positive(self):
        self.assertGreater(profile_delta_null(TRUE,True)['deviance'],1)
    def test_joint_profile_scales_with_n(self):
        v1=profile_delta_null(TRUE,True,100)['deviance'];v2=profile_delta_null(TRUE,True,1000)['deviance']
        self.assertAlmostEqual(v2/v1,10,places=3)
    def test_free_test_drift_exact_equivalence(self):
        self.assertLess(unconstrained_ordinary_model_equivalence(TRUE),1e-12)
    def test_summary(self):
        s=summary();self.assertEqual((s['test_only_rank'],s['joint_rank']),(4,5))
        self.assertGreater(s['joint_null_fit']['deviance'],0)

if __name__=='__main__':unittest.main()
