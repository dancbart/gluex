#include <iostream>
#include <fstream>
#include <string>

R__LOAD_LIBRARY(libDSelector.so)
   
void runFSFlattenINTERACTIVE(){

gEnv->SetValue("ProofLite.Sandbox", "/w/halld-scshelf2101/home/dbarton/gluex/dselectors/tmp");

//increase the max file size for a output tree //this is optional for VERY LARGE files
TTree::SetMaxTreeSize(2000000000000LL); // 2TB


gROOT->ProcessLine(".x $(ROOT_ANALYSIS_HOME)/scripts/Load_DSelector.C");

// TString nameOfTree = "Thrown_Tree"; // if using thrown trees
TString nameOfTree = "ntFSGlueX_100000000_100001"; // K+ pi0 lambda analysis
TChain *chain = new TChain(nameOfTree);

// Add all files together
chain->Add("/lustre24/expphy/cache/halld/RunPeriod-2018-08/analysis/ver23/tree_pi0kplamb__B4_M18/merged/tree_pi0kplamb__B4_M18_05174*.root");

//  DPROOFLiteManager::Process_Chain(chain, "DSelector_KKpiFlatte.C++", 6);
DPROOFLiteManager::Process_Chain(chain, "DSelector_pi0kplamb_flat.C++", 6);
  
  return;
}
