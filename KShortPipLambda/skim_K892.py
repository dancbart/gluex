#!/usr/bin/env python3
import ROOT
ROOT.gROOT.SetBatch(True)

# Bring in FSRoot
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# Inputs
# SMALL DATA FILE
FND0 = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_small.root"
# LARGE DATA FILE
# FND0 = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root"
FND0_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__sp-fa18_B4_M16_M18_gen_amp_V2_FSflat_REACTIONFILTER-ONLY.root"
FND0_THROWN = "/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_thrown_sp-fa18_gen_amp_V2_FSflat_RXNfltrONLY.root"
NT = "ntFSGlueX_100000000_1100"

DecayingLambda = "1"
Proton         = "1a"
PiMinus2       = "1b"
DecayingKShort = "2"
PiPlus2        = "2a"
PiMinus1       = "2b"
PiPlus1        = "3"

# --------------------- cuts ---------------------
def setup():
    ROOT.FSCut.defineCut("tRange", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")

    ROOT.FSCut.defineCut("rf", "abs(RFDeltaT)>2.0", "abs(RFDeltaT)>6.0", 0.1667)
    ROOT.FSCut.defineCut("chi2DOF", "Chi2DOF<5.0")
    ROOT.FSCut.defineCut("unusedE", "EnUnusedSh<0.1")
    ROOT.FSCut.defineCut("unusedTracks", "NumUnusedTracks<1")
    ROOT.FSCut.defineCut("coherentPeak", "EnPB>8.2 && EnPB<8.8")
    ROOT.FSCut.defineCut("flightLengthLambda", "VeeLP1>2.0")
    ROOT.FSCut.defineCut("flightLengthKShort", "VeeLP2>2.0")
    ROOT.FSCut.defineCut("targetZ", "ProdVz>52.0 && ProdVz<78.0")

    ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("selectKSTAR892", f"MASS({DecayingKShort},{PiPlus1})>0.80 && MASS({DecayingKShort},{PiPlus1})<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})>2.0 && MASS({DecayingLambda},{PiPlus1})<4.0")

def setupTHROWN():
    ROOT.FSCut.defineCut("tRangeTHROWN", "abs(-1*MCMASS2(GLUEXTARGET,-1))<0.1 && abs(-1*MCMASS2(GLUEXTARGET,-1))<1.0")
    ROOT.FSCut.defineCut("KShortTHROWN", "abs(MCMASS(2)-0.4976)<0.03", "(abs(MCMASS(2)-0.4976+0.0974)<0.015 || abs(MCMASS(2)-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("LambdaTHROWN", "abs(MCMASS(1)-1.119)<0.01375", "(abs(MCMASS(1)-1.119+0.032875)<0.006875 || abs(MCMASS(1)-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("coherentPeakTHROWN", "MCEnPB>8.2 && MCEnPB<8.8")
    ROOT.FSCut.defineCut("selectKSTAR892THROWN", "MCMASS(2,3)>0.80 && MCMASS(2,3)<1.00")


# --------------------- skims ---------------------
def skim_K892_DATA():
    setup()
    ROOT.FSModeTree.skimTree(
        FND0, NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root",
        "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda)"
    )
    ROOT.FSModeTree.skimTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root",
        NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892.root",
        "CUT(rejectSigma1385)*CUTWT(rf,KShort,Lambda)"
    )
    ROOT.FSModeTree.skimTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root",
        NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root",
        "CUTSBWT(rf,KShort,Lambda)"
    )
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString("CUTSBWT(rf,KShort,Lambda)"))]
    ROOT.FSModeTree.createFriendTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root",
        NT, "", "weight", friendTreeContents
    )

def skim_K892_MC():
    setup()
    ROOT.FSModeTree.skimTree(
        FND0_MC, NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root",
        "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
    )
    ROOT.FSModeTree.skimTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root",
        NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root",
        "CUT(rf,KShort,Lambda)"
    )
    ROOT.FSModeTree.skimTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root",
        NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_MC.root",
        "CUT()"
    )
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString("CUTSBWT(rf,KShort,Lambda)"))]
    ROOT.FSModeTree.createFriendTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_MC.root",
        NT, "", "weight", friendTreeContents
    )

def skim_K892_THROWN():
    setupTHROWN()
    ROOT.FSModeTree.skimTree(
        FND0_THROWN, NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root",
        "CUT()"
    )
    ROOT.FSModeTree.skimTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root",
        NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_SIGNAL_SKIM_K892_THROWN.root",
        "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"
    )
    ROOT.FSModeTree.skimTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root",
        NT, "",
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_SIDEBAND_SKIM_K892_THROWN.root",
        "CUTSBWT()"
    )
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString("CUTSBWT()"))]
    ROOT.FSModeTree.createFriendTree(
        "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_SIDEBAND_SKIM_K892_THROWN.root",
        NT, "", "weight", friendTreeContents
    )

def skim_K892():
    skim_K892_DATA()
    skim_K892_MC()
    skim_K892_THROWN()

if __name__ == "__main__":
    skim_K892()
