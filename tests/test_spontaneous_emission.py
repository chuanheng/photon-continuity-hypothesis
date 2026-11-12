import math
import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from spontaneous_emission import excited_population,emitted_by_time,waiting_time_density,emission_quantile,density_matrix

class TestSpontaneousEmission(unittest.TestCase):
    def test_initial_excited(self): self.assertEqual(excited_population(2,0),1)
    def test_lifetime(self): self.assertAlmostEqual(excited_population(2,.5),math.exp(-1))
    def test_emission_cdf(self): self.assertAlmostEqual(emitted_by_time(2,.5),1-math.exp(-1))
    def test_cdf_complement(self):
        for t in (0,.1,1,10): self.assertAlmostEqual(excited_population(.7,t)+emitted_by_time(.7,t),1)
    def test_density(self): self.assertAlmostEqual(waiting_time_density(2,0),2)
    def test_median(self): self.assertAlmostEqual(emission_quantile(2,.5),math.log(2)/2)
    def test_quantile_inverse(self):
        for p in (0,.1,.5,.99): self.assertAlmostEqual(emitted_by_time(1.2,emission_quantile(1.2,p)),p)
    def test_zero_rate(self): self.assertEqual(emitted_by_time(0,100),0)
    def test_density_trace(self):
        rho=density_matrix(.7,complex(.1,.2),.8,2)
        self.assertAlmostEqual(rho[0][0]+rho[1][1],1)
        self.assertEqual(rho[1][0],rho[0][1].conjugate())
    def test_coherence_decay(self):
        rho=density_matrix(.5,.5,2,1)
        self.assertAlmostEqual(rho[0][1].real,.5*math.exp(-1))
    def test_full_decay(self): self.assertLess(density_matrix(1,0,1,100)[0][0],1e-40)
    def test_invalid_rate(self):
        with self.assertRaises(ValueError): excited_population(-1,1)
    def test_invalid_probability(self):
        with self.assertRaises(ValueError): emission_quantile(1,1)
    def test_invalid_density(self):
        with self.assertRaises(ValueError): density_matrix(.5,1,1,1)
    def test_invalid_time(self):
        with self.assertRaises(ValueError): waiting_time_density(1,float('nan'))

if __name__=='__main__': unittest.main()
