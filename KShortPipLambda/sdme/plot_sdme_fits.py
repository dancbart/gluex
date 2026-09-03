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

import ROOT

ROOT.gROOT.SetBatch(True)

# -----------------------------------------------------------------------------
# Panel definitions -- order is row-major to match the reference figure.
# Parameter names follow rho<m><m'><alpha>.
#   (param name, y-axis LaTeX label, SCHC+NPE line, paper ymin, paper ymax)
# -----------------------------------------------------------------------------

SDME_PANELS = [
    ("rho000",  "#rho^{0}_{00}",     0.0,  -1.00,  1.00),
    ("rho100",  "Re#rho^{0}_{10}",   0.0,  -1.00,  1.00),
    ("rho1m10", "#rho^{0}_{1-1}",    0.0,  -1.00,  1.00),
    ("rho111",  "#rho^{1}_{11}",     0.0,  -1.00,  1.00),
    ("rho001",  "#rho^{1}_{00}",     0.0,  -1.00,  1.00),
    ("rho101",  "Re#rho^{1}_{10}",   0.0,  -1.00,  1.00),
    ("rho1m11", "#rho^{1}_{1-1}",    0.0,  -1.00,  1.00),
    ("rho102",  "Im#rho^{2}_{10}",   0.0,  -1.00,  1.00),
    ("rho1m12", "Im#rho^{2}_{1-1}",  0.0,  -1.00,  1.00),
]

# filename token: t<2 digits><2 digits>, each read as tenths of GeV^2
T_TOKEN_RE = re.compile(r"t(\d{2})(\d{2})")

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


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------
def sdme_vs_t_plots(fit_bins, out_path="plots/sdme_fit_plots.pdf",
                    tmin=0.0, tmax=2.5, fixed_ranges=False):
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

    for i, (name, ylabel, schc, pymin, pymax) in enumerate(SDME_PANELS):
        pad = grid_pad.cd(i + 1)   # was c.cd(i + 1)
        pad.SetLeftMargin(0.17)
        pad.SetRightMargin(0.04)
        pad.SetBottomMargin(0.14)
        pad.SetTopMargin(0.13)

        ymin, ymax = -1.0, 1.0

        frame = pad.DrawFrame(tmin, ymin, tmax, ymax)
        frame.SetLineWidth(1)
        frame.GetXaxis().SetTitle("#minus t (GeV^{2})")
        frame.GetYaxis().SetTitle("") # was SetTitle(ylabel)
        frame.GetXaxis().SetTitleSize(0.06)
        frame.GetYaxis().SetTitleSize(0.06)
        frame.GetXaxis().SetLabelSize(0.05)
        frame.GetYaxis().SetLabelSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.25)
        frame.GetYaxis().SetNdivisions(-4)   # negative = "optimize off", use exactly N
        frame.GetXaxis().SetNdivisions(408)
        frame.GetXaxis().SetTitleOffset(1.00)
        draw_grid(pad, tmin, tmax, ymin, ymax,
                  xticks=[0.5, 1.0, 1.5, 2.0],
                  yticks=[-0.5, 0.0, 0.5])

        # to drop the outer tick labels, but keep the ticks.
        frame.GetYaxis().ChangeLabel(1,  -1,-1,-1,-1,-1, " ")
        frame.GetYaxis().ChangeLabel(-1, -1,-1,-1,-1,-1, " ")
        frame.GetXaxis().ChangeLabel(1,  -1,-1,-1,-1,-1, " ")
        frame.GetXaxis().ChangeLabel(-1, -1,-1,-1,-1,-1, " ")

        lab = ROOT.TLatex()
        lab.SetNDC(True)                 # coordinates are now 0-1 across the pad
        lab.SetTextFont(42)
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
        gr.SetMarkerStyle(20)
        gr.SetMarkerSize(1.0)
        gr.SetMarkerColor(ROOT.kBlack)
        gr.SetLineColor(ROOT.kBlack)
        gr.SetLineWidth(1)
        gr.Draw("P same")

        # pad.SetFrameLineWidth(1)
        pad.RedrawAxis()   # redraw the frame box/ticks on top of the grid

        _KEEP.extend([frame, line, gr])

    leg_pad.cd()
    leg = ROOT.TLegend(0.30, 0.05, 0.70, 0.95)  # fills the strip vertically
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.3)          # strip is short, so text size is large in its NDC
    leg.AddEntry(gr, "Schilling SDME fit", "pe")
    leg.Draw()
    _KEEP.append(leg)

    c.Update()

    c.Update()
    c.Print(out_path)
    if out_path.lower().endswith(".pdf"):
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

    sdme_vs_t_plots(bins, out_path=args.output,
                    tmin=args.tmin, tmax=args.tmax,
                    fixed_ranges=args.fixed_ranges)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()