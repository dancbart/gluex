void pipkmks_flat_bx2_analysis() {
    // Open the ROOT file containing the data tree of interest
    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    // Define new RDataFrame 'df2' from 'df', then add columns (using '.Define')
    auto df2 = df
                 // k_short (pip2 & pim)
                 .Define("pip2pim_E", "pip2_E + pim_E") // 4-momentum
                    .Alias("ks_E", "pip2pim_E")
                 .Define("pip2pim_px", "pip2_px + pim_px")
                    .Alias("ks_px", "pip2pim_px")
                 .Define("pip2pim_py", "pip2_py + pim_py")
                    .Alias("ks_py", "pip2pim_py")
                 .Define("pip2pim_pz", "pip2_pz + pim_pz")
                    .Alias("ks_pz", "pip2pim_pz")
                 // total mass:
                 .Define("pip2pim_m", "sqrt(pip2pim_E*pip2pim_E - pip2pim_px*pip2pim_px - pip2pim_py*pip2pim_py - pip2pim_pz*pip2pim_pz)")
                    .Alias("ks_m", "pip2pim_m")
                 
                 // delta++ (pip1 & proton')
                 .Define("pip1p_E", "pip1_E + p_E")  // 4-momentum
                 .Define("pip1p_px", "pip1_px + p_px")
                 .Define("pip1p_py", "pip1_py + p_py")
                 .Define("pip1p_pz", "pip1_pz + p_pz")
                 // total mass
                 .Define("pip1p_m", "sqrt(pip1p_E*pip1p_E - pip1p_px*pip1p_px - pip1p_py*pip1p_py - pip1p_pz*pip1p_pz)")
                 
                 // lambda (proton' & k_minus -- 1500, 1900?)
                 .Define("pkm_E", "p_E + km_E") // 4-momentum
                 .Define("pkm_px", "p_px + km_px")
                 .Define("pkm_py", "p_py + km_py")
                 .Define("pkm_pz", "p_pz + km_pz")
                 // total mass:
                 .Define("pkm_m" , "sqrt(pkm_E*pkm_E - pkm_px*pkm_px - pkm_py*pkm_py - pkm_pz*pkm_pz)")

                 // k_minus * pip1
                 .Define("kmpip1_E", "km_E + pip1_E") // 4-momentum
                 .Define("kmpip1_px", "km_px + pip1_px")
                 .Define("kmpip1_py", "km_py + pip1_py")
                 .Define("kmpip1_pz", "km_pz + pip1_pz")
                 // total mass:
                 .Define("kmpip1_m", "sqrt(kmpip1_E*kmpip1_E - kmpip1_px*kmpip1_px - kmpip1_py*kmpip1_py - kmpip1_pz*kmpip1_pz)")

                 // k_short & pip1
                 .Define("kspip1_E", "ks_E + pip1_E") // 4-momentum
                 .Define("kspip1_px", "ks_px + pip1_px")
                 .Define("kspip1_py", "ks_py + pip1_py")
                 .Define("kspip1_pz", "ks_pz + pip1_pz")
                 // total mass:
                 .Define("kspip1_m", "sqrt(kspip1_E*kspip1_E - kspip1_px*kspip1_px - kspip1_py*kspip1_py - kspip1_pz*kspip1_pz)")

                 // f1 (pip1 & km & ks[pip2 + pim])
                 .Define("pipkmks_E", "pip1_E + km_E + ks_E") // 4-momentum
                     .Alias("f1_E", "pipkmks_E")
                 .Define("pipkmks_px", "pip1_px + km_px + ks_px")
                     .Alias("f1_px", "pipkmks_px")
                 .Define("pipkmks_py", "pip1_py + km_py + ks_py")
                     .Alias("f1_py", "pipkmks_py")
                 .Define("pipkmks_pz", "pip1_pz + km_pz + ks_pz")
                     .Alias("f1_pz", "pipkmks_pz")
                 // total mass:
                 .Define("pipkmks_m", "sqrt(pipkmks_E*pipkmks_E - pipkmks_px*pipkmks_px - pipkmks_py*pipkmks_py - pipkmks_pz*pipkmks_pz)")
                     .Alias("f1_m", "pipkmks_m");

    auto cut_df = df2.Filter("pathlength_sig > 5")
                     .Filter("pip1p_m > 1.4") // delta++ cut
                     .Filter("pkm_m > 1.9") // lambda cut (1500, 1900?)
                     .Filter("kspip1_m > 1.1") // kspip1 cut
                     .Filter("kmpip1_m > 1.1"); // kmpip1 cut

    // Histogram - use for investigating various resonances to reject (cut)
    //auto h1 = df2.Histo1D({"h1", "kmpip1_m", 100, 0.0, 3.0}, "kmpip1_m");
    
    //Histogram with cuts
    auto h1 = cut_df.Histo1D({"h1", "f1", 100, 0.8, 3.8}, "f1_m");
    auto h2 = df2.Histo1D({"h2", "f1", 100, 0.8, 3.8}, "f1_m");

    TCanvas* c1 = new TCanvas("Canvas1", "f1_m", 800, 600); // Draw the histogram on a canvas
    h1->SetLineColor(kGreen);
    h1->Draw();
    h2->SetLineColor(kRed);
    h2->Draw("same");
    
    auto legend1 = new TLegend(0.77, 0.68, .98, 0.76);
    legend1->AddEntry("h1", "f1_m with cuts", "l");
    legend1->AddEntry("h2", "f1_m without cuts", "l");
    legend1->Draw();

    c1->Update();
    c1->SaveAs("plots/f1_m.png");
}

int main() {
    pipkmks_flat_bx2_analysis();
    return 0;
}
