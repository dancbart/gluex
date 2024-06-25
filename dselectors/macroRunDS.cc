#include <iostream>
#include <fstream>
#include <string>

R__LOAD_LIBRARY(libDSelector.so)
   
void macroRunDS(){

gEnv->SetValue("ProofLite.Sandbox", "/w/halld-scshelf2101/home/dbarton/gluex/dselectors/tmp");

//increase the max file size for a output tree //this is optional for VERY LARGE files
TTree::SetMaxTreeSize(2000000000000LL); // 2TB


gROOT->ProcessLine(".x $(ROOT_ANALYSIS_HOME)/scripts/Load_DSelector.C");

//TString nameOfTree = "Thrown_Tree"; // for if using Thrown Trees,  is it caps????
TString nameOfTree = "pipkmks__B4_M16_Tree"; 
TChain *chain = new TChain(nameOfTree);

//All File
// chain->Add( "/cache/halld/gluex_simulations/REQUESTED_MC/ebarriga_phasespace_omegaEta_spring_2018_genr8_20220701062744am/root/trees/tree_pi0pippimeta__B4_M7_M17_genr8_04*");
 chain->Add( "/lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/dbarton_MC_v1_pipkmks_genr8_2017_01_anaVer50_3837/trees/tree_pipkmks__B4_M16_genr8/tree_pipkmks__B4_M16_genr8_*" );

 DPROOFLiteManager::Process_Chain(chain, "DSelector_KKpi_mc_v1.C++", 6);
 // there is an option to add a custom name for the Tree output name, look it up!
  
  return;
}
