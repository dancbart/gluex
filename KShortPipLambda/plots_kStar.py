from operator import le
import os
from re import T
import shutil
import time
# from xml.etree.ElementTree import PI
import ROOT
ROOT.gROOT.SetBatch(True)  # don't pop up canvases with X11
from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)
ROOT.TGaxis.SetMaxDigits(3) # set scientific notation globally
# ROOT.TGaxis.SetExponentOffset(-0.05, 0.01, "y")  # (xoff, yoff, axis)


# -----------------------------
# File options (pick one)
# -----------------------------
# BIG FILE
FND = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root"
# MONTE CARLO - use this if you want to plot DATA and MC in the same script
FND_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"


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

DecayingLambda = "1"
Proton         = "1a"
PiMinus2       = "1b"
DecayingKShort = "2"
PiPlus2        = "2a"
PiMinus1       = "2b"
PiPlus1        = "3"

# Toggle BGGEN overlays
bggen = False

def setup():
    startTime = time.time()
    # include the gluex_style
    gluex_style()
    # Early out if already configured
    if ROOT.FSModeCollection.modeVector().size() != 0:
        return
    # ROOT.FSHistogram.readHistogramCache()
    ROOT.FSModeCollection.addModeInfo("100000000_1100").addCategory("m100000000_1100")

    # -----------------------------
    # Output directory / file
    # -----------------------------
    shutil.rmtree("plots", ignore_errors=True)
    os.makedirs("plots", exist_ok=True)
    allPlots = "plots/plots_kStar.pdf"

    # -----------------------------
    # Histogram label
    # -----------------------------
    label = "MC" if "gen_amp" in FND or "bggen" in FND else "Data"
    lab1 = ROOT.TLatex()
    lab1.SetNDC(True)
    lab1.SetTextAlign(23)   # 23 = center/top
    lab1.SetTextFont(62)    # bold
    lab1.SetTextSize(0.045)


    # mand t CUTS:
    ROOT.FSCut.defineCut("tRange", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")

    # STATIC CUTS
    ROOT.FSCut.defineCut("rf", "abs(RFDeltaT)>2.0", "abs(RFDeltaT)>6.0", 0.1667)
    ROOT.FSCut.defineCut("chi2DOF", "Chi2DOF<5.0")
    ROOT.FSCut.defineCut("unusedE", "EnUnusedSh<0.1")
    ROOT.FSCut.defineCut("unusedTracks", "NumUnusedTracks<1")
    ROOT.FSCut.defineCut("coherentPeak", "EnPB>8.2 && EnPB<8.8")
    ROOT.FSCut.defineCut("flightLengthLambda", "VeeLP1>2.0")
    ROOT.FSCut.defineCut("flightLengthKShort", "VeeLP2>2.0")
    ROOT.FSCut.defineCut("targetZ", "ProdVz>52.0 && ProdVz<78.0")

    # CUTS WITH SIDEBANDS
    ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0,)
    ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0,)
    ROOT.FSCut.defineCut("selectKSTAR892", f"MASS({DecayingKShort},{PiPlus1})>0.80 && MASS({DecayingKShort},{PiPlus1})<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})>2.0 && MASS({DecayingLambda},{PiPlus1})<4.0")
    # ROOT.FSCut.defineCut("selectKSTAR1430", f"MASS({DecayingKShort},{PiPlus1})", "0.85", "0.95", "0.0", "0.85", "0.95", "1.0",)


    # -----------------------------
    # Canvas 3a K* DATA vs MC
    # -----------------------------
    c3b = ROOT.TCanvas("c3b", "c3b", 800, 600)

    hMKShortpiSig = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    hMKShortpiSig.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig.SetYTitle("Events")
    hMKShortpiSig.SetLineColor(ROOT.kBlack)
    hMKShortpiSig.SetLineWidth(2)
    hMKShortpiSig.SetMarkerStyle(20)
    hMKShortpiSig.SetMarkerSize(0.8)
    hMKShortpiSig.DrawClone("E1")

    hMKShortpiSig_MC = ROOT.FSModeHistogram.getTH1F(FND_MC, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    hMKShortpiSig_MC.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig_MC.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig_MC.SetYTitle("Events")
    hMKShortpiSig_MC.SetLineColor(ROOT.kRed)
    hMKShortpiSig_MC.SetLineWidth(2)
    hMKShortpiSig_MC.SetMarkerStyle(24)
    hMKShortpiSig_MC.SetMarkerColor(ROOT.kRed)
    hMKShortpiSig_MC.SetMarkerSize(0.8)
    hMKShortpiSig_MC.Scale(0.012)
    hMKShortpiSig_MC.Draw("E1 same")

    lab1.DrawLatex(0.5, 1.00, f"{label}")    
    legend3a = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend3a.AddEntry(hMKShortpiSig, "Data", "pl")
    legend3a.AddEntry(hMKShortpiSig_MC, "Signal MC", "pl")
    legend3a.Draw("same")
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    print(hMKShortpiSig.Integral())

    c3b.Print(allPlots)  # middle pages



    # ROOT.FSHistogram.dumpHistogramCache("kspiplamb_plots_v2")

    endTime = time.time()
    print(f"Time to run: {endTime - startTime:.1f} seconds")

if __name__ == "__main__":
    setup()
