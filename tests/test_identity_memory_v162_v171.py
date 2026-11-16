"""Ten stage checks for v1.62-v1.71. Run with unittest discover."""
import unittest
import numpy as np
from models.identity_memory_v162_v171 import run,storage_unitary,fringe,dephase,density
class IdentityMemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=run()
    def test_v162(self):self.assertLess(self.data['v1.62']['unitarity_max_error'],1e-12)
    def test_v163(self):self.assertAlmostEqual(self.data['v1.63']['matter_probability'],1)
    def test_v164(self):self.assertAlmostEqual(self.data['v1.64']['fidelity'],1)
    def test_v165(self):self.assertAlmostEqual(self.data['v1.65']['coherence_visibility'],.6)
    def test_v166(self):self.assertEqual(self.data['v1.66']['trace_distance'],0)
    def test_v167(self):self.assertGreater(self.data['v1.67']['conditional_mode0_fraction'],.5)
    def test_v168(self):self.assertLess(abs(self.data['v1.68']['local_fisher_eigenvalues'][0]),1e-10)
    def test_v169(self):self.assertGreater(self.data['v1.69']['joint_determinant'],0)
    def test_v170(self):
        self.assertEqual(self.data['v1.70']['positive_count'],7314)
        self.assertGreater(self.data['v1.70']['KL_to_fixed_baseline'],0)
        self.assertEqual(self.data['v1.70']['profiled_KL'],0)
    def test_v171(self):self.assertFalse(self.data['v1.71']['unique_identity_observable'])
if __name__=='__main__':unittest.main()
