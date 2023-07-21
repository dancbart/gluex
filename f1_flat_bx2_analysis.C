void f1_flat_bx2_analysis() {

    ROOT::RDataFrame df("pipkmks__B4_M16", "pipkmks_flat_bestX2_2017.root");

    // Define resonances, add columns to dataframe for each (using '.Define')
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

    // Cuts
    auto reject_delta = "pip1p_m > 1.4"; // delta++ cut
    auto reject_lambda = "pkm_m > 1.9"; // lambda cut
    auto keep_kstar_plus = "kspip1_m >= 0.8 && kspip1_m <= 1.0";
    auto keep_kstar_zero = "kmpip1_m >= 0.8 && kmpip1_m <= 1.0";
    auto reject_kstar_plus = "kspip1_m <= 0.8 || kspip1_m >= 1.0";
    auto reject_kstar_zero = "kmpip1_m <= 0.8 || kmpip1_m >= 1.0";

    auto cut_df = df2.Filter("pathlength_sig > 5");
                     //.Filter(reject_delta);
                     //.Filter(reject_lambda);
    
    // Making Histogram
    auto h1 = cut_df.Histo1D({"h1", "ks_m (pip2pim_m)", 300, 0.3, 0.7}, "ks_m");
    //auto h2 = cut_df.Filter(keep_kstar_plus).Filter(keep_kstar_zero).Histo1D({"h2", "f1", 60, 1.1, 1.7}, "f1_m");
    //auto xMin = 1.0;
    //auto xMax = 5.0;
    //auto yMin = 0;
    //auto yMax = 12500;

    // Function fits
    // std::unique_ptr<TF1> fitFcn1 = std::make_unique<TF1>("fitFcn1", "gaus", 0.3, 0.7);
    // fitFcn->SetNpx(500);
    // fitFcn->SetLineWidth(2);
    // fitFcn1->SetLineColor(kMagenta);
    // h1->Fit(fitFcn1.get(), "R");

    // std::unique_ptr<TF1> fitFcn2 = std::make_unique<TF1>("fitFcn2", "pol1", 0.3, 0.7);
    // fitFcn2->SetNpx(500);
    // fitFcn2->SetLineWidth(2);
    // fitFcn2->SetLineColor(kBlack);
    // h1->Fit(fitFcn2.get(), "R");

    // Build composite fit function
    // 'gaus(0)' is a substitute for: [0]*exp(-0.5*((x-[1])/[2])**2) and (0) means start numbering parameters at 0
    // 'expo(3)' is a substitute for: exp([3]+[4]*x)
    // 'pol1(3)' is a substitute for: [3]+[4]*x ??need to check
    // std::unique_ptr<TF1> fitFcn3 = std::make_unique<TF1>("fitFcn3", "gaus(0)*expo(3)", 0.3, 0.7);
    std::unique_ptr<TF1> fitFcn3 = std::make_unique<TF1>("fitFcn3", "gaus(0) + pol1(3)", 0.3, 0.7);
    fitFcn3->SetParameter(0, 30000);
    fitFcn3->SetParameter(1, 0.55);
    fitFcn3->SetParameter(2, 0.011);
    fitFcn3->SetParameter(3, 0.1);
    fitFcn3->SetParameter(4, 1);
    fitFcn3->SetLineColor(kRed);
    h1->Fit(fitFcn3.get());

    // Painting canvas
    std::shared_ptr<TCanvas> c1 = std::make_shared<TCanvas>("Canvas1", "ks_m_fitGauss", 800, 600); //Draw the histogram on a canvas
    h1->SetLineColor(kBlue);
    //h1->GetXaxis()->SetRangeUser(xMin,xMax);
    //h1->GetYaxis()->SetRangeUser(yMin,yMax);
    h1->Draw();
    // fitFcn1->Draw("same");
    // fitFcn2->Draw("same");    
    fitFcn3->Draw("same");
    
    auto legend1 = new TLegend(0.15, 0.95, .35, 0.85); //(x_topLeft, y_topLeft, x_bottomRight, y_bottomRight)
    legend1->AddEntry("h1", "ks_m", "l");
    // legend1->AddEntry(fitFcn1.get(), "fit: gaus", "l");
    // legend1->AddEntry(fitFcn2.get(), "fit: pol1", "l");
    legend1->AddEntry(fitFcn3.get(), "fit: gaus + pol1", "l");
    legend1->Draw();

    c1->Update();
    c1->SaveAs("plots/f1_m_fit.png");
}

int main() {
    f1_flat_bx2_analysis();
    return 0;
}