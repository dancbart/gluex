# from wurlitzer import pipes

# apptainer exec --contain --writable-tmpfs -B /volatile/halld/home/dbarton,/cache/halld/home/dbarton,/work/halld/home/dbarton/gluex,/scratch --env BASH_ENV=/dev/null /w/halld-scshelf2101/lng/WORK/PyAmpTools9/pyamptools.sif bash -c "source /etc/bash.bashrc; pip install gitpython; jupyter-lab --no-browser --port=8888; exec bash"

import ROOT
from pyamptools import atiSetup
# import os
# os.chdir("/work/halld/home/dbarton/gluex/KShortPipLambda")
# os.listdir()
atiSetup.setup(globals(), use_fsroot=True)

# INDICES ASSIGNED BY 'flatten':
# 1. DecayingLambda (0)   1a. Proton (1)   1b. PiMinus2 (2)
# 2. DecayingKShort (3)   2a. PiPlus2 (4)   2b. PiMinus1 (5)
# 3. PiPlus1 (6)

# DEFINE VARIABLES CORRESPOONDING TO THE INDICES
DecayingLambda = "1"
Proton = "1a"
PiMinus2 = "1b"
DecayingKShort = "2"
PiPlus2 = "2a"
PiMinus1 = "2b"
PiPlus1 = "3"
NegOne = "-1.*"


# DEFINE CUTS
ROOT.FSCut.defineCut("rf","RFDeltaT", "-2.004","2.004", "-20.0","-6.0","6.0","20.0", 1./6.) # from Hao's kp pi0 channel.  Adjust for kspip
ROOT.FSCut.defineCut("chi2DOF","Chi2DOF","0.0","5.0")
ROOT.FSCut.defineCut("unusedE","EnUnusedSh","0.0","0.1") # UnusedEnergy (unused "shower"? energy)
ROOT.FSCut.defineCut("unusedTracks","NumUnusedTracks<1") # No unused tracks
ROOT.FSCut.defineCut("coherentPeak","EnPB","8.2","8.8") # Coherent peak: 8.2 < E_beam < 8.8
ROOT.FSCut.defineCut("tRange",f"abs(MASS2(GLUEXTARGET,-{DecayingLambda})<1.0)")
ROOT.FSCut.defineCut("tBin1",f"abs(MASS2(GLUEXTARGET,-{DecayingLambda})", "0.1", "0.4")
ROOT.FSCut.defineCut("tBin2",f"abs(MASS2(GLUEXTARGET,-{DecayingLambda})", "0.4", "0.7")
ROOT.FSCut.defineCut("tBin3",f"abs(MASS2(GLUEXTARGET,-{DecayingLambda})", "0.7", "1.0")

ROOT.FSCut.defineCut("flightSigLambda","VeeLP1>2.0")
ROOT.FSCut.defineCut("flightSigKShort","VeeLP2>2.0")
ROOT.FSCut.defineCut("selectLambda",f"MASS({Proton},{PiMinus2})","1.11","1.125", "1.00", "1.11", "1.125", "1.132")
ROOT.FSCut.defineCut("selectKShort",f"MASS({DecayingKShort})","0.48","0.52", "0.3", "0.48", "0.52", "0.7")
ROOT.FSCut.defineCut("selectKSTAR892",f"MASS({DecayingKShort},{PiPlus1})","0.83","0.96", "0.60", "0.83", "0.96", "1.1")
ROOT.FSCut.defineCut("selectKSTAR1430",f"MASS({DecayingKShort},{PiPlus1})","1.30","1.55", "1.1", "1.30", "1.55", "1.7")
ROOT.FSCut.defineCut("rejectSigmas", f"MASS({DecayingLambda},{PiPlus1})","2.0","3.5")

# Other cuts.  ARE THESE RIGHT???
ROOT.FSCut.defineCut("targetZ","ZVertex","-10.0","10.0") # Target Z
ROOT.FSCut.defineCut("missingMass2Lambda","MM2Lambda","-0.1","0.1") # 

# MissingMass2 for Lambda

def gluex_style():
    style = ROOT.TStyle("GlueX", "Default GlueX Style")

    style.SetCanvasBorderMode(0)
    style.SetPadBorderMode(0)
    style.SetPadColor(0)
    style.SetCanvasColor(0)
    style.SetTitleColor(0)
    style.SetStatColor(0)

    style.SetCanvasDefW(800)
    style.SetCanvasDefH(600)

    style.SetPadBottomMargin(0.15)
    style.SetPadLeftMargin(0.15)
    style.SetPadTopMargin(0.05)
    style.SetPadRightMargin(0.08)

    style.SetStripDecimals(0)
    style.SetLabelSize(0.055, "xyz")
    style.SetTitleSize(0.06, "xyz")
    style.SetTitleFont(42, "xyz")
    style.SetLabelFont(42, "xyz")
    style.SetTitleOffset(1.2, "y")
    style.SetLabelOffset(0.01, "xyz")

    style.SetOptStat(0)
    style.SetOptTitle(0)
    style.SetHistLineWidth(2)
    style.SetHistFillColor(920)  # grey

    # style.SetPadGridX(1)
    # style.SetPadGridY(1)

    style.SetPalette(ROOT.kViridis)

    style.cd()

# ROOT.FSHistogram.readHistogramCache("/work/halld/home/dbarton/gluex/KShortPipLambda/histos_pipkslamb")


# POSSIBLE CUTS
# rf,chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,flightSigLambda,flightSigKShort,selectLambda,selectKShort,selectKSTAR892,selectKSTAR1430,rejectSigmas

cutsKS = "chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,flightSigKShort"
cutsLAMB = "chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,flightSigLambda"
cutsK892 = "chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,flightSigLambda,flightSigKShort,rejectSigmas"
cutsK892loose = "chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,flightSigLambda,flightSigKShort"
cutsDALITZ = "chi2DOF,unusedE,unusedTracks,coherentPeak,tRange,rejectSigmas"
cutsDALITZloose = "chi2DOF,unusedE,unusedTracks,coherentPeak,tRange"


# # KSHORT
# hist_ks_prompt = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({DecayingKShort})", "(100, 0.45, 0.55)", f"CUT({cutsKS},rf)")
# hist_ks_OUTATIMEsb = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({DecayingKShort})", "(100, 0.45, 0.55)", f"CUT({cutsKS})&&CUTSB(rf)")
# hist_ks_reduced = hist_ks_prompt.Clone("hist_ks_reduced")
# hist_ks_reduced.Add(hist_ks_OUTATIMEsb, -1)

# LAMBDA
hist_lamb_prompt = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({Proton}, {PiMinus2})", "(64, 1.1, 1.132)", f"CUT({cutsLAMB},rf)")
hist_lamb_OUTATIMEsb = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({Proton}, {PiMinus2})", "(64, 1.1, 1.132)", f"CUT({cutsLAMB})&&CUTSB(rf)")
hist_lamb_reduced = hist_lamb_prompt.Clone("hist_lamb_reduced")
hist_lamb_reduced.Add(hist_lamb_OUTATIMEsb, -1)

# # K*
# hist_k892_prompt = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1})", "(100, 0.6, 2.00)", f"CUT({cutsK892},rf)")
# hist_k892_OUTATIMEsb = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1})", "(100, 0.6, 2.00)", f"CUT({cutsK892})&&CUTSB(rf)")
# hist_k892_reduced = hist_k892_prompt.Clone("hist_k892_reduced")
# hist_k892_reduced.Add(hist_k892_OUTATIMEsb, -1)

# # K* Loose
# hist_k892_prompt_Loose = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1})", "(100, 0.6, 2.00)", f"CUT({cutsK892loose},rf)")
# hist_k892_OUTATIMEsb_Loose = ROOT.FSHistogram.getTH1F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1})", "(100, 0.6, 2.00)", f"CUT({cutsK892loose})&&CUTSB(rf)")
# hist_k892_reduced_Loose = hist_k892_prompt_Loose.Clone("hist_k892_reduced_Loose")
# hist_k892_reduced_Loose.Add(hist_k892_OUTATIMEsb_Loose, -1)

# # DALITZ PLOTS
# dalitz_kspipVSlambpip_prompt = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100, 0.0, 14.0, 100, 0.0, 9.0)", f"CUT({cutsK892},rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# dalitz_kspipVSlambpip_OUTATIMEsb = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100, 0.0, 14.0, 100, 0.0, 9.0)", f"CUT({cutsK892})&&CUTSB(rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# dalitz_kspipVSlambpip_reduced = dalitz_kspipVSlambpip_prompt.Clone("dalitz_kspipVSlambpip_reduced")
# dalitz_kspipVSlambpip_reduced.Add(dalitz_kspipVSlambpip_OUTATIMEsb, -1)

# # DALITZ PLOTS Loose
# dalitz_kspipVSlambpip_prompt_Loose = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100, 0.0, 14.0, 100, 0.0, 9.0)", f"CUT({cutsK892loose},rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# dalitz_kspipVSlambpip_OUTATIMEsb_Loose = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS2({DecayingKShort},{PiPlus1}):MASS2({DecayingLambda},{PiPlus1})", "(100, 0.0, 14.0, 100, 0.0, 9.0)", f"CUT({cutsK892loose})&&CUTSB(rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# dalitz_kspipVSlambpip_reduced_Loose = dalitz_kspipVSlambpip_prompt_Loose.Clone("dalitz_kspipVSlambpip_reduced_Loose")
# dalitz_kspipVSlambpip_reduced_Loose.Add(dalitz_kspipVSlambpip_OUTATIMEsb_Loose, -1)

# # 2_DIMENSIONAL PLOTS
# twoD_kspipVSlambpip_prompt = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1}):MASS({DecayingLambda},{PiPlus1})", "(100, 1.0, 4.0, 100, 0.2, 3.5)", f"CUT({cutsK892},rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# twoD_kspipVSlambpip_OUTATIMEsb = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1}):MASS({DecayingLambda},{PiPlus1})", "(100, 1.0, 4.0, 100, 0.2, 3.5)", f"CUT({cutsK892})&&CUTSB(rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# twoD_kspipVSlambpip_reduced = twoD_kspipVSlambpip_prompt.Clone("twoD_kspipVSlambpip_reduced")
# twoD_kspipVSlambpip_reduced.Add(twoD_kspipVSlambpip_OUTATIMEsb, -1)

# # 2_DIMENSIONAL PLOTS Loose
# twoD_kspipVSlambpip_prompt_Loose = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1}):MASS({DecayingLambda},{PiPlus1})", "(100, 1.0, 4.0, 100, 0.2, 3.5)", f"CUT({cutsK892loose},rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# twoD_kspipVSlambpip_OUTATIMEsb_Loose = ROOT.FSHistogram.getTH2F(fileName, treeName, f"MASS({DecayingKShort},{PiPlus1}):MASS({DecayingLambda},{PiPlus1})", "(100, 1.0, 4.0, 100, 0.2, 3.5)", f"CUT({cutsK892loose})&&CUTSB(rf)") # MASS2(y-axis1,y-axis2):MASS2(x-axis1,x-axis2), "x_bins, x_min, x_max, y_bins, y_min, y_max"
# twoD_kspipVSlambpip_reduced_Loose = twoD_kspipVSlambpip_prompt_Loose.Clone("twoD_kspipVSlambpip_reduced_Loose")
# twoD_kspipVSlambpip_reduced_Loose.Add(twoD_kspipVSlambpip_OUTATIMEsb_Loose, -1)

# ROOT.FSHistogram.clearHistogramCache("histos_pipkslamb")

# FOR MULTIPLE FINAL STATES AND TO MANAGE PARTICLE COMBINATORICS WITHIN THOSE FINAL STATES.    
# h1 = ROOT.FSModeHistogram.getTH1F(fileName, treeName, f"MASS({KPlus},{DecayingPi0},{Proton},{PiMinus})", "(80, 0.0, 4.0)", "", "CUT(chi2DOF,unusedE,unusedTracks,coherentPeak)&&CUTSB(selectLambda)")

from IPython.display import Image, display
latex = ROOT.TLatex()

plotTitle = 'Data: \gamma p \\rightarrow K_{s} \pi^{+} \Lambda'
axisLabel = 'M(Proton \pi^{-}) [GeV]'

# INDICES ASSIGNED BY 'flatten':
# 1. DecayingLambda (0)   1a. Proton (1)   1b. PiMinus2 (2)
# 2. DecayingKShort (3)   2a. PiPlus2 (4)   2b. PiMinus1 (5)
# 3. PiPlus1 (6)

def plot_hist():

    gluex_style()
    ROOT.gStyle.SetOptStat(1111)  # show stats (gluex_style hides this off by default)
    ROOT.FSHistogram.clearHistogramCache()
    
    canvas = ROOT.TCanvas('c', 'c', 800, 600)
    canvas.SetLeftMargin(0.15)

    gaussNdbl = ROOT.TF1("gaussNdbl","((gausn(0) + gausn(3) + [6] + [7]*x) / 0.0005)",1.1,1.132)
    gaussNdbl.SetLineColor(ROOT.kBlue)
    gaussNdbl.SetLineWidth(2)
    gaussNdbl.SetLineStyle(1)
    print("Formula string:", gaussNdbl.GetFormula().GetExpFormula())
    gaussNdbl.SetParName(0, "gaus1_amplitude")
    gaussNdbl.SetParName(1, "gaus1_mean")
    gaussNdbl.SetParName(2, "gaus1_sigma_detectorResolution")
    gaussNdbl.SetParName(3, "GAUS2_AMPLITUDE")
    gaussNdbl.SetParName(4, "GAUS2_MEAN")
    gaussNdbl.SetParName(5, "GAUS2_SIGMA_detectorResolution")
    gaussNdbl.SetParName(6, "Linear_offset")
    gaussNdbl.SetParName(7, "Linear_factor")
    print("Formula string:", gaussNdbl.GetFormula().GetExpFormula())

    gaussNdbl.SetParameter("gaus1_amplitude", 0.00625)
    # gaussNdbl.SetParameter("gaus1_amplitude", 0.0317)
    gaussNdbl.SetParameter("gaus1_mean", 1.116)
    gaussNdbl.SetParameter("gaus1_sigma_detectorResolution", 0.00251)
    # gaussNdbl.SetParameter("gaus1_sigma_detectorResolution", 0.00522)
    # gaussNdbl.FixParameter(0, 00.003)
    # gaussNdbl.FixParameter(1, 1.115683)
    # gaussNdbl.FixParameter(2, 0.00005)

    gaussNdbl.SetParameter("GAUS2_AMPLITUDE", 0.00502)
    gaussNdbl.SetParameter("GAUS2_MEAN", 1.11746)
    gaussNdbl.SetParameter("GAUS2_SIGMA_detectorResolution", 0.00280)
    # gaussNdbl.FixParameter(3, 0.00025)
    # gaussNdbl.FixParameter(4, 1.11746)
    # gaussNdbl.FixParameter(5, 0.00159)

    # gaussNdbl.SetParameter("Linear_offset", 0.04077)
    gaussNdbl.SetParameter("Linear_factor", 0.00008)
    gaussNdbl.FixParameter(6, 0.04077)
    # gaussNdbl.FixParameter(7, 0.00)

    hist_lamb_reduced.SetStats(False)
    hist_lamb_reduced.SetLineColor(ROOT.kBlack)
    # hist_lamb_reduced.SetLineStyle(1)
    # hist_lamb_reduced.SetLineWidth(2)
    hist_lamb_reduced.SetMarkerStyle(20)
    hist_lamb_reduced.SetMarkerSize(0.6)
    hist_lamb_reduced.GetXaxis().SetTitle(axisLabel)
    hist_lamb_reduced.GetYaxis().SetTitle("Counts / 0.5 MeV")
    hist_lamb_reduced.Draw("")
    hist_lamb_reduced.Fit(gaussNdbl, "RSQ")
    fit_result = hist_lamb_reduced.Fit(gaussNdbl, "RSQ")
    print("Fit valid:", fit_result.IsValid())
    print("Fit status code:", fit_result.Status())
    print("Covariance matrix status:", fit_result.CovMatrixStatus())
    print("Chi2:", fit_result.Chi2())
    print("NDF:", fit_result.Ndf())
    print("Chi2/NDF:", fit_result.Chi2() / fit_result.Ndf() if fit_result.Ndf() else float('inf'))
    gaussNdbl.Draw("same")

    # hMC.SetStats(False)
    # # hMC.SetMarkerColor(ROOT.kBlue)
    # # hMC.SetMarkerStyle(4)
    # hMC.SetMarkerStyle(0)
    # # hMC.SetMarkerSize(0.8)
    # hMC.SetMarkerSize(0)
    # hMC.SetLineColor(ROOT.kBlue)
    # hMC.SetLineStyle(1)
    # hMC.SetLineWidth(2)
    # hMC.SetFillColor(ROOT.kBlue)
    # hMC.SetFillStyle(3002)
    # hMC.GetXaxis().SetTitle(axisLabel)
    # hMC.Scale(3.8)
    # hMC.Draw("same hist")
    # # hMC.Fit(voigtian, "RQ")
    # # voigtian.Draw("same")

    # hTHROWN.

    legend1 = ROOT.TLegend(0.67, 0.82, 0.92, 0.92) # x_left, y_bottom, x_right, y_top
    legend1.AddEntry(hist_lamb_reduced, ' KinFit Data', 'lP')
    legend1.AddEntry(hist_lamb_reduced, ' accidentals subtracted', "")
    legend1.AddEntry(gaussNdbl, ' gaussNdbl fit', 'l')
    legend1.Draw("same hist")

    print("Minimum bin content in histogram:", hist_lamb_reduced.GetMinimum())

    print(f"{'Index':<5} {'Name':<30} {'Value':>10} {'Error':>10}")
    print("-" * 60)
    for i in range(gaussNdbl.GetNpar()):
        name = gaussNdbl.GetParName(i)
        val = gaussNdbl.GetParameter(i)
        err = gaussNdbl.GetParError(i)
        print(f"{i:<5} {name:<30} {val:>10.5f} {err:>10.5f}")

    img_path = 'plots/Lambda_m_sb_gaussNdbl_TEST1'
    canvas.SaveAs(img_path + '.pdf')
    canvas.SaveAs(img_path + '.png')
    canvas.Close()
    display(Image(filename=img_path + '.png'))
    os.remove(img_path + '.png')

plot_hist()