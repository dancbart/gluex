#!/usr/bin/env python3
"""
cuts_kStar.py
------------
Shared cut definitions for the KShort-Pip-Lambda / K*(892) analysis.

Import this module in any script that needs FSRoot cut definitions or
cut strings — skimming scripts, plotting scripts, etc. — to guarantee
identical cuts are applied everywhere.

Usage:
    from pyamptools import atiSetup
    atiSetup.setup(globals(), use_fsroot=True)   # must come first

    from cuts_K892 import (
        ALL_T_BINS, EVENT_SELECTION_T_BINS,
        setup, setup_genmc,
        generalCuts_eventSelection, ...
    )

    T_BINS = ALL_T_BINS          # or a subset
    T_BIN_EVENT_SELECTION = EVENT_SELECTION_T_BINS

    setup(T_BINS, T_BIN_EVENT_SELECTION)
    setup_genmc(T_BINS, T_BIN_EVENT_SELECTION)
"""

import ROOT


# =========================================================
# PARTICLE DEFINITIONS
# (from 'flatten' for FSRoot)
# =========================================================
DecayingLambda = "1"
Proton         = "1a"
PiMinus2       = "1b"
DecayingKShort = "2"
PiPlus2        = "2a"
PiMinus1       = "2b"
PiPlus1        = "3"


# =========================================================
# MASTER T-BIN LISTS
# (label, reco_t_cut_name, thrown_t_cut_name, t_lo, t_hi)
#
# Scripts import these and assign to their own T_BINS /
# T_BIN_EVENT_SELECTION — using all bins, a subset, or a
# custom list — then pass them into setup() / setup_genmc().
#
# The cut *expressions* are always generated from the bins
# the calling script provides, so they are guaranteed correct
# regardless of which bins are selected.
# =========================================================

EVENT_SELECTION_T_BINS = ("tEvSel", "tRange_evSel", "tRangeTHROWN_evSel", 0.1, 2.0)

ALL_T_BINS = [
    ("t0120", "tRange0120", "tRangeTHROWN0120", 0.1, 2.0),
    ("t0103", "tRange0103", "tRangeTHROWN0103", 0.1, 0.3),
    ("t0305", "tRange0305", "tRangeTHROWN0305", 0.3, 0.5),
    ("t0507", "tRange0507", "tRangeTHROWN0507", 0.5, 0.7),
    ("t0710", "tRange0710", "tRangeTHROWN0710", 0.7, 1.0),
    ("t1013", "tRange1013", "tRangeTHROWN1013", 1.0, 1.3),
    ("t1316", "tRange1316", "tRangeTHROWN1316", 1.3, 1.6),
    ("t1620", "tRange1620", "tRangeTHROWN1620", 1.6, 2.0),
]


# =========================================================
# CUT DEFINITIONS
# Call setup() for reconstructed data/MC scripts.
# Call setup_genmc() for thrown-MC scripts.
# Both must be called AFTER atiSetup.setup(globals(), use_fsroot=True).
# =========================================================

def setup(t_bins, t_bin_event_selection):
    """Define all FSRoot cuts for reconstructed data and MC.

    Args:
        t_bins: list of (label, t_cut_name, thrown_t_cut_name, lo, hi)
        t_bin_event_selection: single tuple of the same format for the
                               event-selection t-range cut
    """
    # Guard: skip if cuts are already registered (e.g. setup() called twice)
    if ROOT.FSModeCollection.modeVector().size() != 0:
        return

    ROOT.FSModeCollection.addModeInfo("100000000_1100").addCategory("m100000000_1100")

    # --- t-prime cuts (KShort) ---
    ROOT.FSCut.defineCut("tprimeKsLow",  "TPRIMEKS > 0.0 && TPRIMEKS < 0.2")
    ROOT.FSCut.defineCut("tprimeKsMid",  "TPRIMEKS > 0.2 && TPRIMEKS < 0.6")
    ROOT.FSCut.defineCut("tprimeKsHigh", "TPRIMEKS > 0.6 && TPRIMEKS < 1.0")

    # --- t-range cuts: generated from t_bins + t_bin_event_selection ---
    for (label, t_cut_name, _, lo, hi) in t_bins + [t_bin_event_selection]:
        ROOT.FSCut.defineCut(t_cut_name,
            f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>{lo} && "
            f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<{hi}")

    # --- all other cuts ---
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
    ROOT.FSCut.defineCut("KShort",
        f"abs(MASS({DecayingKShort})-0.4976)<0.03",
        f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)",
        1.0)
    ROOT.FSCut.defineCut("Lambda",
        f"abs(MASS({DecayingLambda})-1.119)<0.01375",
        f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)",
        1.0)
    ROOT.FSCut.defineCut("selectKSTAR892",
        f"MASS({DecayingKShort},{PiPlus1})>0.80 && MASS({DecayingKShort},{PiPlus1})<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385",
        f"MASS({DecayingLambda},{PiPlus1})>2.00 && MASS({DecayingLambda},{PiPlus1})<4.0")
    # Outside Lambda window — used to check for non-Lambda K*'s and understand K* background
    ROOT.FSCut.defineCut("nonLambda", "MASS(1a,1b)>1.14 && MASS(1a,1b)<1.675")


def setup_genmc(t_bins, t_bin_event_selection):
    """Define all FSRoot cuts for thrown MC trees.

    Args:
        t_bins: list of (label, t_cut_name, thrown_t_cut_name, lo, hi)
        t_bin_event_selection: single tuple of the same format for the
                               event-selection t-range cut
    """
    # --- t-range cuts: generated from t_bins + t_bin_event_selection ---
    for (label, _, thrown_t_cut_name, lo, hi) in t_bins + [t_bin_event_selection]:
        ROOT.FSCut.defineCut(thrown_t_cut_name,
            f"abs(-1*MCMASS2(GLUEXTARGET,-1))>{lo} && "
            f"abs(-1*MCMASS2(GLUEXTARGET,-1))<{hi}")

    # --- all other cuts ---
    ROOT.FSCut.defineCut("KShortTHROWN",
        "abs(MCMASS(2)-0.4976)<0.03",
        "(abs(MCMASS(2)-0.4976+0.0974)<0.015 || abs(MCMASS(2)-0.4976-0.1226)<0.015)",
        1.0)
    ROOT.FSCut.defineCut("LambdaTHROWN",
        "abs(MCMASS(1)-1.119)<0.01375",
        "(abs(MCMASS(1)-1.119+0.032875)<0.006875 || abs(MCMASS(1)-1.119-0.032125)<0.006875)",
        1.0)
    ROOT.FSCut.defineCut("coherentPeakTHROWN", "MCEnPB>8.2 && MCEnPB<8.6")
    ROOT.FSCut.defineCut("selectKSTAR892THROWN", "MCMASS(2,3)>0.80 && MCMASS(2,3)<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385THROWN", "MCMASS(1,3)>2.00 && MCMASS(1,3)<4.0")


# =========================================================
# CUT STRINGS
#
# Static cut strings are defined here. t-dependent cut strings
# are built dynamically inside loops using .format(t_cut_name=...).
#
# Context: FSRoot expects strings passed to macros like "CUT()".
# FSRoot-->ROOT-->Python: FSRoot lives inside ROOT, ROOT inside
# Python. Cut strings defined once here ensure identical cuts
# are applied across all scripts that import this module.
#
# Note: generalCuts_eventSelection and thrownCuts_eventSelection
# reference EVENT_SELECTION_T_BINS. If your script uses a
# custom t_bin_event_selection, build these strings locally using
# your tuple's [1] and [2] elements.
# =========================================================

# ------ USE FOR EVENT SELECTION PLOTS ONLY ------- #
generalCuts_eventSelection = f"CUT({EVENT_SELECTION_T_BINS[1]},chi2DOF,unusedTracks,coherentPeak,targetZ)"
thrownCuts_eventSelection  = f"CUT({EVENT_SELECTION_T_BINS[2]},coherentPeakTHROWN,selectKSTAR892THROWN)"

# ---------- USE FOR ROOFIT FITTING ONLY ---------- #
KPiSystemCuts         = f"CUT({EVENT_SELECTION_T_BINS[1]},chi2DOF,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
KPiSystemCuts_weights = "CUTWT(rf,KShort,Lambda)"

# ----------- USE FOR AMPTOOLS FITTING ------------ #

# General skim: no t-bin cut. One file per polarization / MC period.
# These are intermediate files to speed up iteration on signal cuts.
# Toggle off skim_K892_data_GENERAL_SKIMS() and skim_K892_accmc_GENERAL_SKIMS()
# safely — t-bin cuts are applied downstream in the signal/sideband loop.
generalCuts_noT = ("CUT(chi2DOF,unusedTracks,coherentPeak,targetZ,"
                   "flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)")

# Signal / sideband skims: t-bin cut strings built dynamically per bin inside loops.
# Usage:  signalCuts_t = signalCuts.format(t_cut_name=t_cut_name)
signalCuts                 = "CUT({t_cut_name},rf,KShort,Lambda)"
sidebandWeights            = "CUT({t_cut_name})*CUTSBWT(rf,KShort,Lambda)"
sidebandWeights_friendTree = "CUTSBWT(rf,KShort,Lambda)"  # no t_cut_name needed here

# MC signal skim (no RF cut for MC).
# Usage:  MC_signalCuts_t = MC_signalCuts.format(t_cut_name=t_cut_name)
MC_signalCuts               = "CUT({t_cut_name},KShort,Lambda)"
# MC background skim not used — MC sideband weights applied to signal file via friend tree instead.
MC_signalWeights_friendTree = "CUTWT(KShort,Lambda)"  # no t_cut_name needed here

# MC thrown skim (no RF cut, no signal-cleaning cuts — preserves full phase space for acceptance corrections).
# Usage:  MC_thrownCuts_t = MC_thrownCuts.format(thrown_t_cut_name=thrown_t_cut_name)
MC_thrownCuts = "CUT({thrown_t_cut_name},coherentPeakTHROWN,selectKSTAR892THROWN)"

# ----------- USE FOR EVENT SELECTION PLOTS ------------ #
# Like signalCuts / MC_signalCuts but with selectKSTAR892 included,
# since event-selection skims are not pre-filtered by the general skim's selectKSTAR892 cut.
# t-bin cut built dynamically: signalCuts_eventSelection.format(t_cut_name=t_cut_name)
signalCuts_eventSelection    = "CUT({t_cut_name},rf,KShort,Lambda,selectKSTAR892)"
MC_signalCuts_eventSelection = "CUT({t_cut_name},KShort,Lambda,selectKSTAR892)"

# ----------- FOR CUT-COMPARISON PLOTS ------------ #
signalCuts_weights = "CUTWT(rf,KShort,Lambda)"
baseCuts           = "flightLengthKShort,flightLengthLambda,rejectSigma1385"
sidebandCuts       = "rf,KShort,Lambda"

# Explanation of cut methods (Boris):

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