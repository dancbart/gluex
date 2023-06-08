#include <iostream>

void ROOT_hist_beamX4meas_useRDataFrame() {
    // Open the ROOT file containing the data tree of interest:
    //ROOT::RDataFrame will open the file for you.
    //TFile* file = new TFile("pipkmks_flat_bestX2_2017.root");

    // Get the data tree from the file:
    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    auto cut1 = df.Filter("e_beam > 8.0");

    // Create a histogram object and fill it with the data from the column "e_beam":
    // TH1D* h1 = new TH1D("Beam Energy", "Energy (x4 measured)", 10, 1.0, 1.7);
    auto h1 = cut1.Histo1D("e_beam");
    // h1 = df.Histo1D("e_beam").GetValue();

    // Customize the appearance of the histogram:
    h1->SetFillColor(kBlue);
    h1->SetLineWidth(2);
    h1->SetFillColor(kOrange);
    // h1->GetYaxis()->SetRangeUser(0.0, 1.0);

    // Draw the histogram on a canvas:
    TCanvas* c1 = new TCanvas("Canvas", "Canvas: Beam Energy", 800, 600);
    h1->Draw();
    c1->Update();
    c1->SaveAs("beamX4meas.png");
    c1->SaveAs("beamX4meas.pdf");
    c1->SaveAs("beamX4meas.root");

    // Close the ROOT file:
//  file->Close();
}

int main() {
    ROOT_hist_beamX4meas_useRDataFrame();
    return 0;
}
