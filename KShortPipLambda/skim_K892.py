#!/usr/bin/env python3
import signal
import os
import ROOT
ROOT.gROOT.SetBatch(True)

# Bring in FSRoot
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# ---------------------- inputs (DATA & MC) ---------------------
FND0 = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PARA_0_sp18fa18sp20_40856_73266.root"
FND45 = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PERP_45_sp18fa18sp20_40856_73266.root"
FND90 = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PERP_90_sp18fa18sp20_40856_73266.root"
FND135 = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PARA_135_sp18fa18sp20_40856_73266.root"
FND_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"
FND_THROWN = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_thrown_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"
NT = "ntFSGlueX_100000000_1100"

# ----------------------- outputs (DATA) ---------------------
baseDir = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/sourceFiles/"

# mandelstam t(0.1, 1.0)
# FND0_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol0.root"
# FND45_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol45.root"
# FND90_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol90.root"
# FND135_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol135.root"

# mandelstam t(0.1, 0.3)
FND0_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol0.root"
FND45_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol45.root"
FND90_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol90.root"
FND135_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol135.root"

# mandelstam t(0.3, 0.5)
FND0_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol0.root"
FND45_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol45.root"
FND90_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol90.root"
FND135_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol135.root"

# mandelstam t(0.5, 1.0)
FND0_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol0.root"
FND45_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol45.root"
FND90_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol90.root"
FND135_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol135.root"

FND0_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol0.root"
FND45_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol45.root"
FND90_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol90.root"
FND135_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol135.root"

FND0_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol0.root"
FND45_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol45.root"
FND90_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol90.root"
FND135_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol135.root"

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
    ROOT.FSCut.defineCut("tRange110", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")
    ROOT.FSCut.defineCut("tRange13", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<0.3")
    ROOT.FSCut.defineCut("tRange35", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.3 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<0.5")
    ROOT.FSCut.defineCut("tRange510", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.5 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")
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

generalCuts = "CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
generalCuts_t13 = "CUT(tRange13,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
generalCuts_t35 = "CUT(tRange35,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
generalCuts_t510 = "CUT(tRange510,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
signalCuts = "CUT(rf,KShort,Lambda)"
signalCutsMC = "CUT(KShort,Lambda)"
# signalCuts_weights = "CUTWT(rf,KShort,Lambda)" # "CUTWT" only used for MC
signalCuts_weightsMC = "CUTWT(KShort,Lambda)"
sidebandWeights = "CUTSBWT(rf,KShort,Lambda)"
signalCuts_THROWN = "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"

# --------------------- skims ---------------------

def skim_K892_data_GENERAL_SKIMS():
    setup()
    ROOT.FSModeTree.skimTree(FND0, NT, "", FND0_generalCuts, f"{generalCuts}")
    ROOT.FSModeTree.skimTree(FND45, NT, "", FND45_generalCuts, f"{generalCuts}")
    ROOT.FSModeTree.skimTree(FND90, NT, "", FND90_generalCuts, f"{generalCuts}")
    ROOT.FSModeTree.skimTree(FND135, NT, "", FND135_generalCuts, f"{generalCuts}")

def skim_K892_data_GENERAL_SKIMS_t13():
    setup()
    ROOT.FSModeTree.skimTree(FND0, NT, "", FND0_generalCuts_t13, f"{generalCuts_t13}")
    ROOT.FSModeTree.skimTree(FND45, NT, "", FND45_generalCuts_t13, f"{generalCuts_t13}")
    ROOT.FSModeTree.skimTree(FND90, NT, "", FND90_generalCuts_t13, f"{generalCuts_t13}")
    ROOT.FSModeTree.skimTree(FND135, NT, "", FND135_generalCuts_t13, f"{generalCuts_t13}")

def skim_K892_data_GENERAL_SKIMS_t35():
    setup()
    ROOT.FSModeTree.skimTree(FND0, NT, "", FND0_generalCuts_t35, f"{generalCuts_t35}")
    ROOT.FSModeTree.skimTree(FND45, NT, "", FND45_generalCuts_t35, f"{generalCuts_t35}")
    ROOT.FSModeTree.skimTree(FND90, NT, "", FND90_generalCuts_t35, f"{generalCuts_t35}")
    ROOT.FSModeTree.skimTree(FND135, NT, "", FND135_generalCuts_t35, f"{generalCuts_t35}")

def skim_K892_data_GENERAL_SKIMS_t510():
    setup()
    ROOT.FSModeTree.skimTree(FND0, NT, "", FND0_generalCuts_t510, f"{generalCuts_t510}")
    ROOT.FSModeTree.skimTree(FND45, NT, "", FND45_generalCuts_t510, f"{generalCuts_t510}")
    ROOT.FSModeTree.skimTree(FND90, NT, "", FND90_generalCuts_t510, f"{generalCuts_t510}")
    ROOT.FSModeTree.skimTree(FND135, NT, "", FND135_generalCuts_t510, f"{generalCuts_t510}")

def skim_K892_data_SIG_BKGND_SKIMS_pol0():
    setup()
    ROOT.FSModeTree.skimTree(FND0_generalCuts, NT, "", FND0_data, f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND0_generalCuts, NT, "", FND0_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND0_bkgnd, NT, "", "weight", friendTreeContents)

def skim_K892_data_SIG_BKGND_SKIMS_pol45():
    setup()
    ROOT.FSModeTree.skimTree(FND45_generalCuts, NT, "", FND45_data, f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND45_generalCuts, NT, "", FND45_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND45_bkgnd, NT, "", "weight", friendTreeContents)

def skim_K892_data_SIG_BKGND_SKIMS_pol90():
    setup()
    ROOT.FSModeTree.skimTree(FND90_generalCuts, NT, "", FND90_data, f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND90_generalCuts, NT, "", FND90_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND90_bkgnd, NT, "", "weight", friendTreeContents)

def skim_K892_data_SIG_BKGND_SKIMS_pol135():
    setup()
    ROOT.FSModeTree.skimTree(FND135_generalCuts, NT, "", FND135_data, f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND135_generalCuts, NT, "", FND135_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND135_bkgnd, NT, "", "weight", friendTreeContents)

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
    # skim_K892_data_GENERAL_SKIMS()
    # skim_K892_data_GENERAL_SKIMS_t13()
    # skim_K892_data_GENERAL_SKIMS_t35()
    # skim_K892_data_GENERAL_SKIMS_t510()
    skim_K892_data_SIG_BKGND_SKIMS_pol0()
    skim_K892_data_SIG_BKGND_SKIMS_pol45()
    skim_K892_data_SIG_BKGND_SKIMS_pol90()
    skim_K892_data_SIG_BKGND_SKIMS_pol135()
    # skim_K892_accmc()
    # skim_K892_genmc()

if __name__ == "__main__":
    skim_K892()
