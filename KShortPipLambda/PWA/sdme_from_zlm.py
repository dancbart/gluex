#!/usr/bin/env python3
"""
sdme_from_zlm.py -- project the nine K*(892) SDMEs out of an AmpTools Zlm PWA fit.

Reads one or more .fit files with FitResults, finds the Zlm P-wave amplitudes
(l = 1, m = -1, 0, +1) for both reflectivities, and computes the Schilling SDMEs
from the reflectivity-basis density matrices (Mathieu et al., PRD 100, 054017,
Eqs. D8a-c), normalized to the P-wave trace only (S-wave and S-P interference
are ignored on purpose).

Reflectivity is taken from the Zlm arguments, not from the sum names:
    Zlm l m r s   ->   epsilon = r * s
    (+1,+1) Re(1+P)  eps=+     (-1,-1) Im(1-P)  eps=+
    (+1,-1) Re(1-P)  eps=-     (-1,+1) Im(1+P)  eps=-

Errors: linear propagation, sigma^2 = J C J^T, with C the fit covariance of the
Re/Im parts of the P-wave production parameters and J a numerical Jacobian.

Usage (inside the PyAmpTools container):
    python sdme_from_zlm.py twoPS_PWA_allPol.fit
    python sdme_from_zlm.py fits/t0305/*.fit --best          # lowest -lnL of the restarts
    python sdme_from_zlm.py twoPS_PWA_allPol.fit --reaction KsPipLamb_00 --csv out.csv
    python sdme_from_zlm.py --selftest                        # math check, no AmpTools needed

Assumptions (check against your config):
  * One nucleon-helicity sum (k = 0), as in standard GlueX Zlm configs.
  * Any extra amplitude factors (lineshapes, scales) are common to all P-waves,
    so they cancel in the ratio. The script warns if P-waves carry extra factors.
  * Amplitudes are not renormalized to their normalization integrals.
"""

import argparse
import math
import sys

import numpy as np

SDME_NAMES = [
    "rho0_00", "Re_rho0_10", "rho0_1m1",
    "rho1_11", "rho1_00", "Re_rho1_10", "rho1_1m1",
    "Im_rho2_10", "Im_rho2_1m1",
]

M_VALUES = (-1, 0, 1)


# --------------------------------------------------------------------------
# Physics: P-wave amplitudes -> SDMEs
# --------------------------------------------------------------------------
def density_matrices(P):
    """
    P: dict {(eps, m): complex} for eps in (+1,-1), m in (-1,0,1); missing -> 0.
    Returns rho0, rho1, rho2 as 3x3 complex arrays indexed [m+1, m'+1],
    unnormalized (kappa = 1), from Eqs. (D8a-c) with l = l' = 1.
    """
    def a(eps, m):
        return P.get((eps, m), 0j)

    rho = [np.zeros((3, 3), dtype=complex) for _ in range(3)]
    for eps in (+1, -1):
        for m in M_VALUES:
            for mp in M_VALUES:
                i, j = m + 1, mp + 1
                sm, smp = (-1) ** abs(m), (-1) ** abs(mp)
                rho[0][i, j] += (a(eps, m) * a(eps, mp).conjugate()
                                 + (-1) ** abs(m - mp) * a(eps, -m) * a(eps, -mp).conjugate())
                t1 = sm * a(eps, -m) * a(eps, mp).conjugate()
                t2 = smp * a(eps, m) * a(eps, -mp).conjugate()
                rho[1][i, j] += -eps * (t1 + t2)
                rho[2][i, j] += -1j * eps * (t1 - t2)
    return rho


def sdmes_from_P(P):
    """Nine normalized Schilling SDMEs (dict) from P-wave amplitudes."""
    r0, r1, r2 = density_matrices(P)
    tr = np.trace(r0).real
    if tr <= 0:
        raise ValueError("P-wave intensity is zero; cannot normalize")
    r0, r1, r2 = r0 / tr, r1 / tr, r2 / tr
    I0, I1, Im1 = 1, 2, 0  # array indices for m = 0, +1, -1
    return {
        "rho0_00":     r0[I0, I0].real,
        "Re_rho0_10":  r0[I1, I0].real,
        "rho0_1m1":    r0[I1, Im1].real,
        "rho1_11":     r1[I1, I1].real,
        "rho1_00":     r1[I0, I0].real,
        "Re_rho1_10":  r1[I1, I0].real,
        "rho1_1m1":    r1[I1, Im1].real,
        "Im_rho2_10":  r2[I1, I0].imag,
        "Im_rho2_1m1": r2[I1, Im1].imag,
    }


def sdme_vector(x, keys):
    """x: flat real vector [Re a1, Im a1, Re a2, ...] matching keys [(eps,m),...]."""
    P = {k: complex(x[2 * n], x[2 * n + 1]) for n, k in enumerate(keys)}
    s = sdmes_from_P(P)
    return np.array([s[name] for name in SDME_NAMES])


def jacobian(x, keys, h=1e-6):
    """Central-difference Jacobian d(SDMEs)/d(x), step relative to |x|."""
    x = np.asarray(x, dtype=float)
    scale = max(np.max(np.abs(x)), 1e-12)
    J = np.zeros((len(SDME_NAMES), len(x)))
    for i in range(len(x)):
        dx = h * scale
        xp, xm = x.copy(), x.copy()
        xp[i] += dx
        xm[i] -= dx
        J[:, i] = (sdme_vector(xp, keys) - sdme_vector(xm, keys)) / (2 * dx)
    return J


# --------------------------------------------------------------------------
# AmpTools I/O
# --------------------------------------------------------------------------
def load_amptools():
    """Make FitResults available. Adjust to match the import in plot_sdme_fits.py."""
    try:
        from pyamptools import atiSetup
        atiSetup.setup(globals())
        return globals()["FitResults"]
    except Exception as err:
        try:
            import ROOT
            return ROOT.FitResults
        except Exception:
            sys.exit("Could not load FitResults (%s). Use the same import as "
                     "plot_sdme_fits.py inside the PyAmpTools container." % err)


def to_complex(z):
    try:
        return complex(z)
    except TypeError:
        return complex(z.real(), z.imag())


def zlm_args(amp_info):
    """Return (l, m, r, s) from an AmplitudeInfo, or None if it has no Zlm factor.
    Also returns the names of any other factors."""
    zlm, others = None, []
    for factor in amp_info.factors():
        f = [str(x) for x in factor]
        if f[0] == "Zlm":
            zlm = tuple(int(float(v)) for v in f[1:5])
        else:
            others.append(f[0])
    return zlm, others


def extract_P(fr, reaction=None, verbose=True):
    """
    Returns:
      P      dict {(eps, m): complex}  P-wave production parameters
      S      dict {eps: complex}       S-wave production parameters (info only)
      names  dict {(eps, m): full amplitude name used}
      reac   reaction used
    """
    cfg = fr.configInfo()
    amps = list(cfg.amplitudeList())
    reactions = sorted({str(a.reactionName()) for a in amps})
    reac = reaction or reactions[0]
    if reac not in reactions:
        sys.exit("Reaction %s not in fit. Available: %s" % (reac, ", ".join(reactions)))

    P, S, names = {}, {}, {}
    for a in amps:
        if str(a.reactionName()) != reac:
            continue
        name = str(a.fullName())
        zargs, others = zlm_args(a)
        if zargs is None:
            continue
        l, m, r, s = zargs
        eps = r * s
        val = to_complex(fr.productionParameter(name))
        if l == 1:
            if others and verbose:
                print("  note: %s has extra factors %s (assumed common to all P-waves)"
                      % (name, others))
            key = (eps, m)
            if key in P:
                if abs(P[key] - val) > 1e-6 * max(abs(val), 1e-12):
                    print("  WARNING: %s = %s differs from %s = %s (same eps, m). "
                          "Check constraints." % (name, val, names[key], P[key]))
            else:
                P[key], names[key] = val, name
        elif l == 0:
            S.setdefault(eps, val)
    return P, S, names, reac


def param_indices(fr, amp_name):
    """Indices of <amp>_re and <amp>_im in parNameList(), or None if not free."""
    pnames = [str(p) for p in fr.parNameList()]
    idx = {n: i for i, n in enumerate(pnames)}
    return idx.get(amp_name + "_re"), idx.get(amp_name + "_im")


def find_free_params(fr, P_names, all_names_by_key):
    """
    For each (eps, m) find the Minuit parameter indices of its production
    parameter. Constrained amplitudes share one free parameter, which may be
    registered under any member of the constraint group, so try them all.
    """
    out = {}
    for key in P_names:
        found = (None, None)
        for name in all_names_by_key.get(key, [P_names[key]]):
            ire, iim = param_indices(fr, name)
            if ire is not None:
                found = (ire, iim)
                break
        out[key] = found
    return out


def all_amp_names_by_key(fr):
    """(eps, m) -> list of all P-wave amplitude full names (all reactions)."""
    res = {}
    for a in fr.configInfo().amplitudeList():
        zargs, _ = zlm_args(a)
        if zargs and zargs[0] == 1:
            l, m, r, s = zargs
            res.setdefault((r * s, m), []).append(str(a.fullName()))
    return res


def analyze(fr, reaction=None, verbose=True):
    P, S, names, reac = extract_P(fr, reaction, verbose)
    keys = sorted(P.keys(), key=lambda k: (-k[0], k[1]))
    if not keys:
        raise RuntimeError("No Zlm P-wave (l=1) amplitudes found")

    x = []
    for k in keys:
        x += [P[k].real, P[k].imag]
    x = np.array(x)

    sd = sdme_vector(x, keys)

    # covariance of the 2*len(keys) real parameters
    C_full = np.array([list(row) for row in fr.errorMatrix()])
    pidx = find_free_params(fr, names, all_amp_names_by_key(fr))
    C = np.zeros((len(x), len(x)))
    flat = []
    for k in keys:
        flat += list(pidx[k])  # (re, im); None if fixed/not found
    missing = [keys[n // 2] for n, i in enumerate(flat) if i is None and n % 2 == 0]
    if missing and verbose:
        print("  note: no free parameter found for %s (fixed or real-constrained); "
              "zero variance assumed" % missing)
    for a_, ia in enumerate(flat):
        for b_, ib in enumerate(flat):
            if ia is not None and ib is not None:
                C[a_, b_] = C_full[ia, ib]

    J = jacobian(x, keys)
    err = np.sqrt(np.clip(np.diag(J @ C @ J.T), 0, None))

    nP = sum(abs(v) ** 2 for v in P.values())
    nS = sum(abs(v) ** 2 for v in S.values())
    info = {
        "reaction": reac,
        "lnL": fr.likelihood(),
        "S_fraction": nS / (nS + nP) if (nS + nP) > 0 else float("nan"),
        "P": {k: P[k] for k in keys},
        "names": names,
    }
    return dict(zip(SDME_NAMES, sd)), dict(zip(SDME_NAMES, err)), info


# --------------------------------------------------------------------------
# Self-test (no AmpTools needed)
# --------------------------------------------------------------------------
def hand_formulas(P):
    """Section 7 of zlm_to_sdme.pdf, written out by hand, for cross-checking."""
    a = lambda e, m: P.get((e, m), 0j)
    N = sum(abs(v) ** 2 for v in P.values())
    out = dict.fromkeys(SDME_NAMES, 0.0)
    for e in (+1, -1):
        p1, p0, pm = a(e, 1), a(e, 0), a(e, -1)
        out["rho0_00"] += abs(p0) ** 2 / N
        out["Re_rho0_10"] += ((p1 - pm) * p0.conjugate()).real / (2 * N)
        out["rho0_1m1"] += (p1 * pm.conjugate()).real / N
        out["rho1_11"] += e * (p1 * pm.conjugate()).real / N
        out["rho1_00"] += -e * abs(p0) ** 2 / N
        out["Re_rho1_10"] += -e * ((p1 - pm) * p0.conjugate()).real / (2 * N)
        out["rho1_1m1"] += e * (abs(p1) ** 2 + abs(pm) ** 2) / (2 * N)
        out["Im_rho2_10"] += e * ((p1 + pm) * p0.conjugate()).real / (2 * N)
        out["Im_rho2_1m1"] += e * (abs(pm) ** 2 - abs(p1) ** 2) / (2 * N)
    return out


def selftest():
    ok = True
    # 1) pure natural-parity helicity-conserving: rho1_1m1 = 1/2, Im rho2_1m1 = -1/2
    s = sdmes_from_P({(+1, 1): 1.0 + 0j})
    exp = dict.fromkeys(SDME_NAMES, 0.0)
    exp["rho1_1m1"], exp["Im_rho2_1m1"] = 0.5, -0.5
    for n in SDME_NAMES:
        if abs(s[n] - exp[n]) > 1e-12:
            ok = False
            print("FAIL pure-P1+ %s: got %g expected %g" % (n, s[n], exp[n]))

    # 2) general matrices vs hand-reduced formulas, random amplitudes
    rng = np.random.default_rng(1)
    for _ in range(200):
        P = {(e, m): complex(*rng.normal(size=2)) for e in (1, -1) for m in M_VALUES}
        s, h = sdmes_from_P(P), hand_formulas(P)
        for n in SDME_NAMES:
            if abs(s[n] - h[n]) > 1e-10:
                ok = False
                print("FAIL random %s: matrices %g vs hand %g" % (n, s[n], h[n]))
                break

    # 3) the angular distribution built from Zlm amplitudes equals the Schilling W
    def Y1(m, th, ph):
        if m == 0:
            return math.sqrt(3 / (4 * math.pi)) * math.cos(th)
        return -m * math.sqrt(3 / (8 * math.pi)) * math.sin(th) * complex(math.cos(m * ph), math.sin(m * ph))

    def I_zlm(P, th, ph, Ph, Pg):
        tot = 0.0
        for e in (1, -1):
            A = sum(P.get((e, m), 0j) * (Y1(m, th, ph) * complex(math.cos(Ph), -math.sin(Ph))).real for m in M_VALUES)
            B = sum(P.get((e, m), 0j) * (Y1(m, th, ph) * complex(math.cos(Ph), -math.sin(Ph))).imag for m in M_VALUES)
            tot += (1 + e * Pg) * abs(A) ** 2 + (1 - e * Pg) * abs(B) ** 2
        return 2 * tot

    def W_schilling(r, th, ph, Ph, Pg):
        c, s2 = math.cos(th), math.sin(th)
        W0 = 0.5 * (1 - r["rho0_00"]) + 0.5 * (3 * r["rho0_00"] - 1) * c * c \
            - math.sqrt(2) * r["Re_rho0_10"] * math.sin(2 * th) * math.cos(ph) \
            - r["rho0_1m1"] * s2 * s2 * math.cos(2 * ph)
        W1 = r["rho1_11"] * s2 * s2 + r["rho1_00"] * c * c \
            - math.sqrt(2) * r["Re_rho1_10"] * math.sin(2 * th) * math.cos(ph) \
            - r["rho1_1m1"] * s2 * s2 * math.cos(2 * ph)
        W2 = math.sqrt(2) * r["Im_rho2_10"] * math.sin(2 * th) * math.sin(ph) \
            + r["Im_rho2_1m1"] * s2 * s2 * math.sin(2 * ph)
        return 3 / (4 * math.pi) * (W0 - Pg * math.cos(2 * Ph) * W1 - Pg * math.sin(2 * Ph) * W2)

    for _ in range(20):
        P = {(e, m): complex(*rng.normal(size=2)) for e in (1, -1) for m in M_VALUES}
        r = sdmes_from_P(P)
        norm = 2 * sum(abs(v) ** 2 for v in P.values())  # Tr rho0 with kappa = 1
        for _ in range(20):
            th, ph, Ph, Pg = rng.uniform(0, math.pi), rng.uniform(-math.pi, math.pi), \
                rng.uniform(-math.pi, math.pi), rng.uniform(0, 1)
            lhs = I_zlm(P, th, ph, Ph, Pg)
            rhs = norm * W_schilling(r, th, ph, Ph, Pg)
            if abs(lhs - rhs) > 1e-9 * max(1, abs(lhs)):
                ok = False
                print("FAIL Zlm vs Schilling W: %g vs %g" % (lhs, rhs))
                break

    print("selftest:", "PASSED" if ok else "FAILED")
    return ok


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fits", nargs="*", help=".fit file(s)")
    ap.add_argument("--reaction", help="reaction to read production parameters from "
                                       "(default: first alphabetically, e.g. KsPipLamb_00)")
    ap.add_argument("--best", action="store_true",
                    help="among the given files, report only the lowest -lnL fit")
    ap.add_argument("--csv", help="write results to this CSV file")
    ap.add_argument("--allow-unconverged", action="store_true",
                    help="keep fits whose MINUIT status != 0 or eMatrix status != 3")
    ap.add_argument("--selftest", action="store_true", help="run math checks and exit")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(0 if selftest() else 1)
    if not args.fits:
        ap.error("give at least one .fit file (or --selftest)")

    FitResults = load_amptools()
    results = []
    for f in args.fits:
        fr = FitResults(f)
        if not fr.valid():
            print("skipping unreadable fit: %s" % f)
            continue
        # Convergence: MINUIT status 0 = last command (MIGRAD/HESSE) succeeded;
        # eMatrixStatus 3 = full, accurate covariance matrix.
        status, emat = fr.lastMinuitCommandStatus(), fr.eMatrixStatus()
        converged = (status == 0 and emat == 3)
        if not converged:
            print("%s: NOT converged (minuit status %d, eMatrix status %d)%s"
                  % (f, status, emat, "" if args.allow_unconverged else " -- skipped"))
            if not args.allow_unconverged:
                continue
        print("== %s" % f)
        val, err, info = analyze(fr, args.reaction)
        info["status"], info["eMatrix"] = status, emat
        results.append((f, val, err, info))

    if not results:
        sys.exit("no converged fits (use --allow-unconverged to inspect them anyway)")
    print("\n%d of %d fits used" % (len(results), len(args.fits)))
    if args.best:
        results = [min(results, key=lambda r: r[3]["lnL"])]

    for f, val, err, info in results:
        print("\n%s   reaction %s   -lnL = %.3f   status %d/%d   S fraction = %.3f"
              % (f, info["reaction"], info["lnL"], info["status"], info["eMatrix"],
                 info["S_fraction"]))
        for k, v in info["P"].items():
            print("   P(eps=%+d, m=%+d) = %+.4g %+.4gi   [%s]"
                  % (k[0], k[1], v.real, v.imag, info["names"][k]))
        for n in SDME_NAMES:
            print("   %-12s = %+.4f +/- %.4f" % (n, val[n], err[n]))

    if args.csv:
        with open(args.csv, "w") as fh:
            fh.write("file,lnL,minuit_status,eMatrix_status,S_fraction," +
                     ",".join("%s,%s_err" % (n, n) for n in SDME_NAMES) + "\n")
            for f, val, err, info in results:
                fh.write("%s,%.6f,%d,%d,%.6f," % (f, info["lnL"], info["status"],
                                                  info["eMatrix"], info["S_fraction"]) +
                         ",".join("%.6f,%.6f" % (val[n], err[n]) for n in SDME_NAMES) + "\n")
        print("\nwrote %s" % args.csv)


if __name__ == "__main__":
    main()
