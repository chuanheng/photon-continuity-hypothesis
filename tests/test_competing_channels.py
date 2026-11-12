import math
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'models'))
from competing_channels import populations, absorption_fraction_at_first_transfer

class CompetingChannelsTests(unittest.TestCase):
    def test_initial(self): self.assertEqual(populations(1,1,0),(1,0,0))
    def test_survival_only(self):
        p=populations(1,0,math.pi/2)
        self.assertAlmostEqual(p[1],1)
        self.assertEqual(p[2],0)
    def test_absorption_only(self):
        p=populations(0,1,math.pi/2)
        self.assertAlmostEqual(p[2],1)
    def test_equal_couplings(self):
        p=populations(1,1,math.pi/(2*math.sqrt(2)))
        self.assertAlmostEqual(p[1],.5)
        self.assertAlmostEqual(p[2],.5)
    def test_normalization(self):
        for k,g in ((0,0),(1,0),(0,1),(1,2),(3,.01)):
            for t in (0,.1,1,5):
                p=populations(k,g,t)
                self.assertAlmostEqual(sum(p),1)
                self.assertTrue(all(-1e-12<=x<=1+1e-12 for x in p))
    def test_fraction(self): self.assertAlmostEqual(absorption_fraction_at_first_transfer(3,4),.64)
    def test_zero_coupling(self): self.assertEqual(populations(0,0,1),(1,0,0))
    def test_invalid(self):
        with self.assertRaises(ValueError): populations(-1,1,1)
        with self.assertRaises(ValueError): absorption_fraction_at_first_transfer(0,0)

if __name__=='__main__': unittest.main()
