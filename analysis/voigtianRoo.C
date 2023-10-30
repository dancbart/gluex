// this is pieced together and may not run.  Also, it mixes up ROOT and RuFit which aren't friendly.
void callRooVoigtian() {
    std::unique_ptr<RooRealVar> x = std::make_unique<RooRealVar>("x", "x", 1.2, 1.5);
    std::unique_ptr<RooRealVar> mean = std::make_unique<RooRealVar>("mean", "mean", 1.285, 1.283, 1.287);
    std::unique_ptr<RooRealVar> width = std::make_unique<RooRealVar>("width", "width", 0.022, 0.001, 0.1);
    std::unique_ptr<RooRealVar> sigma = std::make_unique<RooRealVar>("sigma", "sigma", 0.3, 0.001, 0.1);
    // Create a Voigtian
    std::unique_ptr<RooVoigtian> voigt = std::make_unique<RooVoigtian>("voigt", "voigtian PDF", *x, *mean, *width, *sigma);

}

int rooVooigtian() {
  callRooVoigtian();
  return 0;
}
