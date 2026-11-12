import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from hidden_successor_budget import successor_energy,massless_successor_momentum,detectable_above_threshold

class HiddenSuccessorTests(unittest.TestCase):
    def test_residual(self): self.assertAlmostEqual(successor_energy(60,59.999),.001)
    def test_other_outgoing(self): self.assertAlmostEqual(successor_energy(60,58,1),1)
    def test_no_zero_residual(self):
        with self.assertRaises(ValueError): successor_energy(60,60)
    def test_no_negative_residual(self):
        with self.assertRaises(ValueError): successor_energy(60,61)
    def test_massless_momentum(self):
        self.assertAlmostEqual(massless_successor_momentum(299792458),1)
    def test_threshold(self):
        self.assertFalse(detectable_above_threshold(.001,.01))
        self.assertTrue(detectable_above_threshold(.01,.01))
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError): detectable_above_threshold(1,-1)
    def test_invalid_incident(self):
        with self.assertRaises(ValueError): successor_energy(0,0)

if __name__=="__main__": unittest.main()
