// Description: Analysis of f1(1285) resonance in flat bx2 data.

void f1_flat_bx2_analysis() {

    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

   
   // ********** DEFINITIONS **********

    // Define resonances; add columns to dataframe for each....using '.Define' method
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

    
    
    // ********** CUTS **********
    
    auto reject_delta = "pip1p_m > 1.4"; // delta++ cut
    auto reject_lambda = "pkm_m > 1.9"; // lambda cut
    auto keep_kstar_plus = "kspip1_m >= 0.8 && kspip1_m <= 1.0"; // aka "charged" K*(KsPi+)
    auto keep_kstar_zero = "kmpip1_m >= 0.8 && kmpip1_m <= 1.0"; // aka "neutral" K*(K-Pi+)
    auto reject_kstar_plus = "kspip1_m <= 0.8 || kspip1_m >= 1.0"; // aka "charged" K*(KsPi+)
    auto reject_kstar_zero = "kmpip1_m <= 0.8 || kmpip1_m >= 1.0"; // aka "neutral" K*(K-Pi+)

    // Apply cuts; make new dataframe
    auto cut_df = df2.Filter("pathlength_sig > 5")
                     .Filter(reject_delta)
                     .Filter(reject_lambda);
    
    
    
    // ********** HISTOGRAMS **********
    
    auto h1 = cut_df.Filter(keep_kstar_plus).Filter(reject_kstar_zero).Histo1D({"h1", "f1_m (select charged K*, reject neutral K*)", 60, 1.2, 1.7}, "f1_m");
    h1->SetLineColor(kBlack);
    //auto h2 = cut_df.Filter(keep_kstar_plus).Filter(keep_kstar_zero).Histo1D({"h2", "f1", 60, 1.1, 1.7}, "f1_m");
    // auto xMin = 1.0;
    // auto xMax = 1.8;
    // auto yMin = 0;
    // auto yMax = 15000;


    // ********** FITTING **********

    std::unique_ptr<TF1> bkg = std::make_unique<TF1>("bkg", "TMath::Exp([0] + [1] * x + [2] * x * x)", 1.2, 1.7);
    bkg->SetParName(0, "bkg_expPar1");
    bkg->SetParName(1, "bkg_expPar2");
    bkg->SetParName(2, "bkg_expPar3");
    std::unique_ptr<TF1> bw1420 = std::make_unique<TF1>("bw1420", "breitwigner(0)", 1.2, 1.7); // used to have BreitWigner(x, [4], [5])
    bw1420->SetParName(0, "bw1420_amplitude");
    bw1420->SetParName(1, "bw1420_mass");
    bw1420->SetParName(2, "bw1420_width");
    std::unique_ptr<TF1> fitCombined = std::make_unique<TF1>("fitCombined", "bkg + bw1420", 1.2, 1.7);
    fitCombined->SetParameter("bkg_expPar1", -6.47E0); //  -6.47E0);
    fitCombined->SetParameter("bkg_expPar2", 9.29E0); //  9.29E0);
    fitCombined->SetParameter("bkg_expPar3", -2.970E0); // -2.970E0);
    fitCombined->SetParameter("bw1420_amplitude", 145); // 1.609E2
    fitCombined->SetParameter("bw1420_mass", 1.42); // 1.420E0
    fitCombined->SetParameter("bw1420_width", 7.082E-2); // 7.082E-2
    fitCombined->SetLineColor(kMagenta);
    fitCombined->SetLineWidth(2);
    fitCombined->SetLineStyle(4);
    h1->Fit(fitCombined.get(), "RV");


    bkg->SetParameter(0, fitCombined->GetParameter("bkg_expPar1")); // 
    bkg->SetParameter(1, fitCombined->GetParameter("bkg_expPar2")); // 
    bkg->SetParameter(2, fitCombined->GetParameter("bkg_expPar3")); // 
    bkg->SetLineColor(kCyan);
    bkg->SetLineWidth(2);
    bkg->SetLineStyle(2);

    bw1420->SetParameter(0, fitCombined->GetParameter("bw1420_amplitude")); //
    bw1420->SetParameter(1, fitCombined->GetParameter("bw1420_mass")); //
    bw1420->SetParameter(2, fitCombined->GetParameter("bw1420_width")); //
    bw1420->SetLineColor(kGreen);
    bw1420->SetLineWidth(2);
    bw1420->SetLineStyle(2);

    
    // ******** PLOTTING ********

    std::shared_ptr<TCanvas> c1 = std::make_shared<TCanvas>("c1", "f1_m_fit", 800, 600);
    
    // h1->GetXaxis()->SetRangeUser(xMin,xMax);
    // h1->GetYaxis()->SetRangeUser(yMin,yMax);
    h1->Draw("E"); // "E"
    bkg->Draw("same");
    bw1420->Draw("same");
    fitCombined->Draw("same");
    
    auto legend1 = new TLegend(0.75, 0.77, .98, 0.58); //(x_topLeft, y_topLeft, x_bottomRight, y_bottomRight)
    legend1->AddEntry("h1", "Data: ks_m", "l");
    legend1->AddEntry(bkg.get(), "fcn: bkg", "l");
    legend1->AddEntry(bw1420.get(), "fcn: bw1420", "l");
    legend1->AddEntry(fitCombined.get(), "bkg + bw1420", "l");
    legend1->Draw();

    c1->Update();
    c1->SaveAs("../plots/f1_m_fit.png");

// ********** END OF PROGRAM **********

    // But...keep the canvas displayed and wait for user input to close

while (true) {
    // Create a TApplication object to handle the event loop
    TApplication app("app", nullptr, nullptr);

    // Wait for user input to close the program
    std::cout << "Press Enter to continue..." << std::endl;
    std::cin.ignore(); // this line clears the input buffer before the user presses enter so no previously entered characters are registered
    c1->Close();
    //app.Terminate(); // not working, so trying below
    gApplication->Terminate(0);
    }

}

// ********** MAIN FUNCTION **********

// Runs above analysis:
int main() {
    f1_flat_bx2_analysis();
    return 0;
}