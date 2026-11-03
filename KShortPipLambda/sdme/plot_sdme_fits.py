#!/usr/bin/env python
"""plot_sdme_fits.py

Draw the nine K*(892) spin-density matrix elements (SDMEs) versus -t from a
folder of AmpTools TwoPiAngles .fit files (one fit per t-bin), in the standard
3x3 paper layout.

Workflow
--------
Point it at a folder containing one .fit file per t-bin:

    python plot_sdme_fits.py /path/to/fit_folder
    python plot_sdme_fits.py /path/to/fit_folder -o plots/sdme_fit_plots.pdf
    python plot_sdme_fits.py /path/to/fit_folder --fixed-ranges --recursive

The -t range of each bin is parsed from the filename token 't<lo><hi>', where
each pair of digits is read as tenths of GeV^2 (e.g. 't0103' -> -t = 0.1-0.3),
matching the KShortPipLambda naming convention. Files without a recognizable
t-token are skipped with a warning. Edit T_TOKEN_RE / parse_t_range below if
your naming differs.

Each panel plots the SDME value at the bin center with a horizontal bar over
the bin width and a vertical bar for the Minuit error, plus the SCHC+NPE
reference line (0 for all elements except rho^1_{1-1}=+1/2 and
Im rho^2_{1-1}=-1/2).
"""

import argparse
import glob
import os
import re
import sys
import csv

import ROOT

ROOT.gROOT.SetBatch(True)

# -----------------------------------------------------------------------------
# Panel definitions -- order is row-major to match the reference figure.
# Parameter names follow rho<m><m'><alpha>.
#   (param name, y-axis LaTeX label, SCHC+NPE line, paper ymin, paper ymax)
# -----------------------------------------------------------------------------

SDME_PANELS = [
    ("rho000",  "#rho^{0}_{00}",     0.0,  -1.00,  1.00),
    ("rho100",  "Re #rho^{0}_{10}",   0.0,  -1.00,  1.00),
    ("rho1m10", "#rho^{0}_{1-1}",    0.0,  -1.00,  1.00),
    ("rho111",  "#rho^{1}_{11}",     0.0,  -1.00,  1.00),
    ("rho001",  "#rho^{1}_{00}",     0.0,  -1.00,  1.00),
    ("rho101",  "Re #rho^{1}_{10}",   0.0,  -1.00,  1.00),
    ("rho1m11", "#rho^{1}_{1-1}",    0.0,  -1.00,  1.00),
    ("rho102",  "Im #rho^{2}_{10}",   0.0,  -1.00,  1.00),
    ("rho1m12", "Im #rho^{2}_{1-1}",  0.0,  -1.00,  1.00),
]

# D.Barton Zlm->SDME projections for K*(892)
MY_COLS = {
    "rho000":"rho0_00", "rho100":"Re_rho0_10", "rho1m10":"rho0_1m1",
    "rho111":"rho1_11", "rho001":"rho1_00",    "rho101":"Re_rho1_10",
    "rho1m11":"rho1_1m1","rho102":"Im_rho2_10","rho1m12":"Im_rho2_1m1",
}

# filename token: t<2 digits><2 digits>, each read as tenths of GeV^2
T_TOKEN_RE = re.compile(r"t(\d{2})(\d{2})")

def load_my_zlm_ref(csv_path, variant):
    """My Zlm->SDME projections for one waveset.
       variant: 'onlyPwave_BW', 'SPwave_BW', or 'SPwave' (no BW).
       Returns {par: [(t_center, value, err), ...]} sorted by t."""
    ref = {p: [] for p in MY_COLS}
    with open(csv_path) as fh:
        for row in csv.DictReader(fh):
            tag = row["folder"].split("fit_PWA_")[1].rsplit("_t", 1)[0]
            if tag != variant:          # exact match: 'SPwave' != 'SPwave_BW'
                continue
            tok = T_TOKEN_RE.search(row["folder"])
            if not tok:
                continue
            t = 0.5 * (int(tok.group(1))/10.0 + int(tok.group(2))/10.0)
            for par, col in MY_COLS.items():
                ref[par].append((t, float(row[col]), float(row[col + "_err"])))
    for p in ref:
        ref[p].sort(key=lambda x: x[0])
    return ref

MY_CSV = "/work/halld/home/dbarton/gluex/KShortPipLambda/PWA/fits/sdme_from_zlm_combined.csv"
MY_PONLY   = load_my_zlm_ref(MY_CSV, "onlyPwave_BW")
MY_SP_BW   = load_my_zlm_ref(MY_CSV, "SPwave_BW")
MY_SP_NOBW = load_my_zlm_ref(MY_CSV, "SPwave")


# Schilling fits from Hao (09/30/2026)
def load_schilling_ref(csv_path):
    """Hao's Schilling-model SDMEs -> {par: [(t_center, value, err), ...]}."""
    pars = ["rho000","rho100","rho1m10","rho111","rho001",
            "rho101","rho1m11","rho102","rho1m12"]
    ref = {p: [] for p in pars}
    with open(csv_path) as fh:
        for row in csv.DictReader(fh):
            t = float(row["t_center"])
            for p in pars:
                ref[p].append((t, float(row[p]), float(row[p + "_err"])))
    return ref

HAO_DIR = "/work/halld/home/dbarton/gluex/KShortPipLambda/sdme/fits/Hao_fit_results"
SCHILLING_REF = load_schilling_ref(f"{HAO_DIR}/SDMEs_SchillingModel_Hao_09302026.csv")
ZLM_P_REF     = load_schilling_ref(f"{HAO_DIR}/SDMEs_ZLM_P_only_Hao.csv")
ZLM_SP_REF    = load_schilling_ref(f"{HAO_DIR}/SDMEs_ZLM_SP_Hao.csv")

_KEEP = []  # keep ROOT objects alive


# -----------------------------------------------------------------------------
# AmpTools / ROOT setup
# -----------------------------------------------------------------------------
def load_amptools():
    """Load AmpTools libraries so ROOT.FitResults is available."""
    try:
        from pyamptools import atiSetup
        atiSetup.setup(globals(), use_fsroot=True)
    except Exception as exc:
        print(f"WARNING: pyamptools atiSetup failed ({exc}).")
        print("         Falling back to assuming AmpTools is already on the ROOT path.")
    if not hasattr(ROOT, "FitResults"):
        raise RuntimeError(
            "ROOT.FitResults is not available. Load the AmpTools libraries first "
            "(e.g. via 'source setup_gluex.csh' and atiSetup)."
        )

# helper function to draw a grid of lines at the given x and y ticks, since ROOT's built-in grid doesn't work.
def draw_grid(pad, tmin, tmax, ymin, ymax, xticks, yticks):
    pad.cd()
    for x in xticks:
        l = ROOT.TLine(x, ymin, x, ymax)
        l.SetLineColor(ROOT.kGray); l.SetLineStyle(1); l.SetLineWidth(1)
        l.Draw(); _KEEP.append(l)
    for y in yticks:
        l = ROOT.TLine(tmin, y, tmax, y)
        l.SetLineColor(ROOT.kGray); l.SetLineStyle(1); l.SetLineWidth(1)
        l.Draw(); _KEEP.append(l)


# -----------------------------------------------------------------------------
# File discovery / parsing
# -----------------------------------------------------------------------------
def parse_t_range(fit_path):
    """(t_low, t_high) in GeV^2 from the 't<lo><hi>' token.

    Tries the filename first, then the data-file paths in the .fit file's
    embedded config (e.g. '..._t0103_pol0.root'). Returns None if not found.
    """
    m = T_TOKEN_RE.search(os.path.basename(fit_path))
    if m:
        return int(m.group(1)) / 10.0, int(m.group(2)) / 10.0
    try:
        with open(fit_path, "r", errors="ignore") as fh:
            for line in fh:
                s = line.lstrip()
                if s.startswith(("data ", "bkgnd ", "accmc ", "genmc ")):
                    m = T_TOKEN_RE.search(s)
                    if m:
                        return int(m.group(1)) / 10.0, int(m.group(2)) / 10.0
    except OSError:
        pass
    return None

def read_best_minimum(fit_path):
    """The fit's bestMinimum (NLL) from the .fit text, or None."""
    try:
        with open(fit_path, "r", errors="ignore") as fh:
            for line in fh:
                parts = line.split()
                if len(parts) == 2 and parts[0] == "bestMinimum":
                    return float(parts[1])
    except (OSError, ValueError):
        pass
    return None

def find_fit_bins(fit_dir, recursive=False, t_override=None):
    """Scan for .fit files, group by t-bin, keep the best (lowest-NLL) fit each.

    Returns (bins, skipped): bins is [(best_fit_path, t_low, t_high)] sorted by
    t_low; skipped lists files with no resolvable t-range.
    """
    pattern = os.path.join(fit_dir, "**", "*.fit") if recursive \
        else os.path.join(fit_dir, "*.fit")
    files = sorted(glob.glob(pattern, recursive=recursive))

    groups, skipped = {}, []
    for f in files:
        tr = t_override if t_override is not None else parse_t_range(f)
        if tr is None:
            skipped.append(f)
            continue
        groups.setdefault(tr, []).append((f, read_best_minimum(f)))

    bins = []
    for (t_lo, t_hi), members in groups.items():
        # lowest NLL wins; files with no NLL sink to the bottom
        best_path = sorted(members, key=lambda m: (m[1] is None, m[1]))[0][0]
        if len(members) > 1:
            print(f"  -t = {t_lo:.2f}-{t_hi:.2f}: {len(members)} fits, "
                  f"using best NLL -> {os.path.basename(best_path)}")
        bins.append((best_path, t_lo, t_hi))
    bins.sort(key=lambda b: b[1])
    return bins, skipped


def read_sdmes_from_fit(fit_path, par_names):
    """{par_name: (value, error)} from a .fit file via AmpTools FitResults."""
    results = ROOT.FitResults(fit_path)
    if not results.valid():
        raise RuntimeError(f"Invalid fit results in file: {fit_path}")
    out = {}
    for name in par_names:
        out[name] = (results.parValue(name), results.parError(name))
    return out

def read_parity_asym_from_fit(fit_path):
    """P_sigma = 2*rho^1_{1-1} - rho^1_{00}, with full 2-parameter error propagation.
       Returns (P_sigma, error)."""
    r = ROOT.FitResults(fit_path)
    if not r.valid():
        raise RuntimeError(f"Invalid fit results: {fit_path}")
    a, b = "rho1m11", "rho001"          # rho^1_{1-1}, rho^1_{00}
    va, vb = r.parValue(a), r.parValue(b)
    ea, eb = r.parError(a), r.parError(b)
    cov    = r.covariance(a, b)
    P   = 2.0*va - vb
    var = 4.0*ea*ea + eb*eb - 4.0*cov   # sigma_P^2 = 4 var_a + var_b - 4 cov
    return P, (var**0.5 if var > 0 else 0.0)

def parity_from_csv(ref_dict):
    """P_sigma per t-bin from a loaded SDME dict (naive error, no covariance)."""
    out = []
    for (t, a, ea), (_, b, eb) in zip(ref_dict["rho1m11"], ref_dict["rho001"]):
        out.append((t, 2.0*a - b, (4.0*ea*ea + eb*eb)**0.5))
    return out


def parity_asym_plot(fit_bins, out_path="plots/parity_asym.pdf",
                     tmin=0.0, tmax=2.5, ref="mine"):
    outdir = os.path.dirname(out_path)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    ROOT.gStyle.SetEndErrorSize(5)

    # --- your Schilling points, exact propagation from the .fit files ---
    my_t, my_th, my_P, my_E = [], [], [], []
    for fit_path, t_lo, t_hi in fit_bins:
        P, E = read_parity_asym_from_fit(fit_path)
        my_t.append(0.5*(t_lo+t_hi)); my_th.append(0.5*(t_hi-t_lo))
        my_P.append(P); my_E.append(E)
    n = len(my_t)

    # --- overlay series (naive errors from CSVs) ---
    if ref == "hao":
        overlays = [
            (SCHILLING_REF, ROOT.kGreen+2,  24, -0.03, "Schilling (K+pi0)"),
            (ZLM_P_REF,     ROOT.kOrange+7, 24,  0.00, "Zlm P only (K+pi0)"),
            (ZLM_SP_REF,    ROOT.kBlue+1,   24,  0.03, "Zlm S+P (K+pi0)"),
        ]
    else:
        overlays = [
            (MY_PONLY,   ROOT.kOrange+7, 25, -0.01, "Zlm P-only, BW"),
            (MY_SP_BW,   ROOT.kBlue+1,   26,  0.01, "Zlm S+P, BW"),
            (MY_SP_NOBW, ROOT.kRed+1,    32,  0.03, "Zlm S+P, no BW"),
        ]

    c = ROOT.TCanvas("c_parity", "Parity asymmetry", 1100, 850)

    leg_pad = ROOT.TPad("pleg_pad", "pleg_pad", 0.0, 0.90, 1.0, 1.0)
    leg_pad.SetFillStyle(0); leg_pad.SetBorderMode(0); leg_pad.Draw()

    pad = ROOT.TPad("pplot_pad", "pplot_pad", 0.0, 0.0, 1.0, 0.90)
    pad.SetFillStyle(0); pad.SetBorderMode(0)
    pad.SetLeftMargin(0.15); pad.SetRightMargin(0.05)
    pad.SetBottomMargin(0.14); pad.SetTopMargin(0.02)
    pad.Draw(); pad.cd()
    _KEEP.extend([leg_pad, pad])

    ymin, ymax = -1.2, 1.2
    frame = pad.DrawFrame(tmin, ymin, tmax, ymax)
    frame.SetLineWidth(1)
    frame.GetXaxis().SetTitle("#minus t (GeV^{2})"); frame.GetXaxis().CenterTitle(True)
    frame.GetYaxis().SetTitle("P_{#sigma} = 2#rho^{1}_{1-1} #minus #rho^{1}_{00}")
    for ax in (frame.GetXaxis(), frame.GetYaxis()):
        ax.SetTitleFont(132); ax.SetLabelFont(132); ax.SetTitleSize(0.05); ax.SetLabelSize(0.045)
    frame.GetYaxis().SetTitleOffset(1.35)

    draw_grid(pad, tmin, tmax, ymin, ymax,
              xticks=[0.5, 1.0, 1.5, 2.0], yticks=[-1.0, -0.5, 0.0, 0.5, 1.0])

    # reference line: pure natural-parity-exchange limit
    for yref in (1.0,):            # add -1.0 here if you want the UPE line too
        l = ROOT.TLine(tmin, yref, tmax, yref)
        l.SetLineColor(ROOT.kGray+2); l.SetLineStyle(2); l.SetLineWidth(1); l.Draw()
        _KEEP.append(l)

    # your black points (exact errors)
    gr = ROOT.TGraphErrors(n)
    for j in range(n):
        gr.SetPoint(j, my_t[j], my_P[j]); gr.SetPointError(j, my_th[j], my_E[j])
    gr.SetMarkerStyle(20); gr.SetMarkerSize(1.0)
    gr.SetMarkerColor(ROOT.kBlack); gr.SetLineColor(ROOT.kBlack); gr.SetLineWidth(2)
    gr.Draw("P same"); _KEEP.append(gr)

    # overlays
    handles = {}
    for ref_dict, col, mk, dx, lbl in overlays:
        pts = parity_from_csv(ref_dict)
        if not pts: continue
        go = ROOT.TGraphErrors(len(pts))
        for j, (t, P, E) in enumerate(pts):
            go.SetPoint(j, t+dx, P); go.SetPointError(j, 0.0, E)
        go.SetMarkerStyle(mk); go.SetMarkerSize(1.0)
        go.SetMarkerColor(col); go.SetLineColor(col); go.SetLineWidth(2)
        go.Draw("P same"); _KEEP.append(go); handles[lbl] = go

    leg_pad.cd()
    leg = ROOT.TLegend(0.10, 0.05, 0.90, 0.95)   # fills the strip
    leg.SetBorderSize(0); leg.SetFillStyle(0); leg.SetTextFont(132); leg.SetTextSize(0.40)
    leg.SetNColumns(2)
    leg.AddEntry(gr, "Schilling (this analysis)", "pe")
    for _d,_c,_m,_dx,lbl in overlays:
        if lbl in handles: leg.AddEntry(handles[lbl], lbl, "pe")
    leg.Draw(); _KEEP.append(leg)

    pad.RedrawAxis()
    c.Update(); c.Print(out_path); _KEEP.append(c)
    return c


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def sdme_vs_t_plots(fit_bins, out_path="plots/sdme_fit_plots.pdf",
                    tmin=0.0, tmax=2.5, fixed_ranges=False, ref="mine"):
    """
    fit_bins: list of (fit_path, t_low, t_high). Point drawn at bin center with
              a horizontal bar over [t_low, t_high].
    fixed_ranges: True  -> reference paper y-ranges (panels line up like the figure)
                  False -> auto-range each panel to your data (nothing clips)
    """
    outdir = os.path.dirname(out_path)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    par_names = [p[0] for p in SDME_PANELS]

    ROOT.gStyle.SetEndErrorSize(2)   # error-bar end-cap length; 0 = no caps

    t_centers, t_halfwidths = [], []
    values = {name: [] for name in par_names}
    errors = {name: [] for name in par_names}
    for fit_path, t_lo, t_hi in fit_bins:
        res = read_sdmes_from_fit(fit_path, par_names)
        t_centers.append(0.5 * (t_lo + t_hi))
        t_halfwidths.append(0.5 * (t_hi - t_lo))
        for name in par_names:
            values[name].append(res[name][0])
            errors[name].append(res[name][1])

    n = len(t_centers)
    if n == 0:
        raise ValueError("No fit bins to plot.")

    c = ROOT.TCanvas("c_sdme_vs_t", "SDME vs -t", 1300, 920)

    # Top strip for the legend (top 8% of the canvas)
    leg_pad = ROOT.TPad("leg_pad", "leg_pad", 0.0, 0.92, 1.0, 1.0)
    leg_pad.SetFillStyle(0); leg_pad.SetBorderMode(0)
    leg_pad.Draw()

    # Bottom pad holds the 3x3 grid (lower 92%)
    grid_pad = ROOT.TPad("grid_pad", "grid_pad", 0.0, 0.0, 1.0, 0.92)
    grid_pad.SetFillStyle(0); grid_pad.SetBorderMode(0)
    grid_pad.Draw()
    grid_pad.Divide(3, 3, 0.001, 0.001)
    _KEEP.extend([leg_pad, grid_pad])

    legend_handles = {}
    for i, (name, ylabel, schc, pymin, pymax) in enumerate(SDME_PANELS):
        pad = grid_pad.cd(i + 1)   # was c.cd(i + 1)
        pad.SetLeftMargin(0.17)
        pad.SetRightMargin(0.04)
        pad.SetBottomMargin(0.14)
        pad.SetTopMargin(0.13)
        pad.SetBottomMargin(0.20 if i in (6, 7, 8) else 0.14) # bottom row has x-axis labels, so bigger bottom margin

        ymin, ymax = -1.0, 1.0

        frame = pad.DrawFrame(tmin, ymin, tmax, ymax)
        frame.SetLineWidth(1)
        frame.GetYaxis().SetTitle("") # was SetTitle(ylabel)
        frame.GetYaxis().SetTitleSize(0.06)
        frame.GetYaxis().SetLabelSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.25)
        frame.GetYaxis().SetNdivisions(-4)   # negative = "optimize off", use exactly N
        if i in (6, 7, 8):                     # x-axis labels on bottom row only
            frame.GetXaxis().SetTitle("#minus t (GeV^{2})")
            frame.GetXaxis().CenterTitle(True)
        else:
            frame.GetXaxis().SetTitle("")
            frame.GetXaxis().SetLabelSize(0) # removes tick labels on all but bottom row
        frame.GetXaxis().SetTitleSize(0.085)   # was 0.06 — bigger title
        frame.GetXaxis().SetLabelSize(0.070)   # was 0.05 — bigger tick numbers
        frame.GetXaxis().SetTitleOffset(0.965)
        frame.GetXaxis().SetNdivisions(408)
        draw_grid(pad, tmin, tmax, ymin, ymax,
                  xticks=[0.5, 1.0, 1.5, 2.0],
                  yticks=[-0.5, 0.0, 0.5])
        for ax in (frame.GetXaxis(), frame.GetYaxis()):
            ax.SetTitleFont(132)
            ax.SetLabelFont(132)

        # to drop the outer tick labels, but keep the ticks.
        frame.GetYaxis().ChangeLabel(1,  -1,-1,-1,-1,-1, " ")
        frame.GetYaxis().ChangeLabel(-1, -1,-1,-1,-1,-1, " ")
        frame.GetXaxis().ChangeLabel(1,  -1,-1,-1,-1,-1, " ")
        frame.GetXaxis().ChangeLabel(-1, -1,-1,-1,-1,-1, " ")

        lab = ROOT.TLatex()
        lab.SetNDC(True)                 # coordinates are now 0-1 across the pad
        lab.SetTextFont(132)
        lab.SetTextSize(0.075)
        lab.SetTextAlign(23)             # centered horizontally, top-aligned
        # x = center of the plotting area (between the L/R margins); y just above the frame
        xmid = 0.17 + 0.5 * (1.0 - 0.17 - 0.04)
        lab.DrawLatex(xmid, 0.985, ylabel)
        _KEEP.append(lab)

        # Draw reference line (currently at 0, but could be nonzero for rho^1_{1-1} and Im rho^2_{1-1} if SCHC is valid for K*, as it is for rho(770))
        line = ROOT.TLine(tmin, schc, tmax, schc)
        line.SetLineColor(ROOT.kGray + 2)
        line.SetLineWidth(1)
        line.Draw()

        gr = ROOT.TGraphErrors(n)
        for j in range(n):
            gr.SetPoint(j, t_centers[j], values[name][j])
            gr.SetPointError(j, t_halfwidths[j], errors[name][j])
        gr.SetMarkerStyle(1)
        # gr.SetMarkerStyle(20)
        gr.SetMarkerSize(1.0)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetLineWidth(1)
        gr.Draw("P same")

        # (ref dict, color, marker, t-nudge, legend label)
        if ref == "hao":
            overlays = [
                (SCHILLING_REF, ROOT.kGreen+2,  24, -0.03, "Schilling SDME fit"),
                (ZLM_P_REF,     ROOT.kOrange+7, 24,  0.00, "Zlm PWA, P only"),
                (ZLM_SP_REF,    ROOT.kBlue+1,   24,  0.03, "Zlm PWA, S+P"),
            ]
        else:  # mine
            overlays = [
                (MY_PONLY,   ROOT.kOrange+7, 25, -0.01, "Zlm P-only, BW"),
                (MY_SP_BW,   ROOT.kBlue+1,   26,  0.01, "Zlm S+P, BW"),
                (MY_SP_NOBW, ROOT.kRed-1,    32,  0.03, "Zlm S+P, no BW"),
            ]
        
        for ref_dict, col, mk, dx, _lab in overlays:
            pts = ref_dict.get(name, [])
            if not pts:
                continue
            go = ROOT.TGraphErrors(len(pts))
            for j, (t, v, e) in enumerate(pts):
                go.SetPoint(j, t + dx, v)
                go.SetPointError(j, 0.0, e)   # vertical only
            go.SetMarkerStyle(mk)
            go.SetMarkerSize(1.0)
            go.SetMarkerColor(col)
            go.SetLineColor(col)
            go.SetLineWidth(2)
            go.Draw("P same")
            _KEEP.append(go)
            legend_handles[_lab] = go   # overwrites each panel; any one works

        # pad.SetFrameLineWidth(1)
        pad.RedrawAxis()   # redraw the frame box/ticks on top of the grid

        _KEEP.extend([frame, line, gr])

    leg_pad.cd()
    leg = ROOT.TLegend(0.10, 0.05, 0.90, 0.95)  # fills the strip vertically
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(132)   # in the i==2 / legend block
    leg.SetTextSize(0.3)          # strip is short, so text size is large in its NDC
    leg.AddEntry(gr, "Schilling (Ks Pi+), BW", "pe")
    for _d, _c, _m, _dx, lbl in overlays:
        if lbl in legend_handles:
            leg.AddEntry(legend_handles[lbl], lbl, "pe")
    leg.SetNColumns(len(overlays) + 1)
    leg.Draw()
    _KEEP.append(leg)

    c.Update()
    c.Print(out_path)
    _KEEP.append(c)
    return c


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Plot K*(892) SDMEs vs -t from a folder of AmpTools .fit files."
    )
    ap.add_argument("--ref", choices=["hao", "mine"], default="mine",
                    help="Overlay Hao's K+pi0 results (hao) or my own Zlm "
                         "projections (mine).")
    ap.add_argument("--parity", action="store_true",
                help="Plot the parity asymmetry P_sigma instead of the 9 SDMEs.")
    ap.add_argument("fit_dir", nargs="+",
                    help="One or more folders, each containing the .fit files "
                        "for a t-bin. Point at several to build the -t scan.")
    ap.add_argument("-o", "--output", default="plots/sdme_fit_plots.pdf",
                    help="Output file (.pdf; a .png is also written). "
                         "Default: plots/sdme_fit_plots.pdf")
    ap.add_argument("--fixed-ranges", action="store_true",
                    help="Use the reference paper y-ranges instead of auto-ranging.")
    ap.add_argument("--recursive", action="store_true",
                    help="Search sub-folders for .fit files as well.")
    ap.add_argument("--tmin", type=float, default=0.0, help="X-axis min (-t).")
    ap.add_argument("--tmax", type=float, default=2.5, help="X-axis max (-t).")
    ap.add_argument("--t-range", nargs=2, type=float, metavar=("LO", "HI"),
                default=None,
                help="Force this -t range (GeV^2) for ALL fits found, "
                        "e.g. --t-range 0.1 0.3. Use if the bin can't be read "
                        "from the filename or config.")
    args = ap.parse_args()
    if args.parity and args.output == "plots/sdme_fit_plots.pdf":
        args.output = "plots/parity_asym.pdf"

    for d in args.fit_dir:
        if not os.path.isdir(d):
            sys.exit(f"ERROR: not a directory: {d}")

    load_amptools()

    t_override = tuple(args.t_range) if args.t_range else None
    bins, skipped = [], []
    for d in args.fit_dir:
        b, s = find_fit_bins(d, recursive=args.recursive, t_override=t_override)
        bins.extend(b)
        skipped.extend(s)
    bins.sort(key=lambda x: x[1])

    if skipped:
        print(f"Skipped {len(skipped)} file(s) with no 't<lo><hi>' token:")
        for f in skipped:
            print(f"    {f}")
    if not bins:
        sys.exit("ERROR: no .fit files with a parseable t-range were found.")

    print(f"Found {len(bins)} t-bin(s):")
    for f, lo, hi in bins:
        print(f"    -t = {lo:.2f}-{hi:.2f}   {os.path.basename(f)}")

    if args.parity:
        parity_asym_plot(bins, out_path=args.output,
                         tmin=args.tmin, tmax=args.tmax, ref=args.ref)
    else:
        sdme_vs_t_plots(bins, out_path=args.output,
                        tmin=args.tmin, tmax=args.tmax,
                        fixed_ranges=args.fixed_ranges, ref=args.ref)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()