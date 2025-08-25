TString FND0("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root");
TString FND0_MC("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__sp-fa18_B4_M16_M18_gen_amp_V2_FSflat_REACTIONFILTER-ONLY.root");
TString FND0_THROWN("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_thrown_sp-fa18_gen_amp_V2_FSflat_RXNfltrONLY.root");
TString NT("ntFSGlueX_100000000_1100");

// INDICES ASSIGNED BY 'flatten':
// 1. DecayingLambda (0)   1a. Proton (1)   1b. PiMinus2 (2)
// 2. DecayingKShort (3)   2a. PiPlus2 (4)   2b. PiMinus1 (5)
// 3. PiPlus1 (6)

// ORIGINAL SCRIPT: /work/halld/home/dbarton/gluex/forMalte/EtaPi0_FSRoot/skim.C

  // if (FSModeCollection::modeVector().size() != 0) return;
  // FSModeCollection::addModeInfo("101_1")->addCategory("m101_1");

void setup(){
  // FIXED CUTS
  FSCut::defineCut("chi2DOF", "Chi2DOF<5.0", "Chi2DOF>10.0&&Chi2DOF<15.0");
  FSCut::defineCut("unusedE", "EnUnusedSh<0.1");
  FSCut::defineCut("unusedTracks", "NumUnusedTracks<1");
  FSCut::defineCut("coherentPeak", "EnPB", "8.2", "8.8");
  FSCut::defineCut("tRange", "abs(MASS2(GLUEXTARGET,-1))<1.0");

  // CUTS WITH SIDEBANDS
  FSCut::defineCut("rf", "abs(RFDeltaT)<2.004", "abs(RFDeltaT)>6.0", 0.167);
  FSCut::defineCut("flightSigLambda", "VeeLP1>2.0");
  FSCut::defineCut("flightSigKShort", "VeeLP2>2.0");
  
  FSCut::defineCut("Lambda",
    "1.105 < MASS(1a,1b) && MASS(1a,1b) < 1.1325",
    "(1.08 < MASS(1a,1b) && MASS(1a,1b) < 1.09375) || (1.1450 < MASS(1a,1b) && MASS(1a,1b) < 1.15875)");
  
  FSCut::defineCut("KShort",
    "0.47 < MASS(2) && MASS(2) < 0.53",
    "(0.36 < MASS(2) && MASS(2) < 0.39) || (0.58 < MASS(2) && MASS(2) < 0.61)");

  FSCut::defineCut("KSTAR892",
    "0.85 < MASS(2,3) && MASS(2,3) < 0.95");

  FSCut::defineCut("KSTAR1430",
    "1.30 < MASS(2,3) && MASS(2,3) < 1.60");
}

void setupTHROWN(){
  // FIXED THROWN CUTS
  // FSCut::defineCut("coherentPeak", "EnPB", "8.2", "8.8");
  FSCut::defineCut("tRangeTHROWN", "abs(-1*MCMASS2(1,-GLUEXTARGET))<1.0");
  
  // THROWN CUTS WITH SIDEBANDS
  FSCut::defineCut("LambdaTHROWN",
    "1.105 < MCMASS(1) && MCMASS(1) < 1.1325",
    "(1.08 < MCMASS(1) && MCMASS(1) < 1.09375) || (1.1450 < MCMASS(1) && MCMASS(1) < 1.15875)");
  
  FSCut::defineCut("KShortTHROWN",
    "0.47 < MCMASS(2) && MCMASS(2) < 0.53",
    "(0.36 < MCMASS(2) && MCMASS(2) < 0.39) || (0.58 < MCMASS(2) && MCMASS(2) < 0.61)");

  FSCut::defineCut("KSTAR892THROWN",
    "0.85 < MCMASS(2,3) && MCMASS(2,3) < 0.95");

  FSCut::defineCut("KSTAR1430THROWN",
    "1.30 < MCMASS(2,3) && MCMASS(2,3) < 1.60");
}

void skim_K892_DATA(){

  setup();

    // Write out skimmed tree with GENERAL CUTS applied:
  FSModeTree::skimTree(FND0,NT,"","/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root","CUT(chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,flightSigLambda,flightSigKShort)");
  
  // Write out skimmed tree with GENERAL CUTS applied for SIGNAL REGION ONLY:
  FSModeTree::skimTree("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root",NT,"","/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892.root","CUT(rf,Lambda,KShort,KSTAR892)");

  // Write out skimmed tree with GENERAL CUTS applied with SIDEBAND WEIGHTS:
  FSModeTree::skimTree("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root",NT,"","/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root","CUTSBWT(rf,Lambda,KShort)");

  vector< pair<TString,TString> > friendTreeContents;
  friendTreeContents.push_back(pair<TString,TString>("weight","CUTSBWT(rf,Lambda,KShort)"));
  FSModeTree::createFriendTree("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root",NT,"","weight",friendTreeContents);

}

void skim_K892_MC(){

  setup();

  // Write out skimmed tree with GENERAL CUTS applied:
  FSModeTree::skimTree(FND0_MC,NT,"","/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root","CUT(chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,flightSigLambda,flightSigKShort)");
  
  // Write out skimmed tree with GENERAL CUTS applied for SIGNAL REGION ONLY:
  FSModeTree::skimTree("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root",NT,"","/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root","CUT(rf,Lambda,KShort,KSTAR892)");

  // Write out skimmed tree with GENERAL CUTS applied with SIDEBAND WEIGHTS:
  FSModeTree::skimTree("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root",NT,"","/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_MC.root","CUTSBWT(rf,Lambda,KShort)");

  vector< pair<TString,TString> > friendTreeContents;
  friendTreeContents.push_back(pair<TString,TString>("weight","CUTSBWT(rf,Lambda,KShort)"));
  FSModeTree::createFriendTree("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_MC.root",NT,"","weight",friendTreeContents);

}

void skim_K892_THROWN(){

  setupTHROWN();

  // Write out skimmed tree with GENERAL CUTS applied:
  FSModeTree::skimTree(FND0_THROWN,NT,"","/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root","CUT(tRangeTHROWN)");
  
  // Write out skimmed tree with GENERAL CUTS applied for SIGNAL REGION ONLY:
  FSModeTree::skimTree("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root",NT,"","/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_pipkslamb_SIGNAL_SKIM_K892_THROWN.root","CUT(LambdaTHROWN,KShortTHROWN,KSTAR892THROWN)");

  // Write out skimmed tree with GENERAL CUTS applied with SIDEBAND WEIGHTS:
  FSModeTree::skimTree("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root",NT,"","/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_pipkslamb_SIDEBAND_SKIM_K892_THROWN.root","CUTSBWT()");

  vector< pair<TString,TString> > friendTreeContents;
  friendTreeContents.push_back(pair<TString,TString>("weight","CUTSBWT(LambdaTHROWN,KShortTHROWN)"));
  FSModeTree::createFriendTree("/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/thrown/flatten/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_THROWN.root",NT,"","weight",friendTreeContents);

}

void skim_K892(){

  // // Skim DATA
  skim_K892_DATA();

  // // Skim MC
  skim_K892_MC();

  // Skim THROWN
  skim_K892_THROWN();

}
