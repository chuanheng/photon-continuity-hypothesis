import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from photon_correlations import g2_zero,fock_distribution,cross_covariance

class Tests(unittest.TestCase):
    def test_fock_one(self): self.assertEqual(g2_zero(fock_distribution(1)),0)
    def test_fock_two(self): self.assertAlmostEqual(g2_zero(fock_distribution(2)),.5)
    def test_fock_three(self): self.assertAlmostEqual(g2_zero(fock_distribution(3)),2/3)
    def test_vacuum_undefined(self):
        with self.assertRaises(ValueError): g2_zero([1.0])
    def test_independent(self): self.assertAlmostEqual(cross_covariance([[.25,.25],[.25,.25]]),0)
    def test_correlated(self): self.assertGreater(cross_covariance([[.5,0],[0,.5]]),0)
    def test_invalid(self):
        with self.assertRaises(ValueError): g2_zero([.1,.1])

if __name__=="__main__": unittest.main()
