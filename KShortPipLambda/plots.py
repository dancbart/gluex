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


# NOTES: Make arccos(theta) for pi+ and compare to that for KS
# integrate under the curves to get total number of events in signal and sidebands
# change axis labels for ProdVz if it really is z in cm and not energy in GeV
# understand the godfried angle distribution for KS and pi+ plot
# understand why we want low t, why is it that our signal/reactions occur at low t? i.e. what theory.
# add Sigma cut on ks pip system and on DALITZ plot(s)
# understand why we want small bins of t.  Is it because the amplitude analysis fits converge better when t is relatively constant?
# understand and read that pdf justin sent on Intensity (to understand what the intensity is).
# understand the difference between a "binned fit" and the AmpTools "unbinned fit"
# what "thing", exactly, therefore, does the Amptools software "fit" when doing this so called "unbinned fit"?
# understand why a photoproduction reaction of k*892 is "so much better" than the CLAS data.  Is it just because we have more statistics, or because we are at higher enegies, or because we have polarized photons (and therefore constrain some quantum number?)? or is it something else, or all the above?
# read the coherent peak paper from Richard Jones, and understand the intuition behind the coherent peak cut.
# understand the E_unused cut, why is it there, what does it do, what physics does it represent?
# understand the chi2/dof cut, why is it there, what does it do, what physics does it represent?
# understand the RF cut, why is it there, what does it do, what physics does it represent?
# understand the unused tracks cut, why is it there, what does it do, what physics does it represent?
# understand how the sideband subtractions are calculated.
# do integrals of signal vs sideband, to confirm the sideband subtraction is really the amount by which raw signal is reduced.
# do fits of KShort to "prove" that it really is a KShort.
# do fits of Lambda to "prove" that it really is a Lambda.
# understand "width"
# redo axes on plots to be "Events / (bin width)" instead of just "Events"


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
    ROOT.FSCut.defineCut("tRange", f"(abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda})-0.5)<0.5)")

    # STATIC CUTS
    ROOT.FSCut.defineCut("rf", "OR(abs(RFDeltaT)<2.0)", "abs(RFDeltaT)>6.0", 0.1667)
    ROOT.FSCut.defineCut("chi2DOF", "Chi2DOF", "0.0", "5.0")
    ROOT.FSCut.defineCut("unusedE", "EnUnusedSh<0.1")
    ROOT.FSCut.defineCut("unusedTracks", "NumUnusedTracks<1")  # No unused tracks
    ROOT.FSCut.defineCut("coherentPeak", "EnPB", "8.2", "8.8")  # Coherent peak: 8.2 < E_beam < 8.8
    ROOT.FSCut.defineCut("flightSigLambda", "VeeLP1>2.0")
    ROOT.FSCut.defineCut("flightSigKShort", "VeeLP2>2.0")

    # CUTS WITH SIDEBANDS
    ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0,)
    ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0,)
    ROOT.FSCut.defineCut("selectKSTAR892", f"MASS({DecayingKShort},{PiPlus1})", "0.80", "1.00",)
    # ROOT.FSCut.defineCut("selectKSTAR1430", f"MASS({DecayingKShort},{PiPlus1})", "0.85", "0.95", "0.0", "0.85", "0.95", "1.0",)
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})", "2.0", "4.0",) # remove Sigma(1385) and higher

    # -----------------------------
    # Canvas 1
    # -----------------------------
    c1 = ROOT.TCanvas("c1", "c1", 1600, 1200)
    c1.Divide(3, 3)

    c1.cd(1)
    h1 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "EnUnusedSh", "(100,0.0,1.0)", "CUT(tRange,rf,chi2DOF,unusedTracks,coherentPeak)")
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
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "EnUnusedSh", "(100,0.0,1.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")

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
    h3 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "(100,0,2)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    h3.SetTitle("|-t|")
    h3.SetXTitle("|-t| [GeV^{2}]")
    h3.SetYTitle("Events")
    cutt_low = ROOT.TLine(0.1, 0, 0.1, h3.GetMaximum()); cutt_low.SetLineColor(ROOT.kRed)
    h3.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "(100,0,1)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    cutt_low.Draw("same")
    cutt_hi = ROOT.TLine(1.0, 0, 1.0, h3.GetMaximum()); cutt_hi.SetLineColor(ROOT.kRed); cutt_hi.Draw("same")

    c1.cd(4)
    h4 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "EnPB", "(125,5,12)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks)")
    h4.SetTitle("E_{beam} for -t in (0.0,1.0)")
    h4.SetXTitle("E_{beam} [GeV]")
    h4.SetYTitle("Events")
    cutEb_low = ROOT.TLine(8.2, 0, 8.2, h4.GetMaximum()); cutEb_low.SetLineColor(ROOT.kRed)
    h4.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "EnPB", "(125,5,12)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks)")
    cutEb_low.Draw("same")
    cutEb_hi = ROOT.TLine(8.8, 0, 8.8, h4.GetMaximum()); cutEb_hi.SetLineColor(ROOT.kRed); cutEb_hi.Draw("same")

    c1.cd(5)
    h5 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "Chi2DOF", "(80,0,20)", "CUT(tRange,rf,unusedE,unusedTracks,coherentPeak)")
    h5.SetTitle("#chi^{2}/dof for -t in (0.0,1.0)")
    h5.SetXTitle("#chi^{2}/dof")
    h5.SetYTitle("Events")
    cutChi2 = ROOT.TLine(5.0, 0, 5.0, h5.GetMaximum()); cutChi2.SetLineColor(ROOT.kRed)
    h5.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "Chi2DOF", "(80,0,20)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    cutChi2.Draw("same")

    c1.cd(6)
    h6 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "VeeLP1", "(60,0,10)", "CUT(tRange,rf,chi2DOF,unusedE,coherentPeak,Lambda)")
    h6.SetTitle("Lambda flight significance for -t in (0.0,1.0)")
    h6.SetXTitle("Flight significance for M(p #pi^{-})")
    h6.SetYTitle("Events")
    cutFlightSig = ROOT.TLine(2.0, 0, 2.0, h6.GetMaximum()); cutFlightSig.SetLineColor(ROOT.kRed)
    h6.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c1.cd(7)
    h9 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "VeeLP2", "(60,0,10)", "CUT(tRange,rf,chi2DOF,unusedE,coherentPeak,KShort)")
    h9.SetTitle("K_{s} flight significance for -t in (0.0,1.0)")
    h9.SetXTitle("Flight significance for M(#pi^{+} #pi^{-})")
    h9.SetYTitle("Events")
    cutFlightSigKShort = ROOT.TLine(2.0, 0, 2.0, h9.GetMaximum()); cutFlightSigKShort.SetLineColor(ROOT.kRed)
    h9.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c1.Print(f"{allPlots}(")  # open multipage PDF


    # -----------------------------
    # Canvas 2a
    # -----------------------------
    c2a = ROOT.TCanvas("c2a", "c2a", 1800, 800)
    c2a.Divide(3, 2)

    c2a.cd(1)
    h7a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
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
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")


    c2a.cd(2)
    h8a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
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
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")

    c2a.cd(3)
    h9a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
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
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")

    c2a.cd(4)
    h7b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)")
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
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)")

    c2a.cd(5)
    h8b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)")
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
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)")

    c2a.cd(6)
    h9b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
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
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({PiPlus1})", "(60,0.08,0.2)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")


    c2a.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 2b
    # -----------------------------
    c2b = ROOT.TCanvas("c2b", "c2b", 1200, 800)
    c2b.Divide(2, 2)

    c2b.cd(1)
    h7 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)")
    h7.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    h7.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    h7.SetYTitle("Events")
    h7.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)")
    cutKShortSigL   = ROOT.TLine(0.47, 0, 0.47, h7.GetMaximum())
    cutKShortSigR   = ROOT.TLine(0.53, 0, 0.53, h7.GetMaximum())
    cutKShortSBLowL = ROOT.TLine(0.36, 0, 0.36, h7.GetMaximum())
    cutKShortSBLowR = ROOT.TLine(0.39, 0, 0.39, h7.GetMaximum())
    cutKShortSBHiL  = ROOT.TLine(0.58, 0, 0.58, h7.GetMaximum())
    cutKShortSBHiR  = ROOT.TLine(0.61, 0, 0.61, h7.GetMaximum())
    for ln in (cutKShortSigL, cutKShortSigR, cutKShortSBLowL, cutKShortSBLowR, cutKShortSBHiL, cutKShortSBHiR):
        ln.SetLineColor(ROOT.kRed); ln.Draw("same")

    c2b.cd(2)
    h8 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)")
    h8.SetTitle("M(#Lambda) for -t in (0.0,1.0)")
    h8.SetXTitle("M(p #pi^{-})  [GeV/c^{2}]")
    h8.SetYTitle("Events")
    h8.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)")
    cutLambSigL   = ROOT.TLine(1.10500, 0, 1.10500, h8.GetMaximum())
    cutLambSigR   = ROOT.TLine(1.13250, 0, 1.13250, h8.GetMaximum())
    cutLambSBLowL = ROOT.TLine(1.08000, 0, 1.08000, h8.GetMaximum())
    cutLambSBLowR = ROOT.TLine(1.09375, 0, 1.09375, h8.GetMaximum())
    cutLambSBHiL  = ROOT.TLine(1.14500, 0, 1.14500, h8.GetMaximum())
    cutLambSBHiR  = ROOT.TLine(1.15875, 0, 1.15875, h8.GetMaximum())
    for ln in (cutLambSigL, cutLambSigR, cutLambSBLowL, cutLambSBLowR, cutLambSBHiL, cutLambSBHiR):
        ln.SetLineColor(ROOT.kRed); ln.Draw("same")

    c2b.cd(3)
    hMKShortpi = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda,KShort,Lambda)")
    hMKShortpi.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpi.SetXTitle("M(K_{s} #pi^{+})  [GeV/c^{2}]")
    hMKShortpi.SetYTitle("Events")
    hMKShortpi.Draw()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.8,1.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda,KShort,Lambda)")
    
    hMKShortpiSig = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTWT(rf,KShort,Lambda)")
    hMKShortpiSig.SetFillColor(ROOT.kBlue)
    hMKShortpiSig.Draw("hist,same")
    
    hMKShortpiBg = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTSBWT(rf,KShort,Lambda)")
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
    h10 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", "RFDeltaT", "(400,-20,20)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    h10.SetTitle("#Delta t_{RF} for -t in (0.0,1.0)")
    h10.SetXTitle("#Delta t_{RF}")
    h10.SetYTitle("Events")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    cutRFSigL = ROOT.TLine(-2.0, 0, -2.0, h10.GetMaximum())
    cutRFSigR = ROOT.TLine(+2.0, 0, +2.0, h10.GetMaximum())
    cutRFSigL.SetLineColor(ROOT.kRed); cutRFSigR.SetLineColor(ROOT.kRed)
    h10.Draw()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", "RFDeltaT", "(400,-20,20)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    cutRFSigL.Draw("same"); cutRFSigR.Draw("same")

    c2b.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 3
    # -----------------------------
    c3 = ROOT.TCanvas("c3", "c3", 900, 400)
    c3.Divide(2, 1)

    c3.cd(1)
    hMKShortpiSig = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTWT(rf,KShort,Lambda)")
    hMKShortpiSig.SetFillColor(ROOT.kBlue)
    hMKShortpiSig.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig.SetYTitle("Events")
    # hMKShortpiSig.Draw("hist")
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
    legend2.AddEntry(hMKShortpiSig, "Signal", "l")
    legend2.Draw("same")
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    print(hMKShortpiSig.Integral())

    ROOT.FSFitUtilities.createFunction(ROOT.FSFitPOLY("p", 1.04, 1.56, 1, 0.0), 1600.0, -900)
    ROOT.FSFitUtilities.createFunction(ROOT.FSFitGAUS("g", 1.04, 1.56), 500.0, 1.32, 0.05)
    ROOT.FSFitUtilities.createFunction("pg", "p+g")
    ROOT.FSFitUtilities.fixParameters("p")
    ROOT.FSFitUtilities.migrad(hMKShortpiSig, "pg")
    fpg = ROOT.FSFitUtilities.getTF1("pg"); fpg.SetLineColor(ROOT.kRed);  fpg.SetLineStyle(ROOT.kSolid); fpg.Draw("same")
    fg  = ROOT.FSFitUtilities.getTF1("g");  fg.SetLineColor(ROOT.kBlue); fg.SetLineStyle(ROOT.kSolid); fg.Draw("same")
    print("fg Integral:", fg.Integral(1.04, 1.56))

    c3.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 3a
    # -----------------------------
    c3a = ROOT.TCanvas("c3a", "c3a", 800, 600)

    hMKShortpiSig.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig.SetYTitle("Events")
    hMKShortpiSig.SetLineColor(ROOT.kBlue)
    hMKShortpiSig.SetLineWidth(2)
    hMKShortpiSig.SetFillColor(ROOT.kBlue)
    hMKShortpiSig.DrawClone("hist")

    hMKShortpiSig_MC = ROOT.FSModeHistogram.getTH1F(FND_MC, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTWT(rf,KShort,Lambda)")
    hMKShortpiSig_MC.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hMKShortpiSig_MC.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hMKShortpiSig_MC.SetYTitle("Events")
    hMKShortpiSig_MC.SetLineColor(ROOT.kRed)
    hMKShortpiSig_MC.SetLineWidth(2)
    hMKShortpiSig_MC.SetFillColor(ROOT.kRed)
    hMKShortpiSig_MC.Scale(0.6)
    hMKShortpiSig_MC.Draw("hist same")

    # lab1.DrawLatex(0.5, 1.00, f"{label}")    
    lineK892 = ROOT.TLine(0.892, 0, 0.892, hMKShortpiSig.GetMaximum()); lineK892.SetLineColor(ROOT.kRed)
    lineK892.Draw("same")
    lineK1430 = ROOT.TLine(1.430, 0, 1.430, hMKShortpiSig.GetMaximum()); lineK1430.SetLineColor(ROOT.kRed)
    lineK1430.Draw("same")
    legend3a = ROOT.TLegend(0.6, 0.7, 0.85, 0.85)
    legend3a.AddEntry(hMKShortpiSig, "Data", "l")
    legend3a.AddEntry(hMKShortpiSig_MC, "Signal MC", "l")
    legend3a.Draw("same")
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.5,2.5)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,rejectSigma1385)*CUTWT(rf,KShort,Lambda)")
    print(hMKShortpiSig.Integral())



    c3a.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 4
    # -----------------------------
    c4 = ROOT.TCanvas("c4", "c4", 1000, 300)
    c4.Divide(3, 1)


    c4.cd(1)
    HKsPipVSLambPip = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100,0.00,14.0,100,0.0,9.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)")
    HKsPipVSLambPip.SetTitle("M(K_{s} #pi^{+})^{2} vs M(#Lambda #pi^{+})^{2} for -t in (0.0,1.0)")
    HKsPipVSLambPip.SetXTitle("M(#Lambda #pi^{+})^{2} [GeV^{2}]")
    HKsPipVSLambPip.SetYTitle("M(K_{s} #pi^{+})^{2} [GeV^{2}]")
    HKsPipVSLambPip.Draw("colz")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100,0.0,4.0,100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)")
    print("X range:", HKsPipVSLambPip.GetXaxis().GetXmin(), HKsPipVSLambPip.GetXaxis().GetXmax())
    print("Y range:", HKsPipVSLambPip.GetYaxis().GetXmin(), HKsPipVSLambPip.GetYaxis().GetXmax())

    c4.cd(2)
    hLambPip = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)*CUTWT(rf)")
    hLambPip.SetTitle("M(K_{s} #pi^{+}) for -t in (0.0,1.0)")
    hLambPip.SetXTitle("M(K_{s} #pi^{+}) [GeV/c^{2}]")
    hLambPip.SetYTitle("Events")
    hLambPip.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)*CUTWT(rf)")

    c4.cd(3)
    HLambKS = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)*CUTWT(rf)")
    HLambKS.SetTitle("M(#Lambda #pi^{+}) for -t in (0.0,1.0)")
    HLambKS.SetXTitle("M(#Lambda #pi^{+}) [GeV/c^{2}]")
    HLambKS.SetYTitle("Events")
    HLambKS.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    # draw line at 2.0 to show where we cut out the Sigmas
    cutSigmaLow = ROOT.TLine(2.0, 0, 2.0, HLambKS.GetMaximum()); cutSigmaLow.SetLineColor(ROOT.kRed); cutSigmaLow.Draw("same")
    cutSigmaLow.SetLineColor(ROOT.kRed);
    cutSigmaLow.Draw("same")
    cutSigmaHigh = ROOT.TLine(4.0, 0, 4.0, HLambKS.GetMaximum()); cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.Draw("same")

    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)*CUTWT(rf)")


    c4.Print(allPlots)  # middle pages

    # -----------------------------
    # Canvas 5
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
    HKsPipVSLambPip = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"MASS2({DecayingLambda},{PiMinus1}):MASS2({PiPlus1},{PiMinus1})", "(100,0.0,14.0,100,0.0,14.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)")
    HKsPipVSLambPip.SetTitle("M(#Lambda \pi^{-})^{2} vs M(#pi^{+} \pi^{-})^{2} for -t in (0.0,1.0)")
    HKsPipVSLambPip.SetXTitle("M(#Lambda #pi^{-})^{2} [GeV^{2}]")
    HKsPipVSLambPip.SetYTitle("M(#pi^{+} #pi^{-})^{2} [GeV^{2}]")
    HKsPipVSLambPip.Draw("colz")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS2({DecayingLambda},{PiMinus1}):MASS2({PiPlus1},{PiMinus1})", "(100,0.0,14.0,100,0.0,14.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)")  

    c5.cd(2)
    hLambPip = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiMinus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTWT(rf)")
    hLambPip.SetTitle("M(#Lambda #pi^{-}) for -t in (0.0,1.0)")
    hLambPip.SetXTitle("M(#Lambda #pi^{-}) [GeV/c^{2}]")
    hLambPip.SetYTitle("Events")
    hLambPip.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiMinus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTWT(rf)")

    c5.cd(3)
    HLambKS = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({PiPlus1},{PiMinus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTWT(rf)")
    HLambKS.SetTitle("M(#pi^{+} #pi^{-}) for -t in (0.0,1.0)")
    HLambKS.SetXTitle("M(#pi^{+} #pi^{-}) [GeV/c^{2}]")
    HLambKS.SetYTitle("Events")
    HLambKS.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({PiPlus1},{PiMinus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)*CUTWT(rf)")

    c5.Print(allPlots)  # middle pages


    # -----------------------------
    # Canvas 6
    # -----------------------------
    c6 = ROOT.TCanvas("c6", "c6", 1200, 800)
    c6.Divide(2, 2)

    c6.cd(1)
    h11a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    h11a.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    h11a.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    h11a.SetYTitle("Events")
    h11a.Draw()
    h11b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)*CUTWT(rf)")
    h11b.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    h11b.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    h11b.SetYTitle("Events  MeV/c^{2}")
    h11b.SetLineColor(ROOT.kBlack)
    h11b.SetLineWidth(1)
    h11b.SetFillColor(ROOT.kBlue)
    h11b.Draw("hist same")
    legend11 = ROOT.TLegend(0.6, 0.7, 0.94, 0.94) # xleft, ylow, xright, yup
    legend11.AddEntry(h11a, "ksFS OFF", "l")
    legend11.AddEntry(h11b, "ksFS ON", "l")
    legend11.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)")

    c6.cd(2)
    h12a = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)")
    h12a.SetTitle("M(#Lambda) for -t in (0.0,1.0)")
    h12a.SetXTitle("M(p #pi^{-})  [GeV/c^{2}]")
    h12a.SetYTitle("Events")
    h12a.Draw()
    h12b = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)*CUTWT(rf)")
    h12b.SetTitle("M(#Lambda) for -t in (0.0,1.0)")
    h12b.SetXTitle("M(p #pi^{-})  [GeV/c^{2}]")
    h12b.SetYTitle("Events")
    h12b.SetLineColor(ROOT.kBlack)
    h12b.SetLineWidth(1)
    h12b.SetFillColor(ROOT.kBlue)
    h12b.Draw("hist same")
    legend12 = ROOT.TLegend(0.6, 0.7, 0.94, 0.94)
    legend12.AddEntry(h12a, "lambFS OFF", "l")
    legend12.AddEntry(h12b, "lambFS ON", "l")
    legend12.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)")

    c6.cd(3)
    h11b.SetTitle("M(K_{s}) for -t in (0.0,1.0)")
    h11b.SetXTitle("M(#pi^{+} #pi^{-})  [GeV/c^{2}]")
    h11b.SetYTitle("Events")
    h11b.DrawClone("hist")
    # create legend
    legend13 = ROOT.TLegend(0.6, 0.7, 0.95, 0.85)
    legend13.AddEntry(h11b, "ksFS rfSB", "l")
    legend13.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingKShort})", "(60,0.2,0.8)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort)*CUTWT(rf,KShort)")

    c6.cd(4)
    h12b.SetTitle("M(#Lambda) for -t in (0.0,1.0)")
    h12b.SetXTitle("M(p #pi^{-})  [GeV/c^{2}]")
    h12b.SetYTitle("Events")
    h12b.DrawClone("hist")
    legend14 = ROOT.TLegend(0.6, 0.7, 0.95, 0.85)
    legend14.AddEntry(h12b, "lambFS rfSB", "l")
    legend14.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"MASS({DecayingLambda})", "(60,1.075,1.22)", "CUT(tRange,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)*CUTWT(rf,Lambda)")

    c6.Print(allPlots)  # middle pages


    # -----------------------------
    # Canvas 8
    # -----------------------------
    c8 = ROOT.TCanvas("c8", "c8", 1000, 800)
    c8.Divide(2, 2)
    
    # cos(theta_GJ) of K_S in M rest frame
    c8.cd(1)
    h_gj = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)", "(60,-1.0,1.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda,selectKSTAR892)")
    h_gj.SetTitle("K^{*}(M) #rightarrow K_{S}#pi^{+}, -t #in (0,1)")
    h_gj.SetXTitle("cos#theta_{GJ}(K_{S})")
    h_gj.SetYTitle("Events")
    h_gj.Draw()
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c8.cd(2)
    hMKShortpiVsGJCosTheta = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM):MASS({DecayingKShort})", "(60,0.7,2.7,50,-1.,1.)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigKShort,flightSigLambda)")
    hMKShortpiVsGJCosTheta.SetTitle("K^{*}(M) #rightarrow K_{S}#pi^{+}, -t #in (0,1)")
    hMKShortpiVsGJCosTheta.SetXTitle("M(K_{s}) [GeV/c^{2}]")
    hMKShortpiVsGJCosTheta.SetYTitle("cos#theta_{GJ}")
    hMKShortpiVsGJCosTheta.Draw("colz")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c8.cd(3)
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

    c8.cd(4)
    HLambKS = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"MASS({DecayingLambda},{PiPlus1})", "(100,0.0,4.0)", "CUT(tRange,rf,chi2DOF,unusedE,unusedTracks,coherentPeak,flightSigLambda)*CUTWT(rf)")
    HLambKS.SetTitle("M(#Lambda #pi^{+}) for -t in (0.0,1.0)")
    HLambKS.SetXTitle("M(#Lambda #pi^{+}) [GeV/c^{2}]")
    HLambKS.SetYTitle("Events")
    HLambKS.Draw("same")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()
    # draw line at 2.0 to show where we cut out the Sigmas
    cutSigmaLow = ROOT.TLine(2.0, 0, 2.0, HLambKS.GetMaximum()); cutSigmaLow.SetLineColor(ROOT.kRed); cutSigmaLow.Draw("same")
    cutSigmaLow.SetLineColor(ROOT.kRed);
    cutSigmaLow.Draw("same")
    cutSigmaHigh = ROOT.TLine(4.0, 0, 4.0, HLambKS.GetMaximum()); cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.SetLineColor(ROOT.kRed); cutSigmaHigh.Draw("same")
    cutSigmaHigh.Draw("same")

    c8.Print(f"{allPlots})")  # close multipage PDF


    # ROOT.FSHistogram.dumpHistogramCache("kspiplamb_plots_v2")

    endTime = time.time()
    print(f"Time to run: {endTime - startTime:.1f} seconds")

if __name__ == "__main__":
    setup()
