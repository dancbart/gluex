#!/usr/bin/env python3
"""
rank_kStar.py
Creates HybridChi2Rank friend trees for all input files fed into skim_kStar.py.
One-time preprocessing step. Run BEFORE skim_kStar.py.

Workflow: flatten --> rank (this script) --> skim --> AmpTools

Friend trees are written alongside the flat _sum.root files on /volatile.
No cuts are applied here; all cuts remain in cuts_kStar.py / skim_kStar.py.
"""

import sys
import os
import ROOT

ROOT.gROOT.SetBatch(True)

from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# Pull file paths and tree name from the skimming script (single source of truth)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skim_kStar import (
    NT,
    FND0, FND45, FND90, FND135,
    FND_MC_sp18, FND_MC_fa18, FND_MC_sp20,
)

# ---------------------------------------------------------------------------
# Mode registration
# ---------------------------------------------------------------------------
ROOT.FSModeCollection.addModeInfo("100000000_1100").addCategory("m100000000_1100")

CATEGORY   = "m100000000_1100"
RANK_NAME  = "HybridChi2Rank"
RANK_VAR   = "1000*Chi2"


# ---------------------------------------------------------------------------
# Data: 4 polarisations
# Grouping: (Run, Event) uniquely identify a physics event in data.
# Third variable (EnPB*100000 + RFDeltaT*100) discriminates beam bunches
# so that each RF bunch is ranked independently.
# ---------------------------------------------------------------------------
def rank_data():
    data_files = [
        ("pol0",   FND0),
        ("pol45",  FND45),
        ("pol90",  FND90),
        ("pol135", FND135),
    ]
    for pol_label, fnd in data_files:
        print(f"\n[rank_data] {pol_label}: {fnd}")
        ROOT.FSModeTree.createRankingTree(
            fnd, NT, CATEGORY,
            RANK_NAME, RANK_VAR, "",
            "Run", "Event", "EnPB*100000+RFDeltaT*100",
        )


# ---------------------------------------------------------------------------
# Accepted MC (reconstructed): 3 run periods
# Grouping: (Run, Event, MCPxP2*10000)
# A third variable is added because Run/Event may not be globally unique
# across independently generated MC batches.  MCPxP2 (thrown beam 4-momentum
# x-component) is unique per thrown event and provides that disambiguation.
# ---------------------------------------------------------------------------
def rank_accmc():
    mc_files = [
        ("sp18", FND_MC_sp18),
        ("fa18", FND_MC_fa18),
        ("sp20", FND_MC_sp20),
    ]
    for period_label, fnd in mc_files:
        print(f"\n[rank_accmc] {period_label}: {fnd}")
        ROOT.FSModeTree.createRankingTree(
            fnd, NT, CATEGORY,
            RANK_NAME, RANK_VAR, "",
            "Run", "Event", "EnPB*100000+RFDeltaT*100",
        )


# ---------------------------------------------------------------------------
# Thrown (generated) MC is NOT ranked: each thrown event has exactly one
# "combination", so there is no combinatorial ambiguity to resolve.
# ---------------------------------------------------------------------------


def rank_kStar():
    # rank_data()
    rank_accmc()


if __name__ == "__main__":
    rank_kStar()