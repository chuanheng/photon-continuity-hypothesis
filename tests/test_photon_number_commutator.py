import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from photon_number_commutator import commutator_with_photon_number,is_photon_number_conserved

class CommutatorTests(unittest.TestCase):
    def test_block_diagonal_conserves(self):
        self.assertTrue(is_photon_number_conserved([[0,2,0],[2,1,0],[0,0,3]]))
    def test_high_to_vacuum_breaks(self):
        self.assertFalse(is_photon_number_conserved([[0,0,.1],[0,1,0],[.1,0,2]]))
    def test_low_to_vacuum_breaks(self):
        self.assertFalse(is_photon_number_conserved([[0,0,0],[0,1,.2],[0,.2,2]]))
    def test_sign(self):
        c=commutator_with_photon_number([[0,0,2],[0,1,0],[2,0,3]])
        self.assertEqual(c[0][2],-2)
        self.assertEqual(c[2][0],2)
    def test_bad_shape(self):
        with self.assertRaises(ValueError): commutator_with_photon_number([[1]])
    def test_asymmetric(self):
        with self.assertRaises(ValueError): commutator_with_photon_number([[0,0,1],[0,1,0],[0,0,2]])
    def test_tolerance(self):
        with self.assertRaises(ValueError): is_photon_number_conserved([[0,0,0],[0,1,0],[0,0,2]],-1)

if __name__=="__main__": unittest.main()
