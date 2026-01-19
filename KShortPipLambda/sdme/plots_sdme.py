from operator import le
import os
from re import T
import shutil
import time
# from xml.etree.ElementTree import PI
import ROOT
ROOT.gROOT.SetBatch(True)  # don't pop up canvases with X11 (this script loads the pdf file instead).
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)
ROOT.TGaxis.SetMaxDigits(3) # set scientific notation globally
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


    file.Close()


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

    # cosThetaacc_sdme.SetLineColor(ROOT.kGreen-6)
    # cosThetaacc_sdme.SetFillColorAlpha(ROOT.kGreen-2, 0.60)
    # cosThetaacc_sdme.Draw("hist same")

    # Integral(s) for legend
    int0 = cosThetadat.Integral()
    int1 = cosThetaacc_sdme.Integral()
    int2 = cosThetabkg_sdme.Integral()


    legend = ROOT.TLegend(0.70, 0.85, 0.94, 0.94)
    legend.AddEntry(cosThetadat, f"data. Integral: {int0:.0f}", "l")
    legend.AddEntry(cosThetaacc_sdme, f"accmc. Integral: {int1:.0f}", "l")
    legend.AddEntry(cosThetabkg_sdme, f"bkgmc. Integral: {int2:.0f}", "l")
    legend.Draw("same")

    c1.Print(f"{allPlots}(") # open multipage pdf


    # -----------------------------
    # Retrieve histogram(s)
    # -----------------------------

    file = ROOT.TFile.Open(FND)

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


    file.Close()

    # -----------------------------
    # Canvas 2
    # -----------------------------
    c2 = ROOT.TCanvas("c2", "c2", 1600, 1200)
    # c2.Divide(1, 1)
    # c2.cd(1)

    cosThetadat.SetTitle("twopi_plot outputs")
    cosThetadat.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    cosThetadat.SetYTitle("Counts / bin?")
    cosThetadat.SetLineColor(ROOT.kBlack)
    cosThetadat.Draw("")

    cosThetaacc_sdme.SetLineColor(ROOT.kGreen-6)
    cosThetaacc_sdme.SetFillColorAlpha(ROOT.kGreen-2, 0.60)
    cosThetaacc_sdme.Draw("hist same")

    cosThetabkg_sdme.SetLineColor(ROOT.kRed-6)
    cosThetabkg_sdme.SetFillColorAlpha(ROOT.kRed-4, 0.60)
    cosThetabkg_sdme.SetFillStyle(1001)  # solid fill
    cosThetabkg_sdme.Draw("hist same")

    # Integral(s) for legend
    int3 = cosThetadat.Integral()
    int4 = cosThetaacc_sdme.Integral()
    int5 = cosThetabkg_sdme.Integral()


    legend = ROOT.TLegend(0.70, 0.85, 0.94, 0.94)
    legend.AddEntry(cosThetadat, f"data. Integral: {int3:.0f}", "l")
    legend.AddEntry(cosThetaacc_sdme, f"accmc. Integral: {int4:.0f}", "l")
    legend.AddEntry(cosThetabkg_sdme, f"bkgmc. Integral: {int5:.0f}", "l")
    legend.Draw("same")

    c2.Print(f"{allPlots})") # close multipage pdf

    endTime = time.time()
    print(f"Time to run: {endTime - startTime:.1f} seconds")

if __name__ == "__main__":
    setup()
