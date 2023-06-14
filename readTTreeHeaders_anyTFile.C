//Use this script to read headers for any root file.  Replace 'file' & 'tree' names below.
// #include <TFile.h>
// #include <TTree.h>
// #include <iostream>

void readTTreeHeaders_anyTFile() {

    std::string fileName = "pipkmks_flat_bestX2_2017.root";
    std::string treeName = "pipkmks__B4_M16";
    ROOT::RDataFrame df(treeName, fileName);

// const auto& columnNames = df.GetColumnNames();
//     for (const auto& columnName : columnNames) {
//     cout << columnName << endl;

auto h1 = df.Histo1D({"h1", "e_beam", 100, 0.0, 14.0}, "e_beam");

    TCanvas* c1 = new TCanvas("Canvas1", "e_beam", 800, 600);
    h1->SetLineColor(kGreen);
    h1->Draw();
    
    auto legend = new TLegend(0.77, 0.68, .98, 0.76);
    legend->AddEntry("h1", "e_beam", "l");
    legend->Draw();

    c1->Update();
    c1->SaveAs("e_beam.png");

}

int main() {
    readTTreeHeaders_anyTFile();
    return 0;
}
