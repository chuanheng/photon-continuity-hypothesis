import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from photoelectric_energy_budget import electron_energy_budget,difference_from_standard

class PhotoelectricBudgetTests(unittest.TestCase):
    def test_zero_extra(self):
        self.assertAlmostEqual(electron_energy_budget(60,1.56),58.44)
    def test_extra_reduces_electron_energy(self):
        self.assertAlmostEqual(electron_energy_budget(60,1.56,.01),58.43)
    def test_energy_balance(self):
        e=electron_energy_budget(60,1.56,.01,.002,.003)
        self.assertAlmostEqual(e+1.56+.01+.002+.003,60)
    def test_negative_input(self):
        with self.assertRaises(ValueError): electron_energy_budget(60,1.56,-.01)
    def test_over_budget(self):
        with self.assertRaises(ValueError): electron_energy_budget(1,2)
    def test_shift(self):
        self.assertAlmostEqual(difference_from_standard(.01,.002),-.012)

if __name__=="__main__": unittest.main()
