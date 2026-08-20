
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
  FSCut::defineCut("KpiMass","abs(MASS([pi0],[K+]) - 1.2) < 0.8");

  FSCut::defineCut("Lambda2DSB","abs(MASS(1) - 1.115) < 0.010","abs(MASS(1) - 1.115) > 0.015 && abs(MASS(1) - 1.115) < 0.035",0.5);
  FSCut::defineCut("Pi02DSB","abs(MASS([pi0]) - 0.135) < 0.0125","abs(MASS([pi0]) - 0.135) > 0.02 && abs(MASS([pi0]) - 0.135) < 0.045",0.5);

  FSCut::defineCut("rf","abs(RFDeltaT) < 2.004","abs(RFDeltaT) > 2.004 && abs(RFDeltaT) < 18.036",0.125);

  FSCut::defineCut("Sigma1385Veto","MASS(1,[pi0]) > 2.0"); // 1.5 for Sigma(1350)

  // SET SOME DEFAULT SKIM CUTS
  DEFAULT_CUTS = "eBeam,chi2,unusedE,unusedTracks,z,MM2,t,Lambda,Pi0,KpiMass";
  DEFAULT_CUTS += ",Sigma1385Veto";
}

void plot_pi0kplamb_hybrid(bool bggen=false){

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
    CUTS.ReplaceAll(",unusedE","");
    TH1F* hEnUnusedSh = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","EnUnusedSh","(100,0.0,1.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hEnUnusedSh->SetXTitle("E_{unused}  [GeV/c^{2}]");
    hEnUnusedSh->SetYTitle("Events");
    hEnUnusedSh->Draw();
    TH1F* hEnUnusedShMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","EnUnusedSh","(100,0.0,1.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hEnUnusedShMC->Scale(hEnUnusedSh->GetMaximum()/hEnUnusedShMC->GetMaximum());
    hEnUnusedShMC->SetMarkerColor(kMagenta);
    hEnUnusedShMC->Draw("same");
    TLine* cutUnusedE = new TLine(0.1,0,0.1,hEnUnusedSh->GetMaximum());
    cutUnusedE->SetLineColor(kRed);
    cutUnusedE->Draw("same");
    
    c1->cd(2);
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",z","");
    TH1F* hProdVz = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","ProdVz","(100,0.,100.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hProdVz->SetXTitle("ProdVz  [cm]");
    hProdVz->SetYTitle("Events");
    hProdVz->Draw();
    TH1F* hProdVzMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","ProdVz","(100,0.,100.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hProdVzMC->Scale(hProdVz->GetMaximum()/hProdVzMC->GetMaximum());
    hProdVzMC->SetMarkerColor(kMagenta);
    hProdVzMC->Draw("same");
    TLine* cutVz_low = new TLine(52,0,52,hProdVz->GetMaximum());
    cutVz_low->SetLineColor(kRed);
    cutVz_low->Draw("same");
    TLine* cutVz_hi = new TLine(78,0,78,hProdVz->GetMaximum());
    cutVz_hi->SetLineColor(kRed);
    cutVz_hi->Draw("same");

    c1->cd(3);
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",t","");
    TH1F* htk = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","abs(-1*MASS2(1,-GLUEXTARGET))","(100,0,5)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    htk->SetXTitle("|-t| [GeV^{2}]");
    htk->SetYTitle("Entries");
    htk->Draw();
    htk->Fit("expo","","",0.5,1.0);
    TH1F* htkMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","abs(-1*MASS2(1,-GLUEXTARGET))","(100,0,5)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    htkMC->Scale(htk->GetMaximum()/htkMC->GetMaximum());
    htkMC->SetMarkerColor(kMagenta);
    htkMC->Draw("same");
    htkMC->Fit("expo","","",0.5,1.0);

    c1->cd(4);
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll("eBeam,","");
    TH1F* hEnPB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","EnPB","(125,5,12)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hEnPB->SetXTitle("E_{beam} [GeV]");
    hEnPB->SetYTitle("Entries");
    hEnPB->Draw();
    TH1F* hEnPBMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","EnPB","(125,5,12)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hEnPBMC->Scale(hEnPB->GetMaximum()/hEnPBMC->GetMaximum());
    hEnPBMC->SetMarkerColor(kMagenta);
    hEnPBMC->Draw("same");

    c1->cd(5);
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",MM2","");
    TH1F* hMM2 = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","RMASS2(GLUEXTARGET,B,-1,-2,-[pi0])","(100,-0.1,0.1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMM2->SetXTitle("Missing Mass Squared [GeV^{2}]");
    hMM2->SetYTitle("Entries");
    hMM2->Draw();
    TH1F* hMM2MC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","RMASS2(GLUEXTARGET,B,-1,-2,-[pi0])","(100,-0.1,0.1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMM2MC->Scale(hMM2->GetMaximum()/hMM2MC->GetMaximum());
    hMM2MC->SetMarkerColor(kMagenta);
    hMM2MC->Draw("same");

    c1->cd(6);
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",chi2,",",");
    TH1F* hChi2DOF = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","Chi2DOF","(40,0,20)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hChi2DOF->SetXTitle("#chi^{2}/dof");
    hChi2DOF->SetYTitle("Events");
    hChi2DOF->Draw();
    TH1F* hChi2DOFMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","Chi2DOF","(40,0,20)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hChi2DOFMC->Scale(hChi2DOF->GetMaximum()/hChi2DOFMC->GetMaximum());
    hChi2DOFMC->SetMarkerColor(kMagenta);
    hChi2DOFMC->Draw("same");
    
    CUTS.ReplaceAll(",Lambda",",LambdaSB");
    TH1F* hChi2DOFSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","Chi2DOF","(40,0,20)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hChi2DOFSB->SetMarkerColor(kBlue);
    hChi2DOFSB->Draw("same");

    TLegend *legCuts = new TLegend(0.5,0.5,0.85,0.88);
    legCuts->AddEntry(hChi2DOF,"GlueX Data","pe");
    legCuts->AddEntry(hChi2DOFSB,"Sideband Data","pe");
    legCuts->AddEntry(hChi2DOFMC,"Phasespace MC","pe");
    legCuts->Draw("same");

    c1->Print("plots/pi0kplamb_cuts_hybrid.pdf");

    if(bggen) {
	    cb->cd(1);   
	    CUTS = DEFAULT_CUTS;
	    CUTS.ReplaceAll(",chi2,",",");
	    TH1F* hChi2DOF_BGGEN = FSModeHistogram::getTH1F(FND_BGGEN,NT,"pi0kplamb","Chi2DOF","(40,0,20)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
	    hChi2DOF_BGGEN->SetXTitle("#chi^{2}/dof");
	    hChi2DOF_BGGEN->SetYTitle("Events");
	    hChi2DOF_BGGEN->Draw();
	    FSModeHistogram::drawMCComponentsSame(FND_BGGEN,NT,"pi0kplamb","Chi2DOF","(40,0,20)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    }

    // Momentum and angle distributions
    CUTS = "eBeam,Lambda,Pi0"; //DEFAULT_CUTS;
    FSCut::defineCut("Kstar892Mass","abs(MASS([pi0],[K+]) - 0.892) < 0.05");
    FSCut::defineCut("t05","abs(-1*MASS2(1,-GLUEXTARGET))<0.5");
    CUTS += ",Kstar892Mass,t05";

    //DEFAULT_CUTS = "eBeam,chi2,unusedE,unusedTracks,z,MM2,t,Lambda,Pi0,KpiMass";
    //DEFAULT_CUTS += ",Sigma1385Veto";
    //CUTS.ReplaceAll(",Sigma1385Veto","");

    TH2F* hLambdaMomentumVsPathLengthSignal = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","RMOMENTUM(1):VeeLP1","(100,-50,50,100,0,1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH2F* hLambdaMomentumVsPathLengthMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","RMOMENTUM(1):VeeLP1","(100,-50,50,100,0,1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));

    TH2F* hProtonMomentumVsThetaSignal = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","RMOMENTUM(1a):acos(RCOSINE(1a))*180/3.141","(180,0,90,100,0,1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH2F* hProtonMomentumVsThetaMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","RMOMENTUM(1a):acos(RCOSINE(1a))*180/3.141","(180,0,90,100,0,1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH2F* hPiMinusMomentumVsThetaSignal = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","RMOMENTUM(1b):acos(RCOSINE(1b))*180/3.141","(180,0,90,100,0,0.5)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH2F* hPiMinusMomentumVsThetaMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","RMOMENTUM(1b):acos(RCOSINE(1b))*180/3.141","(180,0,90,100,0,0.5)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));

    TH2F* hProtonMomentumVsPiMinusMomentumSignal = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","RMOMENTUM(1a):RMOMENTUM(1b)","(100,0,0.5,100,0,1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH2F* hProtonMomentumVsPiMinusMomentumMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","RMOMENTUM(1a):RMOMENTUM(1b)","(100,0,0.5,100,0,1)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));

    TH2F* hProtonThetaVsPiMinusThetaSignal = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","acos(COSINE(1a))*180/3.141:acos(COSINE(1b))*180/3.141","(100,0,90,100,0,90)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH2F* hProtonThetaVsPiMinusThetaMC = FSModeHistogram::getTH2F(FND_MC,NT,"pi0kplamb","acos(COSINE(1a))*180/3.141:acos(COSINE(1b))*180/3.141","(100,0,90,100,0,90)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));

    //hProtonThetaMC->Scale(hProtonThetaSignal->GetMaximum()/hProtonThetaMC->GetMaximum());
    //hProtonThetaMC->SetMarkerColor(kMagenta);
    

    // Some mass spectra...
    
    // protonpi mass
    CUTS = DEFAULT_CUTS;
    TH1F* hMpimpSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH1F* hMpimpMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMpimpMC->Scale(hMpimpSignal->GetMaximum()/hMpimpMC->GetMaximum());
    hMpimpMC->SetMarkerColor(kMagenta);
    
    CUTS.ReplaceAll(",Lambda",",LambdaSB");
    TH1F* hMpimpSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMpimpSB->SetFillColor(kBlue);

    CUTS.ReplaceAll(",LambdaSB","");
    TH1F* hMpimp = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));

    if(bggen) {
	    cb->cd(2);    
	    TH1F* hMpimp_BGGEN = FSModeHistogram::getTH1F(FND_BGGEN,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
	    hMpimp_BGGEN->SetXTitle("Mass(p#pi^{-}) [GeV]");
	    hMpimp_BGGEN->SetYTitle("Events");
	    hMpimp_BGGEN->Draw();
	    FSModeHistogram::drawMCComponentsSame(FND_BGGEN,NT,"pi0kplamb","MASS(1)","(100,1.08,1.155)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    }
     
    // gg mass
    CUTS = DEFAULT_CUTS;
    TH1F* hMggSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH1F* hMggMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMggMC->Scale(hMggSignal->GetMaximum()/hMggMC->GetMaximum());
    hMggMC->SetMarkerColor(kMagenta);
    
    CUTS.ReplaceAll(",Pi0",",Pi0SB");
    TH1F* hMggSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMggSB->SetFillColor(kBlue);
    
    CUTS.ReplaceAll(",Pi0SB","");
    TH1F* hMgg = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));

    if(bggen) {
	    cb->cd(3);    
	    TH1F* hMgg_BGGEN = FSModeHistogram::getTH1F(FND_BGGEN,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
	    hMgg_BGGEN->SetXTitle("Mass(#gamma#gamma) [GeV]");
	    hMgg_BGGEN->SetYTitle("Events");
	    hMgg_BGGEN->Draw();
	    FSModeHistogram::drawMCComponentsSame(FND_BGGEN,NT,"pi0kplamb","MASS([pi0])","(200,0.09,0.18)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    }

    // Lambda pi0 mass
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",Sigma1385Veto","");
    TH1F* hMpiLambdaSignal = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1,[pi0])","(100,1.2,2.2)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH1F* hMpiLambdaMC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS(1,[pi0])","(100,1.2,2.2)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMpiLambdaMC->Scale(hMpiLambdaSignal->GetMaximum()/hMpiLambdaMC->GetMaximum());
    hMpiLambdaMC->SetMarkerColor(kMagenta);
    
    CUTS.ReplaceAll(",Lambda",",LambdaSB");
    TH1F* hMpiLambdaSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS(1,[pi0])","(100,1.2,2.2)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMpiLambdaSB->SetFillColor(kBlue);

    // 2D sideband
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",Pi0","");
    CUTS.ReplaceAll(",Lambda","");
    TH2F* hMgg_pimp = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","MASS(1):MASS([pi0])","(100,0.09,0.18,100,1.08,1.18)",Form("CUT(%s)*CUTWT(Lambda2DSB,Pi02DSB,rf)",CUTS.Data()));

    // Kpi mass
    CUTS = DEFAULT_CUTS;
    TH1F* hMkppi0 = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    TH1F* hMkppi0MC = FSModeHistogram::getTH1F(FND_MC,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMkppi0MC->Scale(hMkppi0->GetMaximum()/hMkppi0MC->GetMaximum());
    hMkppi0MC->SetMarkerColor(kMagenta);

    if(bggen) {
	    cb->cd(4);    
	    TH1F* hMkppi0_BGGEN = FSModeHistogram::getTH1F(FND_BGGEN,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
	    hMkppi0_BGGEN->SetXTitle("Mass(K^{+}#pi^{0}) [GeV]");
	    hMkppi0_BGGEN->SetYTitle("Events");
	    hMkppi0_BGGEN->Draw();
	    FSModeHistogram::drawMCComponentsSame(FND_BGGEN,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    }
    
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",Lambda",",LambdaSB");
    TH1F* hMkppi0SB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    hMkppi0SB->SetFillColor(kBlue);

    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",Pi0","");
    CUTS.ReplaceAll(",Lambda","");
    TH1F* hMkppi02DSB = FSModeHistogram::getTH1F(FND_DATA,NT,"pi0kplamb","MASS([K+],[pi0])","(100,0.5,2.0)",Form("CUT(%s)*CUTWT(Lambda2DSB,Pi02DSB,rf)",CUTS.Data()));
    hMkppi02DSB->SetMarkerColor(kRed);

    // mass correlations
    CUTS = DEFAULT_CUTS;
    CUTS.ReplaceAll(",Sigma1385Veto","");
    TH2F* hMkppi_piLambda = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","MASS(1,[pi0]):MASS([K+],[pi0])","(100,0.5,2.0,100,1.0,3.0)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
 
    //TH1F* hGJCosTheta = FSHistogram::getTH1F(FND_DATA,"ntFSGlueX_100000000_100001","GJCOSTHETA(2;3;1;B)","(50,-1.,1.)",""); //,Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));
    //TH2F* hMkppi0VsGJCosTheta = FSModeHistogram::getTH2F(FND_DATA,NT,"pi0kplamb","HELCOSTHETA(2;3;1;B):MASS(2,3)","(100,0.5,2.0,50,-1.,1.)",Form("CUT(%s)*CUTWT(rf)",CUTS.Data()));


    FSHistogram::dumpHistogramCache();

    if(bggen) cb->Print("plots/pi0kplamb_bggen_hybrid.pdf");
    
    hMpimp->SetTitle("; Mass(p#pi^{-}) [GeV]; Counts");
    hMpimp->GetXaxis()->SetNdivisions(5);
    hMpimp->GetYaxis()->SetNdivisions(5);
    hMpimp->GetXaxis()->CenterTitle(true);
    hMpimp->GetYaxis()->CenterTitle(true);
    hMpimp->SetLabelSize(0.07,"xyz");
    hMpimp->SetTitleSize(0.07,"xyz");

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

#if 0
    TCanvas* c12 = new TCanvas("c12","c12",1000,600);
    c12->Divide(3,2);
    c12->cd(1);
    hProtonMomentumVsThetaMC->Draw("colz");
    c12->cd(2);
    hPiMinusMomentumVsThetaMC->Draw("colz");
    c12->cd(3);
    //hLambdaMomentumVsPathLengthMC->Draw("colz");
    //hProtonMomentumVsPiMinusMomentumMC->Draw("colz");
    hProtonThetaVsPiMinusThetaMC->Draw("colz");

    c12->cd(4);
    hProtonMomentumVsThetaSignal->Draw("colz");    
    c12->cd(5);
    hPiMinusMomentumVsThetaSignal->Draw("colz");
    c12->cd(6);
    //hLambdaMomentumVsPathLengthSignal->Draw("colz");
    //hProtonMomentumVsPiMinusMomentumSignal->Draw("colz");
    hProtonThetaVsPiMinusThetaSignal->Draw("colz");

    // Save histograms for making plots in separate macro
    TFile *f = new TFile("out_hybrid.root","recreate");
    
    hMpimp->SetName("hMpimp"); hMpimp->Write();
    hMpimpMC->SetName("hMpimpMC"); hMpimpMC->Write();
    hMpimpSB->SetName("hMpimpSB"); hMpimpSB->Write();
    
    hMpi0->SetName("hMpi0"); hMpi0->Write();
    hMpi0MC->SetName("hMpi0MC"); hMpi0MC->Write();
    hMpi0SB->SetName("hMpi0SB"); hMpi0SB->Write();
    
    hMkppi0->SetName("hMkppi0"); hMkppi0->Write();
    hMkppi0MC->SetName("hMkppi0MC"); hMkppi0MC->Write();
    hMkppi0SB->SetName("hMkppi0SB"); hMkppi0SB->Write();
    
    hMkppi0->SetName("hMkppi0"); hMkppi0->Write();
    hMkppi0MC->SetName("hMkppi0MC"); hMkppi0MC->Write();
    hMkppi0SB->SetName("hMkppi0SB"); hMkppi0SB->Write();
#endif
    
    return;
}
