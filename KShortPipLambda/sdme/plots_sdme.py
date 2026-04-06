import os
import time
import ROOT

ROOT.gROOT.SetBatch(True)

from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

# -----------------------------
# Files / globals
# -----------------------------
t_bin = "#bf{-t = (0.1 - 1.0) GeV^{2}}" # t_bin label for plots.  MUST match the t_bin used to create the ROOT file.
FND = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/outputTrees/032926_t110_fit1/KsPipLamb_ALL.root"
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


def load_histograms(filename):
    f = ROOT.TFile.Open(filename)
    if not f or f.IsZombie():
        raise RuntimeError(f"Could not open ROOT file: {filename}")

    hist = {
        "cosThetadat":      get_hist_or_raise(f, "cosThetadat"),
        "cosThetaacc_sdme": get_hist_or_raise(f, "cosThetaacc_sdme"),
        "cosThetabkg_sdme": get_hist_or_raise(f, "cosThetabkg_sdme"),
        "cosThetagen_sdme": get_hist_or_raise(f, "cosThetagen_sdme"),

        "phidat":      get_hist_or_raise(f, "phidat"),
        "phiacc_sdme": get_hist_or_raise(f, "phiacc_sdme"),
        "phibkg_sdme": get_hist_or_raise(f, "phibkg_sdme"),
        "phigen_sdme": get_hist_or_raise(f, "phigen_sdme"),

        "Phidat":      get_hist_or_raise(f, "Phidat"),
        "Phiacc_sdme": get_hist_or_raise(f, "Phiacc_sdme"),
        "Phibkg_sdme": get_hist_or_raise(f, "Phibkg_sdme"),
        "Phigen_sdme": get_hist_or_raise(f, "Phigen_sdme"),

        "psidat":      get_hist_or_raise(f, "psidat"),
        "psiacc_sdme": get_hist_or_raise(f, "psiacc_sdme"),
        "psibkg_sdme": get_hist_or_raise(f, "psibkg_sdme"),
        "psigen_sdme": get_hist_or_raise(f, "psigen_sdme"),
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


# -----------------------------
# cosTheta plots
# -----------------------------
def cosTheta_plots(hist, pdf_path):
    cosThetadat      = hist["cosThetadat"]
    cosThetaacc_sdme = hist["cosThetaacc_sdme"]
    cosThetabkg_sdme = hist["cosThetabkg_sdme"]
    cosThetagen_sdme = hist["cosThetagen_sdme"]

    # -----------------------------
    # CosineTheta of Ks in helicity frame
    # -----------------------------
    c1, pad_plot, pad_info = make_canvas_with_bottompad("c1_cosTheta", info_frac=0.22)

    pad_plot.cd()

    h_data = cosThetadat.Clone("h_data_cos")
    h_acc  = cosThetaacc_sdme.Clone("h_acc_cos")
    h_bkg  = cosThetabkg_sdme.Clone("h_bkg_cos")
    h_sum  = h_acc.Clone("h_sum_cos")
    h_sum.Add(h_bkg)

    h_data.SetTitle("")
    h_data.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.01")

    style_data_mc_overlay(h_data, h_sum, h_bkg)

    h_data.Draw()
    h_sum.Draw("hist same")
    h_bkg.Draw("hist same")

    # integrals to display in info pad
    data_int = integral_between(h_data, -1.0, 0.5)
    acc_int  = integral_between(h_acc, -1.0, 0.5)
    bkg_int  = integral_between(h_bkg, -1.0, 0.5)

    draw_bottom_info_pad(
        pad_info,
        label_text="Not acceptance-corrected",
        legend_items=[
            (h_data, "data", "l"),
            (h_sum,  "accmc + bkg", "f"),
            (h_bkg,  "bkgmc", "f"),
        ],
        notes=[
            f"{t_bin}",
            "Fit all Polarizations (0, 45, 90, 135)",
            f"Data int: {data_int:.0f} = acc+bkg = {(acc_int + bkg_int):.0f}",
            "#bf{DATA:} sp18, fa18, sp20. #bf{MC:} sp18, fa18.",
        ],
    )

    open_pdf(c1, pdf_path)

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
            graph.GetYaxis().SetRangeUser(0.0, 0.1)
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
        label_text="Efficiency (fitted trees)",
        legend_items=legend_items,
        notes=notes,
    )

    add_pdf_page(c2, pdf_path)

    # -----------------------------
    # DIAGNOSTIC PLOT: accmc / efficiency = genmc
    # -----------------------------
    c3, pad_plot, pad_info = make_canvas_with_bottompad("c3_cosTheta_diag", info_frac=0.22)
    pad_plot.cd()

    h_eff = cosThetaacc_sdme.Clone("h_eff_cos")
    h_eff.Divide(cosThetagen_sdme)

    h_diag = cosThetaacc_sdme.Clone("h_diag_cos")
    h_diag.Divide(h_eff)
    h_diag.SetTitle("")
    h_diag.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    h_diag.SetYTitle("Count")
    h_diag.SetLineColor(ROOT.kBlue + 1)
    h_diag.SetLineWidth(2)
    h_diag.GetXaxis().SetNdivisions(4, 0, 0, True)
    h_diag.GetYaxis().SetRangeUser(1100, 2000)
    h_diag.GetYaxis().SetTitleOffset(1.21)
    h_diag.GetYaxis().SetMaxDigits(3)
    h_diag.Draw()

    h_gen = cosThetagen_sdme.Clone("h_gen_cos")
    h_gen.SetTitle("")
    h_gen.SetXTitle("cos#theta_{K_{S}} (Helicity frame)")
    # h_gen.SetYTitle("Generated MC")
    h_gen.SetLineColor(ROOT.kGreen - 6)
    h_gen.SetFillColorAlpha(ROOT.kGreen - 2, 0.60)
    h_gen.SetFillStyle(1001)
    h_gen.SetLineWidth(2)
    h_gen.GetYaxis().SetRangeUser(1100, 2000)
    h_gen.GetYaxis().SetTitleOffset(1.21)
    h_gen.GetYaxis().SetMaxDigits(3)
    h_gen.Draw("hist same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Diagnostic plot (fitted trees)",
        legend_items=[
            (h_diag, "accmc / efficiency", "l"),
            (h_gen, "genmc", "f"),
        ],
        notes=[
            "",
            f"Integral acc / eff: {integral_between(h_diag, -1.0, 0.5):.0f}",
            f"Integral genmc: {integral_between(h_gen, -1.0, 0.5):.0f}",
            "#theta = (-1, 0.5)",
        ],
    )

    add_pdf_page(c3, pdf_path)

# -----------------------------
# Azimuthal angle of Ks in helicity frame
# -----------------------------
def phi_plots(hist, pdf_path):
    phidat      = hist["phidat"]
    phiacc_sdme = hist["phiacc_sdme"]
    phibkg_sdme = hist["phibkg_sdme"]
    phigen_sdme = hist["phigen_sdme"]

    c1, pad_plot, pad_info = make_canvas_with_bottompad("c_phi", info_frac=0.22)

    pad_plot.cd()

    h_data = phidat.Clone("h_phi_data")
    h_acc  = phiacc_sdme.Clone("h_phi_acc")
    h_bkg  = phibkg_sdme.Clone("h_phi_bkg")
    h_sum  = h_acc.Clone("h_phi_sum")
    h_sum.Add(h_bkg)

    h_data.SetTitle("")
    h_data.SetXTitle("#phi (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")

    style_data_mc_overlay(h_data, h_sum, h_bkg)

    h_data.Draw()
    h_sum.Draw("hist same")
    h_bkg.Draw("hist same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Azmuthal angle of Ks",
        legend_items=[
            (h_data, "data", "l"),
            (h_sum,  "accmc + bkg", "f"),
            (h_bkg,  "bkgmc", "f"),
        ],
        notes=[
            f"Data int: {h_data.Integral():.0f}",
            f"Acc int: {h_acc.Integral():.0f}",
            f"Bkg int: {h_bkg.Integral():.0f}",
        ],
    )

    open_pdf(c1, pdf_path)


    # -----------------------------
    # Azimuthal EFFICIENCY
    # -----------------------------
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_phi_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items = []
    notes = []

    # integrals to display in info pad
    acc_int = integral_between(phiacc_sdme, -1.0, 0.5)
    gen_int  = integral_between(phigen_sdme, -1.0, 0.5)

    if ROOT.TEfficiency.CheckConsistency(phiacc_sdme, phigen_sdme):
        eff = ROOT.TEfficiency(phiacc_sdme, phigen_sdme)
        eff.SetTitle(";#phi_{K_{S}} (Helicity frame);Efficiency")
        eff.Draw("AP")
        c2.Update()

        graph = eff.GetPaintedGraph()
        if graph:
            graph.GetXaxis().SetTitle("#phi_{K_{S}} (Helicity frame)")
            graph.GetYaxis().SetTitle("Efficiency (accmc / genmc)")
            graph.GetYaxis().SetRangeUser(0.0, 0.1)
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
        label_text="Efficiency (fitted trees)",
        legend_items=legend_items,
        notes=notes,
    )

    add_pdf_page(c2, pdf_path)

# -----------------------------
# Polarization angle of Ks in helicity frame
# -----------------------------
def bigPhi_plots(hist, pdf_path):
    Phidat      = hist["Phidat"]
    Phiacc_sdme = hist["Phiacc_sdme"]
    Phibkg_sdme = hist["Phibkg_sdme"]
    Phigen_sdme = hist["Phigen_sdme"]

    c1, pad_plot, pad_info = make_canvas_with_bottompad("c_bigPhi", info_frac=0.22)

    pad_plot.cd()

    h_data = Phidat.Clone("h_bigPhi_data")
    h_acc  = Phiacc_sdme.Clone("h_bigPhi_acc")
    h_bkg  = Phibkg_sdme.Clone("h_bigPhi_bkg")
    h_sum  = h_acc.Clone("h_bigPhi_sum")
    h_sum.Add(h_bkg)

    h_data.SetTitle("")
    h_data.SetXTitle("#Phi (rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")

    style_data_mc_overlay(h_data, h_sum, h_bkg)

    h_data.Draw()
    h_sum.Draw("hist same")
    h_bkg.Draw("hist same")

    draw_bottom_info_pad(
        pad_info,
        label_text="Polarization angle of Ks",
        legend_items=[
            (h_data, "data", "l"),
            (h_sum,  "accmc + bkg", "f"),
            (h_bkg,  "bkgmc", "f"),
        ],
        notes=[
            f"Data int: {h_data.Integral():.0f}",
            f"Acc int: {h_acc.Integral():.0f}",
            f"Bkg int: {h_bkg.Integral():.0f}",
        ],
    )

    open_pdf(c1, pdf_path)

    # -----------------------------
    # Polarization angle EFFICIENCY
    # -----------------------------
    c2, pad_plot, pad_info = make_canvas_with_bottompad("c2_bigPhi_eff", info_frac=0.22)
    pad_plot.cd()

    legend_items = []
    notes = []

    # integrals to display in info pad
    acc_int = integral_between(Phiacc_sdme, -3.0, 3.0)
    gen_int  = integral_between(Phigen_sdme, -3.0, 3.0)

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
            "#phi = (-1, 0.5)",
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

# -----------------------------
# psi = phi - Phi (azimuthal angle minus Polarization angle)
# -----------------------------
def phi_minus_bigPhi_plots(hist, pdf_path):
    psidat      = hist["psidat"]
    psiacc_sdme = hist["psiacc_sdme"]
    psibkg_sdme = hist["psibkg_sdme"]

    c, pad_plot, pad_info = make_canvas_with_bottompad("c_psi", info_frac=0.22)

    pad_plot.cd()

    h_data = psidat.Clone("h_psi_data")
    h_acc  = psiacc_sdme.Clone("h_psi_acc")
    h_bkg  = psibkg_sdme.Clone("h_psi_bkg")
    h_sum  = h_acc.Clone("h_psi_sum")
    h_sum.Add(h_bkg)

    h_data.SetTitle("")
    h_data.SetXTitle("#phi_{Ks}(rad) - #Phi_{Ks}(rad) (Helicity frame)")
    h_data.SetYTitle("Candidates / 0.035")

    style_data_mc_overlay(h_data, h_sum, h_bkg)

    h_data.Draw()
    h_sum.Draw("hist same")
    h_bkg.Draw("hist same")

    draw_bottom_info_pad(
        pad_info,
        label_text="azimuthal - pol. angle",
        legend_items=[
            (h_data, "data", "l"),
            (h_sum,  "accmc + bkg", "f"),
            (h_bkg,  "bkgmc", "f"),
        ],
        notes=[
            f"Data int: {h_data.Integral():.0f}",
            f"Acc int: {h_acc.Integral():.0f}",
            f"Bkg int: {h_bkg.Integral():.0f}",
        ],
    )

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

    end_time = time.time()
    print(f"Time to run: {end_time - start_time:.1f} seconds")


if __name__ == "__main__":
    main()
