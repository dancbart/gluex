#include "gluex_style.h"

// Pots for flattened DATA trees:

// TString fileName ("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root");
TString fileName ("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_small.root");
TString treeName("ntFSGlueX_100000000_1100");

inline TString mand_t0(const TString& I, const TString& J) {
    return "MASS2(" + I + "," + J + ") - 2*(ENERGY(" + I + ")*ENERGY(" + J + ") - MOMENTUM(" + I + ")*MOMENTUM(" + J + "))";
}

void setup() {

  const TString DecayingLambda = "1";
  const TString Proton = "1a";
  const TString PiMinus2 = "1b";
  const TString DecayingKShort = "2";
  const TString PiPlus2 = "2a";
  const TString PiMinus1 = "2b";
  const TString PiPlus1 = "3";
  const TString NegOne = "-1.*";    
  
  FSCut::defineCut("flightSigLambda", "VeeLP1>5.0");
  FSCut::defineCut("flightSigKShort", "VeeLP2>5.0");
  FSCut::defineCut("chi2DOF", "Chi2DOF", "0.0", "3.0");
  FSCut::defineCut("unusedE", "EnUnusedSh", "0.0", "0.1");
  FSCut::defineCut("unusedTracks", "NumUnusedTracks<1");
  FSCut::defineCut("coherentPeak", "EnPB", "8.2", "8.8");
  FSCut::defineCut("constrainLambda", "MASS(" + Proton + "," + PiMinus2 + ")", "1.1", "1.132", "1.08", "1.1", "1.132", "1.22");
  FSCut::defineCut("constrainKShort", "MASS(" + DecayingKShort + ")", "0.49", "0.51", "0.0", "0.49", "0.51", "1.0");
  FSCut::defineCut("constrainKSTAR892", "MASS(" + DecayingKShort + "," + PiPlus1 + ")", "0.85", "0.95", "0.0", "0.85", "0.95", "1.0");
  FSCut::defineCut("constrainKSTAR1430", "MASS(" + DecayingKShort + "," + PiPlus1 + ")", "0.85", "0.95", "0.0", "0.85", "0.95", "1.0");
  
  // 1D VARIABLES
  const TString mand_t     = NegOne + "MASS2(GLUEXTARGET,-" + DecayingLambda + ")";
  const TString mand_t_k   = NegOne + "MASS2(GLUEXBEAM,-" + DecayingKShort + ")";
  const TString mand_t_pi  = NegOne + "MASS2(GLUEXBEAM,-" + PiPlus1 + ")";
  const TString mand_t_kpi = NegOne + "MASS2(GLUEXBEAM,-" + DecayingKShort + ",-" + PiPlus1 + ")";
  
  const TString mand_tPrime     = mand_t     + " - (" + mand_t0("GLUEXTARGET", DecayingLambda) + ")";
  const TString mand_tPrime_k   = mand_t_k   + " - (" + mand_t0("GLUEXBEAM", DecayingKShort) + ")";
  const TString mand_tPrime_pi  = mand_t_pi  + " - (" + mand_t0("GLUEXBEAM", PiPlus1) + ")";
  const TString mand_tPrime_kpi = mand_t_kpi + " - (" + mand_t0(DecayingKShort, PiPlus1) + ")";
  
  // 2D VARIABLES
  const TString mand_t_kVSkpi = mand_t_k + ":" + mand_t_kpi;
  const TString mand_t_piVSkpi = mand_t_pi + ":" + mand_t_kpi;
  
  const TString mand_t0_kVSkpi = mand_t_k + ":" + mand_t_kpi;
  const TString mand_t0_piVSkpi = mand_t_pi + ":" + mand_t_kpi;
  
  const TString mand_tPrime_kVSkpi = mand_t_k + ":" + mand_t_kpi;
  const TString mand_tPrime_piVSkpi = mand_t_pi + ":" + mand_t_kpi;
  
}

void mand_t_plots(){

  setup();
  gluex_style();

  TCanvas* c1 = new TCanvas("c1","c1",1200,800);
  TH2F* h1 = FSHistogram::getTH2F(fileName, treeName, mand_t_kVSkpi, "(100, 0.0, 1.0, 100, 0.0, 1.0)", "CUT()");
  h1->SetTitle("mand_t_k vs mand_t_kpi");
  h1->GetXaxis()->SetTitle("t_{K_{S}#pi^{+}}");  
  h1->GetYaxis()->SetTitle("t_{K_{S}}");
  h1->SetLineColor(kRed);
  h1->Draw("colz");

  gROOT->SetBatch(kTRUE); // Batch mode on (disables XQuartz display)
  TString plotName = "../plots/test-CPP-plotting.pdf";
  c1->SaveAs(plotName);
  TString cmd = "evince "; // Display using evince, nice pdf viewer
  cmd += plotName; 
  gSystem->Exec(cmd);
  

}

// Runs above analysis:
int main() {
    mand_t_plots();
    return 0;
}
