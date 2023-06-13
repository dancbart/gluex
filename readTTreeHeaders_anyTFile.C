//Use this script to read headers for any root file.  Replace 'file' & 'tree' names below.
#include <TFile.h>
#include <TTree.h>
#include <iostream>

void ROOT_readHeaders_anyFile() {

    std::string fileName = "pipkmks_flat_bestX2_2017.root";
    std::string treeName = "pipkmks__B4_M16";
    ROOT::RDataFrame df(treeName, fileName);
//    cout<<df.GetColumnNames()<<endl;

const auto& columnNames = df.GetColumnNames();
    for (const auto& columnName : columnNames) {
    cout << columnName << endl;
}

}

int main() {
    ROOT_readHeaders_anyFile();
    return 0;
}
