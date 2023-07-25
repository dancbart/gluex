// Prints the color wheel with the recommended 216 colors for web applications.
// https://root.cern.ch/doc/master/classTColor.html#C01

void colorWheel() {

    // Create the Color Wheel
    std::unique_ptr<TColorWheel> w = std::make_unique<TColorWheel>(); // Smart pointer method
    // TColorWheel *w = new TColorWheel(); // Raw pointer method
    
    // Create the canvas
    auto cw = new TCanvas("cw", "cw",0,0,400,400);
    w->SetCanvas(cw);
    w->Draw();

    cw->SaveAs("colorWheel.png");

};

int main() {
    colorWheel();
    return(0);
}