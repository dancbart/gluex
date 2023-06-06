#include <TFile.h>
#include <TTree.h>
#include <iostream>

void ROOT_read_headers() {

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
    ROOT_read_headers();
    return 0;
}
