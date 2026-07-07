#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooChebychev.h"
#include "RooAddPdf.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooPlot.h"
#include "/work/halld/home/dbarton/gluex/KShortPipLambda/fitting/Roo2BW.h"
#include <fstream>
#include "/work/halld/home/dbarton/gluex/KShortPipLambda/fitting/RooBernsteinQ.h"

using namespace RooFit;

void plots_roofit(){

  // contains all cuts including weighting (but might not weight correctly)
  // TFile* mProjFile = TFile::Open("/volatile/halld/home/dbarton/pipkslamb/skims/tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols_KPiSystem.root","READ");
  // Contains only "event selection" cuts, no weighting.  Apply weights manually in this script.
  TFile* mProjFile = TFile::Open("/volatile/halld/home/dbarton/pipkslamb/skims/tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols.root","READ");




  TTree * tree = (TTree*)mProjFile->Get("ntFSGlueX_100000000_1100");
  Long64_t nEntries = tree->GetEntries();

  // Lambda
  double PxP1, PyP1, PzP1, EnP1;
  tree->SetBranchAddress("PxP1", &PxP1);
  tree->SetBranchAddress("PyP1", &PyP1);
  tree->SetBranchAddress("PzP1", &PzP1);
  tree->SetBranchAddress("EnP1", &EnP1);

  // KShort
  double PxP2, PyP2, PzP2, EnP2;
  tree->SetBranchAddress("PxP2", &PxP2);
  tree->SetBranchAddress("PyP2", &PyP2);
  tree->SetBranchAddress("PzP2", &PzP2);
  tree->SetBranchAddress("EnP2", &EnP2);

  // Bachelor pi+
  double PxP3, PyP3, PzP3, EnP3;
  tree->SetBranchAddress("PxP3", &PxP3);
  tree->SetBranchAddress("PyP3", &PyP3);
  tree->SetBranchAddress("PzP3", &PzP3);
  tree->SetBranchAddress("EnP3", &EnP3);

  TH1 *h_Pwave = new TH1D("h_Pwave", "h_Pwave", 63, 0.628, 2.203);
  for (Long64_t i = 0; i < nEntries; ++i)
  {
    tree->GetEntry(i);

    double massKpi  = sqrt(pow(EnP2+EnP3,2) - pow(PxP2+PxP3,2) - pow(PyP2+PyP3,2) - pow(PzP2+PzP3,2));

    double totalWeight = 1;
    if(totalWeight != 0)
      h_Pwave->Fill(massKpi, totalWeight);
  }

  // ---- RooFit setup ----
  RooRealVar mass("mass", "mass", 0.5, 2.5);
  RooDataHist dataHist_P("dataHist_P", "dataHist_P", mass, Import(*h_Pwave));

  //// RelBW1
  RooRealVar massBW_1("massBW_1", "mass_1",  0.892, 0.6,  1.0);
  RooRealVar widthBW_1("widthBW_1","width_1", 0.088, 0.04, 0.15);
  RooRealVar spin_1("spin1","spin_1", 1);
  //// RelBW2
  RooRealVar massBW_2("massBW_2", "mass_2",  1.4,   1.0,  2.0);
  RooRealVar widthBW_2("widthBW_2","width_2", 0.167, 0.05, 0.35);
  RooRealVar spin_2("spin2","spin_2", 1);
  //// Scale/Phase
  RooRealVar scale("scale",  "scale",  0.59,  0.0, 1.0);
  RooRealVar phase("phase",  "phase",  1.79, -TMath::Pi(), TMath::Pi());
  RooRealVar rInt("rInt",    "rInt",   0.98, 0.0, 1.0);
  RooRealVar massd1("massd1_2","massd1", 0.497);
  RooRealVar massd2("massd2_2","massd2", 0.139);
  Roo2BW rel_intBW("rel_intBW","Int. Rel. BW", mass,
                   massBW_1, widthBW_1, spin_1,
                   massBW_2, widthBW_2, spin_2,
                   scale, phase, rInt, massd1, massd2);

  //// Bernstein background
  RooRealVar coef0("coef0","coef0", 0.0);
  RooRealVar coef1("coef1","coef1", 0.905, 0., 1.);
  RooRealVar coef2("coef2","coef2", 0.030, 0., 1.);
  RooRealVar coef3("coef3","coef3", 0.0);

  // Breakup momentum range over fit range (0.61 to 2.3 GeV in mass)
  // You'll need to compute q at mass=0.61 and mass=2.3 once to get qmin/qmax,
  // or just pick a wide enough range and let the data normalize within it.
  RooRealVar qmin("qmin","qmin", 0.0);
  RooRealVar qmax("qmax","qmax", 1.2);  // adjust to match your kinematic range

  RooBernsteinQ bkg("bkg","Background (Bernstein in q)", mass, massd1, massd2, qmin, qmax,
                    RooArgList(coef0, coef1, coef2, coef3));

  RooRealVar sig2bkg("sig2bkg","signal fraction", 0.6, 0., 1.);
  RooAddPdf bern2BW("bern2BW","bern2BW", RooArgList(rel_intBW, bkg), sig2bkg);

  // ---- Write initial parameters BEFORE fitting ----
  ofstream fitLog("/work/halld/home/dbarton/gluex/KShortPipLambda/fitting/plots/plots_rooFit_kStar_fitresult.txt");
  fitLog << "======================================================" << endl;
  fitLog << "  Interfering 2 Relativistic Breit-Wigner + Bernstein" << endl;
  fitLog << "  M(Ks pi+) Fit Results" << endl;
  fitLog << "======================================================" << endl;
  fitLog << endl;
  fitLog << "--- Initial Parameters (starting values) ---" << endl;
  fitLog << Form("  massBW_1   = %.4f  [%.4f, %.4f]", massBW_1.getVal(), massBW_1.getMin(), massBW_1.getMax()) << endl;
  fitLog << Form("  widthBW_1  = %.4f  [%.4f, %.4f]", widthBW_1.getVal(), widthBW_1.getMin(), widthBW_1.getMax()) << endl;
  fitLog << Form("  massBW_2   = %.4f  [%.4f, %.4f]", massBW_2.getVal(), massBW_2.getMin(), massBW_2.getMax()) << endl;
  fitLog << Form("  widthBW_2  = %.4f  [%.4f, %.4f]", widthBW_2.getVal(), widthBW_2.getMin(), widthBW_2.getMax()) << endl;
  fitLog << Form("  scale      = %.4f  [%.4f, %.4f]", scale.getVal(),    scale.getMin(),    scale.getMax())    << endl;
  fitLog << Form("  phase      = %.4f  [%.4f, %.4f]", phase.getVal(),    phase.getMin(),    phase.getMax())    << endl;
  fitLog << Form("  rInt       = %.4f  [%.4f, %.4f]", rInt.getVal(),     rInt.getMin(),     rInt.getMax())     << endl;
  fitLog << Form("  sig2bkg    = %.4f  [%.4f, %.4f]", sig2bkg.getVal(),  sig2bkg.getMin(),  sig2bkg.getMax())  << endl;
  fitLog << Form("  coef0      = %.4f  [%.4f, %.4f]", coef0.getVal(),    coef0.getMin(),    coef0.getMax())    << endl;
  fitLog << Form("  coef1      = %.4f  [%.4f, %.4f]", coef1.getVal(),    coef1.getMin(),    coef1.getMax())    << endl;
  fitLog << Form("  coef2      = %.4f  [%.4f, %.4f]", coef2.getVal(),    coef2.getMin(),    coef2.getMax())    << endl;
  fitLog << Form("  coef3      = %.4f  [%.4f, %.4f]", coef3.getVal(),    coef3.getMin(),    coef3.getMax())    << endl;
  fitLog << endl;

  // ---- Fit ----
  mass.setRange("PWA Fit", 0.61, 2.3);
  RooFitResult* fitResult = bern2BW.fitTo(dataHist_P, Range("PWA Fit"), SumW2Error(true), Save(true));

  // Integrate signal component over K*(892) region (to calculate Figures of Merit)
  mass.setRange("FOM", 0.8, 1.0);
  RooAbsReal* sig_int  = rel_intBW.createIntegral(mass, NormSet(mass), Range("FOM"));
  RooAbsReal* bkg_int  = bkg.createIntegral(mass, NormSet(mass), Range("FOM"));
  RooAbsReal* tot_int  = bern2BW.createIntegral(mass, NormSet(mass), Range("FOM"));

  double S = sig_int->getVal() * sig2bkg.getVal()  * h_Pwave->Integral();
  double B = bkg_int->getVal() * (1-sig2bkg.getVal()) * h_Pwave->Integral();
  double purity = S / (S + B);
  double SoverB = S / B;

  fitLog << "--- Figures of Merit (0.8, 1.0) GeV ---" << endl;
  fitLog << Form("  Signal yield : %.1f", S) << endl;
  fitLog << Form("  Background   : %.1f", B) << endl;
  fitLog << Form("  S/B          : %.3f", SoverB) << endl;
  fitLog << Form("  Purity S/(S+B): %.3f", purity) << endl;

  // Write Figures of Merit to ROOT file for use in other analyses
  TVectorD fom(4);
  fom[0] = S;
  fom[1] = B;
  fom[2] = SoverB;
  fom[3] = purity;

  // ---- Plotting ----
  mass.setRange("PWA Plot", 0.5, 2.5);
  RooPlot* frame_intBW_P = mass.frame();
  frame_intBW_P->GetXaxis()->SetTitle("M[K_{s}#pi^{+}] (GeV)");
  frame_intBW_P->GetYaxis()->SetTitle("Combinations / 25 MeV");
  frame_intBW_P->GetYaxis()->SetTitleOffset(1.1);
  frame_intBW_P->GetYaxis()->SetMaxDigits(3);
  dataHist_P.plotOn(frame_intBW_P);
  bern2BW.plotOn(frame_intBW_P, Range("PWA Plot"));
  bern2BW.plotOn(frame_intBW_P, Components(rel_intBW),
                 LineStyle(kDotted), LineColor(kOrange),   Range("PWA Plot"));
  bern2BW.plotOn(frame_intBW_P, Components(bkg),
                 LineStyle(kDotted), LineColor(kOrange+7), Range("PWA Plot"));


  // Debugging: get names of fit components to export to ROOT file for use in external plotter.
  // // Print all object names stored in the frame
  // TList* items = frame_intBW_P->getObject(0) ? new TList() : new TList();
  // for(int i = 0; i < 100; i++){
  //   TObject* obj = frame_intBW_P->getObject(i);
  //   if(!obj) break;
  //   cout << "  i=" << i << "  Name: " << obj->GetName() << "  Class: " << obj->ClassName() << endl;
  // }

  // ---- Write fit results AFTER fitting ----
  fitLog << "--- Fit Convergence ---" << endl;
  fitLog << Form("  Status     : %d  (%s)", fitResult->status(),
                 fitResult->status() == 0 ? "CONVERGED" : "NOT CONVERGED") << endl;
  fitLog << Form("  Edm        : %.6f", fitResult->edm()) << endl;
  fitLog << Form("  NLL value  : %.6f", fitResult->minNll()) << endl;
  fitLog << Form("  Chi2/NDF   : %.4f", frame_intBW_P->chiSquare()) << endl;
  fitLog << Form("  Num invalid NLL : %d", fitResult->numInvalidNLL()) << endl;
  fitLog << endl;
  fitLog << "--- Fitted Parameters ---" << endl;
  fitLog << Form("  massBW_1   = %.6f +/- %.6f GeV", massBW_1.getVal(), massBW_1.getError()) << endl;
  fitLog << Form("  widthBW_1  = %.6f +/- %.6f GeV", widthBW_1.getVal(), widthBW_1.getError()) << endl;
  fitLog << Form("  massBW_2   = %.6f +/- %.6f GeV", massBW_2.getVal(), massBW_2.getError()) << endl;
  fitLog << Form("  widthBW_2  = %.6f +/- %.6f GeV", widthBW_2.getVal(), widthBW_2.getError()) << endl;
  fitLog << Form("  scale      = %.6f +/- %.6f",      scale.getVal(),   scale.getError())   << endl;
  fitLog << Form("  phase      = %.6f +/- %.6f rad",  phase.getVal(),   phase.getError())   << endl;
  fitLog << Form("  rInt       = %.6f +/- %.6f",      rInt.getVal(),    rInt.getError())    << endl;
  fitLog << Form("  sig2bkg    = %.6f +/- %.6f",      sig2bkg.getVal(), sig2bkg.getError()) << endl;
  fitLog << Form("  coef0      = %.6f +/- %.6f",      coef0.getVal(),   coef0.getError())   << endl;
  fitLog << Form("  coef1      = %.6f +/- %.6f",      coef1.getVal(),   coef1.getError())   << endl;
  fitLog << Form("  coef2      = %.6f +/- %.6f",      coef2.getVal(),   coef2.getError())   << endl;
  fitLog << Form("  coef3      = %.6f +/- %.6f",      coef3.getVal(),   coef3.getError())   << endl;
  fitLog << endl;
  fitLog << "--- PDG Reference Values ---" << endl;
  fitLog << "  K*(892):  mass = 0.89166 GeV,  width = 0.0508 GeV" << endl;
  fitLog << "  K*(1410): mass = 1.421   GeV,  width = 0.236  GeV" << endl;
  fitLog << endl;
  fitLog << "--- Fit Range ---" << endl;
  fitLog << "  M(Ks pi+) in [0.61, 2.3] GeV" << endl;
  fitLog << "======================================================" << endl;
  fitLog.close();
  cout << "Fit log written." << endl;

  // ---- Save fit output to ROOT file for use in other analyses ----
  TGraph* g_total = (TGraph*)frame_intBW_P->findObject("bern2BW_Norm[mass]_Range[PWA Plot]_NormRange[PWA Plot]");
  TGraph* g_sig   = (TGraph*)frame_intBW_P->findObject("bern2BW_Norm[mass]_Comp[rel_intBW]_Range[PWA Plot]_NormRange[PWA Plot]");
  TGraph* g_bkg   = (TGraph*)frame_intBW_P->findObject("bern2BW_Norm[mass]_Comp[bkg]_Range[PWA Plot]_NormRange[PWA Plot]");

  // Warn immediately if not found
  if(g_total) cout << "Found curve_total" << endl;
  else        cout << "WARNING: curve_total not found" << endl;
  if(g_sig)   cout << "Found curve_sig" << endl;
  else        cout << "WARNING: curve_sig not found" << endl;
  if(g_bkg)   cout << "Found curve_bkg" << endl;
  else        cout << "WARNING: curve_bkg not found" << endl;

  TFile* outFile = new TFile("/work/halld/home/dbarton/gluex/KShortPipLambda/fitting/plots/plots_rooFit_kStar.root", "RECREATE");
  h_Pwave->Write();

  // Write as TVectorD pairs -- these are pure ROOT with no RooFit ancestry
  if(g_total){
    int n = g_total->GetN();
    TVectorD vx(n), vy(n);
    for(int i=0; i<n; i++){ vx[i]=g_total->GetX()[i]; vy[i]=g_total->GetY()[i]; }
    vx.Write("curve_total_x"); vy.Write("curve_total_y");
  }
  if(g_sig){
    int n = g_sig->GetN();
    TVectorD vx(n), vy(n);
    for(int i=0; i<n; i++){ vx[i]=g_sig->GetX()[i]; vy[i]=g_sig->GetY()[i]; }
    vx.Write("curve_sig_x"); vy.Write("curve_sig_y");
  }
  if(g_bkg){
    int n = g_bkg->GetN();
    TVectorD vx(n), vy(n);
    for(int i=0; i<n; i++){ vx[i]=g_bkg->GetX()[i]; vy[i]=g_bkg->GetY()[i]; }
    vx.Write("curve_bkg_x"); vy.Write("curve_bkg_y");
  }
  fom.Write("figures_of_merit");
  outFile->Close();

  // ---- Print to PDF ----
  cout << "Chi2/NDF: " << frame_intBW_P->chiSquare() << endl;
  TCanvas* fit_c = new TCanvas("fit","", 1200, 1400);
  frame_intBW_P->Draw();
  fit_c->Print("/work/halld/home/dbarton/gluex/KShortPipLambda/fitting/plots/plots_rooFit_kStar.pdf");
}