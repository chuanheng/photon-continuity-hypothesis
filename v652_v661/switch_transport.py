"""Compare predeclared Geant4 EM lists, production cuts, and Al foil thickness."""
import argparse
import json
from pathlib import Path
import geant4_pybind as g
from v622_v631.geant import Source
from v632_v641.trace import Trace


class Foil(g.G4VUserDetectorConstruction):
    def __init__(self, thickness):
        super().__init__()
        self.thickness = thickness*g.mm

    def Construct(self):
        materials = g.G4NistManager.Instance()
        world = g.G4LogicalVolume(g.G4Box('world',2*g.cm,2*g.cm,2*g.cm),
                                  materials.FindOrBuildMaterial('G4_Galactic'),'world')
        root = g.G4PVPlacement(None,g.G4ThreeVector(),world,'world',None,False,0)
        foil = g.G4LogicalVolume(g.G4Tubs('foil',0,5*g.mm,self.thickness/2,0,360*g.deg),
                                 materials.FindOrBuildMaterial('G4_Al'),'foil')
        position = g.G4ThreeVector(0,0,.5*g.mm-self.thickness/2)
        g.G4PVPlacement(None,position,foil,'foil',world,False,0)
        return root


class Physics(g.G4VModularPhysicsList):
    def __init__(self, variant, cut):
        super().__init__()
        ctor = {'polarized':g.G4EmLivermorePolarizedPhysics,
                'penelope':g.G4EmPenelopePhysics}[variant]
        self.RegisterPhysics(ctor())
        self.SetDefaultCutValue(cut*g.mm)



class Scorer(Trace):
    def __init__(self):
        super().__init__()
        self.gamma = 0
        self.birth_events = set()

    def UserSteppingAction(self, step):
        super().UserSteppingAction(step)
        track=step.GetTrack()
        if track.GetCurrentStepNumber()==1 and track.GetParentID() and track.GetDefinition().GetParticleName()=='gamma':
            self.gamma += 1
            self.birth_events.add(g.G4RunManager.GetRunManager().GetCurrentEvent().GetEventID())


def main():
    p=argparse.ArgumentParser()
    p.add_argument('output',type=Path)
    p.add_argument('variant',choices=['polarized','penelope'])
    p.add_argument('cut_mm',type=float)
    p.add_argument('thickness_mm',type=float)
    p.add_argument('seed',type=int)
    p.add_argument('--count',type=int,default=1000000)
    a=p.parse_args()
    g.HepRandom.setTheSeed(a.seed)
    m=g.G4RunManager()
    geometry=Foil(a.thickness_mm)
    physics=Physics(a.variant,a.cut_mm)
    m.SetUserInitialization(geometry)
    m.SetUserInitialization(physics)
    gun=Source()
    gun.gun.SetParticlePosition(g.G4ThreeVector(0,0,-2*g.mm))
    m.SetUserAction(gun)
    trace=Scorer()
    m.SetUserAction(trace)
    m.Initialize()
    m.BeamOn(a.count)
    a.output.write_text(json.dumps(dict(physics=a.variant,cut_mm=a.cut_mm,
        thickness_mm=a.thickness_mm,seed=a.seed,incident=a.count,counts=trace.counts,
        selected=trace.rows,single_losses=trace.single_losses,
        secondary_gamma_births=trace.gamma,events_with_secondary_gamma=len(trace.birth_events)),indent=2)+'\n')


if __name__=='__main__':
    main()
