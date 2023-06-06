//Include necessary ROOT headers in c++ script:
#include <TFile.h>
#include <TTree.h>
#include <iostream>
#include <TH1F.h>
#include <TCanvas.h>
#include <TH1D.h>
#include <RDataFrame.h>

void createHistogram() {
  // Open the ROOT file
  ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

  // Define the variable and binning for the histogram
  std::string variable = "e_beam";  // Replace with the actual variable name
  int numBins = 100;  // Number of bins
  double binMin = 0.0;  // Minimum value of the bins
  double binMax = 10.0;  // Maximum value of the bins

  // Create the histogram using RDataFrame
  auto hist = df.Histo1D({variable.c_str(), variable.c_str(), numBins, binMin, binMax}, variable.c_str());

  // Create a canvas to display the histogram
  ROOT::TCanvas canvas("canvas", "Histogram", 800, 600);

  // Draw the histogram on the canvas
  hist->Draw();

  // Save the canvas as an image file
  canvas.SaveAs("histogram.png");
}

int main() {
  createHistogram();
  return 0;
}