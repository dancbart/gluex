#!/usr/bin/env python3
import signal
import os
import ROOT
import subprocess
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



# =========================================================
# OUTPUT file locations
# =========================================================
# ------ for event selection plots only, not for AmpTools. ------
baseDir_eventSelection = "/volatile/halld/home/dbarton/pipkslamb/skims/"
# ------ for AmpTools. Files needed for AmpTools go here. -------
baseDir = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/sourceFiles/"



# =========================================================
# OUTPUT file names
# =========================================================

# ---------------------------------------------------------
# EVENT SELECTION OUTPUT FILENAMES, not for AmpTools.
# These are just for event selection plots.
# ---------------------------------------------------------

FND0_eventSelectionCuts = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol0.root"
FND45_eventSelectionCuts = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol45.root"
FND90_eventSelectionCuts = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol90.root"
FND135_eventSelectionCuts = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol135.root"
FND_eventSelectionCuts_ALLpols = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols.root"

FND_eventSelectionCuts_MC = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_MC.root"
FND_eventSelectionCuts_THROWN_MC = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_THROWN_MC.root"


# ---------------------------------------------------------
# AMPTOOLS OUTPUT FILENAMES, DATA
# These are the files that get fed into AmpTools.
# ---------------------------------------------------------

# mandelstam t(0.1, 1.0)
FND0_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol0.root"
FND45_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol45.root"
FND90_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol90.root"
FND135_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol135.root"

# mandelstam t(0.1, 0.3)
FND0_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol0.root"
FND45_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol45.root"
FND90_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol90.root"
FND135_generalCuts_t13 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t13_pol135.root"

# mandelstam t(0.3, 0.5)
FND0_generalCuts_t35 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol0.root"
FND45_generalCuts_t35 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol45.root"
FND90_generalCuts_t35 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol90.root"
FND135_generalCuts_t35 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t35_pol135.root"

# mandelstam t(0.5, 1.0)
FND0_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol0.root"
FND45_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol45.root"
FND90_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol90.root"
FND135_generalCuts_t510 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_t510_pol135.root"

FND0_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol0.root"
FND45_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol45.root"
FND90_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol90.root"
FND135_data = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_pol135.root"
FND_data_ALLpols = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_ALLpols.root"

FND0_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol0.root"
FND45_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol45.root"
FND90_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol90.root"
FND135_bkgnd = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_pol135.root"


# ---------------------------------------------------------
# AMPTOOLS OUTPUT FILENAMES, MONTE CARLO
# These are the files that get fed into AmpTools.
# ---------------------------------------------------------
FND_generalCuts_MC = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC_sp18fa18.root"
FND_accmc = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root" # this is the accepted MC, not THROWN.
FND_genmc = f"{baseDir}tree_pipkslamb_SIGNAL_SKIM_K892_THROWN_sp18fa18.root" # aka THROWN.



# --------------- particle definitions (from 'flatten' for FSRoot) --------------
DecayingLambda = "1"
Proton         = "1a"
PiMinus2       = "1b"
DecayingKShort = "2"
PiPlus2        = "2a"
PiMinus1       = "2b"
PiPlus1        = "3"



# -------------- CUT DEFINITIONS ----------------
def setup():
    ROOT.FSCut.defineCut("tRange110", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")
    ROOT.FSCut.defineCut("tRange13", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<0.3")
    ROOT.FSCut.defineCut("tRange35", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.3 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<0.5")
    ROOT.FSCut.defineCut("tRange510", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.5 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")
    ROOT.FSCut.defineCut("rf", "abs(RFDeltaT)>2.0", "abs(RFDeltaT)>6.0", 0.1667)
    ROOT.FSCut.defineCut("chi2DOF", "Chi2DOF<5.0")
    ROOT.FSCut.defineCut("unusedE", "EnUnusedSh<0.1")
    ROOT.FSCut.defineCut("unusedTracks", "NumUnusedTracks<1")
    # Spring 2017 - Fall 2018: runs 30,000 - 59,999.  Spring 2020 - Spring 2023: runs 70,000 - 122,000. Spring 2025: runs 130,000 - 139,999
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
    ROOT.FSCut.defineCut("tRangeTHROWN", "abs(-1*MCMASS2(GLUEXTARGET,-1))>0.1 && abs(-1*MCMASS2(GLUEXTARGET,-1))<1.0")
    ROOT.FSCut.defineCut("tRangeTHROWN35", "abs(-1*MCMASS2(GLUEXTARGET,-1))>0.3 && abs(-1*MCMASS2(GLUEXTARGET,-1))<0.5")
    ROOT.FSCut.defineCut("KShortTHROWN", "abs(MCMASS(2)-0.4976)<0.03", "(abs(MCMASS(2)-0.4976+0.0974)<0.015 || abs(MCMASS(2)-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("LambdaTHROWN", "abs(MCMASS(1)-1.119)<0.01375", "(abs(MCMASS(1)-1.119+0.032875)<0.006875 || abs(MCMASS(1)-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("coherentPeakTHROWN", "MCEnPB>8.2 && MCEnPB<8.6")
    ROOT.FSCut.defineCut("selectKSTAR892THROWN", "MCMASS(2,3)>0.80 && MCMASS(2,3)<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385THROWN", "MCMASS(1,3)>2.00 && MCMASS(1,3)<4.0")


# =========================================================
# CUT LISTS

# Context: FSRoot expects strings to be passed into macros, such as "CUT()".  As formatted, the lists below are parsed as strings by FSRoot, satisfying this requirement.  Within this script, FSRoot functions as a "nested software".  This (nested) software workflow can be visualized as: FSRoot-->ROOT-->Python (i.e. FSRoot lives inside ROOT, ROOT lives inside Python, Python runs the script).  Why we do this:  FSRoot contins specialized macros making analysis much quicker; ROOT is the basic framework for processing .root files; Python is the script that calls all this into action.  There are other ways to do this, like using ROOT directly in a c++ script.  This is just a preference.

# Also, why are cut lists defined here, instead of passing lists dirctly to functions: Defining the lists once as global variables, then passing those globals to all the different skim functions ensures the same cuts are applied accross the board.  Alternatively, cut lists can be passed directly to the functions, as mentioned.  Either approach works, as long as FSRoot gets arguments in the format it expects, i.e. strings.
# =========================================================

# ----- USE FOR EVENT SELECTION PLOTS ONLY!!! ----- #
generalCuts_eventSelection = "CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"

# ----------- USE FOR AMPTOOLS FITTING ------------ #
generalCuts = "CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"
generalCuts_t13 = "CUT(tRange13,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"
generalCuts_t35 = "CUT(tRange35,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"
generalCuts_t510 = "CUT(tRange510,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"
# ----- Above: to make smaller trees. Below: actually used in AmpTools ---- #
signalCuts = "CUT(rf,KShort,Lambda)"
signalCutsMC = "CUT(KShort,Lambda)"
# signalCuts_weights = "CUTWT(rf,KShort,Lambda)" # "CUTWT" only used for MC in the amptools skimming process.
signalCuts_weightsMC = "CUTWT(KShort,Lambda)"
sidebandWeights = "CUTSBWT(rf,KShort,Lambda)"
# THROWN trees are used for efficiency corrections, among other things.  In deciding what cuts to apply think: In general, we want to see the whole phase space, BUT in the kinematic region of interest.  For example, it makes sense to cut on the beam energy used in the analysis, and the invariant mass of the resonance being studied (i.e. K*), and Mandalstam t.  But cuts on THROWN should NOT try to "clean the signal" by applying sideband cuts, or to improve selection of individual final-state particles(flight lengths, rf or baryon background rejection, etc), in so doing you wouldn't be looking at the "whole" phase space, and an acceptance correction (one of the main functions of the THROWN tree) would be inaccurate.
# The cuts below satisfy these criteria.  They cut on the beam energy and the invariant mass of the K* resonance, and Mandalstam t, but they do NOT apply cuts that would otherwise "clean the signal".
signalCuts_THROWN = "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"


# actual skimming functions start here...


# ---------------------------------------------------------
# EVENT SELECTION SKIMS.  NOT for AmpTools.  These are just for event selection plots.
# ---------------------------------------------------------
def skim_DATA_EVENT_SELECTION_SKIMS():
    setup()
    ROOT.FSModeTree.skimTree(FND0, NT, "", FND0_eventSelectionCuts, f"{generalCuts_eventSelection}")
    ROOT.FSModeTree.skimTree(FND45, NT, "", FND45_eventSelectionCuts, f"{generalCuts_eventSelection}")
    ROOT.FSModeTree.skimTree(FND90, NT, "", FND90_eventSelectionCuts, f"{generalCuts_eventSelection}")
    ROOT.FSModeTree.skimTree(FND135, NT, "", FND135_eventSelectionCuts, f"{generalCuts_eventSelection}")

    # merge individual polarization skims into one file for plotting.
    merged_file = FND_eventSelectionCuts_ALLpols

    cmd = [
        "hadd", "-f", merged_file,
        FND0_eventSelectionCuts,
        FND45_eventSelectionCuts,
        FND90_eventSelectionCuts,
        FND135_eventSelectionCuts,
    ]

    print("Merging event-selection skim files:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)

def skim_MONTE_CARLO_EVENT_SELECTION_SKIMS():
    setup()
    ROOT.FSModeTree.skimTree(FND_MC, NT, "", FND_eventSelectionCuts_MC, f"{generalCuts_eventSelection}")


# skim_THROWN_MC_EVENT_SELECTION_SKIMS is NOT created.
# Instead of skimming the tree here, just use the tree created below in function called 'skim_K892_genmc()' since the cuts are the same.  No need to create two separate skim files with the same cuts.  Then in the workflow (i.e. plotting scripts), just point to that location.  It will be the one file that is in a different directory than those directly above.  This is to prevent accidentally having different cuts by mistake with two different skim files, and also to save disk space.


# ---------------------------------------------------------
# GENERAL SKIMS:  These are created simply to provide smaller
# files to use in the 'SIGNAL SKIMS' section below.
# (not used for AmpTools directly, just a pre-skimming).
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# SIGNAL SKIMS (these get fed into AmpTools)
# ---------------------------------------------------------
def skim_K892_data_SIG_BKGND_SKIMS_ALL():
    setup()

    # ------------------------------------------------------------
    # pol0
    # ------------------------------------------------------------
    ROOT.FSModeTree.skimTree(FND0_generalCuts, NT, "", FND0_data,  f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND0_generalCuts, NT, "", FND0_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND0_bkgnd, NT, "", "weight", friendTreeContents)

    # ------------------------------------------------------------
    # pol45
    # ------------------------------------------------------------
    ROOT.FSModeTree.skimTree(FND45_generalCuts, NT, "", FND45_data,  f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND45_generalCuts, NT, "", FND45_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND45_bkgnd, NT, "", "weight", friendTreeContents)

    # ------------------------------------------------------------
    # pol90
    # ------------------------------------------------------------
    ROOT.FSModeTree.skimTree(FND90_generalCuts, NT, "", FND90_data,  f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND90_generalCuts, NT, "", FND90_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND90_bkgnd, NT, "", "weight", friendTreeContents)

    # ------------------------------------------------------------
    # pol135
    # ------------------------------------------------------------
    ROOT.FSModeTree.skimTree(FND135_generalCuts, NT, "", FND135_data,  f"{signalCuts}")
    ROOT.FSModeTree.skimTree(FND135_generalCuts, NT, "", FND135_bkgnd, f"{sidebandWeights}")
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights}"))]
    ROOT.FSModeTree.createFriendTree(FND135_bkgnd, NT, "", "weight", friendTreeContents)

    # ------------------------------------------------------------
    # merge signal skims
    # ------------------------------------------------------------
    if os.path.exists(FND_data_ALLpols):
        os.remove(FND_data_ALLpols)

    cmd_sig = [
        "hadd", "-f", FND_data_ALLpols,
        FND0_data,
        FND45_data,
        FND90_data,
        FND135_data,
    ]
    print("Merging signal skim files:")
    print(" ".join(cmd_sig))
    subprocess.run(cmd_sig, check=True)

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
    skim_DATA_EVENT_SELECTION_SKIMS()
    skim_MONTE_CARLO_EVENT_SELECTION_SKIMS()
    skim_K892_data_GENERAL_SKIMS()
    skim_K892_data_GENERAL_SKIMS_t13()
    skim_K892_data_GENERAL_SKIMS_t35()
    skim_K892_data_GENERAL_SKIMS_t510()
    skim_K892_data_SIG_BKGND_SKIMS_ALL()
    skim_K892_accmc()
    skim_K892_genmc()

if __name__ == "__main__":
    skim_K892()
