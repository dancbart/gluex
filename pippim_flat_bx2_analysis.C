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

    auto fsCut1 = df2.Filter("pathlength_sig > 0 && pathlength_sig < 10");

    // Create histogram: Occurences ("counts") vs. mass:
    auto h1 = df2.Histo1D({"h1", "Mass of pip2pim", 100, 0.0, 1.0}, "pip2pim_m");
    h1->SetFillColor(kBlue); // Customize the appearance of the histogram
    h1->SetLineWidth(2);
    h1->SetFillColor(kOrange);
    TCanvas* c1 = new TCanvas("Canvas1", "Mass of pip2pim", 800, 600); // Draw the histogram on a canvas
    h1->Draw();
    c1->Update();
    c1->SaveAs("pip2pim_m.png");
    
    // Create 2D plot: pathlength_sig (0 is low confidence, 10 is high) vs. pip2pim_m
    // First argument is mass (x-axis), second argument is pathlength_sig (y-axis)
    auto h2 = df2.Histo2D<TH2D>({"h2", "pathlength_sig vs pip2pim_m", 100, 0.3, 0.7, 100, 0.0, 10.0}, "pip2pim_m", "pathlength_sig");
    h2->SetFillColor(kBlue);
    h2->SetLineWidth(2);
    h2->SetFillColor(kOrange);
    TCanvas* c2 = new TCanvas("Canvas2", "pathlength_sig vs. pip2pim_m", 800, 600);
    h2->Draw("colz");
    c2->Update();
    c2->SaveAs("pathlength_sigVSpip2pim_m.png");
}

int main() {
    pippim_flat_bx2_analysis();
    return 0;
}
