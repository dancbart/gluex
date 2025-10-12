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
FND_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/genamp2/fall2018_SBT_test2/root/trees/flatten/tree_pipkslamb__sp-fa18_B4_M16_M18_gen_amp_V2_FSflat_REACTIONFILTER-ONLY.root"

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
    allPlots = "plots/all_plots.pdf"

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
    # ROOT.FSCut.defineCut("tRange", f"(abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda})-0.5)<0.5)")
    ROOT.FSCut.defineCut("tRange", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "0.1", "1.0")


    # STATIC CUTS
    ROOT.FSCut.defineCut("rf", "OR(abs(RFDeltaT)<2.0)", "abs(RFDeltaT)>6.0", 0.1667)
    ROOT.FSCut.defineCut("chi2DOF", "Chi2DOF", "0.0", "5.0")
    ROOT.FSCut.defineCut("unusedE", "EnUnusedSh<0.1")
    ROOT.FSCut.defineCut("unusedTracks", "NumUnusedTracks<1")  # No unused tracks
    ROOT.FSCut.defineCut("coherentPeak", "EnPB", "8.2", "8.8")  # Coherent peak: 8.2 < E_beam < 8.8
    ROOT.FSCut.defineCut("flightLengthLambda", "VeeLP1>2.0")
    ROOT.FSCut.defineCut("flightLengthKShort", "VeeLP2>2.0")
    ROOT.FSCut.defineCut("targetZ", "ProdVz", "52.0", "78.0")  # target z position cut

    # CUTS WITH SIDEBANDS
    ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0,)
    ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0,)
    ROOT.FSCut.defineCut("selectKSTAR892", f"MASS({DecayingKShort},{PiPlus1})", "0.80", "1.00",)
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})", "2.0", "4.0",) # remove Sigma(1385) and higher
    # ROOT.FSCut.defineCut("selectKSTAR1430", f"MASS({DecayingKShort},{PiPlus1})", "0.85", "0.95", "0.0", "0.85", "0.95", "1.0",)


    # -----------------------------
    # Canvas 1 BASIC CUT VARIABLES
    # -----------------------------
    c1 = ROOT.TCanvas("c1", "c1", 1600, 1200)
    c1.Divide(3, 3)

    c1.cd(1)
    h1 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "EnUnusedSh", "(100,0.0,1.0)", "CUT(tRange,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)")
    h1.SetTitle("E_{unused} for -t in (0.0,1.0)")
    h1.SetXTitle("E_{unused}  [GeV/c^{2}]")
    h1.SetYTitle("Events (log)")
    ROOT.gPad.SetLogy(1)
    h1.SetMinimum(0.5)
    h1.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    cutUnusedE = ROOT.TLine(0.1, 0, 0.1, h1.GetMaximum())
    cutUnusedE.SetLineColor(ROOT.kRed)
    cutUnusedE.Draw("same")
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "EnUnusedSh", "(100,0.0,1.0)", "CUT(tRange,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)")

    c1.cd(2)
    h2 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "ProdVz", "(100,0.,100.0)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    h2.SetTitle("Production vertex z-position for -t in (0.0,1.0)")
    h2.SetXTitle("Production vertex z-position  [cm]")
    h2.SetYTitle("Events")
    h2.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "ProdVz", "(100,0.,100.0)","CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    cutVz_low = ROOT.TLine(52, 0, 52, h2.GetMaximum()); cutVz_low.SetLineColor(ROOT.kRed); cutVz_low.Draw("same")
    cutVz_hi  = ROOT.TLine(78, 0, 78, h2.GetMaximum());  cutVz_hi.SetLineColor(ROOT.kRed);  cutVz_hi.Draw("same")

    c1.cd(3)
    h3 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "(100,0,2)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
    h3.SetTitle("|-t|")
    h3.SetXTitle("|-t| [GeV^{2}]")
    h3.SetYTitle("Events")
    h3.Draw()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "(100,0,2)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    cutt_low = ROOT.TLine(0.1, 0, 0.1, h3.GetMaximum()); cutt_low.SetLineColor(ROOT.kRed); cutt_low.Draw("same")
    cutt_hi = ROOT.TLine(1.0, 0, 1.0, h3.GetMaximum()); cutt_hi.SetLineColor(ROOT.kRed); cutt_hi.Draw("same")

    c1.cd(4)
    h4 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "EnPB", "(125,5,12)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,targetZ)")
    h4.SetTitle("E_{beam} for -t in (0.0,1.0)")
    h4.SetXTitle("E_{beam} [GeV]")
    h4.SetYTitle("Events")
    cutEb_low = ROOT.TLine(8.2, 0, 8.2, h4.GetMaximum()); cutEb_low.SetLineColor(ROOT.kRed)
    h4.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "EnPB", "(125,5,12)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,targetZ)")
    cutEb_low.Draw("same")
    cutEb_hi = ROOT.TLine(8.8, 0, 8.8, h4.GetMaximum()); cutEb_hi.SetLineColor(ROOT.kRed); cutEb_hi.Draw("same")

    c1.cd(5)
    h5 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "Chi2DOF", "(80,0,20)", "CUT(tRange,rf,unusedE,unusedTracks,coherentPeak,targetZ)")
    h5.SetTitle("#chi^{2}/dof for -t in (0.0,1.0)")
    h5.SetXTitle("#chi^{2}/dof")
    h5.SetYTitle("Events")
    cutChi2 = ROOT.TLine(5.0, 0, 5.0, h5.GetMaximum()); cutChi2.SetLineColor(ROOT.kRed)
    h5.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "Chi2DOF", "(80,0,20)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
    cutChi2.Draw("same")

    c1.cd(6)
    h6 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "VeeLP1", "(60,0,10)", "CUT(tRange,rf,chi2DOF,unusedE,coherentPeak,Lambda,targetZ)")
    h6.SetTitle("Lambda flight length for -t in (0.0,1.0)")
    h6.SetXTitle("Flight length for M(p #pi^{-})")
    h6.SetYTitle("Events")
    cutFlightSig = ROOT.TLine(2.0, 0, 2.0, h6.GetMaximum()); cutFlightSig.SetLineColor(ROOT.kRed)
    h6.Draw()
    lambFLline = ROOT.TLine(2.0, 0, 2.0, h6.GetMaximum())
    lambFLline.SetLineColor(ROOT.kRed)
    lambFLline.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c1.cd(7)
    h9 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "VeeLP2", "(60,0,10)", "CUT(tRange,rf,chi2DOF,unusedE,coherentPeak,KShort,targetZ)")
    h9.SetTitle("K_{s} flight length for -t in (0.0,1.0)")
    h9.SetXTitle("Flight length for M(#pi^{+} #pi^{-})")
    h9.SetYTitle("Events")
    cutflightLengthKShort = ROOT.TLine(2.0, 0, 2.0, h9.GetMaximum()); cutflightLengthKShort.SetLineColor(ROOT.kRed)
    h9.Draw()
    ksFLline = ROOT.TLine(2.0, 0, 2.0, h9.GetMaximum())
    ksFLline.SetLineColor(ROOT.kRed)
    ksFLline.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c1.Print(f"{allPlots}(")  # open multipage PDF


    # -----------------------------
    # Canvas 2a MASS PLOTS: FLIGHT length OFF vs ON
    # -----------------------------
    c2a = ROOT.TCanvas("c2a", "c2a", 1800, 800)
    c2a.Divide(3, 2)

    c2a.cd(1)
    h7a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,Lambda)*CUTWT(rf,Lambda)")
    # turn stats box on
    h7a.SetStats(True)
    h7a.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    h7a.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    h7a.SetYTitle("Events")
    h7a.Draw()
    legend7a = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend7a.AddEntry(h7a, "flightSig OFF", "l")
    legend7a.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,Lambda)")


    c2a.cd(2)
    h8a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort)*CUTWT(rf,KShort)")
    h8a.SetTitle("M(#Lambda) for -t in (0.0,1.0)")
    h8a.SetXTitle("M(p #pi^{-})  [GeV/c^{2}]")
    h8a.SetYTitle("Events")
    h8a.Draw()
    legend8a = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend8a.AddEntry(h8a, "flightSig OFF", "l")
    legend8a.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort)*CUTWT(rf,KShort)")

    c2a.cd(3)
    h9a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    h9a.SetTitle("M(#pi^{+}) for -t in (0.0,1.0)")
    h9a.SetXTitle("Bachelor pion: M(#pi^{+})  [GeV/c^{2}]")
    h9a.SetYTitle("Events")
    h9a.Draw("hist")
    legend9a = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend9a.AddEntry(h9a, "flightSig n/a", "l")
    legend9a.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")

    c2a.cd(4)
    h7b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,Lambda,flightLengthKShort)*CUTWT(rf,Lambda)")
    h7b.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    h7b.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    h7b.SetYTitle("Events")
    h7b.Draw()
    legend7b = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend7b.AddEntry(h7b, "flightSig ON", "l")
    legend7b.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,Lambda,flightLengthKShort)*CUTWT(rf,Lambda)")

    c2a.cd(5)
    h8b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,flightLengthLambda)*CUTWT(rf,KShort)")
    h8b.SetTitle("M(#Lambda) for -t in (0.0,1.0)")
    h8b.SetXTitle("M(p #pi^{-})  [GeV/c^{2}]")
    h8b.SetYTitle("Events")
    h8b.Draw()
    legend8b = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend8b.AddEntry(h8b, "flightSig ON", "l")
    legend8b.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthLambda)")

    c2a.cd(6)
    h9b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,Lambda,flightLengthKShort,flightLengthLambda)*CUTWT(rf,KShort,Lambda)")
    h9b.SetTitle("M(#pi^{+}) for -t in (0.0,1.0)")
    h9b.SetXTitle("Bachelor pion: M(#pi^{+})  [GeV/c^{2}]")
    h9b.SetYTitle("Events")
    h9b.Draw("hist")
    legend9b = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend9b.AddEntry(h9b, "flightSig n/a", "l")
    legend9b.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,Lambda,flightLengthKShort,flightLengthLambda)*CUTWT(rf,KShort,Lambda)")


    c2a.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 2b SIDEBAND SUBTRACTION ON K*
    # -----------------------------
    c2b = ROOT.TCanvas("c2b", "c2b", 1200, 800)
    c2b.Divide(2, 2)

    c2b.cd(1)
    h7 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,Lambda,flightLengthKShort,flightLengthLambda)*CUTWT(rf,Lambda)")
    h7.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    h7.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    h7.SetYTitle("Events")
    h7.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,Lambda,flightLengthKShort,flightLengthLambda)*CUTWT(rf,Lambda)")
    cutKShortSigL   = ROOT.TLine(0.47, 0, 0.47, h7.GetMaximum())
    cutKShortSigR   = ROOT.TLine(0.53, 0, 0.53, h7.GetMaximum())
    cutKShortSBLowL = ROOT.TLine(0.36, 0, 0.36, h7.GetMaximum())
    cutKShortSBLowR = ROOT.TLine(0.39, 0, 0.39, h7.GetMaximum())
    cutKShortSBHiL  = ROOT.TLine(0.58, 0, 0.58, h7.GetMaximum())
    cutKShortSBHiR  = ROOT.TLine(0.61, 0, 0.61, h7.GetMaximum())
    for ln in (cutKShortSigL, cutKShortSigR, cutKShortSBLowL, cutKShortSBLowR, cutKShortSBHiL, cutKShortSBHiR):
        ln.SetLineColor(ROOT.kRed); ln.Draw("same")

    c2b.cd(2)
    h8 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,flightLengthKShort,flightLengthLambda)*CUTWT(rf,KShort)")
    h8.SetTitle("M(#Lambda) for -t in (0.0,1.0)")
    h8.SetXTitle("M(p #pi^{-})  [GeV/c^{2}]")
    h8.SetYTitle("Events")
    h8.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,KShort,flightLengthKShort,flightLengthLambda)*CUTWT(rf,KShort)")
    cutLambSigL   = ROOT.TLine(1.10500, 0, 1.10500, h8.GetMaximum())
    cutLambSigR   = ROOT.TLine(1.13250, 0, 1.13250, h8.GetMaximum())
    cutLambSBLowL = ROOT.TLine(1.08000, 0, 1.08000, h8.GetMaximum())
    cutLambSBLowR = ROOT.TLine(1.09375, 0, 1.09375, h8.GetMaximum())
    cutLambSBHiL  = ROOT.TLine(1.14500, 0, 1.14500, h8.GetMaximum())
    cutLambSBHiR  = ROOT.TLine(1.15875, 0, 1.15875, h8.GetMaximum())
    for ln in (cutLambSigL, cutLambSigR, cutLambSBLowL, cutLambSBLowR, cutLambSBHiL, cutLambSBHiR):
        ln.SetLineColor(ROOT.kRed); ln.Draw("same")

    c2b.cd(3)
    hMKShortpi = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)")
    hMKShortpi.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpi.SetXTitle("M(K_{s} #pi^{+})  [GeV/c^{2}]")
    hMKShortpi.SetYTitle("Events")
    hMKShortpi.Draw()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.8,1.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)")
    
    hMKShortpiSig = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    hMKShortpiSig.SetFillColor(ROOT.kBlue)
    hMKShortpiSig.Draw("hist,same")
    
    hMKShortpiBg = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTSBWT(rf,KShort,Lambda)")
    hMKShortpiBg.SetFillColor(ROOT.kRed)
    hMKShortpiBg.Draw("hist,same")
    
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    legend = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend.AddEntry(hMKShortpi, "Data", "l")
    legend.AddEntry(hMKShortpiSig, "Signal", "f")
    legend.AddEntry(hMKShortpiBg, "Sideband", "f")
    legend.Draw("same")

    c2b.cd(4)
    h10sig = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "RFDeltaT", "(400,-2,2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)")
    h10sbLa = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "RFDeltaT", "(400,-18,0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)")
    h10sbLb = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "RFDeltaT", "(400,-18,-2.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)")
    h10sbRa = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "RFDeltaT", "(400,0,18)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)")
    h10sbRb = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "RFDeltaT", "(400,2,18)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)")
    h10sig.SetTitle("#Delta t_{RF} for -t in (0.0,1.0)")
    h10sig.SetXTitle("#Delta t_{RF}")
    h10sig.SetYTitle("Events")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    cutRFSigL = ROOT.TLine(-2.0, 0, -2.0, h10sig.GetMaximum())
    cutRFSigR = ROOT.TLine(+2.0, 0, +2.0, h10sig.GetMaximum())
    cutRFSigL.SetLineColor(ROOT.kBlue); cutRFSigR.SetLineColor(ROOT.kBlue)
    cutRFSigL.Draw("same"); cutRFSigR.Draw("same")
    cutRFbgL1 = ROOT.TLine(-18.0, 0.0, -18.0, h10sbLa.GetMaximum()); cutRFbgL1.SetLineColor(ROOT.kRed)
    cutRFbgL2 = ROOT.TLine(-6.0, 0.0, -6.0, h10sbLa.GetMaximum()); cutRFbgL2.SetLineColor(ROOT.kRed)
    cutRFbgR1 = ROOT.TLine(6.0, 0.0, 6.0, h10sbRa.GetMaximum());   cutRFbgR1.SetLineColor(ROOT.kRed)
    cutRFbgR2 = ROOT.TLine(18.0, 0.0, 18.0, h10sbRa.GetMaximum()); cutRFbgR2.SetLineColor(ROOT.kRed)
    cutRFbgL1.Draw("same"); cutRFbgL2.Draw("same")
    cutRFbgR1.Draw("same"); cutRFbgR2.Draw("same")
    h10sig.SetFillColor(ROOT.kBlue)
    h10sig.Draw("hist")
    h10sbLa.Draw("same")
    h10sbLb.Draw("hist, same")
    h10sbRa.Draw("same")
    h10sbRb.Draw("hist, same")
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "RFDeltaT", "(400,-20,20)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)")

    c2b.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 3 JUST K*
    # -----------------------------
    c3 = ROOT.TCanvas("c3", "c3", 900, 400)
    c3.Divide(2, 1)

    c3.cd(1)
    hMKShortpiSig.SetFillColor(ROOT.kBlue)
    hMKShortpiSig.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig.SetYTitle("Events")
    hMKShortpiSig.DrawClone("hist")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    legend1 = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend1.AddEntry(hMKShortpiSig, "Signal", "f")
    legend1.Draw("same")

    c3.cd(2)
    hMKShortpiSig.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig.SetYTitle("Events")
    hMKShortpiSig.DrawClone()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    lineK892 = ROOT.TLine(0.892, 0, 0.892, hMKShortpiSig.GetMaximum()); lineK892.SetLineColor(ROOT.kRed)
    lineK892.Draw("same")
    lineK1430 = ROOT.TLine(1.430, 0, 1.430, hMKShortpiSig.GetMaximum()); lineK1430.SetLineColor(ROOT.kRed)
    lineK1430.Draw("same")
    legend2 = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend2.AddEntry(hMKShortpiSig, "Signal", "f")
    legend2.Draw("same")
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    print(hMKShortpiSig.Integral())

    # ROOT.FSFitUtilities.createFunction(ROOT.FSFitPOLY("p", 1.04, 1.56, 1, 0.0), 1600.0, -900)
    # ROOT.FSFitUtilities.createFunction(ROOT.FSFitGAUS("g", 1.04, 1.56), 500.0, 1.32, 0.05)
    # ROOT.FSFitUtilities.createFunction("pg", "p+g")
    # ROOT.FSFitUtilities.fixParameters("p")
    # ROOT.FSFitUtilities.migrad(hMKShortpiSig, "pg")
    # fpg = ROOT.FSFitUtilities.getTF1("pg"); fpg.SetLineColor(ROOT.kRed);  fpg.SetLineStyle(ROOT.kSolid); fpg.Draw("same")
    # fg  = ROOT.FSFitUtilities.getTF1("g");  fg.SetLineColor(ROOT.kBlue); fg.SetLineStyle(ROOT.kSolid); fg.Draw("same")
    # print("fg Integral:", fg.Integral(1.04, 1.56))

    c3.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 3a K* DATA vs MC
    # -----------------------------
    c3a = ROOT.TCanvas("c3a", "c3a", 800, 600)

    hMKShortpiSig.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig.SetYTitle("Events")
    hMKShortpiSig.SetLineColor(ROOT.kBlack)
    hMKShortpiSig.SetLineWidth(2)
    hMKShortpiSig.SetMarkerStyle(20)
    hMKShortpiSig.SetMarkerSize(0.8)
    hMKShortpiSig.DrawClone("E1")

    # hMKShortpiSig_MC = ROOT.FSModeHistogram.getTH1F(FND_MC, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    # hMKShortpiSig_MC.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    # hMKShortpiSig_MC.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    # hMKShortpiSig_MC.SetYTitle("Events")
    # hMKShortpiSig_MC.SetLineColor(ROOT.kRed)
    # hMKShortpiSig_MC.SetLineWidth(2)
    # hMKShortpiSig_MC.SetMarkerStyle(24)
    # hMKShortpiSig_MC.SetMarkerColor(ROOT.kRed)
    # hMKShortpiSig_MC.SetMarkerSize(0.8)
    # hMKShortpiSig_MC.Scale(0.6)
    # hMKShortpiSig_MC.Draw("E1 same")

    # lab1.DrawLatex(0.5, 1.00, f"{label}")    
    lineK892 = ROOT.TLine(0.892, 0, 0.892, hMKShortpiSig.GetMaximum()); lineK892.SetLineColor(ROOT.kRed)
    lineK892.Draw("same")
    lineK1430 = ROOT.TLine(1.430, 0, 1.430, hMKShortpiSig.GetMaximum()); lineK1430.SetLineColor(ROOT.kRed)
    lineK1430.Draw("same")
    legend3a = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend3a.AddEntry(hMKShortpiSig, "Data", "pl")
    # legend3a.AddEntry(hMKShortpiSig_MC, "Signal MC", "pl")
    legend3a.Draw("same")
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    print(hMKShortpiSig.Integral())



    c3a.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 4 BARYON BACKGROUND, SIGMA(1385) CUT
    # -----------------------------
    c4 = ROOT.TCanvas("c4", "c4", 1000, 300)
    c4.Divide(3, 1)


    c4.cd(1)
    ROOT.gPad.SetRightMargin(0.20)
    HKsPipVSLambPip = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100,0.00,14.0,100,0.0,9.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    HKsPipVSLambPip.SetTitle("M(K_{s} #pi^{+})^{2} vs M(#Lambda #pi^{+})^{2} for -t in (0.0,1.0)")
    HKsPipVSLambPip.SetXTitle("M(#Lambda #pi^{+})^{2} [GeV^{2}]")
    HKsPipVSLambPip.SetYTitle("M(K_{s} #pi^{+})^{2} [GeV^{2}]")
    HKsPipVSLambPip.Draw("colz")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100,0.0,4.0,100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    print("X range:", HKsPipVSLambPip.GetXaxis().GetXmin(), HKsPipVSLambPip.GetXaxis().GetXmax())
    print("Y range:", HKsPipVSLambPip.GetYaxis().GetXmin(), HKsPipVSLambPip.GetYaxis().GetXmax())

    c4.cd(2)
    hKSpip = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    hKSpip.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hKSpip.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hKSpip.SetYTitle("Events")
    hKSpip.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")

    c4.cd(3)
    hLambPip = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    hLambPip.SetTitle("M(#Lambda #pi^{+}) for -t in (0.0,1.0)")
    hLambPip.SetXTitle("M(#Lambda #pi^{+}) [GeV/c^{2}]")
    hLambPip.SetYTitle("Events")
    hLambPip.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    cutSigmaLow = ROOT.TLine(2.0, 0, 2.0, hLambPip.GetMaximum()); cutSigmaLow.SetLineColor(ROOT.kRed); cutSigmaLow.Draw("same")
    cutSigmaLow.SetLineColor(ROOT.kRed);
    cutSigmaLow.Draw("same")
    cutSigmaHigh = ROOT.TLine(4.0, 0, 4.0, hLambPip.GetMaximum()); cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.Draw("same")


    c4.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 5 OTHER BARYON BACKGROUND, LAMBDA PI-
    # -----------------------------
    c5 = ROOT.TCanvas("c5", "c5", 1000, 300)
    c5.Divide(3, 1)

    # DecayingLambda = "1"
    # Proton         = "1a"
    # PiMinus2       = "1b"
    # DecayingKShort = "2"
    # PiPlus2        = "2a"
    # PiMinus1       = "2b"
    # PiPlus1        = "3"

    c5.cd(1)
    ROOT.gPad.SetRightMargin(0.20)
    HKsPipVSLambPip = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"MASS2({DecayingLambda},{PiMinus1}):MASS2({PiPlus1},{PiMinus1})", "(100,0.0,14.0,100,0.0,14.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    HKsPipVSLambPip.SetTitle("M(#Lambda \pi^{-})^{2} vs M(#pi^{+} \pi^{-})^{2} for -t in (0.0,1.0)")
    HKsPipVSLambPip.SetXTitle("M(#Lambda #pi^{-})^{2} [GeV^{2}]")
    HKsPipVSLambPip.SetYTitle("M(#pi^{+} #pi^{-})^{2} [GeV^{2}]")
    HKsPipVSLambPip.Draw("colz")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS2({DecayingLambda},{PiMinus1}):MASS2({PiPlus1},{PiMinus1})", "(100,0.0,14.0,100,0.0,14.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")  

    c5.cd(2)
    hLambPip.SetTitle("M(#Lambda #pi^{-}) for -t in (0.0,1.0)")
    hLambPip.SetXTitle("M(#Lambda #pi^{-}) [GeV/c^{2}]")
    hLambPip.SetYTitle("Events")
    hLambPip.DrawClone()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiMinus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")

    c5.cd(3)
    HLambKS = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({PiPlus1},{PiMinus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    HLambKS.SetTitle("M(#pi^{+} #pi^{-}) for -t in (0.0,1.0)")
    HLambKS.SetXTitle("M(#pi^{+} #pi^{-}) [GeV/c^{2}]")
    HLambKS.SetYTitle("Events")
    HLambKS.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({PiPlus1},{PiMinus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")

    c5.Print(allPlots)  # middle pages


    # -----------------------------
    # Canvas 8 COS THETA GJ
    # -----------------------------
    c8 = ROOT.TCanvas("c8", "c8", 1400, 800)
    c8.Divide(3, 2)
    
    # cos(theta_GJ) of K_S in M rest frame
    c8.cd(1)
    h_gj = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)", "(60,-1.0,1.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385,selectKSTAR892)*CUTWT(rf,KShort,Lambda)")
    h_gj.SetTitle("K^{*}(M) #rightarrow K_{S}#pi^{+}, -t #in (0,1)")
    h_gj.SetXTitle("cos#theta_{GJ}(K_{S})")
    h_gj.SetYTitle("Events")
    h_gj.SetLineColor(ROOT.kBlack)
    h_gj.SetLineWidth(2)
    h_gj.SetMarkerStyle(20)
    h_gj.SetMarkerColor(ROOT.kBlack)
    h_gj.SetMarkerSize(0.8)
    h_gj.Draw("E1")

    h_gj_MC = ROOT.FSModeHistogram.getTH1F(FND_MC, NT, "m100000000_1100", f"GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)", "(60,-1.0,1.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385,selectKSTAR892)*CUTWT(rf,KShort,Lambda)")
    h_gj_MC.SetTitle("K^{*}(M) #rightarrow K_{S}#pi^{+}, -t #in (0,1)")
    h_gj_MC.SetXTitle("cos#theta_{GJ}(K_{S})")
    h_gj_MC.SetYTitle("Events")
    h_gj_MC.SetLineColor(ROOT.kRed)
    h_gj_MC.SetLineWidth(2)
    h_gj_MC.SetMarkerStyle(24)
    h_gj_MC.SetMarkerColor(ROOT.kRed)
    h_gj_MC.SetMarkerSize(0.8)
    h_gj_MC.Scale(0.6)
    h_gj_MC.Draw("E1 same")

    legend8 = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend8.AddEntry(h_gj, "Data", "pl")
    legend8.AddEntry(h_gj_MC, "Signal MC", "pl")
    legend8.Draw("same")


    c8.cd(2)
    ROOT.gPad.SetRightMargin(0.20)
    hMKShortpiVsGJCosTheta = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM):MASS({DecayingKShort},{PiPlus1})", "(60,0.7,2.7,50,-1.,1.)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    hMKShortpiVsGJCosTheta.SetTitle("K^{*}(M) #rightarrow K_{S}#pi^{+}, -t #in (0,1)")
    hMKShortpiVsGJCosTheta.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiVsGJCosTheta.SetYTitle("cos#theta_{GJ}")
    hMKShortpiVsGJCosTheta.Draw("colz")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c8.cd(3)
    h_gj_phi = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"GJPHI({DecayingKShort};{PiPlus1};GLUEXBEAM;{DecayingLambda})*180/3.141", "(60,-180.00,180.00)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda,rejectSigma1385,selectKSTAR892)*CUTWT(rf,KShort,Lambda)")
    h_gj_phi.SetTitle("K^{*}(M) #rightarrow K_{S}#pi^{+}, -t #in (0,1)")
    h_gj_phi.GetXaxis().SetTitle("#phi_{GJ}(K_{S}) [#circ]")
    h_gj_phi.SetYTitle("Events")
    h_gj_phi.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c8.cd(4)
    hMKShortpiSig.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig.SetYTitle("Events")
    hMKShortpiSig.DrawClone()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    lineK892 = ROOT.TLine(0.800, 0, 0.800, hMKShortpiSig.GetMaximum()); lineK892.SetLineColor(ROOT.kRed)
    lineK892.Draw("same")
    lineK1430 = ROOT.TLine(1.000, 0, 1.000, hMKShortpiSig.GetMaximum()); lineK1430.SetLineColor(ROOT.kRed)
    lineK1430.Draw("same")


    c8.cd(5)
    ROOT.gPad.SetRightMargin(0.20)
    HKsPipVSLambPip_cor = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiPlus1}):MASS({DecayingKShort},{PiPlus1})", "(100,0.50,2.0,100,1.0,3.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")
    HKsPipVSLambPip_cor.SetTitle("M(K_{s} #pi^{+}) vs M(#Lambda #pi^{+}) for -t in (0.0,1.0)")
    HKsPipVSLambPip_cor.SetXTitle("M(K_{s} #pi^{+}) [GeV]")
    HKsPipVSLambPip_cor.SetYTitle("M(#Lambda #pi^{+}) [GeV]")
    HKsPipVSLambPip_cor.Draw("colz")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiPlus1}):MASS({DecayingKShort},{PiPlus1})", "(100,0.0,4.0,100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,KShort,Lambda)*CUTWT(rf,KShort,Lambda)")

    c8.cd(6)
    hLambPip.SetTitle("M(#Lambda #pi^{+}) for -t in (0.0,1.0)")
    hLambPip.SetXTitle("M(#Lambda #pi^{+}) [GeV/c^{2}]")
    hLambPip.SetYTitle("Events")
    hLambPip.DrawClone()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    # draw line at 2.0 to show where we cut out the Sigmas
    cutSigmaLow = ROOT.TLine(2.0, 0, 2.0, hLambPip.GetMaximum()); cutSigmaLow.SetLineColor(ROOT.kRed); cutSigmaLow.Draw("same")
    cutSigmaLow.SetLineColor(ROOT.kRed);
    cutSigmaLow.Draw("same")
    cutSigmaHigh = ROOT.TLine(4.0, 0, 4.0, hLambPip.GetMaximum()); cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.Draw("same")

    c8.Print(f"{allPlots})")  # close multipage PDF


    # ROOT.FSHistogram.dumpHistogramCache("kspiplamb_plots_v2")

    endTime = time.time()
    print(f"Time to run: {endTime - startTime:.1f} seconds")

if __name__ == "__main__":
    setup()
