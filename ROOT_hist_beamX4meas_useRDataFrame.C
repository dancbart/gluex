#include <iostream>
#include <ROOT/RDataFrame.hxx>
#include <TH1.h>
#include <TCanvas.h>

void ROOT_hist_beamX4meas_useRDataFrame() {
    // Open the ROOT file containing the data tree of interest
    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    // Create a new RDataFrame object for applying column transformations
    auto df2 = df.Define("pip2pim_E", "pip2_E + pim_E")
                 .Define("pip2pim_px", "pip2_px + pim_px")
                 .Define("pip2pim_py", "pip2_py + pim_py")
                 .Define("pip2pim_pz", "pip2_pz + pim_pz")
                 .Define("pip2pim_m", "sqrt(pip2pim_E*pip2pim_E - pip2pim_px*pip2pim_px - pip2pim_py*pip2pim_py - pip2pim_pz*pip2pim_pz)");

    // Create a histogram object and fill it with the data from the column "pip2pim_m2"
    auto h1 = df2.Histo1D({"h1", "Mass of pip2pim", 100, 0.0, 1.0}, "pip2pim_m");

    // Customize the appearance of the histogram
    h1->SetFillColor(kBlue);
    h1->SetLineWidth(2);
    h1->SetFillColor(kOrange);
    // h1->GetYaxis()->SetRangeUser(0.0, 1.0);

    // Draw the histogram on a canvas
    TCanvas* c1 = new TCanvas("Canvas", "Mass", 800, 600);
    h1->Draw();
    c1->Update();
    c1->SaveAs("pip2pim_m.png");
    c1->SaveAs("pip2pim_m.root");
}

int main() {
    ROOT_hist_beamX4meas_useRDataFrame();
    return 0;
}
