import os
import time
import ROOT

ROOT.gROOT.SetBatch(True)

from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)
allPlots = "plots/PWA_plots.pdf"

# -----------------------------
# Files / globals
# -----------------------------
t_bin = "#bf{-t = (0.8 - 1.0) GeV^{2}}" # t_bin label for plots.  MUST match the t_bin used to create the ROOT file.
FND = "/work/halld/home/dbarton/gluex/KShortPipLambda/PWA/outputTrees/FIT_pipkslamb_Zlm_20260804_110953/KsPipLamb_ALL.root"

NT = "ntFSGlueX_MODECODE"
TREENAME = "ntFSGlueX_100000000_1100"

# Keep ROOT objects alive if needed
_KEEP = []

def keep(*objs):
    _KEEP.extend(objs)


# -----------------------------
# Style / setup
# -----------------------------
def gluex_style():
    style = ROOT.TStyle("GlueX", "Default GlueX Style")

    style.SetCanvasBorderMode(0)
    style.SetPadBorderMode(0)
    style.SetPadColor(0)
    style.SetCanvasColor(0)
    style.SetTitleColor(0)
    style.SetStatColor(0)

    style.SetCanvasDefW(900)
    style.SetCanvasDefH(800)

    style.SetPadBottomMargin(0.16)
    style.SetPadLeftMargin(0.16)
    style.SetPadTopMargin(0.05)
    style.SetPadRightMargin(0.06)

    style.SetStripDecimals(0)
    style.SetLabelSize(0.045, "xyz")
    style.SetTitleSize(0.055, "xyz")
    style.SetTitleFont(42, "xyz")
    style.SetLabelFont(42, "xyz")
    style.SetTitleOffset(1.25, "y")
    style.SetTitleOffset(1.05, "x")

    style.SetOptStat(0)
    style.SetOptTitle(0)
    style.SetHistLineWidth(2)
    style.SetHistFillColor(920)
    style.SetPalette(ROOT.kViridis)

    ROOT.gROOT.SetStyle("GlueX")
    ROOT.gROOT.ForceStyle()


def setup():
    if ROOT.FSModeCollection.modeVector().size() != 0:
        return
    ROOT.FSModeCollection.addModeInfo("100000000_1100").addCategory("m100000000_1100")


# -----------------------------
# Histogram loading
# -----------------------------
def get_hist_or_raise(root_file, name):
    h = root_file.Get(name)
    if not h:
        raise RuntimeError(f"Histogram '{name}' not found in file")
    h = h.Clone(name)
    h.SetDirectory(0)
    return h

def load_histograms(filename):
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        raise RuntimeError(f"Could not open ROOT file: {filename}")

# def load_histograms(filename):
#     f = ROOT.TFile.Open(filename)
#     if not f or f.IsZombie():
#         raise RuntimeError(f"Could not open ROOT file: {filename}")

    hist = {
        "CosThetaM2_hel_dat":      get_hist_or_raise(f, "CosThetaM2_hel_dat"),
        "CosThetaM2_hel_acc_All_Full": get_hist_or_raise(f, "CosThetaM2_hel_acc_All_Full"),
        "CosThetaM2_hel_acc_0S_BothRefl": get_hist_or_raise(f, "CosThetaM2_hel_acc_0S_BothRefl"),
        "CosThetaM2_hel_acc_1P+1p_BothRefl": get_hist_or_raise(f, "CosThetaM2_hel_acc_1P+1p_BothRefl"),
        "CosThetaM2_hel_acc_1P+0p_BothRefl": get_hist_or_raise(f, "CosThetaM2_hel_acc_1P+0p_BothRefl"),
        "CosThetaM2_hel_acc_1P-1p_BothRefl": get_hist_or_raise(f, "CosThetaM2_hel_acc_1P-1p_BothRefl"),
        "CosThetaM2_hel_acc_1P_BothRefl": get_hist_or_raise(f, "CosThetaM2_hel_acc_1P_BothRefl"),
        "CosThetaM2_hel_gen_All_Full": get_hist_or_raise(f, "CosThetaM2_hel_gen_All_Full"),
        "CosThetaM2_hel_bkg": get_hist_or_raise(f, "CosThetaM2_hel_bkg"),

        "PhiM2_hel_dat":      get_hist_or_raise(f, "PhiM2_hel_dat"),
        "PhiM2_hel_acc_All_Full": get_hist_or_raise(f, "PhiM2_hel_acc_All_Full"),
        "PhiM2_hel_acc_0S_BothRefl": get_hist_or_raise(f, "PhiM2_hel_acc_0S_BothRefl"),
        "PhiM2_hel_acc_1P+1p_BothRefl": get_hist_or_raise(f, "PhiM2_hel_acc_1P+1p_BothRefl"),
        "PhiM2_hel_acc_1P+0p_BothRefl": get_hist_or_raise(f, "PhiM2_hel_acc_1P+0p_BothRefl"),
        "PhiM2_hel_acc_1P-1p_BothRefl": get_hist_or_raise(f, "PhiM2_hel_acc_1P-1p_BothRefl"),
        "PhiM2_hel_acc_1P_BothRefl": get_hist_or_raise(f, "PhiM2_hel_acc_1P_BothRefl"),
        "PhiM2_hel_gen_All_Full": get_hist_or_raise(f, "PhiM2_hel_gen_All_Full"),
        "PhiM2_hel_bkg": get_hist_or_raise(f, "PhiM2_hel_bkg"),
    
        "BigPhi_hel_dat":      get_hist_or_raise(f, "BigPhi_hel_dat"),
        "BigPhi_hel_acc_All_Full": get_hist_or_raise(f, "BigPhi_hel_acc_All_Full"),
        "BigPhi_hel_acc_0S_BothRefl": get_hist_or_raise(f, "BigPhi_hel_acc_0S_BothRefl"),
        "BigPhi_hel_acc_1P+1p_BothRefl": get_hist_or_raise(f, "BigPhi_hel_acc_1P+1p_BothRefl"),
        "BigPhi_hel_acc_1P+0p_BothRefl": get_hist_or_raise(f, "BigPhi_hel_acc_1P+0p_BothRefl"),
        "BigPhi_hel_acc_1P-1p_BothRefl": get_hist_or_raise(f, "BigPhi_hel_acc_1P-1p_BothRefl"),
        "BigPhi_hel_acc_1P_BothRefl": get_hist_or_raise(f, "BigPhi_hel_acc_1P_BothRefl"),
        "BigPhi_hel_gen_All_Full": get_hist_or_raise(f, "BigPhi_hel_gen_All_Full"),
        "BigPhi_hel_bkg": get_hist_or_raise(f, "BigPhi_hel_bkg"),

        "PhiMinusBigPhiM2_hel_dat":      get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_dat"),
        "PhiMinusBigPhiM2_hel_acc_All_Full": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_acc_All_Full"),
        "PhiMinusBigPhiM2_hel_acc_0S_BothRefl": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_acc_0S_BothRefl"),
        "PhiMinusBigPhiM2_hel_acc_1P+1p_BothRefl": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_acc_1P+1p_BothRefl"),
        "PhiMinusBigPhiM2_hel_acc_1P+0p_BothRefl": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_acc_1P+0p_BothRefl"),
        "PhiMinusBigPhiM2_hel_acc_1P-1p_BothRefl": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_acc_1P-1p_BothRefl"),
        "PhiMinusBigPhiM2_hel_acc_1P_BothRefl": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_acc_1P_BothRefl"),
        "PhiMinusBigPhiM2_hel_gen_All_Full": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_gen_All_Full"),
        "PhiMinusBigPhiM2_hel_bkg": get_hist_or_raise(f, "PhiMinusBigPhiM2_hel_bkg"),

        "hMass23_dat":      get_hist_or_raise(f, "hMass23_dat"),
        "hMass23_acc_All_Full": get_hist_or_raise(f, "hMass23_acc_All_Full"),
        "hMass23_acc_0S_BothRefl": get_hist_or_raise(f, "hMass23_acc_0S_BothRefl"),
        "hMass23_acc_1P+1p_BothRefl": get_hist_or_raise(f, "hMass23_acc_1P+1p_BothRefl"),
        "hMass23_acc_1P+0p_BothRefl": get_hist_or_raise(f, "hMass23_acc_1P+0p_BothRefl"),
        "hMass23_acc_1P-1p_BothRefl": get_hist_or_raise(f, "hMass23_acc_1P-1p_BothRefl"),
        "hMass23_acc_1P_BothRefl": get_hist_or_raise(f, "hMass23_acc_1P_BothRefl"),
        "hMass23_gen_All_Full": get_hist_or_raise(f, "hMass23_gen_All_Full"),
        "hMass23_bkg": get_hist_or_raise(f, "hMass23_bkg"),

    }

    f.Close()
    return hist


# -----------------------------
# Small helpers
# -----------------------------
def ensure_plot_dir(pdf_path):
    outdir = os.path.dirname(pdf_path)
    if outdir:
        os.makedirs(outdir, exist_ok=True)


def make_canvas_with_bottompad(
    name,
    width=1000,
    height=1100,
    info_frac=0.22,
    left_margin=0.18,
    right_margin=0.06,
    top_margin=0.08,
    bottom_margin_plot=0.18,
    top_margin_info=0.02,
    bottom_margin_info=0.20,
):
    """
    Layout:
      - plot pad on top
      - info pad on bottom

    info_frac is the fractional height of the bottom info pad.
    """
    c = ROOT.TCanvas(name, name, width, height)

    # Top plot pad: y from info_frac to 1
    pad_plot = ROOT.TPad(
        f"{name}_plot", f"{name}_plot",
        0.00, info_frac, 1.00, 1.00
    )
    pad_plot.SetFillColor(0)
    pad_plot.SetBorderMode(0)
    pad_plot.SetLeftMargin(left_margin)
    pad_plot.SetRightMargin(right_margin)
    pad_plot.SetTopMargin(top_margin)
    pad_plot.SetBottomMargin(bottom_margin_plot)
    pad_plot.Draw()

    # Bottom info pad: y from 0 to info_frac
    pad_info = ROOT.TPad(
        f"{name}_info", f"{name}_info",
        0.00, 0.00, 1.00, info_frac
    )
    pad_info.SetFillColor(0)
    pad_info.SetBorderMode(0)
    pad_info.SetLeftMargin(left_margin)
    pad_info.SetRightMargin(right_margin)
    pad_info.SetTopMargin(top_margin_info)
    pad_info.SetBottomMargin(bottom_margin_info)
    pad_info.Draw()

    keep(c, pad_plot, pad_info)
    return c, pad_plot, pad_info


def draw_bottom_info_pad(info_pad, label_text, legend_items=None, notes=None):
    """
    legend_items: list of (obj, text, drawopt)
    notes: list of strings
    """
    info_pad.cd()
    info_pad.Clear()

    # separator line at top of info pad
    line = ROOT.TLine(0.0, 0.98, 1.0, 0.98)
    line.SetNDC(True)
    line.SetLineColor(ROOT.kGray + 1)
    line.Draw()
    keep(line)

    # Legend on right
    if legend_items:
        leg = ROOT.TLegend(0.58, 0.18, 0.90, 0.86)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.SetTextSize(0.10)
        for obj, text, opt in legend_items:
            leg.AddEntry(obj, text, opt)
        leg.Draw()
        keep(leg)

    # Label + notes on left
    tex = ROOT.TLatex()
    tex.SetNDC(True)
    tex.SetTextFont(42)
    tex.SetTextAlign(13)

    tex.SetTextSize(0.18)
    tex.DrawLatex(0.06, 0.92, f"#bf{{{label_text}}}")
    keep(tex)

    if notes:
        y = 0.73
        for note in notes:
            t = ROOT.TLatex()
            t.SetNDC(True)
            t.SetTextFont(42)
            t.SetTextSize(0.12)
            t.SetTextAlign(13)
            t.DrawLatex(0.06, y, note)
            keep(t)
            y -= 0.17

    info_pad.Modified()
    info_pad.Update()


def integral_between(hist, xmin, xmax):
    ax = hist.GetXaxis()
    bin1 = ax.FindBin(xmin)
    bin2 = ax.FindBin(xmax)
    return hist.Integral(bin1, bin2)


def open_pdf(canvas, pdf_path):
    canvas.Print(f"{pdf_path}(")


def add_pdf_page(canvas, pdf_path):
    canvas.Print(pdf_path)


def close_pdf(canvas, pdf_path):
    canvas.Print(f"{pdf_path})")


def style_data_mc_overlay(h_data, h_sum, h_bkg):
    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)

    h_sum.SetLineColor(ROOT.kGreen - 6)
    h_sum.SetFillColorAlpha(ROOT.kGreen - 2, 0.60)
    h_sum.SetFillStyle(1001)

    h_bkg.SetLineColor(ROOT.kRed - 6)
    h_bkg.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_bkg.SetFillStyle(1001)

def make_efficiency_corrected(h_data, h_acc, h_gen, name):
    """
    Divide data by (acc/gen) bin-by-bin.
    Bins where gen == 0 are set to 0.
    """
    h_eff = h_acc.Clone(f"h_eff_{name}")
    h_eff.Divide(h_gen)  # eff = acc / gen, bin-by-bin

    h_corr = h_data.Clone(f"h_corr_{name}")
    for i in range(1, h_corr.GetNbinsX() + 1):
        eff_val = h_eff.GetBinContent(i)
        if eff_val > 0:
            h_corr.SetBinContent(i, h_data.GetBinContent(i) / eff_val)
            # Error propagation: δ(data/eff) ≈ sqrt(data)/eff  (stat. only)
            h_corr.SetBinError(i, h_data.GetBinError(i) / eff_val)
        else:
            h_corr.SetBinContent(i, 0)
            h_corr.SetBinError(i, 0)
    return h_corr



def cosTheta_plots(hist, pdf_path):

    CosThetaM2_hel_dat = hist["CosThetaM2_hel_dat"]
    CosThetaM2_hel_acc_All_Full = hist["CosThetaM2_hel_acc_All_Full"]
    CosThetaM2_hel_acc_0S_BothRefl = hist["CosThetaM2_hel_acc_0S_BothRefl"]
    CosThetaM2_hel_acc_1P_plus1p_BothRefl = hist["CosThetaM2_hel_acc_1P+1p_BothRefl"]
    CosThetaM2_hel_acc_1P_plus0p_BothRefl = hist["CosThetaM2_hel_acc_1P+0p_BothRefl"]
    CosThetaM2_hel_acc_1P_minus1p_BothRefl = hist["CosThetaM2_hel_acc_1P-1p_BothRefl"]
    CosThetaM2_hel_acc_1P_BothRefl = hist["CosThetaM2_hel_acc_1P_BothRefl"]
    CosThetaM2_hel_gen_All_Full = hist["CosThetaM2_hel_gen_All_Full"]
    CosThetaM2_hel_bkg = hist["CosThetaM2_hel_bkg"]

    # -----------------------------
    # CosineTheta of Ks in helicity frame
    # -----------------------------
    c1, pad_plot, pad_info = make_canvas_with_bottompad("c1_cosTheta", info_frac=0.22)
    pad_plot.cd()

    h_data = CosThetaM2_hel_dat.Clone("h_data_cos")
    h_acc_all = CosThetaM2_hel_acc_All_Full.Clone("h_acc_cos")
    h_acc_0S = CosThetaM2_hel_acc_0S_BothRefl.Clone("h_acc_0S_cos")
    h_acc_P_plus1 = CosThetaM2_hel_acc_1P_plus1p_BothRefl.Clone("h_acc_P_plus1_cos")
    h_acc_P_plus0 = CosThetaM2_hel_acc_1P_plus0p_BothRefl.Clone("h_acc_P_plus0_cos")
    h_acc_P_minus1 = CosThetaM2_hel_acc_1P_minus1p_BothRefl.Clone("h_acc_P_minus1_cos")
    h_acc_P = CosThetaM2_hel_acc_1P_BothRefl.Clone("h_acc_P_cos")
    h_gen = CosThetaM2_hel_gen_All_Full.Clone("h_gen_cos")
    h_bkg = CosThetaM2_hel_bkg.Clone("h_bkg_cos")

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.01")
    # h_data.GetYaxis().SetMaxDigits(1)

    # Layer 1 (bottom): accidental sidebands only
    h_bkg.SetLineColor(ROOT.kRed - 3)
    h_bkg.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_bkg.SetFillStyle(1001)

    # Layer 3 (top): accidental + bernstein + signal MC
    h_total = h_bkg.Clone("h_total_cos")
    h_total.Add(h_acc_all)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_acc_0S.SetLineColor(ROOT.kBlack)
    h_acc_P_plus1.SetLineColor(ROOT.kRed + 1)
    h_acc_P_plus0.SetLineColor(ROOT.kOrange + 7)
    h_acc_P_minus1.SetLineColor(ROOT.kMagenta + 1)
    h_acc_P_minus1.SetMarkerSize(2.0)
    h_acc_P_minus1.SetMarkerStyle(10)
    h_acc_P.SetLineColor(ROOT.kBlue + 1)

    for h in (h_acc_0S, h_acc_P_plus1, h_acc_P_plus0, h_acc_P_minus1, h_acc_P):
        h.SetLineWidth(2)
        h.SetMarkerColor(h.GetLineColor())
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.5)

    # Draw largest first so smaller layers appear on top
    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg.Draw("hist same")
    h_acc_0S.Draw("same")
    h_acc_P_plus1.Draw("LP same")
    h_acc_P_plus0.Draw("LP same")
    h_acc_P_minus1.Draw("LP same")
    h_acc_P.Draw("same")


    data_int = integral_between(h_data, -1.0, 1.0)
    acc_int  = integral_between(h_total,  -1.0, 1.0)
    bkg_int  = integral_between(h_bkg, -1.0, 1.0)

    draw_bottom_info_pad(
        pad_info,
        label_text="Not acceptance-corrected",
        legend_items=[
            (h_data,         "data",                   "l"),
            (h_total,        "total fit",             "f"),
            (h_bkg,          "accidental bkg", "f"),
            (h_acc_0S,       "0S wave", "l"),
            (h_acc_P_plus1,  "P+1 wave", "l"),
            (h_acc_P_plus0,  "P0 wave", "l"),
            (h_acc_P_minus1, "P-1 wave", "l"),
            (h_acc_P,        "All P waves", "l"),


        ],
        notes=[
            f"{t_bin}",
            "Fit all Polarizations (0, 45, 90, 135)",
            f"Data int: {data_int:.0f}  acc+bkg: {(acc_int + bkg_int):.0f}",
            "#bf{DATA:} sp18, fa18, sp20. #bf{MC:} sp18, fa18.",
        ],
    )

    open_pdf(c1, pdf_path)        # ← FIRST: opens the PDF with c1

    # --- Efficiency-corrected data ---
    c4, pad_plot, pad_info = make_canvas_with_bottompad("c4_cosTheta_corrected", info_frac=0.22)
    pad_plot.cd()

    # Subtract both background components from data first
    h_data_bkgsub = h_data.Clone("h_data_bkgsub_cos")
    h_data_bkgsub.Add(h_bkg, -1)

    h_corr = make_efficiency_corrected(
        h_data_bkgsub, h_acc_all, h_gen, "cosTheta"
    )

    h_corr.SetTitle("")
    h_corr.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    h_corr.SetYTitle("Candidates / 0.01")
    h_corr.GetYaxis().SetMaxDigits(3)
    h_corr.SetLineColor(ROOT.kBlack)
    h_corr.SetLineWidth(2)
    h_corr.Draw("E")

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency-corrected data",
        legend_items=[
            (h_corr, "data", "l"),
        ],
        notes=[
            f"{t_bin}",
            "(data - bkg) / (accmc / genmc)",
            f"Integral: {h_corr.Integral():.0f}",
            f"Bkg subtracted: {h_bkg.Integral():.0f}",
        ],
    )
    keep(c4)
    add_pdf_page(c4, pdf_path)    # ← SECOND: adds corrected plot as next page

    # -----------------------------
    # CosTheta EFFICIENCY
    # -----------------------------
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_cosTheta_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items = []
    notes = []

    # integrals to display in info pad
    acc_int = integral_between(h_acc_all, -1.0, 0.5)
    gen_int  = integral_between(h_gen, -1.0, 0.5)

    if ROOT.TEfficiency.CheckConsistency(h_acc_all, h_gen):
        eff = ROOT.TEfficiency(h_acc_all, h_gen)
        eff.SetTitle(";cos#theta_{K_{S}} (Helicity frame);Efficiency")
        eff.Draw("AP")
        c2.Update()

        graph = eff.GetPaintedGraph()
        if graph:
            graph.GetXaxis().SetTitle("cos#theta_{K_{S}} (Helicity frame)")
            graph.GetYaxis().SetTitle("Efficiency (accmc / genmc)")
            graph.GetYaxis().SetRangeUser(0.04, 0.06)
            graph.GetYaxis().SetTitleSize(0.055)
            graph.GetYaxis().SetTitleOffset(1.15)
            graph.GetXaxis().SetTitleSize(0.055)
            graph.GetXaxis().SetLabelSize(0.045)
            graph.GetYaxis().SetLabelSize(0.045)

        legend_items = [(graph if graph else h_acc_all, "accmc / genmc", "p")]
        notes = [
            "",
            f"Accepted MC integral: {acc_int:.0f}",
            f"Generated MC integral: {gen_int:.0f}",
            "#theta = (-1, 0.5)",
        ]
    else:
        notes = ["TEfficiency consistency check failed"]

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency",
        legend_items=legend_items,
        notes=notes,
    )

    add_pdf_page(c2, pdf_path)

    

def phi_plots(hist, pdf_path):

    PhiM2_hel_dat = hist["PhiM2_hel_dat"]
    PhiM2_hel_acc_All_Full = hist["PhiM2_hel_acc_All_Full"]
    PhiM2_hel_acc_0S_BothRefl = hist["PhiM2_hel_acc_0S_BothRefl"]
    PhiM2_hel_acc_1P_plus1p_BothRefl = hist["PhiM2_hel_acc_1P+1p_BothRefl"]
    PhiM2_hel_acc_1P_plus0p_BothRefl = hist["PhiM2_hel_acc_1P+0p_BothRefl"]
    PhiM2_hel_acc_1P_minus1p_BothRefl = hist["PhiM2_hel_acc_1P-1p_BothRefl"]
    PhiM2_hel_acc_1P_BothRefl = hist["PhiM2_hel_acc_1P_BothRefl"]
    PhiM2_hel_gen_All_Full = hist["PhiM2_hel_gen_All_Full"]
    PhiM2_hel_bkg = hist["PhiM2_hel_bkg"]

    c1, pad_plot, pad_info = make_canvas_with_bottompad("c1_phi", info_frac=0.22)
    pad_plot.cd()

    h_data         = PhiM2_hel_dat.Clone("h_data_phi")
    h_acc_all      = PhiM2_hel_acc_All_Full.Clone("h_acc_phi")
    h_acc_0S       = PhiM2_hel_acc_0S_BothRefl.Clone("h_acc_0S_phi")
    h_acc_P_plus1  = PhiM2_hel_acc_1P_plus1p_BothRefl.Clone("h_acc_P_plus1_phi")
    h_acc_P_plus0  = PhiM2_hel_acc_1P_plus0p_BothRefl.Clone("h_acc_P_plus0_phi")
    h_acc_P_minus1 = PhiM2_hel_acc_1P_minus1p_BothRefl.Clone("h_acc_P_minus1_phi")
    h_acc_P        = PhiM2_hel_acc_1P_BothRefl.Clone("h_acc_P_phi")
    h_gen          = PhiM2_hel_gen_All_Full.Clone("h_gen_phi")
    h_bkg          = PhiM2_hel_bkg.Clone("h_bkg_phi")

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("#phi_{K_{S}} (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")

    h_bkg.SetLineColor(ROOT.kRed - 3)
    h_bkg.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_bkg.SetFillStyle(1001)

    h_total = h_bkg.Clone("h_total_phi")
    h_total.Add(h_acc_all)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_acc_0S.SetLineColor(ROOT.kBlack)
    h_acc_P_plus1.SetLineColor(ROOT.kRed + 1)
    h_acc_P_plus0.SetLineColor(ROOT.kOrange + 7)
    h_acc_P_minus1.SetLineColor(ROOT.kMagenta + 1)
    h_acc_P.SetLineColor(ROOT.kBlue + 1)

    for h in (h_acc_0S, h_acc_P_plus1, h_acc_P_plus0, h_acc_P_minus1, h_acc_P):
        h.SetLineWidth(2)
        h.SetMarkerColor(h.GetLineColor())
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.5)

    # Draw largest first so smaller layers appear on top
    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg.Draw("hist same")
    h_acc_0S.Draw("LP same")
    h_acc_P_plus1.Draw("LP same")
    h_acc_P_plus0.Draw("LP same")
    h_acc_P_minus1.Draw("LP same")
    h_acc_P.Draw("same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Not acceptance-corrected",
        legend_items=[
            (h_data,         "data",           "l"),
            (h_total,        "total fit",      "f"),
            (h_bkg,          "accidental bkg", "f"),
            (h_acc_0S,       "0S wave",        "l"),
            (h_acc_P_plus1,  "P+1 wave",       "l"),
            (h_acc_P_plus0,  "P0 wave",        "l"),
            (h_acc_P_minus1, "P-1 wave",       "l"),
            (h_acc_P,        "All P waves",    "l"),
        ],
        notes=[
            f"{t_bin}",
            "Fit all Polarizations (0, 45, 90, 135)",
            f"Data int: {h_data.Integral():.0f}  total fit: {h_total.Integral():.0f}",
            "#bf{DATA:} sp18, fa18, sp20. #bf{MC:} sp18, fa18.",
        ],
    )
    keep(c1)
    add_pdf_page(c1, pdf_path)      # cosTheta_plots is the PDF opener

    # --- Efficiency-corrected data ---
    c_corr, pad_plot, pad_info = make_canvas_with_bottompad("c_phi_corrected", info_frac=0.22)
    pad_plot.cd()

    h_data_bkgsub = h_data.Clone("h_phi_data_bkgsub")
    h_data_bkgsub.Add(h_bkg, -1)

    h_corr = make_efficiency_corrected(h_data_bkgsub, h_acc_all, h_gen, "phi")
    h_corr.SetTitle("")
    h_corr.SetXTitle("#phi_{K_{S}} (rad) (Helicity frame)")
    h_corr.SetYTitle("Candidates / 0.035")
    h_corr.GetYaxis().SetMaxDigits(3)
    h_corr.SetLineColor(ROOT.kBlack)
    h_corr.SetLineWidth(2)
    h_corr.Draw("E")

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency-corrected data",
        legend_items=[(h_corr, "data", "l")],
        notes=[
            f"{t_bin}",
            "(data - bkg) / (accmc / genmc)",
            f"Integral: {h_corr.Integral():.0f}",
            f"Bkg subtracted: {h_bkg.Integral():.0f}",
        ],
    )
    keep(c_corr)
    add_pdf_page(c_corr, pdf_path)

    # --- Efficiency ---
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_phi_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items, notes = [], []
    if ROOT.TEfficiency.CheckConsistency(h_acc_all, h_gen):
        eff = ROOT.TEfficiency(h_acc_all, h_gen)
        eff.SetTitle(";#phi_{K_{S}} (Helicity frame);Efficiency")
        eff.Draw("AP")
        c2.Update()
        graph = eff.GetPaintedGraph()
        if graph:
            graph.GetXaxis().SetTitle("#phi_{K_{S}} (Helicity frame)")
            graph.GetYaxis().SetTitle("Efficiency (accmc / genmc)")
            graph.GetYaxis().SetTitleSize(0.055)
            graph.GetYaxis().SetTitleOffset(1.15)
            graph.GetXaxis().SetTitleSize(0.055)
            graph.GetXaxis().SetLabelSize(0.045)
            graph.GetYaxis().SetLabelSize(0.045)
        legend_items = [(graph if graph else h_acc_all, "accmc / genmc", "p")]
        notes = ["", f"Accepted MC integral: {h_acc_all.Integral():.0f}",
                 f"Generated MC integral: {h_gen.Integral():.0f}", "full range"]
    else:
        notes = ["TEfficiency consistency check failed"]

    draw_bottom_info_pad(pad_info, label_text="Efficiency", legend_items=legend_items, notes=notes)
    keep(c2)
    add_pdf_page(c2, pdf_path)



def bigPhi_plots(hist, pdf_path):

    BigPhi_hel_dat = hist["BigPhi_hel_dat"]
    BigPhi_hel_acc_All_Full = hist["BigPhi_hel_acc_All_Full"]
    BigPhi_hel_acc_0S_BothRefl = hist["BigPhi_hel_acc_0S_BothRefl"]
    BigPhi_hel_acc_1P_plus1p_BothRefl = hist["BigPhi_hel_acc_1P+1p_BothRefl"]
    BigPhi_hel_acc_1P_plus0p_BothRefl = hist["BigPhi_hel_acc_1P+0p_BothRefl"]
    BigPhi_hel_acc_1P_minus1p_BothRefl = hist["BigPhi_hel_acc_1P-1p_BothRefl"]
    BigPhi_hel_acc_1P_BothRefl = hist["BigPhi_hel_acc_1P_BothRefl"]
    BigPhi_hel_gen_All_Full = hist["BigPhi_hel_gen_All_Full"]
    BigPhi_hel_bkg = hist["BigPhi_hel_bkg"]

    c1, pad_plot, pad_info = make_canvas_with_bottompad("c1_bigPhi", info_frac=0.22)
    pad_plot.cd()

    h_data         = BigPhi_hel_dat.Clone("h_data_bigPhi")
    h_acc_all      = BigPhi_hel_acc_All_Full.Clone("h_acc_bigPhi")
    h_acc_0S       = BigPhi_hel_acc_0S_BothRefl.Clone("h_acc_0S_bigPhi")
    h_acc_P_plus1  = BigPhi_hel_acc_1P_plus1p_BothRefl.Clone("h_acc_P_plus1_bigPhi")
    h_acc_P_plus0  = BigPhi_hel_acc_1P_plus0p_BothRefl.Clone("h_acc_P_plus0_bigPhi")
    h_acc_P_minus1 = BigPhi_hel_acc_1P_minus1p_BothRefl.Clone("h_acc_P_minus1_bigPhi")
    h_acc_P        = BigPhi_hel_acc_1P_BothRefl.Clone("h_acc_P_bigPhi")
    h_gen          = BigPhi_hel_gen_All_Full.Clone("h_gen_bigPhi")
    h_bkg          = BigPhi_hel_bkg.Clone("h_bkg_bigPhi")

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("#Phi_{K_{S}} (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")

    h_bkg.SetLineColor(ROOT.kRed - 3)
    h_bkg.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_bkg.SetFillStyle(1001)

    h_total = h_bkg.Clone("h_total_bigPhi")
    h_total.Add(h_acc_all)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_acc_0S.SetLineColor(ROOT.kBlack)
    h_acc_P_plus1.SetLineColor(ROOT.kRed + 1)
    h_acc_P_plus0.SetLineColor(ROOT.kOrange + 7)
    h_acc_P_minus1.SetLineColor(ROOT.kMagenta + 1)
    h_acc_P.SetLineColor(ROOT.kBlue + 1)

    for h in (h_acc_0S, h_acc_P_plus1, h_acc_P_plus0, h_acc_P_minus1, h_acc_P):
        h.SetLineWidth(2)
        h.SetMarkerColor(h.GetLineColor())
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.5)

    # Draw largest first so smaller layers appear on top
    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg.Draw("hist same")
    h_acc_0S.Draw("LP same")
    h_acc_P_plus1.Draw("LP same")
    h_acc_P_plus0.Draw("LP same")
    h_acc_P_minus1.Draw("LP same")
    h_acc_P.Draw("same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Not acceptance-corrected",
        legend_items=[
            (h_data,         "data",           "l"),
            (h_total,        "total fit",      "f"),
            (h_bkg,          "accidental bkg", "f"),
            (h_acc_0S,       "0S wave",        "l"),
            (h_acc_P_plus1,  "P+1 wave",       "l"),
            (h_acc_P_plus0,  "P0 wave",        "l"),
            (h_acc_P_minus1, "P-1 wave",       "l"),
            (h_acc_P,        "All P waves",    "l"),
        ],
        notes=[
            f"{t_bin}",
            "Fit all Polarizations (0, 45, 90, 135)",
            f"Data int: {h_data.Integral():.0f}  total fit: {h_total.Integral():.0f}",
            "#bf{DATA:} sp18, fa18, sp20. #bf{MC:} sp18, fa18.",
        ],
    )
    keep(c1)
    add_pdf_page(c1, pdf_path)

    # --- Efficiency-corrected data ---
    c_corr, pad_plot, pad_info = make_canvas_with_bottompad("c_bigPhi_corrected", info_frac=0.22)
    pad_plot.cd()

    h_data_bkgsub = h_data.Clone("h_bigPhi_data_bkgsub")
    h_data_bkgsub.Add(h_bkg, -1)

    h_corr = make_efficiency_corrected(h_data_bkgsub, h_acc_all, h_gen, "bigPhi")
    h_corr.SetTitle("")
    h_corr.SetXTitle("#Phi_{K_{S}} (rad) (Helicity frame)")
    h_corr.SetYTitle("Candidates / 0.035")
    h_corr.GetYaxis().SetMaxDigits(3)
    h_corr.SetLineColor(ROOT.kBlack)
    h_corr.SetLineWidth(2)
    h_corr.Draw("E")

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency-corrected data",
        legend_items=[(h_corr, "data", "l")],
        notes=[
            f"{t_bin}",
            "(data - bkg) / (accmc / genmc)",
            f"Integral: {h_corr.Integral():.0f}",
            f"Bkg subtracted: {h_bkg.Integral():.0f}",
        ],
    )
    keep(c_corr)
    add_pdf_page(c_corr, pdf_path)

    # --- Efficiency ---
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_bigPhi_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items, notes = [], []
    if ROOT.TEfficiency.CheckConsistency(h_acc_all, h_gen):
        eff = ROOT.TEfficiency(h_acc_all, h_gen)
        eff.SetTitle(";#Phi_{K_{S}} (Helicity frame);Efficiency")
        eff.Draw("AP")
        c2.Update()
        graph = eff.GetPaintedGraph()
        if graph:
            graph.GetXaxis().SetTitle("#Phi_{K_{S}} (Helicity frame)")
            graph.GetYaxis().SetTitle("Efficiency (accmc / genmc)")
            graph.GetYaxis().SetTitleSize(0.055)
            graph.GetYaxis().SetTitleOffset(1.15)
            graph.GetXaxis().SetTitleSize(0.055)
            graph.GetXaxis().SetLabelSize(0.045)
            graph.GetYaxis().SetLabelSize(0.045)
        legend_items = [(graph if graph else h_acc_all, "accmc / genmc", "p")]
        notes = ["", f"Accepted MC integral: {h_acc_all.Integral():.0f}",
                 f"Generated MC integral: {h_gen.Integral():.0f}", "full range"]
    else:
        notes = ["TEfficiency consistency check failed"]

    draw_bottom_info_pad(pad_info, label_text="Efficiency", legend_items=legend_items, notes=notes)
    keep(c2)
    add_pdf_page(c2, pdf_path)


def phi_minus_bigPhi_plots(hist, pdf_path):

    psi_dat = hist["PhiMinusBigPhiM2_hel_dat"]
    psi_acc_All_Full = hist["PhiMinusBigPhiM2_hel_acc_All_Full"]
    psi_acc_0S_BothRefl = hist["PhiMinusBigPhiM2_hel_acc_0S_BothRefl"]
    psi_acc_1P_plus1p_BothRefl = hist["PhiMinusBigPhiM2_hel_acc_1P+1p_BothRefl"]
    psi_acc_1P_plus0p_BothRefl = hist["PhiMinusBigPhiM2_hel_acc_1P+0p_BothRefl"]
    psi_acc_1P_minus1p_BothRefl = hist["PhiMinusBigPhiM2_hel_acc_1P-1p_BothRefl"]
    psi_acc_1P_BothRefl = hist["PhiMinusBigPhiM2_hel_acc_1P_BothRefl"]
    psi_gen_All_Full = hist["PhiMinusBigPhiM2_hel_gen_All_Full"]
    psi_bkg = hist["PhiMinusBigPhiM2_hel_bkg"]

    c1, pad_plot, pad_info = make_canvas_with_bottompad("c1_psi", info_frac=0.22)
    pad_plot.cd()

    h_data         = psi_dat.Clone("h_data_psi")
    h_acc_all      = psi_acc_All_Full.Clone("h_acc_psi")
    h_acc_0S       = psi_acc_0S_BothRefl.Clone("h_acc_0S_psi")
    h_acc_P_plus1  = psi_acc_1P_plus1p_BothRefl.Clone("h_acc_P_plus1_psi")
    h_acc_P_plus0  = psi_acc_1P_plus0p_BothRefl.Clone("h_acc_P_plus0_psi")
    h_acc_P_minus1 = psi_acc_1P_minus1p_BothRefl.Clone("h_acc_P_minus1_psi")
    h_acc_P        = psi_acc_1P_BothRefl.Clone("h_acc_P_psi")
    h_gen          = psi_gen_All_Full.Clone("h_gen_psi")
    h_bkg          = psi_bkg.Clone("h_bkg_psi")

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("(#phi - #Phi)_{K_{S}} (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")

    h_bkg.SetLineColor(ROOT.kRed - 3)
    h_bkg.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_bkg.SetFillStyle(1001)

    h_total = h_bkg.Clone("h_total_psi")
    h_total.Add(h_acc_all)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_acc_0S.SetLineColor(ROOT.kBlack)
    h_acc_P_plus1.SetLineColor(ROOT.kRed + 1)
    h_acc_P_plus0.SetLineColor(ROOT.kOrange + 7)
    h_acc_P_minus1.SetLineColor(ROOT.kMagenta + 1)
    h_acc_P.SetLineColor(ROOT.kBlue + 1)

    for h in (h_acc_0S, h_acc_P_plus1, h_acc_P_plus0, h_acc_P_minus1, h_acc_P):
        h.SetLineWidth(2)
        h.SetMarkerColor(h.GetLineColor())
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.5)

    # Draw largest first so smaller layers appear on top
    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg.Draw("hist same")
    h_acc_0S.Draw("LP same")
    h_acc_P_plus1.Draw("LP same")
    h_acc_P_plus0.Draw("LP same")
    h_acc_P_minus1.Draw("LP same")
    h_acc_P.Draw("same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Not acceptance-corrected",
        legend_items=[
            (h_data,         "data",           "l"),
            (h_total,        "total fit",      "f"),
            (h_bkg,          "accidental bkg", "f"),
            (h_acc_0S,       "0S wave",        "l"),
            (h_acc_P_plus1,  "P+1 wave",       "l"),
            (h_acc_P_plus0,  "P0 wave",        "l"),
            (h_acc_P_minus1, "P-1 wave",       "l"),
            (h_acc_P,        "All P waves",    "l"),
        ],
        notes=[
            f"{t_bin}",
            "Fit all Polarizations (0, 45, 90, 135)",
            f"Data int: {h_data.Integral():.0f}  total fit: {h_total.Integral():.0f}",
            "#bf{DATA:} sp18, fa18, sp20. #bf{MC:} sp18, fa18.",
        ],
    )
    keep(c1)
    add_pdf_page(c1, pdf_path)

    # --- Efficiency-corrected data ---
    c_corr, pad_plot, pad_info = make_canvas_with_bottompad("c_psi_corrected", info_frac=0.22)
    pad_plot.cd()

    h_data_bkgsub = h_data.Clone("h_psi_data_bkgsub")
    h_data_bkgsub.Add(h_bkg, -1)

    h_corr = make_efficiency_corrected(h_data_bkgsub, h_acc_all, h_gen, "psi")
    h_corr.SetTitle("")
    h_corr.SetXTitle("(#phi - #Phi)_{K_{S}} (rad) (Helicity frame)")
    h_corr.SetYTitle("Candidates / 0.035")
    h_corr.GetYaxis().SetMaxDigits(3)
    h_corr.SetLineColor(ROOT.kBlack)
    h_corr.SetLineWidth(2)
    h_corr.Draw("E")

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency-corrected data",
        legend_items=[(h_corr, "data", "l")],
        notes=[
            f"{t_bin}",
            "(data - bkg) / (accmc / genmc)",
            f"Integral: {h_corr.Integral():.0f}",
            f"Bkg subtracted: {h_bkg.Integral():.0f}",
        ],
    )
    keep(c_corr)
    add_pdf_page(c_corr, pdf_path)

    # --- Efficiency ---
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_psi_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items, notes = [], []
    if ROOT.TEfficiency.CheckConsistency(h_acc_all, h_gen):
        eff = ROOT.TEfficiency(h_acc_all, h_gen)
        eff.SetTitle(";(#phi - #Phi)_{K_{S}} (Helicity frame);Efficiency")
        eff.Draw("AP")
        c2.Update()
        graph = eff.GetPaintedGraph()
        if graph:
            graph.GetXaxis().SetTitle("(#phi - #Phi)_{K_{S}} (Helicity frame)")
            graph.GetYaxis().SetTitle("Efficiency (accmc / genmc)")
            graph.GetYaxis().SetTitleSize(0.055)
            graph.GetYaxis().SetTitleOffset(1.15)
            graph.GetXaxis().SetTitleSize(0.055)
            graph.GetXaxis().SetLabelSize(0.045)
            graph.GetYaxis().SetLabelSize(0.045)
        legend_items = [(graph if graph else h_acc_all, "accmc / genmc", "p")]
        notes = ["", f"Accepted MC integral: {h_acc_all.Integral():.0f}",
                 f"Generated MC integral: {h_gen.Integral():.0f}", "full range"]
    else:
        notes = ["TEfficiency consistency check failed"]

    draw_bottom_info_pad(pad_info, label_text="Efficiency", legend_items=legend_items, notes=notes)
    keep(c2)
    add_pdf_page(c2, pdf_path)



def MKpi_plots(hist, pdf_path):

    hMass23_dat = hist["hMass23_dat"]
    hMass23_acc_All_Full = hist["hMass23_acc_All_Full"]
    hMass23_acc_0S_BothRefl = hist["hMass23_acc_0S_BothRefl"]
    hMass23_acc_1P_plus1p_BothRefl = hist["hMass23_acc_1P+1p_BothRefl"]
    hMass23_acc_1P_plus0p_BothRefl = hist["hMass23_acc_1P+0p_BothRefl"]
    hMass23_acc_1P_minus1p_BothRefl = hist["hMass23_acc_1P-1p_BothRefl"]
    hMass23_acc_1P_BothRefl = hist["hMass23_acc_1P_BothRefl"]
    hMass23_bkg = hist["hMass23_bkg"]

    c, pad_plot, pad_info = make_canvas_with_bottompad("c_MKpi", info_frac=0.22)
    pad_plot.cd()

    h_data         = hMass23_dat.Clone("h_MKpi_data")
    h_acc_all      = hMass23_acc_All_Full.Clone("h_MKpi_acc")
    h_acc_0S       = hMass23_acc_0S_BothRefl.Clone("h_acc_0S_MKpi")
    h_acc_P_plus1  = hMass23_acc_1P_plus1p_BothRefl.Clone("h_acc_P_plus1_MKpi")
    h_acc_P_plus0  = hMass23_acc_1P_plus0p_BothRefl.Clone("h_acc_P_plus0_MKpi")
    h_acc_P_minus1 = hMass23_acc_1P_minus1p_BothRefl.Clone("h_acc_P_minus1_MKpi")
    h_acc_P        = hMass23_acc_1P_BothRefl.Clone("h_acc_P_MKpi")
    h_bkg          = hMass23_bkg.Clone("h_bkg_MKpi")

    h_bkg.SetLineColor(ROOT.kRed - 3)
    h_bkg.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_bkg.SetFillStyle(1001)

    h_total = h_bkg.Clone("h_MKpi_total")
    h_total.Add(h_acc_all)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    for h in (h_acc_0S, h_acc_P_plus1, h_acc_P_plus0, h_acc_P_minus1, h_acc_P):
        h.SetLineColor(ROOT.kBlue)

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)

    h_total.SetTitle("")
    h_total.SetXTitle("M(K_{S} #pi^{+}) [GeV/c^{2}]")
    h_total.SetYTitle("Candidates / 40 MeV")
    h_total.SetMinimum(0)

    h_acc_0S.SetLineColor(ROOT.kBlack)
    h_acc_P_plus1.SetLineColor(ROOT.kRed + 1)
    h_acc_P_plus0.SetLineColor(ROOT.kOrange + 7)
    h_acc_P_minus1.SetLineColor(ROOT.kMagenta + 1)
    h_acc_P.SetLineColor(ROOT.kBlue + 1)

    for h in (h_acc_0S, h_acc_P_plus1, h_acc_P_plus0, h_acc_P_minus1, h_acc_P):
        h.SetLineWidth(2)
        h.SetMarkerColor(h.GetLineColor())
        h.SetMarkerStyle(20)
        h.SetMarkerSize(0.5)

    # Draw largest first so smaller layers appear on top
    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg.Draw("hist same")
    h_acc_0S.Draw("LP same")
    h_acc_P_plus1.Draw("LP same")
    h_acc_P_plus0.Draw("LP same")
    h_acc_P_minus1.Draw("LP same")
    h_acc_P.Draw("same")

    draw_bottom_info_pad(
        pad_info,
        label_text="M(K_{S} #pi^{+}) PWA fit",
        legend_items=[
            (h_data,         "data",        "l"),
            (h_total,        "bkg + accmc", "f"),
            (h_bkg,          "background",  "f"),
            (h_acc_0S,       "0S wave",     "l"),
            (h_acc_P_plus1,  "P+1 wave",    "l"),
            (h_acc_P_plus0,  "P0 wave",     "l"),
            (h_acc_P_minus1, "P-1 wave",    "l"),
            (h_acc_P,        "All P waves", "l"),
        ],
        notes=[
            f"{t_bin}",
            f"Total int: {h_total.Integral():.0f}",
            f"accmc int: {h_acc_all.Integral():.0f}",
            f"bkg int: {h_bkg.Integral():.0f}",
        ],
    )
    keep(c)
    close_pdf(c, pdf_path)


# -----------------------------
# Main
# -----------------------------
def main():
    start_time = time.time()

    ensure_plot_dir(allPlots)
    gluex_style()
    setup()
    hist = load_histograms(FND)

    cosTheta_plots(hist, allPlots)
    phi_plots(hist, allPlots)
    bigPhi_plots(hist, allPlots)
    phi_minus_bigPhi_plots(hist, allPlots)
    MKpi_plots(hist, allPlots) 

    end_time = time.time()
    print(f"Time to run: {end_time - start_time:.1f} seconds")


if __name__ == "__main__":
    main()
