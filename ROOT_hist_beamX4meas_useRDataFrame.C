#include <iostream>

void ROOT_hist_beamX4meas_useRDataFrame() {
    // Open the ROOT file containing the data tree of interest:
    //ROOT::RDataFrame will open the file for you.
    //TFile* file = new TFile("pipkmks_flat_bestX2_2017.root");

    // Get the data tree from the file:
    auto df = ROOT::RDataFrame("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    auto df = df.Define("pip2pim_E", "pip2_E + pim_E");
    auto df = df.Define("pip2pim_px", "pip2_px + pim_px");
    auto df = df.Define("pip2pim_py", "pip2_py + pim_py");
    auto df = df.Define("pip2pim_pz", "pip2_pz + pim_pz");

    auto df = df.Define("pip2pim_m2", "pip2pim_E*pip2pim_E - pip2pim_px*pip2pim_px - pip2pim_py*pip2pim_py - pip2pim_pz*pip2pim_pz");

    auto df = df.Filter("e_beam > 6.0 && e_beam < 10.0");

    // Create a histogram object and fill it with the data from the column "pip2pim_m2":
    auto h1 = df.Histo1D("pip2pim_m2");

    // Customize the appearance of the histogram:
    h1->SetFillColor(kBlue);
    h1->SetLineWidth(2);
    h1->SetFillColor(kOrange);
    // h1->GetYaxis()->SetRangeUser(0.0, 1.0);

    // Draw the histogram on a canvas:
    TCanvas* c1 = new TCanvas("Canvas", "Canvas: Beam Energy", 800, 600);
    h1->Draw();
    c1->Update();
    c1->SaveAs("pip2pim_m2.png");
    c1->SaveAs("pip2pim_m2.root");

    // Close the ROOT file:
//  file->Close();
}

int main() {
    ROOT_hist_beamX4meas_useRDataFrame();
    return 0;
}
