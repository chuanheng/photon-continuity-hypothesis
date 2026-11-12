import pathlib,sys,unittest,math
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from persistence_sequences import fractional_energy,expected_poisson_energy,fixed_gap_energy

class PersistenceTests(unittest.TestCase):
    def test_finite_steps_positive(self):
        for n in range(100):
            self.assertGreater(fractional_energy(60,.1,n),0)
    def test_monotone(self):
        self.assertLess(fractional_energy(60,.1,10),fractional_energy(60,.1,9))
    def test_poisson_zero(self):
        self.assertEqual(expected_poisson_energy(60,.1,1,0),60)
    def test_poisson_mean(self):
        self.assertAlmostEqual(expected_poisson_energy(60,.1,2,3),60*math.exp(-.6))
    def test_fixed_gap_threshold(self):
        with self.assertRaises(ValueError): fixed_gap_energy(3,1,3)
    def test_fixed_gap_positive(self):
        self.assertEqual(fixed_gap_energy(3,1,2),1)
    def test_invalid(self):
        with self.assertRaises(ValueError): fractional_energy(60,1,2)

if __name__=="__main__": unittest.main()
