import os
import time
import ROOT

ROOT.gROOT.SetBatch(True)

from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# -----------------------------
# Files / globals
# -----------------------------
t_bin = "#bf{-t = (0.3 - 0.8) GeV^{2}}" # t_bin label for plots.  MUST match the t_bin used to create the ROOT file.
# FND = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/outputTrees/032926_t110_fit1/KsPipLamb_ALL.root"
# FND = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/outputTrees/042826_t110_fit1/KsPipLamb_ALL.root"
# FND = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/outputTrees/20260529_t38_fit0_v3/KsPipLamb_ALL.root"
FND = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/outputTrees/20260601_t38_fit0_v0/KsPipLamb_ALL.root"
allPlots = "plots/sdme_plots.pdf"

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

# DON'T USE THIS.  ADD THE HISTOGRAMS IN EACH INDIVIDUAL PLOT.
# used in 'load_histograms' (below)
# def _sum_hists(root_file, name1, name2):
#     h1 = get_hist_or_raise(root_file, name1)
#     h2 = get_hist_or_raise(root_file, name2)
#     h1.Add(h2)
#     return h1

def load_histograms(filename):
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        raise RuntimeError(f"Could not open ROOT file: {filename}")

    hist = {
        "cosThetadat":      get_hist_or_raise(f, "cosThetadat"),
        "cosThetaacc_sdme": get_hist_or_raise(f, "cosThetaacc_sdme"),
        "cosThetagen_sdme": get_hist_or_raise(f, "cosThetagen_sdme"),
        "cosThetabkg_sdme": get_hist_or_raise(f, "cosThetabkg_sdme"),
        "cosThetaacc_bernBkg": get_hist_or_raise(f, "cosThetaacc_bernBkg"),

        "phidat":      get_hist_or_raise(f, "phidat"),
        "phiacc_sdme": get_hist_or_raise(f, "phiacc_sdme"),
        "phigen_sdme": get_hist_or_raise(f, "phigen_sdme"),
        "phibkg_sdme": get_hist_or_raise(f, "phibkg_sdme"),
        "phiacc_bernBkg": get_hist_or_raise(f, "phiacc_bernBkg"),

        "Phidat":      get_hist_or_raise(f, "Phidat"),
        "Phiacc_sdme": get_hist_or_raise(f, "Phiacc_sdme"),
        "Phigen_sdme": get_hist_or_raise(f, "Phigen_sdme"),
        "Phibkg_sdme": get_hist_or_raise(f, "Phibkg_sdme"),
        "Phiacc_bernBkg": get_hist_or_raise(f, "Phiacc_bernBkg"),

        "psidat":      get_hist_or_raise(f, "psidat"),
        "psiacc_sdme": get_hist_or_raise(f, "psiacc_sdme"),
        "psigen_sdme": get_hist_or_raise(f, "psigen_sdme"),
        "psibkg_sdme": get_hist_or_raise(f, "psibkg_sdme"),
        "psiacc_bernBkg": get_hist_or_raise(f, "psiacc_bernBkg"),
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
        leg.SetTextSize(0.16)
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
    cosThetadat         = hist["cosThetadat"]
    cosThetaacc_sdme    = hist["cosThetaacc_sdme"]
    cosThetabkg_sdme    = hist["cosThetabkg_sdme"]
    cosThetagen_sdme    = hist["cosThetagen_sdme"]
    cosThetaacc_bernBkg = hist["cosThetaacc_bernBkg"]

    # -----------------------------
    # CosineTheta of Ks in helicity frame
    # -----------------------------
    c1, pad_plot, pad_info = make_canvas_with_bottompad("c1_cosTheta", info_frac=0.22)
    pad_plot.cd()

    h_data       = cosThetadat.Clone("h_data_cos")
    h_acc        = cosThetaacc_sdme.Clone("h_acc_cos")
    h_accidental = cosThetabkg_sdme.Clone("h_accidental_cos")
    h_bern       = cosThetaacc_bernBkg.Clone("h_bern_cos")

    # Layer 1 (bottom): accidental sidebands only
    h_accidental.SetLineColor(ROOT.kRed - 3)
    h_accidental.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_accidental.SetFillStyle(1001)

    # Layer 2 (middle): accidental + bernstein
    h_bkg_total = h_accidental.Clone("h_bkg_total_cos")
    h_bkg_total.Add(h_bern)
    h_bkg_total.SetLineColor(ROOT.kBlue - 3)
    h_bkg_total.SetFillColorAlpha(ROOT.kBlue, 0.30)
    h_bkg_total.SetFillStyle(1001)

    # Layer 3 (top): accidental + bernstein + signal MC
    h_total = h_bkg_total.Clone("h_total_cos")
    h_total.Add(h_acc)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.01")
    # h_data.GetYaxis().SetMaxDigits(1)

    # Draw largest first so smaller layers appear on top
    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg_total.Draw("hist same")
    h_accidental.Draw("hist same")

    data_int = integral_between(h_data, -1.0, 1.0)
    acc_int  = integral_between(h_acc,  -1.0, 1.0)
    bkg_int  = integral_between(h_bkg_total, -1.0, 1.0)

    draw_bottom_info_pad(
        pad_info,
        label_text="Not acceptance-corrected",
        legend_items=[
            (h_data,       "data",                   "l"),
            (h_total,      "accmc + bkg",             "f"),
            (h_bkg_total,  "accidental + poly",  "f"),
            (h_accidental, "accidental only",     "f"),
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
    h_data_bkgsub.Add(h_accidental, -1)
    h_data_bkgsub.Add(h_bern, -1)

    h_corr = make_efficiency_corrected(
        h_data_bkgsub, cosThetaacc_sdme, cosThetagen_sdme, "cosTheta"
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
            f"Bkg subtracted: {integral_between(h_bkg_total,-1.,1.):.0f}",
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
    acc_int = integral_between(cosThetaacc_sdme, -1.0, 0.5)
    gen_int  = integral_between(cosThetagen_sdme, -1.0, 0.5)

    if ROOT.TEfficiency.CheckConsistency(cosThetaacc_sdme, cosThetagen_sdme):
        eff = ROOT.TEfficiency(cosThetaacc_sdme, cosThetagen_sdme)
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

        legend_items = [(graph if graph else cosThetaacc_sdme, "accmc / genmc", "p")]
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

    # -----------------------------
    # DIAGNOSTIC PLOT: accmc / efficiency = genmc
    # -----------------------------
    # c3, pad_plot, pad_info = make_canvas_with_bottompad("c3_cosTheta_diag", info_frac=0.22)
    # pad_plot.cd()

    # h_eff = cosThetaacc_sdme.Clone("h_eff_cos")
    # h_eff.Divide(cosThetagen_sdme)

    # h_diag = cosThetaacc_sdme.Clone("h_diag_cos")
    # h_diag.Divide(h_eff)
    # h_diag.SetTitle("")
    # h_diag.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    # h_diag.SetYTitle("Count")
    # h_diag.SetLineColor(ROOT.kBlue + 1)
    # h_diag.SetLineWidth(2)
    # h_diag.GetXaxis().SetNdivisions(4, 0, 0, True)
    # h_diag.GetYaxis().SetRangeUser(1100, 2000)
    # h_diag.GetYaxis().SetTitleOffset(1.21)
    # h_diag.GetYaxis().SetMaxDigits(3)
    # h_diag.Draw()

    # h_gen = cosThetagen_sdme.Clone("h_gen_cos")
    # h_gen.SetTitle("")
    # h_gen.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    # # h_gen.SetYTitle("Generated MC")
    # h_gen.SetLineColor(ROOT.kGreen - 6)
    # h_gen.SetFillColorAlpha(ROOT.kGreen - 2, 0.60)
    # h_gen.SetFillStyle(1001)
    # h_gen.SetLineWidth(2)
    # h_gen.GetYaxis().SetRangeUser(1100, 2000)
    # h_gen.GetYaxis().SetTitleOffset(1.21)
    # h_gen.GetYaxis().SetMaxDigits(3)
    # h_gen.Draw("hist same")

    # draw_bottom_info_pad(
    #     pad_info,
    #     label_text="Diagnostic plot (fitted trees)",
    #     legend_items=[
    #         (h_diag, "accmc / efficiency", "l"),
    #         (h_gen, "genmc", "f"),
    #     ],
    #     notes=[
    #         "",
    #         f"Integral acc / eff: {integral_between(h_diag, -1.0, 0.5):.0f}",
    #         f"Integral genmc: {integral_between(h_gen, -1.0, 0.5):.0f}",
    #         "#theta = (-1, 0.5)",
    #     ],
    # )

    # add_pdf_page(c3, pdf_path)

def phi_plots(hist, pdf_path):
    phidat          = hist["phidat"]
    phiacc_sdme     = hist["phiacc_sdme"]
    phibkg_sdme     = hist["phibkg_sdme"]
    phigen_sdme     = hist["phigen_sdme"]
    phiacc_bernBkg  = hist["phiacc_bernBkg"]

    c1, pad_plot, pad_info = make_canvas_with_bottompad("c_phi", info_frac=0.22)
    pad_plot.cd()

    h_data       = phidat.Clone("h_phi_data")
    h_acc        = phiacc_sdme.Clone("h_phi_acc")
    h_accidental = phibkg_sdme.Clone("h_phi_accidental")
    h_bern       = phiacc_bernBkg.Clone("h_phi_bern")

    # Layer 1 (bottom): accidental sidebands only
    h_accidental.SetLineColor(ROOT.kRed - 3)
    h_accidental.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_accidental.SetFillStyle(1001)

    # Layer 2 (middle): accidental + bernstein
    h_bkg_total = h_accidental.Clone("h_phi_bkg_total")
    h_bkg_total.Add(h_bern)
    h_bkg_total.SetLineColor(ROOT.kBlue - 3)
    h_bkg_total.SetFillColorAlpha(ROOT.kBlue, 0.30)
    h_bkg_total.SetFillStyle(1001)

    # Layer 3 (top): accidental + bernstein + signal MC
    h_total = h_bkg_total.Clone("h_phi_total")
    h_total.Add(h_acc)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("#phi_{K_{s}} (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")
    # h_data.GetYaxis().SetMaxDigits(1)

    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg_total.Draw("hist same")
    h_accidental.Draw("hist same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Azimuthal angle of Ks",
        legend_items=[
            (h_data,       "data",                  "l"),
            (h_total,      "accmc + bkg",            "f"),
            (h_bkg_total,  "accidental + bernstein", "f"),
            (h_accidental, "accidental sideband",    "f"),
        ],
        notes=[
            f"{t_bin}",
            f"Data int: {h_data.Integral():.0f}",
            f"Acc int: {h_acc.Integral():.0f}",
            f"Bkg int: {h_bkg_total.Integral():.0f}",
        ],
    )

    open_pdf(c1, pdf_path)

    # -----------------------------
    # Efficiency-corrected phi (background subtracted)
    # -----------------------------
    c_phi_corr, pad_plot, pad_info = make_canvas_with_bottompad("c_phi_corrected", info_frac=0.22)
    pad_plot.cd()

    h_data_bkgsub = h_data.Clone("h_phi_data_bkgsub")
    h_data_bkgsub.Add(h_accidental, -1)
    h_data_bkgsub.Add(h_bern, -1)

    h_corr = make_efficiency_corrected(h_data_bkgsub, phiacc_sdme, phigen_sdme, "phi")

    h_corr.SetTitle("")
    h_corr.SetXTitle("#phi_{K_{s}} (rad) (Helicity frame)")
    h_corr.SetYTitle("Candidates / 0.035")
    h_corr.GetYaxis().SetMaxDigits(3)
    h_corr.SetLineColor(ROOT.kBlack)
    h_corr.SetLineWidth(2)
    h_corr.Draw("E")

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency-corrected",
        legend_items=[
            (h_corr, "data", "l"),
        ],
        notes=[
            f"{t_bin}",
            "(data - bkg) / (accmc / genmc)",
            f"Integral: {h_corr.Integral():.0f}",
            f"Bkg subtracted: {h_bkg_total.Integral():.0f}",
        ],
    )
    keep(c_phi_corr)
    add_pdf_page(c_phi_corr, pdf_path)

    # -----------------------------
    # Azimuthal EFFICIENCY
    # -----------------------------
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_phi_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items = []
    notes = []

    acc_int = integral_between(phiacc_sdme, -1.0, 0.5)
    gen_int = integral_between(phigen_sdme, -1.0, 0.5)

    if ROOT.TEfficiency.CheckConsistency(phiacc_sdme, phigen_sdme):
        eff = ROOT.TEfficiency(phiacc_sdme, phigen_sdme)
        eff.SetTitle(";#phi_{K_{S}} (Helicity frame);Efficiency")
        eff.Draw("AP")
        c2.Update()

        graph = eff.GetPaintedGraph()
        if graph:
            graph.GetXaxis().SetTitle("#phi_{K_{S}} (Helicity frame)")
            graph.GetYaxis().SetTitle("Efficiency (accmc / genmc)")
            # graph.GetYaxis().SetRangeUser(0.1, 0.9)
            graph.GetYaxis().SetTitleSize(0.055)
            graph.GetYaxis().SetTitleOffset(1.15)
            graph.GetXaxis().SetTitleSize(0.055)
            graph.GetXaxis().SetLabelSize(0.045)
            graph.GetYaxis().SetLabelSize(0.045)

        legend_items = [(graph if graph else phiacc_sdme, "accmc / genmc", "p")]
        notes = [
            "",
            f"Accepted MC integral: {acc_int:.0f}",
            f"Generated MC integral: {gen_int:.0f}",
            "#phi = (-1, 0.5)",
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

    # # -----------------------------
    # # Efficiency-corrected phi overlay
    # # -----------------------------
    # c_phi_corr, pad_plot, pad_info = make_canvas_with_bottompad("c_phi_corrected", info_frac=0.22)
    # pad_plot.cd()

    # # Efficiency-correct each bin
    # h_corr_data = make_efficiency_corrected(phidat,      phiacc_sdme, phigen_sdme, "phi_data")
    # h_corr_acc  = make_efficiency_corrected(phiacc_sdme, phiacc_sdme, phigen_sdme, "phi_acc")
    # h_corr_bkg  = make_efficiency_corrected(phibkg_sdme, phiacc_sdme, phigen_sdme, "phi_bkg")
    # h_corr_sum  = h_corr_acc.Clone("h_phi_corr_sum")
    # h_corr_sum.Add(h_corr_bkg)

    # h_corr_data.SetTitle("")
    # h_corr_data.SetXTitle("#phi (rad) (Helicity frame)")
    # h_corr_data.SetYTitle("Candidates / 0.035")
    # h_corr_data.GetYaxis().SetMaxDigits(1)

    # style_data_mc_overlay(h_corr_data, h_corr_sum, h_corr_bkg)

    # h_corr_data.Draw("E")
    # # h_corr_sum.Draw("hist same")
    # # h_corr_bkg.Draw("hist same")

    # draw_bottom_info_pad(
    #     pad_info,
    #     label_text="Efficiency-corrected azimuthal angle",
    #     legend_items=[
    #         (h_corr_data, "data", "l"),
    #         (h_corr_sum,  "accmc + bkg", "f"),
    #         (h_corr_bkg,  "bkgnd", "f"),
    #     ],
    #     notes=[
    #         f"{t_bin}",
    #         "Each bin divided by (accmc / genmc)",
    #         f"Data int: {h_corr_data.Integral():.0f}",
    #         f"Acc int: {h_corr_acc.Integral():.0f}  Bkg int: {h_corr_bkg.Integral():.0f}",
    #     ],
    # )
    # keep(c_phi_corr)
    # add_pdf_page(c_phi_corr, pdf_path)

def bigPhi_plots(hist, pdf_path):
    Phidat          = hist["Phidat"]
    Phiacc_sdme     = hist["Phiacc_sdme"]
    Phibkg_sdme     = hist["Phibkg_sdme"]
    Phigen_sdme     = hist["Phigen_sdme"]
    Phiacc_bernBkg  = hist["Phiacc_bernBkg"]

    c1, pad_plot, pad_info = make_canvas_with_bottompad("c_bigPhi", info_frac=0.22)
    pad_plot.cd()

    h_data       = Phidat.Clone("h_bigPhi_data")
    h_acc        = Phiacc_sdme.Clone("h_bigPhi_acc")
    h_accidental = Phibkg_sdme.Clone("h_bigPhi_accidental")
    h_bern       = Phiacc_bernBkg.Clone("h_bigPhi_bern")

    h_accidental.SetLineColor(ROOT.kRed - 3)
    h_accidental.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_accidental.SetFillStyle(1001)

    h_bkg_total = h_accidental.Clone("h_bigPhi_bkg_total")
    h_bkg_total.Add(h_bern)
    h_bkg_total.SetLineColor(ROOT.kBlue - 3)
    h_bkg_total.SetFillColorAlpha(ROOT.kBlue, 0.30)
    h_bkg_total.SetFillStyle(1001)

    h_total = h_bkg_total.Clone("h_bigPhi_total")
    h_total.Add(h_acc)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("#Phi_{K_{s}} (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")
    # h_data.GetYaxis().SetMaxDigits(1)

    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg_total.Draw("hist same")
    h_accidental.Draw("hist same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Polarization angle of Ks",
        legend_items=[
            (h_data,       "data",                  "l"),
            (h_total,      "accmc + bkg",            "f"),
            (h_bkg_total,  "accidental + bernstein", "f"),
            (h_accidental, "accidental sideband",    "f"),
        ],
        notes=[
            f"{t_bin}",
            f"Data int: {h_data.Integral():.0f}",
            f"Acc int: {h_acc.Integral():.0f}",
            f"Bkg int: {h_bkg_total.Integral():.0f}",
        ],
    )

    open_pdf(c1, pdf_path)

    # -----------------------------
    # Efficiency-corrected Phi (background subtracted)
    # -----------------------------
    c_Phi_corr, pad_plot, pad_info = make_canvas_with_bottompad("c_bigPhi_corrected", info_frac=0.22)
    pad_plot.cd()

    h_data_bkgsub = h_data.Clone("h_bigPhi_data_bkgsub")
    h_data_bkgsub.Add(h_accidental, -1)
    h_data_bkgsub.Add(h_bern, -1)

    h_corr = make_efficiency_corrected(h_data_bkgsub, Phiacc_sdme, Phigen_sdme, "Phi")

    h_corr.SetTitle("")
    h_corr.SetXTitle("#Phi_{K_{s}} (rad) (Helicity frame)")
    h_corr.SetYTitle("Candidates / 0.035")
    h_corr.GetYaxis().SetMaxDigits(3)
    h_corr.SetLineColor(ROOT.kBlack)
    h_corr.SetLineWidth(2)
    h_corr.Draw("E")

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency-corrected",
        legend_items=[
            (h_corr, "data", "l"),
        ],
        notes=[
            f"{t_bin}",
            "(data - bkg) / (accmc / genmc)",
            f"Integral: {h_corr.Integral():.0f}",
            f"Bkg subtracted: {h_bkg_total.Integral():.0f}",
        ],
    )
    keep(c_Phi_corr)
    add_pdf_page(c_Phi_corr, pdf_path)

    # -----------------------------
    # Polarization angle EFFICIENCY
    # -----------------------------
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_bigPhi_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items = []
    notes = []

    acc_int = integral_between(Phiacc_sdme, -3.0, 3.0)
    gen_int = integral_between(Phigen_sdme, -3.0, 3.0)

    if ROOT.TEfficiency.CheckConsistency(Phiacc_sdme, Phigen_sdme):
        eff = ROOT.TEfficiency(Phiacc_sdme, Phigen_sdme)
        eff.SetTitle(";#Phi_{K_{S}} (Helicity frame);Efficiency")
        eff.Draw("AP")
        c2.Update()

        graph = eff.GetPaintedGraph()
        if graph:
            graph.GetXaxis().SetTitle("#Phi_{K_{S}} (Helicity frame)")
            graph.GetYaxis().SetTitle("Efficiency (accmc / genmc)")
            graph.GetYaxis().SetRangeUser(0.0, 0.1)
            graph.GetYaxis().SetTitleSize(0.055)
            graph.GetYaxis().SetTitleOffset(1.15)
            graph.GetXaxis().SetTitleSize(0.055)
            graph.GetXaxis().SetLabelSize(0.045)
            graph.GetYaxis().SetLabelSize(0.045)

        legend_items = [(graph if graph else Phiacc_sdme, "accmc / genmc", "p")]
        notes = [
            "Polarization angle.",
            f"Accepted MC integral: {acc_int:.0f}",
            f"Generated MC integral: {gen_int:.0f}",
            "#Phi = (-3, 3)",
        ]
    else:
        notes = ["TEfficiency consistency check failed"]

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency (fitted trees)",
        legend_items=legend_items,
        notes=notes,
    )

    add_pdf_page(c2, pdf_path)

def phi_minus_bigPhi_plots(hist, pdf_path):
    psidat          = hist["psidat"]
    psiacc_sdme     = hist["psiacc_sdme"]
    psibkg_sdme     = hist["psibkg_sdme"]
    psigen_sdme     = hist["psigen_sdme"]
    psiacc_bernBkg  = hist["psiacc_bernBkg"]

    c, pad_plot, pad_info = make_canvas_with_bottompad("c_psi", info_frac=0.22)
    pad_plot.cd()

    h_data       = psidat.Clone("h_psi_data")
    h_acc        = psiacc_sdme.Clone("h_psi_acc")
    h_accidental = psibkg_sdme.Clone("h_psi_accidental")
    h_bern       = psiacc_bernBkg.Clone("h_psi_bern")

    h_accidental.SetLineColor(ROOT.kRed - 3)
    h_accidental.SetFillColorAlpha(ROOT.kRed - 4, 0.60)
    h_accidental.SetFillStyle(1001)

    h_bkg_total = h_accidental.Clone("h_psi_bkg_total")
    h_bkg_total.Add(h_bern)
    h_bkg_total.SetLineColor(ROOT.kBlue - 3)
    h_bkg_total.SetFillColorAlpha(ROOT.kBlue, 0.30)
    h_bkg_total.SetFillStyle(1001)

    h_total = h_bkg_total.Clone("h_psi_total")
    h_total.Add(h_acc)
    h_total.SetLineColor(ROOT.kGreen - 6)
    h_total.SetFillColorAlpha(ROOT.kGreen - 2, 0.50)
    h_total.SetFillStyle(1001)

    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetLineWidth(2)
    h_data.SetMinimum(0)
    h_data.SetTitle("")
    h_data.SetXTitle("(#phi - #Phi)_{Ks} (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")
    # h_data.GetYaxis().SetMaxDigits(1)

    h_data.Draw()
    h_total.Draw("hist same")
    h_bkg_total.Draw("hist same")
    h_accidental.Draw("hist same")

    draw_bottom_info_pad(
        pad_info,
        label_text="azimuthal - pol. angle",
        legend_items=[
            (h_data,       "data",                  "l"),
            (h_total,      "accmc + bkg",            "f"),
            (h_bkg_total,  "accidental + bernstein", "f"),
            (h_accidental, "accidental sideband",    "f"),
        ],
        notes=[
            f"{t_bin}",
            f"Data int: {h_data.Integral():.0f}",
            f"Acc int: {h_acc.Integral():.0f}",
            f"Bkg int: {h_bkg_total.Integral():.0f}",
        ],
    )

    open_pdf(c, pdf_path)

    # -----------------------------
    # Efficiency-corrected psi (background subtracted)
    # -----------------------------
    c_psi_corr, pad_plot, pad_info = make_canvas_with_bottompad("c_psi_corrected", info_frac=0.22)
    pad_plot.cd()

    h_data_bkgsub = h_data.Clone("h_psi_data_bkgsub")
    h_data_bkgsub.Add(h_accidental, -1)
    h_data_bkgsub.Add(h_bern, -1)

    h_corr = make_efficiency_corrected(h_data_bkgsub, psiacc_sdme, psigen_sdme, "psi")

    h_corr.SetTitle("")
    h_corr.SetXTitle("(#phi - #Phi)_{Ks} (rad) (Helicity frame)")
    h_corr.SetYTitle("Candidates / 0.035")
    h_corr.GetYaxis().SetMaxDigits(3)
    h_corr.SetLineColor(ROOT.kBlack)
    h_corr.SetLineWidth(2)
    h_corr.Draw("E")

    draw_bottom_info_pad(
        pad_info,
        label_text="Efficiency-corrected",
        legend_items=[
            (h_corr, "data", "l"),
        ],
        notes=[
            f"{t_bin}",
            "(data - bkg) / (accmc / genmc)",
            f"Integral: {h_corr.Integral():.0f}",
            f"Bkg subtracted: {h_bkg_total.Integral():.0f}",
        ],
    )
    keep(c_psi_corr)
    add_pdf_page(c_psi_corr, pdf_path)

    close_pdf(c_psi_corr,pdf_path)  # ← fixed: was close_pdf(pdf_path)


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

    end_time = time.time()
    print(f"Time to run: {end_time - start_time:.1f} seconds")


if __name__ == "__main__":
    main()
