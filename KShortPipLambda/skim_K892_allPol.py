#!/usr/bin/env python3
import signal
import os
import ROOT
ROOT.gROOT.SetBatch(True)

# Bring in FSRoot
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# ---------------------- inputs (DATA & MC) ---------------------
FND_sp18 = "/volatile/halld/home/dbarton/pipkslamb/data/spring2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_sp18_pol_ALL.root"
FND_fa18 = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_fa18_pol_ALL.root"
FND_sp20 = "/volatile/halld/home/dbarton/pipkslamb/data/spring2020/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_sp20_polALL.root"
FND_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"
FND_THROWN = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_thrown_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"
NT = "ntFSGlueX_100000000_1100"

# ----------------------- outputs (DATA) ---------------------
baseDir = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/sourceFiles/"
pols = ["0", "45", "90", "135"]

FND_generalCuts_sp18 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_sp18_pol_ALL.root"
FND_generalCuts_fa18 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_fa18_pol_ALL.root"
FND_generalCuts_sp20 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_sp20_pol_ALL.root"
# hadd above 3 files (separate script) to match fileName below ...sp18fa18sp20_pol_ALL.root
FND_generalCuts_sp18fa18sp20 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_sp18fa18sp20_pol_ALL.root"
FND_data_prefix = f"tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol"
FND_bkgnd_prefix = f"tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol"

# ----------------------- outputs (MC) ----------------------
FND_generalCuts_MC = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC_sp18fa18.root"
FND_accmc = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root" # this is the accepted MC, not THROWN.
FND_genmc = f"{baseDir}tree_pipkslamb_SIGNAL_SKIM_K892_THROWN_sp18fa18.root" # aka THROWN.

# ---------------------- particle definitions (FSRoot) ----------------------
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
    # Spring 2017 - Fall 2018: 30,000 - 59,999.  Spring 2020 - Spring 2023: 70,000 - 122,000. Spring 2025: 130,000 - 139,999gg
    ROOT.FSCut.defineCut(
        "coherentPeak",
        "("
        "(Run>=30000 && Run<=59999 && EnPB>8.2 && EnPB<8.8) ||"
        "(Run>=70000 && Run<=122000 && EnPB>8.0 && EnPB<8.6) ||"
        "(Run>=130000 && Run<=139999 && EnPB>8.3 && EnPB<8.9)"
        ")")
    ROOT.FSCut.defineCut("flightLengthLambda", "VeeLP1>2.0")
    ROOT.FSCut.defineCut("flightLengthKShort", "VeeLP2>2.0")
    ROOT.FSCut.defineCut("targetZ", "ProdVz>52.0 && ProdVz<78.0")
    ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("selectKSTAR892", f"MASS({DecayingKShort},{PiPlus1})>0.80 && MASS({DecayingKShort},{PiPlus1})<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})>2.00 && MASS({DecayingLambda},{PiPlus1})<4.0")

def setup_genmc():
    ROOT.FSCut.defineCut("tRangeTHROWN", "abs(-1*MCMASS2(GLUEXTARGET,-1))<0.1 && abs(-1*MCMASS2(GLUEXTARGET,-1))<1.0")
    ROOT.FSCut.defineCut("KShortTHROWN", "abs(MCMASS(2)-0.4976)<0.03", "(abs(MCMASS(2)-0.4976+0.0974)<0.015 || abs(MCMASS(2)-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("LambdaTHROWN", "abs(MCMASS(1)-1.119)<0.01375", "(abs(MCMASS(1)-1.119+0.032875)<0.006875 || abs(MCMASS(1)-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("coherentPeakTHROWN", "MCEnPB>8.2 && MCEnPB<8.6")
    ROOT.FSCut.defineCut("selectKSTAR892THROWN", "MCMASS(2,3)>0.80 && MCMASS(2,3)<1.00")

generalCuts = "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
signalCuts = f"CUT(rf,KShort,Lambda)"
signalCutsMC = "CUT(KShort,Lambda)"
# signalCuts_weights = "CUTWT(rf,KShort,Lambda)" # "CUTWT" only used for MC
signalCuts_weightsMC = "CUTWT(KShort,Lambda)"
sidebandWeights = "CUTSBWT(rf,KShort,Lambda)"
signalCuts_THROWN = "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"

# --------------------- skims ---------------------

def skim_K892_DATA_generalSkims():
    setup()
    ROOT.FSModeTree.skimTree(FND_sp18, NT, "", FND_generalCuts_sp18, f"{generalCuts}")
#    ROOT.FSModeTree.skimTree(FND_fa18, NT, "", FND_generalCuts_fa18, f"{generalCuts}")
#    ROOT.FSModeTree.skimTree(FND_sp20, NT, "", FND_generalCuts_sp20, f"{generalCuts}")

def skim_K892_data_bkgnd_allPol(FND_data, FND_bkgnd, pol):
    setup()
    polCutName = f"polAngle{pol}"
    ROOT.FSCut.defineCut(polCutName, f"PolarizationAngle=={pol}")
    signalCuts_pol = f"CUT({polCutName},rf,KShort,Lambda)"
    sidebandWeights_pol = f"CUT({polCutName})*CUTSBWT(rf,KShort,Lambda)"
    print(f"signalCuts_pol: {signalCuts_pol}")
    print(f"sidebandWeights_pol: {sidebandWeights_pol}")
    ROOT.FSModeTree.skimTree(FND_generalCuts_sp18fa18sp20, NT, "", FND_data, signalCuts_pol)
    ROOT.FSModeTree.skimTree(FND_generalCuts_sp18fa18sp20, NT, "", FND_bkgnd, sidebandWeights_pol)
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(sidebandWeights_pol))]
    ROOT.FSModeTree.createFriendTree(FND_bkgnd, NT, "", "weight", friendTreeContents)

def skim_K892_accmc():
    setup()
    ROOT.FSModeTree.skimTree(FND_MC, NT, "", FND_generalCuts_MC, f"{generalCuts}")
    ROOT.FSModeTree.skimTree(FND_generalCuts_MC, NT, "", FND_accmc, f"{signalCutsMC}")
    friendTreeContentsMC = [(ROOT.TString("weight"), ROOT.TString(f"{signalCuts_weightsMC}"))]
    ROOT.FSModeTree.createFriendTree(FND_accmc, NT, "", "weight", friendTreeContentsMC)

def skim_K892_genmc():
    setup_genmc()
    ROOT.FSModeTree.skimTree(FND_THROWN, NT, "", FND_genmc, f"{signalCuts_THROWN}")

def skim_K892():
    skim_K892_DATA_generalSkims()
#    print("Exists?", os.path.exists(FND_generalCuts_sp18fa18sp20))
#    print("Input file:", FND_generalCuts_sp18fa18sp20)
#    for pol in pols:
#        FND_data = f"{baseDir}{FND_data_prefix}{pol}.root"
#        FND_bkgnd = f"{baseDir}{FND_bkgnd_prefix}{pol}.root"
#        print (f"Skimming data and background for polarization {pol}...")
#        skim_K892_data_bkgnd_allPol(FND_data, FND_bkgnd, pol)
#    skim_K892_accmc()
#    skim_K892_genmc()

if __name__ == "__main__":
    skim_K892()
