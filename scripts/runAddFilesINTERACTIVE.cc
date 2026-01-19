#include <iostream>
#include <fstream>
#include <string>

void runAddFilesINTERACTIVE(){

gEnv->SetValue("ProofLite.Sandbox", "/w/halld-scshelf2101/home/dbarton/gluex/files/tmp");

//increase the max file size for a output tree //this is optional for VERY LARGE files
TTree::SetMaxTreeSize(2000000000000LL); // 2TB

// TString nameOfTree = "Thrown_Tree"; // if using thrown trees
TString nameOfTree = "ntFSGlueX_100000000_100001"; // K+ pi0 lambda analysis
TChain *chain = new TChain(nameOfTree);

// Combine files
chain->Add("/lustre24/expphy/volatile/halld/home/dbarton/pi0kplamb/flatten/*.root");

// Create TChain with all input files
TChain chain("myTreeName");
chain.Add("your_input_files*.root");

// Write out merged file
chain.Merge("merged.root");


//  DPROOFLiteManager::Process_Chain(chain, "DSelector_KKpiFlatte.C++", 6);
DPROOFLiteManager::Process_Chain(chain, "someScript.C++", 6);
  
  return;
}
