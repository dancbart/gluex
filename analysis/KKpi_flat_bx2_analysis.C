// Description: Analysis of f1(1420) resonance in flat bx2 data.

void analysis(double f1_mMin, double f1_mMax, int plotIndex) {
    gStyle->SetOptStat(0); // don't show statistics box on plots
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
    auto select_f1 = [=](double f1_m) { return f1_m >= f1_mMin && f1_m <= f1_mMax; }; // lambda function to select f1 mass range

    // Apply cuts; make new dataframe

    // // Old cuts (~5/2023).  Used when originally looking for f1(1420) resonance
    // auto cut_df0 = df2.Filter("pkm_m > 1.9") // lambda cut
    //                  .Filter("pip1p_m > 1.4") // delta++ cut
    //                  .Filter("pathlength_sig > 5");
    //                 //  Not sure why these kspip1 and kmpip1 cuts were here.  They don't make much sense, and also cut out almost all the data.
    //                 //  .Filter("kspip1_m > 1.1") // kspip1 cut
    //                 //  .Filter("kmpip1_m > 1.1") // kmpip1 cut

    // Working cuts (2/2024).  Use these for active analysis
    auto cut_df1 = df2.Filter("pathlength_sig > 5")
                    //  .Filter(select_f1, {"f1_m"})
                     .Filter(reject_delta)
                     .Filter(reject_lambda);
                    //  .Filter(select_kShort);

    // // Other cuts (in case I want two histograms on the same canvas, for example)
    // auto cut_df2 = df2.Filter("pathlength_sig > 5");
    //                 //  .Filter(reject_delta)
    //                 //  .Filter(reject_lambda)
    //                 //  .Filter(select_f1, {"f1_m"})
    //                 //  .Filter(select_kShort);
    
    // ********** 1D HISTOGRAMS **********
    
    // // 1D histogram for pip1p_m > 1.4" (delta++ cut)
    // auto h1 = cut_df1.Histo1D({"h1", "M(#pi^{+} + proton) (#Delta++ distribution)", 60, 1.0, 3.5}, "pip1p_m");
    // h1->GetXaxis()->SetTitle("#Delta++ & #Lambda (GeV) & kShort"); // X-axis label
    // h1->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h1->SetLineColor(kBlue);

    // 1D histogram for pkm_m > 1.9 (lambda cut)
    // auto h2 = cut_df1.Histo1D({"h2", "M(p + K^{-}) (#Lambda distribution)", 60, 1.4, 3.8}, "pkm_m");
    // h2->GetXaxis()->SetTitle("#Lambda: M(proton + K^{-}) (GeV)"); // X-axis label
    // h2->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h2->SetLineColor(kMagenta);

    // // 1D histograms for kShort
    // auto h3 = df2.Histo1D({"h4", "M(K_{s}) (kShort distribution)", 60, 0.4, 0.6}, "ks_m");
    // h3->GetXaxis()->SetTitle("kShort: M(K_{s}) (GeV)"); // X-axis label
    // h3->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h3->SetLineColor(kBlack);
    // h3->SetMinimum(0);

    // auto h4 = cut_df1.Histo1D({"h3", "M(K_{s}) (kShort distribution)", 60, 0.4, 0.6}, "ks_m");
    // h4->GetXaxis()->SetTitle("kShort: M(K_{s}) (GeV)"); // X-axis label
    // h4->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h4->SetLineColor(kRed);
    // h4->SetMinimum(0);

    // auto h1 = cut_df.Filter(keep_kstar_plus).Histo1D({"h1", "f1_m (keep charged K only)", 60, 1.2, 1.7}, "f1_m");
    // h1->SetLineColor(kBlack);
    // auto xMin = 1.0;
    // auto xMax = 1.8;
    // auto yMin = 0;
    // auto yMax = 15000;

    // 1D Histogram of KKpi full mass range (to see where the f1(1420) is)
    // auto h1 = df2.Histo1D({"h1", "M(K^{-}K_{s}#pi^{+})", 60, 0.2, 2.0}, "f1_m");
    // h1->GetXaxis()->SetTitle("M(K^{-}K_{s}#pi^{+}) (GeV)"); // X-axis label
    // h1->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h1->SetLineColor(kBlue);
    // auto h2 = cut_df1.Filter("pathlength_sig > 5").Filter(reject_delta).Histo1D({"h2", "M(K^{-}K_{s}#pi^{+})", 60, 1.2, 1.7}, "f1_m");
    // h2->GetXaxis()->SetTitle("M(K^{-}K_{s}#pi^{+}) (GeV)"); // X-axis label
    // h2->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h2->SetLineColor(kMagenta);
    // auto h3 = cut_df1.Filter("pathlength_sig > 5").Filter(reject_lambda).Histo1D({"h3", "M(K^{-}K_{s}#pi^{+})", 60, 1.2, 1.7}, "f1_m");
    // h3->GetXaxis()->SetTitle("M(K^{-}K_{s}#pi^{+}) (GeV)"); // X-axis label
    // h3->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h3->SetLineColor(kBlack);
    // auto h4 = cut_df1.Filter("pathlength_sig > 5").Filter(select_kShort).Histo1D({"h4", "M(K^{-}K_{s}#pi^{+})", 60, 1.2, 1.7}, "f1_m");
    // h4->GetXaxis()->SetTitle("M(KK^{-}#_{s}pi^{+}) (GeV)"); // X-axis label
    // h4->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h4->SetLineColor(TColor::GetColor(160, 32, 240)); // A shade of purple
    // auto h5 = cut_df1.Filter("pathlength_sig > 5").Filter(reject_delta).Filter(reject_lambda).Filter(select_kShort).Histo1D({"h5", "M(K^{-}K_{s}#pi^{+})", 60, 1.2, 1.7}, "f1_m");
    // h5->GetXaxis()->SetTitle("M(K^{-}K_{s}#pi^{+}) (GeV)"); // X-axis label
    // h5->GetYaxis()->SetTitle("Counts"); // Y-axis label
    // h5->SetLineColor(kBlue);

    // // 1D histogram of M(pip2 + pim) (mass of Ks).
    // auto h1 = cut_df.Histo1D({"hNew", Form("M(pip2 + pim).  Bins of: pipKmKs invariant mass (GeV): %.2f - %.2f", f1_mMin, f1_mMax), 60, 0.400, 0.600}, "ks_m");
    // h1->SetLineColor(kRed);
    // // 1D histogram of M(pip2 + pim) (mass of Ks). DIFFERENT CUTS!
    // // auto h2 = cut_df_alternate.Histo1D({"hNew", Form("M(pip2 + pim).  Bins of: pipKmKs invariant mass (GeV): %.2f - %.2f", f1_mMin, f1_mMax), 60, 0.400, 0.600}, "ks_m");
    // // h2->SetLineColor(kBlue);

    // ********** DALITZ PLOTS ********** (i.e. 2D HISTOGRAMS)

    // // kShort Dalitz plot
    // auto h2 = cut_df.Histo2D({"h2", Form("Bins of: pipKmKs invariant mass (GeV): %.2f - %.2f", f1_mMin, f1_mMax), 40, 0.100, 0.200, 40, 0.100, 0.200}, "pip2_m2", "pim_m2");
    // K* Dalitz plot
    auto h3 = cut_df1.Histo2D({"h3", Form("Bins of: KKpi invariant mass (GeV): %.2f - %.2f", f1_mMin, f1_mMax), 40, 0.1, 1.4, 40, 0.1, 1.4}, "kspip1_m2", "kmpip1_m2");
    h3->SetLineColor(kRed);


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

    std::shared_ptr<TCanvas> c1 = std::make_shared<TCanvas>("c1", "Canvas", 800, 600);
    c1->SetLeftMargin(0.15);

    // options to draw histogram with are: "E" (error bars), "H" (histogram), "L" (line), "P" (markers), "C" (curve), "B" (bar chart), "A" (area), "9" (same as "H" but fills with a color), "hist" (same as "H"), "histc" (same as "C"), "same" (superimpose on previous picture), "nostack" (don't stack bars), "nol" (don't draw the line), "noc" (don't draw the markers), "nofunction" (don't draw the function), "text" (draw bin contents as text), "goff" (graphics off), "e1" (draw error bars only), "e2" (draw error rectangles only), "e3" (draw error bars and rectangles), "e4" (draw a fill area through the end points of the vertical error bars), "e5" (draw a smooth fill area through the end points of the vertical error bars), "e6" (draw a smooth fill area through the end points of the error bars), "e7" (draw a fill area through the end points of the error bars)
    // and options to draw the dalitz plot (h2) with are: "COLZ" (draw a color plot representing the cell contents), "CONTZ" (draw a contour plot representing the cell contents), "LEGO" (draw a lego plot representing the cell contents), "SURF" (draw a surface plot representing the cell contents), "SURF1" (draw a surface plot representing the cell contents, with hidden line removal), "SURF2" (draw a surface plot representing the cell contents, with color representation of the cell contents), "SURF3" (draw a surface plot representing the cell contents, with color representation of the cell contents and hidden line removal), "SURF4" (draw a surface plot representing the cell contents, with Gouraud shading), "SURF5" (draw a surface plot representing the cell contents, with color representation of the cell contents and Gouraud shading), "SURF6" (draw a surface plot representing the cell contents, with color representation of the cell contents, Gouraud shading and hidden line removal)

    // h1->GetXaxis()->SetRangeUser(xMin,xMax);
    // h1->GetYaxis()->SetRangeUser(yMin,yMax);
    // h1->Draw("E"); // "E"
    // draw as a histogram instead of data points
    // h1->Draw("HIST");
    // h2->Draw("HIST");
    h3->Draw("COLZ");
    // h4->Draw("same");
    
    // // Draw line at x-value
    // double x_value1 = 0.45;
    // double x_value2 = 0.55;
    // double y_value1 = 0;
    // double y_value2 = 50000;
    // TLine *line1 = new TLine(x_value1, y_value1, x_value1, y_value2);
    // line1->SetLineColor(kBlack);
    // line1->SetLineWidth(4);
    // line1->Draw();
    // // Add a label near the top of the line
    // TLatex latex1;
    // latex1.SetTextSize(0.03);
    // latex1.SetTextAlign(22); // Center the text horizontally and vertically
    // // Adjust the y position slightly above the line for visibility
    // latex1.DrawLatex(x_value1, y_value2 * 1.1, "0.45 GeV");

    // TLine *line2 = new TLine(x_value2, y_value1, x_value2, y_value2);
    // line2->SetLineColor(kBlack);
    // line2->SetLineWidth(4);
    // line2->Draw();
    // // Add a label near the top of the line
    // TLatex latex2;
    // latex2.SetTextSize(0.03);
    // latex2.SetTextAlign(22); // Center the text horizontally and vertically
    // // Adjust the y position slightly above the line for visibility
    // latex2.DrawLatex(x_value2, y_value2 * 1.1, "0.55 GeV");

    // latex.DrawLatex(x_value, y_value, "0.45 Gev");
    // h5->Draw("same");
    // Usage: auto arrow = new TArrow(x_position, y_start, x_position, y_end, 0.02, "|>"); // Adjust x_position, y_start, y_end as needed
    // auto arrow1 = new TArrow(1.295, 2200, 1.295, 1200, 0.01, "|>"); // Example positions
    // arrow1->SetLineWidth(8);
    // arrow1->Draw();
    // arrow1->SetLineColor(kRed);
    // auto latex1 = new TLatex(1.295, 2300, "1.295 GeV"); // Adjust position and LaTeX formatted text as needed
    // latex1->SetTextAlign(22); // Centers the text horizontally and vertically
    // latex1->SetTextSize(0.03); // Adjust text size as needed
    // latex1->Draw();

    // auto arrow2 = new TArrow(1.420, 3000, 1.420, 4000, 0.01, "|>"); // Example positions
    // arrow2->SetLineWidth(8);
    // arrow2->Draw();
    // arrow2->SetLineColor(kRed);
    // auto latex2 = new TLatex(1.420, 2800, "1.420 GeV"); // Adjust position and LaTeX formatted text as needed
    // latex2->SetTextAlign(22); // Centers the text horizontally and vertically
    // latex2->SetTextSize(0.03); // Adjust text size as needed
    // latex2->Draw();

    // // Draw histogram for pip2 vs. pim mass squared (evidence of Ks)
    // h2->Draw("same");
    // h2->Draw("COLZ");
    // h2->GetXaxis()->SetTitle("#pi^{+} mass Squared (GeV^{2})");
    // h2->GetYaxis()->SetTitle("#pi^{-} mass Squared (GeV^{2})");

    // // Draw histogram for (Ks + pip1) vs. (Km + pip1) mass squared (evidence of f1(1420))
    // h3->Draw("COLZ");
    // h3->GetXaxis()->SetTitle("K_{S}#pi^{+} mass squared (GeV^{2})");
    // h3->GetYaxis()->SetTitle("K^{-}#pi^{+} mass squared (GeV^{2})");
    
    // bkg->Draw("same");
    // bw1420->Draw("same");
    // voigtian->Draw("same");
    // voigtian2->Draw("same");
    // fitCombined->Draw("same");


    // auto legend1 = new TLegend(0.60, 0.88, .85, 0.75); //(x_topLeft, y_topLeft, x_bottomRight, y_bottomRight)
    // legend1->AddEntry(h3.GetPtr(), "Pathlength_sig > 5", "l"); // using "GetPtr()" instead of "get()" because "get()" is a method of unique_ptr, not shared_ptr, something like that.
    // legend1->AddEntry(h2.GetPtr(), "No pathlength cut", "l");
    
    // legend for KKpi mass range
    // legend1->AddEntry(h1.GetPtr(), "M(K^{-}K_{s}#pi^{+})", "l");
    // legend1->AddEntry(h1.GetPtr(), "M(#pi^{+} + proton) (#Delta++ distribution)", "l");
    // legend1->AddEntry(h2.GetPtr(), "M(p + K^{-}) (#Lambda distribution)", "l");
    // legend1->AddEntry(h3.GetPtr(), "kShort", "l");
    // legend1->AddEntry(h4.GetPtr(), "kShort w/pathlength", "l");
    // legend1->AddEntry(h5.GetPtr(), "All cuts (pl, #Delta, #Lambda, ks)");
    // Legend for h2
    // auto legend2 = new TLegend(0.75, 0.77, .98, 0.58); //(x_topLeft, y_topLeft, x_bottomRight, y_bottomRight)
    // legend2->AddEntry("h2", "Dalitz plot", "l");

    // legend1->AddEntry(bkg.get(), "fcn: bkg", "l");
    // legend1->AddEntry(bw1420.get(), "fcn: bw1420", "l");
    // legend1->AddEntry(voigtian.get(), "fcn: voigtian", "l");
    // legend1->AddEntry(voigtian2.get(), "fcn: voigtian2", "l");
    // legend1->AddEntry(fitCombined.get(), "bkg + voigtan", "l");
    // legend1->Draw();
    // legend2->Draw();

    // TString plotName = Form("../plots/dalitzPlots/_TEST_%d.png", plotIndex); // plotIndex is the index of the KKpi mass range and is set in the for loop in the main function
    TString plotName = Form("../_plots/dalitzPlots/TEST.png"); // plotIndex is the index of the KKpi mass range and is set in the for loop in the main function
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
    for (int i = 0; i < 1; i++) {
        int plotIndex = i;
        double f1_mMin = 1.2 + i * 0.05;
        double f1_mMax = 1.70 + i * 0.05;
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


