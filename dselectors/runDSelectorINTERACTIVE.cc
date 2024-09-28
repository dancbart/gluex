#include <iostream>
#include <fstream>
#include <string>

R__LOAD_LIBRARY(libDSelector.so)
   
void runDSelectorINTERACTIVE(){

gEnv->SetValue("ProofLite.Sandbox", "/w/halld-scshelf2101/home/dbarton/gluex/dselectors/tmp");

//increase the max file size for a output tree //this is optional for VERY LARGE files
TTree::SetMaxTreeSize(2000000000000LL); // 2TB


gROOT->ProcessLine(".x $(ROOT_ANALYSIS_HOME)/scripts/Load_DSelector.C");

TString nameOfTree = "Thrown_Tree"; // if using thrown trees
// TString nameOfTree = "pipkmks__B4_M16_Tree"; // mc tree for Tyler's KKpi analysis, but with the flatte model
// TString nameOfTree = "pi0kplamb__B4_M18_Tree"; // K+ pi- lambda analysis
TChain *chain = new TChain(nameOfTree);

// Add all files together
// chain->Add("/lustre19/expphy/cache/halld/RunPeriod-2018-08/analysis/ver23/tree_pi0kplamb__B4_M18/merged/*.root");

// chain->Add("/lustre19/expphy/cache/halld/RunPeriod-2018-01/analysis/ver24/tree_pi0kplamb__B4_M18/merged/tree_pi0kplamb__B4_M18_04085*");

// chain->Add("/lustre24/expphy/volatile/halld/home/dbarton/root_analysis/MC/KKpi_mc_flatte/root/trees/*.root"); // Tyler's KKpi analysis.  Reconstructed trees

chain->Add("/lustre24/expphy/volatile/halld/home/dbarton/root_analysis/MC/KKpi_mc_flatte/root/thrown/*.root"); // Tyler's KKpi analysis.  Thrown trees

//  DPROOFLiteManager::Process_Chain(chain, "DSelector_KKpiFlatte.C++", 6);
// chain->Add("/lustre19/expphy/cache/halld/RunPeriod-2018-08/analysis/ver23/tree_pi0kplamb__B4_M18/merged/*.root");
DPROOFLiteManager::Process_Chain(chain, "DSelector_KKpi_mcThrown_genamp2.C++", 6);
//  DPROOFLiteManager::Process_Chain(chain, "DSelector_pi0kplamb_flat.C++", 6);
  
  return;
}
