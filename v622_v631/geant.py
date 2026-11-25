"""Serial Geant4 primary escape benchmark with Livermore polarized EM physics.

Run with GEANT4_DATA_DIR containing G4EMLOW8.8 and G4ENSDFSTATE3.0.
"""
from collections import Counter
import argparse
import json
from pathlib import Path
import geant4_pybind as g

class Geometry(g.G4VUserDetectorConstruction):
    def Construct(self):
        nist=g.G4NistManager.Instance()
        world=g.G4LogicalVolume(g.G4Box("world",2*g.cm,2*g.cm,2*g.cm),
                                nist.FindOrBuildMaterial("G4_Galactic"),"world")
        root=g.G4PVPlacement(None,g.G4ThreeVector(),world,"world",None,False,0)
        foil=g.G4LogicalVolume(g.G4Tubs("foil",0,5*g.mm,.5*g.mm,0,360*g.deg),
                               nist.FindOrBuildMaterial("G4_Al"),"foil")
        g.G4PVPlacement(None,g.G4ThreeVector(),foil,"foil",world,False,0)
        return root

class Physics(g.G4VModularPhysicsList):
    def __init__(self):
        super().__init__()
        self.RegisterPhysics(g.G4EmLivermorePolarizedPhysics())

class Source(g.G4VUserPrimaryGeneratorAction):
    def __init__(self):
        super().__init__()
        self.gun=g.G4ParticleGun(1)
        self.gun.SetParticleDefinition(g.G4Gamma.GammaDefinition())
        self.gun.SetParticleEnergy(60*g.keV)
        self.gun.SetParticlePosition(g.G4ThreeVector(0,0,-.6*g.mm))
        self.gun.SetParticleMomentumDirection(g.G4ThreeVector(0,0,1))
    def GeneratePrimaries(self,event):
        self.gun.GeneratePrimaryVertex(event)

class Score(g.G4UserSteppingAction):
    def __init__(self):
        super().__init__()
        self.line=self.selected=self.forward=0
        self.paths=Counter()
        self.history=[]
    def UserSteppingAction(self,step):
        if step.GetTrack().GetParentID()!=0:
            return
        if step.GetTrack().GetCurrentStepNumber()==1:
            self.history=[]
        pre=step.GetPreStepPoint()
        end=step.GetPostStepPoint()
        if pre.GetTouchable().GetVolume().GetName()!="foil":
            return
        if end.GetStepStatus()!=g.fGeomBoundary:
            self.history.append(end.GetProcessDefinedStep().GetProcessName())
            return
        if abs(end.GetPosition().z-.5*g.mm)>1e-7*g.mm:
            return
        if end.GetMomentumDirection().z<0.9986295347545738:
            return
        self.forward+=1
        e=end.GetKineticEnergy()/g.keV
        # Includes zero-loss Rayleigh: recorded separately from true selected.
        self.line+=int(abs(e-60)<1e-9)
        if 35<=e<=58:
            self.selected+=1
            self.paths["/".join(self.history)]+=1

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('count',type=int)
    parser.add_argument('output',type=Path)
    parser.add_argument('--seed',type=int,default=622628)
    args=parser.parse_args()
    g.HepRandom.setTheSeed(args.seed)
    rm=g.G4RunManagerFactory.CreateRunManager(g.G4RunManagerType.Serial)
    rm.SetUserInitialization(Geometry())
    rm.SetUserInitialization(Physics())
    source=Source()
    score=Score()
    rm.SetUserAction(source)
    rm.SetUserAction(score)
    rm.Initialize()
    rm.BeamOn(args.count)
    result=dict(incident=args.count,seed=args.seed,selected=score.selected,
                forward=score.forward,forward_line=score.line,selected_paths=dict(score.paths))
    args.output.write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    main()
