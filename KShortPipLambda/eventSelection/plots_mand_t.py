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
# Files
# -----------------------------
# FND = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSflat_Spr-Fa18.root"
FND = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_small.root"
FND_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"
# FNC_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/spring2020/testMC_webform/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_071350-58.root"

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


# -----------------------------
# Define variables for t_prime_Ks: t' = |t - t_0|
# -----------------------------
p3_ks ="2"   # KShort
p4_ks = "1,3"   # recoil Lambda

s_ks    = "MASS2(GLUEXBEAM,GLUEXTARGET)"
sqs_ks  = f"sqrt({s_ks})"
m1sq_ks = "0.0"
m2sq_ks = "MASS2(GLUEXTARGET)"
m3sq_ks = f"MASS2({p3_ks})"
m4sq_ks = f"MASS2({p4_ks})"

E1_ks   = f"(({s_ks})+({m1sq_ks})-({m2sq_ks}))/(2*({sqs_ks}))"
E3_ks   = f"(({s_ks})+({m3sq_ks})-({m4sq_ks}))/(2*({sqs_ks}))"
p1_ks   = f"sqrt(({E1_ks})*({E1_ks})-({m1sq_ks}))"      # = E1 for photon
p3cm_ks = f"sqrt(({E3_ks})*({E3_ks})-({m3sq_ks}))"

t_ks    = f"MASS2(GLUEXBEAM,-{p3_ks})"
t0_ks   = f"({m1sq_ks})+({m3sq_ks})-2*((({E1_ks})*({E3_ks}))-(({p1_ks})*({p3cm_ks})))"

tprime_ks     = f"(({t_ks})-({t0_ks}))"

# -----------------------------
# Define variables for t_prime_Pip: t' = |t - t_0|
# -----------------------------
p3_pip = "3"   # PiPlus
p4_pip = "1,2"   # recoil Lambda

s_pip    = "MASS2(GLUEXBEAM,GLUEXTARGET)"
sqs_pip  = f"sqrt({s_pip})"
m1sq_pip = "0.0"
m2sq_pip = "MASS2(GLUEXTARGET)"
m3sq_pip = f"MASS2({p3_pip})"
m4sq_pip = f"MASS2({p4_pip})"

E1_pip   = f"(({s_pip})+({m1sq_pip})-({m2sq_pip}))/(2*({sqs_pip}))"
E3_pip   = f"(({s_pip})+({m3sq_pip})-({m4sq_pip}))/(2*({sqs_pip}))"
p1_pip   = f"sqrt(({E1_pip})*({E1_pip})-({m1sq_pip}))"      # = E1 for photon
p3cm_pip = f"sqrt(({E3_pip})*({E3_pip})-({m3sq_pip}))"

t_pip    = f"MASS2(GLUEXBEAM,-{p3_pip})"
t0_pip   = f"({m1sq_pip})+({m3sq_pip})-2*((({E1_pip})*({E3_pip}))-(({p1_pip})*({p3cm_pip})))"

tprime_pip     = f"(({t_pip})-({t0_pip}))"



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
    allPlots = "plots/plots_mand_t.pdf"

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
#    ROOT.FSCut.defineCut("coherentPeak", "EnPB>8.2 && EnPB<8.8")
    ROOT.FSCut.defineCut("coherentPeak", "EnPB>8.2 && EnPB<8.6")
    ROOT.FSCut.defineCut("flightLengthLambda", "VeeLP1>2.0")
    ROOT.FSCut.defineCut("flightLengthKShort", "VeeLP2>2.0")
    ROOT.FSCut.defineCut("targetZ", "ProdVz>52.0 && ProdVz<78.0")

    # CUTS WITH SIDEBANDS
    ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0,)
    ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0,)
    ROOT.FSCut.defineCut("selectKSTAR892", f"MASS({DecayingKShort},{PiPlus1})>0.80 && MASS({DecayingKShort},{PiPlus1})<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})>2.0 && MASS({DecayingLambda},{PiPlus1})<4.0")
    # ROOT.FSCut.defineCut("selectKSTAR1430", f"MASS({DecayingKShort},{PiPlus1})", "0.85", "0.95", "0.0", "0.85", "0.95", "1.0",)


#     # -----------------------------
#     # Canvas 1 Delta_t (t_ks - t_pip)
#     # -----------------------------
#     c1 = ROOT.TCanvas("c1", "c1", 1600, 1200)
# #    c1.Divide(3, 3)

# #    c1.cd(1)
#     ROOT.gPad.SetRightMargin(0.18)
#     h1 = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"(-1*MASS2(GLUEXBEAM,-{DecayingKShort})) - (-1*MASS2(GLUEXBEAM,-{PiPlus1})):MASS({DecayingKShort},{PiPlus1})", "(100,0.4,4.0,100,-10.0, 10.0)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
# #    h1b = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"(-1*MASS2(GLUEXBEAM,-{PiPlus1})):MASS({DecayingKShort},{PiPlus1})", "(100,0.4,4.0,100,0.0, 10.0)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
# #    h1c = h1a.Clone("h1c")
# #    h1c.Add(h1b, -1)
#     h1.SetTitle("|-t|")
#     h1.SetXTitle("M(K_{s} \pi^{+})")
#     h1.SetYTitle("t_{K_{s}} - t_{\pi^{+}}")
#     h1.Draw("colz")
#     ROOT.gPad.Update()
#     if bggen:
#         ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "(100,0,2)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
#     lab1.DrawLatex(0.5, 1.00, f"{label}")
#     ROOT.gPad.Update()

#     c1.Print(f"{allPlots}(") # open multipage PDF


    # -----------------------------
    # Canvas 1 Delta_t (t_ks - t_pip)
    # -----------------------------
    c1 = ROOT.TCanvas("c1", "c1", 1600, 1200)
#    c1.Divide(3, 3)

#    c1.cd(1)
    ROOT.gPad.SetRightMargin(0.18)
    h1 = ROOT.FSModeHistogram.getTH1F(FND, NT, "m100000000_1100", f"(MMASS({DecayingKShort},{PiPlus1})", "(100,0.0,2.0)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
#    h1b = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"(-1*MASS2(GLUEXBEAM,-{PiPlus1})):MASS({DecayingKShort},{PiPlus1})", "(100,0.4,4.0,100,0.0, 10.0)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
#    h1c = h1a.Clone("h1c")
#    h1c.Add(h1b, -1)
    # h1.SetTitle("|-t|")
    h1.SetXTitle("MM(K_{s} \pi^{+})")
    h1.SetYTitle("counts")
    h1.Draw()
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "(100,0,2)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c1.Print(f"{allPlots}(") # open multipage PDF


    # -----------------------------
    # Canvas 2 Delta_t_PRIME (t_prime_ks - t_prime_pip). t' = |t - t_min| with t_min = t(theta_cm = 0) = t_0, i.e. forward-angle limit
    # -----------------------------
    c2 = ROOT.TCanvas("c2", "c2", 1600, 1200)
#    c1.Divide(3, 3)


#    c2.cd(1)
    ROOT.gPad.SetRightMargin(0.18)
    h2 = ROOT.FSModeHistogram.getTH2F(FND, NT, "m100000000_1100", f"{tprime_ks} - {tprime_pip}:MASS({DecayingKShort},{PiPlus1})", "(100,0.4,4.0,100,0.0, 10.0)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
    h2.SetTitle("|-t|")
    h2.SetXTitle("M(K_{s} \pi^{+})")
    h2.SetYTitle("t'_{K_{s}} - t'_{\pi^{+}}")
    h2.Draw("colz")
    ROOT.gPad.Update()
    if bggen:
        ROOT.FSModeHistogram.drawMCComponentsSame(FND, NT, "m100000000_1100", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))", "(100,0,2)", "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)")
    lab1.DrawLatex(0.5, 1.00, f"{label}")
    ROOT.gPad.Update()

    c2.Print(f"{allPlots})") # close multipage PDF

    endTime = time.time()
    print(f"Time to run: {endTime - startTime:.1f} seconds")

if __name__ == "__main__":
    setup()
