// Basic pLots for flattened DATA trees:
// BIG FILE
// TString FND("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root");
// SMALL FILE (same dataset, only flattened 3-4 runs)
TString FND("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_small.root");

// Basic plots for flattened and skimmed DATA trees:
// TString FND("/work/halld/gluex_workshop_data/tutorial_2022/session2d/skim/tree_pi0eta__B4_M17_M7_DATA_sp17_*_GENERAL_SKIM.root");

// Basic plots for flattened MC trees:
//TString FND("/work/halld/gluex_workshop_data/tutorial_2022/session2d/flatten/flatMC/tree_pi0eta__B4_M17_M7_FLAT_MC.root");

// Basic plots for flattened BGGEN MC trees:
//TString FND("/work/halld/gluex_workshop_data/tutorial_2022/session2d/flatten/bggen/tree_pi0eta__B4_M17_M7_*.root");


// INDICES ASSIGNED BY 'flatten':
// 1. DecayingLambda (0)   1a. Proton (1)   1b. PiMinus2 (2)
// 2. DecayingKShort (3)   2a. PiPlus2 (4)   2b. PiMinus1 (5)
// 3. PiPlus1 (6)

TString NT("ntFSGlueX_MODECODE");

void setup(){
  if (FSModeCollection::modeVector().size() != 0) return;
  FSHistogram::readHistogramCache();
  FSModeCollection::addModeInfo("100000000_1100")->addCategory("m100000000_1100");

  // mand t CUTS:
  FSCut::defineCut("tRange","(abs(-1*MASS2(GLUEXTARGET,-1)-0.5)<0.5)");    // 0.1 < t < 0.3

  // STATIC CUTS
  FSCut::defineCut("rf","OR(abs(RFDeltaT)<2.0)", "abs(RFDeltaT)>6.0",0.125);
  FSCut::defineCut("chi2DOF","Chi2DOF","0.0","5.0");
  FSCut::defineCut("unusedE","EnUnusedSh<0.1");
  FSCut::defineCut("unusedTracks","NumUnusedTracks<1"); // No unused tracks
  FSCut::defineCut("coherentPeak","EnPB","8.2","8.8"); // Coherent peak: 8.2 < E_beam < 8.8
  FSCut::defineCut("flightSigLambda","VeeLP1>2.0");
  FSCut::defineCut("flightSigKShort","VeeLP2>2.0");

  // CUTS WITH SIDEBANDS
  FSCut::defineCut("KShort","abs(MASS(2a,2b)-0.4976)<0.03","(abs(MASS(2a,2b)-0.4976+0.0974)<0.015 || abs(MASS(2a,2b)-0.4976-0.1226)<0.015)", 1.0);
  FSCut::defineCut("Lambda","abs(MASS(1a,1b)-1.119)<0.01375","(abs(MASS(1a,1b)-1.119+0.032875)<0.006875 || abs(MASS(1a,1b)-1.119-0.032125)<0.006875)", 1.0);

  FSCut::defineCut("selectKSTAR892","MASS({DecayingKShort},{PiPlus1})","0.85","0.95", "0.0", "0.85", "0.95", "1.0");
  FSCut::defineCut("selectKSTAR1430","MASS({DecayingKShort},{PiPlus1})","0.85","0.95", "0.0", "0.85", "0.95", "1.0");
  FSCut::defineCut("rejectSigmas", "MASS({DecayingLambda},{PiPlus1})","2.0","3.5");
}

void plots(bool bggen=false){
  // FSHistogram::clearHistogramCache("kspiplamb_plots");
  gROOT->SetBatch(kTRUE);
  setup();

  // --- Debug: confirm file & tree names ---
  std::cout << "[DBG] FND = " << FND << "\n";
  std::cout << "[DBG] NT (raw) = " << NT << "\n";
  TString resolvedNT = NT;                           // what FSMode would substitute
  resolvedNT.ReplaceAll("MODECODE","100000000_1100");
  std::cout << "[DBG] NT (resolved) = " << resolvedNT << "\n";

  TFile f(FND, "READ");
  if (f.IsZombie()) {
    std::cout << "[DBG] Could not open file: " << FND << "\n";
  } else {
    f.ls();
    auto t = dynamic_cast<TTree*>(f.Get(resolvedNT));
    std::cout << "[DBG] Tree ptr for resolvedNT: " << t << "\n";
    if (!t) {
      std::cout << "[DBG] TTrees available (ntFSGlueX*):\n";
      TIter nextkey(f.GetListOfKeys());
      while (TObject* o = nextkey()) {
        auto* k = dynamic_cast<TKey*>(o);
        if (!k) continue;
        if (TString(k->GetClassName())=="TTree" && TString(k->GetName()).BeginsWith("ntFSGlueX"))
          std::cout << "    " << k->GetName() << "\n";
      }
    }
  }
  // --- End debug ---

  system("rm -rf plots");  gSystem->mkdir("plots",kTRUE);
  const char* out = "plots/all_plots.pdf";

  // TH1F* hM1 = FSModeHistogram::getTH1F(FND,NT,"m101_1","EnUnusedSh","(100,0.0,1.0)","CUT(unusedTracks,zProton,chi2,cet0103,e8288,photFiducialA,photFiducialB,photFiducialC,photFiducialD,delta,rf,eta,pi0,rejectOmega,protMom)");


  TCanvas* c1 = new TCanvas("c1","c1",1200,800);
  c1->Divide(3,2);
  c1->cd(1);
  TH1F* hM1 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","EnUnusedSh","(100,0.0,1.0)","CUT(tRange,rf,chi2DOF,unusedTracks,coherentPeak)");
  hM1->SetTitle("E_{unused} for -tt in (0.0,1.0)");
  hM1->SetXTitle("E_{unused}  [GeV/c^{2}]");
  hM1->SetYTitle("Events (log)");
  gPad->SetLogy(1);
  hM1->SetMinimum(0.5);
  hM1->Draw();
  TLine* cutUnusedE = new TLine(0.1,0,0.1,hM1->GetMaximum());
  cutUnusedE->SetLineColor(kRed);
  cutUnusedE->Draw("same");
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","EnUnusedSh","(100,0.0,1.0)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  c1->cd(2);
  TH1F* hM6 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","ProdVz","(100,0.,100.0)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM6->SetTitle("ProdVz for -t in (0.0,1.0)");
  hM6->SetXTitle("ProdVz  [GeV/c^{2}]");
  hM6->SetYTitle("Events");
  hM6->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","ProdVz","(100,0.,100.0)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  TLine* cutVz_low = new TLine(52,0,52,hM6->GetMaximum());
  cutVz_low->SetLineColor(kRed);
  cutVz_low->Draw("same");
  TLine* cutVz_hi = new TLine(78,0,78,hM6->GetMaximum());
  cutVz_hi->SetLineColor(kRed);
  cutVz_hi->Draw("same");
  c1->cd(3);
  TH1F* hM4a = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","abs(-1*MASS2(GLUEXTARGET,-1))","(100,0,1)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM4a->SetTitle("|-t|");
  hM4a->SetXTitle("|-t| [GeV^{2}]");
  hM4a->SetYTitle("Entries");
  TLine* cutt_low = new TLine(0.1,0,0.1,hM4a->GetMaximum());
  cutt_low->SetLineColor(kRed);
  hM4a->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","abs(-1*MASS2(GLUEXTARGET,-1))","(100,0,1)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  cutt_low->Draw("same");
  TLine* cutt_hi = new TLine(0.3,0,0.3,hM4a->GetMaximum());
  cutt_hi->SetLineColor(kRed);
  cutt_hi->Draw("same");
  c1->cd(4);
  TH1F* hM4b = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","EnPB","(125,5,12)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM4b->SetTitle("E_{beam} for -t in (0.0,1.0)");
  hM4b->SetXTitle("E_{beam} [GeV]");
  hM4b->SetYTitle("Entries");
  TLine* cutEb_low = new TLine(8.2,0,8.2,hM4b->GetMaximum());
  cutEb_low->SetLineColor(kRed);
  hM4b->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","EnPB","(125,5,12)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  cutEb_low->Draw("same");
  TLine* cutEb_hi = new TLine(8.8,0,8.8,hM4b->GetMaximum());
  cutEb_hi->SetLineColor(kRed);
  cutEb_hi->Draw("same");
  c1->cd(5);
  TH1F* hM4 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","Chi2DOF","(80,0,20)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM4->SetTitle("#chi^{2}/dof for -t in (0.0,1.0)");
  hM4->SetXTitle("#chi^{2}/dof");
  hM4->SetYTitle("Events");
  TLine* cutChi2 = new TLine(3.3,0,3.3,hM4->GetMaximum());
  cutChi2->SetLineColor(kRed);
  hM4->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","Chi2DOF","(80,0,20)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  cutChi2->Draw("same");
  
  c1->cd(6);
  TH1F* hM8 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","acos(COSINE(2,3))*180/3.141","(240,0.,60)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM8->SetTitle("#vartheta_{#pi^{+}} for -t in (0.0,1.0)");
  hM8->SetXTitle("#vartheta_{#pi^{+}}  [#circ]");
  hM8->SetYTitle("Entries");
  hM8->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","acos(COSINE(2,3))*180/3.141","(240,0.,60)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  TLine* cutFidu1 = new TLine(2.5,0,2.5,hM8->GetMaximum());
  cutFidu1->SetLineColor(kRed);
  cutFidu1->Draw("same");
  TLine* cutFidu2 = new TLine(10.3,0,10.3,hM8->GetMaximum());
  cutFidu2->SetLineColor(kRed);
  cutFidu2->Draw("same");
  TLine* cutFidu3 = new TLine(11.9,0,11.9,hM8->GetMaximum());
  cutFidu3->SetLineColor(kRed);
  cutFidu3->Draw("same");
  c1->Print(Form("%s(", out));  // open multipage PDF

  TCanvas* c11 = new TCanvas("c11","c11",800,800);
  c11->Divide(2,2);
  c11->cd(1);
  TH1F* hM2 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(2,3)","(60,0.2,0.8)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM2->SetTitle("M(K^{*}) for -t in (0.0,1.0)");
  hM2->SetXTitle("M(KShort #pi^{+})  [GeV/c^{2}]");
  hM2->SetYTitle("Events / 10??? MeV/c^{2}");
  hM2->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS(2,3)","(60,0.2,0.8)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  TLine* cutEtaSigL = new TLine(0.548-0.05,0,0.548-0.05,hM2->GetMaximum());
  TLine* cutEtaSigR = new TLine(0.548+0.05,0,0.548+0.05,hM2->GetMaximum());
  TLine* cutEtaSBLowL = new TLine(0.42,0,0.42,hM2->GetMaximum());
  TLine* cutEtaSBLowR = new TLine(0.47,0,0.47,hM2->GetMaximum());
  TLine* cutEtaSBHiL = new TLine(0.63,0,0.63,hM2->GetMaximum());
  TLine* cutEtaSBHiR = new TLine(0.68,0,0.68,hM2->GetMaximum());
  cutEtaSigL->SetLineColor(kRed);
  cutEtaSigR->SetLineColor(kRed);
  cutEtaSBLowL->SetLineColor(kRed);
  cutEtaSBLowR->SetLineColor(kRed);
  cutEtaSBHiL->SetLineColor(kRed);
  cutEtaSBHiR->SetLineColor(kRed);
  cutEtaSigL->Draw("same");
  cutEtaSigR->Draw("same");
  cutEtaSBLowL->Draw("same");
  cutEtaSBLowR->Draw("same");
  cutEtaSBHiL->Draw("same");
  cutEtaSBHiR->Draw("same");
  c11->cd(2);
  TH1F* hM9 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(3)","(60,0.0,0.3)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM9->SetTitle("M(#pi^{+}) for -t in (0.0,1.0)");
  hM9->SetXTitle("M(#pi^{+})  [GeV/c^{2}]");
  hM9->SetYTitle("Events / 10??? MeV/c^{2}");
  hM9->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS(3)","(60,0.0,0.3)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM9->SetTitle("M(#pi^{+}) for -t in (0.0,1.0)");
  TLine* cutPi0SigL = new TLine(0.135-0.025,0,0.135-0.025,hM9->GetMaximum());
  TLine* cutPi0SigR = new TLine(0.135+0.025,0,0.135+0.025,hM9->GetMaximum());
  TLine* cutPi0SBLowL = new TLine(0.08,0,0.08,hM9->GetMaximum());
  TLine* cutPi0SBLowR = new TLine(0.105,0,0.105,hM9->GetMaximum());
  TLine* cutPi0SBHiL = new TLine(0.165,0,0.165,hM9->GetMaximum());
  TLine* cutPi0SBHiR = new TLine(0.19,0,0.19,hM9->GetMaximum());
  cutPi0SigL->SetLineColor(kRed);
  cutPi0SigR->SetLineColor(kRed);
  cutPi0SBLowL->SetLineColor(kRed);
  cutPi0SBLowR->SetLineColor(kRed);
  cutPi0SBHiL->SetLineColor(kRed);
  cutPi0SBHiR->SetLineColor(kRed);
  cutPi0SigL->Draw("same");
  cutPi0SigR->Draw("same");
  cutPi0SBLowL->Draw("same");
  cutPi0SBLowR->Draw("same");
  cutPi0SBHiL->Draw("same");
  cutPi0SBHiR->Draw("same");
  c11->cd(3);
  TH1F* hM3 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(2,3)","(100,0.8,1.8)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM3->SetTitle("M(KS#pi^{+}) for -t in (0.0,1.0)");
  hM3->SetXTitle("M(KS#pi^{+})  [GeV/c^{2}]");
  hM3->SetYTitle("Events / 10?? MeV/c^{2}");
  TLine* cutDelta = new TLine(1.4,0,1.4,hM3->GetMaximum());
  cutDelta->SetLineColor(kRed);
  hM3->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS(2,3)","(100,0.8,1.8)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  cutDelta->Draw("same");
  c11->cd(4);
  TH1F* hM5 = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","RFDeltaT","(400,-20,20)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  hM5->SetTitle("#Delta t_{RF} for -t in (0.0,1.0)");
  hM5->SetXTitle("#Delta t_{RF}");
  hM5->SetYTitle("Events");
  TLine* cutRFSigL = new TLine(-2.0,0,-2.0,hM5->GetMaximum());
  TLine* cutRFSigR = new TLine(2.0,0,2.0,hM5->GetMaximum());
  cutRFSigL->SetLineColor(kRed);
  cutRFSigR->SetLineColor(kRed);
  hM5->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","RFDeltaT","(400,-20,20)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  cutRFSigL->Draw("same");
  cutRFSigR->Draw("same");
  c11->Print(out);              // middle pages
  
  // c1->Print("plots/p001_etapi.pdf");

  TCanvas* c2 = new TCanvas("c2","c2",1200,400);
  c2->Divide(3,1);
  c2->cd(1);
  TH1F* hMetapi = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(2,3)","(100,0.5,2.5)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)");
  TH1F* hMetapiSig = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(2,3)","(100,0.5,2.5)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  TH1F* hMetapiBg = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(2,3)","(100,0.5,2.5)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTSBWT(rf,KShort,Lambda)*(-1.0)");
  hMetapiSig->SetFillColor(kBlue);
  hMetapiBg->SetFillColor(kRed);
  hMetapi->SetTitle("M(KS#pi^{+}) for -t in (0.0,1.0)");
  hMetapi->SetXTitle("M(KS#pi^{+}) [GeV/c^{2}]");
  hMetapi->SetYTitle("Events");
  hMetapi->Draw();
  hMetapiSig->Draw("hist,same");
  hMetapiBg->Draw("hist,same");

  c2->cd(2);
  hMetapiSig->SetTitle("M(KS#pi^{+}) for -t in (0.0,1.0)");
  hMetapiSig->SetXTitle("M(KS#pi^{+}) [GeV/c^{2}]");
  hMetapiSig->SetYTitle("Events");
  hMetapiSig->DrawClone();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS(2,3)","(100,0.5,2.5)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  cout << hMetapiSig->Integral() << endl;

  FSFitUtilities::createFunction(new FSFitPOLY("p",1.04,1.56,1,0.0),1600.0,-900);
  FSFitUtilities::createFunction(new FSFitGAUS("g",1.04,1.56),500.0,1.32,0.05);
  FSFitUtilities::createFunction("pg","p+g");
  FSFitUtilities::fixParameters("p");
  FSFitUtilities::migrad(hMetapiSig,"pg");
  TF1* fpg = FSFitUtilities::getTF1("pg");
  fpg->SetLineColor(kRed); fpg->SetLineStyle(kSolid);
  fpg->Draw("same");
  TF1* fg = FSFitUtilities::getTF1("g");
  fg->SetLineColor(kBlue); fg->SetLineStyle(kSolid);
  fg->Draw("same");
  cout << "fg Integral: " << fg->Integral(1.04,1.56) << endl;
  
  c2->cd(3);
  TH2F* hMetapiVsGJCosTheta = FSModeHistogram::getTH2F(FND,NT,"m100000000_1100","GJCOSTHETA(2;3;GLUEXBEAM):MASS(2,3)","(100,0.7,2.7,50,-1.,1.)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  hMetapiVsGJCosTheta->SetXTitle("M(KS#pi^{+}) [GeV/c^{2}]");
  hMetapiVsGJCosTheta->SetYTitle("cos#theta_{GJ}");
  hMetapiVsGJCosTheta->Draw("colz");
  c2->Print(out);


  TCanvas* c3 = new TCanvas("c3","c3",800,800);
  c3->Divide(2,2);
  c3->cd(1);
  hMetapiSig->DrawClone();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS(2,3)","(100,0.5,2.5)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  
  c3->cd(2);
  TH1F* hMpiproton = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(1,3)","(100,0.9,3.9)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  hMpiproton->SetTitle("M(#Lambda#pi^{+}) for -t in (0.0,1.0)");
  hMpiproton->SetXTitle("M(#Lambda#pi^{+}) [GeV/c^{2}]");
  hMpiproton->SetYTitle("Events");
  hMpiproton->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS(1,3)","(100,0.9,3.9)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  
  c3->cd(3);
  TH1F* hMetaproton = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS(1,2)","(100,1.4,3.9)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  hMetaproton->SetTitle("M(#Lambda# KS) for -t in (0.0,1.0)");
  hMetaproton->SetXTitle("M(#Lambda KS) [GeV/c^{2}]");
  hMetaproton->SetYTitle("Events");
  hMetaproton->Draw();
  if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS(1,2)","(100,1.4,3.9)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");

  // c3->cd(4);
  // TH1F* hMpi0g = FSModeHistogram::getTH1F(FND,NT,"m100000000_1100","MASS([pi0],[eta]b)","(100,0.,2.)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");
  // hMpi0g->SetTitle("M(#pi^{0}#gamma) for -t in (0.0,1.0)");
  // hMpi0g->SetXTitle("M(#pi^{0}#gamma) [GeV/c^{2}]");
  // hMpi0g->SetYTitle("Events");
  // hMpi0g->Draw();
  // if(bggen) FSModeHistogram::drawMCComponentsSame(FND,NT,"m100000000_1100","MASS([pi0],[eta]b)","(100,0.,2.)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)*CUTWT(rf,KShort,Lambda)");

  c3->Print(Form("%s)", out));  // close multipage PDF

  // Auto-open the PDF viewer (even if in batch mode):
  gSystem->Exec(Form("evince %s &", out));

// // print NT and resolve MODECODE by hand
// std::cout << "NT = " << NT << "\n";
// TString resolvedNT = NT;
// resolvedNT.ReplaceAll("MODECODE","100000000_1100");  // your mode code
// std::cout << "Resolved NT = " << resolvedNT << "\n";

// // see what's in the file
// TFile f(FND,"READ");
// f.ls();
// std::cout << "Tree ptr: " << f.Get(resolvedNT) << "\n";


  // FSHistogram::dumpHistogramCache("kspiplamb_plots");
}