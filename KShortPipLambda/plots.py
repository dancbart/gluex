import os
import time
import ROOT

ROOT.gROOT.SetBatch(True)

from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

ROOT.TGaxis.SetMaxDigits(3)

# ------------------------------------------------------------
# Files / globals
# ------------------------------------------------------------

# ------ Use to plot variables used as 'global' cuts (beam energy, unused shower, etc).  These are unskimmed files. ---------------------
FND_unSkimmed = "/volatile/halld/home/dbarton/pipkslamb/data/fall2018/flatten/tree_pipkslamb__B4_M16_M18_FSFlat_sum_ALLpols_AMO.root"
FND_unSkimmed_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sp18-fa18_polALL.root"
# Not used:
# FND_unSkimmed_MC_THROWN.  For plotting, use 'FND_signalSkims_MC_THROWN' (created below).

# ------ Use to plot Ks and Lambda, K*, etc. pre-fit distributions -------------------------------------------
FND_eventSelectionSkims = "/volatile/halld/home/dbarton/pipkslamb/skims/tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols.root"
FND_eventSelectionSkims_MC = "/volatile/halld/home/dbarton/pipkslamb/skims/tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_MC.root"
# Not used:
# FND_eventSelectionSkims_MC_THROWN. For plotting, use 'FND_signalSkims_MC_THROWN' (created below).

# ------ Use to plot final signal distributions that would be used for AmpTools fits (K*892 mass, angular distributions, etc.).  These are the ACTUAL trees fed into AmpTools.  ----
FND_signalSkims = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/sourceFiles/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_ALLpols.root"
FND_signalSkims_MC = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/sourceFiles/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC.root"
FND_signalSkims_MC_THROWN = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/sourceFiles/tree_pipkslamb_SIGNAL_SKIM_K892_THROWN.root"

allPlots = "plots/plots.pdf"
NT = "ntFSGlueX_MODECODE"
treeName = "ntFSGlueX_100000000_1100"

DecayingLambda = "1"
Proton         = "1a"
PiMinus2       = "1b"
DecayingKShort = "2"
PiPlus2        = "2a"
PiMinus1       = "2b"
PiPlus1        = "3"

bggen = False

# Helper function: Label each plot as either DATA or Monte Carlo:
def file_label(fname):
    s = fname.lower()
    return "MC" if ("mc" in s or "bggen" in s) else "Data"

# Keep ROOT objects alive
_KEEP = []


def keep(obj):
    _KEEP.append(obj)
    return obj


# ------------------------------------------------------------
# Style
# ------------------------------------------------------------
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

    style.SetPadBottomMargin(0.14)
    style.SetPadLeftMargin(0.16)
    style.SetPadTopMargin(0.05)
    style.SetPadRightMargin(0.06)

    style.SetStripDecimals(0)
    style.SetLabelSize(0.045, "xyz")
    style.SetTitleSize(0.055, "xyz")
    style.SetTitleFont(42, "xyz")
    style.SetLabelFont(42, "xyz")
    style.SetTitleOffset(1.15, "x")
    style.SetTitleOffset(1.35, "y")
    style.SetLabelOffset(0.010, "xyz")

    style.SetOptStat(0)
    style.SetOptTitle(0)
    style.SetHistLineWidth(2)
    style.SetHistFillColor(920)
    style.SetPalette(ROOT.kViridis)

    ROOT.gROOT.SetStyle("GlueX")
    ROOT.gROOT.ForceStyle()


# ------------------------------------------------------------
# Cuts
# ------------------------------------------------------------
def setup():
    if ROOT.FSModeCollection.modeVector().size() != 0:
        return

    ROOT.FSModeCollection.addModeInfo("100000000_1100").addCategory("m100000000_1100")

    ROOT.FSCut.defineCut("tRange110", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")
    ROOT.FSCut.defineCut("tRange13", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.1 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<0.3")
    ROOT.FSCut.defineCut("tRange35", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.3 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<0.5")
    ROOT.FSCut.defineCut("tRange510", f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))>0.5 && abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))<1.0")
    ROOT.FSCut.defineCut("rf", "abs(RFDeltaT)>2.0", "abs(RFDeltaT)>6.0", 0.1667)
    ROOT.FSCut.defineCut("chi2DOF", "Chi2DOF<5.0")
    ROOT.FSCut.defineCut("unusedE", "EnUnusedSh<0.1")
    ROOT.FSCut.defineCut("unusedTracks", "NumUnusedTracks<1")
    # Spring 2017 - Fall 2018: 30,000 - 59,999.  Spring 2020 - Spring 2023: 70,000 - 122,000. Spring 2025: 130,000 - 139,999gg
    ROOT.FSCut.defineCut(
        "coherentPeak",
        "("
        "(Run>=30000 && Run<=59999 && EnPB>8.2 && EnPB<8.8) ||"
        "(Run>=70000 && Run<=122000 && EnPB>8.0 && EnPB<8.6) ||"
        "(Run>=130000 && Run<=139999 && EnPB>8.3 && EnPB<8.9)"
        ")")
    ROOT.FSCut.defineCut("flightLengthLambda", "VeeLP1>2.0")
    ROOT.FSCut.defineCut("flightLengthKShort", "VeeLP2>2.0")
    ROOT.FSCut.defineCut("targetZ", "ProdVz>52.0 && ProdVz<78.0")
    ROOT.FSCut.defineCut("KShort", f"abs(MASS({DecayingKShort})-0.4976)<0.03", f"(abs(MASS({DecayingKShort})-0.4976+0.0974)<0.015 || abs(MASS({DecayingKShort})-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("Lambda", f"abs(MASS({DecayingLambda})-1.119)<0.01375", f"(abs(MASS({DecayingLambda})-1.119+0.032875)<0.006875 || abs(MASS({DecayingLambda})-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("selectKSTAR892", f"MASS({DecayingKShort},{PiPlus1})>0.80 && MASS({DecayingKShort},{PiPlus1})<1.00")
    ROOT.FSCut.defineCut("rejectSigma1385", f"MASS({DecayingLambda},{PiPlus1})>2.00 && MASS({DecayingLambda},{PiPlus1})<4.0")

def setup_genmc():
    ROOT.FSCut.defineCut("tRangeTHROWN", "abs(-1*MCMASS2(GLUEXTARGET,-1))>0.1 && abs(-1*MCMASS2(GLUEXTARGET,-1))<1.0")
    ROOT.FSCut.defineCut("tRangeTHROWN35", "abs(-1*MCMASS2(GLUEXTARGET,-1))>0.3 && abs(-1*MCMASS2(GLUEXTARGET,-1))<0.5")
    ROOT.FSCut.defineCut("KShortTHROWN", "abs(MCMASS(2)-0.4976)<0.03", "(abs(MCMASS(2)-0.4976+0.0974)<0.015 || abs(MCMASS(2)-0.4976-0.1226)<0.015)", 1.0)
    ROOT.FSCut.defineCut("LambdaTHROWN", "abs(MCMASS(1)-1.119)<0.01375", "(abs(MCMASS(1)-1.119+0.032875)<0.006875 || abs(MCMASS(1)-1.119-0.032125)<0.006875)", 1.0)
    ROOT.FSCut.defineCut("coherentPeakTHROWN", "MCEnPB>8.2 && MCEnPB<8.6")
    ROOT.FSCut.defineCut("selectKSTAR892THROWN", "MCMASS(2,3)>0.80 && MCMASS(2,3)<1.00")

# -------------------------- for reference only ----------------------------
# These cuts are already applied in the skimming script.  They are shown here for
# reference only.
generalCuts_eventSelection = "CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"
# --------------------------------------------------------------------------

generalCuts = "CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
generalCuts_t13 = "CUT(tRange13,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
generalCuts_t35 = "CUT(tRange35,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
generalCuts_t510 = "CUT(tRange510,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"
signalCuts = "CUT(rf,KShort,Lambda,selectKSTAR892)"
signalCutsMC = "CUT(KShort,Lambda,selectKSTAR892)"
signalCuts_weights = "CUTWT(rf,KShort,Lambda)"
signalCuts_weightsMC = "CUTWT(KShort,Lambda)"
sidebandWeights = "CUTSBWT(rf,KShort,Lambda)"
signalCuts_THROWN = "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"

# For the cut-comparison plot
baseCuts = "tRange110,flightLengthKShort,flightLengthLambda,rejectSigma1385"
sidebandCuts = "rf,KShort,Lambda"

# Explanation of cut methods (Boris):

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

# ------------------------------------------------------------
# Canvas helper functions
# ------------------------------------------------------------
import textwrap

def make_panel_grid(canvas, ncols, nrows, info_frac=0.30, main_info_frac=0.42,
                    left_margin=0.16, right_margin=0.06,
                    top_margin=0.06, bottom_margin_plot=0.22,
                    bottom_margin_info=0.12):
    """
    Returns a list of dicts:
        {
          "plot": TPad,
          "info_main": TPad,
          "info_notes": TPad,
          "row": row_index,
          "col": col_index
        }

    Layout is vertically stacked within each cell:
        top    : plot
        middle : primary info pad
        bottom : notes / cuts pad
    """
    panels = []

    cell_w = 1.0 / ncols
    cell_h = 1.0 / nrows

    for row in range(nrows):
        for col in range(ncols):
            x1 = col * cell_w
            x2 = (col + 1) * cell_w
            y1 = 1.0 - (row + 1) * cell_h
            y2 = 1.0 - row * cell_h

            total_info_h = info_frac * cell_h
            notes_h = total_info_h * (1.0 - main_info_frac)
            main_h = total_info_h * main_info_frac

            notes_y1 = y1
            notes_y2 = notes_y1 + notes_h
            main_y1 = notes_y2
            main_y2 = main_y1 + main_h
            plot_y1 = main_y2
            plot_y2 = y2

            plot_pad = ROOT.TPad(f"plot_r{row}_c{col}", "", x1, plot_y1, x2, plot_y2)
            info_main_pad = ROOT.TPad(f"info_main_r{row}_c{col}", "", x1, main_y1, x2, main_y2)
            info_notes_pad = ROOT.TPad(f"info_notes_r{row}_c{col}", "", x1, notes_y1, x2, notes_y2)

            keep(plot_pad)
            keep(info_main_pad)
            keep(info_notes_pad)

            for pad in (plot_pad, info_main_pad, info_notes_pad):
                pad.SetFillColor(0)
                pad.SetBorderMode(0)
                pad.SetFrameBorderMode(0)

            lm = left_margin if col == 0 else 0.05
            rm = right_margin if col == ncols - 1 else 0.03
            tm = top_margin if row == 0 else 0.03

            plot_pad.SetLeftMargin(lm)
            plot_pad.SetRightMargin(rm)
            plot_pad.SetTopMargin(tm)
            plot_pad.SetBottomMargin(bottom_margin_plot)

            info_main_pad.SetLeftMargin(lm)
            info_main_pad.SetRightMargin(rm)
            info_main_pad.SetTopMargin(0.04)
            info_main_pad.SetBottomMargin(bottom_margin_info)

            info_notes_pad.SetLeftMargin(lm)
            info_notes_pad.SetRightMargin(rm)
            info_notes_pad.SetTopMargin(0.04)
            info_notes_pad.SetBottomMargin(bottom_margin_info)

            plot_pad.Draw()
            info_main_pad.Draw()
            info_notes_pad.Draw()

            panels.append({
                "plot": plot_pad,
                "info_main": info_main_pad,
                "info_notes": info_notes_pad,
                "row": row,
                "col": col,
            })

    return panels


def _draw_pad_separator(pad):
    pad.cd()
    line = ROOT.TLine(0.0, 0.98, 1.0, 0.98)
    line.SetNDC(True)
    line.SetLineColor(ROOT.kGray + 1)
    line.Draw()
    keep(line)


# def draw_info_pad(info_pad, label_text, legend_items=None, notes=None):
#     """
#     Primary info pad: label + optional legend + short summary notes.
#     legend_items: list of (obj, text, drawopt)
#     notes: list of strings
#     """
#     info_pad.cd()
#     info_pad.Clear()
#     _draw_pad_separator(info_pad)

#     if legend_items:
#         leg = ROOT.TLegend(0.40, 0.16, 0.96, 0.86)
#         leg.SetBorderSize(0)
#         leg.SetFillStyle(0)
#         leg.SetTextSize(0.12)
#         for obj, text, opt in legend_items:
#             leg.AddEntry(obj, text, opt)
#         leg.Draw()
#         keep(leg)

#     tex = ROOT.TLatex()
#     tex.SetNDC(True)
#     tex.SetTextFont(42)
#     tex.SetTextSize(0.12)
#     tex.SetTextAlign(13)
#     tex.DrawLatex(0.06, 0.92, f"#bf{{{label_text}}}")
#     keep(tex)

#     if notes:
#         y = 0.73
#         for note in notes:
#             x = 0.06
#             text = note
#             if isinstance(note, tuple):
#                 x, text = note
#             t = ROOT.TLatex()
#             t.SetNDC(True)
#             t.SetTextFont(42)
#             t.SetTextSize(0.08)
#             t.SetTextAlign(13)
#             t.DrawLatex(x, y, text)
#             keep(t)
#             y -= 0.15

#     info_pad.Modified()
#     info_pad.Update()

def draw_info_pad(
    info_pad,
    label_text,
    legend_items=None,
    notes=None,
    legend_box=(0.40, 0.16, 0.96, 0.86),
    legend_text_size=0.12,
    label_pos=(0.06, 0.92),
    label_font=42,
    label_size=0.12,
    notes_start_y=0.73,
    notes_text_size=0.08,
    notes_step=0.15,
    notes_font=42,
    notes_x_default=0.06,
    draw_separator=True,
    clear_pad=True,
):
    info_pad.cd()
    if clear_pad:
        info_pad.Clear()
    if draw_separator:
        _draw_pad_separator(info_pad)

    tex = ROOT.TLatex()
    tex.SetNDC(True)
    tex.SetTextFont(label_font)
    tex.SetTextSize(label_size)
    tex.SetTextAlign(13)
    tex.DrawLatex(label_pos[0], label_pos[1], label_text)
    keep(tex)

    if legend_items:
        x1, y1, x2, y2 = legend_box
        leg = ROOT.TLegend(x1, y1, x2, y2)
        leg.SetTextSize(legend_text_size)
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        for obj, text, opt in legend_items:
            leg.AddEntry(obj, text, opt)
        leg.Draw()
        keep(leg)

    if notes:
        y = notes_start_y
        for note in _normalize_note_lines(notes):
            if isinstance(note, tuple):
                x, text = note
            else:
                x, text = notes_x_default, note

            t = ROOT.TLatex()
            t.SetNDC(True)
            t.SetTextFont(notes_font)
            t.SetTextSize(notes_text_size)
            t.SetTextAlign(13)
            t.DrawLatex(x, y, text)
            keep(t)
            y -= notes_step

    info_pad.Modified()
    info_pad.Update()

def _normalize_note_lines(lines, width=90):
    out = []
    for line in lines or []:
        if isinstance(line, tuple):
            out.append(line)
            continue

        s = str(line)

        # Only wrap if it's actually longer than the width
        if len(s) <= width:
            out.append(s)
        else:
            wrapped = textwrap.wrap(
                s,
                width=width,
                break_long_words=False,
                break_on_hyphens=False
            )
            out.extend(wrapped if wrapped else [""])

    return out

# def draw_notes_pad(notes_pad, title="Notes", notes=None):
#     """Secondary bottom info pad for detailed notes / cut strings."""
#     notes_pad.cd()
#     notes_pad.Clear()
#     _draw_pad_separator(notes_pad)

#     title_tex = ROOT.TLatex()
#     title_tex.SetNDC(True)
#     title_tex.SetTextFont(42)
#     title_tex.SetTextSize(0.11)
#     title_tex.SetTextAlign(13)
#     title_tex.DrawLatex(0.04, 0.92, f"#bf{{{title}}}")
#     keep(title_tex)

#     y = 0.78
#     for line in _normalize_note_lines(notes):
#         x = 0.04
#         text = line
#         if isinstance(line, tuple):
#             x, text = line
#         t = ROOT.TLatex()
#         t.SetNDC(True)
#         t.SetTextFont(42)
#         t.SetTextSize(0.072)
#         t.SetTextAlign(13)
#         t.DrawLatex(x, y, text)
#         keep(t)
#         y -= 0.11
#         if y < 0.10:
#             break

#     notes_pad.Modified()
#     notes_pad.Update()

def draw_notes_pad(
    info_pad,
    title=None,
    notes=None,
    title_pos=(0.06, 0.88),
    title_font=62,
    title_size=0.12,
    notes_start_y=0.70,
    notes_text_size=0.10,
    notes_step=0.18,
    notes_font=42,
    notes_x_default=0.06,
    draw_separator=True,
    clear_pad=True,
):
    info_pad.cd()
    if clear_pad:
        info_pad.Clear()
    if draw_separator:
        _draw_pad_separator(info_pad)

    if title:
        tex = ROOT.TLatex()
        tex.SetNDC(True)
        tex.SetTextFont(title_font)
        tex.SetTextSize(title_size)
        tex.SetTextAlign(13)
        tex.DrawLatex(title_pos[0], title_pos[1], title)
        keep(tex)

    if notes:
        y = notes_start_y
        for note in _normalize_note_lines(notes):
            if isinstance(note, tuple):
                x, text = note
            else:
                x, text = notes_x_default, note

            t = ROOT.TLatex()
            t.SetNDC(True)
            t.SetTextFont(notes_font)
            t.SetTextSize(notes_text_size)
            t.SetTextAlign(13)
            t.DrawLatex(x, y, text)
            keep(t)
            y -= notes_step
            if y < 0.10:
                break

    info_pad.Modified()
    info_pad.Update()

# ------------------------------------------------------------
# Other helper functions
# ------------------------------------------------------------

def integral_between(hist, xmin, xmax):
    ax = hist.GetXaxis()
    bin1 = ax.FindBin(xmin)
    bin2 = ax.FindBin(xmax)
    return hist.Integral(bin1, bin2)

def draw_vertical_lines(hist, xs, color=ROOT.kBlue, style=1, width=2):
    ymax = hist.GetMaximum()
    lines = []
    for x in xs:
        ln = ROOT.TLine(x, 0.0, x, ymax)
        ln.SetLineColor(color)
        ln.SetLineStyle(style)
        ln.SetLineWidth(width)
        ln.Draw("same")
        lines.append(keep(ln))
    return lines


def draw_horizontal_lines(hist, ys, color=ROOT.kBlue, style=1, width=2):
    xmin = hist.GetXaxis().GetXmin()
    xmax = hist.GetXaxis().GetXmax()
    lines = []
    for y in ys:
        ln = ROOT.TLine(xmin, y, xmax, y)
        ln.SetLineColor(color)
        ln.SetLineStyle(style)
        ln.SetLineWidth(width)
        ln.Draw("same")
        lines.append(keep(ln))
    return lines


def fs_get_th1(file_name, expr, bins, cuts):
    h = ROOT.FSModeHistogram.getTH1F(file_name, NT, "m100000000_1100", expr, bins, cuts)
    keep(h)
    return h


def fs_get_th2(file_name, expr, bins, cuts):
    h = ROOT.FSModeHistogram.getTH2F(file_name, NT, "m100000000_1100", expr, bins, cuts)
    keep(h)
    return h


def draw_mc_same(file_name, expr, bins, cuts):
    ROOT.FSModeHistogram.drawMCComponentsSame(file_name, NT, "m100000000_1100", expr, bins, cuts)


# ============================================================
# GLOBAL CUT PLOTS
# ============================================================
def global_eventSelection_Cuts(pdf_path):

    # ============================================================
    # Page 1: Unused shower energy
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_unusedE", "c_eventCuts_unusedE", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()
    ROOT.gPad.SetLogy(True)

    h1 = fs_get_th1(
        FND_unSkimmed,
        "EnUnusedSh",
        "(100,0.0,1.0)",
        "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)"
    )
    h1.SetXTitle("E_{unused} [GeV]")
    h1.SetYTitle("Events")
    h1.SetMinimum(0.5)
    h1.Draw("hist")

    if bggen:
        draw_mc_same(
            FND_unSkimmed, "EnUnusedSh", "(100,0.0,1.0)",
            "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)"
        )
    draw_vertical_lines(h1, [0.1])

    draw_info_pad(
        p["info_main"],
        file_label(FND_unSkimmed),
        legend_items=[(h1, "Data", "l")],
        notes=["Cut: E_{unused} < 0.1 GeV", "log scale"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts:",
            "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)",
            "Plotted variable: EnUnusedSh",
        ],
    )

    c.Print(f"{pdf_path}(")


    # ============================================================
    # Page 2: Production vertex z
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_targetZ", "c_eventCuts_targetZ", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()
    ROOT.gPad.SetLogy(False)

    h2 = fs_get_th1(
        FND_unSkimmed,
        "ProdVz",
        "(100,0.,100.0)",
        "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)"
    )
    h2.SetXTitle("Production vertex z-position [cm]")
    h2.SetYTitle("Events")
    h2.Draw("hist")

    if bggen:
        draw_mc_same(
            FND_unSkimmed, "ProdVz", "(100,0.,100.0)",
            "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)"
        )
    draw_vertical_lines(h2, [52.0, 78.0])

    draw_info_pad(
        p["info_main"],
        file_label(FND_unSkimmed),
        legend_items=[(h2, "Data", "l")],
        notes=["Cut: 52 < V_{z} < 78 cm"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts:",
            "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)",
            "Plotted variable: ProdVz",
        ],
    )

    c.Print(pdf_path)


    # ============================================================
    # Page 3: t-range
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_tRange", "c_eventCuts_tRange", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    h3 = fs_get_th1(
        FND_unSkimmed,
        f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
        "(100,0,2)",
        "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"
    )
    h3.SetXTitle("|-t| [GeV^{2}]")
    h3.SetYTitle("Events")
    h3.Draw("hist")

    if bggen:
        draw_mc_same(
            FND_unSkimmed,
            f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
            "(100,0,2)",
            "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"
        )
    draw_vertical_lines(h3, [0.1, 1.0])

    draw_info_pad(
        p["info_main"],
        file_label(FND_unSkimmed),
        legend_items=[(h3, "Data", "l")],
        notes=["Cut: 0.1 < |-t| < 1.0"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts:",
            "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)",
            f"Plotted variable: abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
        ],
    )

    c.Print(pdf_path)


    # ============================================================
    # Page 4: Beam energy / coherent peak
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_beamE", "c_eventCuts_beamE", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    h4 = fs_get_th1(
        FND_unSkimmed,
        "EnPB",
        "(125,5,12)",
        "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,targetZ)"
    )
    h4.SetXTitle("E_{beam} [GeV]")
    h4.SetYTitle("Events")
    h4.Draw("hist")

    if bggen:
        draw_mc_same(
            FND_unSkimmed, "EnPB", "(125,5,12)",
            "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,targetZ)"
        )
    draw_vertical_lines(h4, [8.2, 8.6])

    draw_info_pad(
        p["info_main"],
        file_label(FND_unSkimmed),
        legend_items=[(h4, "Data", "l")],
        notes=["Coherent peak", "8.2 < E_{beam} < 8.6 GeV"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts:",
            "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,targetZ)",
            "Plotted variable: EnPB",
        ],
    )

    c.Print(pdf_path)


    # ============================================================
    # Page 5: chi2/dof
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_chi2", "c_eventCuts_chi2", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    h5 = fs_get_th1(
        FND_unSkimmed,
        "Chi2DOF",
        "(80,0,20)",
        "CUT(tRange110,rf,unusedE,unusedTracks,coherentPeak,targetZ)"
    )
    h5.SetXTitle("#chi^{2}/dof")
    h5.SetYTitle("Events")
    h5.Draw("hist")

    if bggen:
        draw_mc_same(
            FND_unSkimmed, "Chi2DOF", "(80,0,20)",
            "CUT(tRange110,rf,unusedE,unusedTracks,coherentPeak,targetZ)"
        )
    draw_vertical_lines(h5, [5.0])

    draw_info_pad(
        p["info_main"],
        file_label(FND_unSkimmed),
        legend_items=[(h5, "Data", "l")],
        notes=["Cut: #chi^{2}/dof < 5"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts:",
            "CUT(tRange110,rf,unusedE,unusedTracks,coherentPeak,targetZ)",
            "Plotted variable: Chi2DOF",
        ],
    )

    c.Print(pdf_path)


    # ============================================================
    # Page 6: Lambda flight length
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_lambdaFL", "c_eventCuts_lambdaFL", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    h6 = fs_get_th1(
        FND_unSkimmed,
        "VeeLP1",
        "(60,0,10)",
        "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,Lambda,targetZ)"
    )
    h6.SetXTitle("#Lambda flight length [cm]")
    h6.SetYTitle("Events")
    h6.Draw("hist")
    draw_vertical_lines(h6, [2.0])

    draw_info_pad(
        p["info_main"],
        file_label(FND_unSkimmed),
        legend_items=[(h6, "Data", "l")],
        notes=["Cut: L_{#Lambda} > 2 cm"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts:",
            "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,Lambda,targetZ)",
            "Plotted variable: VeeLP1",
        ],
    )

    c.Print(pdf_path)


    # ============================================================
    # Page 7: KShort flight length
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_kshortFL", "c_eventCuts_kshortFL", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    h7 = fs_get_th1(
        FND_unSkimmed,
        "VeeLP2",
        "(60,0,10)",
        "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,KShort,targetZ)"
    )
    h7.SetXTitle("K_{S} flight length [cm]")
    h7.SetYTitle("Events")
    h7.Draw("hist")
    draw_vertical_lines(h7, [2.0])

    draw_info_pad(
        p["info_main"],
        file_label(FND_unSkimmed),
        legend_items=[(h7, "Data", "l")],
        notes=["Cut: L_{K_{S}} > 2 cm"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts:",
            "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,KShort,targetZ)",
            "Plotted variable: VeeLP2",
        ],
    )

    c.Print(pdf_path)

# ------------------------------------------------------------
# KSHORT & LAMBDA MASS PLOTS
# ------------------------------------------------------------


# ------------------------------------------------------------
# Compare FSRoot's cut macros (shown for KSHORT)
# ------------------------------------------------------------

def massPlots_KShort_cutComparisons(pdf_path):
    c = ROOT.TCanvas("c_mass_ks_cutComparisons", "c_mass_ks_cutComparisons", 900, 950)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    # ------------------------------------------------------------
    # Histograms
    # ------------------------------------------------------------
    hKShort0 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})"
    )

    hKShort1 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts},{sidebandCuts})"
    )

    hKShort2 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})&&CUTSB({sidebandCuts})"
    )

    hKShort3 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})"
    )

    hKShort4 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})&&CUTSUB({sidebandCuts})"
    )

    hKShort5 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )

    # ------------------------------------------------------------
    # Styling
    # ------------------------------------------------------------
    hKShort0.SetXTitle("M(#pi^{+}#pi^{-}) [GeV/c^{2}]")
    hKShort0.SetYTitle("Counts / 5 MeV")
    hKShort0.SetMinimum(0.0)
    hKShort0.SetLineColor(ROOT.kBlack)
    hKShort0.SetLineWidth(2)

    hKShort1.SetLineColor(ROOT.kOrange + 7)
    hKShort1.SetLineWidth(2)
    hKShort1.SetFillColor(ROOT.kOrange + 7)
    hKShort1.SetFillStyle(3004)

    hKShort2.SetLineColor(ROOT.kRed)
    hKShort2.SetLineWidth(2)
    hKShort2.SetFillColor(ROOT.kRed)

    hKShort3.SetLineColor(ROOT.kBlue)
    hKShort3.SetLineWidth(2)
    hKShort3.SetFillColor(ROOT.kBlue)
    hKShort3.SetFillStyle(3005)

    hKShort4.SetLineColor(ROOT.kMagenta)
    hKShort4.SetLineWidth(2)
    hKShort4.SetFillColor(ROOT.kMagenta)

    hKShort5.SetLineColor(ROOT.kGreen + 2)
    hKShort5.SetLineWidth(2)
    hKShort5.SetFillColor(ROOT.kGreen + 2)
    hKShort5.SetFillStyle(3006)

    # ------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------
    hKShort0.Draw("hist")
    hKShort1.Draw("hist same")
    hKShort2.Draw("hist same")
    hKShort3.Draw("hist same")
    hKShort4.Draw("hist same")
    hKShort5.Draw("hist same")

    # ------------------------------------------------------------
    # Integrals
    # ------------------------------------------------------------
    int0 = hKShort0.Integral()
    int1 = hKShort1.Integral()
    int2 = hKShort2.Integral()
    int3 = hKShort3.Integral()
    int4 = hKShort4.Integral()
    int5 = hKShort5.Integral()

    # ------------------------------------------------------------
    # Info pad
    # ------------------------------------------------------------
    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hKShort0, f"CUT(base): {int0:.0f}", "l"),
            (hKShort1, f"CUT(base,sideband): {int1:.0f}", "lf"),
            (hKShort2, f"CUT(base) && CUTSB(sideband): {int2:.0f}", "lf"),
            (hKShort3, f"CUT(base) * CUTSBWT(sideband): {int3:.0f}", "lf"),
            (hKShort4, f"CUT(base) && CUTSUB(sideband): {int4:.0f}", "lf"),
            (hKShort5, f"CUT(base) * CUTWT(sideband): {int5:.0f}", "lf"),
        ],
        notes=[
            "K_{S} FSRoot cut macro comparison",
        ]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Global Cuts: {generalCuts_eventSelection}",
            f"Base Cuts = {baseCuts}",
            f"Sideband Cuts = {sidebandCuts}",
        ]
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")
    ROOT.FSHistogram.clearHistogramCache()

# hMetapi
# CUT(unusedTracks,unusedE,zProton,chi2,cet0103,e8288,photFiducialA,photFiducialB,photFiducialC,photFiducialD,delta,rejectOmega,protMom,rf,eta,pi0)
# hMetapiSig
# CUT(unusedTracks,unusedE,zProton,chi2,cet0103,e8288,photFiducialA,photFiducialB,photFiducialC,photFiducialD,delta,rejectOmega,protMom)*CUTWT(rf,eta,pi0)");
# hMetapiBg
# CUT(unusedTracks,unusedE,zProton,chi2,cet0103,e8288,photFiducialA,photFiducialB,photFiducialC,photFiducialD,delta,rejectOmega,protMom)*CUTSBWT(rf,eta,pi0)


# -------- KSHORT -------------
def massPlots_KShort(pdf_path):
    c = ROOT.TCanvas("c_mass_ks", "c_mass_ks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})",
    )

    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})",
    )
    hBkgNegative = hBkg.Clone("hBkgNegative")
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(#pi^{+}#pi^{-}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 5 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)


    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    integral_ks = integral_between(hData, 0.35, 0.65)
    integral_ksSig = integral_between(hSig, 0.35, 0.65)
    integral_ksBkg = integral_between(hBkg, 0.35, 0.65)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "Ks " "(Integral: " f"{integral_ks:.0f})", "pE"),
            (hSig, "Ks Signal " "(Integral: " f"{integral_ksSig:.0f})", "f"),
            (hBkgNegative, "Ks Background " "(Integral: " f"{integral_ksBkg:.0f})", "f"),
        ],
        notes=["K_{S} sideband study"],

        # --- layout tweaks ---
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.68,
        notes_text_size=0.075,
        notes_step=0.12,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            f"Base cuts: CUT({baseCuts},{sidebandCuts})",
            f"Signal: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"Background: CUT({baseCuts})*CUTSBWT({sidebandCuts})",
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.16,
    )

    # c.Print(pdf_path)
    c.Print(f"{pdf_path}(")
    ROOT.FSHistogram.clearHistogramCache()

# -------- Missing Mass KSHORT -------------
def missingMassPlots_KShort(pdf_path):
    c = ROOT.TCanvas("c_mass_ks", "c_mass_ks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})",
    )

    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})",
    )
    hBkgNegative = hBkg.Clone("hBkgNegative")
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(#pi^{+}#pi^{-}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 5 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)


    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    integral_ks = integral_between(hData, 0.35, 0.65)
    integral_ksSig = integral_between(hSig, 0.35, 0.65)
    integral_ksBkg = integral_between(hBkg, 0.35, 0.65)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "Ks " "(Integral: " f"{integral_ks:.0f})", "pE"),
            (hSig, "Ks Signal " "(Integral: " f"{integral_ksSig:.0f})", "f"),
            (hBkgNegative, "Ks Background " "(Integral: " f"{integral_ksBkg:.0f})", "f"),
        ],
        notes=["K_{S} sideband study"],

        # --- layout tweaks ---
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.68,
        notes_text_size=0.075,
        notes_step=0.12,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            f"Base cuts: CUT({baseCuts},{sidebandCuts})",
            f"Signal: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"Background: CUT({baseCuts})*CUTSBWT({sidebandCuts})",
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.16,
    )

    # c.Print(pdf_path)
    c.Print(f"{pdf_path}(")
    ROOT.FSHistogram.clearHistogramCache()

# -------- LAMBDA -------------
def massPlots_Lambda(pdf_path):
    c = ROOT.TCanvas("c_mass_ks_lambda", "c_mass_ks_lambda", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})",
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})",
    )
    hBkgNegative = hBkg.Clone("hLambBkgNegative")
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(p#pi^{-}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 2 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)

    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    integral_Lamb = integral_between(hData, 1.08, 1.20)
    integral_LambSig = integral_between(hSig, 1.08, 1.20)
    integral_LambBkg = integral_between(hBkg, 1.08, 1.20)


    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "Lambda " "(Integral: " f"{integral_Lamb:.0f})", "pE"),
            (hSig, "Lambda Signal " "(Integral: " f"{integral_LambSig:.0f})", "f"),
            (hBkgNegative, "Lamb Backgnd " "(Integral: " f"{integral_LambBkg:.0f})", "f"),
        ],
        notes=["#Lambda sideband study"],

        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.68,
        notes_text_size=0.075,
        notes_step=0.12,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            f"Base cuts: CUT({baseCuts},{sidebandCuts})",
            f"Signal: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"Background: CUT({baseCuts})*CUTSBWT({sidebandCuts})",
        ],

        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.16,
    )

    c.Print(pdf_path)
    ROOT.FSHistogram.clearHistogramCache()

# -------- Missing Mass LAMBDA -------------
def missingMassPlots_Lambda(pdf_path):
    c = ROOT.TCanvas("c_mass_ks_lambda", "c_mass_ks_lambda", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    # hData = fs_get_th1(
    #     FND_eventSelectionSkims,
    #     f"MASS({DecayingLambda})",
    #     "(60,1.08,1.20)",
    #     f"CUT({baseCuts},{sidebandCuts})"
    
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET) + MASS(GLUEXBEAM) - MASS({DecayingKShort}) - MASS({PiPlus1})",
        "(60,1.08,1.20)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})",
    )
    # hBkg = fs_get_th1(
    #     FND_eventSelectionSkims,
    #     f"MASS({DecayingLambda})",
    #     "(60,1.08,1.20)",
    #     f"CUT({baseCuts})*CUTSBWT({sidebandCuts})",
    # )
    # hBkgNegative = hBkg.Clone("hLambBkgNegative")
    # hBkgNegative.Scale(-1.0)

    # hData.SetXTitle("MM(Ks#pi^{+}) [GeV/c^{2}]")
    hSig.SetYTitle("Counts / 2 MeV")
    # hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    # hBkgNegative.SetLineColor(ROOT.kBlack)
    # hBkgNegative.SetFillColor(ROOT.kRed)

    # hData.Draw("pE")
    hSig.Draw("pE")
    # hBkgNegative.Draw("hist same")

    # integral_Lamb = integral_between(hData, 1.08, 1.20)
    integral_LambSig = integral_between(hSig, 1.08, 1.20)
    # integral_LambBkg = integral_between(hBkg, 1.08, 1.20)


    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            # (hData, "Lambda " "(Integral: " f"{integral_Lamb:.0f})", "pE"),
            (hSig, "Lambda Signal " "(Integral: " f"{integral_LambSig:.0f})", "f"),
            # (hBkgNegative, "Lamb Backgnd " "(Integral: " f"{integral_LambBkg:.0f})", "f"),
        ],
        notes=["#Missing mass Lambda"],

        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.68,
        notes_text_size=0.075,
        notes_step=0.12,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            f"Base cuts: CUT({baseCuts},{sidebandCuts})",
            f"Signal: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"Background: CUT({baseCuts})*CUTSBWT({sidebandCuts})",
        ],

        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.16,
    )

    c.Print(pdf_path)
    ROOT.FSHistogram.clearHistogramCache()

# ------------------------------------------------------------
# BACKGROUND PLOTS: LAMBDA-PI+
# ------------------------------------------------------------
def massPlots_lambdaPiBackground(pdf_path):
    c = ROOT.TCanvas("c_baryon_bkg", "c_baryon_bkg", 2000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=2, nrows=1, info_frac=0.23)

    # 2D
    p = panels[0]
    p["plot"].cd()
    ROOT.gPad.SetRightMargin(0.16)

    h2 = fs_get_th2(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1}):MASS({DecayingLambda},{PiPlus1})",
        "(80,1.20,3.6,80,0.6,2.5)",
        f"CUT(tRange110,flightLengthKShort,flightLengthLambda)*CUTWT({sidebandCuts})"
    )
    h2.SetXTitle("M(#Lambda#pi^{+}) [GeV/c^{2}]")
    h2.SetYTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    h2.Draw("colz")

    draw_vertical_lines(h2, [2.0, 2.0])


    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[(h2, "Counts", "f")],
        notes=["Baryon background map"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "2D histogram:",
            f"CUT(tRange110,flightLengthKShort,flightLengthLambda)*CUTWT({sidebandCuts})",
            f"Expr: MASS({DecayingKShort},{PiPlus1}):MASS({DecayingLambda},{PiPlus1})",
        ]
    )

    # 1D
    p = panels[1]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda},{PiPlus1})",
        "(80,1.20,3.60)",
        f"CUT(tRange110,flightLengthKShort,flightLengthLambda)*CUTWT({sidebandCuts})"
    )
    h1.SetXTitle("M(#Lambda#pi^{+}) [GeV/c^{2}]")
    h1.SetYTitle("Events")
    h1.SetMinimum(0.0)
    h1.Draw("hist")

    draw_vertical_lines(h1, [2.0, 2.0])

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[(h1, "Data", "l")],
        notes=["Reject #Sigma(1385)", "2.0 < M(#Lambda#pi^{+}) < 4.0"]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "1D histogram:",
            f"CUT(tRange110,flightLengthKShort,flightLengthLambda)*CUTWT({sidebandCuts})",
            f"Expr: MASS({DecayingLambda},{PiPlus1})",
        ]
    )

    c.Print(pdf_path)

# ------------------------------------------------------------
# KSTAR MASS PLOTS -- DATA
# ------------------------------------------------------------
def massPlots_KStar_sidebands(pdf_path):
    c = ROOT.TCanvas("c_kstar_sidebands", "c_kstar_sidebands", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})"
    )
    hBkgNegative = hBkg.Clone("hBkgNegative")
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 40 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)


    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    draw_vertical_lines(hData, [0.8, 1.0], color=ROOT.kRed)


    integral_kStar = integral_between(hData, 0.8, 1.0)
    integral_kStarSig = integral_between(hSig, 0.8, 1.0)
    integral_kStarBkg = integral_between(hBkg, 0.8, 1.0)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "kStar " "(Integral: " f"{integral_kStar:.0f})", "pE"),
            (hSig, "kStar Signal " "(Integral: " f"{integral_kStarSig:.0f})", "f"),
            (hBkgNegative, "kStar background " "(Integral: " f"{integral_kStarBkg:.0f})", "f"),
        ],
        notes=[
            "kStar sideband subtraction study",
            "Selecting K*(892) mass region from",
            "M(Ks #pi^{+}) = (0.8, 1.0) GeV/c^{2}",
        ],

        # new optional controls
        legend_box=(0.48, 0.18, 0.96, 0.84),
        legend_text_size=0.10,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.62,
        notes_text_size=0.12,
        notes_step=0.11,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Data: CUT({baseCuts},{sidebandCuts})",
            f"Signal weight: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"Sideband weight: CUT({baseCuts})*CUTSBWT({sidebandCuts})",
        ],

        # new optional controls
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.68,
        notes_text_size=0.075,
        notes_step=0.16,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")


# ------------------------------------------------------------
# KSTAR MASS PLOTS -- DATA and MONTE CARLO
# ------------------------------------------------------------
def massPlots_KStar_Signal_DATA_and_MC(pdf_path):
    c = ROOT.TCanvas("c_kstar_data_mc", "c_kstar_data_mc", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(100,0.5,2.5)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"

    )
    hMC = fs_get_th1(
        FND_eventSelectionSkims_MC,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(100,0.5,2.5)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )

    integral = integral_between(hData,0.8,1.0)

    hData.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Events")
    hData.SetLineColor(ROOT.kBlack)
    hData.SetLineWidth(2)
    hData.SetMarkerStyle(20)
    hData.SetMarkerSize(0.8)
    hData.SetMinimum(0.0)


    hMC.SetLineColor(ROOT.kRed)
    hMC.SetLineWidth(2)
    hMC.SetMarkerStyle(24)
    hMC.SetMarkerColor(ROOT.kRed)
    hMC.SetMarkerSize(0.8)
    hMC.Scale(0.1)
    hMC.SetMinimum(0.0)

    hData.Draw("pE")
    hMC.Draw("pE same")

    draw_vertical_lines(hData, [0.80, 1.00])

    draw_info_pad(
        p["info_main"],
        f"{file_label(FND_eventSelectionSkims)} / {file_label(FND_eventSelectionSkims_MC)}",
        legend_items=[
            (hData, "Data", "pE"),
            (hMC, "Signal MC (scaled)", "pE"),
        ],
        notes=["Select signal between 0.80 and 1.00 GeV",
               "Integral M(K_{S}#pi^{+}) = [0.8, 1.0][GeV/c^{2}]: " f"{integral:.0f}",
        ]
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Data cuts: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"MC cuts:   CUT({baseCuts})*CUTWT({sidebandCuts})",
        ]
    )

    c.Print(pdf_path)

# ------------------------------------------------------------
# KSTAR MASS PLOTS  -- AMPTOOLS OUTPUTS
# ------------------------------------------------------------
def massPlots_KStar_FIT_RESULTS(pdf_path):
    c = ROOT.TCanvas("c_kstar_data_mc", "c_kstar_data_mc", 1150, 1400)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_signalSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(100,0.5,2.5)",
        f"CUT()"
    )
    integral_data = integral_between(hData, 0.8, 1.0)

    hMC = fs_get_th1(
        FND_signalSkims_MC,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(100,0.5,2.5)",
        f"CUT()"
    )
    integral_data = integral_between(hData, 0.8, 1.0)
    integral_MC = integral_between(hMC, 0.8, 1.0)

    hData.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Events")
    hData.SetLineColor(ROOT.kBlack)
    hData.SetLineWidth(2)
    hData.SetMarkerStyle(20)
    hData.SetMarkerSize(0.8)

    hMC.SetLineColor(ROOT.kRed)
    hMC.SetLineWidth(2)
    hMC.SetMarkerStyle(24)
    hMC.SetMarkerColor(ROOT.kRed)
    hMC.SetMarkerSize(0.8)
    hMC.Scale(0.6)

    hData.Draw("pE")
    hMC.Draw("pE same")

    draw_vertical_lines(hData, [0.80, 1.00])

    draw_info_pad(
        p["info_main"],
        f"{file_label(FND_signalSkims)} / {file_label(FND_signalSkims_MC)}",
        legend_items=[
            (hData, "Data - fit results " "(Integral: " f"{integral_data:.0f})", "pE"),
            (hMC,   "MC - fit results "   "(Integral: " f"{integral_MC:.0f})",   "pE"),
        ],
        notes=[
            "Select signal between",
            "M(K_{S}#pi^{+}) = [0.8, 1.0] GeV/c^{2}",
        ],

        legend_box=(0.45, 0.22, 0.96, 0.84),
        legend_text_size=0.14,

        label_pos=(0.06, 0.90),
        label_size=0.16,

        notes_start_y=0.66,
        notes_text_size=0.18,
        notes_step=0.14,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Data cuts: CUT()",
            "MC cuts: CUT()",
            "These files are already the final signal skims fed to AmpTools.",
        ],

        title_pos=(0.06, 0.88),
        title_size=0.16,

        notes_start_y=0.70,
        notes_text_size=0.12,
        notes_step=0.16,
    )

    c.Print(pdf_path)

# ------------------------------------------------------------
# ANGULAR PLOTS - AMPTOOLS OUTPUTS
# ------------------------------------------------------------

# ---------- cosThetaGJ -----------
def cosThetaGJ_KShort(pdf_path):
    c = ROOT.TCanvas("c_costheta_gj", "c_costheta_gj", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_signalSkims,
        f"GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)",
        "(72,-1.0,1.0)",
        f"CUT(tRange110,rf,KShort,Lambda,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"
    )

    h1.SetXTitle("cos#theta_{GJ}(K_{S})")
    h1.SetYTitle("Counts / bin")
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineWidth(2)
    h1.SetMarkerStyle(20)
    h1.SetMarkerColor(ROOT.kBlack)
    h1.SetMarkerSize(0.8)
    h1.SetMinimum(0.0)
    h1.Draw("E1")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims) + "#bf{ Not acceptance-corrected}",
        legend_items=[(h1, "#bf{pre-fit DATA}", "pE")],
        notes=["Select K*(892)"],

        # --- give more breathing room (only 1 legend entry) ---
        legend_box=(0.55, 0.35, 0.95, 0.80),
        legend_text_size=0.11,

        label_pos=(0.06, 0.90),
        label_size=0.11,

        notes_start_y=0.70,
        notes_text_size=0.085,
        notes_step=0.14,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Histogram cuts: CUT()",
            (0.08, f"Expr: GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)"),
            (0.08, "Selection is already built into the signal skim file."),
        ],

        # --- emphasize clarity for explanation text ---
        title_pos=(0.06, 0.88),
        title_size=0.12,

        notes_start_y=0.72,
        notes_text_size=0.085,
        notes_step=0.17,
    )

    c.Print(pdf_path)


# ------- cosTheta Helicity EVENT SELECTION SKIMMED TREES --------
def cosThetaHelicity_KShort_eventSelectionSkim(pdf_path):
    c = ROOT.TCanvas("c_costheta_hel_data", "c_costheta_hel_data", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h = fs_get_th1(
        FND_eventSelectionSkims,
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};{DecayingLambda})",
        "(36,-1.0,1.0)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)*CUTWT(rf,KShort,Lambda)"
    )

    # AMPTOOLS SKIM CUTS:
    # generalCuts: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)
    # signalCuts: CUT(rf,KShort,Lambda)
    # sidebandWeights: CUTSBWT(rf,KShort,Lambda)

    # PLOTTING SKIM CUTS:
    # generalCuts_eventSelection: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)
    # histogram cuts: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort,Lambda)*CUTSBWT(rf,KShort,Lambda)

    integral = integral_between(h,-1.0,0.5)

    h.SetXTitle("cos#theta_{Helicity}(K_{S})")
    h.SetYTitle("10 degrees / bin")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("E1")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims) + "#bf{ (Not acceptance-corrected)}",
        legend_items=[(h, "event selection skim", "pE")],
        notes=[
            "#bf{Integral (-1.0, 1.0): }" f"{integral:.0f}",
            "NO sideband subtraction",
        ],

        # --- layout ---
        legend_box=(0.55, 0.32, 0.95, 0.80),
        legend_text_size=0.16,

        label_pos=(0.06, 0.90),
        label_size=0.14,

        notes_start_y=0.66,
        notes_text_size=0.16,
        notes_step=0.13,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used:",
        notes=[
            (0.08, "General Cuts: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ"),
            (0.12, "Histogram cuts: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.12, "Histogram cuts: &&CUT(rf,KShort,Lambda)*CUTSBWT(rf,KShort,Lambda)"),
        ],

        # --- bottom pad ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.15,
    )

    # c.Print(pdf_path)
    c.Print(f"{pdf_path}(")


# ------- cosTheta Helicity AMPTOOLS INPUT FILE --------
def cosThetaHelicity_KShort_ampToolsSkim(pdf_path):
    c = ROOT.TCanvas("c_costheta_hel_data", "c_costheta_hel_data", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h = fs_get_th1(
        FND_signalSkims,
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};{DecayingLambda})",
        "(36,-1.0,1.0)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)&&CUT(rf,KShort,Lambda)*CUTSBWT(rf,KShort,Lambda)"
    )

    integral = integral_between(h,-1.0,0.5)

    h.SetXTitle("cos#theta_{Helicity}(K_{S})")
    h.SetYTitle("10 degrees / bin")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("E1")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims) + "#bf{ (Not acceptance-corrected)}",
        legend_items=[(h, "amptools input file", "pE")],
        notes=[
            "#bf{Integral (-1.0, 1.0): }" f"{integral:.0f}",
            "NO sideband subtraction",
        ],

        # --- layout ---
        legend_box=(0.55, 0.32, 0.95, 0.80),
        legend_text_size=0.16,

        label_pos=(0.06, 0.90),
        label_size=0.14,

        notes_start_y=0.66,
        notes_text_size=0.16,
        notes_step=0.13,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used:",
        notes=[
            (0.08, "General Cuts: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,"),
            (0.10, "flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.12, "Signal cuts: CUT(rf,KShort,Lambda)"),
            (0.12, "Histogram cuts: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,"),
            (0.12, "selectKSTAR892)&&CUT(rf,KShort,Lambda)*CUTSBWT(rf,KShort,Lambda)"),
        ],

        # --- bottom pad ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.15,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")



# ------- cosTheta vs Lambda Pi EVENT SELECTION SKIM --------
def cosTheta_vs_lambdaPi_eventSelection(pdf_path):
    c = ROOT.TCanvas("c_costheta_hel_data", "c_costheta_hel_data", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h = fs_get_th2(
        FND_eventSelectionSkims,
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM):MASS({DecayingLambda},{PiPlus1})",
        "(36, 1.20,3.60, 36,-1.0,1.0)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort,Lambda)"
    )

    # integral = integral_between(h,-1.0,0.5)

    h.SetXTitle("M(#Lambda#pi^{+}) [GeV/c^{2}]")
    h.SetYTitle("cos#theta_{Helicity}(K_{S})")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("colz")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims) + "#bf{ (Not acceptance-corrected)}",
        legend_items=[(h, "Event Selection DATA", "")],
        notes=[
            # "#bf{Integral (-1.0, 0.5): }" f"{integral:.0f}",
            "NO sideband subtraction",
        ],

        # --- layout ---
        legend_box=(0.55, 0.32, 0.95, 0.80),
        legend_text_size=0.16,

        label_pos=(0.06, 0.90),
        label_size=0.14,

        notes_start_y=0.66,
        notes_text_size=0.16,
        notes_step=0.13,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.08, "General Cuts: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"),
            (0.10, "Histogram cuts:CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort,Lambda)"),
        ],

        # --- bottom pad ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.15,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")




# ------- cosTheta vs Lambda Pi AMPTOOLS SKIM --------
def cosTheta_vs_lambdaPi_ampToolsSkim(pdf_path):
    c = ROOT.TCanvas("c_costheta_hel_data", "c_costheta_hel_data", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h = fs_get_th2(
        FND_signalSkims,
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM):MASS({DecayingLambda},{PiPlus1})",
        "(36, 1.20,3.60, 36,-1.0,1.0)",
        f"CUT()"
    )

    # integral = integral_between(h,-1.0,0.5)

    h.SetXTitle("M(#Lambda#pi^{+}) [GeV/c^{2}]")
    h.SetYTitle("cos#theta_{Helicity}(K_{S})")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("colz")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims) + "#bf{ (Not acceptance-corrected)}",
        legend_items=[(h, "AmpTools input file", "")],
        notes=[
            # "#bf{Integral (-1.0, 0.5): }" f"{integral:.0f}",
            "NO sideband subtraction",
        ],

        # --- layout ---
        legend_box=(0.55, 0.32, 0.95, 0.80),
        legend_text_size=0.16,

        label_pos=(0.06, 0.90),
        label_size=0.14,

        notes_start_y=0.66,
        notes_text_size=0.16,
        notes_step=0.13,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used in skim (no actual cuts applied in histogram!)",
        notes=[
            (0.08, "General Cuts: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ,"),
            (0.10, "flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.12, "Signal cuts: CUT(rf,KShort,Lambda)"),
        ],

        # --- bottom pad ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.15,
    )

    # c.Print(pdf_path)
    c.Print(f"{pdf_path})")


# ------- cosTheta Helicity MC --------
def cosThetaHelicity_KShort_MC(pdf_path):
    c = ROOT.TCanvas("c_costheta_hel_mc", "c_costheta_hel_mc", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h = fs_get_th1(
        FND_signalSkims_MC,
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)",
        "(36,-1.0,1.0)",
        f"CUT(tRange110,rf,KShort,Lambda,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"
    )

    integral = integral_between(h,-1.0,1.0)

    h.SetXTitle("cos#theta_{Helicity}(K_{S})")
    h.SetYTitle("10 degrees / bin")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlue + 1)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlue + 1)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("E1")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims_MC),
        legend_items=[(h, "#bf{pre-fit MC}", "pE")],
        notes=[
            "#bf{Integral (-1.0, 1.0): }" f"{integral:.0f}",
            "Accepted MC helicity distribution",
        ],

        legend_box=(0.55, 0.32, 0.95, 0.80),
        legend_text_size=0.11,

        label_pos=(0.06, 0.90),
        label_size=0.11,

        notes_start_y=0.66,
        notes_text_size=0.080,
        notes_step=0.13,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"General cuts: {generalCuts}",
            "Histogram cuts:",
            (0.08, "CUT(tRange110,rf,KShort,Lambda,flightLengthKShort,flightLengthLambda,"),
            (0.10, "rejectSigma1385,selectKSTAR892)"),
        ],

        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.15,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")



# ------- EFFICIENCY: cosTheta Helicity --------
def efficiency_cosThetaHelicity_KShort(pdf_path):
    c = ROOT.TCanvas("c_eff_costheta_hel", "c_eff_costheta_hel", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h_accmc = fs_get_th1(
        FND_signalSkims_MC,
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)",
        "(36,-1.0,1.0)",
        f"CUT(tRange110,rf,KShort,Lambda,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"
    )

    hel_expr_thrown = (
        "FSMath::helcostheta("
        "MCPxP2,MCPyP2,MCPzP2,MCEnP2,"
        "MCPxP3,MCPyP3,MCPzP3,MCEnP3,"
        "MCPxPB,MCPyPB,MCPzPB,MCEnPB)"
    )

    h_genmc = fs_get_th1(
        FND_signalSkims_MC_THROWN,
        hel_expr_thrown,
        "(36,-1.0,1.0)",
        "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"
    )

    h_efficiency = h_accmc.Clone("h_eff_costheta_hel")
    keep(h_efficiency)
    h_efficiency.Divide(h_genmc)

    h_efficiency.SetXTitle("cos#theta_{Helicity}(K_{S})")
    h_efficiency.SetYTitle("Efficiency")
    h_efficiency.SetLineColor(ROOT.kBlue)
    h_efficiency.SetLineWidth(2)
    h_efficiency.SetMarkerStyle(20)
    h_efficiency.SetMarkerColor(ROOT.kBlack)
    h_efficiency.SetMarkerSize(0.8)
    h_efficiency.GetYaxis().SetNoExponent(True)
    h_efficiency.GetYaxis().SetNdivisions(505)
    h_efficiency.SetMinimum(0.0)
    h_efficiency.SetMaximum(0.01)
    h_efficiency.Draw("pE")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims_MC),
        legend_items=[(h_efficiency, "accmc/genmc", "pE")],
        notes=[
            "Efficiency = accepted MC / thrown MC",
            "Helicity angle for K_{S}",
        ],

        # --- layout ---
        legend_box=(0.55, 0.40, 0.95, 0.80),
        legend_text_size=0.16,

        label_pos=(0.06, 0.90),
        label_size=0.11,

        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.14,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Accepted MC:",
            (0.08, "CUT(tRange110,rf,KShort,Lambda,flightLengthKShort,flightLengthLambda,"),
            (0.10, "rejectSigma1385,selectKSTAR892)*CUTWT(rf,KShort,Lambda)"),
            "",
            "Thrown MC:",
            (0.08, "CUT(tRangeTHROWN,coherentPeakTHROWN,selectKSTAR892THROWN)"),
        ],

        # --- bottom pad ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.15,
    )

    c.Print(f"{pdf_path})")

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
def main():
    t0 = time.time()

    os.makedirs("plots", exist_ok=True)

    gluex_style()
    setup()
    setup_genmc()

    # global_eventSelection_Cuts(allPlots)
    # massPlots_KShort_cutComparisons(allPlots)
    # massPlots_KShort(allPlots)
    # missingMassPlots_KShort(allPlots)
    # massPlots_Lambda(allPlots)
    # missingMassPlots_Lambda(allPlots)
    # massPlots_lambdaPiBackground(allPlots)
    # massPlots_KStar_sidebands(allPlots)
    # massPlots_KStar_Signal_DATA_and_MC(allPlots)
    # massPlots_KStar_FIT_RESULTS(allPlots)
    # cosThetaGJ_KShort(allPlots)
    cosThetaHelicity_KShort_eventSelectionSkim(allPlots)
    cosThetaHelicity_KShort_ampToolsSkim(allPlots)
    cosTheta_vs_lambdaPi_eventSelection(allPlots)
    cosTheta_vs_lambdaPi_ampToolsSkim(allPlots)
    # cosThetaHelicity_KShort_MC(allPlots)
    # efficiency_cosThetaHelicity_KShort(allPlots)

    dt = time.time() - t0
    print(f"Total execution time: {dt:.1f} s")


if __name__ == "__main__":
    main()