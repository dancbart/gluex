//Include necessary ROOT headers in c++ script:
#include <TFile.h>
#include <TTree.h>
#include <iostream>
#include <TH1F.h>
#include <TCanvas.h>

//Open the ROOT file containing the data tree of interest:
TFile* file = new TFile("pipkmks_flat_bestX2_2017.root");

//Get the data tree from the file:
TTree* tree = (TTree*)file->Get("pipkmks__B4_M16");

void ROOT_hist_beamX4meas() {

    //Create a histogram object and draw the data tree variable "e_beam" into it:
    TH1F* h1 = new TH1F("Beam Energy", "Energy (x4 measured)", 10, 1.0, 1.7);

    //Fill the histogram from the data tree (e.g. "e_beam"):
    tree->Draw("e_beam>>Beam Energy");

    //Customize appearance of the histogram:
    h1->SetFillColor(kBlue);
    h1->SetLineWidth(20);
    h1->SetFillColor(kOrange);
    //Set the y-axis range:
    h1->GetYaxis()->SetRangeUser(0.0, 1.0);

    //Draw the histogram on a canvas:
    TCanvas* c1 = new TCanvas("Canvas", "Canvas: Beam Energy", 800, 600);
    //h1->GetXaxis()->SetRangeUser(min_value, max_value);
    h1->Draw();
    c1->Update();
    c1->SaveAs("beamX4meas.png"); //Save the canvas as a PNG file
    c1->SaveAs("beamX4meas.pdf");
    c1->SaveAs("beamX4meas.root");

//Close the ROOT file:
    file->Close();

}

// int main() {
//     ROOT_hist_beamX4meas(); //Call the function.  Without this line, the function 'ROOT_hist_beamX4meas' gets called twice for some reason.
//     return 0;
// }