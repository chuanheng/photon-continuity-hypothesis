"""Score foil energy deposition and outgoing gamma tracks in a common event."""
import argparse
from collections import Counter
import json
from pathlib import Path

import geant4_pybind as g
from v622_v631.geant import Geometry, Physics, Source


class FoilEvents(g.G4UserSteppingAction):
    def __init__(self):
        super().__init__()
        self.event = -1
        self.rows = []
        self.selected = []
        self.deposited = 0.
        self.counts = Counter()

    def finish_event(self):
        for energy in self.selected:
            self.rows.append(dict(event=self.event, exit_keV=energy,
                                  foil_deposit_keV=self.deposited))

    def UserSteppingAction(self, step):
        pre = step.GetPreStepPoint()
        if pre.GetTouchable().GetVolume().GetName() != 'foil':
            return
        number = g.G4RunManager.GetRunManager().GetCurrentEvent().GetEventID()
        if number != self.event:
            self.finish_event()
            self.event = number
            self.selected = []
            self.deposited = 0.
        self.deposited += step.GetTotalEnergyDeposit() / g.keV
        end = step.GetPostStepPoint()
        if end.GetStepStatus() != g.fGeomBoundary or step.GetTrack().GetParentID() != 0:
            return
        if abs(end.GetPosition().z - .5*g.mm) > 1e-7*g.mm:
            return
        if end.GetMomentumDirection().z < 0.9986295347545738:
            return
        energy = end.GetKineticEnergy()/g.keV
        self.counts['forward'] += 1
        if 35 <= energy <= 58:
            self.selected.append(energy)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('--count', type=int, default=5000000)
    parser.add_argument('--seed', type=int, default=622628)
    args = parser.parse_args()
    g.HepRandom.setTheSeed(args.seed)
    manager = g.G4RunManagerFactory.CreateRunManager(g.G4RunManagerType.Serial)
    manager.SetUserInitialization(Geometry())
    manager.SetUserInitialization(Physics())
    manager.SetUserAction(Source())
    scorer = FoilEvents()
    manager.SetUserAction(scorer)
    manager.Initialize()
    manager.BeamOn(args.count)
    scorer.finish_event()
    args.output.write_text(json.dumps(dict(seed=args.seed, incident=args.count,
        counts=scorer.counts, selected=scorer.rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
