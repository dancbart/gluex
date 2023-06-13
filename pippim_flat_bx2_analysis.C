//This method uses RDataFrames, instead of reading directly from ROOT file with TTrees method.
#include <iostream>
#include <ROOT/RDataFrame.hxx>
#include <TH1.h>
#include <TCanvas.h>

void pippim_flat_bx2_analysis() {
    // Open the ROOT file containing the data tree of interest
    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    // Define new RDataFrame 'df2' from 'df', then add columns (using '.Define')
    auto df2 = df.Define("pip2pim_E", "pip2_E + pim_E")
                 .Define("pip2pim_px", "pip2_px + pim_px")
                 .Define("pip2pim_py", "pip2_py + pim_py")
                 .Define("pip2pim_pz", "pip2_pz + pim_pz")
                 .Define("pip2pim_m", "sqrt(pip2pim_E*pip2pim_E - pip2pim_px*pip2pim_px - pip2pim_py*pip2pim_py - pip2pim_pz*pip2pim_pz)");

    auto h1 = df2.Histo1D({"h1", "Mass of pip2pim", 100, 0.0, 1.0}, "pip2pim_m");
    auto h2 = df2.Filter("pathlength_sig > 1").Histo1D({"h2", "title2", 100, 0.3, 0.75}, "pip2pim_m");
    auto h3 = df2.Filter("pathlength_sig > 3").Histo1D({"h3", "title3", 100, 0.3, 0.75}, "pip2pim_m");
    auto h4 = df2.Filter("pathlength_sig > 5").Histo1D({"h4", "title4", 100, 0.3, 0.75}, "pip2pim_m");

    TCanvas* c1 = new TCanvas("Canvas1", "pip2pim_flightSig", 800, 600); // Draw the histogram on a canvas
    // h1->SetLineColor(kBlue);
    // h1->Draw();
    h2->SetLineColor(kBlue);
    h2->Draw("SAME");
    h3->SetLineColor(kGreen);
    h3->Draw("SAME");
    h4->SetLineColor(kRed);
    h4->Draw("SAME");
    c1->Update();
    c1->SaveAs("pip2pim_m.png");
    

}

int main() {
    pippim_flat_bx2_analysis();
    return 0;
}
