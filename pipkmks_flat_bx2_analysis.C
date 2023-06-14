void pipkmks_flat_bx2_analysis() {
    // Open the ROOT file containing the data tree of interest
    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    // Define new RDataFrame 'df2' from 'df', then add columns (using '.Define')
    auto df2 = df.Define("pip2pim_E", "pip2_E + pim_E") //pi+2 and pim 4-momentum
                 .Define("pip2pim_px", "pip2_px + pim_px")
                 .Define("pip2pim_py", "pip2_py + pim_py")
                 .Define("pip2pim_pz", "pip2_pz + pim_pz")
                 .Define("pip2pim_m", "sqrt(pip2pim_E*pip2pim_E - pip2pim_px*pip2pim_px - pip2pim_py*pip2pim_py - pip2pim_pz*pip2pim_pz)")
                 .Define("pip1p_E", "pip1_E + p_E")  //pi+1 and proton 4-momentum
                 .Define("pip1p_px", "pip1_px + p_px")
                 .Define("pip1p_py", "pip1_py + p_py")
                 .Define("pip1p_pz", "pip1_pz + p_pz")
                 .Define("pip1p_m", "sqrt(pip1p_E*pip1p_E - pip1p_px*pip1p_px - pip1p_py*pip1p_py - pip1p_pz*pip1p_pz)");

    auto h1 = df2.Histo1D({"h1", "pip2pim & pip1p masses", 100, 0.0, 2.0}, "pip2pim_m");
    auto h2 = df2.Histo1D({"h2", "pip2pim & pip1p masses", 100, 0.0, 2.2}, "pip1p_m");

    TCanvas* c1 = new TCanvas("Canvas1", "pip1p_m", 800, 600); // Draw the histogram on a canvas
    h1->SetLineColor(kBlue);
    h1->Draw();
    h2->SetLineColor(kGreen);
    h2->Draw("SAME");
    c1->Update();
    c1->SaveAs("pip1p_m.png");
    

}

int main() {
    pipkmks_flat_bx2_analysis();
    return 0;
}
