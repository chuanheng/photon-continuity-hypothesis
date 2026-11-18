import unittest
from models.identity_light_matter_v262_v271 import run
class TenRounds(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_262(self):self.assertLess(self.r['v2.62']['unitarity_error'],1e-12)
 def test_263(self):self.assertAlmostEqual(self.r['v2.63']['matter_probability'],1)
 def test_264(self):self.assertAlmostEqual(self.r['v2.64']['retrieval_fidelity'],1)
 def test_265(self):self.assertGreater(self.r['v2.65']['detuned_free_energy_commutator_norm'],1)
 def test_266(self):self.assertAlmostEqual(self.r['v2.66']['analytic_max_transfer'],self.r['v2.66']['numerical_max_transfer'])
 def test_267(self):self.assertGreater(self.r['v2.67']['mode_transfer_probabilities'][0]-self.r['v2.67']['mode_transfer_probabilities'][1],.2)
 def test_268(self):self.assertAlmostEqual(self.r['v2.68']['probe_Xplus_m0']+self.r['v2.68']['probe_Xplus_m1'],1)
 def test_269(self):self.assertAlmostEqual(self.r['v2.69']['probe_free_energy_commutator_fro'],4)
 def test_270(self):self.assertGreater(self.r['v2.70']['KL_vs_fixed_resonance'],.2);self.assertEqual(self.r['v2.70']['profiled_KL_with_standard_detuning'],0)
 def test_271(self):self.assertFalse(self.r['v2.71']['identity_specific_prediction'])
if __name__=='__main__':unittest.main()
