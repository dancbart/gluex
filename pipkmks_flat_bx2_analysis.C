void pipkmks_flat_bx2_analysis() {
    // Open the ROOT file containing the data tree of interest
    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    // Define new RDataFrame 'df2' from 'df', then add columns (using '.Define')
    auto df2 = df.Define("pip2pim_E", "pip2_E + pim_E") // ks (aka k_short; pip2 & pim) 4-momentum
                    .Alias("ks_E", "pip2pim_E")
                 .Define("pip2pim_px", "pip2_px + pim_px")
                    .Alias("ks_px", "pip2pim_px")
                 .Define("pip2pim_py", "pip2_py + pim_py")
                    .Alias("ks_py", "pip2pim_py")
                 .Define("pip2pim_pz", "pip2_pz + pim_pz")
                    .Alias("ks_pz", "pip2pim_pz")
                 // ks (aka k_short; pip2 & pim) total mass:
                 .Define("pip2pim_m", "sqrt(pip2pim_E*pip2pim_E - pip2pim_px*pip2pim_px - pip2pim_py*pip2pim_py - pip2pim_pz*pip2pim_pz)")
                    .Alias("ks_m", "pip2pim_m")
                 
                 .Define("pip1p_E", "pip1_E + p_E")  // pip1 & proton 4-momentum
                 .Define("pip1p_px", "pip1_px + p_px")
                 .Define("pip1p_py", "pip1_py + p_py")
                 .Define("pip1p_pz", "pip1_pz + p_pz")
                 // pip1 & proton total mass:
                 .Define("pip1p_m", "sqrt(pip1p_E*pip1p_E - pip1p_px*pip1p_px - pip1p_py*pip1p_py - pip1p_pz*pip1p_pz)")
                 
                 .Define("pkm_E", "p_E + km_E") // proton & k_minus 4-momentum
                 .Define("pkm_px", "p_px + km_px")
                 .Define("pkm_py", "p_py + km_py")
                 .Define("pkm_pz", "p_pz + km_pz")
                 // Proton and k_minus total mass:
                 .Define("pkm_m" , "sqrt(pkm_E*pkm_E - pkm_px*pkm_px - pkm_py*pkm_py - pkm_pz*pkm_pz)")

                .Define("pipkmks_E", "pip1_E + km_E + ks_E")
                .Define("pipkmks_px", "pip1_px + km_px + ks_px")
                .Define("pipkmks_py", "pip1_py + km_py + ks_py")
                .Define("pipkmks_pz", "pip1_pz + km_pz + ks_pz")
                .Define("pipkmks_m", "sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)");

    auto cut_df = df2.Filter("pathlength_sig > 3")
                     .Filter("pip1p_m > 1.4")
                     .Filter("pkm_m > 1.9");

    auto h1 = cut_df.Histo1D({"h2", "pipkmks_m fs", 100, 1.0, 2.0}, "pipkmks_m");

    TCanvas* c1 = new TCanvas("Canvas1", "pipkmks_m", 800, 600); // Draw the histogram on a canvas
    h1->SetLineColor(kGreen);
    h1->Draw();
    
    auto legend1 = new TLegend(0.77, 0.68, .98, 0.76);
    legend1->AddEntry("h1", "with cuts - pipkmks_m", "l");
    legend1->Draw();

    c1->Update();
    c1->SaveAs("pipkmks_fs_m.png");
}

int main() {
    pipkmks_flat_bx2_analysis();
    return 0;
}
