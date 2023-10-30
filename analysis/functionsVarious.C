
std::unique_ptr<TF1> bw = std::make_unique<TF1>("bw", "breitwigner(0)", 1.2, 1.7);
bw->SetParName(0, "bw_amplitude");
bw->SetParName(1, "bw_mass");
bw->SetParName(2, "bw_width");
bw->SetParameter("bw_amplitude", fitFcnCombined->GetParameter(0)); //
bw->SetParameter("bw_mass", fitFcnCombined->GetParameter(1)); //
bw->SetParameter("bw_width", fitFcnCombined->GetParameter(2)); //
bw->SetLineColor(kGreen);
bw->SetLineWidth(2);
bw->SetLineStyle(2);
std::unique_ptr<TF1> pol2 = std::make_unique<TF1>("pol2", "pol2(3)", 1.2, 1.7);
pol2->SetParName(3, "pol2_par1");
pol2->SetParName(4, "pol2_par2");
pol2->SetParName(5, "pol2_par3");
pol2->SetParameter("pol2_par1", fitFcnCombined->GetParameter(3)); //
pol2->SetParameter("pol2_par2", fitFcnCombined->GetParameter(4)); //
pol2->SetParameter("pol2_par3", fitFcnCombined->GetParameter(5)); //
pol2->SetLineColor(kCyan);
pol2->SetLineWidth(2);
pol2->SetLineStyle(2);

// 'breitwigner(0)' is a substitute for??: [0]/(pow(x*x-[1]*[1],2)+[1]*[1]*[2]*[2]) ? Need to check.
'pol2(3)' is a substitute for: [3]+[4]*x+[5]*x*x

// 'gaus(0)' is a substitute for: [0]*exp(-0.5*((x-[1])/[2])**2) and (0) means start numbering parameters at 0
std::unique_ptr<TF1> fitGaus = std::make_unique<TF1>("fitGaus", "gaus(0)", 1.2, 1.8);

// 'expo(3)' is a substitute for: exp([3]+[4]*x).  Not used here.
std::unique_ptr<TF1> fitExpo = std::make_unique<TF1>("fitExpo", "expo(3)", 1.2, 1.8);

// 'pol1(3)' is a substitute for: [3]+[4]*x ??need to check
std::unique_ptr<TF1> fitPol1 = std::make_unique<TF1>("fitPol1", "pol1(3)", 1.2, 1.8);

// 'pol2(3)' is a substitute for: [3]+[4]*x+[5]*x*x
std::unique_ptr<TF1> fitPol2 = std::make_unique<TF1>("fitPol2", "pol2(3)", 1.2, 2.8);

std::unique_ptr<TF1> bkg = std::make_unique<TF1>("bkg", "TMath::Exp([0] + [1] * x + [2] * x * x)", 1.2, 1.7);
bkg->SetParName(0, "bkg_expPar1");
bkg->SetParName(1, "bkg_expPar2");
bkg->SetParName(2, "bkg_expPar3");

std::unique_ptr<TF1> bw1420 = std::make_unique<TF1>("bw1420", "breitwigner(0)", 1.2, 1.7); // used to have BreitWigner(x, [4], [5])
bw1420->SetParName(0, "bw1420_amplitude");
bw1420->SetParName(1, "bw1420_mass");
bw1420->SetParName(2, "bw1420_width");

std::unique_ptr<TF1> voigtian = std::make_unique<TF1>("voigtian", "TMath::Voigt(x, [0], [1], [2])", 1.2, 1.7);
voigtian->SetParName(0, "voigtian_sigma");
voigtian->SetParName(1, "voigtian_lg");
voigtian->SetParName(2, "voigtian_r");

// I think this is a RooFit function. It doesn't work with ROOT i guess.
std::unique_ptr<RooRealVar> x = std::make_unique<RooRealVar>("x", "x", 1.2, 1.5);
std::unique_ptr<RooRealVar> mean = std::make_unique<RooRealVar>("mean", "mean", 1.285, 1.283, 1.287);
std::unique_ptr<RooRealVar> width = std::make_unique<RooRealVar>("width", "width", 0.022, 0.001, 0.1);
std::unique_ptr<RooRealVar> sigma = std::make_unique<RooRealVar>("sigma", "sigma", 0.3, 0.001, 0.1);
// Create a Voigtian
std::unique_ptr<RooVoigtian> voigt = std::make_unique<RooVoigtian>("voigt", "voigtian PDF", *x, *mean, *width, *sigma);
