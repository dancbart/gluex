import os
import time
import ROOT

ROOT.gROOT.SetBatch(True)

from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

ROOT.TGaxis.SetMaxDigits(3)
# for loading histograms and fits into KStar RooFit function(s)
# ROOT.gSystem.Load("libRooFit")
# ROOT.gSystem.Load("libRooFitCore")

#used in helper function that dumps fit results to log file
logFile = "plots/plotEventSelection.txt"

# ------------------------------------------------------------
# Files / globals
# ------------------------------------------------------------

# ------ Fit results histogram(s) for K Pi system

FND_fits = "/work/halld/home/dbarton/gluex/KShortPipLambda/fitting/plots/plots_rooFit_kStar.root"

# ------ Use to plot variables used as 'global' cuts (beam energy, unused shower, etc).  These are unskimmed files. ---------------------
FND_unSkimmed = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sp18fa18sp20_40856_73266_allPols.root"
FND_unSkimmed_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"
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

    ROOT.FSCut.defineCut("tprimeKsLow", "TPRIMEKS > 0.0 && TPRIMEKS < 0.2")
    ROOT.FSCut.defineCut("tprimeKsMid", "TPRIMEKS > 0.2 && TPRIMEKS < 0.6")
    ROOT.FSCut.defineCut("tprimeKsHigh", "TPRIMEKS > 0.6 && TPRIMEKS < 1.0")
    
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
    # use this cut to select "outside" the Lambda window to check for "non-lambda K*'s.  Purpose: understand K* background."
    ROOT.FSCut.defineCut("nonLambda", "MASS(1a,1b)>1.14 && MASS(1a,1b)<1.675")
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
generalCuts_eventSelection = "CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"
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
# Fit helper functions
# ------------------------------------------------------------

def make_breit_wigner(name, xmin, xmax,
                      amp=None, mean=None, width=None):
    """
    Breit-Wigner signal: breitwigner(0)
    ROOT convention: [0]=amplitude, [1]=mean, [2]=width
    """
    f = ROOT.TF1(name, "breitwigner(0)", xmin, xmax)

    f.SetParameter(0, amp   if amp   is not None else 1000.0)
    f.SetParameter(1, mean  if mean  is not None else (xmin + xmax) / 2.0)
    f.SetParameter(2, width if width is not None else 0.010)

    keep(f)
    return f


def make_expo2(name, xmin, xmax,
               p0=None, p1=None, p2=None):
    """Background: exp(p0 + p1*x + p2*x^2)"""
    f = ROOT.TF1(name, "TMath::Exp([0] + [1]*x + [2]*x*x)", xmin, xmax)

    f.SetParName(0, "expo_p0")
    f.SetParName(1, "expo_p1")
    f.SetParName(2, "expo_p2")

    f.SetParameter(0, p0 if p0 is not None else  0.0)
    f.SetParameter(1, p1 if p1 is not None else  1.0)
    f.SetParameter(2, p2 if p2 is not None else  0.0)

    keep(f)
    return f


def make_voigtian(name, xmin, xmax,
                  amp=None, mean=None, sigma=None, width=None):
    """
    Signal: amp * Voigt(x - mean, sigma, width)

    sigma = Gaussian detector resolution
    width = Lorentzian/natural width
    Ref: https://root.cern.ch/root/html524/TMath.html#TMath:Voigt
    """
    f = ROOT.TF1(name, "[0]*TMath::Voigt(x - [1], [2], [3])", xmin, xmax)

    f.SetParName(0, "voigt_amp")
    f.SetParName(1, "voigt_mean")
    f.SetParName(2, "voigt_sigma")
    f.SetParName(3, "voigt_width")

    f.SetParameter(0, amp   if amp   is not None else 1000.0)
    f.SetParameter(1, mean  if mean  is not None else (xmin + xmax) / 2.0)
    f.SetParameter(2, sigma if sigma is not None else 0.005)
    f.SetParameter(3, width if width is not None else 0.005)

    keep(f)
    return f


def make_voigtian_plus_expo2(name, xmin, xmax,
                              amp=None, mean=None, sigma=None, width=None,
                              p0=None, p1=None, p2=None):
    f = ROOT.TF1(name, "[0]*TMath::Voigt(x - [1], [2], [3]) + TMath::Exp([4] + [5]*x + [6]*x*x)", xmin, xmax)
    
    # Initialize with generic defaults.  Change when calling function.
    f.SetParameter(0, amp   if amp   is not None else 1.0)
    f.SetParameter(1, mean  if mean  is not None else (xmin + xmax) / 2.0)
    f.SetParameter(2, sigma if sigma is not None else 1.0)
    f.SetParameter(3, width if width is not None else 1.0)
    f.SetParameter(4, p0    if p0    is not None else 1.0)
    f.SetParameter(5, p1    if p1    is not None else 1.0)
    f.SetParameter(6, p2    if p2    is not None else 1.0)

    keep(f)
    return f

def make_bernstein(name, xmin, xmax, degree=3,
                   coeffs=None):
    """
    Bernstein polynomial background of given degree.
    Rescales x to [0,1] over [xmin, xmax], matching RooBernstein convention.
    Parameters [0..degree] are the Bernstein coefficients c_i.

    PDF(x) = sum_{i=0}^{n} c_i * B(n,i) * t^i * (1-t)^(n-i)
    where t = (x - xmin) / (xmax - xmin)
    """
    # Build the formula string term by term
    t = f"(x - {xmin}) / ({xmax} - {xmin})"   # rescaled variable
    terms = []
    for i in range(degree + 1):
        binom = int(__import__('math').comb(degree, i))
        term = f"[{i}] * {binom} * pow({t}, {i}) * pow(1 - ({t}), {degree - i})"
        terms.append(term)
    formula = " + ".join(terms)

    f = ROOT.TF1(name, formula, xmin, xmax)

    defaults = coeffs if coeffs is not None else [1.0] * (degree + 1)
    for i, val in enumerate(defaults):
        f.SetParName(i, f"bern_c{i}")
        f.SetParameter(i, val)

    keep(f)
    return f

# for plotting K* stuff
def make_two_voigtians_plus_bernstein(name, xmin, xmax, bern_degree=3,
                                      amp1=None, mean1=None, sigma1=None, width1=None,
                                      amp2=None, mean2=None, sigma2=None, width2=None,
                                      coeffs=None):
    """
    Two Voigtians + Bernstein polynomial background.

    Parameter layout:
        [0]  voigt1_amp
        [1]  voigt1_mean
        [2]  voigt1_sigma
        [3]  voigt1_width
        [4]  voigt2_amp
        [5]  voigt2_mean
        [6]  voigt2_sigma
        [7]  voigt2_width
        [8 .. 8+bern_degree]  Bernstein coefficients
    """
    import math

    t = f"(x - {xmin}) / ({xmax} - {xmin})"
    bern_terms = []
    for i in range(bern_degree + 1):
        par_idx = 8 + i
        binom = int(math.comb(bern_degree, i))
        term = f"[{par_idx}] * {binom} * pow({t}, {i}) * pow(1 - ({t}), {bern_degree - i})"
        bern_terms.append(term)
    bern_formula = " + ".join(bern_terms)

    formula = (
        "[0]*TMath::Voigt(x - [1], [2], [3]) + "
        "[4]*TMath::Voigt(x - [5], [6], [7]) + "
        + bern_formula
    )

    f = ROOT.TF1(name, formula, xmin, xmax)

    # --- Voigtian 1 (K*(892))
    f.SetParName(0, "voigt1_amp");   f.SetParameter(0, amp1   if amp1   is not None else 1000.0)
    f.SetParName(1, "voigt1_mean");  f.SetParameter(1, mean1  if mean1  is not None else 0.892)
    f.SetParName(2, "voigt1_sigma"); f.SetParameter(2, sigma1 if sigma1 is not None else 0.005)
    f.SetParName(3, "voigt1_width"); f.SetParameter(3, width1 if width1 is not None else 0.050)

    # --- Voigtian 2 (K*(1430) or whatever second peak you're fitting)
    f.SetParName(4, "voigt2_amp");   f.SetParameter(4, amp2   if amp2   is not None else 500.0)
    f.SetParName(5, "voigt2_mean");  f.SetParameter(5, mean2  if mean2  is not None else 1.43)
    f.SetParName(6, "voigt2_sigma"); f.SetParameter(6, sigma2 if sigma2 is not None else 0.005)
    f.SetParName(7, "voigt2_width"); f.SetParameter(7, width2 if width2 is not None else 0.100)

    # --- Bernstein coefficients
    defaults = coeffs if coeffs is not None else [1.0] * (bern_degree + 1)
    for i, val in enumerate(defaults):
        f.SetParName(8 + i, f"bern_c{i}")
        f.SetParameter(8 + i, val)

    keep(f)
    return f

# for drawing the individual functions for the overall K* fit function
def make_component_funcs_kstar(f, xmin, xmax, bern_degree=3):
    """
    Extract drawable TF1 components from two_voigtians_plus_bernstein.
    Returns (f_voigt1, f_voigt2, f_bern)
    """
    import math

    f_voigt1 = ROOT.TF1(f"{f.GetName()}_voigt1",
                        "[0]*TMath::Voigt(x - [1], [2], [3])", xmin, xmax)
    for i in range(4):
        f_voigt1.SetParameter(i, f.GetParameter(i))

    f_voigt2 = ROOT.TF1(f"{f.GetName()}_voigt2",
                        "[0]*TMath::Voigt(x - [1], [2], [3])", xmin, xmax)
    for i in range(4):
        f_voigt2.SetParameter(i, f.GetParameter(i + 4))

    t = f"(x - {xmin}) / ({xmax} - {xmin})"
    terms = []
    for i in range(bern_degree + 1):
        binom = int(math.comb(bern_degree, i))
        terms.append(f"[{i}] * {binom} * pow({t}, {i}) * pow(1 - ({t}), {bern_degree - i})")
    f_bern = ROOT.TF1(f"{f.GetName()}_bern", " + ".join(terms), xmin, xmax)
    for i in range(bern_degree + 1):
        f_bern.SetParameter(i, f.GetParameter(i + 8))

    keep(f_voigt1)
    keep(f_voigt2)
    keep(f_bern)
    return f_voigt1, f_voigt2, f_bern

# ------------------------------------------------------------
# Calculate figures of merit for voigt1, voigt2 and Bernstein polynomial
# ------------------------------------------------------------

def fit_integral_voigt1(f, xmin, xmax, bin_width=1.0, name=None):
    """Extract first Voigtian component from two_voigtians_plus_bernstein. Params [0-3]."""
    if name is None:
        name = f"f_voigt1_{f.GetName()}"
    f_v = ROOT.TF1(name, "[0]*TMath::Voigt(x - [1], [2], [3])", xmin, xmax)
    for i in range(4):
        f_v.SetParameter(i, f.GetParameter(i))
    keep(f_v)
    return f_v.Integral(xmin, xmax, 1e-6) / bin_width


def fit_integral_voigt2(f, xmin, xmax, bin_width=1.0, name=None):
    """Extract second Voigtian component from two_voigtians_plus_bernstein. Params [4-7]."""
    if name is None:
        name = f"f_voigt2_{f.GetName()}"
    f_v = ROOT.TF1(name, "[0]*TMath::Voigt(x - [1], [2], [3])", xmin, xmax)
    for i in range(4):
        f_v.SetParameter(i, f.GetParameter(i + 4))
    keep(f_v)
    return f_v.Integral(xmin, xmax, 1e-6) / bin_width


def fit_integral_bernstein(f, xmin, xmax, bin_width=1.0, bern_degree=3, name=None):
    """Extract Bernstein component from two_voigtians_plus_bernstein. Params [8..]."""
    import math
    if name is None:
        name = f"f_bern_{f.GetName()}"
    t = f"(x - {xmin}) / ({xmax} - {xmin})"
    terms = []
    for i in range(bern_degree + 1):
        binom = int(math.comb(bern_degree, i))
        terms.append(f"[{i}] * {binom} * pow({t}, {i}) * pow(1 - ({t}), {bern_degree - i})")
    f_b = ROOT.TF1(name, " + ".join(terms), xmin, xmax)
    for i in range(bern_degree + 1):
        f_b.SetParameter(i, f.GetParameter(i + 8))
    keep(f_b)
    return f_b.Integral(xmin, xmax, 1e-6) / bin_width


def compute_figureOfMerit_kstar(f, xmin, xmax, bin_width=1.0, bern_degree=3):
    """
    Figure of merit for two_voigtians_plus_bernstein.
    Signal = voigt1 + voigt2, Background = Bernstein.
    """
    S1 = fit_integral_voigt1(f, xmin, xmax, bin_width=bin_width)
    S2 = fit_integral_voigt2(f, xmin, xmax, bin_width=bin_width)
    S  = S1 + S2
    B  = fit_integral_bernstein(f, xmin, xmax, bin_width=bin_width, bern_degree=bern_degree)

    SB           = S / B if B > 0 else 0.0
    significance = S / (S + B)**0.5 if (S + B) > 0 else 0.0
    purity       = S / (S + B) if (S + B) > 0 else 0.0

    return S1, S2, S, B, SB, significance, purity

# ------------------------------------------------------------
# Functions to plot signal and background lines individually
# ------------------------------------------------------------

def make_component_funcs(f, xmin, xmax):
    """
    Extract Voigtian and Expo2 components from a combined fit TF1.
    Parameters: [0-3] = Voigtian, [4-6] = Expo2
    """
    f_voigt = ROOT.TF1(
        f"{f.GetName()}_voigt",
        "[0]*TMath::Voigt(x - [1], [2], [3])",
        xmin, xmax
    )
    for i in range(4):
        f_voigt.SetParameter(i, f.GetParameter(i))

    f_expo2 = ROOT.TF1(
        f"{f.GetName()}_expo2",
        "TMath::Exp([0] + [1]*x + [2]*x*x)",
        xmin, xmax
    )
    for i in range(3):
        f_expo2.SetParameter(i, f.GetParameter(i + 4))  # offset by 4

    keep(f_voigt)
    keep(f_expo2)
    return f_voigt, f_expo2

# ------------------------------------------------------------
# Fit integral helpers (signal & background)
# ------------------------------------------------------------

def fit_integral_signal(f, xmin, xmax, bin_width=1.0, name=None):
    """
    Signal yield from Voigtian component of combined fit.
    Assumes [0-3] = Voigtian.
    """
    if name is None:
        name = f"f_sig_{f.GetName()}"

    f_sig = ROOT.TF1(
        name,
        "[0]*TMath::Voigt(x - [1], [2], [3])",
        xmin,
        xmax
    )

    for i in range(4):
        f_sig.SetParameter(i, f.GetParameter(i))

    keep(f_sig)
    result = f_sig.Integral(xmin, xmax, 1e-6) / bin_width
    return result


def fit_integral_background(f, xmin, xmax, bin_width=1.0, name=None):
    """
    Background yield from exponential component of combined fit.
    Assumes [4-6] = exponential.
    """
    if name is None:
        name = f"f_bkg_{f.GetName()}"

    f_bkg = ROOT.TF1(
        name,
        "TMath::Exp([0] + [1]*x + [2]*x*x)",
        xmin,
        xmax
    )

    for i in range(3):
        f_bkg.SetParameter(i, f.GetParameter(i + 4))

    keep(f_bkg)
    result =  f_bkg.Integral(xmin, xmax, 1e-6) / bin_width
    return result


def compute_figureOfMerit(f, xmin, xmax, bin_width=1.0):
    """
    Compute fitted signal, fitted background, S/B, and S/sqrt(S+B)
    over the selected mass window.
    """
    S = fit_integral_signal(f, xmin, xmax, bin_width=bin_width)
    B = fit_integral_background(f, xmin, xmax, bin_width=bin_width)

    SB = S / B if B > 0 else 0.0
    significance = S / (S + B)**0.5 if (S + B) > 0 else 0.0
    purity = S / (S + B)

    return S, B, SB, significance, purity


# ------------------------------------------------------------
# Create Log file from fit restults
# ------------------------------------------------------------
def log_fit_results(f, hist_name, cut_string, xmin, xmax, notes=None):
    """
    Append fit results for a given TF1 to the running log file.
    Call this after any Fit() call.
    
    Args:
        f:           the TF1 after fitting
        hist_name:   string identifying the histogram (e.g. "hData_FLoff")
        cut_string:  the FSRoot cut string used to fill the histogram
        xmin, xmax:  integration/fit range
        notes:       optional list of extra strings to append
    """
    import datetime

    lines = []
    lines.append("=" * 70)
    lines.append(f"Timestamp:    {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Fit function: {f.GetName()}")
    lines.append(f"Histogram:    {hist_name}")
    lines.append(f"Cut string:   {cut_string}")
    lines.append(f"Fit range:    ({xmin}, {xmax})")
    lines.append(f"Chi2 / NDF:   {f.GetChisquare():.4f} / {f.GetNDF()} = {f.GetChisquare() / f.GetNDF() if f.GetNDF() > 0 else float('nan'):.4f}")
    lines.append(f"Fit status:   {int(f.GetParError(0) > 0)}")  # rough proxy: errors defined = converged
    lines.append("Parameters:")
    for i in range(f.GetNpar()):
        lines.append(f"  [{i}] {f.GetParName(i):<20s} = {f.GetParameter(i):>14.6f} +/- {f.GetParError(i):.6f}")
    if notes:
        lines.append("Notes:")
        for note in notes:
            lines.append(f"  {note}")
    lines.append("")  # blank line between entries

    with open(logFile, "a") as fout:
        fout.write("\n".join(lines) + "\n")

# ------------------------------------------------------------
# Calculate Figures of Merit for RooFit K* plot 
# (which imports histogram and fit values from outside function)
# ------------------------------------------------------------
def vecs_to_tgraph(f, xname, yname, name):
    vx = f.Get(xname)
    vy = f.Get(yname)
    if not vx or not vy:
        return None
    n = vx.GetNoElements()
    import array
    xs = array.array('d', [vx[i] for i in range(n)])
    ys = array.array('d', [vy[i] for i in range(n)])
    g = ROOT.TGraph(n, xs, ys)
    g.SetName(name)
    keep(g)
    return g


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

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_eventSelectionSkims,
        "EnUnusedSh",
        "(100,0.06,1.0)",
        "CUT()"
    )
    h1.SetXTitle("Unused shower energy [GeV]")
    h1.SetYTitle("Combos")
    h1.SetLineColor(ROOT.kBlack)

    h1b = fs_get_th1(
        FND_eventSelectionSkims_MC,
        "EnUnusedSh",
        "(100,0.06,1.0)",
        "CUT()"
    )
    h1b.SetXTitle("Unused shower energy [GeV]")
    h1b.SetYTitle("Combos")
    h1b.SetLineColor(ROOT.kBlack)
    h1b.SetFillColor(ROOT.kBlue)

    integral_data = integral_between(h1, 0.1, 1.0)
    integral_MC_raw   = integral_between(h1b, 0.1, 1.0)
    if integral_MC_raw > 0:
        scaleFactor = integral_data / integral_MC_raw
        h1b.Scale(scaleFactor)
    else:
        print("WARNING: MC integral is zero, not scaling")
    integral_MC_scaled = integral_between(h1b, 0.1, 1.0)

    # after scaling
    h1b.SetMinimum(0.5)
    h1.SetMinimum(0.5)

    h1b.Draw("hist")
    h1.Draw("pE same")   # use E1 instead of pE for safer error bars

    # p["plot"].SetLogy(1)
    p["plot"].Modified()
    p["plot"].Update()


    if bggen:
        draw_mc_same(
            FND_unSkimmed, "EnUnusedSh", "(100,0.0,1.0)",
            "CUT()"
        )

    draw_info_pad(
        p["info_main"],
        "#bf{No cut applied on this variable.}",
        legend_items=[(h1, "Data " "(integral: " f"{integral_data:.0f})", "pE"),
                      (h1b, f"MC scaled (raw: {integral_MC_raw:.0f} -> scaled: {integral_MC_scaled:.0f})", "f"),
                      ],
        # notes=["Cut: E_{unused} < 0.1 GeV", "log scale"],
        notes=["Unused Shower Energy",
                # "Log scale",
               "Integral between (0.1, 1.0)"
               ],
        
        # middle pad tweaks
        legend_box=(0.33, 0.18, 0.96, 0.84),
        legend_text_size=0.12,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.62,
        notes_text_size=0.12,
        notes_step=0.13,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            "Global cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)",
            "Histogram cuts: none",
            "#bf{Notes:} Signal MC in good agreement with DATA.  Therefore, it is ",
            "unlikely events from #it{Unused shower energy} are wrong topology.",
            "#bf{Further Study:} consider generating background MC with different",
             "topology (i.e. an extra #pi^{0}, etc.) and compare #it{that} to data.",
        ],

        # bottom pad tweaks
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.10,
        notes_step=0.12,

    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")


    # # ============================================================
    # # Page 2: Production vertex z
    # # ============================================================
    # c = ROOT.TCanvas("c_eventCuts_targetZ", "c_eventCuts_targetZ", 1000, 1300)
    # keep(c)

    # panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    # p = panels[0]
    # p["plot"].cd()
    # ROOT.gPad.SetLogy(False)

    # h2 = fs_get_th1(
    #     FND_unSkimmed,
    #     "ProdVz",
    #     "(100,0.,100.0)",
    #     "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)"
    # )
    # h2.SetXTitle("Production vertex z-position [cm]")
    # h2.SetYTitle("Events")
    # h2.Draw("hist")

    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed, "ProdVz", "(100,0.,100.0)",
    #         "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)"
    #     )
    # draw_vertical_lines(h2, [52.0, 78.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h2, "Data", "l")],
    #     notes=["Cut: 52 < V_{z} < 78 cm"],

    #     # --- layout tweaks ---
    #     legend_box=(0.44, 0.22, 0.96, 0.84),
    #     legend_text_size=0.13,

    #     label_pos=(0.06, 0.90),
    #     label_size=0.16,

    #     notes_start_y=0.68,
    #     notes_text_size=0.16,
    #     notes_step=0.08,


    # )
    # draw_notes_pad(
    #     p["info_notes"],
    #     title="Cuts used",
    #     notes=[
    #         "Histogram cuts:",
    #         "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,coherentPeak)",
    #         "Plotted variable: ProdVz",
    #     ],

    #     # --- bottom pad tweaks ---
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.75,
    #     notes_text_size=0.08,
    #     notes_step=0.10,

    # )

    # c.Print(pdf_path)


    # # ============================================================
    # # Page 3: t-range
    # # ============================================================
    # c = ROOT.TCanvas("c_eventCuts_tRange", "c_eventCuts_tRange", 1000, 1300)
    # keep(c)

    # panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    # p = panels[0]
    # p["plot"].cd()

    # h3 = fs_get_th1(
    #     FND_unSkimmed,
    #     f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
    #     "(100,0,2)",
    #     "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"
    # )
    # h3.SetXTitle("|-t| [GeV^{2}]")
    # h3.SetYTitle("Events")
    # h3.Draw("hist")

    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed,
    #         f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
    #         "(100,0,2)",
    #         "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"
    #     )
    # draw_vertical_lines(h3, [0.1, 1.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h3, "Data", "l")],
    #     notes=["Cut: 0.1 < |-t| < 1.0"],

    #     # --- layout tweaks ---
    #     legend_box=(0.44, 0.22, 0.96, 0.84),
    #     legend_text_size=0.13,

    #     label_pos=(0.06, 0.90),
    #     label_size=0.16,

    #     notes_start_y=0.68,
    #     notes_text_size=0.16,
    #     notes_step=0.08,

    # )
    # draw_notes_pad(
    #     p["info_notes"],
    #     title="Cuts used",
    #     notes=[
    #         "Histogram cuts:",
    #         "CUT(rf,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)",
    #         f"Plotted variable: abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
    #     ],

    #     # --- bottom pad tweaks ---
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.75,
    #     notes_text_size=0.08,
    #     notes_step=0.10,

    # )

    # c.Print(pdf_path)


    # # ============================================================
    # # Page 4: Beam energy / coherent peak
    # # ============================================================
    # c = ROOT.TCanvas("c_eventCuts_beamE", "c_eventCuts_beamE", 1000, 1300)
    # keep(c)

    # panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    # p = panels[0]
    # p["plot"].cd()

    # h4 = fs_get_th1(
    #     FND_unSkimmed,
    #     "EnPB",
    #     "(125,5,12)",
    #     "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,targetZ)"
    # )
    # h4.SetXTitle("E_{beam} [GeV]")
    # h4.SetYTitle("Events")
    # h4.Draw("hist")

    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed, "EnPB", "(125,5,12)",
    #         "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,targetZ)"
    #     )
    # draw_vertical_lines(h4, [8.2, 8.6])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h4, "Data", "l")],
    #     notes=["Coherent peak", "8.2 < E_{beam} < 8.6 GeV"],

    #     # --- layout tweaks ---
    #     legend_box=(0.44, 0.22, 0.96, 0.84),
    #     legend_text_size=0.13,

    #     label_pos=(0.06, 0.90),
    #     label_size=0.16,

    #     notes_start_y=0.68,
    #     notes_text_size=0.16,
    #     notes_step=0.08,

    # )
    # draw_notes_pad(
    #     p["info_notes"],
    #     title="Cuts used",
    #     notes=[
    #         "Histogram cuts:",
    #         "CUT(tRange110,rf,chi2DOF,unusedE,unusedTracks,targetZ)",
    #         "Plotted variable: EnPB",
    #     ],

    #     # --- bottom pad tweaks ---
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.75,
    #     notes_text_size=0.08,
    #     notes_step=0.10,

    # )

    # c.Print(pdf_path)


    # # ============================================================
    # # Page 5: chi2/dof
    # # ============================================================
    # c = ROOT.TCanvas("c_eventCuts_chi2", "c_eventCuts_chi2", 1000, 1300)
    # keep(c)

    # panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    # p = panels[0]
    # p["plot"].cd()

    # h5 = fs_get_th1(
    #     FND_unSkimmed,
    #     "Chi2DOF",
    #     "(80,0,20)",
    #     "CUT(tRange110,rf,unusedE,unusedTracks,coherentPeak,targetZ)"
    # )
    # h5.SetXTitle("#chi^{2}/dof")
    # h5.SetYTitle("Events")
    # h5.Draw("hist")

    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed, "Chi2DOF", "(80,0,20)",
    #         "CUT(tRange110,rf,unusedE,unusedTracks,coherentPeak,targetZ)"
    #     )
    # draw_vertical_lines(h5, [5.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h5, "Data", "l")],
    #     notes=["Cut: #chi^{2}/dof < 5"],

    #     # --- layout tweaks ---
    #     legend_box=(0.44, 0.22, 0.96, 0.84),
    #     legend_text_size=0.13,

    #     label_pos=(0.06, 0.90),
    #     label_size=0.16,

    #     notes_start_y=0.68,
    #     notes_text_size=0.16,
    #     notes_step=0.08,

    # )
    # draw_notes_pad(
    #     p["info_notes"],
    #     title="Cuts used",
    #     notes=[
    #         "Histogram cuts:",
    #         "CUT(tRange110,rf,unusedE,unusedTracks,coherentPeak,targetZ)",
    #         "Plotted variable: Chi2DOF",
    #     ],

    #     # --- bottom pad tweaks ---
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.75,
    #     notes_text_size=0.08,
    #     notes_step=0.10,

    # )

    # c.Print(pdf_path)


    # # ============================================================
    # # Page 6: Lambda flight length
    # # ============================================================
    # c = ROOT.TCanvas("c_eventCuts_lambdaFL", "c_eventCuts_lambdaFL", 1000, 1300)
    # keep(c)

    # panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    # p = panels[0]
    # p["plot"].cd()

    # h6 = fs_get_th1(
    #     FND_unSkimmed,
    #     "VeeLP1",
    #     "(60,0,10)",
    #     "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,Lambda,targetZ)"
    # )
    # h6.SetXTitle("#Lambda flight length [cm]")
    # h6.SetYTitle("Events")
    # h6.Draw("hist")
    # draw_vertical_lines(h6, [2.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h6, "Data", "l")],
    #     notes=["Cut: L_{#Lambda} > 2 cm"],

    #     # --- layout tweaks ---
    #     legend_box=(0.44, 0.22, 0.96, 0.84),
    #     legend_text_size=0.13,

    #     label_pos=(0.06, 0.90),
    #     label_size=0.16,

    #     notes_start_y=0.68,
    #     notes_text_size=0.16,
    #     notes_step=0.08,

    # )
    # draw_notes_pad(
    #     p["info_notes"],
    #     title="Cuts used",
    #     notes=[
    #         "Histogram cuts:",
    #         "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,Lambda,targetZ)",
    #         "Plotted variable: VeeLP1",
    #     ],

    #     # --- bottom pad tweaks ---
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.75,
    #     notes_text_size=0.08,
    #     notes_step=0.10,

    # )

    # c.Print(pdf_path)


    # # ============================================================
    # # Page 7: KShort flight length
    # # ============================================================
    # c = ROOT.TCanvas("c_eventCuts_kshortFL", "c_eventCuts_kshortFL", 1000, 1300)
    # keep(c)

    # panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    # p = panels[0]
    # p["plot"].cd()

    # h7 = fs_get_th1(
    #     FND_unSkimmed,
    #     "VeeLP2",
    #     "(60,0,10)",
    #     "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,KShort,targetZ)"
    # )
    # h7.SetXTitle("K_{S} flight length [cm]")
    # h7.SetYTitle("Events")
    # h7.Draw("hist")
    # draw_vertical_lines(h7, [2.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h7, "Data", "l")],
    #     notes=["Cut: L_{K_{S}} > 2 cm"],

    #     # --- layout tweaks ---
    #     legend_box=(0.44, 0.22, 0.96, 0.84),
    #     legend_text_size=0.13,

    #     label_pos=(0.06, 0.90),
    #     label_size=0.16,

    #     notes_start_y=0.68,
    #     notes_text_size=0.16,
    #     notes_step=0.08,

    # )
    # draw_notes_pad(
    #     p["info_notes"],
    #     title="Cuts used",
    #     notes=[
    #         "Histogram cuts:",
    #         "CUT(tRange110,rf,chi2DOF,unusedE,coherentPeak,KShort,targetZ)",
    #         "Plotted variable: VeeLP2",
    #     ],

    #     # --- bottom pad tweaks ---
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.75,
    #     notes_text_size=0.08,
    #     notes_step=0.10,

    # )

    # c.Print(pdf_path)




# ------------------------------------------------------------
# Helpers for mand/t diagnostic plots
# ------------------------------------------------------------
def style_th1_basic(h, xtitle, ytitle):
    h.SetXTitle(xtitle)
    h.SetYTitle(ytitle)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMinimum(0.0)


def style_th2_basic(h, xtitle, ytitle):
    h.SetXTitle(xtitle)
    h.SetYTitle(ytitle)


# ============================================================
# DELTA t PLOTS
# ============================================================

# # -----------------------------
# # Define variables for t_prime_Ks: t' = |t - t_0|
# # -----------------------------
# p3_ks ="2"   # KShort
# p4_ks = "1,3"   # recoil Lambda

# s_ks    = "MASS2(GLUEXBEAM,GLUEXTARGET)"
# sqs_ks  = f"sqrt({s_ks})"
# m1sq_ks = "0.0"
# m2sq_ks = "MASS2(GLUEXTARGET)"
# m3sq_ks = f"MASS2({p3_ks})"
# m4sq_ks = f"MASS2({p4_ks})"

# E1_ks   = f"(({s_ks})+({m1sq_ks})-({m2sq_ks}))/(2*({sqs_ks}))"
# E3_ks   = f"(({s_ks})+({m3sq_ks})-({m4sq_ks}))/(2*({sqs_ks}))"
# p1_ks   = f"sqrt(({E1_ks})*({E1_ks})-({m1sq_ks}))"      # = E1 for photon
# p3cm_ks = f"sqrt(({E3_ks})*({E3_ks})-({m3sq_ks}))"

# t_ks    = f"MASS2(GLUEXBEAM,-{p3_ks})"
# t0_ks   = f"({m1sq_ks})+({m3sq_ks})-2*((({E1_ks})*({E3_ks}))-(({p1_ks})*({p3cm_ks})))"

# tprime_ks     = f"(({t_ks})-({t0_ks}))"

# # -----------------------------
# # Define variables for t_prime_Pip: t' = |t - t_0|
# # -----------------------------
# p3_pip = "3"   # PiPlus
# p4_pip = "1,2"   # recoil Lambda

# s_pip    = "MASS2(GLUEXBEAM,GLUEXTARGET)"
# sqs_pip  = f"sqrt({s_pip})"
# m1sq_pip = "0.0"
# m2sq_pip = "MASS2(GLUEXTARGET)"
# m3sq_pip = f"MASS2({p3_pip})"
# m4sq_pip = f"MASS2({p4_pip})"

# E1_pip   = f"(({s_pip})+({m1sq_pip})-({m2sq_pip}))/(2*({sqs_pip}))"
# E3_pip   = f"(({s_pip})+({m3sq_pip})-({m4sq_pip}))/(2*({sqs_pip}))"
# p1_pip   = f"sqrt(({E1_pip})*({E1_pip})-({m1sq_pip}))"      # = E1 for photon
# p3cm_pip = f"sqrt(({E3_pip})*({E3_pip})-({m3sq_pip}))"

# t_pip    = f"MASS2(GLUEXBEAM,-{p3_pip})"
# t0_pip   = f"({m1sq_pip})+({m3sq_pip})-2*((({E1_pip})*({E3_pip}))-(({p1_pip})*({p3cm_pip})))"

# tprime_pip     = f"(({t_pip})-({t0_pip}))"


# ------------------------------------------------------------
# Delta t = t_KS - t_pi+
# ------------------------------------------------------------
def deltaTPlots_KShort_vs_PiPlus(pdf_path):
    c = ROOT.TCanvas("c_delta_t_ks_pip", "c_delta_t_ks_pip", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]

    p["plot"].cd()
    ROOT.gPad.SetRightMargin(0.14)

    expr = f"(-1*MASS2(GLUEXBEAM,-{DecayingKShort})) - (-1*MASS2(GLUEXBEAM,-{PiPlus1})):MASS({DecayingKShort},{PiPlus1})"

    h = fs_get_th2(
        FND_eventSelectionSkims,
        expr,
        "(100,0.4,4.0,100,-10.0,10.0)",
        f"CUT({baseCuts},{sidebandCuts})"
    )

    style_th2_basic(
        h,
        "M(K_{S}#pi^{+}) [GeV/c^{2}]",
        "t_{K_{S}} - t_{#pi^{+}} [GeV^{2}]"
    )
    h.Draw("colz")

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        # legend_items=[(h, "Data density", "f")],
        notes=[
            "#Delta t",
        ],
        # --- layout tweaks ---
        legend_box=(0.44, 0.22, 0.96, 0.84),
        legend_text_size=0.13,

        label_pos=(0.06, 0.90),
        label_size=0.16,

        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.08,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            f"Histogram cuts: CUT({baseCuts},{sidebandCuts})",
            f"x = MASS({DecayingKShort},{PiPlus1})",
            f"y = (-1*MASS2(GLUEXBEAM,-{DecayingKShort})) - (-1*MASS2(GLUEXBEAM,-{PiPlus1}))",
        ],
        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.75,
        notes_text_size=0.08,
        notes_step=0.10,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")
    ROOT.FSHistogram.clearHistogramCache()

# ------------------------------------------------------------
# Delta t' = t'_KS - t'_pi+ - USING FSROOT'S IN-LINE MACRO CREATOR
# ------------------------------------------------------------

# K. Saldana 4/17/2026
# t' = t-t0
# MASS2(P1-P3) - ( MASS(1) + MASS(3) - 2*((E1*E3) -MOMENTUM(P1,P3)))

# K. Saldana 4/17/2026
# FSMode::defineMacro("E1",3,(MASS2(1,3)+MASS(1)+MASS(3))/(2*sqrt(MASS2(1,3))))

def deltaTPrimePlots_KShort_vs_PiPlus(pdf_path):
    c = ROOT.TCanvas("c_delta_tPrime_ks_pip", "c_delta_tPrime_ks_pip", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]

    p["plot"].cd()
    ROOT.gPad.SetRightMargin(0.14)

    # Define a simple test macro.
    # E1(I,J) = energy of particle I in the rest frame of system I+J
    # ROOT.FSTree.defineMacro("E1",2,"((MASS2([I],[J]) + MASS2([I]) - MASS2([J]))/(2*sqrt(MASS2([I],[J]))))")

    ROOT.FSTree.defineMacro(
    "E1",
    2,
    "((pow(EnP[I]+EnP[J],2)"
    "-pow(PxP[I]+PxP[J],2)"
    "-pow(PyP[I]+PyP[J],2)"
    "-pow(PzP[I]+PzP[J],2)"
    "+"
    "pow(EnP[I],2)-pow(PxP[I],2)-pow(PyP[I],2)-pow(PzP[I],2)"
    "-"
    "(pow(EnP[J],2)-pow(PxP[J],2)-pow(PyP[J],2)-pow(PzP[J],2)))"
    "/"
    "(2*sqrt(pow(EnP[I]+EnP[J],2)"
    "-pow(PxP[I]+PxP[J],2)"
    "-pow(PyP[I]+PyP[J],2)"
    "-pow(PzP[I]+PzP[J],2))))"
    )

    expr = f"E1({DecayingLambda};{DecayingKShort}) - E1({DecayingLambda};{PiPlus1}):MASS({DecayingKShort},{PiPlus1})"

    h = fs_get_th2(
        FND_eventSelectionSkims,
        expr,
        "(100,0.4,4.0,100,0.0,4.0)",
        f"CUT({baseCuts},{sidebandCuts})"
    )

    style_th2_basic(
        h,
        "M(K_{S}#pi^{+}) [GeV/c^{2}]",
        "t'_{K_{S}} - t'_{#pi^{+}} [GeV^{2}]"
    )

    h.Draw("colz")

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        notes=["#Delta t'"],
        legend_box=(0.44, 0.22, 0.96, 0.84),
        legend_text_size=0.13,
        label_pos=(0.06, 0.90),
        label_size=0.16,
        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.08,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            f"Histogram cuts: CUT({baseCuts},{sidebandCuts})",
            f"x = MASS({DecayingKShort},{PiPlus1})",
            "y = E1({DecayingLambda};{DecayingKShort}) - E1({DecayingLambda};{PiPlus1})",
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.75,
        notes_text_size=0.08,
        notes_step=0.10,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")
    ROOT.FSHistogram.clearHistogramCache()

# ------------------------------------------------------------
# Delta t' = t'_KS - t'_pi+ - TO MAKE THIS VERSION, EDIT FSROOT TO ADD THE MACRO.
# ------------------------------------------------------------

# print("Testing FSMath::tprime...")
# ROOT.gROOT.ProcessLine(
#     "double test_tprime = FSMath::tprime("
#     "1,0,0,1,"
#     "0,0,0,0.938272,"
#     "0,0,1,1.2,"
#     "0,0,-1,1.5);"
# )

# print("testing which .so file is loaded...")
# print(ROOT.gSystem.ListLibraries())

# def deltaTPrimePlots_KShort_vs_PiPlus(pdf_path):
#     c = ROOT.TCanvas("c_delta_tprime_ks_pip", "c_delta_tprime_ks_pip", 1000, 1300)
#     keep(c)

#     panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
#     p = panels[0]

#     p["plot"].cd()
#     ROOT.gPad.SetRightMargin(0.14)

#     h = fs_get_th2(
#         FND_eventSelectionSkims,
#         f"TPRIMEKS-TPRIMEPIP:MASS({DecayingKShort},{PiPlus1})",
#         "(100,0.4,4.0,100,-2.0,2.0)",
#         f"CUT({baseCuts},{sidebandCuts})"
#     )

#     h.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
#     h.SetYTitle("t'_{K_{S}} - t'_{#pi^{+}} [GeV^{2}]")
#     h.Draw("colz")

#     draw_info_pad(
#         p["info_main"],
#         file_label(FND_eventSelectionSkims),
#         legend_items=[(h, "Data density", "f")],
#         notes=["#Delta t' diagnostic plot"],
        
#         legend_box=(0.62, 0.24, 0.96, 0.84),
#         legend_text_size=0.10,
#         label_pos=(0.06, 0.90),
#         label_size=0.10,
#         notes_start_y=0.68,
#         notes_text_size=0.09,
#         notes_step=0.12,
#     )

#     draw_notes_pad(
#         p["info_notes"],
#         title="Cuts used",
#         notes=[
#             f"Global cuts: {generalCuts_eventSelection}",
#             f"Histogram cuts: CUT({baseCuts},{sidebandCuts})",
#             f"x = MASS({DecayingKShort},{PiPlus1})",
#             "y = TPRIMEKS - TPRIMEPIP",
#             ],
        
#         title_pos=(0.06, 0.88),
#         title_size=0.11,
#         notes_start_y=0.70,
#         notes_text_size=0.075,
#         notes_step=0.15,
#     )

#     # c.Print(pdf_path)
#     c.Print(f"{pdf_path})")
#     ROOT.FSHistogram.clearHistogramCache()


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


# -------- KSHORT FLIGHTLENGTH STUDY -------------
def massPlots_KShort_flightLength(pdf_path):
    c = ROOT.TCanvas("c_mass_ks", "c_mass_ks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData_FLoff = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        "CUT(rejectSigma1385,rf,Lambda)"
    )

    hData_FLon = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        "CUT(rejectSigma1385,flightLengthKShort,rf,Lambda)"
    )

    fit_FLoff = make_voigtian_plus_expo2(
        name="fit_ks_FLoff_voigt_exp",
        xmin=0.35,
        xmax=0.65,
        amp=8.0,
        mean=0.4976,
        sigma=0.003,
        width=0.0025,
        p0=1.0,
        p1=2.0,
        p2=0.0,
    )
    fit_FLoff.SetParLimits(2, 0.0001, 0.01)   # sigma
    fit_FLoff.SetParLimits(3, 0.0001, 0.01)   # width

    fit_FLon = make_voigtian_plus_expo2(
        name="fit_ks_FLon_voigt_exp",
        xmin=0.35,
        xmax=0.65,
        amp=8.0,
        mean=0.4976,
        sigma=0.003,
        width=0.0025,
        p0=0.0,
        p1=0.3,
        p2=0.0,
    )
    hData_FLon.SetFillColor(ROOT.kBlue)
    hData_FLoff.SetXTitle("M(#pi^{+}#pi^{-}) [GeV/c^{2}]")
    hData_FLoff.SetYTitle("Counts / 5 MeV")
    hData_FLoff.Draw("pE")
    hData_FLon.Draw("hist same")

    # Fitting
    fit_FLoff.SetParLimits(2, 0.0001, 0.01)   # sigma
    fit_FLoff.SetParLimits(3, 0.0001, 0.01)   # width
    
    hData_FLoff.Fit(fit_FLoff, "R0")
    hData_FLon.Fit(fit_FLon, "R0")

    fit_FLoff.SetLineColor(ROOT.kBlack)
    fit_FLoff.SetLineWidth(2)

    fit_FLon.SetLineColor(ROOT.kRed)
    fit_FLon.SetLineWidth(2)

    fit_FLoff.Draw("same")
    fit_FLon.Draw("same")

    # fit_FLoff_voigt, fit_FLoff_expo2 = make_component_funcs(fit_FLoff, xmin=0.35, xmax=0.65)
    # fit_FLoff_voigt.SetLineColor(ROOT.kBlue)
    # fit_FLoff_expo2.SetLineColor(ROOT.kRed)
    # fit_FLoff_voigt.Draw("same")
    # fit_FLoff_expo2.Draw("same")

    p["plot"].Modified()
    p["plot"].Update()

    # ----- Integration limits for signal and background functions
    xmin, xmax = 0.4676, 0.5276   # K_S mass 0.4976 +/- 0.03
    bin_width = hData_FLoff.GetXaxis().GetBinWidth(1)

    # integrate under histograms
    integral_FLoff = integral_between(hData_FLoff, xmin, xmax)
    integral_FLon  = integral_between(hData_FLon,  xmin, xmax)

    # integrate under signal and background components separately
    integral_fit_FLoff_voigt = fit_integral_signal(fit_FLoff, xmin, xmax, bin_width=bin_width)
    integral_fit_FLoff_expo2 = fit_integral_background(fit_FLoff, xmin, xmax, bin_width=bin_width)

    # ----- Figures of merit
    S_off, B_off, SB_off, significance_off, purity_off = compute_figureOfMerit(
        fit_FLoff, xmin, xmax, bin_width=bin_width
    )
    S_on, B_on, SB_on, significance_on, purity_on = compute_figureOfMerit(
        fit_FLon, xmin, xmax, bin_width=bin_width
    )

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData_FLoff, "Ks FL OFF " f"(Integral: {integral_FLoff:.0f})", "pE"),
            (hData_FLon,  "Ks FL ON "  f"(Integral: {integral_FLon:.0f})",  "f"),
            (fit_FLoff,   "Ks FL OFF Fit", "l"),
            (fit_FLon,    "Ks FL ON Fit",  "l"),
        ],
        notes=[
            f"Signal / Background FL_OFF: {SB_off:.2f}",
            f"Signal / Background FL_ON:  {SB_on:.2f}",
            # f"Significance (Sig/#sqrt{{Sig+Bkg}}) FL_OFF: {significance_off:.2f}",
            # f"Significance (Sig/#sqrt{{Sig+Bkg}}) FL_ON:  {significance_on:.2f}",
            f"Purity [Sig/(Sig+Bkg)] FL_OFF: {purity_off:.2f}",
            f"Purity [Sig/(Sig+Bkg)] FL_ON:  {purity_on:.2f}",
        ],

        # --- layout tweaks ---
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.13,

        label_pos=(0.06, 0.90),
        label_size=0.16,

        notes_start_y=0.70,
        notes_text_size=0.118,
        notes_step=0.16,
    )

    draw_notes_pad(
        p["info_notes"],
        title="#bf{Cuts used}",
        notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            "hist FL_OFF: CUT(rejectSigma1385,rf,Lambda)",
            "hist FL_ON: CUT(rejectSigma1385,flightLengthKShort,rf,Lambda)",
            "#bf{Figure of merit raw values}",
            f"Sig FL_OFF: {S_off:.0f}, Bkg FL_OFF: {B_off:.0f}. Compare to #rightarrow  voigt: {integral_fit_FLoff_voigt:.0f}, exp: {integral_fit_FLoff_expo2:.0f}",
            f"Sig FL_ON:  {S_on:.0f}, Bkg FL_ON:  {B_on:.0f}",
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.11,
    )

    # c.Print(pdf_path)
    c.Print(f"{pdf_path}(")
    ROOT.FSHistogram.clearHistogramCache()

# def massPlots_KShort_flightLength(pdf_path):
#     c = ROOT.TCanvas("c_mass_ks", "c_mass_ks", 1000, 1300)
#     keep(c)

#     panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
#     p = panels[0]
#     p["plot"].cd()

#     hData_FLoff = fs_get_th1(
#         FND_eventSelectionSkims,
#         f"MASS({DecayingKShort})",
#         "(60,0.35,0.65)",
#         "CUT(rejectSigma1385,rf,Lambda)"
#     )

#     hData_FLon = fs_get_th1(
#         FND_eventSelectionSkims,
#         f"MASS({DecayingKShort})",
#         "(60,0.35,0.65)",
#         "CUT(rejectSigma1385,flightLengthKShort,rf,Lambda)"
#     )

#     hData_FLoff.SetXTitle("M(#pi^{+}#pi^{-}) [GeV/c^{2}]")
#     hData_FLoff.SetYTitle("Counts / 5 MeV")
#     hData_FLoff.SetLineColor(ROOT.kBlack)

#     hData_FLon.SetLineColor(ROOT.kBlack)
#     hData_FLon.SetFillColor(ROOT.kBlue)

#     hData_FLoff.Draw("pE")
#     hData_FLon.Draw("hist same")

#     integral_FLoff = integral_between(hData_FLoff, 0.35, 0.65)
#     integral_FLon = integral_between(hData_FLon, 0.35, 0.65)

#     draw_info_pad(
#         p["info_main"],
#         file_label(FND_eventSelectionSkims),
#         legend_items=[
#             (hData_FLoff, "Ks FL OFF " "(Integral: " f"{integral_FLoff:.0f})", "pE"),
#             (hData_FLon, "Ks FL ON " "(Integral: " f"{integral_FLon:.0f})", "f"),
#         ],
#         notes=["K_{S} Flightlength #bf{(FL)} study"],

#         # --- layout tweaks ---
#         legend_box=(0.48, 0.22, 0.96, 0.84),
#         legend_text_size=0.13,

#         label_pos=(0.06, 0.90),
#         label_size=0.16,

#         notes_start_y=0.68,
#         notes_text_size=0.16,
#         notes_step=0.08,
#     )

#     draw_notes_pad(
#         p["info_notes"],
#         title="Cuts used",
#         notes=[
#             f"Global cuts: {generalCuts_eventSelection}",
#             "Flightlength OFF cuts: CUT(rejectSigma1385,rf,Lambda)",
#             "Flightlength ON cuts: CUT(rejectSigma1385,flightLengthKShort,rf,Lambda)",
#         ],

#         # --- bottom pad tweaks ---
#         title_pos=(0.06, 0.88),
#         title_size=0.11,

#         notes_start_y=0.70,
#         notes_text_size=0.075,
#         notes_step=0.16,
#     )

#     c.Print(pdf_path)
#     # c.Print(f"{pdf_path}(")
#     ROOT.FSHistogram.clearHistogramCache()



# -------- KSHORT SIDEBAND STUDY -------------
def massPlots_KShort_sideBands(pdf_path):
    c = ROOT.TCanvas("c_mass_ks", "c_mass_ks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.38)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,Lambda)",
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,Lambda)*CUTWT(rf,KShort,Lambda)",
    )

    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,Lambda)*CUTSBWT(rf,KShort,Lambda)",
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
            (hData, "M(#pi^{+} #pi^{-}) " "(Integral: " f"{integral_ks:.0f})", "pE"),
            (hSig, "K_{s} Signal " "(Integral: " f"{integral_ksSig:.0f})", "f"),
            (hBkgNegative, "K_{s} Background " "(Integral: " f"{integral_ksBkg:.0f})", "f"),
        ],
        notes=["K_{S} Sideband study"],

        # --- layout tweaks ---
        legend_box=(0.44, 0.22, 0.96, 0.84),
        legend_text_size=0.13,

        label_pos=(0.06, 0.90),
        label_size=0.16,

        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.08,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.06, f"Global cuts: {generalCuts_eventSelection}"),
            (0.06, "M(#pi^{+} #pi^{-}): CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,Lambda)"),
            (0.06, "Signal: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,Lambda)*CUTWT(rf,KShort,Lambda)"),
            (0.06, "Background: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,Lambda)*CUTSBWT(rf,KShort,Lambda)"),
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.75,
        notes_text_size=0.08,
        notes_step=0.10,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")
    ROOT.FSHistogram.clearHistogramCache()




# -------- KSHORT MISSING MASS -------------
def massPlots_KShort_missingMass(pdf_path):
    c = ROOT.TCanvas("c_mm_ks", "c_mm_ks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingLambda},-{PiPlus1})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingLambda},-{PiPlus1})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingLambda},-{PiPlus1})",
        "(60,0.35,0.65)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})"
    )

    hBkgNegative = hBkg.Clone("hMMKsBkgNegative")
    keep(hBkgNegative)
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("MM(#Lambda#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 5 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)

    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    integral_data = integral_between(hData, 0.35, 0.65)
    integral_sig  = integral_between(hSig, 0.35, 0.65)
    integral_bkg  = integral_between(hBkg, 0.35, 0.65)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, f"K_{{S}} MM (Integral: {integral_data:.0f})", "pE"),
            (hSig,  f"K_{{S}} MM Signal (Integral: {integral_sig:.0f})", "f"),
            (hBkgNegative, f"K_{{S}} MM Background (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["Missing mass K_{S}"],
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


# -------- KSHORT FINAL SELECTION -------------
def massPlots_KShort_FINAL_SELECTION(pdf_path):
    c = ROOT.TCanvas("c_mass_ks", "c_mass_ks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.38)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,Lambda)*CUTWT(rf,Lambda)"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort})",
        "(60,0.35,0.65)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort,Lambda)*CUTWT(rf,KShort,Lambda)",
    )

    hData.SetXTitle("M(#pi^{+}#pi^{-}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 5 MeV")

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)


    hData.Draw("pE")
    hSig.Draw("hist same")

    integral_ks = integral_between(hData, 0.35, 0.65)
    integral_ksSig = integral_between(hSig, 0.35,0.65)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "M(#pi^{+} #pi^{-}) " "(Integral: " f"{integral_ks:.0f})", "pE"),
            (hSig, "K_{s} Signal " "(Integral: " f"{integral_ksSig:.0f})", "f"),
        ],
        notes=["K_{S} final selection"],

        # --- layout tweaks ---
        legend_box=(0.44, 0.22, 0.96, 0.84),
        legend_text_size=0.13,

        label_pos=(0.06, 0.90),
        label_size=0.16,

        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.14,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.06, f"Global cuts: {generalCuts_eventSelection}"),
            (0.06, "M(#pi^{+} #pi^{-}): CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,Lambda)*CUTWT(rf,Lambda)"),
            (0.06, "Signal: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,KShort,Lambda)*CUTWT(rf,KShort,Lambda)"),
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.70,
        notes_text_size=0.08,
        notes_step=0.14,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")
    ROOT.FSHistogram.clearHistogramCache()


# -------- LAMBDA FLIGHTLENGTH STUDY -------------
def massPlots_Lambda_flightLength(pdf_path):
    c = ROOT.TCanvas("c_mass_lambda", "c_mass_lambda", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData_FLoff = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        "CUT(rejectSigma1385,rf,KShort)"
    )

    hData_FLon = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        "CUT(rejectSigma1385,flightLengthLambda,rf,KShort)"
    )

    fit_FLoff = make_voigtian_plus_expo2(
    name="fit_lambda_FLoff_voigt_exp",
    xmin=1.08,
    xmax=1.19,
    amp=8.0,
    mean=1.1157,
    sigma=0.003,
    width=0.0029,
    p0=1.0,
    p1=1.0,
    p2=0.0,
    )

    fit_FLon = make_voigtian_plus_expo2(
    name="fit_lambda_FLon_voigt_exp",
    xmin=1.08,
    xmax=1.19,
    amp=8.0,
    mean=1.1157,
    sigma=0.003,
    width=0.0025,
    p0=1.0,
    p1=0.01,
    p2=0.0,
    )

    hData_FLon.SetFillColor(ROOT.kBlue)
    hData_FLoff.SetXTitle("M(p #pi^{-}) [GeV/c^{2}]")
    hData_FLoff.SetYTitle("Counts / 2 MeV")
    hData_FLoff.Draw("pE")
    hData_FLon.Draw("hist same")

    # Fitting
    fit_FLoff.SetParLimits(2, 0.0001, 0.01)   # sigma
    fit_FLoff.SetParLimits(3, 0.0001, 0.01)   # width
    
    hData_FLoff.Fit(fit_FLoff, "R0")
    hData_FLon.Fit(fit_FLon, "R0")

    fit_FLoff.SetLineColor(ROOT.kBlack)
    fit_FLoff.SetLineWidth(2)

    fit_FLon.SetLineColor(ROOT.kRed)
    fit_FLon.SetLineWidth(2)

    fit_FLoff.Draw("same")
    fit_FLon.Draw("same")

    # fit_FLoff_voigt, fit_FLoff_expo2 = make_component_funcs(fit_FLoff, xmin=1.08, xmax=1.19)
    # fit_FLoff_voigt.SetLineColor(ROOT.kGreen)
    # fit_FLoff_expo2.SetLineColor(ROOT.kMagenta)
    # fit_FLoff_voigt.Draw("same")
    # fit_FLoff_expo2.Draw("same")

    p["plot"].Modified()
    p["plot"].Update()

    # draw lines at 1.119 +/- 0.01375
    # draw_vertical_lines(hData_FLon, [1.10525,1.13275])

    # ----- Integration limits for signal and background functions
    xmin, xmax = 1.10525, 1.13275
    bin_width = hData_FLoff.GetXaxis().GetBinWidth(1)

    # integrate under total fit(s)
    integral_FLoff = integral_between(hData_FLoff, 1.10525, 1.13275)
    integral_FLon  = integral_between(hData_FLon,  1.10525, 1.13275)

    # integrate under signal and background components separately.
    # NOTE: The integrals below are already calculated by 'compute_figureOfMerit' function;
    # They are created here only as a double-check.
    integral_fit_FLoff_voigt = fit_integral_signal(fit_FLoff,     1.10525, 1.13275, bin_width=bin_width)
    integral_fit_FLoff_expo2 = fit_integral_background(fit_FLoff, 1.10525, 1.13275, bin_width=bin_width)

    # ----- Sig/Bkg ratios flightlength OFF
    S_off, B_off, SB_off, significance_off, purity_off = compute_figureOfMerit(
            fit_FLoff, xmin, xmax, bin_width=bin_width
        )
    # ----- Sig/Bkg ratios flightlength ON
    S_on, B_on, SB_on, significance_on, purity_on = compute_figureOfMerit(
            fit_FLon, xmin, xmax, bin_width=bin_width
        )

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData_FLoff, "Lamb FL OFF " "(Integral: " f"{integral_FLoff:.0f})", "pE"),
            (hData_FLon, "Lamb FL ON " "(Integral: " f"{integral_FLon:.0f})", "f"),
            (fit_FLoff, "Lamb FL OFF Fit", "l"),
            (fit_FLon, "Lamb FL ON Fit", "l"),
        ],
        notes=[
            f"Signal / Background FL_OFF: {SB_off:.2f}",
            f"Signal / Background FL_ON:  {SB_on:.2f}",
            # f"Significance (Sig/#sqrt{{Sig+Bkg}}) FL_OFF: {significance_off:.2f}",
            # f"Significance (Sig/#sqrt{{Sig+Bkg}}) FL_ON:  {significance_on:.2f}",
            f"Purity [Sig/(Sig+Bkg)] FL_OFF: {purity_off:.2f}",
            f"Purity [Sig/(Sig+Bkg)] FL_ON:  {purity_on:.2f}",
        ],

        # --- layout tweaks ---
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.13,

        label_pos=(0.06, 0.90),
        label_size=0.16,

        notes_start_y=0.70,
        notes_text_size=0.118,
        notes_step=0.16,
    )

    draw_notes_pad(
        p["info_notes"],
        title="#bf{Cuts used}",
            notes=[
            f"Global cuts: {generalCuts_eventSelection}",
            "hist FL_OFF: CUT(rejectSigma1385,rf,KShort)",
            "hist FL_ON: CUT(rejectSigma1385,flightLengthLambda,rf,KShort)",
            "#bf{Figure of merit raw values}",
            f"Sig FL_OFF: {S_off:.0f}, Bkg FL_OFF: {B_off:.0f}. Compare to #rightarrow  voigt: {integral_fit_FLoff_voigt:.0f}, exp: {integral_fit_FLoff_expo2:.0f}",
            f"Sig FL_ON:  {S_on:.0f}, Bkg FL_ON:  {B_on:.0f}",
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.075,
        notes_step=0.11,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")
    ROOT.FSHistogram.clearHistogramCache()


# -------- LAMBDA SIDEBAND STUDY -------------
def massPlots_Lambda_sideBands(pdf_path):
    c = ROOT.TCanvas("c_mass_ks_lambda", "c_mass_ks_lambda", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort)",
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort)*CUTWT(rf,KShort,Lambda)",
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort)*CUTSBWT(rf,KShort,Lambda)",
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
            (hData, "M(p #pi^{+}) " "(Integral: " f"{integral_Lamb:.0f})", "pE"),
            (hSig, "Lambda Signal " "(Integral: " f"{integral_LambSig:.0f})", "f"),
            (hBkgNegative, "Lamb Backgnd " "(Integral: " f"{integral_LambBkg:.0f})", "f"),
        ],
        notes=["Lambda Sideband study"],

        legend_box=(0.44, 0.22, 0.96, 0.84),
        legend_text_size=0.13,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.12,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.06, f"Global cuts: {generalCuts_eventSelection}"),
            (0.06, "M(p #pi^{-}): CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,KShort)"),
            (0.06, "Signal: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,KShort)*CUTWT(rf,KShort,Lambda)"),
            (0.06, "Background: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,KShort)*CUTSBWT(rf,KShort,Lambda)"),
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.75,
        notes_text_size=0.08,
        notes_step=0.10,
    )

    c.Print(pdf_path)
    ROOT.FSHistogram.clearHistogramCache()



# -------- LAMBDA MISSING MASS -------------
def massPlots_Lambda_missingMass(pdf_path):
    c = ROOT.TCanvas("c_mm_lambda", "c_mm_lambda", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingKShort},-{PiPlus1})",
        "(60,1.08,1.20)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingKShort},-{PiPlus1})",
        "(60,1.08,1.20)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingKShort},-{PiPlus1})",
        "(60,1.08,1.20)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})"
    )

    hBkgNegative = hBkg.Clone("hMMLambdaBkgNegative")
    keep(hBkgNegative)
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("MM(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 2 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)

    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    integral_data = integral_between(hData, 1.08, 1.20)
    integral_sig  = integral_between(hSig, 1.08, 1.20)
    integral_bkg  = integral_between(hBkg, 1.08, 1.20)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, f"#Lambda MM (Integral: {integral_data:.0f})", "pE"),
            (hSig,  f"#Lambda MM Signal (Integral: {integral_sig:.0f})", "f"),
            (hBkgNegative, f"#Lambda MM Background (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["Missing mass #Lambda"],
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

    # c.Print(f"{pdf_path})")
    c.Print(pdf_path)
    ROOT.FSHistogram.clearHistogramCache()


# -------- LAMBDA FINAL SELECTION -------------
def massPlots_Lambda_FINAL_SELECTION(pdf_path):
    c = ROOT.TCanvas("c_mass_lambda", "c_mass_lambda", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort)*CUTWT(rf,KShort)"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda})",
        "(60,1.08,1.20)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort)*CUTWT(rf,KShort,Lambda)",
    )

    hData.SetXTitle("M(p #pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 2 MeV")

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)


    hData.Draw("pE")
    hSig.Draw("hist same")

    integral_ks = integral_between(hData, 1.08,1.20)
    integral_ksSig = integral_between(hSig, 1.08,1.20)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "M(p #pi^{-}) " "(Integral: " f"{integral_ks:.0f})", "pE"),
            (hSig, "Lambda Signal " "(Integral: " f"{integral_ksSig:.0f})", "f"),
        ],
        notes=["Lambda final selection"],

        # --- layout tweaks ---
        legend_box=(0.44, 0.22, 0.96, 0.84),
        legend_text_size=0.13,

        label_pos=(0.06, 0.90),
        label_size=0.16,

        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.12,
    )

    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.06, f"Global cuts: {generalCuts_eventSelection}"),
            (0.06, "M(p #pi^{-}): CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,KShort)*CUTWT(rf,KShort)"),
            (0.06, "Signal: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.18, "rf,KShort)*CUTWT(rf,KShort,Lambda)"),
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.70,
        notes_text_size=0.08,
        notes_step=0.14,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")
    ROOT.FSHistogram.clearHistogramCache()


def deltaMassPlots_KShort(pdf_path):
    c = ROOT.TCanvas("c_delta_mass_ks", "c_delta_mass_ks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    expr = f"MASS({DecayingKShort}) - MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingLambda},-{PiPlus1})"

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        expr,
        "(80,-0.10,0.10)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        expr,
        "(80,-0.10,0.10)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        expr,
        "(80,-0.10,0.10)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})"
    )

    hBkgNegative = hBkg.Clone("hDeltaKsBkgNegative")
    keep(hBkgNegative)
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(K_{S}) - MM(#Lambda#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 2.5 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)

    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    zeroLine = ROOT.TLine(0.0, hData.GetMinimum(), 0.0, hData.GetMaximum())
    zeroLine.SetLineColor(ROOT.kBlack)
    zeroLine.SetLineStyle(2)
    zeroLine.Draw("same")
    keep(zeroLine)

    integral_data = integral_between(hData, -0.10, 0.10)
    integral_sig  = integral_between(hSig,  -0.10, 0.10)
    integral_bkg  = integral_between(hBkg,  -0.10, 0.10)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, f"K_{{S}} #DeltaM (Integral: {integral_data:.0f})", "pE"),
            (hSig, f"K_{{S}} Signal #DeltaM (Integral: {integral_sig:.0f})", "f"),
            (hBkgNegative, f"K_{{S}} Background #DeltaM (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["#DeltaM(K_{S}) = M(K_{S}) - MM(#Lambda#pi^{+})"],
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




def deltaMassPlots_Lambda(pdf_path):
    c = ROOT.TCanvas("c_delta_mass_lambda", "c_delta_mass_lambda", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    expr = f"MASS({DecayingLambda}) - MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingKShort},-{PiPlus1})"

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        expr,
        "(80,-0.10,0.10)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        expr,
        "(80,-0.10,0.10)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        expr,
        "(80,-0.10,0.10)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})"
    )

    hBkgNegative = hBkg.Clone("hDeltaLambdaBkgNegative")
    keep(hBkgNegative)
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(#Lambda) - MM(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 2.5 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hSig.SetLineColor(ROOT.kBlack)
    hSig.SetFillColor(ROOT.kBlue)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)

    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    zeroLine = ROOT.TLine(0.0, hData.GetMinimum(), 0.0, hData.GetMaximum())
    zeroLine.SetLineColor(ROOT.kBlack)
    zeroLine.SetLineStyle(2)
    zeroLine.Draw("same")
    keep(zeroLine)

    integral_data = integral_between(hData, -0.10, 0.10)
    integral_sig  = integral_between(hSig,  -0.10, 0.10)
    integral_bkg  = integral_between(hBkg,  -0.10, 0.10)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, f"#Lambda #DeltaM (Integral: {integral_data:.0f})", "pE"),
            (hSig, f"#Lambda Signal #DeltaM (Integral: {integral_sig:.0f})", "f"),
            (hBkgNegative, f"#Lambda Background #DeltaM (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["#DeltaM(#Lambda) = M(#Lambda) - MM(K_{S}#pi^{+})"],
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
    # c.Print(f"{pdf_path})")
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
# KSTAR MASS PLOTS -- DATA FLIGHT LENGTH STUDY
# ------------------------------------------------------------
def massPlots_KStar_flightLength(pdf_path):
    c = ROOT.TCanvas("c_kstar_sidebands", "c_kstar_sidebands", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hSig1 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(rejectSigma1385)*CUTWT({sidebandCuts})"
        # "CUT(rejectSigma1385,nonLambda)*CUTWT(rf,KShort)"
    )
    hSig2 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(flightLengthKShort,rejectSigma1385)*CUTWT({sidebandCuts})"
        # "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,nonLambda)*CUTWT(rf,KShort)"
    )
    hSig3 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
        # "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,nonLambda)*CUTWT(rf,KShort)"
    )
    
    hSig4 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
        # "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,nonLambda)*CUTWT(rf,KShort)"
    )


    hSig1.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hSig1.SetYTitle("Combinations / 40 MeV")

    hSig1.SetLineColor(ROOT.kBlack)
    hSig1.SetFillColor(ROOT.kBlack)
    hSig2.SetLineColor(ROOT.kBlack)
    hSig2.SetFillColor(ROOT.kMagenta)
    hSig3.SetLineColor(ROOT.kBlack)
    hSig3.SetFillColor(ROOT.kGreen)
    hSig4.SetLineColor(ROOT.kBlack)
    hSig4.SetFillColor(ROOT.kBlue)

    hSig1.Draw("hist")
    hSig2.Draw("hist same")
    hSig3.Draw("hist same")
    hSig4.Draw("hist same")

    integral_kStarSig1 = integral_between(hSig1, 0.8, 1.0)
    integral_kStarSig2 = integral_between(hSig2, 0.8, 1.0)
    integral_kStarSig3 = integral_between(hSig3, 0.8, 1.0)
    integral_kStarSig4 = integral_between(hSig4, 0.8, 1.0)

    # ----- Fitting
    fit1_kstar = make_two_voigtians_plus_bernstein(
        name="fit_kstar_2voigt_bern",
        # xmin, xmax for fitting (integration limits defined elsewhere).
        xmin=0.6,
        xmax=2.5,
        bern_degree=3,
        # K*(892)
        amp1=500.0, mean1=0.892, sigma1=0.003, width1=0.050,
        # K*(1430)
        amp2=200.0, mean2=1.43,  sigma2=0.003, width2=0.100,
        coeffs=[100.0, 100.0, 100.0, 100.0],
    )
    # Keep sigma physically small, let width carry the Lorentzian broadening
    fit1_kstar.SetParLimits(2, 0.0001, 0.02)   # voigt1 sigma
    fit1_kstar.SetParLimits(3, 0.010,  0.150)  # voigt1 width
    fit1_kstar.SetParLimits(6, 0.0001, 0.02)   # voigt2 sigma
    fit1_kstar.SetParLimits(7, 0.050,  0.300)  # voigt2 width
    # Bernstein coeffs must stay positive to be well-behaved
    for i in range(4):
        fit1_kstar.SetParLimits(8 + i, 0.0, 1e6)

    hSig1.Fit(fit1_kstar, "R0")
    fit1_kstar.SetLineColor(ROOT.kBlack)
    fit1_kstar.SetLineWidth(2)
    # fit1_kstar.Draw("same")

    fit2_kstar = make_two_voigtians_plus_bernstein(
        name="fit_kstar_2voigt_bern",
        # xmin, xmax for fitting (integration limits defined elsewhere).
        xmin=0.6,
        xmax=2.5,
        bern_degree=3,
        # K*(892)
        amp1=500.0, mean1=0.892, sigma1=0.003, width1=0.050,
        # K*(1430)
        amp2=400.0, mean2=1.43,  sigma2=0.003, width2=0.100,
        coeffs=[100.0, 100.0, 100.0, 100.0],
    )
    # Keep sigma physically small, let width carry the Lorentzian broadening
    fit2_kstar.SetParLimits(2, 0.0001, 0.02)   # voigt1 sigma
    fit2_kstar.SetParLimits(3, 0.010,  0.150)  # voigt1 width
    fit2_kstar.SetParLimits(6, 0.0001, 0.02)   # voigt2 sigma
    fit2_kstar.SetParLimits(7, 0.050,  0.300)  # voigt2 width
    # Bernstein coeffs must stay positive to be well-behaved
    for i in range(4):
        fit2_kstar.SetParLimits(8 + i, 0.0, 1e6)

    hSig2.Fit(fit2_kstar, "R0")
    fit2_kstar.SetLineColor(ROOT.kBlue)
    fit2_kstar.SetLineWidth(2)
    # fit2_kstar.Draw("same")

    fit3_kstar = make_two_voigtians_plus_bernstein(
        name="fit_kstar_2voigt_bern",
        # xmin, xmax for fitting (integration limits defined elsewhere).
        xmin=0.6,
        xmax=2.5,
        bern_degree=3,
        # K*(892)
        amp1=500.0, mean1=0.892, sigma1=0.003, width1=0.050,
        # K*(1430)
        amp2=400.0, mean2=1.43,  sigma2=0.003, width2=0.100,
        coeffs=[100.0, 100.0, 100.0, 100.0],
    )
    # Keep sigma physically small, let width carry the Lorentzian broadening
    fit3_kstar.SetParLimits(2, 0.0001, 0.02)   # voigt1 sigma
    fit3_kstar.SetParLimits(3, 0.010,  0.150)  # voigt1 width
    fit3_kstar.SetParLimits(6, 0.0001, 0.02)   # voigt2 sigma
    fit3_kstar.SetParLimits(7, 0.050,  0.300)  # voigt2 width
    # Bernstein coeffs must stay positive to be well-behaved
    for i in range(4):
        fit3_kstar.SetParLimits(8 + i, 0.0, 1e6)

    hSig3.Fit(fit3_kstar, "R0")
    fit3_kstar.SetLineColor(ROOT.kBlue)
    fit3_kstar.SetLineWidth(2)
    # fit3_kstar.Draw("same")

    fit4_kstar = make_two_voigtians_plus_bernstein(
        name="fit_kstar_2voigt_bern",
        # xmin, xmax for fitting (integration limits defined elsewhere).
        xmin=0.6,
        xmax=2.5,
        bern_degree=3,
        # K*(892)
        amp1=500.0, mean1=0.892, sigma1=0.003, width1=0.050,
        # K*(1430)
        amp2=400.0, mean2=1.43,  sigma2=0.003, width2=0.100,
        coeffs=[100.0, 100.0, 100.0, 100.0],
    )
    # Keep sigma physically small, let width carry the Lorentzian broadening
    fit4_kstar.SetParLimits(2, 0.0001, 0.02)   # voigt1 sigma
    fit4_kstar.SetParLimits(3, 0.010,  0.150)  # voigt1 width
    fit4_kstar.SetParLimits(6, 0.0001, 0.02)   # voigt2 sigma
    fit4_kstar.SetParLimits(7, 0.050,  0.300)  # voigt2 width
    # Bernstein coeffs must stay positive to be well-behaved
    for i in range(4):
        fit4_kstar.SetParLimits(8 + i, 0.0, 1e6)

    hSig4.Fit(fit4_kstar, "R0")
    fit4_kstar.SetLineColor(ROOT.kBlue)
    fit4_kstar.SetLineWidth(2)
    # fit4_kstar.Draw("same")

    # Extract individual voigtian and bernstein parameters from above fit.  Then plot those lines individually.
    fit_voigt1, fit_voigt2, fit_bern = make_component_funcs_kstar(fit2_kstar, xmin=0.6, xmax=2.5, bern_degree=3)
    fit_voigt1.SetLineColor(ROOT.kBlue)
    fit_voigt1.SetLineStyle(2)
    fit_voigt2.SetLineColor(ROOT.kBlue)
    fit_voigt2.SetLineStyle(2)
    fit_bern.SetLineColor(ROOT.kRed + 2)
    fit_bern.SetLineStyle(2)
    # fit_voigt1.Draw("same")
    # fit_voigt2.Draw("same")
    # fit_bern.Draw("same")

    p["plot"].Modified()
    p["plot"].Update()

    # xmin, xmax for integration.
    xmin, xmax = 0.80, 1.00
    bin_width = hSig1.GetXaxis().GetBinWidth(1)

    S1_h1, S2_h1, S_h1, B_h1, SB_h1, significance_h1, purity_h1 = compute_figureOfMerit_kstar(
        fit1_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )
    S1_h2, S2_h2, S_h2, B_h2, SB_h2, significance_h2, purity_h2 = compute_figureOfMerit_kstar(
        fit2_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )
    S1_h3, S2_h3, S_h3, B_h3, SB_h3, significance_h3, purity_h3 = compute_figureOfMerit_kstar(
        fit3_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )
    S1_h4, S2_h4, S_h4, B_h4, SB_h4, significance_h4, purity_h4 = compute_figureOfMerit_kstar(
        fit4_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )

    # draw_vertical_lines(hSig1, [0.8, 1.0], color=ROOT.kRed)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hSig1, "M(Ks #pi^{+}) Sig1 (no FL. Int: " f"{integral_kStarSig1:.0f})", "f"),
            (hSig2, "M(Ks #pi^{+}) Sig2 (Ks FL. Int: " f"{integral_kStarSig2:.0f})", "f"),
            (hSig3, "M(Ks #pi^{+}) Sig3 (Lam FL. Int: " f"{integral_kStarSig3:.0f})", "f"),
            (hSig4, "M(Ks #pi^{+}) Sig4 (Ks & Lamb FL. Int: " f"{integral_kStarSig4:.0f})", "f"),
            # (fit1_kstar, "Sig1: 2 Voigt + Bernstein fit", "l"),
            # (fit2_kstar, "Sig2: 2 Voigt + Bernstein fit", "l"),
            # (fit3_kstar, "Sig3: 2 Voigt + Bernstein fit", "l"),
            # (fit4_kstar, "Sig4: 2 Voigt + Bernstein fit", "l"),
        ],
        notes=[
            (0.08, "K*(892) yield, Sig/Bkg, purity [S/(S+B)]"),
            (0.08, f"Sig1 yld: {S1_h1:.0f} S/B: {SB_h1:.2f} Purty: {purity_h1:.2f}"),
            (0.08, f"Sig2 yld: {S1_h2:.0f} S/B: {SB_h2:.2f} Purty: {purity_h2:.2f}"),
            (0.08, f"Sig3 yld: {S1_h3:.0f} S/B: {SB_h3:.2f} Purty: {purity_h3:.2f}"),
            (0.08, f"Sig4 yld: {S1_h4:.0f} S/B: {SB_h4:.2f} Purty: {purity_h4:.2f}"),
        ],

        # middle pad tweaks
        legend_box=(0.48, 0.18, 0.96, 0.84),
        legend_text_size=0.10,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.78,
        notes_text_size=0.12,
        notes_step=0.15,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.08, "Global cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"),
            (0.08, f"Sig1: CUT(rejectSigma1385)*CUTWT({sidebandCuts}). Sig: {S1_h1:.0f}, Bkg: {B_h1:.0f}"),
            (0.08, f"Sig2: CUT(flightLengthKShort,rejectSigma1385)*CUTWT({sidebandCuts}), Sig: {S1_h2:.0f}, Bkg:  {B_h2:.0f}"),
            (0.08, f"Sig3: CUT(flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts}), Sig: {S1_h3:.0f}, Bkg:  {B_h3:.0f}"),
            (0.08, f"Sig4: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts}), Sig: {S1_h4:.0f}, Bkg:  {B_h4:.0f}"),
        ],

        # bottom pad tweaks
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.060,
        notes_step=0.09,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")

# ------------------------------------------------------------
# KSTAR MASS PLOTS -- DATA UNUSED ENERGY STUDY STUDY
# ------------------------------------------------------------
def massPlots_KStar_unusedEnergyStudy(pdf_path):
    c = ROOT.TCanvas("c_kstar_sidebands", "c_kstar_sidebands", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hSig1 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
    )
    hSig2 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(unusedE,flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
    )
    

    hSig1.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hSig1.SetYTitle("Combinations / 40 MeV")

    hSig1.SetLineColor(ROOT.kBlack)
    hSig1.SetFillColor(ROOT.kBlue)
    hSig2.SetLineColor(ROOT.kBlack)
    # hSig2.SetFillColor(ROOT.kBlue)

    hSig1.Draw("hist")
    hSig2.Draw("pE same")

    integral_kStarSig1 = integral_between(hSig1, 0.8, 1.0)
    integral_kStarSig2 = integral_between(hSig2, 0.8, 1.0)

    # ----- Fitting
    fit1_kstar = make_two_voigtians_plus_bernstein(
        name="fit_kstar_2voigt_bern",
        # xmin, xmax for fitting (integration limits defined elsewhere).
        xmin=0.6,
        xmax=2.5,
        bern_degree=3,
        # K*(892)
        amp1=500.0, mean1=0.892, sigma1=0.003, width1=0.050,
        # K*(1430)
        amp2=200.0, mean2=1.43,  sigma2=0.003, width2=0.100,
        coeffs=[100.0, 100.0, 100.0, 100.0],
    )
    # Keep sigma physically small, let width carry the Lorentzian broadening
    fit1_kstar.SetParLimits(2, 0.0001, 0.02)   # voigt1 sigma
    fit1_kstar.SetParLimits(3, 0.010,  0.150)  # voigt1 width
    fit1_kstar.SetParLimits(6, 0.0001, 0.02)   # voigt2 sigma
    fit1_kstar.SetParLimits(7, 0.050,  0.300)  # voigt2 width
    # Bernstein coeffs must stay positive to be well-behaved
    for i in range(4):
        fit1_kstar.SetParLimits(8 + i, 0.0, 1e6)

    hSig1.Fit(fit1_kstar, "R0")
    fit1_kstar.SetLineColor(ROOT.kBlack)
    fit1_kstar.SetLineWidth(2)
    # fit1_kstar.Draw("same")

    fit2_kstar = make_two_voigtians_plus_bernstein(
        name="fit_kstar_2voigt_bern",
        # xmin, xmax for fitting (integration limits defined elsewhere).
        xmin=0.6,
        xmax=2.5,
        bern_degree=3,
        # K*(892)
        amp1=500.0, mean1=0.892, sigma1=0.003, width1=0.050,
        # K*(1430)
        amp2=400.0, mean2=1.43,  sigma2=0.003, width2=0.100,
        coeffs=[100.0, 100.0, 100.0, 100.0],
    )
    # Keep sigma physically small, let width carry the Lorentzian broadening
    fit2_kstar.SetParLimits(2, 0.0001, 0.02)   # voigt1 sigma
    fit2_kstar.SetParLimits(3, 0.010,  0.150)  # voigt1 width
    fit2_kstar.SetParLimits(6, 0.0001, 0.02)   # voigt2 sigma
    fit2_kstar.SetParLimits(7, 0.050,  0.300)  # voigt2 width
    # Bernstein coeffs must stay positive to be well-behaved
    for i in range(4):
        fit2_kstar.SetParLimits(8 + i, 0.0, 1e6)

    hSig2.Fit(fit2_kstar, "R0")
    fit2_kstar.SetLineColor(ROOT.kBlue)
    fit2_kstar.SetLineWidth(2)
    # fit2_kstar.Draw("same")


    # Extract individual voigtian and bernstein parameters from above fit.  Then plot those lines individually.
    fit_voigt1, fit_voigt2, fit_bern = make_component_funcs_kstar(fit2_kstar, xmin=0.6, xmax=2.5, bern_degree=3)
    fit_voigt1.SetLineColor(ROOT.kBlue)
    fit_voigt1.SetLineStyle(2)
    fit_voigt2.SetLineColor(ROOT.kBlue)
    fit_voigt2.SetLineStyle(2)
    fit_bern.SetLineColor(ROOT.kRed + 2)
    fit_bern.SetLineStyle(2)
    # fit_voigt1.Draw("same")
    # fit_voigt2.Draw("same")
    # fit_bern.Draw("same")

    p["plot"].Modified()
    p["plot"].Update()

    # xmin, xmax for integration.
    xmin, xmax = 0.80, 1.00
    bin_width = hSig1.GetXaxis().GetBinWidth(1)

    S1_h1, S2_h1, S_h1, B_h1, SB_h1, significance_h1, purity_h1 = compute_figureOfMerit_kstar(
        fit1_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )
    S1_h2, S2_h2, S_h2, B_h2, SB_h2, significance_h2, purity_h2 = compute_figureOfMerit_kstar(
        fit2_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )

    # draw_vertical_lines(hSig1, [0.8, 1.0], color=ROOT.kRed)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hSig1, "M(Ks #pi^{+}) Sig1 (no unused shower Int: " f"{integral_kStarSig1:.0f})", "f"),
            (hSig2, "M(Ks #pi^{+}) Sig2 (w/unused shower Int: " f"{integral_kStarSig2:.0f})", "l"),
            # (fit1_kstar, "Sig1: 2 Voigt + Bernstein fit", "l"),
            # (fit2_kstar, "Sig2: 2 Voigt + Bernstein fit", "l"),
        ],
        notes=[
            (0.08, "K*(892) yield, Sig/Bkg, purity [S/(S+B)]"),
            (0.08, f"Sig1 yld: {S1_h1:.0f} S/B: {SB_h1:.2f} Purty: {purity_h1:.2f}"),
            (0.08, f"Sig2 yld: {S1_h2:.0f} S/B: {SB_h2:.2f} Purty: {purity_h2:.2f}"),
        ],

        # middle pad tweaks
        legend_box=(0.48, 0.18, 0.96, 0.84),
        legend_text_size=0.10,

        label_pos=(0.06, 0.90),
        label_size=0.10,

        notes_start_y=0.78,
        notes_text_size=0.12,
        notes_step=0.15,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.08, "Global cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"),
            (0.08, f"Sig1: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts}), Sig: {S1_h1:.0f}, Bkg:  {B_h1:.0f}"),
            (0.08, f"Sig2: CUT(unusedE,flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts}), Sig: {S1_h2:.0f}, Bkg:  {B_h2:.0f}"),
        ],

        # bottom pad tweaks
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.060,
        notes_step=0.09,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")

def missingMassPlots_KStar_sidebands(pdf_path):
    c = ROOT.TCanvas("c_mm_kstar_sidebands", "c_mm_kstar_sidebands", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingLambda})",
        "(50,0.5,2.5)",
        f"CUT({baseCuts},{sidebandCuts})"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingLambda})",
        "(50,0.5,2.5)",
        f"CUT({baseCuts})*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS(GLUEXTARGET,GLUEXBEAM,-{DecayingLambda})",
        "(50,0.5,2.5)",
        f"CUT({baseCuts})*CUTSBWT({sidebandCuts})"
    )
    hBkgNegative = hBkg.Clone("hBkgNegative_MM_KStar")
    keep(hBkgNegative)
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("MM(K*) [GeV/c^{2}]")
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
            (hData, "MM(K*): Data " "(Integral: " f"{integral_kStar:.0f})", "pE"),
            (hSig, "MM(K*): Signal " "(Integral: " f"{integral_kStarSig:.0f})", "f"),
            (hBkgNegative, "MM(K*): Background " "(Integral: " f"{integral_kStarBkg:.0f})", "f"),
        ],
        notes=[
            "K* missing-mass sideband subtraction study",
            "Selecting K*(892) mass region from",
            "MM(#Lambda) = (0.8, 1.0) GeV/c^{2}",
        ],
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
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.68,
        notes_text_size=0.075,
        notes_step=0.16,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")


# ------------------------------------------------------------
# KSTAR MASS PLOTS -- FINAL SELECTION
# ------------------------------------------------------------
def massPlots_KStar_FINAL_SELECTION(pdf_path):
    c = ROOT.TCanvas("c_kstar_sidebands", "c_kstar_sidebands", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hData = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,rf,KShort,Lambda)"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(50,0.5,2.5)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTSBWT({sidebandCuts})"
    )
    hBkgNegative = hBkg.Clone("hBkgNegative")
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Combinations / 40 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hData.SetLineColor(ROOT.kBlack)
    hSig.SetLineColor(ROOT.kBlue - 3)
    hSig.SetFillColor(ROOT.kBlue - 3)
    hBkgNegative.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetFillColor(ROOT.kRed)

    hData.Draw("pE")
    hSig.Draw("hist same")
    hBkgNegative.Draw("hist same")

    integral_kStarData = integral_between(hData, 0.8, 1.0)
    integral_kStarSig  = integral_between(hSig,  0.8, 1.0)
    integral_kStarBkg  = integral_between(hBkg,  0.8, 1.0)

    # ----- Fit setup (shared limits)
    def _apply_kstar_limits(f):
        f.FixParameter(2, 0.003) # voigt1 sigma - detector res only
        f.SetParLimits(3, 0.030,  0.200) # voigt1 width - K*(892) PDG ~50 MeV
        f.FixParameter(6, 0.003) # voigt2 sigma
        f.SetParLimits(7, 0.050,  0.500) # voigt2 width - K*(1430) is broad
        for i in range(4):
            f.SetParLimits(8 + i, 0.0, 1e6)

    def _make_kstar_fit(name, amp2=200.0):
        return make_two_voigtians_plus_bernstein(
            name=name, xmin=0.6, xmax=2.5, bern_degree=3,
            amp1=1000.0, mean1=0.892, sigma1=0.002, width1=0.050,
            amp2=400.0,  mean2=1.43,  sigma2=0.002, width2=0.200,
            coeffs=[100.0, 100.0, 100.0, 100.0],
        )

    fitData_kstar = _make_kstar_fit("fitData_kstar_2voigt_bern", amp2=200.0)
    _apply_kstar_limits(fitData_kstar)
    hData.Fit(fitData_kstar, "R0")
    log_fit_results(fitData_kstar,
                    hist_name="hData",
                    cut_string="CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,rf,KShort,Lambda)",
                    xmin=0.6, xmax=2.5,
                    notes=["FOM integration range: (0.80, 1.00)"])
    fitData_kstar.SetLineColor(ROOT.kBlack)
    fitData_kstar.SetLineWidth(2)

    fitSig_kstar = _make_kstar_fit("fitSig_kstar_2voigt_bern", amp2=400.0)
    _apply_kstar_limits(fitSig_kstar)
    hSig.Fit(fitSig_kstar, "R0")
    log_fit_results(fitSig_kstar,
                    hist_name="hSig",
                    cut_string=f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})",
                    xmin=0.6, xmax=2.5,
                    notes=["FOM integration range: (0.80, 1.00)"])
    fitSig_kstar.SetLineColor(ROOT.kMagenta + 2)
    fitSig_kstar.SetLineWidth(3)
    fitSig_kstar.Draw("same")

    fitBkg_kstar = _make_kstar_fit("fitBkg_kstar_2voigt_bern", amp2=400.0)
    _apply_kstar_limits(fitBkg_kstar)
    hBkg.Fit(fitBkg_kstar, "R0")
    log_fit_results(fitBkg_kstar,
                    hist_name="hBkg",
                    cut_string=f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTSBWT({sidebandCuts})",
                    xmin=0.6, xmax=2.5,
                    notes=["FOM integration range: (0.80, 1.00)"])
    fitBkg_kstar.SetLineColor(ROOT.kBlue)
    fitBkg_kstar.SetLineWidth(2)

    fit_voigt1, fit_voigt2, fit_bern = make_component_funcs_kstar(fitSig_kstar, xmin=0.6, xmax=2.5, bern_degree=3)
    fit_voigt1.SetLineColor(ROOT.kMagenta + 2)
    fit_voigt1.SetLineStyle(2)
    fit_voigt2.SetLineColor(ROOT.kMagenta + 2)
    fit_voigt2.SetLineStyle(2)
    fit_bern.SetLineColor(ROOT.kMagenta + 2)
    fit_bern.SetLineStyle(2)
    fit_voigt1.Draw("same")
    fit_voigt2.Draw("same")
    fit_bern.Draw("same")

    p["plot"].Modified()
    p["plot"].Update()

    xmin, xmax = 0.80, 1.00
    bin_width = hData.GetXaxis().GetBinWidth(1)

    S1_h1, S2_h1, S_h1, B_h1, SB_h1, significance_h1, purity_h1 = compute_figureOfMerit_kstar(
        fitData_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )
    S1_h2, S2_h2, S_h2, B_h2, SB_h2, significance_h2, purity_h2 = compute_figureOfMerit_kstar(
        fitSig_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )
    S1_h3, S2_h3, S_h3, B_h3, SB_h3, significance_h3, purity_h3 = compute_figureOfMerit_kstar(
        fitBkg_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData,        f"M(Ks #pi^{{+}}) Data Int: {integral_kStarData:.0f}",       "pE"),
            (hSig,         f"M(Ks #pi^{{+}}) Signal Int: {integral_kStarSig:.0f}",       "f"),
            (hBkgNegative, f"M(Ks #pi^{{+}}) Background Int: {integral_kStarBkg:.0f}",   "f"),
            (fitSig_kstar, "Fit signal: 2 Voigtians + Bernstein",                         "l"),
            (fit_voigt1,   "Fit signal: Voigtian [K*(892)]",                              "l"),
            (fit_bern,     "Fit signal: Bernstein",                                       "l"),
        ],
        notes=[
            (0.08, "Integrals: M(Ks #pi^{+}) = (0.8, 1.0) GeV/c^{2}"),
            (0.08, "K*(892) yield, Sig/Bkg, Purity S/(S+B):"),
            (0.08, f"Sig. yield: {S1_h2:.0f}  S/B: {SB_h2:.2f}  Purity: {purity_h2:.2f}"),
        ],
        legend_box=(0.48, 0.18, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.10,
        notes_start_y=0.78,
        notes_text_size=0.12,
        notes_step=0.15,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.08, "Global cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"),
            (0.08, f"Data: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,rf,KShort,Lambda). Sig: {S1_h1:.0f}, Bkg: {B_h1:.0f}"),
            (0.08, f"Sig:  CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts}). Sig: {S1_h2:.0f}, Bkg: {B_h2:.0f}"),
            (0.08, f"Bkg:  CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTSBWT({sidebandCuts}). Sig: {S1_h3:.0f}, Bkg: {B_h3:.0f}"),
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.72,
        notes_text_size=0.060,
        notes_step=0.09,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")


def massPlots_KStar_FINAL_SELECTION_ROOFIT(pdf_path):
    c = ROOT.TCanvas("c_kstar_roofit", "c_kstar_roofit", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    roofit_file = ROOT.TFile.Open(FND_fits, "READ")
    h_Pwave = roofit_file.Get("h_Pwave")
    h_Pwave.SetDirectory(0)

    curve_total = vecs_to_tgraph(roofit_file, "curve_total_x", "curve_total_y", "curve_total")
    curve_sig   = vecs_to_tgraph(roofit_file, "curve_sig_x",   "curve_sig_y",   "curve_sig")
    curve_bkg   = vecs_to_tgraph(roofit_file, "curve_bkg_x",   "curve_bkg_y",   "curve_bkg")

    # Import figures of merit (calculated in C++ RooFit script)
    fom = roofit_file.Get("figures_of_merit")
    if fom:
        S, B, SoverB, purity = fom[0], fom[1], fom[2], fom[3]
    else:
        print("WARNING: figures_of_merit not found in ROOT file - run C++ script first")
        S, B, SoverB, purity = 0., 0., 0., 0.

    roofit_file.Close()
    keep(h_Pwave)

    h_Pwave.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    h_Pwave.SetYTitle("Combinations / 40 MeV")
    h_Pwave.SetLineColor(ROOT.kBlack)
    h_Pwave.SetMinimum(-1.2 * abs(h_Pwave.GetMinimum()))
    h_Pwave.Draw("pE")

    if curve_total:
        curve_total.SetLineColor(ROOT.kMagenta + 2)
        curve_total.SetLineWidth(3)
        curve_total.Draw("same")
    if curve_sig:
        curve_sig.SetLineColor(ROOT.kOrange)
        curve_sig.SetLineStyle(ROOT.kDotted)
        curve_sig.SetLineWidth(2)
        curve_sig.Draw("same")
    if curve_bkg:
        curve_bkg.SetLineColor(ROOT.kOrange + 7)
        curve_bkg.SetLineStyle(ROOT.kDotted)
        curve_bkg.SetLineWidth(2)
        curve_bkg.Draw("same")

    integral_kStarSig = integral_between(h_Pwave, 0.8, 1.0)

    p["plot"].Modified()
    p["plot"].Update()

    legend_items = [
        (h_Pwave,     f"M(Ks #pi^{{+}}) RooFit sideband-subtracted Int: {integral_kStarSig:.0f}", "pE"),
        (curve_total, "Total Fit: interfering 2 RBW + Bernstein", "l") if curve_total else None,
        (curve_sig,   "Fit: signal (2 Relativistic BW)",                "l") if curve_sig   else None,
        (curve_bkg,   "Fit: background (Bernstein)",        "l") if curve_bkg   else None,
    ]
    legend_items = [item for item in legend_items if item is not None]

    draw_info_pad(
        p["info_main"],
        file_label(FND_fits),
        legend_items=legend_items,
        notes=[
            (0.08, "Integrals: M(Ks #pi^{+}) = (0.8, 1.0) GeV/c^{2}"),
            (0.08, "K*(892) yield, Sig/Bkg, Purity S/(S+B):"),
            (0.08, f"Sig. yield: {S:.0f}  S/B: {SoverB:.2f}  Purity: {purity:.2f}"),
        ],
        legend_box=(0.48, 0.18, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.10,
        notes_start_y=0.78,
        notes_text_size=0.12,
        notes_step=0.15,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.08, "Global cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"),
            (0.08, f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"),
            (0.08, f"K*(892) region: (0.80, 1.00) GeV. Sig: {S:.0f}, Bkg: {B:.0f}"),
            (0.08, "Full fit: RooFit C++ script (interfering 2 RBW + Bernstein)"),
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.72,
        notes_text_size=0.060,
        notes_step=0.09,
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
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"

    )
    hMC = fs_get_th1(
        FND_eventSelectionSkims_MC,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(100,0.5,2.5)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
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
# ANGULAR PLOTS
# ------------------------------------------------------------

# ---------- cosThetaGJ AMPTOOLS INPUT FILE -----------
def cosThetaGJ_KShort(pdf_path):
    c = ROOT.TCanvas("c_costheta_gj", "c_costheta_gj", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h = fs_get_th1(
        FND_signalSkims,
        f"GJCOSTHETA({DecayingKShort};{PiPlus1};GLUEXBEAM)",
        "(36,-1.0,1.0)",
        f"CUT()*CUTWT(rf,KShort,Lambda)"
    )

    h.SetXTitle("cos#theta_{GJ}(K_{S})")
    h.SetYTitle("10 degrees / bin")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("pE")

    integral = integral_between(h,-1.0,1.0)


    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims) + "#bf{ Not acceptance-corrected}",
        legend_items=[(h, "AmpTools input file", "pE")],
        notes=[
            "#bf{Integral (-1.0, 1.0): }" f"{integral:.0f}",
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
            (0.08, "#bf{General skim:} CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,"),
            (0.10, "targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.08, "#bf{Signal skim:} CUT(rf,KShort,Lambda)"),
            (0.08, "#bf{Histogram cuts:} CUT()*CUTWT(rf,KShort,Lambda)"),
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
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort,Lambda)*CUTWT(rf,KShort,Lambda)"
    )

    integral = integral_between(h,-1.0,1.0)

    h.SetXTitle("cos#theta_{Helicity}(K_{S})")
    h.SetYTitle("10 degrees / bin")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("pE")

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims) + "#bf{ (Not acceptance-corrected)}",
        legend_items=[(h, "event selection skim", "pE")],
        notes=[
            "#bf{Integral (-1.0, 1.0): }" f"{integral:.0f}",
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
            (0.08, "GeneralCuts_eventSelection: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"),
            (0.08, "Histogram cuts: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.10, "rf,KShort,Lambda)*CUTWT(rf,KShort,Lambda)"),
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
        "CUT()*CUTWT(rf,KShort,Lambda)",
    )


    integral = integral_between(h,-1.0,1.0)

    h.SetXTitle("cos#theta_{Helicity}(K_{S})")
    h.SetYTitle("10 degrees / bin")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("pE")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims) + "#bf{ (Not acceptance-corrected)}",
        legend_items=[(h, "AmpTools input file", "pE")],
        notes=[
            "#bf{Integral (-1.0, 1.0): }" f"{integral:.0f}",
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
            (0.08, "#bf{General skim:} CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,"),
            (0.10, "targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.08, "#bf{Signal skim:} CUT(rf,KShort,Lambda)"),
            (0.08, "#bf{Histogram cuts:} CUT()*CUTWT(rf,KShort,Lambda)"),
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
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};{DecayingLambda}):MASS({DecayingLambda},{PiPlus1})",
        "(36, 1.20,3.60, 36,-1.0,1.0)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,rf,KShort,Lambda)*CUTWT(rf,KShort,Lambda)"
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
        file_label(FND_eventSelectionSkims) + "#bf{ (Not acceptance-corrected)}",
        legend_items=[(h, "Event Selection skim", "colz")],
        notes=[
            # "#bf{Integral (-1.0, 0.5): }" f"{integral:.0f}",
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
            (0.08, "GeneralCuts_eventSelection: CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,targetZ)"),
            (0.10, "Histogram cuts: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892,"),
            (0.08, "rf,KShort,Lambda)*CUTWT(rf,KShort,Lambda)"),
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
        f"HELCOSTHETA({DecayingKShort};{PiPlus1};{DecayingLambda}):MASS({DecayingLambda},{PiPlus1})",
        "(36, 1.20,3.60, 36,-1.0,1.0)",
        f"CUT()*CUTWT(rf,KShort,Lambda)"
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
        legend_items=[(h, "AmpTools input file", "colz")],
        notes=[
            # "#bf{Integral (-1.0, 0.5): }" f"{integral:.0f}",
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
            (0.08, "#bf{General skim:} CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,"),
            (0.10, "targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.08, "#bf{Signal skim:} CUT(rf,KShort,Lambda)"),
            (0.08, "#bf{Histogram cuts:} CUT()*CUTWT(rf,KShort,Lambda)"),
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



# ------- cosTheta Helicity MC AMPTOOLS INPUT FILE --------
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
        "CUT()*CUTWT(rf,KShort,Lambda)"
    )

    integral = integral_between(h,-1.0,1.0)

    h.SetXTitle("cos#theta_{Helicity}(K_{S})")
    h.SetYTitle("10 degrees / bin")
    h.GetXaxis().SetNdivisions(505)
    h.SetLineColor(ROOT.kBlack)
    h.SetLineWidth(2)
    h.SetMarkerStyle(20)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetMarkerSize(0.8)
    h.SetMinimum(0.0)
    h.Draw("pE")

    draw_info_pad(
        p["info_main"],
        file_label(FND_signalSkims_MC),
        legend_items=[(h, "AmpTools input file", "pE")],
        notes=[
            "#bf{Integral (-1.0, 1.0): }" f"{integral:.0f}",
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
            (0.08, "#bf{General skim:} CUT(tRange110,chi2DOF,unusedE,unusedTracks,coherentPeak,"),
            (0.10, "targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.08, "#bf{Signal skim:} CUT(rf,KShort,Lambda)"),
            (0.08, "#bf{Histogram cuts:} CUT()*CUTWT(rf,KShort,Lambda)"),
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
        f"CUT()*CUTWT(rf,KShort,Lambda)"
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
            (0.08, "CUT()*CUTWT(rf,KShort,Lambda)"),
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
    # deltaTPlots_KShort_vs_PiPlus(allPlots)
    # deltaTPrimePlots_KShort_vs_PiPlus(allPlots)
    # massPlots_KShort_cutComparisons(allPlots)
    # massPlots_KShort_flightLength(allPlots)
    # massPlots_KShort_sideBands(allPlots)
    # massPlots_KShort_missingMass(allPlots)
    # massPlots_KShort_FINAL_SELECTION(allPlots)
    # massPlots_Lambda_flightLength(allPlots)
    # massPlots_Lambda_sideBands(allPlots)
    # massPlots_Lambda_missingMass(allPlots)
    # massPlots_Lambda_FINAL_SELECTION(allPlots)
    # deltaMassPlots_KShort(allPlots)
    # deltaMassPlots_Lambda(allPlots)
    # massPlots_lambdaPiBackground(allPlots)
    # massPlots_KStar_flightLength(allPlots)
    # massPlots_KStar_unusedEnergyStudy(allPlots)
    # massPlots_KStar_FINAL_SELECTION(allPlots)
    massPlots_KStar_FINAL_SELECTION_ROOFIT(allPlots)
    # missingMassPlots_KStar_sidebands(allPlots)
    # massPlots_KStar_Signal_DATA_and_MC(allPlots)
    # massPlots_KStar_FIT_RESULTS(allPlots)
    # cosThetaGJ_KShort(allPlots)
    # cosThetaHelicity_KShort_eventSelectionSkim(allPlots)
    # cosThetaHelicity_KShort_ampToolsSkim(allPlots)
    # cosTheta_vs_lambdaPi_eventSelection(allPlots)
    # cosTheta_vs_lambdaPi_ampToolsSkim(allPlots)
    # cosThetaHelicity_KShort_MC(allPlots)
    # efficiency_cosThetaHelicity_KShort(allPlots)

    dt = time.time() - t0
    print(f"Total execution time: {dt:.1f} s")


if __name__ == "__main__":
    main()