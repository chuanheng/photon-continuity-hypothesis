import unittest
from v402_v411.model import run
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=run()
 def test_402(self):self.assertAlmostEqual(sum(self.r['two_time']),1)
 def test_403(self):self.assertAlmostEqual(sum(self.r['three_time']),1)
 def test_404(self):self.assertEqual(len(self.r['three_time']),8)
 def test_405(self):self.assertGreater(self.r['conditional_history_difference'],.08)
 def test_406(self):self.assertAlmostEqual(self.r['strong_lumpability_failure'],.3)
 def test_407(self):self.assertGreater(self.r['observed_first_order_Markov_TV'],.04)
 def test_408(self):self.assertAlmostEqual(self.r['reset_normalization'],1)
 def test_409(self):self.assertLess(max(self.r['independent_device_label_errors'].values()),1e-12)
 def test_410(self):self.assertAlmostEqual(self.r['length5_normalization'],1)
 def test_411(self):self.assertFalse(self.r['identity_unique'])
if __name__=='__main__':unittest.main()
