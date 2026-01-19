#!/usr/bin/env python3
import signal
import ROOT
ROOT.gROOT.SetBatch(True)

# Bring in FSRoot
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# Inputs
# SMALL DATA FILE
# FND0 = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_small.root"
# LARGE DATA FILE
FND0 = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root"
FND0_MC = "/volatile/halld/home/dbarton/pipkslamb/mc_eventSelection/fall2018/root/trees/flatten/tree_pipkslamb__sp-fa18_B4_M16_M18_gen_amp_V2_FSflat_REACTIONFILTER-ONLY.root"
FND0_THROWN = "/volatile/halld/home/dbarton/pipkslamb/mc_eventSelection/fall2018/root/thrown/flatten/tree_thrown_sp-fa18_gen_amp_V2_FSflat_RXNfltrONLY.root"
NT = "ntFSGlueX_100000000_1100"

DecayingLambda = "1"
Proton         = "1a"
PiMinus2       = "1b"
DecayingKShort = "2"
PiPlus2        = "2a"
PiMinus1       = "2b"
PiPlus1        = "3"

# CUT(base, sideband)
#     logical AND of signal region(s) in `base` and `sideband` cuts, weight = 1
#     yields not sideband-subtracted signal distribution
# CUT(base) && CUTSB(sideband)
#     logical AND of signal region(s) in `base` cut(s) and all sideband regions in `sideband` cut(s)
#     histograms are scaled with sideband weights and summed
#     yields sideband distribution that is subtracted from signal distribution
# CUT(base) * CUTSBWT(sideband)
#     equivalent to above; but the sideband weights are baked into cut string and only a single histogram is created
#     NOTE! applying weights in TFormulas does not work with RDataFrame
# CUT(base) && CUTSUB(sideband)
#     selects signal region(s) defined by `base` and `sideband` cut(s) and subtracts sideband regions in `sideband` cut(s)
#     the sideband histograms are scaled with the corresponding sideband weight and summed
#     summed sideband histograms are subtracted from signal histogram to yield sideband-subtracted distribution
# CUT(base) * CUTWT(sideband)
#     equivalent to above; but the sideband weights are baked into cut string and only a single sideband histogram is created
#     equivalent to CUT(base, sideband) - CUT(base) * CUTSBWT(sideband)
#     NOTE! applying weights in TFormulas does not work with RDataFrame

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
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})>2.00 && MASS({DecayingLambda},{PiPlus1})<4.0")

def setupTHROWN():
    ROOT.FSCut.defineCut("tRangeTHROWN", "abs(-1*MCMASS2(GLUEXTARGET,-1))<0.1 && abs(-1*MCMASS2(GLUEXTARGET,-1))<1.0")
    ROOT.FSCut.defineCut("KShortTHROWN", "abs(MCMASS(2)-0.4976)<0.03", "(abs(MCMASS(2)-0.4976+0.0974)<0.015 || abs(MCMASS(2)-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("LambdaTHROWN", "abs(MCMASS(1)-1.119)<0.01375", "(abs(MCMASS(1)-1.119+0.032875)<0.006875 || abs(MCMASS(1)-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("coherentPeakTHROWN", "MCEnPB>8.2 && MCEnPB<8.8")
    ROOT.FSCut.defineCut("selectKSTAR892THROWN", "MCMASS(2,3)>0.80 && MCMASS(2,3)<1.00")

generalCuts = "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
signalCuts = "CUT(rf,KShort,Lambda)"
signalCutsMC = "CUT(KShort,Lambda)"
signalCuts_weights = "CUTWT(rf,KShort,Lambda)"
signalCuts_weightsMC = "CUTWT(KShort,Lambda)"
sidebandWeights = "CUTSBWT(rf,KShort,Lambda)"
signalCuts_THROWN = "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"

# --------------------- skims ---------------------
def skim_K892_DATA():
    setup()
    FND0_generalCuts = "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root" # define output fileName for general cuts
    ROOT.FSModeTree.skimTree(FND0, NT, "", FND0_generalCuts, f"{generalCuts}")
    ROOT.FSModeTree.skimTree(FND0_generalCuts, NT, "", "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892.root", f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND0_generalCuts, NT, "", "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root", f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root", NT, "", "weight", friendTreeContents)

def skim_K892_MC():
    setup()
    FND0_MC_generalCuts = "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root" # define output MCfileName for general cuts
    ROOT.FSModeTree.skimTree(FND0_MC, NT, "", FND0_MC_generalCuts, f"{generalCuts}")
    ROOT.FSModeTree.skimTree(FND0_MC_generalCuts, NT, "", "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root", f"{signalCutsMC}")
    friendTreeContentsMC = [(ROOT.TString("weight"), ROOT.TString(f"{signalCuts_weightsMC}"))]
    ROOT.FSModeTree.createFriendTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root", NT, "", "weight", friendTreeContentsMC)

def skim_K892_THROWN():
    setupTHROWN()
    ROOT.FSModeTree.skimTree(FND0_THROWN, NT, "", "/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_SIGNAL_SKIM_K892_THROWN.root", f"{signalCuts_THROWN}")

def skim_K892():
    skim_K892_DATA()
    skim_K892_MC()
    skim_K892_THROWN()

if __name__ == "__main__":
    skim_K892()
