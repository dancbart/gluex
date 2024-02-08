// Description: Analysis of f1(1420) resonance in flat bx2 data.

void analysis(double f1_mMin, double f1_mMax, int plotIndex) {

    ROOT::RDataFrame df("pipkmks__B4_M16", "KKpi_flat_bestX2_2017.root");

   
   // ********** DEFINITIONS **********

    // Define resonances; add columns to dataframe for each....using '.Define' method
    auto df2 = df
                 // pi_plus (pip2).  i.e. one of two components of the kShort.  the other is pi_minus (pim)
                 // total mass:
                 .Define("pip2_m", "sqrt(pip2_E*pip2_E - pip2_px*pip2_px - pip2_py*pip2_py - pip2_pz*pip2_pz)")
                 // Mass squared:
                 .Define("pip2_m2", "pip2_E*pip2_E - pip2_px*pip2_px - pip2_py*pip2_py - pip2_pz*pip2_pz")

                 // pi_minus (pim).  i.e. one of two components of the kShort.  the other is pi_plus (pip2)
                 // total mass:
                 .Define("pim_m", "sqrt(pim_E*pim_E - pim_px*pim_px - pim_py*pim_py - pim_pz*pim_pz)")
                 // Mass squared:
                 .Define("pim_m2", "pim_E*pim_E - pim_px*pim_px - pim_py*pim_py - pim_pz*pim_pz")
                 
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
                 
                 // lambda (proton & k_minus -- 1500, 1900?)
                 .Define("pkm_E", "p_E + km_E") // 4-momentum
                 .Define("pkm_px", "p_px + km_px")
                 .Define("pkm_py", "p_py + km_py")
                 .Define("pkm_pz", "p_pz + km_pz")
                 // total mass:
                 .Define("pkm_m" , "sqrt(pkm_E*pkm_E - pkm_px*pkm_px - pkm_py*pkm_py - pkm_pz*pkm_pz)")

                 // k_minus & pip1
                 .Define("kmpip1_E", "km_E + pip1_E") // 4-momentum
                 .Define("kmpip1_px", "km_px + pip1_px")
                 .Define("kmpip1_py", "km_py + pip1_py")
                 .Define("kmpip1_pz", "km_pz + pip1_pz")
                 // total mass:
                 .Define("kmpip1_m", "sqrt(kmpip1_E*kmpip1_E - kmpip1_px*kmpip1_px - kmpip1_py*kmpip1_py - kmpip1_pz*kmpip1_pz)")
                 // total mass squared:
                 .Define("kmpip1_m2", "kmpip1_E*kmpip1_E - kmpip1_px*kmpip1_px - kmpip1_py*kmpip1_py - kmpip1_pz*kmpip1_pz")

                 // k_short & pip1
                 .Define("kspip1_E", "ks_E + pip1_E") // 4-momentum
                 .Define("kspip1_px", "ks_px + pip1_px")
                 .Define("kspip1_py", "ks_py + pip1_py")
                 .Define("kspip1_pz", "ks_pz + pip1_pz")
                 // total mass:
                 .Define("kspip1_m", "sqrt(kspip1_E*kspip1_E - kspip1_px*kspip1_px - kspip1_py*kspip1_py - kspip1_pz*kspip1_pz)")
                 // total mass squared:
                 .Define("kspip1_m2", "kspip1_E*kspip1_E - kspip1_px*kspip1_px - kspip1_py*kspip1_py - kspip1_pz*kspip1_pz")

                 // f1 (pip1 & km & ks{pip2 + pim]}
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
    auto select_kShort = "ks_m >= 0.45 && ks_m <= 0.55";
    auto reject_kShort = "ks_m <= 0.45 || ks_m >= 0.55";
    // Select f1(1420) mass range
    // auto select_f1 = "f1_m >= f1_mMin && f1_m <= f1_mMax";
    auto select_f1 = [=](double f1_m) { return f1_m >= f1_mMin && f1_m <= f1_mMax; };

    // Apply cuts; make new dataframe
    auto cut_df = df2.Filter(reject_delta)
                     .Filter(reject_lambda)
                     .Filter(select_f1, {"f1_m"})
                     .Filter("pathlength_sig > 5");
                    //  .Filter(select_kShort);

    // Other cuts (in case I want two histograms on the same canvas, for example)
    auto cut_df_alternate = df2.Filter(reject_delta)
                     .Filter(reject_lambda)
                     .Filter(select_f1, {"f1_m"});
                    //  .Filter("pathlength_sig > 5");
                    //  .Filter(select_kShort);
    
    // ********** 1D HISTOGRAMS **********
    
    // auto h1 = cut_df.Filter(keep_kstar_plus).Histo1D({"h1", "f1_m (keep charged K only)", 60, 1.2, 1.7}, "f1_m");
    // h1->SetLineColor(kBlack);
    // auto xMin = 1.0;
    // auto xMax = 1.8;
    // auto yMin = 0;
    // auto yMax = 15000;

    // 1D histogram of M(pip2 + pim) (mass of Ks).
    auto h1 = cut_df.Histo1D({"hNew", Form("M(pip2 + pim).  Bins of: pipKmKs invariant mass (GeV): %.2f - %.2f", f1_mMin, f1_mMax), 60, 0.400, 0.600}, "ks_m");
    h1->SetLineColor(kRed);
    // 1D histogram of M(pip2 + pim) (mass of Ks). DIFFERENT CUTS!
    // auto h2 = cut_df_alternate.Histo1D({"hNew", Form("M(pip2 + pim).  Bins of: pipKmKs invariant mass (GeV): %.2f - %.2f", f1_mMin, f1_mMax), 60, 0.400, 0.600}, "ks_m");
    // h2->SetLineColor(kBlue);

    // ********** DALITZ PLOTS ********** (i.e. 2D HISTOGRAMS)

    // // auto h3 = cut_df.Histo2D({"h3", "Select f1: 1.3 - 1.5)", 200, 0.6, 1.1, 200, 0.6, 1.1}, "kspip1_m", "kmpip1_m");
    // // create histogram where the histogram label is a string that is a function of the f1 mass range
    // auto h3 = cut_df.Histo2D({"h2", Form("Bins of: pipKmKs invariant mass (GeV): %.2f - %.2f", f1_mMin, f1_mMax), 40, 0.100, 0.200, 40, 0.100, 0.200}, "pip2_m2", "pim_m2");
    // // auto h3 = cut_df.Histo2D({"h3", "", 200, 0.6, 1.1, 200, 0.6, 1.1}, "kspip1_m", "kmpip1_m");
    // h3->SetLineColor(kGreen);


    // ********** FITTING **********

    // PUT THIS BACK IN AFTER SELECTION PLOTTING//
    // std::unique_ptr<TF1> bkg = std::make_unique<TF1>("bkg", "TMath::Exp([0] + [1] * x + [2] * x * x)", 1.2, 1.7);
    // bkg->SetParName(0, "bkg_expPar1");
    // bkg->SetParName(1, "bkg_expPar2");
    // bkg->SetParName(2, "bkg_expPar3");

    // std::unique_ptr<TF1> bw1420 = std::make_unique<TF1>("bw1420", "breitwigner(0)", 1.2, 1.7); // used to have BreitWigner(x, [4], [5])
    // bw1420->SetParName(0, "bw1420_amplitude");
    // bw1420->SetParName(1, "bw1420_mass");
    // bw1420->SetParName(2, "bw1420_width");

    // PUT THIS BACK IN AFTER SELECTION PLOTTING/
    // std::unique_ptr<TF1> voigtian = std::make_unique<TF1>("voigtian", "[0]*TMath::Voigt(x - [1], [2], [3])", 1.2, 1.7);
    // voigtian->SetParName(0, "voigtian_amplitude");
    // voigtian->SetParName(1, "voigtian_mean"); // 'mean' is the offset that places the peak at the correct position, where we know the resonance to be.  It represents the particles mass.
    // voigtian->SetParName(2, "voigtian_sigma"); // 'sigma' is the gaussian width (detector resolution)
    // voigtian->SetParName(3, "voigtian_width"); // 'lg' aka "lorentz gamma" is the width of the breit-wigner (natural width of the resonance)

    // std::unique_ptr<TF1> voigtian2 = std::make_unique<TF1>("voigtian2", "[0]*TMath::Voigt(x - [1], [2], [3])", 1.2, 1.7);
    // voigtian->SetParName(0, "voigtian_amplitude2");
    // voigtian->SetParName(1, "voigtian_mean2"); // 'mean' is the offset that places the peak at the correct position, where we know the resonance to be.  It represents the particles mass.
    // voigtian->SetParName(2, "voigtian_sigma2"); // 'sigma' is the gaussian width (detector resolution)
    // voigtian->SetParName(3, "voigtian_width2");

    // std::unique_ptr<TF1> RooVoigtian = std::make_u nique<TF1>("RooVoigtian", "ROOT::RooVoigtian(x, [0], [1], [2])", 1.2, 1.7); // 'doFast use the faster look-up-table-based method for the evaluation of the complex error function.
    // RooVoigtian->SetParName(0, "RooVoigtian_mean");
    // RooVoigtian->SetParName(1, "RooVoigtian_width");
    // RooVoigtian->SetParName(2, "RooVoigtian_sigma");

    // Combine functions: //

// PUT THIS BACK IN AFTER SELECTION PLOTTING/
    // std::unique_ptr<TF1> fitCombined = std::make_unique<TF1>("fitCombined", "bkg + voigtian", 1.2, 1.7);
    // fitCombined->SetParameter("bkg_expPar1", -6.47E0); //  -6.47E0);
    // fitCombined->SetParameter("bkg_expPar2", 9.29E0); //  9.29E0);
    // fitCombined->SetParameter("bkg_expPar3", -2.970E0); // -2.970E0);
    
    // fitCombined->SetParameter("bw1420_amplitude", 145); // 1.609E2
    // fitCombined->SetParameter("bw1420_mass", 1.42); // 1.420E0
    // fitCombined->SetParameter("bw1420_width", 7.082E-2); // 7.082E-2
    
    // PUT THIS BACK IN AFTER SELECTION PLOTTING/
    // fitCombined->SetParameter("voigtian_amplitude", 4.5E2); //
    // fitCombined->SetParameter("voigtian_mean", 1.45807E0); // 
    // fitCombined->SetParameter("voigtian_sigma", 1.0E-02); // detector resolution (this is part of the gaussian component of the voigtian)
    // fitCombined->SetParameter("voigtian_width", 3.81110E-06); // 'lg' here corresponds to the breit wigner width (this is part of the lorentzian component of the voigtian).  I think the 'l' in 'lg' stands for "lorentzian-gamma"    
    
    // fitCombined->SetParameter("voigtian_amplitude2", 4.5E2); //
    // fitCombined->SetParameter("voigtian_mean2", 1.45807E0); // 
    // fitCombined->SetParameter("voigtian_sigma2", 1.0E-02); // detector resolution (this is part of the gaussian component of the voigtian)
    // fitCombined->SetParameter("voigtian_width2", 3.81110E-06);

    // When using 'FixParameter' use index number, not name.  Compiler will complain if you use name.
    
    // PUT THIS BACK IN AFTER SELECTION PLOTTING/
//     fitCombined->FixParameter(5, 1.0E-02); // detector resolution (this is part of the gaussian component of the voigtian)")

// // PUT THIS BACK IN AFTER SELECTION PLOTTING/
//     fitCombined->SetLineColor(kMagenta);
//     fitCombined->SetLineWidth(2);
//     fitCombined->SetLineStyle(4);
//     h1->Fit(fitCombined.get(), "RV");

// // PUT THIS BACK IN AFTER SELECTION PLOTTING/
//     bkg->SetParameter(0, fitCombined->GetParameter("bkg_expPar1")); // 
//     bkg->SetParameter(1, fitCombined->GetParameter("bkg_expPar2")); // 
//     bkg->SetParameter(2, fitCombined->GetParameter("bkg_expPar3")); // 
//     bkg->SetLineColor(kCyan);
//     bkg->SetLineWidth(2);
//     bkg->SetLineStyle(2);

    // bw1420->SetParameter(0, fitCombined->GetParameter("bw1420_amplitude")); //
    // bw1420->SetParameter(1, fitCombined->GetParameter("bw1420_mass")); //
    // bw1420->SetParameter(2, fitCombined->GetParameter("bw1420_width")); //
    // bw1420->SetLineColor(kGreen);
    // bw1420->SetLineWidth(2);
    // bw1420->SetLineStyle(2);

// // PUT THIS BACK IN AFTER SELECTION PLOTTING/
//     voigtian->SetParameter(0, fitCombined->GetParameter("voigtian_amplitude")); //
//     voigtian->SetParameter(1, fitCombined->GetParameter("voigtian_mean")); //
//     voigtian->SetParameter(2, fitCombined->GetParameter("voigtian_sigma")); //
//     voigtian->SetParameter(3, fitCombined->GetParameter("voigtian_width")); //
//     voigtian->SetLineColor(kGreen);
//     voigtian->SetLineWidth(2);
//     voigtian->SetLineStyle(2);

    // voigtian2->SetParameter(0, fitCombined->GetParameter("voigtian_amplitude2")); //
    // voigtian2->SetParameter(1, fitCombined->GetParameter("voigtian_mean2")); //
    // voigtian2->SetParameter(2, fitCombined->GetParameter("voigtian_sigma2")); //
    // voigtian2->SetParameter(3, fitCombined->GetParameter("voigtian_width2")); //
    // voigtian2->SetLineColor(kGreen);
    // voigtian2->SetLineWidth(2);
    // voigtian2->SetLineStyle(2);


    
    // ******** PLOTTING ********

    std::shared_ptr<TCanvas> c1 = std::make_shared<TCanvas>("c1", "M(pi+pi-)", 800, 600);

    // h1->GetXaxis()->SetRangeUser(xMin,xMax);
    // h1->GetYaxis()->SetRangeUser(yMin,yMax);
    // h1->Draw("E"); // "E"
    // draw the histogram as a histogram instead of data points
    h1->Draw("HIST");
    // h2->Draw("same");
    // options to draw histogram with are: "E" (error bars), "H" (histogram), "L" (line), "P" (markers), "C" (curve), "B" (bar chart), "A" (area), "9" (same as "H" but fills with a color), "hist" (same as "H"), "histc" (same as "C"), "same" (superimpose on previous picture), "nostack" (don't stack bars), "nol" (don't draw the line), "noc" (don't draw the markers), "nofunction" (don't draw the function), "text" (draw bin contents as text), "goff" (graphics off), "e1" (draw error bars only), "e2" (draw error rectangles only), "e3" (draw error bars and rectangles), "e4" (draw a fill area through the end points of the vertical error bars), "e5" (draw a smooth fill area through the end points of the vertical error bars), "e6" (draw a smooth fill area through the end points of the error bars), "e7" (draw a fill area through the end points of the error bars)
    // and options to draw the dalitz plot (h2) with are: "COLZ" (draw a color plot representing the cell contents), "CONTZ" (draw a contour plot representing the cell contents), "LEGO" (draw a lego plot representing the cell contents), "SURF" (draw a surface plot representing the cell contents), "SURF1" (draw a surface plot representing the cell contents, with hidden line removal), "SURF2" (draw a surface plot representing the cell contents, with color representation of the cell contents), "SURF3" (draw a surface plot representing the cell contents, with color representation of the cell contents and hidden line removal), "SURF4" (draw a surface plot representing the cell contents, with Gouraud shading), "SURF5" (draw a surface plot representing the cell contents, with color representation of the cell contents and Gouraud shading), "SURF6" (draw a surface plot representing the cell contents, with color representation of the cell contents, Gouraud shading and hidden line removal)
    // h2->Draw("COLZ");
    // axes labels
    // h2->GetXaxis()->SetTitle("K_{S}#pi^{+} mass Squared (GeV^{2})");
    // h2->GetYaxis()->SetTitle("K^{-}#pi^{+} mass Squared (GeV^{2})");
    // h2->GetXaxis()->SetTitle("#pi^{+} mass Squared (GeV^{2})");
    // h2->GetYaxis()->SetTitle("#pi^{-} mass Squared (GeV^{2})");
    // bkg->Draw("same");
    // bw1420->Draw("same");
    // voigtian->Draw("same");
    // voigtian2->Draw("same");
    // fitCombined->Draw("same");


    auto legend1 = new TLegend(0.75, 0.77, .98, 0.58); //(x_topLeft, y_topLeft, x_bottomRight, y_bottomRight)
    legend1->AddEntry(h1.GetPtr(), "Pathlength_sig > 5", "l"); // using "GetPtr()" instead of "get()" because "get()" is a method of unique_ptr, not shared_ptr, something like that.
    // legend1->AddEntry(h2.GetPtr(), "No pathlength cut", "l");
    
    // legend1->AddEntry("h1", "Data, no fitting", "l");
    // Legend for h2
    // auto legend2 = new TLegend(0.75, 0.77, .98, 0.58); //(x_topLeft, y_topLeft, x_bottomRight, y_bottomRight)
    // legend2->AddEntry("h2", "Dalitz plot", "l");

    // legend1->AddEntry(bkg.get(), "fcn: bkg", "l");
    // legend1->AddEntry(bw1420.get(), "fcn: bw1420", "l");
    // legend1->AddEntry(voigtian.get(), "fcn: voigtian", "l");
    // legend1->AddEntry(voigtian2.get(), "fcn: voigtian2", "l");
    // legend1->AddEntry(fitCombined.get(), "bkg + voigtan", "l");
    legend1->Draw();
    // legend2->Draw();

    TString plotName = Form("../plots/kShort/M(pip2 + pim)_%d_pathlength_sig.png", plotIndex); // plotIndex is the index of the KKpi mass range and is set in the for loop in the main function
    c1->Update();
    c1->SaveAs(plotName);
    // c2->Update();
    // c2->SaveAs(plotName);
    // // c2->SaveAs("../plots/dalitz_plot.png");

// ********** END OF PROGRAM **********

    // But...keep the canvas displayed and wait for user input to close

// while (true) {
//     // Create a TApplication object to handle the event loop
//     TApplication app("app", nullptr, nullptr);

//     // Wait for user input to close the program
//     std::cout << "Press Enter to continue..." << std::endl;
//     std::cin.ignore(); // this line clears the input buffer before the user presses enter so no previously entered characters are registered
//     c2->Close();
//     //app.Terminate(); // not working, so trying below
//     gApplication->Terminate(0);
//     }

}

void KKpi_flat_bx2_analysis() {
    // For loop running through "analysis" for different ranges of f1 masses
    // create 2D array of masses from 1.1 to 2.0 GeV in 100 MeV steps
    for (int i = 0; i < 10; i++) {
        int plotIndex = i;
        double f1_mMin = 1.1 + i * 0.1;
        double f1_mMax = 1.2 + i * 0.1;
        analysis(f1_mMin, f1_mMax, plotIndex);
    }

    
}

// ********** MAIN FUNCTION ********** // Used when running using c++ compiler, i.e. "main" function is the entry point for c++ programs.
// However, if running with "ROOT" the entry point is whatever function name in the script matches the file name!  Then "main" is not needed.

// Runs above analysis:
// int main() {
//     f1_flat_bx2_analysis();
//     return 0;
// }


