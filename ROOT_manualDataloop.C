void ROOT_manualDataloop(){
    auto cnt_r_h=new TH1F("count_rate", //Q: so I can't use this histogram since it was already instantiated in this argument.  But, what would be an example of reusing such a histogram, like in an RDataFrame, say?
                "Count Rate;N_{Counts};# occurencies",
                100, // Number of Bins
                -0.5, // Lower X Boundary
                15.5); // Upper X Boundary

    auto mean_count=3.6f;
    TRandom3 rndgen;
    // simulate the measurements
    for (int imeas=0;imeas<400;imeas++)
        cnt_r_h->Fill(rndgen.Poisson(mean_count));

    // Draw the histogram on a canvas:
    TCanvas* canv = new TCanvas("Canvas", "Randomly Filled Histogram", 800, 600);
    cnt_r_h->Draw();
    canv->Update();
    canv->SaveAs("randFill.png");
}

int main() {
    ROOT_manualDataloop();
    return 0;
}