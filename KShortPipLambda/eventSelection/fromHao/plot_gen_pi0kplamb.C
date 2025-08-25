
TString NT("ntFSGlueX_MODECODE");
TString DEFAULT_CUTS;

void setup(){
  if (FSModeCollection::modeVector().size() != 0) return;
  FSHistogram::readHistogramCache();
  FSModeCollection::addModeInfo("100000000_100001")->addCategory("pi0kplamb");

  // FIXED CUTS
  FSCut::defineCut("t","abs(-1*MCMASS2(1,-GLUEXTARGET))<1.0");
  FSCut::defineCut("Lambda","abs(MCMASS(1) - 1.115) < 0.010");
  FSCut::defineCut("Pi0","abs(MCMASS([pi0]) - 0.135) < 0.012");
  FSCut::defineCut("KpiMass","abs(MCMASS([pi0],[K+]) - 1.2) < 0.8");
  FSCut::defineCut("Sigma1385Veto","MCMASS(1,[pi0]) > 2.0"); // 1.5 for Sigma(1350)

  // SET SOME DEFAULT SKIM CUTS
  DEFAULT_CUTS = "t,Lambda,Pi0,KpiMass,Sigma1385Veto";
}

void plot_gen_pi0kplamb(bool bggen=false){

  setup();

  // with mass constraints
  TString FND_MC = "tree_thrown*PSMCGEN.root"; 
  TString CATEGORY = "pi0kplamb";

  setup();

  // Momentum and angle distributions
  TString CUTS = "Lambda,Pi0"; //DEFAULT_CUTS;
  FSCut::defineCut("Kstar892Mass","abs(MCMASS([pi0],[K+]) - 0.892) < 0.05");
  FSCut::defineCut("t05","abs(-1*MCMASS2(1,-GLUEXTARGET))>0.3 && abs(-1*MCMASS2(1,-GLUEXTARGET))<0.5");
  CUTS += ",Kstar892Mass,t05";
  
  //DEFAULT_CUTS = "eBeam,chi2,rf,unusedE,unusedTracks,z,MM2,t,chi2rank,Lambda,Pi0,KpiMass";
  //DEFAULT_CUTS += ",Sigma1385Veto";
  //CUTS.ReplaceAll(",Sigma1385Veto","");
  
  TH2F* hProtonMomentumVsThetaMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","MCMOMENTUM(1a):acos(MCCOSINE(1a))*180/3.141","(180,0,90,100,0,1)",Form("CUT(%s)",CUTS.Data()));
  TH2F* hPiMinusMomentumVsThetaMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","MCMOMENTUM(1b):acos(MCCOSINE(1b))*180/3.141","(180,0,90,100,0,0.5)",Form("CUT(%s)",CUTS.Data()));
  //hProtonThetaMC->Scale(hProtonThetaSignal->GetMaximum()/hProtonThetaMC->GetMaximum());
  //hProtonThetaMC->SetMarkerColor(kMagenta);

  TH2F* hProtonMomentumVsPiMinusMomentumMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","MCMOMENTUM(1a):MCMOMENTUM(1b)","(100,0,0.5,100,0,1)",Form("CUT(%s)",CUTS.Data()));
  TH2F* hProtonThetaVsPiMinusThetaMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","acos(MCCOSINE(1a))*180/3.141:acos(MCCOSINE(1b))*180/3.141","(100,0,90,100,0,90)",Form("CUT(%s)",CUTS.Data()));
  
  FSHistogram::dumpHistogramCache();
  
  TCanvas* c12 = new TCanvas("c12","c12",1000,600);
  c12->Divide(3,2);
  
  c12->cd(1);
  hProtonMomentumVsThetaMC->Draw("colz");
  
  c12->cd(2);  
  hPiMinusMomentumVsThetaMC->Draw("colz");

  c12->cd(3);
  hProtonMomentumVsPiMinusMomentumMC->Draw("colz");

  c12->cd(4);
  hProtonThetaVsPiMinusThetaMC->Draw("colz");

  return;
}
