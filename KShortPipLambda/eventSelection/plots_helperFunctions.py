#!/usr/bin/env python3
import ROOT
import textwrap

"""
plots_helperFunctions.py
------------
Shared helper functions for the KShort-Pip-Lambda / K*(892) analysis.

Import this module in any script that needs to create panel grids or draw info pads.

# Usage:

"""
NT = "ntFSGlueX_MODECODE"
MODE_STRING = "m100000000_1100"
# Keep ROOT objects alive
_KEEP = []

def keep(obj):
    _KEEP.append(obj)
    return obj

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
def log_fit_results(f, hist_name, cut_string, xmin, xmax, logFile, notes=None):
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
    h = ROOT.FSModeHistogram.getTH1F(file_name, NT, MODE_STRING, expr, bins, cuts)
    keep(h)
    return h


def fs_get_th2(file_name, expr, bins, cuts):
    h = ROOT.FSModeHistogram.getTH2F(file_name, NT, MODE_STRING, expr, bins, cuts)
    keep(h)
    return h


def draw_mc_same(file_name, expr, bins, cuts):
    ROOT.FSModeHistogram.drawMCComponentsSame(file_name, NT, MODE_STRING, expr, bins, cuts)
