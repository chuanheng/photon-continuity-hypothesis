"""Replay foil transport and retain individual angles, energies and track ancestry."""
import argparse
from collections import Counter
import json
from math import acos, degrees
from pathlib import Path

import geant4_pybind as g
from v622_v631.geant import Geometry, Physics, Source


def angle(cosine):
    return degrees(acos(max(-1., min(1., cosine))))


class Trace(g.G4UserSteppingAction):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.history = []
        self.counts = Counter()
        self.single_losses = []

    def UserSteppingAction(self, step):
        track = step.GetTrack()
        primary = track.GetParentID() == 0
        if not primary and track.GetDefinition().GetParticleName() != "gamma":
            return
        if track.GetCurrentStepNumber() == 1:
            self.history = []
        pre = step.GetPreStepPoint()
        end = step.GetPostStepPoint()
        if pre.GetTouchable().GetVolume().GetName() != "foil":
            return
        if end.GetStepStatus() != g.fGeomBoundary:
            if track.GetKineticEnergy() > 0:
                mu = pre.GetMomentumDirection().dot(end.GetMomentumDirection())
                self.history.append(dict(process=end.GetProcessDefinedStep().GetProcessName(),
                                         before=pre.GetKineticEnergy()/g.keV,
                                         after=end.GetKineticEnergy()/g.keV, angle=angle(mu)))
            return
        if abs(end.GetPosition().z-.5*g.mm)>1e-7*g.mm:
            return
        direction = end.GetMomentumDirection()
        if direction.z < 0.9986295347545738:
            return
        energy = end.GetKineticEnergy()/g.keV
        who = 'primary' if primary else 'secondary'
        self.counts[who+'_forward'] += 1
        if abs(energy-60) < 1e-9:
            self.counts[who+'_line'] += 1
        if primary and len(self.history)==1 and self.history[0]['process']=='compt':
            self.single_losses.append([angle(direction.z),60-energy])
        if 35 <= energy <= 58:
            event = g.G4RunManager.GetRunManager().GetCurrentEvent().GetEventID()
            self.rows.append(dict(event=event,track=track.GetTrackID(),parent=track.GetParentID(),
                                  energy=energy,exit_angle=angle(direction.z),steps=self.history.copy()))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('output', type=Path)
    parser.add_argument('count', type=int)
    parser.add_argument('seed', type=int)
    args=parser.parse_args()
    g.HepRandom.setTheSeed(args.seed)
    manager=g.G4RunManagerFactory.CreateRunManager(g.G4RunManagerType.Serial)
    manager.SetUserInitialization(Geometry())
    manager.SetUserInitialization(Physics())
    manager.SetUserAction(Source())
    scorer=Trace()
    manager.SetUserAction(scorer)
    manager.Initialize()
    manager.BeamOn(args.count)
    args.output.write_text(json.dumps(dict(incident=args.count,seed=args.seed,
        counts=scorer.counts,events=scorer.rows,single_losses=scorer.single_losses),indent=2)+'\n')


if __name__=='__main__':
    main()
