//Include necessary ROOT headers in c++ script:
#include <TFile.h>
#include <TTree.h>
#include <iostream>
#include <TH1F.h>
#include <TCanvas.h>
#include <TH1D.h>
//#include <RDataFrame.h>

#include <ROOT/RDataFrame.hxx>
#include <TFile.h>
#include <TCanvas.h>
#include <TH1F.h>

void ROOT_hist_beamX4meas() {
    // Open the ROOT file containing the data tree of interest:
    TFile* file = new TFile("pipkmks_flat_bestX2_2017.root");

    // Get the data tree from the file:
    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    // Create a histogram object and fill it with the data from the column "e_beam":
    TH1F* h1 = new TH1F("Beam Energy", "Energy (x4 measured)", 10, 1.0, 1.7);
    df.Histo1D<float>(h1, "e_beam");

    // Customize the appearance of the histogram:
    h1->SetFillColor(kBlue);
    h1->SetLineWidth(20);
    h1->SetFillColor(kOrange);
    h1->GetYaxis()->SetRangeUser(0.0, 1.0);

    // Draw the histogram on a canvas:
    TCanvas* c1 = new TCanvas("Canvas", "Canvas: Beam Energy", 800, 600);
    h1->Draw();
    c1->Update();
    c1->SaveAs("beamX4meas.png");
    c1->SaveAs("beamX4meas.pdf");
    c1->SaveAs("beamX4meas.root");

    // Close the ROOT file:
    file->Close();
}

int main() {
    ROOT_hist_beamX4meas();
    return 0;
}
