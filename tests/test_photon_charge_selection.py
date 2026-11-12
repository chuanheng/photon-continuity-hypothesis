import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"models"))
from photon_charge_selection import photon_number_change,conserves_photon_number,excitation_total_change

class ChargeSelectionTests(unittest.TestCase):
    def test_absorption(self): self.assertEqual(photon_number_change(1,0),-1)
    def test_emission(self): self.assertEqual(photon_number_change(0,1),1)
    def test_scattering(self): self.assertEqual(photon_number_change(1,1),0)
    def test_jc_not_photon_conserving(self):
        self.assertFalse(conserves_photon_number([(1,0),(0,1)]))
    def test_scattering_conserves(self):
        self.assertTrue(conserves_photon_number([(1,1),(2,2)]))
    def test_jc_total_excitation(self):
        self.assertEqual(excitation_total_change(1,0,1,0),0)
        self.assertEqual(excitation_total_change(0,1,0,1),0)
    def test_invalid(self):
        with self.assertRaises(ValueError): photon_number_change(-1,0)
        with self.assertRaises(ValueError): photon_number_change(True,0)

if __name__=="__main__": unittest.main()
