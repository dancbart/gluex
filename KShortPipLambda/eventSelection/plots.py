import sys, os
import time
import ROOT

ROOT.gROOT.SetBatch(True)

from pyamptools import atiSetup
atiSetup.setup(globals(), use_fsroot=True)

ROOT.TGaxis.SetMaxDigits(3)

# path to shared libraries
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "libraries"))

logFile = "plots/plotEventSelection.txt"
allPlots = "plots/plots.pdf"
treeName = "ntFSGlueX_100000000_1100"
bggen = False

from gluex_style import gluex_style
gluex_style()

# ------------------------------------------------------------
# Files
# ------------------------------------------------------------
# ------ Fit results histogram(s) for K Pi system
FND_fits = "/work/halld/home/dbarton/gluex/KShortPipLambda/fitting/plots/plots_rooFit_kStar.root"

# ------ Use to plot variables used as 'global' cuts (beam energy, unused shower, etc).  These are unskimmed files. ---------------------
FND_unSkimmed = "/volatile/halld/home/dbarton/pipkslamb/data/sp18fa18sp20/tree_pipkslamb__B4_M16_M18_FSFlat_sum_*_sp18fa18sp20_40856_73266.root"
FND_unSkimmed_MC = "/volatile/halld/home/dbarton/pipkslamb/mc/fall2018/MCWjob4434/tree_pipkslamb__B4_M16_M18_gen_amp_V2_FSFlat_sp18-fa18_ALL.root"
# Not used:
# FND_unSkimmed_MC_THROWN.  For plotting, use 'FND_signalSkims_MC_THROWN' (created below).

# ------ Use to plot Ks and Lambda, K*, etc. pre-fit distributions -------------------------------------------
FND_eventSelectionSkims = "/volatile/halld/home/dbarton/pipkslamb/skims/tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_ALLpols.root"
FND_eventSelectionSkims_MC = "/volatile/halld/home/dbarton/pipkslamb/skims/tree_pipkslamb__B4_M16_M18_EVENT_SELECTION_SKIM_MC_sp18fa18sp20.root"
# Not used:
# FND_eventSelectionSkims_MC_THROWN. For plotting, use 'FND_signalSkims_MC_THROWN' (created below).

# ------ Use to plot final signal distributions that would be used for AmpTools fits (K*892 mass, angular distributions, etc.).  These are the ACTUAL trees fed into AmpTools.  ----
FND_signalSkims = "/work/halld/home/dbarton/gluex/KShortPipLambda/fitSourceFiles/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_t0103_ALLpols.root"
FND_signalSkims_MC = "/work/halld/home/dbarton/gluex/KShortPipLambda/fitSourceFiles/tree_pipkslamb__B4_M16_M18_SIGNAL_SKIM_K892_MC_t0103.root"
FND_signalSkims_MC_THROWN = "/work/halld/home/dbarton/gluex/KShortPipLambda/fitSourceFiles/tree_pipkslamb_SIGNAL_SKIM_K892_THROWN_t0103_sp18fa18sp20.root"

# Label each plot as either DATA or Monte Carlo:
def file_label(fname):
    s = fname.lower()
    return "MC" if ("mc" in s or "bggen" in s) else "Data"


# =========================================================
# CUTS — imported from the shared module (single source of truth)
# =========================================================

from cuts_kStar import (   # noqa: I001
    # particle names (needed by the MASS(...) f-strings throughout)
    DecayingLambda, Proton, PiMinus2, DecayingKShort, PiPlus2, PiMinus1, PiPlus1,
    # t-bin lists
    ALL_T_BINS, EVENT_SELECTION_T_BINS,
    # cut registration
    setup, setup_genmc,
    # cut strings referenced by name in this file
    generalCuts_eventSelection, baseCuts, sidebandCuts,
)

T_BINS                = ALL_T_BINS            # subset if only plotting a few t-bins
T_BIN_EVENT_SELECTION = EVENT_SELECTION_T_BINS

setup(T_BINS, T_BIN_EVENT_SELECTION)          # registers all reconstructed cuts
setup_genmc(T_BINS, T_BIN_EVENT_SELECTION)


# =========================================================
# Import helper functions
# =========================================================
from plots_helperFunctions import (  # noqa: I001
    keep,
    make_panel_grid,
    draw_info_pad,
    _draw_pad_separator,
    _normalize_note_lines,
    draw_notes_pad,
    make_breit_wigner,
    make_expo2,
    make_voigtian,
    make_voigtian_plus_expo2,
    make_bernstein,
    make_two_voigtians_plus_bernstein,
    make_component_funcs_kstar,
    fit_integral_voigt1,
    fit_integral_voigt2,
    fit_integral_bernstein,
    compute_figureOfMerit_kstar,
    make_component_funcs,
    fit_integral_signal,
    fit_integral_background,
    compute_figureOfMerit,
    log_fit_results,
    vecs_to_tgraph,
    integral_between,
    draw_vertical_lines,
    draw_horizontal_lines,
    fs_get_th1,
    fs_get_th2,
    draw_mc_same,
)

# ============================================================
# GLOBAL CUT PLOTS
# ============================================================
def global_eventSelection_Cuts(pdf_path):

    # # ============================================================
    # # Page 1a: Unused shower energy
    # # ============================================================
    # c = ROOT.TCanvas("c_eventCuts_unusedE", "c_eventCuts_unusedE", 1000, 1300)
    # keep(c)

    # panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    # p = panels[0]
    # p["plot"].cd()

    # h1 = fs_get_th1(
    #     FND_unSkimmed,
    #     "EnUnusedSh",
    #     "(100,0.06,1.0)",
    #     "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)"
    # )
    # h1.SetXTitle("Unused shower energy [GeV]")
    # h1.SetYTitle("Combos")
    # h1.SetLineColor(ROOT.kBlack)

    # h1b = fs_get_th1(
    #     FND_unSkimmed_MC,
    #     "EnUnusedSh",
    #     "(100,0.06,1.0)",
    #     "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)"
    # )
    # h1b.SetXTitle("Unused shower energy [GeV]")
    # h1b.SetYTitle("Combos")
    # h1b.SetLineColor(ROOT.kBlue)
    # h1b.SetFillColor(ROOT.kBlue - 5)

    # integral_data = integral_between(h1, 0.1, 1.0)
    # integral_MC_raw   = integral_between(h1b, 0.1, 1.0)
    # if integral_MC_raw > 0:
    #     scaleFactor = integral_data / integral_MC_raw
    #     h1b.Scale(scaleFactor)
    # else:
    #     print("WARNING: MC integral is zero, not scaling")
    # integral_MC_scaled = integral_between(h1b, 0.1, 1.0)

    # # after scaling
    # h1b.SetMinimum(0.5)
    # h1.SetMinimum(0.5)

    # h1b.Draw("hist")
    # h1.Draw("pE same")   # use E1 instead of pE for safer error bars

    # # p["plot"].SetLogy(1)
    # p["plot"].Modified()
    # p["plot"].Update()


    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed, "EnUnusedSh", "(100,0.0,1.0)",
    #         "CUT()"
    #     )

    # draw_info_pad(
    #     p["info_main"],
    #     "#bf{No cut applied on this variable.}",
    #     legend_items=[(h1, "Data " "(integral: " f"{integral_data:.0f})", "pE"),
    #                   (h1b, f"MC scaled (raw: {integral_MC_raw:.0f} -> scaled: {integral_MC_scaled:.0f})", "f"),
    #                   ],
    #     # notes=["Cut: E_{unused} < 0.1 GeV", "log scale"],
    #     notes=["Unused Shower Energy",
    #             # "Log scale",
    #            "Integral between (0.1, 1.0)"
    #            ],
        
    #     # middle pad tweaks
    #     legend_box=(0.33, 0.18, 0.96, 0.84),
    #     legend_text_size=0.12,

    #     label_pos=(0.06, 0.90),
    #     label_size=0.10,

    #     notes_start_y=0.62,
    #     notes_text_size=0.12,
    #     notes_step=0.13,
    # )
    # draw_notes_pad(
    #     p["info_notes"],
    #     title="Cuts used",
    #     notes=[
    #         "Global cuts: CUT()",
    #         "Histogram cuts: CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ)",
    #         "#bf{Notes:} Signal MC in good agreement with DATA.  Therefore, it is ",
    #         "unlikely events from #it{Unused shower energy} are wrong topology.",
    #         "#bf{Further Study:} consider generating background MC with different",
    #          "topology (i.e. an extra #pi^{0}, etc.) and compare #it{that} to data.",
    #     ],

    #     # bottom pad tweaks
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.72,
    #     notes_text_size=0.10,
    #     notes_step=0.12,

    # )

    # # c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")

    # ============================================================
    # Page 1b: Unused tracks
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_unusedTracks", "c_eventCuts_unusedTracks", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_eventSelectionSkims,
        "NumUnusedTracks",
        "(100,-1.25,1.25)",
        "CUT(rf,chi2DOF,coherentPeak,targetZ)"
    )
    h1.SetXTitle("Unused tracks")
    h1.SetYTitle("Combos")
    h1.SetLineColor(ROOT.kBlack)

    h2 = fs_get_th1(
        FND_eventSelectionSkims_MC,
        "NumUnusedTracks",
        "(100,-1.25,1.25)",
        "CUT(rf,chi2DOF,coherentPeak,targetZ)"
    )
    h2.SetXTitle("Unused tracks")
    h2.SetYTitle("Combos")
    h2.SetLineColor(ROOT.kBlue)
    h2.SetFillColor(ROOT.kBlue - 5)

    integral_data = integral_between(h1, -1.25, 1.25)
    integral_MC_raw   = integral_between(h2, -1.25, 1.25)
    if integral_MC_raw > 0:
        scaleFactor = integral_data / integral_MC_raw
        h2.Scale(scaleFactor)
    else:
        print("WARNING: MC integral is zero, not scaling")
    integral_MC_scaled = integral_between(h2, -1.25, 1.25)

    h2.Draw("hist")
    h1.Draw("same pE")

    if bggen:
        draw_mc_same(
            FND_unSkimmed, "NumUnusedTracks", "(100,0.0,1.0)",
            "CUT()"
        )

    draw_info_pad(
        p["info_main"],
        "#bf{Data and MC.}",
        legend_items=[(h1, f"Data (integral: {integral_data:.0f})", "pE"),
                      (h2, f"MC scaled (raw: {integral_MC_raw:.0f} -> scaled: {integral_MC_scaled:.0f})", "f"),
                      ],
        # notes=["Cut: E_{unused} < 0.1 GeV", "log scale"],
        notes=["Unused Tracks",
                # "Log scale",
               "Integral between (-1.25, 1.25)"
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
            "Global cuts: CUT()",
            "Histogram cuts: CUT(rf,chi2DOF,coherentPeak,targetZ)",
        ],

        # bottom pad tweaks
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.10,
        notes_step=0.12,

    )

    # c.Print(pdf_path)
    c.Print(f"{pdf_path}(")

    # ============================================================
    # Page 1c: Combos
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_NumCombos", "c_eventCuts_NumCombos", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_eventSelectionSkims,
        "NumCombos",
        "(300,0.0,100.0)",
        "CUT(rf,chi2DOF,coherentPeak,targetZ)"
    )
    h1.SetXTitle("Number of combos")
    h1.SetYTitle("Count")
    h1.SetLineColor(ROOT.kBlack)

    h2 = fs_get_th1(
        FND_eventSelectionSkims_MC,
        "NumCombos",
        "(300,0.0,100.0)",
        "CUT(rf,chi2DOF,coherentPeak,targetZ)"
    )
    h2.SetLineColor(ROOT.kBlue)
    h2.SetFillColor(ROOT.kBlue - 5)

    h3 = fs_get_th1(
        FND_eventSelectionSkims,
        "NumCombos",
        "(300,0.0,100.0)",
        "CUT(chi2DOF,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)*CUTWT(rf,KShort,Lambda)"
    )
    h3.SetXTitle("Number of combos")
    h3.SetYTitle("Count")
    h3.SetLineColor(ROOT.kRed)
    h3.SetFillColor(ROOT.kRed - 5)

    integral_data = integral_between(h1, 0.0, 100.0)
    integral_MC_raw   = integral_between(h2, 0.0, 100.0)
    integral_data_allCuts = integral_between(h3, 0.0, 100.0)
    if integral_MC_raw > 0:
        scaleFactor = integral_data / integral_MC_raw
        h2.Scale(scaleFactor)
    else:
        print("WARNING: MC integral is zero, not scaling")
    integral_MC_scaled = integral_between(h2, 0.0, 100.0)

    h2.Draw("hist")
    h1.Draw("pE same")
    h3.Draw("hist same")


    if bggen:
        draw_mc_same(
            FND_eventSelectionSkims, "NumCombos", "(300,0.0,100.0)",
            "CUT()"
        )

    draw_info_pad(
        p["info_main"],
        "#bf{Data and MC.}",
        legend_items=[(h1, f"Data (integral: {integral_data:.0f})", "pE"),
                      (h2, f"MC scaled (raw: {integral_MC_raw:.0f} -> scaled: {integral_MC_scaled:.0f})", "f"),
                      (h3, f"Data all cuts (integral: {integral_data_allCuts:.0f})", "f")
                      ],
        notes=["Number of Combos",
               "Integral between (0.0, 100.0)"
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
            (0.08, "Global cuts: CUT()"),
            (0.08, "H1 cuts (DATA): CUT(rf,chi2DOF,coherentPeak,targetZ)"),
            (0.08, "H2 cuts (MC): CUT(rf,chi2DOF,coherentPeak,targetZ)"),
            (0.08, "H3 cuts (DATA): CUT(chi2DOF,unusedTracks,coherentPeak,targetZ,"),
            (0.10, "flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.10, "*CUTWT(rf,KShort,Lambda)"),
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

    # ============================================================
    # Page 1d: RFDeltaT
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_RFDeltaT", "c_eventCuts_RFDeltaT", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_eventSelectionSkims,
        "RFDeltaT",
        "(100,-18.0,18.0)",
        "CUT(chi2DOF,coherentPeak,targetZ)"
    )
    h1.SetXTitle("RFDeltaT")
    h1.SetYTitle("Count")
    h1.SetLineColor(ROOT.kBlack)

    h2 = fs_get_th1(
        FND_eventSelectionSkims_MC,
        "RFDeltaT",
        "(100,-18.0,18.0)",
        "CUT(chi2DOF,coherentPeak,targetZ)"
    )
    h2.SetLineColor(ROOT.kBlue)
    h2.SetFillColor(ROOT.kBlue - 5)
    # scale h2
    h2.Scale(integral_between(h1, -18.0, 18.0) / integral_between(h2, -18.0, 18.0))

    h3 = fs_get_th1(
        FND_eventSelectionSkims,
        "RFDeltaT",
        "(100,-18.0,18.0)",
        "CUT(chi2DOF,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)*CUTSBWT(rf,KShort,Lambda)"
    )
    h3.SetXTitle("RFDeltaT")
    h3.SetYTitle("Count")
    h3.SetLineColor(ROOT.kRed)
    h3.SetFillColor(ROOT.kRed - 5)

    integral_data = integral_between(h1, -18.0, 18.0)
    integral_MC_raw   = integral_between(h2, -18.0, 18.0)
    integral_data_allCuts = integral_between(h3, -18.0, 18.0)
    if integral_MC_raw > 0:
        scaleFactor = integral_data / integral_MC_raw
        h2.Scale(scaleFactor)
    else:
        print("WARNING: MC integral is zero, not scaling")
    integral_MC_scaled = integral_between(h2, -18.0, 18.0)

    h1.Draw("pE")
    h2.Draw("hist same")
    h3.Draw("hist same")


    if bggen:
        draw_mc_same(
            FND_eventSelectionSkims, "RFDeltaT", "(100,-10.0,10.0)",
            "CUT()"
        )

    draw_info_pad(
        p["info_main"],
        "#bf{Data and MC.}",
        legend_items=[(h1, f"Data (integral: {integral_data:.0f})", "pE"),
                      (h2, f"MC scaled (raw: {integral_MC_raw:.0f} -> scaled: {integral_MC_scaled:.0f})", "f"),
                      (h3, f"Data all cuts (integral: {integral_data_allCuts:.0f})", "f")
                      ],
        notes=["RFDeltaT",
               "Integral between (-10.0, 10.0)"
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
            (0.08, "Global cuts: CUT()"),
            (0.08, "H1 cuts (DATA): CUT(chi2DOF,coherentPeak,targetZ)"),
            (0.08, "H2 cuts (MC): CUT(chi2DOF,coherentPeak,targetZ)"),
            (0.08, "H3 cuts (DATA): CUT(chi2DOF,unusedTracks,coherentPeak,targetZ,"),
            (0.10, "flightLengthKShort,flightLengthLambda,rejectSigma1385,selectKSTAR892)"),
            (0.10, "*CUTWT(rf,KShort,Lambda)"),
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
    #     "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak)"
    # )
    # h2.SetXTitle("Production vertex z-position [cm]")
    # h2.SetYTitle("Combinations")
    # h2.Draw("pE")

    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed, "ProdVz", "(100,0.,100.0)",
    #         "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak)"
    #     )
    # draw_vertical_lines(h2, [52.0, 78.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h2, "Data", "pE")],
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
    #         "Global cuts: CUT()",
    #         "Histogram cuts: CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak)",
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


    # ============================================================
    # Page 3: t-range
    # ============================================================
    c = ROOT.TCanvas("c_eventCuts_tRange", "c_eventCuts_tRange", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.22)
    p = panels[0]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_eventSelectionSkims,
        f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
        "(100,0,2)",
        "CUT(rf,chi2DOF,unusedTracks,coherentPeak,targetZ)"
    )
    h1.SetXTitle("|-t| [GeV^{2}]")
    h1.SetYTitle("Combinations")
    h1.SetMinimum(0.5)
    h1.SetLineColor(ROOT.kBlack)

    h2 = fs_get_th1(
        FND_eventSelectionSkims_MC,
        f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
        "(100,0,2)",
        "CUT(rf,chi2DOF,unusedTracks,coherentPeak,targetZ)"
    )
    h2.SetLineColor(ROOT.kBlue)
    h2.SetFillColor(ROOT.kBlue - 5)

    h1.Draw("pE1")
    h2.Draw("pE3")

    # p["plot"].SetLogy(1)
    # p["plot"].Modified()
    # p["plot"].Update()

    if bggen:
        draw_mc_same(
            FND_eventSelectionSkims,
            f"abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
            "(100,0,2)",
            "CUT(rf,chi2DOF,unusedTracks,coherentPeak,targetZ)"
        )
    draw_vertical_lines(h1, [0.1, 1.0])

    draw_info_pad(
        p["info_main"],
        "#bf{Data and MC.}",
        legend_items=[
            (h1, "Data", "pE1"),
            (h2, "MC", "pE3")
            ],
        notes=["Cut: 0.1 < |-t| < 1.0"],

        # --- layout tweaks ---
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
            "Global cuts: CUT()",
            "Histogram cuts: CUT(rf,chi2DOF,unusedTracks,coherentPeak,targetZ)",
            f"Plotted variable: abs(-1*MASS2(GLUEXTARGET,-{DecayingLambda}))",
        ],

        # --- bottom pad tweaks ---
        title_pos=(0.06, 0.88),
        title_size=0.11,

        notes_start_y=0.72,
        notes_text_size=0.10,
        notes_step=0.12,

    )

    # c.Print(pdf_path)
    c.Print(f"{pdf_path})")



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
    #     "(100,5,12)",
    #     "CUT(tRange110,rf,chi2DOF,unusedTracks,targetZ)"
    # )
    # h4.SetXTitle("E_{beam} [GeV]")
    # h4.SetYTitle("Combinations")
    # h4.Draw("pE")

    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed, "EnPB", "(125,5,12)",
    #         "CUT(tRange110,rf,chi2DOF,unusedTracks,targetZ)"
    #     )
    # draw_vertical_lines(h4, [8.2, 8.6])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h4, "Data", "pE")],
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
    #         "Global cuts: CUT()",
    #         "Histogram cuts: CUT(tRange110,rf,chi2DOF,unusedTracks,targetZ)",
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
    #     "CUT(tRange110,rf,unusedTracks,coherentPeak,targetZ)"
    # )
    # h5.SetXTitle("#chi^{2}/dof")
    # h5.SetYTitle("Combinations")
    # h5.Draw("pE")

    # if bggen:
    #     draw_mc_same(
    #         FND_unSkimmed, "Chi2DOF", "(80,0,20)",
    #         "CUT(tRange110,rf,unusedTracks,coherentPeak,targetZ)"
    #     )
    # draw_vertical_lines(h5, [5.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h5, "Data", "pE")],
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
    #         "Global cuts: CUT()",
    #         "Histogram cuts: CUT(tRange110,rf,unusedTracks,coherentPeak,targetZ)",
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
    #     "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ,Lambda)"
    # )
    # h6.SetXTitle("#Lambda flight length [cm]")
    # h6.SetYTitle("Combinations")
    # h6.Draw("pE")
    # draw_vertical_lines(h6, [2.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h6, "Data", "pE")],
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
    #         "Global cuts: CUT()",
    #         "Histogram cuts: CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ,Lambda)",
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
    #     "CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ,KShort)"
    # )
    # h7.SetXTitle("K_{S} flight length [cm]")
    # h7.SetYTitle("Combinations")
    # h7.Draw("pE")
    # draw_vertical_lines(h7, [2.0])

    # draw_info_pad(
    #     p["info_main"],
    #     file_label(FND_unSkimmed),
    #     legend_items=[(h7, "Data", "pE")],
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
    #         "Global cuts: CUT()",
    #         "Histogram cuts: CUT(tRange110,rf,chi2DOF,unusedTracks,coherentPeak,targetZ,KShort)",
    #         "Plotted variable: VeeLP2",
    #     ],

    #     # --- bottom pad tweaks ---
    #     title_pos=(0.06, 0.88),
    #     title_size=0.11,

    #     notes_start_y=0.75,
    #     notes_text_size=0.08,
    #     notes_step=0.10,

    # )

    # # c.Print(pdf_path)
    # c.Print(f"{pdf_path})")





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

    # c.Print(pdf_path)
    c.Print(f"{pdf_path}(")
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
    hData_FLon.SetLineColor(ROOT.kBlue)
    hData_FLon.SetFillColor(ROOT.kBlue -5)
    hData_FLoff.SetLineColor(ROOT.kBlack)
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

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")
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

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)


    hData.Draw("hist")
    hSig.Draw("pE same")
    hBkgNegative.Draw("hist same")

    xmin, xmax = 0.4676, 0.5276   # K_S mass 0.4976 +/- 0.03
    integral_ks = integral_between(hData, xmin, xmax)
    integral_ksSig = integral_between(hSig, xmin, xmax)
    integral_ksBkg = integral_between(hBkg, xmin, xmax)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "M(#pi^{+} #pi^{-}) " "(Integral: " f"{integral_ks:.0f})", "f"),
            (hSig, "K_{s} Signal " "(Integral: " f"{integral_ksSig:.0f})", "pE"),
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

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)

    hData.Draw("hist")
    hSig.Draw("pE same")
    hBkgNegative.Draw("hist same")

    xmin, xmax = 0.4676, 0.5276   # K_S mass 0.4976 +/- 0.03
    integral_data = integral_between(hData, xmin, xmax)
    integral_sig  = integral_between(hSig, xmin, xmax)
    integral_bkg  = integral_between(hBkg, xmin, xmax)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, f"K_{{S}} MM (Integral: {integral_data:.0f})", "f"),
            (hSig,  f"K_{{S}} MM Signal (Integral: {integral_sig:.0f})", "pE"),
            (hBkgNegative, f"K_{{S}} MM Background (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["Missing mass K_{S}"],
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.10,
        notes_start_y=0.68,
        notes_text_size=0.14,
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
        notes_step=0.08,
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

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)


    hData.Draw("hist")
    hSig.Draw("pE same")


    xmin, xmax = 0.4676, 0.5276   # K_S mass 0.4976 +/- 0.03
    integral_ks = integral_between(hData, xmin, xmax)
    integral_ksSig = integral_between(hSig,xmin, xmax)

    draw_vertical_lines(hData, [xmin, xmax])

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "M(#pi^{+} #pi^{-}) " "(Integral: " f"{integral_ks:.0f})", "f"),
            (hSig, "K_{s} Signal " "(Integral: " f"{integral_ksSig:.0f})", "pE"),
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

    hData_FLon.SetLineColor(ROOT.kBlue)
    hData_FLon.SetFillColor(ROOT.kBlue -5)
    hData_FLoff.SetLineColor(ROOT.kBlack)
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
    integral_FLoff = integral_between(hData_FLoff, xmin, xmax)
    integral_FLon  = integral_between(hData_FLon,  xmin, xmax)

    # integrate under signal and background components separately.
    # NOTE: The integrals below are already calculated by 'compute_figureOfMerit' function;
    # They are created here only as a double-check.
    integral_fit_FLoff_voigt = fit_integral_signal(fit_FLoff,     xmin, xmax, bin_width=bin_width)
    integral_fit_FLoff_expo2 = fit_integral_background(fit_FLoff, xmin, xmax, bin_width=bin_width)

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

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)

    hData.Draw("hist")
    hSig.Draw("pE same")
    hBkgNegative.Draw("hist same")

    xmin, xmax = 1.10525, 1.13275
    integral_Lamb = integral_between(hData, xmin, xmax)
    integral_LambSig = integral_between(hSig, xmin, xmax)
    integral_LambBkg = integral_between(hBkg, xmin, xmax)


    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "M(p #pi^{+}) " "(Integral: " f"{integral_Lamb:.0f})", "f"),
            (hSig, "Lambda Signal " "(Integral: " f"{integral_LambSig:.0f})", "pE"),
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

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)

    hData.Draw("hist")
    hSig.Draw("pE same")
    hBkgNegative.Draw("hist same")

    integral_data = integral_between(hData, 1.08, 1.20)
    integral_sig  = integral_between(hSig, 1.08, 1.20)
    integral_bkg  = integral_between(hBkg, 1.08, 1.20)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, f"#Lambda MM (Integral: {integral_data:.0f})", "f"),
            (hSig,  f"#Lambda MM Signal (Integral: {integral_sig:.0f})", "pE"),
            (hBkgNegative, f"#Lambda MM Background (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["Missing mass #Lambda"],
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,
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
            f"Global cuts: {generalCuts_eventSelection}",
            f"Base cuts: CUT({baseCuts},{sidebandCuts})",
            f"Signal: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"Background: CUT({baseCuts})*CUTSBWT({sidebandCuts})",
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.12,
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

    hData.SetLineColor(ROOT.kBlack)
    hSig.SetLineColor(ROOT.kBlue)
    hSig.SetFillColor(ROOT.kBlue -5)


    hData.Draw("pE")
    hSig.Draw("hist same")

    xmin, xmax = 1.10525, 1.13275
    integral_ks = integral_between(hData, xmin, xmax)
    integral_ksSig = integral_between(hSig, xmin, xmax)

    draw_vertical_lines(hData, [xmin, xmax])

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

# -------- DELTA MISSING-MASS KSHORT -------------
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
    hData.GetXaxis().SetNdivisions(5, 5, 0, ROOT.kTRUE)

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)

    hData.Draw("hist")
    hSig.Draw("pE same")
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
            (hData, f"K_{{S}} #DeltaM (Integral: {integral_data:.0f})", "f"),
            (hSig, f"K_{{S}} Signal #DeltaM (Integral: {integral_sig:.0f})", "pE"),
            (hBkgNegative, f"K_{{S}} Background #DeltaM (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["#DeltaM(K_{S}) = M(K_{S}) - MM(#Lambda#pi^{+})"],
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.12,
        notes_start_y=0.68,
        notes_text_size=0.12,
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
        notes_step=0.12,
    )

    c.Print(pdf_path)
    ROOT.FSHistogram.clearHistogramCache()



# ----------- DELTA MISSING-MASS LAMBDA -------------
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
    hData.GetXaxis().SetNdivisions(5, 5, 0, ROOT.kTRUE)

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)

    hData.Draw("hist")
    hSig.Draw("pE same")
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
            (hData, f"#Lambda #DeltaM (Integral: {integral_data:.0f})", "f"),
            (hSig, f"#Lambda Signal #DeltaM (Integral: {integral_sig:.0f})", "pE"),
            (hBkgNegative, f"#Lambda Background #DeltaM (Integral: {integral_bkg:.0f})", "f"),
        ],
        notes=["#DeltaM(#Lambda) = M(#Lambda) - MM(K_{S}#pi^{+})"],
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.12,
        notes_start_y=0.68,
        notes_text_size=0.12,
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
        notes_step=0.12,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path})")
    ROOT.FSHistogram.clearHistogramCache()

# ------------------------------------------------------------
# BACKGROUND PLOT: LAMBDA-PI+  (2D map)
# ------------------------------------------------------------
def massPlots_lambdaPiBackground2D(pdf_path):
    c = ROOT.TCanvas("c_baryon_bkg_2d", "c_baryon_bkg_2d", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.30)
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

    # Draw a vertical line at x = 2.0 to indicate the cut for baryon background
    ylo = h2.GetYaxis().GetXmin()
    yhi = h2.GetYaxis().GetXmax()
    xcut = 2.0
    cutLine = ROOT.TLine(xcut, ylo, xcut, yhi)
    cutLine.SetLineColor(ROOT.kBlue)
    cutLine.SetLineWidth(2)
    cutLine.Draw("same")
    keep(cutLine)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[],
        notes=["Baryon background study (correlation plot)"],
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.12,
        notes_start_y=0.68,
        notes_text_size=0.12,
        notes_step=0.12,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"CUT(tRange110,flightLengthKShort,flightLengthLambda)*CUTWT({sidebandCuts})",
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.12,
    )

    c.Print(pdf_path)


# ------------------------------------------------------------
# BACKGROUND PLOT: LAMBDA-PI+  (1D projection)
# ------------------------------------------------------------
def massPlots_lambdaPiBackground1D(pdf_path):
    c = ROOT.TCanvas("c_baryon_bkg_1d", "c_baryon_bkg_1d", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.30)
    p = panels[0]
    p["plot"].cd()

    h1 = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingLambda},{PiPlus1})",
        "(80,1.20,3.60)",
        f"CUT(tRange110,flightLengthKShort,flightLengthLambda)*CUTWT({sidebandCuts})"
    )
    h1.SetXTitle("M(#Lambda#pi^{+}) [GeV/c^{2}]")
    h1.SetYTitle("Counts")
    h1.SetMinimum(0.0)
    h1.SetLineColor(ROOT.kBlack)
    h1.Draw("pE")

    draw_vertical_lines(h1, [2.0, 2.0])

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[(h1, "Data", "pE")],
        notes=["Select events between 2.0 < M(#Lambda#pi^{+}) < 4.0", "Which rejects #Sigma(1385)"],
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.12,
        notes_start_y=0.68,
        notes_text_size=0.16,
        notes_step=0.12,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"CUT(tRange110,flightLengthKShort,flightLengthLambda)*CUTWT({sidebandCuts})",
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.12,
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
    hSig1.SetYTitle("Counts / 40 MeV")

    hSig1.SetLineColor(ROOT.kGray + 3)
    hSig1.SetFillColor(ROOT.kGray + 2)
    hSig2.SetLineColor(ROOT.kMagenta)
    hSig2.SetFillColor(ROOT.kMagenta - 3)
    hSig3.SetLineColor(ROOT.kGreen)
    hSig3.SetFillColor(ROOT.kGreen - 3)
    hSig4.SetLineColor(ROOT.kBlue)
    hSig4.SetFillColor(ROOT.kBlue - 5)

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
# KSTAR MASS PLOTS -- UNUSED ENERGY STUDY STUDY
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
    hSig1.SetYTitle("Counts / 40 MeV")

    hSig1.SetLineColor(ROOT.kBlue)
    hSig1.SetFillColor(ROOT.kBlue -5)
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
            (0.08, "Unused Shower Energy Study"),
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


# ------------------------------------------------------------
# MISSING MASS KSTAR PLOTS -- SIDEBAND STUDY
# ------------------------------------------------------------
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

    hData.SetXTitle("MM(#Lambda) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 40 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)

    hData.Draw("hist")
    hSig.Draw("pE same")
    hBkgNegative.Draw("hist same")

    draw_vertical_lines(hData, [0.8, 1.0], color=ROOT.kRed)

    xmin, xmax = 0.634, 2.203
    # integral_kStar = integral_between(hData, xmin, xmax)
    integral_kStarSig  = integral_between(hSig,  xmin, xmax)
    # integral_kStarBkg = integral_between(hBkg, xmin, xmax)

    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "MM(#Lambda): Data", "f"),
            (hSig, "MM(#Lambda): Signal " "(Integral: " f"{integral_kStarSig:.0f})", "pE"),
            (hBkgNegative, "MM(#Lambda): Background", "f"),
        ],
        notes=[
            "Missing-mass sideband subtraction study",
        ],
        legend_box=(0.48, 0.18, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.10,
        notes_start_y=0.62,
        notes_text_size=0.12,
        notes_step=0.8,
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
        "(63,0.634,2.203)",
        "CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,rf,KShort,Lambda)"
    )
    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(63,0.634,2.203)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
    )
    hBkg = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(63,0.634,2.203)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTSBWT({sidebandCuts})"
    )
    hBkgNegative = hBkg.Clone("hBkgNegative")
    hBkgNegative.Scale(-1.0)

    hData.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts / 25 MeV")
    hData.SetMinimum(-1.2 * abs(hBkgNegative.GetMinimum()))

    hData.SetLineColor(ROOT.kBlue)
    hData.SetFillColor(ROOT.kBlue - 5)
    hSig.SetLineColor(ROOT.kBlack)
    hBkgNegative.SetLineColor(ROOT.kRed)
    hBkgNegative.SetFillColor(ROOT.kRed - 3)

    hData.Draw("hist")
    hSig.Draw("pE same")
    hBkgNegative.Draw("hist same")

    integral_kStarSig  = integral_between(hSig,  0.634,2.203)
    
    p["plot"].Modified()
    p["plot"].Update()


    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hData, "M(Ks #pi^{+}) Data", "f"),
            (hSig, f"M(Ks #pi^{{+}}) Signal {integral_kStarSig:.0f} M(0.634,2.203)", "pE"),
            (hBkgNegative, "M(Ks #pi^{+}) SB Background", "f"),
        ],
        notes=[
            (0.08, "Final K* Selection"),
            (0.08, "3D sideband background = "),
            (0.10, "accidental beam photons x"),
            (0.12, "x Ks sidebands x Lambda sidebands"),
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
            (0.08, "Global skim cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"),
            (0.08, "Data: CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385,rf,KShort,Lambda)"),
            (0.08, "Histogram cuts Sig:  CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)"),
            (0.10, f"*CUTWT({sidebandCuts})"),
            (0.08, f"Bkg:  CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTSBWT({sidebandCuts})"),
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.72,
        notes_text_size=0.060,
        notes_step=0.09,
    )

    c.Print(pdf_path) 
    # c.Print(f"{pdf_path}(") 

# ------------------------------------------------------------
# KSTAR MASS PLOTS -- non-relativistic fit
# ------------------------------------------------------------
def massPlots_KStar_nonRelFIT(pdf_path):
    c = ROOT.TCanvas("c_kstar_sidebands", "c_kstar_sidebands", 1000, 1300)
    keep(c)

    panels = make_panel_grid(c, ncols=1, nrows=1, info_frac=0.36)
    p = panels[0]
    p["plot"].cd()

    hSig = fs_get_th1(
        FND_eventSelectionSkims,
        f"MASS({DecayingKShort},{PiPlus1})",
        "(63,0.634,2.203)",
        f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})"
    )

    hSig.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hSig.SetYTitle("Counts / 25 MeV")
    hSig.SetLineColor(ROOT.kBlack)
    hSig.Draw("pE")

    integral_kStarSig  = integral_between(hSig,  0.634,2.203)

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

    fitSig_kstar = _make_kstar_fit("fitSig_kstar_2voigt_bern", amp2=400.0)
    _apply_kstar_limits(fitSig_kstar)
    hSig.Fit(fitSig_kstar, "R0")
    log_fit_results(fitSig_kstar,
                    hist_name="hSig",
                    cut_string=f"CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)*CUTWT({sidebandCuts})",
                    xmin=0.61, xmax=2.3,
                    logFile=logFile,
                    notes=["FOM integration range: (0.80, 1.00)"])
    fitSig_kstar.SetLineColor(ROOT.kMagenta + 2)
    fitSig_kstar.SetLineWidth(3)
    fitSig_kstar.Draw("same")

    fit_voigt1, fit_voigt2, fit_bern = make_component_funcs_kstar(fitSig_kstar, xmin=0.61, xmax=2.3, bern_degree=3)
    fit_voigt1.SetLineColor(ROOT.kOrange)
    fit_voigt1.SetLineStyle(ROOT.kDotted)
    fit_voigt1.SetLineWidth(3)
    fit_voigt2.SetLineColor(ROOT.kOrange)
    fit_voigt2.SetLineStyle(ROOT.kDotted)
    fit_voigt2.SetLineWidth(3)
    fit_bern.SetLineColor(ROOT.kOrange + 7)
    fit_bern.SetLineStyle(ROOT.kDotted)
    fit_bern.SetLineWidth(2)
    fit_voigt1.Draw("same")
    fit_voigt2.Draw("same")
    fit_bern.Draw("same")

    p["plot"].Modified()
    p["plot"].Update()

    xmin, xmax = 0.80, 1.00
    bin_width = hSig.GetXaxis().GetBinWidth(1)

    S1_h2, S2_h2, S_h2, B_h2, SB_h2, significance_h2, purity_h2 = compute_figureOfMerit_kstar(
        fitSig_kstar, xmin, xmax, bin_width=bin_width, bern_degree=3
    )


    draw_info_pad(
        p["info_main"],
        file_label(FND_eventSelectionSkims),
        legend_items=[
            (hSig,         f"M(Ks #pi^{{+}}) total int {integral_kStarSig:.0f} M(0.634,2.203)", "pE"),
            (fitSig_kstar, "Fit: 2 Voigtians + Bernstein", "l"),
            (fit_voigt1,   "Fit: Voigtian", "l"),
            (fit_bern,     "Fit: Bernstein", "l"),
        ],
        notes=[
            (0.08, "Non-relativistic fit"),
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
            (0.08, "Global skim cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"),
            (0.08, "Histogram cuts Sig:  CUT(flightLengthKShort,flightLengthLambda,rejectSigma1385)"),
            (0.10, f"*CUTWT({sidebandCuts}). Sig: {S1_h2:.0f}, Bkg: {B_h2:.0f}"),
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.72,
        notes_text_size=0.060,
        notes_step=0.09,
    )

    c.Print(pdf_path)
    # c.Print(f"{pdf_path}(")


# ------------------------------------------------------------
# ROOFIT KSTAR MASS PLOTS -- RELATIVISTIC FITTING - ROOFIT
# ------------------------------------------------------------
def massPlots_KStar_relROOFIT(pdf_path):
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
    h_Pwave.SetYTitle("Counts / 25 MeV")
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

    integral_kStarSig = integral_between(h_Pwave, 0.634,2.203)

    p["plot"].Modified()
    p["plot"].Update()

    legend_items = [
        (h_Pwave,     f"M(Ks #pi^{{+}}) total int {integral_kStarSig:.0f} M(0.634,2.203)", "pE"),
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
            (0.08, "Relativistic BWs + Bernstein Poly (RooFit)"),
            (0.08, "Integrals: M(Ks #pi^{+}) = (0.8, 1.0) GeV/c^{2}"),
            (0.08, "K*(892) yield, Sig/Bkg, Purity S/(S+B):"),
            (0.08, f"Sig. yield: {S:.0f}  S/B: {SoverB:.2f}  Purity: {purity:.2f}"),
        ],
        legend_box=(0.48, 0.18, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.10,
        notes_start_y=0.78,
        notes_text_size=0.060,
        notes_step=0.09,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            (0.08, "Global skim cuts: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ)"),
            (0.08, "Sig skim: CUT(tRange110,chi2DOF,unusedTracks,coherentPeak,targetZ,flightLengthKShort,flightLengthLambda,rejectSigma1385)"),
            (0.08, f"Friend tree skim: CUTWT(rf,KShort,Lambda). Sig: {S:.0f}, Bkg: {B:.0f}"),
            (0.08, "Histogram cuts: none"),
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

    integral = integral_between(hData, 0.8, 1.0)

    hData.SetXTitle("M(K_{S}#pi^{+}) [GeV/c^{2}]")
    hData.SetYTitle("Counts")
    hData.SetLineColor(ROOT.kBlue)
    hData.SetLineWidth(2)
    hData.SetMarkerStyle(20)
    hData.SetMarkerSize(0.8)
    hData.SetMinimum(0.0)

    hMC.SetLineColor(ROOT.kRed)
    hMC.SetLineWidth(2)
    hMC.SetMarkerStyle(24)
    hMC.SetMarkerColor(ROOT.kRed)
    hMC.SetMarkerSize(0.8)
    # hMC.Scale(0.1)
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
        ],
        legend_box=(0.48, 0.22, 0.96, 0.84),
        legend_text_size=0.10,
        label_pos=(0.06, 0.90),
        label_size=0.12,
        notes_start_y=0.68,
        notes_text_size=0.12,
        notes_step=0.12,
    )
    draw_notes_pad(
        p["info_notes"],
        title="Cuts used",
        notes=[
            f"Data cuts: CUT({baseCuts})*CUTWT({sidebandCuts})",
            f"MC cuts:   CUT({baseCuts})*CUTWT({sidebandCuts})",
        ],
        title_pos=(0.06, 0.88),
        title_size=0.11,
        notes_start_y=0.70,
        notes_text_size=0.075,
        notes_step=0.12,
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
    hData.SetYTitle("Counts")
    hData.SetLineColor(ROOT.kBlack)
    hData.SetLineWidth(2)
    hData.SetMarkerStyle(20)
    hData.SetMarkerSize(0.8)

    hMC.SetLineColor(ROOT.kRed)
    hMC.SetLineWidth(2)
    hMC.SetMarkerStyle(24)
    hMC.SetMarkerColor(ROOT.kRed)
    hMC.SetMarkerSize(0.8)
    # hMC.Scale(0.6)

    hData.Draw("pE")
    hMC.Draw("pE same")

    draw_vertical_lines(hData, [0.80, 1.00])

    draw_info_pad(
        p["info_main"],
        f"{file_label(FND_signalSkims)} / {file_label(FND_signalSkims_MC)}",
        legend_items=[
            (hData, "Data (input to fit) " "(Int: " f"{integral_data:.0f})", "pE"),
            (hMC,   "MC (input to fit) "   "(Int: " f"{integral_MC:.0f})",   "pE"),
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

    global_eventSelection_Cuts(allPlots)
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
    # massPlots_lambdaPiBackground2D(allPlots)
    # massPlots_lambdaPiBackground1D(allPlots)
    # massPlots_KStar_flightLength(allPlots)
    # massPlots_KStar_unusedEnergyStudy(allPlots)
    # missingMassPlots_KStar_sidebands(allPlots)
    # massPlots_KStar_FINAL_SELECTION(allPlots)
    # massPlots_KStar_nonRelFIT(allPlots)
    # massPlots_KStar_relROOFIT(allPlots)
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