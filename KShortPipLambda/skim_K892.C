// TString FND0("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root");
TString FND0("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_small.root");
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
  // MANDELSTAM t CUTS:
  // ROOT.FSCut.defineCut("tRange", f"(abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda})-0.5)<0.5)")
  FSCut::defineCut("tRange", "abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "0.1", "1.0");


  // STATIC CUTS
  FSCut::defineCut("rf", "OR(abs(RFDeltaT)<2.0)", "abs(RFDeltaT)>6.0", 0.1667);
  FSCut::defineCut("chi2DOF", "Chi2DOF", "0.0", "5.0");
  FSCut::defineCut("unusedE", "EnUnusedSh<0.1");
  FSCut::defineCut("unusedTracks", "NumUnusedTracks<1");  // No unused tracks
  FSCut::defineCut("coherentPeak", "EnPB", "8.2", "8.8");  // Coherent peak: 8.2 < E_beam < 8.8
  FSCut::defineCut("flightLengthLambda", "VeeLP1>2.0");
  FSCut::defineCut("flightLengthKShort", "VeeLP2>2.0");
  FSCut::defineCut("targetZ", "ProdVz", "52.0", "78.0");  // target z position cut

  // CUTS WITH SIDEBANDS
  FSCut::defineCut("KShort", "abs(MASS({DecayingKShort})-0.4976)<0.03", "(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0);
  FSCut::defineCut("Lambda", "abs(MASS({DecayingLambda})-1.119)<0.01375", "(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0,);
  FSCut::defineCut("selectKSTAR892", "MASS({DecayingKShort},{PiPlus1})", "0.80", "1.00");
  FSCut::defineCut("rejectSigma1385", "MASS({DecayingLambda},{PiPlus1})", "2.0", "4.0"); // remove Sigma(1385) and higher
  // ROOT.FSCut.defineCut("selectKSTAR1430", f"MASS({DecayingKShort},{PiPlus1})", "0.85", "0.95", "0.0", "0.85", "0.95", "1.0",);

}

void setupTHROWN(){
  // FIXED THROWN CUTS
  // FSCut::defineCut("coherentPeak", "EnPB", "8.2", "8.8");
  FSCut::defineCut("tRangeTHROWN", "abs(-1*MCMASS2(GLUEXTARGET,-1))", "0.1", "1.0");

  
  // THROWN CUTS WITH SIDEBANDS
  FSCut::defineCut("KShortTHROWN", "abs(MCMASS(2)-0.4976)<0.03", "(abs(MCMASS(2)-0.4976+0.0974)<0.015 || abs(MCMASS(2)-0.4976-0.1226)<0.015)", 1.0,);
  FSCut::defineCut("LambdaTHROWN", "abs(MCMASS(1)-1.119)<0.01375", "(abs(MCMASS(1)-1.119+0.032875)<0.006875 || abs(MCMASS(1)-1.119-0.032125)<0.006875)", 1.0);
  FSCut::defineCut("selectKSTAR892THROWN", "MCMASS(2,3)", "0.80", "1.00");
  // FSCut::defineCut("KSTAR1430THROWN", "1.30 < MCMASS(2,3) && MCMASS(2,3) < 1.60");
}

void skim_K892_DATA(){

  setup();

    // Write out skimmed tree with GENERAL CUTS applied:
  FSModeTree::skimTree(FND0,NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,KShort,Lambda)");
  
  // Write out skimmed tree with GENERAL CUTS applied for SIGNAL REGION ONLY:
  FSModeTree::skimTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root",NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892.root","CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)");

  // Write out skimmed tree with GENERAL CUTS applied, SIDEBAND WEIGHTS only:
  FSModeTree::skimTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892.root",NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root","CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTSBWT(rf,KShort,Lambda)");

  vector< pair<TString,TString> > friendTreeContents;
  friendTreeContents.push_back(pair<TString,TString>("weight","CUTSBWT(rf,Lambda,KShort)"));
  FSModeTree::createFriendTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892.root",NT,"","weight",friendTreeContents);

}

void skim_K892_MC(){

  setup();

  // Write out skimmed tree with GENERAL CUTS applied:
  FSModeTree::skimTree(FND0_MC,NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,KShort,Lambda)");
  
  // Write out skimmed tree with GENERAL CUTS applied for SIGNAL REGION ONLY:
  FSModeTree::skimTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root",NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root","CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)");

  // Write out skimmed tree with GENERAL CUTS applied with SIDEBAND WEIGHTS:
  FSModeTree::skimTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_GENERAL_SKIM_K892_MC.root",NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_MC.root","CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTSBWT(rf,KShort,Lambda)");

  vector< pair<TString,TString> > friendTreeContents;
  friendTreeContents.push_back(pair<TString,TString>("weight","CUTSBWT(rf,KShort,Lambda)"));
  FSModeTree::createFriendTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_MC.root",NT,"","weight",friendTreeContents);

}

void skim_K892_THROWN(){

  setupTHROWN();

  // Write out skimmed tree with GENERAL CUTS applied:
  FSModeTree::skimTree(FND0_THROWN,NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root","CUT(tRangeTHROWN)");
  
  // Write out skimmed tree with GENERAL CUTS applied for SIGNAL REGION ONLY:
  FSModeTree::skimTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root",NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_SIGNAL_SKIM_K892_THROWN.root","CUT(LambdaTHROWN,KShortTHROWN,selectKSTAR892THROWN)");

  // Write out skimmed tree with GENERAL CUTS applied with SIDEBAND WEIGHTS:
  FSModeTree::skimTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_GENERAL_SKIM_K892_THROWN.root",NT,"","/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb_SIDEBAND_SKIM_K892_THROWN.root","CUTSBWT()");

  vector< pair<TString,TString> > friendTreeContents;
  friendTreeContents.push_back(pair<TString,TString>("weight","CUTSBWT(LambdaTHROWN,KShortTHROWN)"));
  FSModeTree::createFriendTree("/work/halld/home/dbarton/gluex/KShortPipLambda/tree_pipkslamb__B4_M16_M18_SIDEBAND_SKIM_K892_THROWN.root",NT,"","weight",friendTreeContents);

}

void skim_K892(){

  // // Skim DATA
  skim_K892_DATA();

  // // Skim MC
  skim_K892_MC();

  // Skim THROWN
  skim_K892_THROWN();

}
