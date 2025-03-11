//Use this script to read headers for any root file.  Replace 'file' & 'tree' names below.
// #include <TFile.h>
// #include <TTree.h>
// #include <iostream>
// #include <fstream>  // Include for file operations

// void readTTreeHeaders_anyTFile() {

//     std::string fileName = "pipkmks_flat_bestX2_2017.root";
//     std::string treeName = "pipkmks__B4_M16";
//     ROOT::RDataFrame df(treeName, fileName);

// const auto& columnNames = df.GetColumnNames();
//     for (const auto& columnName : columnNames) {
//     cout << columnName << endl;

#include <iostream>

int main() {
    // This call would trigger a squiggle if IntelliSense doesn't know the FSRoot namespace
    // (i.e., there's no header or forward declaration for FSRoot::DoSomething)
    FSRoot::DoSomething();

    std::cout << "Hello from main!\n";
    return 0;
}

void FSRoot_test {
    ROOT::RDataFramee df("ntFSGlueX_100000000_1100", "/w/halld-scshelf2101/home/dbarton/gluex/files/data/pipkslamb/tree_pipkslamb__B4_M16_M18_FSflat.root");
}

void FSRoot_test() {

    // Open a file for reading
    std::string fileName = "/w/halld-scshelf2101/home/dbarton/gluex/files/data/pipkslamb/tree_pipkslamb__B4_M16_M18_FSflat.root";
    std::string treeName = "ntFSGlueX_100000000_1100";
    ROOT::RDataFrame df(treeName, fileName);

    // ROOT::FSCut::defineCut("chi2","Chi2DOF","0.0","3.0")
    ROOT::FSCut::defineMything("chi2","Chi2DOF","0.0","3.0")



    // // Write output to terminal
    // const auto& columnNames = df.GetColumnNames();
    // for (const auto& columnName : columnNames) {
    // cout << columnName << endl;

    // Write output to file
    const auto& columnNames = df.GetColumnNames();
    std::ofstream outFile("treeHeaders.txt");  // Open a file for writing
    for (const auto& columnName : columnNames) {
        outFile << columnName << std::endl;  // Write to the file instead of cout
    }
    outFile.close();  // Close the file
}


// auto h1 = df.Histo1D({"h1", "e_beam", 100, 0.0, 14.0}, "e_beam");

//     TCanvas* c1 = new TCanvas("Canvas1", "e_beam", 800, 600);
//     h1->SetLineColor(kGreen);
//     h1->Draw();
    
//     auto legend = new TLegend(0.77, 0.68, .98, 0.76);
//     legend->AddEntry("h1", "e_beam", "l");
//     legend->Draw();

//     c1->Update();
//     c1->SaveAs("e_beam.png");

// }

// int main() {
//     readTTreeHeaders_anyTFile();
//     return 0;
// }
