
TString NT("ntFSGlueX_MODECODE");
TString DEFAULT_CUTS;

void setup(){
  if (FSModeCollection::modeVector().size() != 0) return;
  FSHistogram::readHistogramCache();
  FSModeCollection::addModeInfo("100000000_100001")->addCategory("pi0kplamb");

  // FIXED CUTS
  FSCut::defineCut("unusedE","EnUnusedSh<0.1");
  FSCut::defineCut("unusedTracks","NumUnusedTracks<1");
  FSCut::defineCut("z","ProdVz>=51.2&&ProdVz<=78.8");
  FSCut::defineCut("MM2","abs(RMASS2(GLUEXTARGET,B,-1,-2,-3))<0.05");
  FSCut::defineCut("eBeam","(EnPB>8.2&&EnPB<8.8)");
  FSCut::defineCut("chi2","Chi2DOF<5");
    
  FSCut::defineCut("t","abs(-1*MASS2(1,-GLUEXTARGET))<1.0");
  FSCut::defineCut("Lambda","abs(MASS(1) - 1.115) < 0.010");
  FSCut::defineCut("LambdaSB","abs(MASS(1) - 1.090) < 0.010 || abs(MASS(1) - 1.140) < 0.010");
  FSCut::defineCut("Pi0","abs(MASS([pi0]) - 0.135) < 0.012");
  FSCut::defineCut("Pi0SB","abs(MASS([pi0]) - 0.102) < 0.012 || abs(MASS([pi0]) - 0.168) < 0.012");
  FSCut::defineCut("rf","abs(RFDeltaT) < 2.004");
  FSCut::defineCut("rfSB","abs(RFDeltaT) > 2.004 && abs(RFDeltaT) < 18.036");
  FSCut::defineCut("KpiMass","abs(MASS([pi0],[K+]) - 1.2) < 0.8");

  FSCut::defineCut("Lambda2DSB","abs(MASS(1) - 1.115) < 0.010","abs(MASS(1) - 1.115) > 0.015 && abs(MASS(1) - 1.115) < 0.035",0.5);
  FSCut::defineCut("Pi02DSB","abs(MASS([pi0]) - 0.135) < 0.0125","abs(MASS([pi0]) - 0.135) > 0.02 && abs(MASS([pi0]) - 0.135) < 0.045",0.5);
  FSCut::defineCut("rf2DSB","abs(RFDeltaT)<2.004","abs(RFDeltaT) > 2.004 && abs(RFDeltaT) < 18.036",0.125);

  FSCut::defineCut("Sigma1385Veto","MASS(1,[pi0]) > 2.0"); // 1.5 for Sigma(1350)

  // SET SOME DEFAULT SKIM CUTS
  DEFAULT_CUTS = "eBeam,chi2,unusedE,unusedTracks,z,MM2,t,Lambda,Pi0,rf,KpiMass";
  //DEFAULT_CUTS += ",Sigma1385Veto";
}

void plot_hybrid(bool bggen=false){

	//gStyle->SetCanvasPreferGL();
  gStyle->SetPadBottomMargin(0.22);
  gStyle->SetPadLeftMargin(0.25);
  gStyle->SetPadTopMargin(0.1);
  gStyle->SetPadRightMargin(0.15);

  setup();

  // with mass constraints
  TString FND_DATA = "tree_pi0kplamb__B4_M7_M18_Hybrid_SKIM*.root";
  TString FND_BGGEN = "tree_pi0kplamb__B4_M7_M18_BGGEN_Hybrid_SKIM*.root";
  TString FND_MC = "tree_pi0kplamb__B4_M7_M18_PSMC_Hybrid_SKIM*.root"; 
  TString CATEGORY = "pi0kplamb";

  setup();
    
  system("mkdir -p plots");

  TCanvas* cb = new TCanvas("cb","cb",1000,600);
  cb->Divide(3,2);

  TString CUTS;
  TCanvas* c1 = new TCanvas("c1","c1",1000,600);
  c1->Divide(3,2);
  c1->cd(1);
  CUTS = DEFAULT_CUTS;
  TH1F* hRFDeltaTSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","RFDeltaT","(100,-25,25)",Form("CUT(%s)",CUTS.Data()));
  hRFDeltaTSignal->SetXTitle("#Delta T [ns]");
  hRFDeltaTSignal->SetYTitle("Events");
  hRFDeltaTSignal->Draw();
  TH1F* hRFDeltaTMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","RFDeltaT","(100,-25,25)",Form("CUT(%s)",CUTS.Data()));
  hRFDeltaTMC->Scale(hRFDeltaTSignal->GetMaximum()/hRFDeltaTMC->GetMaximum());
  hRFDeltaTMC->SetMarkerColor(kMagenta);
  //hRFDeltaTMC->Draw("same");

  CUTS.ReplaceAll(",rf",",rfSB");
  TH1F* hRFDeltaTSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","RFDeltaT","(100,-25,25)",Form("CUT(%s)",CUTS.Data()));
  hRFDeltaTSB->SetFillColor(kBlue);
  hRFDeltaTSB->Draw("h same");
    
  // protonpi mass
  CUTS = DEFAULT_CUTS;
  CUTS.ReplaceAll(",Lambda","");
  TH1F* hMpimpRFSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
  
  CUTS.ReplaceAll(",rf",",rfSB");
  TH1F* hMpimpRFSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
  CUTS.ReplaceAll(",rfSB","");
  TH1F* hMpimpRFSub = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)*CUTWT(rf2DSB)",CUTS.Data()));

  TH1F *hMpimpRFDiff = (TH1F*)hMpimpRFSignal->Clone("hMpimpRFDiff"); hMpimpRFDiff->Add(hMpimpRFSB, -0.125);
  hMpimpRFDiff->SetFillColor(kBlue);

  c1->cd(2);
  hMpimpRFSignal->Draw();
  hMpimpRFSB->Draw("same");

  c1->cd(3);
  hMpimpRFSub->Draw();
  hMpimpRFDiff->Draw("h same");

  c1->cd(4);
 
  
  CUTS = DEFAULT_CUTS;
  CUTS.ReplaceAll(",rf","");
  TH1F* hMpimpSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
  TH1F* hMpimpMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
  hMpimpMC->Scale(hMpimpSignal->GetMaximum()/hMpimpMC->GetMaximum());
  hMpimpMC->SetMarkerColor(kMagenta);
  
  CUTS.ReplaceAll(",Lambda",",LambdaSB");
  TH1F* hMpimpSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
  hMpimpSB->SetFillColor(kBlue);
  
  CUTS.ReplaceAll(",LambdaSB","");
  TH1F* hMpimp = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
  
  if(bggen) {
	  cb->cd(2);    
	  TH1F* hMpimp_BGGEN = FSModeHistogram::getTH1F(FND_BGGEN,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
	  hMpimp_BGGEN->SetXTitle("Mass(p#pi^{-}) [GeV]");
	  hMpimp_BGGEN->SetYTitle("Events");
	  hMpimp_BGGEN->Draw();
	  FSModeHistogram::drawMCComponentsSame(FND_BGGEN,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)",CUTS.Data()));
  }
  
  // gg mass
  CUTS = DEFAULT_CUTS;
  TH1F* hMggSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)",CUTS.Data()));
  TH1F* hMggMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)",CUTS.Data()));
  hMggMC->Scale(hMggSignal->GetMaximum()/hMggMC->GetMaximum());
  hMggMC->SetMarkerColor(kMagenta);
  
  CUTS.ReplaceAll(",Pi0",",Pi0SB");
  TH1F* hMggSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)",CUTS.Data()));
  hMggSB->SetFillColor(kBlue);
  
  CUTS.ReplaceAll(",Pi0SB","");
  TH1F* hMgg = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)",CUTS.Data()));
  
  if(bggen) {
	  cb->cd(3);    
	  TH1F* hMgg_BGGEN = FSModeHistogram::getTH1F(FND_BGGEN,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)",CUTS.Data()));
	  hMgg_BGGEN->SetXTitle("Mass(#gamma#gamma) [GeV]");
	  hMgg_BGGEN->SetYTitle("Events");
	  hMgg_BGGEN->Draw();
	  FSModeHistogram::drawMCComponentsSame(FND_BGGEN,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)",CUTS.Data()));
  }

#if 0
  // Lambda pi0 mass
  CUTS = DEFAULT_CUTS;
  CUTS.ReplaceAll(",Sigma1385Veto","");
  TH1F* hMpiLambdaSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1,[pi0])","(100,1.2,2.2)",Form("CUT(%s)",CUTS.Data()));
  TH1F* hMpiLambdaMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS(1,[pi0])","(100,1.2,2.2)",Form("CUT(%s)",CUTS.Data()));
  hMpiLambdaMC->Scale(hMpiLambdaSignal->GetMaximum()/hMpiLambdaMC->GetMaximum());
  hMpiLambdaMC->SetMarkerColor(kMagenta);
  
  CUTS.ReplaceAll(",Lambda",",LambdaSB");
  TH1F* hMpiLambdaSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1,[pi0])","(100,1.2,2.2)",Form("CUT(%s)",CUTS.Data()));
  hMpiLambdaSB->SetFillColor(kBlue);
  
  // 2D sideband
  CUTS = DEFAULT_CUTS;
  CUTS.ReplaceAll(",Pi0","");
  CUTS.ReplaceAll(",Lambda","");
  TH2F* hMgg_pimp = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","MASS(1):MASS([pi0])","(100,0.09,0.18,100,1.08,1.18)",Form("CUT(%s)*CUTWT(Lambda2DSB,Pi02DSB)",CUTS.Data()));
  
  // Kpi mass
  CUTS = DEFAULT_CUTS;
  TH1F* hMkppi0 = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)",CUTS.Data()));
  TH1F* hMkppi0MC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)",CUTS.Data()));
  hMkppi0MC->Scale(hMkppi0->GetMaximum()/hMkppi0MC->GetMaximum());
  hMkppi0MC->SetMarkerColor(kMagenta);
  
  if(bggen) {
	  cb->cd(4);    
	  TH1F* hMkppi0_BGGEN = FSModeHistogram::getTH1F(FND_BGGEN,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)",CUTS.Data()));
	  hMkppi0_BGGEN->SetXTitle("Mass(K^{+}#pi^{0}) [GeV]");
	  hMkppi0_BGGEN->SetYTitle("Events");
	  hMkppi0_BGGEN->Draw();
	  FSModeHistogram::drawMCComponentsSame(FND_BGGEN,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)",CUTS.Data()));
  }
  
  CUTS = DEFAULT_CUTS;
  CUTS.ReplaceAll(",Lambda",",LambdaSB");
  TH1F* hMkppi0SB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)",CUTS.Data()));
  hMkppi0SB->SetFillColor(kBlue);
  
  CUTS = DEFAULT_CUTS;
  CUTS.ReplaceAll(",Pi0","");
  CUTS.ReplaceAll(",Lambda","");
  TH1F* hMkppi02DSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)*CUTWT(Lambda2DSB,Pi02DSB,rf2DSB)",CUTS.Data()));
  hMkppi02DSB->SetMarkerColor(kRed);
  
  // mass correlations
  CUTS = DEFAULT_CUTS;
  CUTS.ReplaceAll(",Sigma1385Veto","");
  TH2F* hMkppi_piLambda = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","MASS(1,[pi0]):MASS([K+],[pi0])","(100,0.5,2.0,100,1.0,3.0)",Form("CUT(%s)",CUTS.Data()));
  
  //TH1F* hGJCosTheta = FSHistogram::getTH1F(FND_DATA,"ntFSGlueX_100000000_100001","GJCOSTHETA(2;3;1;B)","(50,-1.,1.)",""); //,Form("CUT(%s)",CUTS.Data()));
  //TH2F* hMkppi0VsGJCosTheta = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","HELCOSTHETA(2;3;1;B):MASS(2,3)","(100,0.5,2.0,50,-1.,1.)",Form("CUT(%s)",CUTS.Data()));
#endif
  
  FSHistogram::dumpHistogramCache();
  
  if(bggen) cb->Print("plots/pi0kplamb_bggen_hybrid.pdf");
  
  hMpimp->SetTitle("; Mass(p#pi^{-}) [GeV]; Counts");
  hMpimp->GetXaxis()->SetNdivisions(5);
  hMpimp->GetYaxis()->SetNdivisions(5);
  hMpimp->GetXaxis()->CenterTitle(true);
  hMpimp->GetYaxis()->CenterTitle(true);
  hMpimp->SetLabelSize(0.07,"xyz");
  hMpimp->SetTitleSize(0.07,"xyz");

#if 0
  hMkppi0->SetTitle("; Mass(K^{+}#pi^{0}) [GeV]; Counts");
  hMkppi0->Add(hMkppi0SB, -0.5);
  hMkppi0->GetXaxis()->SetNdivisions(5);
  hMkppi0->GetYaxis()->SetNdivisions(5);
  hMkppi0->GetXaxis()->CenterTitle(true);
  hMkppi0->GetYaxis()->CenterTitle(true);
  hMkppi0->SetLabelSize(0.07,"xyz");
  hMkppi0->SetTitleSize(0.07,"xyz");
  
  hMpiLambdaSignal->SetTitle("; Mass(#Lambda#pi^{0}) [GeV]; Counts");
  hMpiLambdaSignal->GetXaxis()->SetNdivisions(5);
  hMpiLambdaSignal->GetYaxis()->SetNdivisions(5);
  hMpiLambdaSignal->GetXaxis()->CenterTitle(true);
  hMpiLambdaSignal->GetYaxis()->CenterTitle(true);
  hMpiLambdaSignal->SetLabelSize(0.07,"xyz");
  hMpiLambdaSignal->SetTitleSize(0.07,"xyz");
#endif
  
  TLegend *leg = new TLegend(0.6,0.6,0.85,0.88);
  leg->AddEntry(hMpimp,"Data","pe");
  leg->AddEntry(hMpimpSB,"Sideband","f");
  leg->AddEntry(hMpimpMC,"PS MC","pe");
  
  TCanvas* c11 = new TCanvas("c11","c11",1000,600);
  c11->Divide(3,2);
  c11->cd(1);
  hMpimp->SetMaximum(hMpimp->GetMaximum()*1.1);
  hMpimp->Draw();
  //hMpimpMC->Draw("same");
  //hMpimpSignal->Draw("same");
  hMpimpSB->Draw("h same");
  leg->Draw("same");
  
  c11->cd(2);
  hMgg->Draw();
  //hMggMC->Draw("same");
  //hMggSignal->Draw("same");
  //hMggSB->Draw("same");

#if 0
  c11->cd(3);
  hMkppi0->SetMinimum(0);
  hMkppi0->Draw();
  hMkppi0MC->Draw("same");
  hMkppi0SB->Scale(0.5);
  hMkppi0SB->Draw("h same");
  //hMkppi02DSB->Draw("same");
  
  c11->cd(4);
  hMpiLambdaSignal->Draw("same");
  hMpiLambdaMC->Draw("same");
  hMpiLambdaSB->Scale(0.5);
  hMpiLambdaSB->Draw("h same");
  
  c11->cd(5);
  hMgg_pimp->Draw("colz");
  
  c11->cd(6);
  hMkppi_piLambda->Draw("colz");

  TCanvas *c22 = new TCanvas("c22","c22",1000,600);
  c22->Divide(3,2);
  c22->cd(1);
  hMpimp->Draw();
  //hMpimpMC->Draw("same");
  hMpimpSignal->Draw("same");
  hMpimpSB->SetFillColorAlpha(kBlue, 0.2);
  //hMpimpSB->Scale(1e6);
  hMpimpSB->Draw("h same");
  hMpimp->Draw("same");
  leg->Draw("same");
  
  c22->cd(2);
  hMgg->SetTitle("; Mass(#gamma#gamma) [GeV]; Counts");
  hMgg->GetXaxis()->SetNdivisions(5);
  hMgg->GetYaxis()->SetNdivisions(5);
  hMgg->GetXaxis()->CenterTitle(true);
  hMgg->GetYaxis()->CenterTitle(true);
  hMgg->SetLabelSize(0.07,"xyz");
  hMgg->SetTitleSize(0.07,"xyz");
  hMgg->Draw();
  //hMggMC->Draw("same");
  hMggSignal->Draw("same");
  hMggSB->SetFillColorAlpha(kBlue, 0.2);
  //hMggSB->Scale(1e6);
  hMggSB->Draw("h same");
  hMgg->Draw("same");
  
  c22->cd(3);
  TH1F *hMkppi0Sub = (TH1F*)hMkppi0->Clone("Mkppi0Sub");
  hMkppi0Sub->SetTitle("; Mass(K^{+}#pi^{0}) [GeV]; Counts");
  hMkppi0Sub->Add(hMkppi0SB, -0.5);
  hMkppi0Sub->GetXaxis()->SetNdivisions(5);
  hMkppi0Sub->GetYaxis()->SetNdivisions(5);
  hMkppi0Sub->GetXaxis()->CenterTitle(true);
  hMkppi0Sub->GetYaxis()->CenterTitle(true);
  hMkppi0Sub->SetLabelSize(0.07,"xyz");
  hMkppi0Sub->SetTitleSize(0.07,"xyz");
  hMkppi0Sub->Draw();
  //hMkppi0MC->Draw("same");
  
  c22->cd(4);
  TH1F *hMpiLambdaSub = (TH1F*)hMpiLambdaSignal->Clone("MpiLambSub");
  hMpiLambdaSub->SetTitle("; Mass(#Lambda#pi^{0}) [GeV]; Counts");
  hMpiLambdaSub->Add(hMpiLambdaSB, -0.5);
  hMpiLambdaSub->GetXaxis()->SetNdivisions(5);
    hMpiLambdaSub->GetYaxis()->SetNdivisions(5);
    hMpiLambdaSub->GetXaxis()->CenterTitle(true);
    hMpiLambdaSub->GetYaxis()->CenterTitle(true);
    hMpiLambdaSub->SetLabelSize(0.07,"xyz");
    hMpiLambdaSub->SetTitleSize(0.07,"xyz");
    hMpiLambdaSub->Draw();
    //hMpiLambdaMC->Draw("same");

    c22->cd(5);
    hMkppi_piLambda->SetTitle("; Mass(K^{+}#pi^{0}) [GeV]; Mass(#Lambda#pi^{0}) [GeV]");
    hMkppi_piLambda->GetXaxis()->SetNdivisions(5);
    hMkppi_piLambda->GetYaxis()->SetNdivisions(5);
    hMkppi_piLambda->GetZaxis()->SetNdivisions(5);
    hMkppi_piLambda->GetXaxis()->CenterTitle(true);
    hMkppi_piLambda->GetYaxis()->CenterTitle(true);
    hMkppi_piLambda->SetLabelSize(0.07,"xyz");
    hMkppi_piLambda->SetTitleSize(0.07,"xyz");
    hMkppi_piLambda->Draw("colz");

    c11->Print("plots/pi0kplamb_mass_sb_hybrid.pdf");

    c22->Print("plots/pi0kplamb_mass_hybrid.pdf");

    //hGJCosTheta->Draw();
    //hMkppi0VsGJCosTheta->Draw("colz");
#endif
    return;
}
