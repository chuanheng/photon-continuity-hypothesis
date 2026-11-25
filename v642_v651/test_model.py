import unittest
from v642_v651 import model

class ReferenceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=list(model.run().values())

    def test_matching(self):
        self.assertAlmostEqual(self.r[0]['expected_blank']+self.r[0]['expected_scatter'],self.r[0]['sample_null_mean'])

    def test_exact(self):
        self.assertLess(max(self.r[1]['unconditional_sizes']),.025)

    def test_power(self):
        v=self.r[2]['powers']
        self.assertEqual(v,sorted(v))
        self.assertGreater(v[-1],.9)

    def test_allocation(self):
        a,b,c=self.r[3]
        self.assertLess(b['variance'],min(a['variance'],c['variance']))

    def test_drift(self):
        self.assertGreater(self.r[4]['false_positives'][2],.07)

    def test_robust(self):
        self.assertLess(self.r[5]['worst_endpoint_size'],.025)
        self.assertLess(self.r[5]['nominal_power'],self.r[2]['powers'][1])

    def test_floor(self):
        self.assertAlmostEqual(self.r[6]['largest_hidden_increment'],.05*model.BACKGROUND,15)

    def test_contamination(self):
        self.assertLess(self.r[7]['powers'][-1],.025)

    def test_overdispersion(self):
        a=self.r[8]
        self.assertGreater(a['independent']['size']-a['shared']['size'],.03)

    def test_equivalence(self):
        self.assertLess(self.r[9]['max_gap'],1e-18)
        self.assertAlmostEqual(self.r[9]['required_control_efficiency'],.36)
