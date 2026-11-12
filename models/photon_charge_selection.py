"""Formal photon-number selection rules for normally ordered monomials.

This is symbolic operator counting, not a QED scattering calculation.
"""
def photon_number_change(annihilations, creations):
    if any(not isinstance(x,int) or isinstance(x,bool) or x<0 for x in (annihilations,creations)):
        raise ValueError("operator counts must be nonnegative integers")
    return creations-annihilations

def conserves_photon_number(terms):
    """Each term is (number_of_annihilations, number_of_creations).

    For distinct independent operator monomials, exact U(1) invariance
    requires every nonzero term to have zero photon-number charge.
    """
    return all(photon_number_change(a,c)==0 for a,c in terms)

def excitation_total_change(annihilations,creations,atomic_raise,atomic_lower):
    """Change of N_photon+N_atomic_excitation for a monomial."""
    if any(not isinstance(x,int) or isinstance(x,bool) or x<0 for x in
           (annihilations,creations,atomic_raise,atomic_lower)):
        raise ValueError("operator counts must be nonnegative integers")
    return creations-annihilations+atomic_raise-atomic_lower

if __name__=="__main__":
    print("JC absorption a sigma_+: photon number change",photon_number_change(1,0))
    print("JC absorption a sigma_+: total excitation change",excitation_total_change(1,0,1,0))
    print("JC interaction conserves photon number:",conserves_photon_number([(1,0),(0,1)]))
    print("Scattering a^dagger a conserves photon number:",conserves_photon_number([(1,1)]))
