"""v1.22-v1.31 ten-stage regression suite; Python stdlib only.
Run: python -m unittest discover -s tests -p 'test_identity_mechanisms_v122_v131.py' -v
"""
import math
import unittest
from models.identity_mechanisms_v122_v131 import (
    HARD,SOFT,E2,E3,SEED,N,BASE_SOFT,EXTRA,EFF,DARK,
    run,householder_to,scatter_matrix,matmul,detector_prob,
    kl_bernoulli,count_clicks,gram2,eig2_sym,
)
class TenStageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results=run()
    def test_v122_hidden_label(self):
        self.assertEqual(self.results["v1.22"]["operational_KL_if_label_only"],0)
    def test_v123_energy_budget(self):
        self.assertEqual(self.results["v1.23"]["energy_mismatch"],E2)
        self.assertGreater(HARD+E2,HARD)
    def test_v124_allowed_soft_channel(self):
        self.assertTrue(self.results["v1.24"]["both_equal_initial"])
    def test_v125_unitarity(self):
        U=scatter_matrix(.7,.25,.05)
        UT=[[U[j][i] for j in range(3)] for i in range(3)]
        I=matmul(U,UT)
        self.assertLess(max(abs(I[i][j]-int(i==j)) for i in range(3) for j in range(3)),1e-12)
        self.assertEqual(len(self.results["v1.25"]["first_column_probabilities"]),3)
    def test_v126_detector_information(self):
        p0=detector_prob(BASE_SOFT)
        p1=detector_prob(BASE_SOFT+EXTRA)
        self.assertGreater(kl_bernoulli(p1,p0),0)
        self.assertAlmostEqual(self.results["v1.26"]["KL_per_trial"],.0013727095186360661,places=11)
    def test_v127_exact_baseline_reparameterization(self):
        self.assertEqual(self.results["v1.27"]["best_fit_KL"],0)
    def test_v128_one_setting_rank_deficiency(self):
        self.assertEqual(self.results["v1.28"]["rank"],1)
        self.assertLess(abs(self.results["v1.28"]["one_setting_Fisher_JtJ_eigenvalues"][0]),1e-12)
    def test_v129_two_setting_local_rank(self):
        self.assertEqual(self.results["v1.29"]["rank"],2)
        self.assertGreater(self.results["v1.29"]["determinant"],.03)
    def test_v130_seeded_counts(self):
        self.assertEqual(self.results["v1.30"]["count_null"],414)
        self.assertEqual(self.results["v1.30"]["count_alternative"],505)
        self.assertGreater(self.results["v1.30"]["alt_logLR"],0)
    def test_v131_no_identity_specific_prediction(self):
        self.assertFalse(self.results["v1.31"]["novel_identity_specific_observable"])
        self.assertFalse(self.results["v1.31"]["identifiable_new_parameter_without_baseline_constraint"])
if __name__=="__main__":
    unittest.main()
