#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "/work/halld/home/dbarton/gluex/KShortPipLambda/RooTestBW.h"
#include "/work/halld/home/dbarton/gluex/KShortPipLambda/Roo2BW.h"

using namespace RooFit;

void fit_projections_roofit(){

  TFile* mProjFile = TFile::Open("/volatile/halld/home/dbarton/pipkslamb/skims/tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols.root","READ");

  TTree * tree = (TTree*)mProjFile->Get( "ntFSGlueX_100000000_1100");

  Long64_t nEntries = tree->GetEntries();

  //// Create 4-vector pointers
  //// Decaying Lambda
  double PxP1, PyP1, PzP1, EnP1;
  tree->SetBranchAddress("PxP1", &PxP1);
  tree->SetBranchAddress("PyP1", &PyP1);
  tree->SetBranchAddress("PzP1", &PzP1);
  tree->SetBranchAddress("EnP1", &EnP1);

  double PxP2, PyP2, PzP2, EnP2;
  tree->SetBranchAddress("PxP2", &PxP2);
  tree->SetBranchAddress("PyP2", &PyP2);
  tree->SetBranchAddress("PzP2", &PzP2);
  tree->SetBranchAddress("EnP2", &EnP2);

  double PxP3, PyP3, PzP3, EnP3;
  tree->SetBranchAddress("PxP3", &PxP3);
  tree->SetBranchAddress("PyP3", &PyP3);
  tree->SetBranchAddress("PzP3", &PzP3);
  tree->SetBranchAddress("EnP3", &EnP3);

  double flightLengthKShort, flightLengthLambda, rf;

  // Cut string used in FSRoot script:
  // CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda})
  
  // regular cuts:
  // ROOT.FSCut.defineCut("flightLengthLambda", "VeeLP1>2.0")
  // ROOT.FSCut.defineCut("flightLengthKShort", "VeeLP2>2.0")
  // ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})>2.00 && MASS({DecayingLambda},{PiPlus1})<4.0")
  
  // weighted cuts:
  // ROOT.FSCut.defineCut("rf", "abs(RFDeltaT)>2.0", "abs(RFDeltaT)>6.0", 0.1667)
  // ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0)
  // ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0)

  tree->SetBranchAddress("VeeLP1", &flightLengthKShort);
  tree->SetBranchAddress("VeeLP2", &flightLengthLambda);
  tree->SetBranchAddress("RFDeltaT", &rf);

  TH1 *h_Pwave = new TH1D("h_Pwave", "h_Pwave", 80, 0.5, 2.5);
  for (Long64_t i = 0; i < nEntries; ++i)
  {
    tree->GetEntry(i);

    //masses
    double massKpi = sqrt(pow(EnP2 + EnP3, 2) - pow(PxP2 + PxP3, 2) - pow(PyP2 + PyP3, 2) - pow(PzP2 + PzP3, 2));
    double massLam = sqrt(pow(EnP1, 2) - pow(PxP1, 2) - pow(PyP1, 2) - pow(PzP1, 2));
    double massKs = sqrt(pow(EnP2, 2) - pow(PxP2, 2) - pow(PyP2, 2) - pow(PzP2, 2));
    double massLamPi = sqrt(pow(EnP1 + EnP3, 2) - pow(PxP1 + PxP3, 2) - pow(PyP1 + PyP3, 2) - pow(PzP1 + PzP3, 2));

    bool flKs = flightLengthKShort > 2.0;
    bool flLam = flightLengthLambda > 2.0;
    bool rejectSig = (massLamPi > 2.00) && (massLamPi < 4.0);
    bool rfCut = abs(rf) > 2.0;
    bool KsCut = abs(massKs - 0.4976) < 0.03;
    bool LamCut = abs(massLam - 1.119) < 0.01375;
    
    /// sidebads
    double totalWeight = 1.0;

    bool lowerKs = (abs(massKs - 0.4976 + 0.0974) < 0.015);
    bool upperKs = (abs(massKs - 0.4976 - 0.1226) < 0.015);
    bool lowerLam = (abs(massLam - 1.119 + 0.032875) < 0.006875);
    bool upperLam = (abs(massLam - 1.119 - 0.032125) < 0.006875);
    bool rfWeight = abs(rf) > 6.0;

    double ksweight = 0.0;
    if( lowerKs || upperKs){
      ksweight = -1.0;
    }
    else if(KsCut){
      ksweight = 1.0;
    }

    double lamweight = 0.0;
    if( lowerLam || upperLam){
      lamweight = -1.0;
    }
    else if(LamCut){
      lamweight = 1.0;
    }

    double rfweight = 0.0;
    if( rfWeight ){
      rfweight = -0.1667;
    }
    else if( rfCut ){
      rfweight = 1.0;
    }

    totalWeight = ksweight * lamweight * rfweight;
    // histogram bins are filled including the lower bound
    //  but excluding the upper bound
    if(totalWeight != 0)
      h_Pwave->Fill(massKpi, totalWeight);
  }

  // Declare observable Ks Pi mass
  RooRealVar mass("mass", "mass", 0.5, 2.5);
 
  //RooDataSet dataetap( "dataetap","Weigted Data M(etap) ", RooArgSet(massetap,weight),  WeightVar(weight), Import(*tree) );

  // Create a binned dataset with contents of TH1 and associates it to mass
  RooDataHist dataHist_P("dataHist_P", "dataHist_P", mass, Import(*h_Pwave));

  // Create Canvas
  TCanvas* fit_c = new TCanvas("fit","", 1200, 1600);
  //  fit_c->SetLeftMargin(100);
  fit_c->SetRightMargin(5);
  
  
  /////////////////// Fit Interfering 2 Rel. Breit-Wigner //////////////////
  /////////////////////// Hall D Parametrization ///////////////////////////
  //////RelBW1//// 
  RooRealVar massBW_1("massBW_1", "mass_2", 0.892, 0.6, 1.0);
  RooRealVar widthBW_1("widthBW_1", "width_1", .088, .04 , .15); 
  RooRealVar spin_1("spin1", "spin_1", 1); // P-wave
  //////RelBW2//// 
  RooRealVar massBW_2("massBW_2", "mass_2", 1.4, 1.0, 2.0);
  RooRealVar widthBW_2("widthBW_2", "width_2", .167, .05, 0.35); 
  RooRealVar spin_2("spin2", "spin_2", 1); // P-wave
  ///Scale/Phase///
  RooRealVar scale("scale", "scale", .59, 0.0, 1.);
  RooRealVar phase("phase", "phase", 1.79 , -TMath::Pi(), TMath::Pi());
  RooRealVar rInt("rInt", "rInt", 1.0, 0., 2.);
  RooRealVar massd1("massd1_2", "massd1", .497); 
  RooRealVar massd2("massd2_2", "massd2", .139); 
  Roo2BW rel_intBW("rel_intBW","Int. Rel. BW", mass, massBW_1, widthBW_1, spin_1,
		   massBW_2, widthBW_2, spin_2, scale, phase, rInt, massd1, massd2);
    mass.setRange("PWA Fit", 0.5, 2.5);

  RooRealVar coef0("coef0", "coef0", 1.0, 0., 10.);
  RooRealVar coef1("coef1", "coef1", 0.0, 0., 10.);
  RooRealVar coef2("coef2", "coef2", 0.0, 0., 10.);
  RooRealVar coef3("coef3", "coef3", 0.0, 0., 10.);

  RooBernstein bkg("bkg", "Background", mass, RooArgList(coef0, coef1, coef2, coef3));
  RooRealVar sig2bkg("sig2bkg", "fraction of component 1 in signal", .6, 0., 1.);
  // Reverse order due to the way the pdf is written
  RooAddPdf bern2BW("bern2BW", "bern2BW", RooArgList(rel_intBW, bkg), sig2bkg);
  
  // bern2BW.fitTo(dataHist_P, Range("PWA Fit"));

  // //// Define BW Compnents //////
  // RooRealVar massBW1_fix("massBW1fix","massBW1fix",massBW_1.getVal());
  // RooRealVar widthBW1_fix("widthBW1fix","widthBW1fix",widthBW_1.getVal());
  // RooTestBW rel_intBW1("rel_inBW1","RelBreitWigner", mass, massBW1_fix,
	// 		       widthBW1_fix, spin_1, massd2, massd1 );
  // RooRealVar massBW2_fix("massBW2fix","massBW2fix",massBW_2.getVal());
  // RooRealVar widthBW2_fix("widthBW2fix","widthBW2fix",widthBW_2.getVal());
  // RooTestBW rel_intBW2("rel_intBW2","RelBreitWigner", mass, massBW2_fix,
	// 		       widthBW2_fix, spin_2, massd2, massd1 );
  // RooRealVar plotfrac("plotfrac", "fraction of component 1 in signal", scale.getVal());
  // // Reverse order due to the way the pdf is written
  // RooAddPdf plot2BW("2BW", "2BW", RooArgList(rel_intBW2, rel_intBW1), plotfrac);

  // RooBernstein plotbkg("plotbkg_obj", "Background", mass, RooArgList(coef0.getVal(), coef1.getVal(), coef2.getVal(), coef3.getVal()));
  // RooRealVar plotsig2bkg("sig2bkg", "fraction of component 1 in signal", sig2bkg.getVal());
  // // Reverse order due to the way the pdf is written
  // RooAddPdf plotbern2BW("plotbern2BW_obj", "bern2BW", RooArgList(plot2BW, plotbkg), plotsig2bkg);


  // // Define Frame for Int. BW
  // mass.setRange("PWA Plot", 0.5, 2.5);
  // RooPlot* frame_intBW_P = mass.frame();
  // frame_intBW_P->GetXaxis()->SetTitle("M[Ks #pi] (GeV)");
  // frame_intBW_P->GetYaxis()->SetTitle("Combinations / 40 MeV");
  // frame_intBW_P->GetYaxis()->SetTitleOffset(1.1);
  // frame_intBW_P->GetYaxis()->SetMaxDigits(3);
  // dataHist_P.plotOn(frame_intBW_P);
  // bern2BW.plotOn(frame_intBW_P, Range("PWA Plot"));
  // plotbern2BW.plotOn(frame_intBW_P, Components(plot2BW), LineStyle(kDotted), LineColor(kOrange),Range("PWA Plot"));
  // plotbern2BW.plotOn(frame_intBW_P, Components(plotbkg), LineStyle(kDotted), LineColor(kOrange+7),Range("PWA Plot"));
  // cout << frame_intBW_P->chiSquare() << endl;

  // // Output pdf
  // frame_intBW_P->Draw();
  // fit_c->Print("fit_rooFit.pdf");

  bern2BW.fitTo(dataHist_P, Range("PWA Fit"), SumW2Error(true));

  // Define Frame for Int. BW
  mass.setRange("PWA Plot", 0.5, 2.5);
  RooPlot* frame_intBW_P = mass.frame();
  frame_intBW_P->GetXaxis()->SetTitle("M[Ks #pi] (GeV)");
  frame_intBW_P->GetYaxis()->SetTitle("Combinations / 40 MeV");
  frame_intBW_P->GetYaxis()->SetTitleOffset(1.1);
  frame_intBW_P->GetYaxis()->SetMaxDigits(3);

  dataHist_P.plotOn(frame_intBW_P);
  bern2BW.plotOn(frame_intBW_P, Range("PWA Plot"));
  bern2BW.plotOn(frame_intBW_P, Components(rel_intBW), 
                LineStyle(kDotted), LineColor(kOrange), Range("PWA Plot"));
  bern2BW.plotOn(frame_intBW_P, Components(bkg), 
                LineStyle(kDotted), LineColor(kOrange+7), Range("PWA Plot"));

  cout << frame_intBW_P->chiSquare() << endl;
  frame_intBW_P->Draw();
  fit_c->Print("fit_rooFit.pdf");

}
