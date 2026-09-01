#!/usr/bin/env python3
import sys, os
import ROOT
import subprocess
ROOT.gROOT.SetBatch(True)

# Bring in FSRoot
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# path to shared libraries
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "libraries"))

NT = "ntFSGlueX_100000000_1100"

# ---------------------- inputs (DATA & MC) ---------------------
FND0   = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PARA_0_sp18fa18sp20_40856_73266.root"
FND45  = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PERP_45_sp18fa18sp20_40856_73266.root"
FND90  = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PERP_90_sp18fa18sp20_40856_73266.root"
FND135 = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_PARA_135_sp18fa18sp20_40856_73266.root"

# FND_MC_sp18 = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/phaseSpace20260630_500M_wTHROWN/root/trees/flatten/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSflat_sum_40856_42559.root"
# FND_MC_fa18 = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/trees/flatten/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSflat_sum_50685_51768.root"
# # this is ACTUALLY fall 2018 (until spring 2020 finishes generating) 7/14/2026.
# FND_MC_sp20 = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/trees/flatten/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSflat_sum_50685_51768.root"

# FND_THROWN_sp18 = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/phaseSpace20260630_500M_wTHROWN/root/thrown/flatten/tree_thrown_gen_amp_V2_FSflat_sum_40856_42559.root"
# FND_THROWN_fa18 = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/thrown/flatten/tree_thrown_gen_amp_V2_FSflat_sum_50685_51768.root"
# # this is ACTUALLY fall 2018 (until spring 2020 finishes generating) 7/14/2026.
# FND_THROWN_sp20 = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/phaseSpace20260630_500M_wTHROWN/root/thrown/flatten/tree_thrown_gen_amp_V2_FSflat_sum_50685_51768.root"

FND_MC_sp18 = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/PS08192026/root/trees/flatten/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSflat_sum.root"
FND_MC_fa18 = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/PS08192026/root/trees/flatten/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sum.root"
FND_MC_sp20 = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2020/PS08192026/root/trees/flatten/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSflat_sum.root"

FND_THROWN_sp18 = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2018/PS08192026/root/thrown/flatten/tree_thrown_gen_amp_V2_FSflat_sum.root"
FND_THROWN_fa18 = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/PS08192026/root/thrown/flatten/tree_thrown_gen_amp_V2_FSflat_FSFlat_sum.root"
FND_THROWN_sp20 = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2020/PS08192026/root/thrown/flatten/tree_thrown_gen_amp_V2_FSflat_sum.root"


# =========================================================
# OUTPUT file locations
# =========================================================
# ------ for event selection plots only, not for AmpTools. ------
baseDir_eventSelection = "/volatile/halld/home/dbarton/pipkslamb/skims/"
# ------ for AmpTools. Files needed for AmpTools go here. -------
baseDir = "/work/halld/home/dbarton/gluex/KShortPipLambda/fitSourceFiles/"


# =========================================================
# CUT DEFINITIONS
# 
# T_BIN_EVENT_SELECTION: used only in event-selection skims.
# T_BINS: used only in AmpTools skims (general, signal, accmc, genmc).
#
# T-BIN DEFINITIONS
# (label, reco_t_cut_name, thrown_t_cut_name, t_lo, t_hi)
#
# setup() and setup_genmc() loop over BOTH to define all t-range cuts,
# guaranteeing the cut expressions are identical across both workflows.
# =========================================================

from cuts_kStar import (  # noqa: I001
    ALL_T_BINS, EVENT_SELECTION_T_BINS,
    setup, setup_genmc,
    generalCuts_eventSelection, thrownCuts_eventSelection,
    KPiSystemCuts, KPiSystemCuts_weights,
    generalCuts_noT,
    signalCuts, sidebandWeights, sidebandWeights_friendTree,
    MC_signalCuts, MC_signalWeights_friendTree, MC_thrownCuts,
)

T_BINS = ALL_T_BINS
T_BIN_EVENT_SELECTION = EVENT_SELECTION_T_BINS

# =========================================================
# OUTPUT file names — EVENT SELECTION (static, not looped)
# =========================================================

# --- DATA --- #
FND0_eventSelectionCuts         = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol0.root"
FND45_eventSelectionCuts        = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol45.root"
FND90_eventSelectionCuts        = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol90.root"
FND135_eventSelectionCuts       = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_pol135.root"
FND_eventSelectionCuts_ALLpols  = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols.root"

# --- MC --- #
FND_eventSelectionCuts_MC_sp18         = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_MC_sp18.root"
FND_eventSelectionCuts_MC_fa18         = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_MC_fa18.root"
FND_eventSelectionCuts_MC_sp20         = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_MC_sp20.root"
FND_eventSelectionCuts_MC_sp18fa18sp20 = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_MC_sp18fa18sp20.root"

# --- THROWN MC --- #
FND_eventSelectionCuts_THROWN_MC_sp18         = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_THROWN_MC_sp18.root"
FND_eventSelectionCuts_THROWN_MC_fa18         = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_THROWN_MC_fa18.root"
FND_eventSelectionCuts_THROWN_MC_sp20         = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_THROWN_MC_sp20.root"
FND_eventSelectionCuts_THROWN_MC_sp18fa18sp20 = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_THROWN_MC_sp18fa18sp20.root"

# --- ROOFIT --- #
FND_eventSelectionCuts_KpiSystem_ALLpols = f"{baseDir_eventSelection}tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols_KPiSystem.root"



# =========================================================
# OUTPUT file names — AMPTOOLS GENERAL SKIMS (Static, no looping).
#
# These are intermediate files used as input to the signal/sideband
# skim loop. They can be toggled off independently without breaking
# the t-bin loop, since they contain no t information.
# 
# Data skims are separated by polarization (but not periods).  Polarization of data required for AmpTools fits.  File sizes small enough to add all periods together later in script.
# MC skims are separated by period (but not polarization).  Polarization not simulated in MC. Period separation done to avoid large file sizes.
# =========================================================

# DATA: Per-polarization general skims (no t-bin cut).
FND0_generalCuts   = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol0.root"
FND45_generalCuts  = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol45.root"
FND90_generalCuts  = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol90.root"
FND135_generalCuts = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_pol135.root"

POLS_GENERAL = [
    ("pol0",   FND0,   FND0_generalCuts),
    ("pol45",  FND45,  FND45_generalCuts),
    ("pol90",  FND90,  FND90_generalCuts),
    ("pol135", FND135, FND135_generalCuts),
]

# MONTE-CARLO: Per-period general skims (no t-bin cut).
FND_generalCuts_MC_sp18 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC_sp18.root"
FND_generalCuts_MC_fa18 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC_fa18.root"
FND_generalCuts_MC_sp20 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC_sp20.root"
FND_generalCuts_MC_sp18fa18sp20 = f"{baseDir}tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC_sp18fa18sp20.root"

MC_PERIODS_GENERAL = [
    ("sp18", FND_MC_sp18,   FND_THROWN_sp18, FND_generalCuts_MC_sp18),
    ("fa18", FND_MC_fa18,   FND_THROWN_fa18, FND_generalCuts_MC_fa18),
    ("sp20", FND_MC_sp20,   FND_THROWN_sp20, FND_generalCuts_MC_sp20),
]


# =========================================================
# actual skimming functions start here . . .
# =========================================================


# ---------------------------------------------------------
# EVENT SELECTION SKIMS.  NOT for AmpTools.
# These are just for event selection plots.
# ---------------------------------------------------------
def skim_DATA_EVENT_SELECTION_SKIMS():
    setup(T_BINS, T_BIN_EVENT_SELECTION)
    ROOT.FSModeTree.skimTree(FND0,   NT, "", FND0_eventSelectionCuts,   generalCuts_eventSelection)
    ROOT.FSModeTree.skimTree(FND45,  NT, "", FND45_eventSelectionCuts,  generalCuts_eventSelection)
    ROOT.FSModeTree.skimTree(FND90,  NT, "", FND90_eventSelectionCuts,  generalCuts_eventSelection)
    ROOT.FSModeTree.skimTree(FND135, NT, "", FND135_eventSelectionCuts, generalCuts_eventSelection)

    cmd = ["hadd", "-f", FND_eventSelectionCuts_ALLpols,
           FND0_eventSelectionCuts, FND45_eventSelectionCuts,
           FND90_eventSelectionCuts, FND135_eventSelectionCuts]
    print("Merging event-selection skim files:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def skim_MONTE_CARLO_EVENT_SELECTION_SKIMS():
    setup(T_BINS, T_BIN_EVENT_SELECTION)
    ROOT.FSModeTree.skimTree(FND_MC_sp18, NT, "", FND_eventSelectionCuts_MC_sp18, generalCuts_eventSelection)
    ROOT.FSModeTree.skimTree(FND_MC_fa18, NT, "", FND_eventSelectionCuts_MC_fa18, generalCuts_eventSelection)
    ROOT.FSModeTree.skimTree(FND_MC_sp20, NT, "", FND_eventSelectionCuts_MC_sp20, generalCuts_eventSelection)

    cmd = ["hadd", "-f", FND_eventSelectionCuts_MC_sp18fa18sp20,
           FND_eventSelectionCuts_MC_sp18, FND_eventSelectionCuts_MC_fa18,
           FND_eventSelectionCuts_MC_sp20]
    print("Merging MC event-selection skim files:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def skim_THROWN_MC_EVENT_SELECTION_SKIMS():
    setup_genmc(T_BINS, T_BIN_EVENT_SELECTION)
    ROOT.FSModeTree.skimTree(FND_THROWN_sp18, NT, "", FND_eventSelectionCuts_THROWN_MC_sp18, thrownCuts_eventSelection)
    ROOT.FSModeTree.skimTree(FND_THROWN_fa18, NT, "", FND_eventSelectionCuts_THROWN_MC_fa18, thrownCuts_eventSelection)
    ROOT.FSModeTree.skimTree(FND_THROWN_sp20, NT, "", FND_eventSelectionCuts_THROWN_MC_sp20, thrownCuts_eventSelection)

    cmd = ["hadd", "-f", FND_eventSelectionCuts_THROWN_MC_sp18fa18sp20,
           FND_eventSelectionCuts_THROWN_MC_sp18, FND_eventSelectionCuts_THROWN_MC_fa18,
           FND_eventSelectionCuts_THROWN_MC_sp20]
    print("Merging THROWN event-selection skim files:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def skim_DATA_KPI_SYSTEM_SKIMS():
    setup(T_BINS, T_BIN_EVENT_SELECTION)
    ROOT.FSModeTree.skimTree(FND_eventSelectionCuts_ALLpols, NT, "",
                             FND_eventSelectionCuts_KpiSystem_ALLpols, KPiSystemCuts)
    friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(KPiSystemCuts_weights))]
    ROOT.FSModeTree.createFriendTree(FND_eventSelectionCuts_KpiSystem_ALLpols, NT, "", "weight", friendTreeContents)


# ---------------------------------------------------------
# AMPTOOLS GENERAL SKIMS (toggleable, no t-bin cut)
# One output file per polarization / MC period.
# Safe to comment out — downstream signal/sideband loop
# applies t-bin cuts, so these files cannot go stale.
# ---------------------------------------------------------

def skim_K892_data_GENERAL_SKIMS():
    setup(T_BINS, T_BIN_EVENT_SELECTION)
    for (pol_label, fnd_raw, general_out) in POLS_GENERAL:
        print(f"General-skimming data {pol_label}: {fnd_raw} --> {general_out}")
        ROOT.FSModeTree.skimTree(fnd_raw, NT, "", general_out, generalCuts_noT)


def skim_K892_accmc_GENERAL_SKIMS():
    """
    General-skim each MC period (no t-bin cut), then hadd into one
    combined file. The signal skim loop reads from the combined file.
    """
    setup(T_BINS, T_BIN_EVENT_SELECTION)
    period_files = []
    for (period_label, fnd_mc, _, general_out) in MC_PERIODS_GENERAL:
        print(f"General-skimming accmc {period_label}: {fnd_mc} --> {general_out}")
        ROOT.FSModeTree.skimTree(fnd_mc, NT, "", general_out, generalCuts_noT)
        period_files.append(general_out)

    cmd = ["hadd", "-f", FND_generalCuts_MC_sp18fa18sp20] + period_files
    print("Merging accmc general-skim files:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


# ---------------------------------------------------------
# AMPTOOLS SIGNAL / SIDEBAND SKIMS — loop over T_BINS
#
# Reads from the general-skim files (no t-bin cut).
# Applies t-bin cut + signal/sideband cuts per bin.
#
# signal:   CUT(tRange*, rf, KShort, Lambda)
# sideband: CUT(tRange*)*CUTSBWT(rf, KShort, Lambda)
#           with createFriendTree for the weight column.
# ---------------------------------------------------------

def skim_K892_data_SIG_BKGND_SKIMS():
    setup(T_BINS, T_BIN_EVENT_SELECTION)
    for (label, t_cut_name, _, lo, hi) in T_BINS:
        signalCuts_t      = signalCuts.format(t_cut_name=t_cut_name)
        sidebandWeights_t = sidebandWeights.format(t_cut_name=t_cut_name)

        signal_files = []
        for (pol_label, _, general_out) in POLS_GENERAL:
            signal_out = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_{label}_{pol_label}.root"
            bkgnd_out  = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_{label}_{pol_label}.root"

            ROOT.FSModeTree.skimTree(general_out, NT, "", signal_out, f"{signalCuts_t}")
            ROOT.FSModeTree.skimTree(general_out, NT, "", bkgnd_out,  f"{sidebandWeights_t}")
            friendTreeContents = [(ROOT.TString("weight"), ROOT.TString(f"{sidebandWeights_friendTree}"))]
            ROOT.FSModeTree.createFriendTree(bkgnd_out, NT, "", "weight", friendTreeContents)

            signal_files.append(signal_out)

        allpols_out = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_{label}_ALLpols.root"
        if os.path.exists(allpols_out):
            os.remove(allpols_out)
        cmd = ["hadd", "-f", allpols_out] + signal_files
        print(f"Merging signal skims for {label}:")
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)


# ---------------------------------------------------------
# AMPTOOLS MC SKIMS — loop over T_BINS
# Reads from general-skim files (accmc) or raw thrown files (genmc).
# ---------------------------------------------------------

def skim_K892_accmc():
    """
    For each t-bin: signal skim + friend-tree weight from the
    combined general-skim file (no t-bin cut).
    """
    setup(T_BINS, T_BIN_EVENT_SELECTION)
    for (label, t_cut_name, _, lo, hi) in T_BINS:
        MC_signalCuts_t = f"{MC_signalCuts.format(t_cut_name=t_cut_name)}"

        accmc_out = f"{baseDir}tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC_{label}.root"
        ROOT.FSModeTree.skimTree(FND_generalCuts_MC_sp18fa18sp20, NT, "", accmc_out, MC_signalCuts_t)
        friendTreeContentsMC = [(ROOT.TString("weight"), ROOT.TString(MC_signalWeights_friendTree))]
        ROOT.FSModeTree.createFriendTree(accmc_out, NT, "", "weight", friendTreeContentsMC)


def skim_K892_genmc():
    """
    For each t-bin: skim each thrown period, then hadd into one
    genmc file per bin. Thrown trees are small enough to skim
    directly without a general-skim step.
    """
    setup_genmc(T_BINS, T_BIN_EVENT_SELECTION)
    for (label, _, thrown_t_cut_name, lo, hi) in T_BINS:
        MC_thrownCuts_t = f"{MC_thrownCuts.format(thrown_t_cut_name=thrown_t_cut_name)}"

        period_files = []
        for (period_label, _, fnd_thrown, _) in MC_PERIODS_GENERAL:
            thrown_out = f"{baseDir}tree_pipkslamb_THROWN_SKIM_K892_{label}_{period_label}.root"
            print(f"Skimming genmc [{label}] {period_label}: {fnd_thrown} --> {thrown_out}")
            ROOT.FSModeTree.skimTree(fnd_thrown, NT, "", thrown_out, MC_thrownCuts_t)
            period_files.append(thrown_out)

        genmc_out = f"{baseDir}tree_pipkslamb_SIGNAL_SKIM_K892_THROWN_{label}_sp18fa18sp20.root"
        cmd = ["hadd", "-f", genmc_out] + period_files
        print(f"Merging genmc skims for {label}:")
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)


def skim_K892():
    # skim_DATA_EVENT_SELECTION_SKIMS()
    # skim_MONTE_CARLO_EVENT_SELECTION_SKIMS()
    # skim_THROWN_MC_EVENT_SELECTION_SKIMS()
    # skim_DATA_KPI_SYSTEM_SKIMS()
    # skim_K892_data_GENERAL_SKIMS()
    skim_K892_accmc_GENERAL_SKIMS()
    # skim_K892_data_SIG_BKGND_SKIMS()
    skim_K892_accmc()
    skim_K892_genmc()

if __name__ == "__main__":
    skim_K892()