// Basic pLots for flattened DATA trees:
#include "gluex_style.h"

// TString fileName ("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root");
TString fileName ("/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_small.root");
TString treeName("ntFSGlueX_MODECODE");

// INDICES ASSIGNED BY 'flatten':
// 1. DecayingLambda (0)   1a. Proton (1)   1b. PiMinus2 (2)
// 2. DecayingKShort (3)   2a. PiPlus2 (4)   2b. PiMinus1 (5)
// 3. PiPlus1 (6)

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

void plots_basic(){

  gluex_style();
  setup();

  TCanvas* c1 = new TCanvas("c1","c1",1200,800);
  TH1F* h1 = FSModeHistogram::getTH1F(fileName, treeName, "m100000000_1100", "MASS(2)", "(80, 0.3, 0.7)", "CUT(chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,rf)");
  h1->SetTitle("test");
  h1->SetXTitle("MASS(2)");
  h1->SetYTitle("Counts");
  h1->SetLineColor(kRed);
  h1->Draw("hist");
  //c1->Update();
  //c1->Show();

  // toggle off 'Show()' above and toggle on below to show plots with evince
  gROOT->SetBatch(kTRUE); // turns off XQuartz display
  TString plotName = "../plots/testPlotting.pdf";
  c1->SaveAs(plotName);
  TString cmd = "evince ";
  cmd += plotName; 
  gSystem->Exec(cmd);
  

  // FSHistogram::dumpHistogramCache();
}

// Runs above analysis:
int main() {
    plots_basic();
    return 0;
}
