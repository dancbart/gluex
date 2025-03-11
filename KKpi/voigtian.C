
// Minimum working example
// https://root-forum.cern.ch/t/voigt-function-with-parameter-which-depends-on-energy/39139/2

void f(){
  TF1 *f = new TF1("f", "TMath::Voigt(x - [0], [1], [2], 4)", -10., 10.);
  f->SetParameters(3., 2., 1.); // median, sigma, lg
  f->Draw();
}

int voigt()
{
  f();
  return 0;
}