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
    auto keep_kstar_plus = "kspip1_m >= 0.8 && kspip1_m <= 1.0";
    auto keep_kstar_zero = "kmpip1_m >= 0.8 && kmpip1_m <= 1.0";
    auto reject_kstar_plus = "kspip1_m <= 0.8 || kspip1_m >= 1.0";
    auto reject_kstar_zero = "kmpip1_m <= 0.8 || kmpip1_m >= 1.0";

    // Apply cuts; make new dataframe
    auto cut_df = df2.Filter("pathlength_sig > 5")
                     .Filter(reject_delta)
                     .Filter(reject_lambda);
    
    
    
    // ********** HISTOGRAMS **********
    
    auto h1 = cut_df.Filter(reject_kstar_plus).Filter(keep_kstar_zero).Histo1D({"h1", "f1_m (aka pipkmks_m)", 30, 1.2, 1.7}, "f1_m");
    h1->SetLineColor(kBlack);
    //auto h2 = cut_df.Filter(keep_kstar_plus).Filter(keep_kstar_zero).Histo1D({"h2", "f1", 60, 1.1, 1.7}, "f1_m");
    // auto xMin = 1.0;
    // auto xMax = 1.8;
    // auto yMin = 0;
    // auto yMax = 15000;


    // ********** FITTING **********

    // // 'gaus(0)' is a substitute for: [0]*exp(-0.5*((x-[1])/[2])**2) and (0) means start numbering parameters at 0
    // std::unique_ptr<TF1> fitGaus = std::make_unique<TF1>("fitGaus", "gaus(0)", 1.2, 1.8);
    // fitGaus->SetParameter(0, 1500); // amplitude
    // fitGaus->SetParameter(1, 1.4); // ?
    // fitGaus->SetParameter(2, 0.05); // ?
    // fitGaus->SetLineColor(kCyan+3);
    // //h1->Fit(fitGaus.get());

    // // 'expo(3)' is a substitute for: exp([3]+[4]*x).  Not used here.
    // std::unique_ptr<TF1> fitExpo = std::make_unique<TF1>("fitExpo", "expo(3)", 1.2, 1.8);
    // fitExpo->SetParameter(3, 0.1); // ?
    // fitExpo->SetParameter(4, 1); // ?
    // fitExpo->SetLineColor(kGreen+3);
    // //h1->Fit(fitExpo.get());

    // // 'pol1(3)' is a substitute for: [3]+[4]*x ??need to check
    // std::unique_ptr<TF1> fitPol1 = std::make_unique<TF1>("fitPol1", "pol1(3)", 1.2, 1.8);
    // fitPol1->SetParameter(3, 0.1); // ?
    // fitPol1->SetParameter(4, 1); // ?
    // fitPol1->SetLineColor(kOrange-6);
    // h1->Fit(fitPol1.get());

    // // 'pol2(3)' is a substitute for: [3]+[4]*x+[5]*x*x
    // std::unique_ptr<TF1> fitPol2 = std::make_unique<TF1>("fitPol2", "pol2(3)", 1.2, 2.8);
    // fitPol2->SetParameter(3, 0.1); // ?
    // fitPol2->SetParameter(4, 1); // ?
    // fitPol2->SetParameter(5, 1); // ?
    // fitPol2->SetLineColor(kGreen-3);
    // h1->Fit(fitPol2.get(), "PBVR");

    // // 'breitwigner(0)' is a substitute for??: [0]/(pow(x*x-[1]*[1],2)+[1]*[1]*[2]*[2]) ? Need to check.
    // std::unique_ptr<TF1> fitBW = std::make_unique<TF1>("fitBW", "breitwigner(0)", 1.2, 2.8);
    // fitBW->SetParameter(0, 1000); // amplitude (put approx. 1/2 of total events, i.e. y-axis)
    // fitBW->SetParameter(1, 1.42); // mass
    // fitBW->SetParameter(2, 0.05); // width
    // fitBW->SetLineColor(kCyan-3);
    // h1->Fit(fitBW.get(), "B");

    // // // 'pol3()' is a substitute for: [0]+[1]*x+[2]*x*x+[3]*x*x*x ? Need to check.
    // std::unique_ptr<TF1> fitPol3 = std::make_unique<TF1>("fitPol3", "pol3()", 1.2, 1.7);

    // Next steps, Tyler Zoom 7/26/2023: 
    // Fix bw paremeters as above, then read off the poly parameters.
    // Then type those poly paremeters (and change 'SetParameter' to 'FixParamerer'), and let the BW parameters float.
    // Then read off the BW parameters.
    // Then set both using those newly gathered parameters, but let them all float, then see how the fit looks.
    // ...it should be better
    // Also, try using a 3rd order poly (instead of just a second-order, like I have now).

    // 8/31/2023 meeting: maybe change fit to exponential + breit-wigner (exp + bw), instead of poly + bw.
    // Define some custom functions from Tyler, line 91, 92:
    // https://github.com/tylerviducic/gluex/blob/main/scripts/fitting/root/relBW_f1_fit.py
    
    // Create exponential function, and pass a lambda function of the form: [0]+[1]*x+[2]*x*x inside.
    std::unique_ptr<TF1> bkg = std::make_unique<TF1>("bkg", "TMath::Exp([6] + [7] * x + [8] * x * x)", 1.2, 1.7);
    std::unique_ptr<TF1> bw1420 = std::make_unique<TF1>("bw1420", "TMath::BreitWigner(x, [4], [5])", 1.2, 1.7);
    bw1420->SetParameter(4, 1.42); // mass
    bw1420->SetParameter(5, 0.05); // width
    bkg->SetParameter(6, 1); // ?
    bkg->SetParameter(7, 1); // ?
    bkg->SetParameter(8, 1); // ?

    // fitFcnCombined->SetParameter(4, 1); //
    // fitFcnCombined->SetParameter(5, 1); //
    // fitFcnCombined->SetParameter(6, 1); //
    // fitFcnCombined->SetParameter(7, 1); //
    // fitFcnCombined->SetParameter(8, 1); // 
    // fitFcnCombined->SetLineColor(kMagenta);
    // h1->Fit(fitFcnCombined.get(), "RV"); // orig params: "PBRV"

    // // 'breitwigner(0)' is a substitute for??: [0]/(pow(x*x-[1]*[1],2)+[1]*[1]*[2]*[2]) ? Need to check.
    // // 'pol2(3)' is a substitute for: [3]+[4]*x+[5]*x*x ? Need to check.
    // std::unique_ptr<TF1> fitFcnCombined = std::make_unique<TF1>("fitFcnCombined", "breitwigner(0) + pol2(3) + bkg + bw1420", 1.2, 1.7);
    // fitFcnCombined->SetParameter(0, 145); // BW: amplitude (put approx. 1/2 of total events, i.e. y-axis) //old: 145
    // fitFcnCombined->SetParameter(1, 1.42); // BW: mass
    // fitFcnCombined->SetParameter(2, 0.0315); // BW: width
    // fitFcnCombined->SetParameter(3, -2.8E4); // Poly: ?
    // fitFcnCombined->SetParameter(4, 3.3E4); // Poly: ?
    // fitFcnCombined->SetParameter(5, -8.2E3); // Poly: ?
    // fitFcnCombined->SetLineColor(kMagenta);
    // h1->Fit(fitFcnCombined.get(), "RV"); // orig params: "PBRV"

    // ******** PRETTY MUCH DON'T NEED THE FITBWGETPAR AND FITPOL2GETPAR FUNCTIONS BELOW ********

    // // 'breitwigner(0)' is a substitute for??: [0]/(pow(x*x-[1]*[1],2)+[1]*[1]*[2]*[2]) ? Need to check.
    // // Just draw this on the histogram, without fitting it.  Note, it is only necessary to fit the combined function, since we know the histogram is more complex than just a Breit-Wigner.
    // std::unique_ptr<TF1> fitBWgetPar = std::make_unique<TF1>("fitBWgetPar", "breitwigner(0)", 1.2, 1.7);
    // fitBWgetPar->SetParameter(0, fitFcnCombined->GetParameter(0)); // amplitude (put approx. 1/2 of total events, i.e. y-axis)
    // fitBWgetPar->SetParameter(1, fitFcnCombined->GetParameter(1)); // mass
    // fitBWgetPar->SetParameter(2, fitFcnCombined->GetParameter(2)); // width
    // fitBWgetPar->SetLineColor(kCyan+2);
    
    // // 'pol2(3)' is a substitute for: [3]+[4]*x+[5]*x*x
    // // Just draw this on the histogram, without fitting it.  Note, it is only necessary fit the combined function, since we know the histogram is more complex than just a Polynomial.
    // std::unique_ptr<TF1> fitPol2getPar = std::make_unique<TF1>("fitPol2getPar", "pol2(3)", 1.2, 1.7);
    // fitPol2getPar->SetParameter(3, fitFcnCombined->GetParameter(3)); // ?
    // fitPol2getPar->SetParameter(4, fitFcnCombined->GetParameter(4)); // ?
    // fitPol2getPar->SetParameter(5, fitFcnCombined->GetParameter(5)); // ?
    // fitPol2getPar->SetLineColor(kGreen+2);
    
    // ******** PLOTTING ********

    std::shared_ptr<TCanvas> c1 = std::make_shared<TCanvas>("c1", "f1_m_fit", 800, 600);
    
    // h1->GetXaxis()->SetRangeUser(xMin,xMax);
    // h1->GetYaxis()->SetRangeUser(yMin,yMax);
    h1->Draw("E"); // "E"
    // fitPol1->Draw("same");
    // fitPol2->Draw("same");
    // fitGaus->Draw("same");
    // fitBW->Draw("same");
    // fitFcnCombined->Draw("same"); // bw + pol2
    // fitBWgetPar->Draw("same");
    // fitPol2getPar->Draw("same");
    bkg->Draw("same");
    
    auto legend1 = new TLegend(0.75, 0.77, .98, 0.58); //(x_topLeft, y_topLeft, x_bottomRight, y_bottomRight)
    legend1->AddEntry("h1", "Data: ks_m", "l");
    // legend1->AddEntry(fitPol1.get(), "fcn: fitPol1", "l");
    // legend1->AddEntry(fitGaus.get(), "fcn: fitGaus", "l");
    // legend1->AddEntry(fitFcnCombined.get(), "fcn: fit(bw + pol3)", "l");
    // legend1->AddEntry(fitBW.get(), "fcn: fitBW", "l");
    // legend1->AddEntry(fitBWgetPar.get(), "fcn: BW", "l");
    // legend1->AddEntry(fitPol2.get(), "fcn: fitPol2", "l");
    // legend1->AddEntry(fitPol2getPar.get(), "fcn: Pol2", "l");
    legend1->AddEntry(bkg.get(), "fcn: bkg", "l");
    legend1->Draw();

    c1->Update();
    c1->SaveAs("plots/f1_m_fit.png");

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