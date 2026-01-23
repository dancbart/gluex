from operator import le
import os
from re import T
import shutil
import time
import ROOT
ROOT.gROOT.SetBatch(True)  # don't pop up canvases with X11 (this script loads the pdf file instead).
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)
# ROOT.TGaxis.SetMaxDigits(3) # set scientific notation globally
# ROOT.TGaxis.SetExponentOffset(-0.05, 0.01, "y")  # (xoff, yoff, axis)


# -----------------------------
# Files
# -----------------------------
FND = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/fits/twopi_plot.root"

# INDICES ASSIGNED BY 'flatten':
# 1. DecayingLambda (0)   1a. Proton (1)   1b. PiMinus2 (2)
# 2. DecayingKShort (3)   2a. PiPlus2 (4)  2b. PiMinus1 (5)
# 3. PiPlus1 (6)

def gluex_style():
    style = ROOT.TStyle("GlueX", "Default GlueX Style")

    # Canvas / Pad
    style.SetCanvasBorderMode(0)
    style.SetPadBorderMode(0)
    style.SetPadColor(0)
    style.SetCanvasColor(0)
    style.SetTitleColor(0)
    style.SetStatColor(0)

    # Sizes
    style.SetCanvasDefW(800)
    style.SetCanvasDefH(600)
    style.SetPadBottomMargin(0.15)
    style.SetPadLeftMargin(0.20)
    style.SetPadTopMargin(0.05)
    style.SetPadRightMargin(0.08)

    # Axis
    style.SetStripDecimals(0)
    style.SetLabelSize(0.025, "xyz")
    style.SetTitleSize(0.06, "xyz")
    style.SetTitleFont(42, "xyz")
    style.SetLabelFont(42, "xyz")
    style.SetTitleOffset(1.2, "y")
    style.SetLabelOffset(0.08, "xyz")


    # Histograms
    style.SetOptStat(0)
    style.SetOptTitle(0)
    style.SetHistLineWidth(2)
    style.SetHistFillColor(920)  # grey

    # Palettes
    style.SetPalette(ROOT.kViridis)

    ROOT.gROOT.SetStyle("GlueX")
    ROOT.gROOT.ForceStyle()



NT = "ntFSGlueX_MODECODE"
treeName = "ntFSGlueX_100000000_1100"

# DecayingLambda = "1"
# Proton         = "1a"
# PiMinus2       = "1b"
# DecayingKShort = "2"
# PiPlus2        = "2a"
# PiMinus1       = "2b"
# PiPlus1        = "3"

# Toggle BGGEN overlays
bggen = False

def setup():
    startTime = time.time()
    gluex_style()
    # Early out if already configured
    if ROOT.FSModeCollection.modeVector().size() != 0:
        return
    # ROOT.FSHistogram.readHistogramCache()
    ROOT.FSModeCollection.addModeInfo("100000000_1100").addCategory("m100000000_1100")

    # -----------------------------
    # Plot output directory / file
    # -----------------------------
    # shutil.rmtree("plots", ignore_errors=True)
    # os.makedirs("plots", exist_ok=True)
    allPlots = "plots/sdme_plots.pdf"

    # -----------------------------
    # Histogram label
    # -----------------------------
    # label = "MC" if "gen_amp" in FND or "bggen" in FND else "Data"
    # lab1 = ROOT.TLatex()
    # lab1.SetNDC(True)
    # lab1.SetTextAlign(23)   # 23 = center/top
    # lab1.SetTextFont(62)    # bold
    # lab1.SetTextSize(0.045)

    # -----------------------------
    # Retrieve histogram(s)
    # -----------------------------

    file = ROOT.TFile.Open(FND)


    # --- Retrieve cosTheta histograms ---

    cosThetadat = file.Get("cosThetadat")
    if not cosThetadat:
        raise RuntimeError("Histogram 'cosThetadat' not found in file")
    cosThetadat = cosThetadat.Clone("cosThetadat") # Detach from file so it survives after close
    cosThetadat.SetDirectory(0)

    cosThetaacc_sdme = file.Get("cosThetaacc_sdme")
    if not cosThetaacc_sdme:
        raise RuntimeError("Histogram 'cosThetaacc_sdme' not found in file")
    cosThetaacc_sdme = cosThetaacc_sdme.Clone("cosThetaacc_sdme") # Detach from file so it survives after close
    cosThetaacc_sdme.SetDirectory(0)

    cosThetabkg_sdme = file.Get("cosThetabkg_sdme")
    if not cosThetabkg_sdme:
        raise RuntimeError("Histogram 'cosThetabkg_sdme' not found in file")
    cosThetabkg_sdme = cosThetabkg_sdme.Clone("cosThetabkg_sdme") # Detach from file so it survives after close
    cosThetabkg_sdme.SetDirectory(0)

    # --- Retrieve phi histograms ---

    phidat = file.Get("phidat")
    if not phidat:
        raise RuntimeError("Histogram 'phidat' not found in file")
    phidat = phidat.Clone("phidat")
    phidat.SetDirectory(0)

    phiacc_sdme = file.Get("phiacc_sdme")
    if not phiacc_sdme:
        raise RuntimeError("Histogram 'phiacc' not found in file")
    phiacc_sdme = phiacc_sdme.Clone("phiacc_sdme")
    phiacc_sdme.SetDirectory(0)

    phibkg_sdme = file.Get("phibkg_sdme")
    if not phibkg_sdme:
        raise RuntimeError("Histogram 'phibkg_sdme' not found in file")
    phibkg_sdme = phibkg_sdme.Clone("phibkg_sdme")
    phibkg_sdme.SetDirectory(0)

    # --- Retrieve Phi histograms ---

    Phidat = file.Get("Phidat")
    if not Phidat:
        raise RuntimeError("Histogram 'Phidat' not found in file")
    Phidat = Phidat.Clone("Phidat")
    Phidat.SetDirectory(0)

    Phiacc_sdme = file.Get("Phiacc_sdme")
    if not Phiacc_sdme:
        raise RuntimeError("Histogram 'Phiacc_sdme' not found in file")
    Phiacc_sdme = Phiacc_sdme.Clone("Phiacc_sdme")
    Phiacc_sdme.SetDirectory(0)

    Phibkg_sdme = file.Get("Phibkg_sdme")
    if not Phibkg_sdme:
        raise RuntimeError("Histogram 'Phibkg_sdme' not found in file")
    Phibkg_sdme = Phibkg_sdme.Clone("Phibkg_sdme")
    Phibkg_sdme.SetDirectory(0)

    file.Close()

    # ? What is "psiacc" do we use that?

    # -----------------------------
    # Canvas 1
    # -----------------------------
    c1 = ROOT.TCanvas("c1", "c1", 1600, 1200)
    # c1.Divide(1, 1)
    # c1.cd(1)

    cosThetadat.SetTitle("twopi_plot outputs")
    cosThetadat.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    cosThetadat.SetYTitle("Counts / bin?")
    cosThetadat.SetLineColor(ROOT.kBlack)
    cosThetadat.Draw("")

    # --- acc + bkg ---
    cosTheta_acc_plus_bkg = cosThetaacc_sdme.Clone("cosTheta_acc_plus_bkg")
    cosTheta_acc_plus_bkg.Add(cosThetabkg_sdme)
    cosTheta_acc_plus_bkg.SetLineColor(ROOT.kGreen-6)
    cosTheta_acc_plus_bkg.SetFillColorAlpha(ROOT.kGreen-2, 0.60)
    cosTheta_acc_plus_bkg.SetFillStyle(1001)
    cosTheta_acc_plus_bkg.Draw("hist same")

    cosThetabkg_sdme.SetLineColor(ROOT.kRed-6)
    cosThetabkg_sdme.SetFillColorAlpha(ROOT.kRed-4, 0.60)
    cosThetabkg_sdme.SetFillStyle(1001)  # solid fill
    cosThetabkg_sdme.Draw("hist same")

    # Integral(s) for legend
    int0 = cosThetadat.Integral()
    int1 = cosThetaacc_sdme.Integral()
    int2 = cosThetabkg_sdme.Integral()


    legend = ROOT.TLegend(0.70, 0.85, 0.94, 0.94)
    legend.AddEntry(cosThetadat, f"data. Integral: {int0:.0f}", "l")
    legend.AddEntry(cosThetaacc_sdme, f"accmc. Integral: {int1:.0f}", "l")
    legend.AddEntry(cosThetabkg_sdme, f"bkgmc. Integral: {int2:.0f}", "l")
    legend.Draw("same")

    c1.Print(f"{allPlots}(")  # open multipage PDF


    # -----------------------------
    # Canvas 2 phi angular plots
    # -----------------------------

    c2 = ROOT.TCanvas("c2", "c2", 1600, 1200)
    # c2.Divide(1, 1)
    # c2.cd(1)

    phidat.SetTitle("twopi_plot outputs")
    phidat.SetXTitle("#phi(rad) (Helicity frame)")
    phidat.SetYTitle("Counts / bin?")
    phidat.SetLineColor(ROOT.kBlack)
    phidat.Draw("")

    # --- acc + bkg ---
    phi_acc_plus_bkg = phiacc_sdme.Clone("phi_acc_plus_bkg")
    phi_acc_plus_bkg.Add(phibkg_sdme)
    phi_acc_plus_bkg.SetLineColor(ROOT.kGreen-6)
    phi_acc_plus_bkg.SetFillColorAlpha(ROOT.kGreen-2, 0.60)
    phi_acc_plus_bkg.SetFillStyle(1001)
    phi_acc_plus_bkg.Draw("hist same")

    phibkg_sdme.SetLineColor(ROOT.kRed-6)
    phibkg_sdme.SetFillColorAlpha(ROOT.kRed-4, 0.60)
    phibkg_sdme.SetFillStyle(1001)  # solid fill
    phibkg_sdme.Draw("hist same")

    # Integral(s) for legend
    int3 = phidat.Integral()
    int4 = phiacc_sdme.Integral()
    int5 = phibkg_sdme.Integral()


    legend = ROOT.TLegend(0.70, 0.85, 0.94, 0.94)
    legend.AddEntry(phidat, f"data. Integral: {int3:.0f}", "l")
    legend.AddEntry(phiacc_sdme, f"accmc. Integral: {int4:.0f}", "l")
    legend.AddEntry(phibkg_sdme, f"bkgmc. Integral: {int5:.0f}", "l")
    legend.Draw("same")

    c2.Print(allPlots)  # add to multipage PDF


    # -----------------------------
    # Canvas 3 Phi angular plots
    # -----------------------------

    c3 = ROOT.TCanvas("c3", "c3", 1600, 1200)
    # c3.Divide(1, 1)
    # c3.cd(1)

    Phidat.SetTitle("twopi_plot outputs")
    Phidat.SetXTitle("#Phi(rad) (Helicity frame)")
    Phidat.SetYTitle("Counts / bin?")
    Phidat.SetLineColor(ROOT.kBlack)
    Phidat.Draw("")

    # --- acc + bkg ---
    Phi_acc_plus_bkg = Phiacc_sdme.Clone("Phi_acc_plus_bkg")
    Phi_acc_plus_bkg.Add(Phibkg_sdme)
    Phi_acc_plus_bkg.SetLineColor(ROOT.kGreen-6)
    Phi_acc_plus_bkg.SetFillColorAlpha(ROOT.kGreen-2, 0.60)
    Phi_acc_plus_bkg.SetFillStyle(1001)
    Phi_acc_plus_bkg.Draw("hist same")

    Phibkg_sdme.SetLineColor(ROOT.kRed-6)
    Phibkg_sdme.SetFillColorAlpha(ROOT.kRed-4, 0.60)
    Phibkg_sdme.SetFillStyle(1001)  # solid fill
    Phibkg_sdme.Draw("hist same")

    # Integral(s) for legend
    int6 = Phidat.Integral()
    int7 = Phiacc_sdme.Integral()
    int8 = Phibkg_sdme.Integral()


    legend = ROOT.TLegend(0.70, 0.85, 0.94, 0.94)
    legend.AddEntry(Phidat, f"data. Integral: {int6:.0f}", "l")
    legend.AddEntry(Phiacc_sdme, f"accmc. Integral: {int7:.0f}", "l")
    legend.AddEntry(Phibkg_sdme, f"bkgmc. Integral: {int8:.0f}", "l")
    legend.Draw("same")

    c3.Print(allPlots)

     # -----------------------------
    # Canvas 4 Phi MINUS phi angular plots
    # -----------------------------

    c4 = ROOT.TCanvas("c4", "c4", 1600, 1200)
    # c4.Divide(1, 1)
    # c4.cd(1)

    PhidatMINUSphi = Phidat.Clone("PhidatMINUSphi")
    PhidatMINUSphi.Add(phidat, -1)
    PhidatMINUSphi.SetTitle("twopi_plot outputs")
    PhidatMINUSphi.SetXTitle("#Phi(rad) - #phi(rad) (Helicity frame)")
    PhidatMINUSphi.SetYTitle("Counts / bin?")
    PhidatMINUSphi.SetLineColor(ROOT.kBlack)
    PhidatMINUSphi.Draw("")

    # --- acc + bkg ---
    PhiMINUSphi = Phiacc_sdme.Clone("PhiMINUSphi")
    PhiMINUSphi.Add(phiacc_sdme, -1)
    PhiMINUSphi.SetLineColor(ROOT.kGreen-6)
    PhiMINUSphi.SetFillColorAlpha(ROOT.kGreen-2, 0.60)
    PhiMINUSphi.SetFillStyle(1001)
    PhiMINUSphi.Draw("hist same")

    PhibkgMINUSbkg = Phibkg_sdme.Clone("PhibkgMINUSbkg")
    PhibkgMINUSbkg.Add(phibkg_sdme, -1)
    PhibkgMINUSbkg.SetLineColor(ROOT.kRed-6)
    PhibkgMINUSbkg.SetFillColorAlpha(ROOT.kRed-4, 0.60)
    PhibkgMINUSbkg.SetFillStyle(1001)  # solid fill
    PhibkgMINUSbkg.Draw("hist same")


    # Integral(s) for legend
    int9 = PhidatMINUSphi.Integral()
    int10 = PhiMINUSphi.Integral()
    int11 = PhibkgMINUSbkg.Integral()


    legend = ROOT.TLegend(0.70, 0.85, 0.94, 0.94)
    legend.AddEntry(PhidatMINUSphi, f"data. Integral: {int9:.0f}", "l")
    legend.AddEntry(PhiMINUSphi, f"accmc. Integral: {int10:.0f}", "l")
    legend.AddEntry(PhibkgMINUSbkg, f"bkgmc. Integral: {int11:.0f}", "l")
    legend.Draw("same")

    c4.Print(f"{allPlots})")  # close multipage PDF

    endTime = time.time()
    print(f"Time to run: {endTime - startTime:.1f} seconds")

if __name__ == "__main__":
    setup()