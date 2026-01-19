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
# SMALL FILE (same dataset, but only 3-4 runs)
# FND = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_small.root"
# MONTE CARLO
# FND = "/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__sp-fa18_B4_M16_M18_gen_amp_V2_FSflat_REACTIONFILTER-ONLY.root"

# MONTE CARLO - use this if you want to plot DATA and MC in the same script
FND_MC = "/volatile/halld/home/dbarton/pipkslamb/mc_eventSelection/fall2018/root/trees/flatten/tree_pipkslamb__sp-fa18_B4_M16_M18_gen_amp_V2_FSflat_REACTIONFILTER-ONLY.root"

# Basic plots for flattened and skimmed DATA trees:
# FND = "/work/halld/gluex_workshop_data/tutorial_2022/session2d/skim/tree_pi0eta__B4_M17_M7_DATA_sp17_*_GENERAL_SKIM.root"

# Basic plots for flattened MC trees:
# FND = "/work/halld/gluex_workshop_data/tutorial_2022/session2d/flatten/flatMC/tree_pi0eta__B4_M17_M7_FLAT_MC.root"

# Basic plots for flattened BGGEN MC trees:
# FND = "/work/halld/gluex_workshop_data/tutorial_2022/session2d/flatten/bggen/tree_pi0eta__B4_M17_M7_*.root"

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
    plotsFileName = "plots/eventSelection_plots.pdf"

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
    # ROOT.FSCut.defineCut("tRange", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "0.1", "1.0")

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


    baseCuts = "tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385"
    sidebandCuts = "rf,KShort,Lambda"
    sidebandCutsMC = "KShort,Lambda"
    signalCuts_THROWN = "tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN"

    # -----------------------------
    # Canvas 1 FINAL STATE PARTICLE MASS PLOTS: signal before and after sideband weighting (various methods CUT, CUTSB, CUTSBWT, CUTSUB, CUTWT)
    # -----------------------------
    
    # Explanation of cut methods:

    # CUT(base, sideband)
    #     logical AND of signal region(s) in `base` and `sideband` cuts, weight = 1
    #     yields not sideband-subtracted signal distribution
    # CUT(base) && CUTSB(sideband)
    #     logical AND of signal region(s) in `base` cut(s) and all sideband regions in `sideband` cut(s)
    #     histograms are scaled with sideband weights and summed
    #     yields sideband distribution that is subtracted from signal distribution
    # CUT(base) * CUTSBWT(sideband)
    #     equivalent to above; but the sideband weights are baked into cut string and only a single histogram is created
    #     NOTE! applying weights in TFormulas does not work with RDataFrame
    # CUT(base) && CUTSUB(sideband)
    #     selects signal region(s) defined by `base` and `sideband` cut(s) and subtracts sideband regions in `sideband` cut(s)
    #     the sideband histograms are scaled with the corresponding sideband weight and summed
    #     summed sideband histograms are subtracted from signal histogram to yield sideband-subtracted distribution
    # CUT(base) * CUTWT(sideband)
    #     equivalent to above; but the sideband weights are baked into cut string and only a single sideband histogram is created
    #     equivalent to CUT(base, sideband) - CUT(base) * CUTSBWT(sideband)
    #     NOTE! applying weights in TFormulas does not work with RDataFrame

    c1 = ROOT.TCanvas("c1", "c1", 1600, 1200)
    c1.Divide(1, 1)

    c1.cd(1)
    hKShort0 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.35,0.65)", f"CUT({baseCuts})")
    hKShort1 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.35,0.65)", f"CUT({baseCuts},{sidebandCuts})")
    hKShort2 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.35,0.65)", f"CUT({baseCuts})&&CUTSB({sidebandCuts})")
    hKShort3 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.35,0.65)", f"CUT({baseCuts})*CUTSBWT({sidebandCuts})")
    hKShort4 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.35,0.65)", f"CUT({baseCuts})&&CUTSUB({sidebandCuts})")
    hKShort5 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.35,0.65)", f"CUT({baseCuts})*CUTWT({sidebandCuts})")
    hKShort0.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    hKShort0.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    hKShort0.SetLineColor(ROOT.kBlack)
    hKShort0.SetYTitle("Counts / 5 MeV")
    hKShort0.SetMinimum(0.0)
    hKShort0.Draw()
    hKShort1.SetLineColor(ROOT.kOrange+7)
    hKShort1.SetFillColor(ROOT.kOrange+7)
    hKShort1.SetFillStyle(3004)
    hKShort1.Draw("same hist")
    hKShort2.SetLineColor(ROOT.kRed)
    hKShort2.SetFillColor(ROOT.kRed)
    hKShort2.Draw("same hist")
    hKShort3.SetLineColor(ROOT.kBlue)
    hKShort3.SetFillColor(ROOT.kBlue)
    hKShort3.SetFillStyle(3005)
    hKShort3.Draw("same hist")
    hKShort4.SetLineColor(ROOT.kMagenta)
    hKShort4.SetFillColor(ROOT.kMagenta)
    hKShort4.Draw("same hist")
    hKShort5.SetLineColor(ROOT.kGreen+2)
    hKShort5.SetFillColor(ROOT.kGreen+2)
    hKShort5.SetFillStyle(3006)
    hKShort5.Draw("same hist")

    # compute integrals for legend
    int0 = hKShort0.Integral()
    int1 = hKShort1.Integral()
    int2 = hKShort2.Integral()
    int3 = hKShort3.Integral()
    int4 = hKShort4.Integral()
    int5 = hKShort5.Integral()

    legendKShort = ROOT.TLegend(0.62, 0.62, 0.94, 0.85)
    legendKShort.AddEntry(hKShort0, "Cut used: integral" , "")
    legendKShort.AddEntry(hKShort0, f"CUT(base): {int0:.0f}" , "l")
    legendKShort.AddEntry(hKShort1, f"CUT(base, sideband): {int1:.0f}", "l")
    legendKShort.AddEntry(hKShort2, f"CUT(base) && CUTSB(sideband): {int2:.0f}", "l")
    legendKShort.AddEntry(hKShort3, f"CUT(base) * CUTSBWT(sideband): {int3:.0f}", "l")
    legendKShort.AddEntry(hKShort4, f"CUT(base) && CUTSUB(sideband): {int4:.0f}", "l")
    legendKShort.AddEntry(hKShort5, f"CUT(base) * CUTWT(sideband): {int5:.0f}", "l")
    legendKShort.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()


    c1.Print(plotsFileName)  # middle pages


    # -----------------------------
    # Canvas 1 K* MASS PLOTS: signal before and after sideband weighting (various methods CUT, CUTSB, CUTSBWT, CUTSUB, CUTWT)
    # -----------------------------

    # c2 = ROOT.TCanvas("c2", "c2", 800, 600)
    # c2.Divide(1, 1)

    # c2.cd(1)
    # hMKShortpi = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,KShort,Lambda)")
    # hMKShortpi.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    # hMKShortpi.SetXTitle("M(K_{s} #pi^{+})  [GeV/c^{2}]")
    # hMKShortpi.SetYTitle("Counts / 20 MeV")
    # hMKShortpi.SetMinimum(0.0)
    # hMKShortpi.Draw()
    # lab1.DrawLatex(0.5, 1.00, f"{label}")
    # ROOT.gPad.Update()
    # legend = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    # legend.AddEntry(hMKShortpi, "Data", "l")
    # legend.Draw("same")

    # c2.Print(plotsFileName)  # middle pages

    endTime = time.time()
    print(f"Time to run: {endTime - startTime:.1f} seconds")

if __name__ == "__main__":
    setup()
