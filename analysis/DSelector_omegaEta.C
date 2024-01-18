#include "DSelector_omegaEta.h"

void DSelector_omegaEta::Init(TTree *locTree)
{
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = "omegaEta.root"; //"" for none
	dOutputTreeFileName = ""; //"" for none
	dFlatTreeFileName = ""; //output flat tree (one combo per tree entry), "" for none
	dFlatTreeName = ""; //if blank, default name will be chosen
	//dSaveDefaultFlatBranches = false; // False: don't save default branches, reduce disk footprint.
	//dSaveTLorentzVectorsAsFundamentaFlatTree = false; // Default (or false): save particles as TLorentzVector objects. True: save as four doubles instead.

	//Because this function gets called for each TTree in the TChain, we must be careful:
		//We need to re-initialize the tree interface & branch wrappers, but don't want to recreate histograms
	bool locInitializedPriorFlag = dInitializedFlag; //save whether have been initialized previously
	DSelector::Init(locTree); //This must be called to initialize wrappers for each new TTree
	//gDirectory now points to the output file with name dOutputFileName (if any)
	if(locInitializedPriorFlag)
		return; //have already created histograms, etc. below: exit

	Get_ComboWrappers();
	dPreviousRunNumber = 0;

	/*********************************** EXAMPLE USER INITIALIZATION: ANALYSIS ACTIONS **********************************/

	//INITIALIZE ACTIONS
	//If you create any actions that you want to run manually (i.e. don't add to dAnalysisActions), be sure to initialize them here as well
	Initialize_Actions();
	//dAnalyzeCutActions->Initialize(); // manual action, must call Initialize()

	/******************************** EXAMPLE USER INITIALIZATION: STAND-ALONE HISTOGRAMS *******************************/
	//EXAMPLE MANUAL HISTOGRAMS:
	gDirectory->mkdir( "Beam_and_MMS" )->cd();
	dHist_MissingMassSquared = new TH1D( "MissingMassSquared", ";Missing Mass Squared (GeV)^{2}; Combos / 2 MeV^{2}", 1000, -.1,.1);
	dHist_MissingEnergy = new TH1D( "MissingE", ";Missing Energy (GeV); Combos / 2 MeV", 3000, -3,3 );
	dHist_BeamEnergy = new TH1D( "BeamEnergy", ";Beam Energy (GeV); Combos / 20 MeV", 500, 2.0, 12.0);
	dHist_BeamTiming = new TH1D ("BeamTiming", ";Beam t_{Tagger}-t_{RF} (ns); Combos / .2 ns", 200, -20, 20 );
        gDirectory->cd( ".." );

	gDirectory->mkdir( "Photon_Mass" )->cd();
	gDirectory->mkdir( "Measured" )->cd();
	dHist_Mass_g1_g2_M = new TH1D( "Mass_g1_g2_M", ";Mass[#gamma_{1}#gamma_{2}] (GeV); Combos / 1.1 MeV", 100, 0.08, .19 );
	dHist_Mass_g1_g3_M = new TH1D( "Mass_g1_g3_M", ";Mass[#gamma_{1}#gamma_{3}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g1_g4_M = new TH1D( "Mass_g1_g4_M", ";Mass[#gamma_{1}#gamma_{4}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g2_g3_M = new TH1D( "Mass_g2_g3_M", ";Mass[#gamma_{2}#gamma_{3}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g2_g4_M = new TH1D( "Mass_g2_g4_M", ";Mass[#gamma_{2}#gamma_{4}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g3_g4_M = new TH1D( "Mass_g3_g4_M", ";Mass[#gamma_{3}#gamma_{4}] (GeV); Combos / 1 MeV", 400, .35, .75 );
	gDirectory->cd( ".." );	
	gDirectory->mkdir( "KinFit" )->cd();
	dHist_Mass_g1_g2 = new TH1D( "Mass_g1_g2", ";Mass[#gamma_{1}#gamma_{2}] (GeV); Combos / 1 MeV", 200, 0.05, .25 );
	dHist_Mass_g1_g3 = new TH1D( "Mass_g1_g3", ";Mass[#gamma_{1}#gamma_{3}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g1_g4 = new TH1D( "Mass_g1_g4", ";Mass[#gamma_{1}#gamma_{4}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g2_g3 = new TH1D( "Mass_g2_g3", ";Mass[#gamma_{2}#gamma_{3}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g2_g4 = new TH1D( "Mass_g2_g4", ";Mass[#gamma_{2}#gamma_{4}] (GeV); Combos / 1 MeV", 1200, 0.0, 1.2 );
	dHist_Mass_g3_g4 = new TH1D( "Mass_g3_g4", ";Mass[#gamma_{3}#gamma_{4}] (GeV); Combos / 1 MeV", 700, 0.2, .9 );
	gDirectory->cd( ".." );	
	gDirectory->mkdir( "3Photon" )->cd();
	dHist_Mass_g1_g2_g3 = new TH1D( "Mass_g1_g2_g3", ";Mass[#gamma_{1}#gamma_{2}#gamma_{3}] (GeV); Combos / 1 MeV", 2500, 0.0, 2.5 );
	dHist_Mass_g1_g2_g4 = new TH1D( "Mass_g1_g2_g4", ";Mass[#gamma_{1}#gamma_{2}#gamma_{4}] (GeV); Combos / 1 MeV", 2500, 0.0, 2.5 );
	dHist_Mass_g1_g3_g4 = new TH1D( "Mass_g1_g3_g4", ";Mass[#gamma_{1}#gamma_{3}#gamma_{4}] (GeV); Combos / 1 MeV", 2500, 0.0, 2.5 );
	dHist_Mass_g2_g3_g4 = new TH1D( "Mass_g2_g3_g4", ";Mass[#gamma_{2}#gamma_{3}#gamma_{4}] (GeV); Combos / 1 MeV", 2500, 0.0, 2.5);
	gDirectory->cd( ".." );	
	gDirectory->mkdir( "4Photon" )->cd();
	dHist_Mass_g1_g2_g3_g4 = new TH1D( "Mass_g1_g2_g3_g4", ";Mass[#gamma_{1}#gamma_{2}#gamma_{3}#gamma_{4}] (GeV); Combos / 1 MeV", 2500, 0., 2.5 );
	gDirectory->cd( ".." );	
	gDirectory->mkdir( "2D_Plots_Measured" )->cd();
	dHist_g1g2vsg3g4_M = new TH2D( "g1g2vsg3g4_M", ";Mass[#gamma_{3}#gamma_{4}] (GeV); Mass[#gamma_{1}#gamma_{2}] (GeV)", 400, 0.35, .75, 100, 0.08, .19 );
        dHist_g1g3vsg2g4_M = new TH2D( "g1g3vsg2g4_M", ";Mass[#gamma_{2}#gamma_{4}] (GeV); Mass[#gamma_{1}#gamma_{3}] (GeV)", 750, 0, .75, 750, 0, .75);
        dHist_g1g4vsg2g3_M = new TH2D( "g1g4vsg2g3_M", ";Mass[#gamma_{2}#gamma_{3}] (GeV); Mass[#gamma_{1}#gamma_{4}] (GeV)", 750, 0, .75, 750, 0, .75);
	gDirectory->cd( ".." );	
	gDirectory->mkdir( "2D_Plots_KinFit" )->cd();
	dHist_g1g2vsg3g4 = new TH2D( "g1g2vsg3g4", ";Mass[#gamma_{3}#gamma_{4}] (GeV); Mass[#gamma_{1}#gamma_{2}] (GeV)", 400, 0.35, .75, 100, 0.08, .19 );
        dHist_g1g3vsg2g4 = new TH2D( "g1g3vsg2g4", ";Mass[#gamma_{2}#gamma_{4}] (GeV); Mass[#gamma_{1}#gamma_{3}] (GeV)", 750, 0, .75, 750, 0, .75);
        dHist_g1g4vsg2g3 = new TH2D( "g1g4vsg2g3", ";Mass[#gamma_{2}#gamma_{3}] (GeV); Mass[#gamma_{1}#gamma_{4}] (GeV)", 750, 0, .75, 750, 0, .75);
	gDirectory->cd( ".." );	
	gDirectory->cd( ".." );	

	gDirectory->mkdir( "3particles_Mass" )->cd();
	gDirectory->mkdir( "Measured" )->cd();
	dHist_Mass3pi = new TH1D( "Mass3pi", ";Mass[3#pi] (GeV); Combos / 3 MeV ", 1000, 0.3, 3.3 );
	dHist_Mass2pi_eta = new TH1D( "Mass2pi_eta", ";Mass[2#pi#eta] (GeV); Combos / 3 MeV ", 1000, 0.5, 3.5 );
	dHist_Mass3pivs2piEta = new TH2D( "Mass3pivs2piEta", "; Mass[2#pi#eta] (GeV); Mass[3#pi] (GeV)", 1000, 0.5, 3.5, 1000, 0.3, 3.3 );
	gDirectory->cd( ".." );
	gDirectory->mkdir( "KinFit")->cd();
	dHist_Mass3pi_KinFit = new TH1D( "Mass3pi_KinFit", ";Mass[3#pi] (GeV); Combos / 3 MeV ", 1000, 0.3, 3.3 );
	dHist_Mass2pi_eta_KinFit = new TH1D( "Mass2pi_eta_KinFit", ";Mass[2#pi#eta] (GeV); Combos / 3 MeV ", 1000, 0.5, 3.5 );
	dHist_Mass3pivs2piEta_KinFit = new TH2D( "Mass3pivs2piEta_KinFit","; Mass[2#pi#eta] (GeV); Mass[3#pi] (GeV)", 1000, 0.5, 3.5, 1000, 0.3, 3.3 );
	gDirectory->cd( ".." );	
	gDirectory->cd( ".." );

	gDirectory->mkdir( "Baryons" )->cd();
	dHist_MassPipP = new TH1D( "MassPipP", "; Mass[#pi^{+}p] (GeV); Combos / 5 MeV", 500, 1, 3.5 );
	dHist_MassPimP = new TH1D( "MassPimP", "; Mass[#pi^{-}p] (GeV); Combos / 5 MeV", 500, 1, 3.5 );
	dHist_MassPi0P = new TH1D( "MassPi0P", "; Mass[#pi^{0}p] (GeV); Combos / 5 MeV", 500, 1, 3.5 );
	dHist_MassEtaP = new TH1D( "MassEtaP", "; Mass[#etap] (GeV); Combos / 5 MeV", 500, 1, 3.5 );
	dHist_MassOmegaP = new TH1D( "MassOmegaP", "; Mass[#omegap] (GeV); Combos / 5 MeV", 600, 1, 4 );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "Mesons" )->cd();
	dHist_MassPipPim =  new TH1D( "MassPipPim", ";Mass[#pi^{+}#pi^{-}] (GeV); Combos / 5 MeV", 400, .2, 2.2 );
	dHist_MassPipPi0 =  new TH1D( "MassPipPi0", ";Mass[#pi^{+}#pi^{0}] (GeV); Combos / 5 MeV", 400, .2, 2.2 );
	dHist_MassPipEta =  new TH1D( "MassPipEta", ";Mass[#pi^{+}#eta] (GeV); Combos / 5 MeV", 400, .2, 2.2 );
	dHist_MassPimPi0 =  new TH1D( "MassPimPi0", ";Mass[#pi^{-}#pi^{0}] (GeV); Combos / 5 MeV", 400, .2, 2.2 );
	dHist_MassPimEta =  new TH1D( "MassPimEta", ";Mass[#pi^{-}#eta] (GeV); Combos / 5 MeV", 400, .2, 2.2 );
	dHist_MassPi0Eta =  new TH1D( "MassPi0Eta", ";Mass[#pi^{0}#eta] (GeV); Combos / 5 MeV", 400, .2, 2.2 );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "Baryon_Meson" )->cd();
	dHist_pipPvspimPi0 = new TH2D( "pipPvspimPi0", ";Mass[#pi^{-}#pi^{0}] (GeV); Mass[#pi^{+}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_pipPvspimEta = new TH2D( "pipPvspimEta", ";Mass[#pi^{-}#eta] (GeV); Mass[#pi^{+}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_pipPvspi0Eta = new TH2D( "pipPvspi0Eta", ";Mass[#pi^{0}#eta] (GeV); Mass[#pi^{+}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );

	dHist_pimPvspipPi0 = new TH2D( "pimPvspipPi0", ";Mass[#pi^{+}#pi^{0}] (GeV); Mass[#pi^{-}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_pimPvspipEta = new TH2D( "pimPvspipEta", ";Mass[#pi^{-}#eta] (GeV); Mass[#pi^{-}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_pimPvspi0Eta = new TH2D( "pimPvspi0Eta", ";Mass[#pi^{0}#eta] (GeV); Mass[#pi^{-}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );

	dHist_pi0PvspipPim = new TH2D( "pi0PvspipPim", ";Mass[#pi^{+}#pi^{-}] (GeV); Mass[#pi^{0}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_pi0PvspipEta = new TH2D( "pi0PvspipEta", ";Mass[#pi^{+}#eta] (GeV); Mass[#pi^{0}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_pi0PvspimEta = new TH2D( "pi0PvspimEta", ";Mass[#pi^{-}#eta] (GeV); Mass[#pi^{0}p] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );

	dHist_etaPvspipPim = new TH2D( "etaPvspipPim", ";Mass[#pi^{+}#pi^{-}] (GeV); Mass[#etap] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_etaPvspipPi0 = new TH2D( "etaPvspipPi0", ";Mass[#pi^{+}#pi^{0}] (GeV); Mass[#etap] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );
	dHist_etaPvspimPi0 = new TH2D( "etaPvspimPi0", ";Mass[#pi^{-}#pi^{0}] (GeV); Mass[#etap] (GeV)", 230, .2, 2.5, 250, 1, 3.5 );

	dHist_OmegaEtavsEtaP = new TH2D( "OmegaEtavsEtaP", "; Mass[#etap] (GeV); Mass[#omega#eta] (GeV)", 250, .7, 3.7, 260, 1.1, 3.7 );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "MesonsVsMesons" )->cd();
	dHist_pipPimvspi0Eta = new TH2D( "pipPimvspi0Eta", ";Mass[#pi^{0}#eta] (GeV); Mass[#pi^{+}#pi^{-}] (GeV)", 230, .2, 2.5, 230, .2, 2.5 );
	dHist_pipPi0vspimEta = new TH2D( "pipPi0vspimEta", ";Mass[#pi^{-}#eta] (GeV); Mass[#pi^{+}#pi^{0}] (GeV)", 230, .2, 2.5, 230, .2, 2.5 );
	dHist_pipEtavspimPi0 = new TH2D( "pipEtavspimPi0", ";Mass[#pi^{+}#eta] (GeV); Mass[#pi^{-}#pi^{0}] (GeV)", 230, .2, 2.5, 230, .2, 2.5 );
	gDirectory->mkdir( "3piVsEta" )->cd();
	dHist_3pivsg3g4_M = new TH2D( "3pivsg3g4_M", ";Mass[#gamma_{3}#gamma_{4}] (GeV); Mass[3#pi] (GeV)", 400, 0.35, .75, 1000, 0.3, 3.3 );
	dHist_3pivsg3g4 = new TH2D( "3pivsg3g4", ";Mass[#gamma_{3}#gamma_{4}] (GeV); Mass[3#pi] (GeV)", 400, 0.35, .75, 1000, 0.3, 3.3 );
	gDirectory->cd( ".." );	
	gDirectory->cd( ".." );

	gDirectory->mkdir( "3pi_Eta_Mass" )->cd();
	gDirectory->mkdir( "Measured" )->cd();
	dHist_Mass3piEta = new TH1D( "Mass3piEta", ";Mass[3#pi#eta] (GeV); Combos / 12 MeV ", 250, 0.7, 3.7 );
	dHist_MassOmegaEta = new TH1D( "MassOmegaEta", ";Mass[#omega#eta] (GeV); Combos / 12 MeV ", 250, 0.7, 3.7 );
	gDirectory->cd( ".." );
	gDirectory->mkdir( "KinFit" )->cd();
	dHist_Mass3piEta_KinFit = new TH1D( "Mass3piEta_KinFit", ";Mass[3#pi#eta] (GeV); Combos / 12 MeV ", 250, 0.7, 3.7 );
	dHist_MassOmegaEta_KinFit = new TH1D( "MassOmegaEta_KinFit", ";Mass[#omega#eta] (GeV); Combos / 12 MeV ", 250, 0.7, 3.7 );
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );	

	gDirectory->mkdir( "PID_Proton" )->cd();
	gDirectory->mkdir( "Delta" )->cd();
	//Delta T vs P
	dHist_DeltaTVsP_Proton_BCAL = new TH2D( "DeltaTVsP_Proton_BCAL", ";Momentum Proton (GeV); #DeltaT_{Measured - RF} BCAL (ns)", 250, 0, 10, 50 , -1, 1 );
	dHist_DeltaTVsP_Proton_TOF = new TH2D( "DeltaTVsP_Proton_TOF", ";Momentum Proton (GeV); #DeltaT_{Measured - RF} TOF (ns)", 250, 0, 10, 25, -.5, .5 );
	gDirectory->cd( ".." );
	gDirectory->mkdir( "dEdx" )->cd();
	//dEdx Plots
	dHist_dEdxVsP_Proton_CDC = new TH2D( "dEdxvsP_Proton_CDC", ";Momentum Proton (GeV); CDC dE/dx", 250, 0, 10, 250, 0, 25 );
	gDirectory->cd( ".." );
	gDirectory->mkdir( "Vertex" )->cd();
	dHist_VertexProtonZ = new TH1D( "VertexProtonZ_M", ";Z Vertex Proton (cm); Combos / .05 cm", 1000, 45, 95 );
	dHist_VertexProtonXY = new TH2D( "VertexProtonXY_M", ";X Vertex Proton (cm); Y Vertex Proton (cm)", 160, -4, 4, 160, -4, 4 );
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "PID_PiP" )->cd();
	gDirectory->mkdir( "Delta" )->cd();
	//Delta T vs P
	dHist_DeltaTVsP_PiP_BCAL = new TH2D( "DeltaTVsP_PiP_BCAL", ";Momentum #pi^{+} (GeV); #DeltaT_{Measured - RF} BCAL (ns)", 250, 0, 10, 50 , -1, 1 );
	dHist_DeltaTVsP_PiP_TOF = new TH2D( "DeltaTVsP_PiP_TOF", ";Momentum #pi^{+} (GeV); #DeltaT_{Measured - RF} TOF (ns)", 250, 0, 10, 25, -.5, .5 );
	gDirectory->cd( ".." );
	gDirectory->mkdir( "dEdx" )->cd();
	//dEdx Plots
	dHist_dEdxVsP_PiP_CDC = new TH2D( "dEdxvsP_PiP_CDC", ";Momentum #pi^{+} (GeV); CDC dE/dx", 250, 0, 10, 250, 0, 25);
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "PID_PiM" )->cd();
	gDirectory->mkdir( "Delta" )->cd();
	//Delta T vs P
	dHist_DeltaTVsP_PiM_BCAL = new TH2D( "DeltaTVsP_PiM_BCAL", ";Momentum #pi^{-} (GeV); #DeltaT_{Measured - RF} BCAL (ns)", 250, 0, 10, 50, -1, 1 );
	dHist_DeltaTVsP_PiM_TOF = new TH2D( "DeltaTVsP_PiM_TOF", ";Momentum #pi^{-} (GeV); #DeltaT_{Measured - RF} TOF (ns)", 250, 0, 10, 25, -.5, .5 );
	gDirectory->cd( ".." );
	gDirectory->mkdir( "dEdx" )->cd();
	//dEdx Plots
	dHist_dEdxVsP_PiM_CDC = new TH2D( "dEdxvsP_PiM_CDC", ";Momentum #pi^{-} (GeV); CDC dE/dx", 250, 0, 10, 250, 0, 25);
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );
	
	gDirectory->mkdir( "PID_Photon" )->cd();
	gDirectory->mkdir( "Delta" )->cd();
	//Delta T vs P
	dHist_DeltaTVsP_Photon_FCAL = new TH2D( "DeltaTVsP_Photon_FCAL", ";Momentum Photon (GeV); #DeltaT_{Measured - RF} FCAL (ns)", 250, 0, 10, 100, -2, 2 );//deltaT-RF
	dHist_DeltaTVsP_Photon_BCAL = new TH2D( "DeltaTVsP_Photon_BCAL", ";Momentum Photon (GeV); #DeltaT_{Measured - RF} BCAL (ns)", 250, 0, 10, 50, -1, 1 );
	gDirectory->cd( ".." );
	gDirectory->mkdir( "Showers" )->cd();
	dHist_ShowerQuality1 = new TH1D( "ShowerQuality1", ";#gamma_{1} Shower Quality; Combos / .01", 100, 0, 1 );
	dHist_ShowerQuality2 = new TH1D( "ShowerQuality2", ";#gamma_{2} Shower Quality; Combos / .01", 100, 0, 1 );
	dHist_ShowerQuality3 = new TH1D( "ShowerQuality3", ";#gamma_{3} Shower Quality; Combos / .01", 100, 0, 1 );
	dHist_ShowerQuality4 = new TH1D( "ShowerQuality4", ";#gamma_{4} Shower Quality; Combos / .01", 100, 0, 1 );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "Unused_Showers" )->cd();
	dHist_UnusedShowerEnergy = new TH1D( "UnusedShowerEnergy", ";Unused Shower Energy (GeV); Combos / 10 MeV", 500, 0 , 5 );
	dHist_MassPi0_MvsUS = new TH2D( "MassPi0_MvsUS", ";Unused Shower Energy (GeV); Mass[#pi^{0}] (GeV)", 500, 0 , 5, 100, 0.08, .19 );
	dHist_MassEtavsUS = new TH2D( "MassEtavsUS", ";Unused Shower Energy (GeV); Mass[#eta] (GeV)", 500, 0 , 5, 400, 0.35, .75 );
	dHist_MEvsUS = new TH2D( "MEvsUS", ";Unused Shower Energy (GeV); ME (GeV)", 500, 0 , 5, 600, -3, 3 );
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "Kinematics" )->cd();

	//Note *** t_p, t_etap, and t_omegap are more likely u ***
	gDirectory->mkdir( "T" )->cd();	
	gDirectory->mkdir( "T_omega" )->cd();	
	dHist_tprime_omega = new TH1D( "tprime_omega", ";t_{#omega} (GeV^{2}); Combos/ 20 MeV^{2}", 150, 0, 3 );
	dHist_t_omegaVsOmegaEtaMass = new TH2D( "t_omegaVsOmegaEtaMass", ";Mass[#omega#eta] (GeV); t_{#omega} (GeV^{2})", 250, 0.7, 3.7, 150, 0, 10);
	dHist_t_omegaVsEtaPMass = new TH2D( "t_omegaVsEtaPMass", ";Mass[#etap] (GeV); t_{#omega} (GeV^{2})", 250, 1, 3.5, 150, 0, 10);
	dHist_tprime_omegaVsEtaPMass = new TH2D( "tprime_omegaVsEtaPMass", ";Mass[#etap] (GeV); t'_{#omega} (GeV^{2})", 500, 1, 3.5, 150, 0, 3);
	dHist_t_omegaVsPi0EtaMass = new TH2D( "t_omegaVsPi0EtaMass", ";Mass[#pi^{0}#eta] (GeV); t_{#omega} (GeV^{2})", 400, .2, 2.2, 150, 0, 10);
	dHist_t_omegaVsVHAngle = new TH2D( "t_omegaVsVHAngle", ";VanHove Angle (rad); t_{#omega} (GeV^{2})",320, 0, 2*TMath::Pi(), 150, 0, 10);
	gDirectory->cd( ".." );
	gDirectory->mkdir( "T_omegaEta" )->cd();	
	dHist_tprime = new TH1D( "tprime", ";t'_{#omega#eta} (GeV^{2}); Combos/ 20 MeV^{2}", 150, 0, 3 );
	dHist_t = new TH1D( "t", ";t_{#omega#eta} (GeV^{2}); Combos/ 20 MeV^{2}", 150, 0, 3 );
	dHist_tprimeVs4Mass = new TH2D( "tprimeVs4Mass", ";Mass[3#pi#eta] (GeV); t'_{#omega#eta} (GeV^{2})", 250, 0.7, 3.7, 150, 0, 3);
	dHist_tprimeVs3piMass = new TH2D( "tprimeVs3piMass", ";Mass[3#pi] (GeV); t'_{#omega#eta} (GeV^{2})", 250, 0.3, 3.3, 150, 0, 3);
	dHist_tprimeVs2piEtaMass = new TH2D( "tprimeVs2piEtaMass", ";Mass[2#pi#eta] (GeV); t'_{#omega#eta} (GeV^{2})", 250, 0.5, 3.5, 150, 0, 3);
	dHist_t_omegaEtaVsOmegaEtaMass = new TH2D( "t_omegaEtaVsOmegaEtaMass", ";Mass[#omega#eta] (GeV); t_{#omega#eta} (GeV^{2})", 250, 0.7, 3.7, 150, 0, 10);
	dHist_t_omegaEtaVsEtaPMass = new TH2D( "t_omegaEtaVsEtaPMass", ";Mass[#etap] (GeV); t_{#omega#eta} (GeV^{2})", 500, 1, 3.5, 150, 0, 10);
	dHist_t_omegaEtaVsPi0EtaMass = new TH2D( "t_omegaEtaVsPi0EtaMass", ";Mass[#pi^{0}#eta] (GeV); t_{#omega#eta} (GeV^{2})", 400, 0.2, 2.2, 150, 0, 10);
	dHist_t_omegaEtaVsVHAngle = new TH2D( "t_omegaEtaVsVHAngle", ";VanHove Angle (rad); t_{#omega#eta} (GeV^{2})", 320, 0, 2*TMath::Pi(), 150, 0, 10);
	gDirectory->cd( ".." );
	gDirectory->mkdir( "T_eta" )->cd();	
	dHist_t_etaVsOmegaEtaMass = new TH2D( "t_etaVsOmegaEtaMass", ";Mass[#omega#eta] (GeV); t_{#eta} (GeV^{2})", 250, 0.7, 3.7, 150, 0, 10);
	dHist_t_etaVsEtaPMass = new TH2D( "t_etaVsEtaPMass", ";Mass[#etap] (GeV); t_{#eta} (GeV^{2})", 500, 1, 3.5, 150, 0, 10);
	dHist_t_etaVsPi0EtaMass = new TH2D( "t_etaVsPi0EtaMass", ";Mass[#pi^{0}#eta] (GeV); t_{#eta} (GeV^{2})", 400, 0.2, 2.2, 150, 0, 10);
	dHist_t_etaVsVHAngle = new TH2D( "t_etaVsVHAngle", ";VanHove Angle (rad); t_{#eta} (GeV^{2})", 320, 0, 2*TMath::Pi(), 150, 0, 10);
	gDirectory->cd( ".." );
	gDirectory->mkdir( "T_proton" )->cd();
	dHist_t_pVsOmegaEtaMass = new TH2D( "t_pVsOmegaEtaMass", ";Mass[#omega#eta] (GeV); t_{p} (GeV^{2})", 250, 0.7, 3.7, 150, 0, 17);
	dHist_t_pVsEtaPMass = new TH2D( "t_pVsEtaPMass", ";Mass[#etap] (GeV); t_{p} (GeV^{2})", 500, 1, 3.5, 150, 0, 17);
	dHist_t_pVsPi0EtaMass = new TH2D( "t_pVsPi0EtaMass", ";Mass[#pi^{0}#eta] (GeV); t_{p} (GeV^{2})", 400, .2, 2.2, 150, 0, 17);	
	dHist_t_pVsVHAngle = new TH2D( "t_pVsVHAngle", ";VanHove Angle (rad); t_{p} (GeV^{2})", 320, 0, 2*TMath::Pi(), 150, 0, 17);
	gDirectory->cd( ".." );
	gDirectory->mkdir( "T_etaProton" )->cd();
	dHist_t_etaPVsOmegaEtaMass = new TH2D( "t_etaPVsOmegaEtaMass", ";Mass[#omega#eta] (GeV); t_{#etap} (GeV^{2})", 250, 0.7, 3.7, 150, 0, 17);
	dHist_t_etaPVsEtaPMass = new TH2D( "t_etaPVsEtaPMass", ";Mass[#etap] (GeV); t_{#etap} (GeV^{2})", 500, 1, 3.5, 150, 0, 17);
	dHist_t_etaPVsPi0EtaMass = new TH2D( "t_etaPVsPi0EtaMass", ";Mass[#pi^{0}#eta] (GeV); t_{#etap} (GeV^{2})", 400, .2, 2.2, 150, 0, 17);	
	dHist_t_etaPVsVHAngle = new TH2D( "t_etaPVsVHAngle", ";VanHove Angle (rad); t_{#etaP} (GeV^{2})", 320, 0, 2*TMath::Pi(), 150, 0, 17);
	gDirectory->cd( ".." );
	gDirectory->mkdir( "T_omegaProton" )->cd();	
	dHist_t_omegaPVsOmegaEtaMass = new TH2D( "t_omegaPVsOmegaEtaMass", ";Mass[#omega#eta] (GeV); t_{#omegap} (GeV^{2})", 250, 0.7, 3.7, 150, 0, 17);
	dHist_t_omegaPVsEtaPMass = new TH2D( "t_omegaPVsEtaPMass", ";Mass[#etap] (GeV); t_{#omegap} (GeV^{2})",  500, 1, 3.5, 150, 0, 17);
	dHist_t_omegaPVsPi0EtaMass = new TH2D( "t_omegaPVsPi0EtaMass", ";Mass[#pi^{0}#eta] (GeV); t_{#omegap} (GeV^{2})", 400, 0.2, 2.2, 150, 0, 17);
	dHist_t_omegaPVsVHAngle = new TH2D( "t_omegaPVsVHAngle", ";VanHove Angle (rad); t_{#omegap} (GeV^{2})", 320, 0, 2*TMath::Pi(), 150, 0, 17);
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "VanHove" )->cd();
	dHist_VanHove3 = new TH2D( "VanHove3", ";Van Hove X; Van Hove Y", 540, -2.7, 2.7, 540, -2.7, 2.7 );
	gDirectory->mkdir( "Test_MassDependet_Cut" )->cd();	
	dHist_MomentumIsobar = new TH2D( "MomentumIsobar", ";Z Momentum P (GeV);Z Momentum #eta (GeV)", 100, -2, 2, 100, -2, 2 );
	dHist_rhoIsobar = new TH1D("rhoIsobar", ";#rho Isobar (rad); Combos / .01 rad", 660, 0, 6.6); //need to recalculate it
	dHist_VanHoveAngleVsM3pi = new TH2D( "VanHoveAngleVsM3pi", ";M[3#pi] (GeV); VanHove Angle (rad)", 250, 0.3, 3.3, 320, 0, 2*TMath::Pi() );
	dHist_VanHoveAngleVsMeta = new TH2D( "VanHoveAngleVsMeta", ";M[#eta] (GeV); VanHove Angle (rad)", 400, 0.35, .75, 320, 0, 2*TMath::Pi() );
	dHist_VanHoveAngleVsMomegaEta = new TH2D( "VanHoveAngleVsMomegaEta", ";M[#omega#eta] (GeV); VanHove Angle (rad)",  250, 0.7, 3.7, 320, 0, 2*TMath::Pi() );
	dHist_VanHoveAngleVsMprotonEta = new TH2D( "VanHoveAngleVsMprotonEta", ";M[#etap] (GeV); VanHove Angle (rad)",  500, 1, 3.5, 320, 0, 2*TMath::Pi() );
	dHist_VanHoveAngleVsCosCMEta = new TH2D( "VanHoveAngleVsCosCMEta", ";cos(#theta)_{#eta}; VanHove Angle (rad)",  100, -1, 1, 320, 0, 2*TMath::Pi() );
	gDirectory->cd( "..");
	gDirectory->cd( "..");


	gDirectory->mkdir( "LAB" )->cd();
	gDirectory->mkdir( "LAB_momenta" )->cd();
	dHist_3piMomentum = new TH1D("3piMomentum",";3#pi Momentum (GeV)", 100, 0, 10);
	dHist_etaMomentum = new TH1D("etaMomentum",";#eta Momentum (GeV)", 100, 0, 10);
	dHist_protonMomentum = new TH1D("protonMomentum",";p Momentum (GeV)", 100, 0, 10);
	dHist_etaProtonMomentum = new TH1D("etaProtonMomentum",";#eta p Momentum (GeV)", 100, 0, 10);
	dHist_deltaMomentum_omegaEta = new TH1D( "deltaMomentum_omegaEta", ";p_{#omega} - p_{#eta}", 100, 10, 10 );
	dHist_omegaVsEtaMomentum = new TH2D("omegaVsEtaMomentum",";p_{eta}; p_{#omega}", 100, 0, 10, 100, 0 ,10 );
	gDirectory->cd( "..");

	gDirectory->mkdir( "LAB_phi" )->cd();
	dHist_3piLABphi =  new TH1D( "3piLABphi", ";#phi_{LAB} 3#pi (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_LABphiVs3pi = new TH2D("LABphiVs3pi", ";M[3#pi] (GeV); #phi_{LAB} 3#pi (rad)", 250, 0.7, 3.7, 160, -3.2, 3.2);
	dHist_pi0LABphi = new TH1D( "pi0LABphi", ";#phi_{LAB} #pi^{0} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_piPlusLABphi = new TH1D( "piPlusLABphi", ";#phi_{LAB} #pi^{+} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_piMinusLABphi = new TH1D( "piMinusLABphi", ";LAB #phi #pi^{-} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_etaLABphi = new TH1D( "etaLABphi", ";#phi_{LAB} #eta (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_protonLABphi = new TH1D( "protonLABphi", ";#phi_{LAB} proton (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "LAB_cos" )->cd();
	dHist_3piLABcos =  new TH1D( "3piLABcos", ";cos#theta_{LAB} 3#pi; Combos / .02", 100, -1 , 1 );
	dHist_LABcosVs3pi = new TH2D("LABcosVs3pi", ";M[3#pi] (GeV); cos#theta_{LAB} 3#pi", 250, 0.7, 3.7, 100, -1 , 1);

	dHist_pi0LABcos = new TH1D( "pi0LABcos", ";cos#theta_{LAB} #pi^{0}; Combos / .02", 100, -1 , 1 );
	dHist_piPlusLABcos = new TH1D( "piPlusLABcos", ";cos#theta_{LAB} #pi^{+}; Combos / .02", 100, -1 , 1 );
	dHist_piMinusLABcos = new TH1D( "piMinusLABcos", ";cos#theta_{LAB} #pi^{-}; Combos / .02", 100, -1 , 1 );
	dHist_etaLABcos = new TH1D( "etaLABcos", ";cos#theta_{LAB} #eta; Combos / .02", 100, -1 , 1 );
	dHist_protonLABcos = new TH1D( "protonLABcos", ";cos#theta_{LAB} proton; Combos / .02", 100, -1 , 1 );
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "CM" )->cd();
	dHist_alpha = new TH1D( "alpha", ";#alpha; Combos / .02", 150, -0.2, 3.2 );

	gDirectory->mkdir( "CM_momenta" )->cd();
	dHist_3piMomentum_CM = new TH1D("3piMomentum_CM",";3#pi Momentum (GeV)", 100, 0, 10);
	dHist_etaMomentum_CM = new TH1D("etaMomentum_CM",";#eta Momentum (GeV)", 100, 0, 10);
	dHist_protonMomentum_CM = new TH1D("protonMomentum_CM",";p Momentum (GeV)", 100, 0, 10);
	dHist_etaProtonMomentum_CM = new TH1D("etaProtonMomentum_CM",";#eta p Momentum (GeV)", 100, 0, 10);
	dHist_deltaMomentum_omegaEta_CM = new TH1D( "deltaMomentum_omegaEta_CM", ";p_{#omega} - p_{#eta}", 100, 10, 10 );
	dHist_omegaVsEtaMomentum_CM = new TH2D("omegaVsEtaMomentum_CM",";p_{eta}; p_{#omega}", 100, 0, 3, 100, 0 ,3 );

	gDirectory->cd( ".." );

	gDirectory->mkdir( "CM_phi" )->cd();
	dHist_3piCMphi =  new TH1D( "3piCMphi", ";#phi_{CM} 3#pi (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_pi0CMphi = new TH1D( "pi0CMphi", ";#phi_{CM} #pi^{0} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_piPlusCMphi = new TH1D( "piPlusCMphi", ";#phi_{CM} #pi^{+} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_piMinusCMphi = new TH1D( "piMinusCMphi", ";#phi_{CM} #pi^{-} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_etaCMphi = new TH1D( "etaCMphi", ";#phi_{CM} #eta (rad); Combos / .04 rad", 160, -3.2, 3.2 );

	dHist_CMphiVs3pi = new TH2D("CMphiVs3pi", ";M[3#pi] (GeV); #phi_{CM} 3#pi (rad)", 250, 0.7, 3.7, 160, -3.2, 3.2);
	dHist_etaPhiCMvsMassEtaP = new TH2D( "etaPhiCMvsMassEtaP", ";Mass[#etap]; #eta #phi_{CM} (rad)", 250, 1, 3.5, 160, -3.2, 3.2 );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "CM_cos" )->cd();
	dHist_3piCMcos =  new TH1D( "3piCMcos", ";cos#theta_{CM} 3#pi; Combos / .02", 100, -1 , 1 );
	dHist_pi0CMcos = new TH1D( "pi0CMcos", ";cos#theta_{CM} #pi^{0}; Combos / .02", 100, -1 , 1 );
	dHist_piPlusCMcos = new TH1D( "piPlusCMcos", ";cos#theta_{CM} #pi^{+}; Combos / .02", 100, -1 , 1 );
	dHist_piMinusCMcos = new TH1D( "piMinusCMcos", ";cos#theta_{CM} #pi^{-}; Combos / .02", 100, -1 , 1 );
	dHist_etaCMcos = new TH1D( "etaCMcos", ";cos#theta_{CM} #eta; Combos / .02", 100, -1 , 1 );

	dHist_CMcosVs3pi = new TH2D("CMcosVs3pi", ";M[3#pi] (GeV); cos#theta_{CM} 3#pi", 250, 0.7, 3.7, 100, -1 , 1);
	dHist_etaCosCMvsMassEtaP = new TH2D( "etaCosCMvsMassEtaP", ";Mass[#etap] (GeV); #eta cos#theta_{CM}",  250, 1, 3.5, 100, -1, 1 );
	dHist_3piCosCMvsProtonEtaMass = new TH2D( "3piCosCMvsProtonEtaMass", ";Mass[#etap] (GeV); #omega cos#theta_{CM}",  250, 1, 3.5, 100, -1, 1 );
	dHist_etaCosCMvsOmegaEtaMass = new TH2D( "etaCosCMvsOmegaEtaMass", ";Mass[#omega#eta] (GeV); #eta cos#theta_{CM}",  250, .7, 3.7, 100, -1, 1 );
	gDirectory->cd( ".." );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "GJ_angles" )->cd();
	gDirectory->mkdir( "GJ_phi" )->cd();
	dHist_3piGJphi =  new TH1D( "3piGJphi", ";#phi_{GJ} 3#pi (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_GJphiVs3pi = new TH2D("GJphiVs3pi", ";M[3#pi] (GeV); #phi_{GJ} 3#pi (rad)", 250, 0.7, 3.7, 160, -3.2, 3.2);
	dHist_pi0GJphi = new TH1D( "pi0GJphi", ";#phi_{GJ} #pi^{0} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_piPlusGJphi = new TH1D( "piPlusGJphi", ";#phi_{GJ} #pi^{+} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_piMinusGJphi = new TH1D( "piMinusGJphi", ";#phi_{GJ} #pi^{-} (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_etaGJphi = new TH1D( "etaGJphi", ";#phi_{GJ} #eta (rad); Combos / .04 rad", 160, -3.2, 3.2 );

	dHist_3piPhivsMass = new TH2D( "3piPhivsMass", ";Mass[#omega#eta] (GeV); #omega #phi_{GJ} (rad)", 250, 0.7, 3.7, 160, -3.2, 3.2 );
	dHist_etaPhivsMass = new TH2D( "etaPhivsMass", ";Mass[#omega#eta]; #eta #phi_{GJ} (rad)", 250, 0.7, 3.7, 160, -3.2, 3.2 );

	dHist_3piPhivsVHAngle = new TH2D( "3piPhivsVHAngle", ";VanHove Angle (rad); #omega #phi_{GJ}", 320, 0, 2*TMath::Pi(), 160, -3.2, 3.2);
       	gDirectory->cd( ".." );

	gDirectory->mkdir( "GJ_cos" )->cd();
	dHist_3piGJcos =  new TH1D( "3piGJcos", ";cos#theta_{GJ} 3#pi; Combos / .02", 100, -1 , 1 );
	dHist_GJcosVs3pi = new TH2D("GJcosVs3pi", ";M[3#pi] (GeV); cos#theta_{GJ} 3#pi", 250, 0.7, 3.7, 100, -1 , 1);
	dHist_pi0GJcos = new TH1D( "pi0GJcos", ";cos#theta_{GJ} #pi^{0}; Combos / .02", 100, -1 , 1 );
	dHist_piPlusGJcos = new TH1D( "piPlusGJcos", ";cos#theta_{GJ} #pi^{+}; Combos / .02", 100, -1 , 1 );
	dHist_piMinusGJcos = new TH1D( "piMinusGJcos", ";cos#theta_{GJ} #pi^{-}; Combos / .02", 100, -1 , 1 );
	dHist_etaGJcos = new TH1D( "etaGJcos", ";cos#theta_{GJ} #eta; Combos / .02", 100, -1 , 1 );

	dHist_3piCosvsMass = new TH2D( "3piCosvsMass", ";Mass[#omega#eta] (GeV); #omega cos#theta_{GJ}",  250, 0.7, 3.7, 100, -1, 1 );
	dHist_etaCosvsMass = new TH2D( "etaCosvsMass", ";Mass[#omega#eta] (GeV); #eta cos#theta_{GJ}",  250, 0.7, 3.7, 100, -1, 1 );
	dHist_3piCosvsProtonEtaMass = new TH2D( "3piCosvsProtonEtaMass", ";Mass[#etap] (GeV); #omega cos#theta_{GJ}",  250, 1, 3.5, 100, -1, 1 );
	dHist_3piCosvsVHAngle = new TH2D( "3piCosvsVHAngle", ";VanHove Angle (rad); #omega cos#theta_{GJ}", 320, 0, 2*TMath::Pi(), 100, -1, 1 );
       	gDirectory->cd( ".." );
       	gDirectory->cd( ".." );

	gDirectory->mkdir( "He_X_angles" )->cd();
	dHist_he1cos =  new TH1D( "he1cos", ";cos#theta_{He1} #omega; Combos / .02", 100, -1 , 1 );
	dHist_he1cosNarrow = new TH1D("he1cosNarrow", ";cos#theta_{He1} #omega; Combos / .02", 100, -1 , 1);
	dHist_he1phi =  new TH1D( "he1phi", ";#phi_{He1} #omega (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_he1phiNarrow = new TH1D( "he1phiNarrow", ";#phi_{He1} #omega (rad); Combos / .04 rad", 160, -3.2, 3.2 );
       	gDirectory->cd( ".." );

	gDirectory->mkdir( "He_normal_angles" )->cd();
	dHist_he2cos =  new TH1D( "he2cos", ";cos#theta_{He1} Normal; Combos / .02", 100, -1 , 1 );
	dHist_he2cosNarrow = new TH1D("he2cosNarrow", ";cos#theta_{He1} Normal; Combos / .02", 100, -1 , 1);
	dHist_he2phi =  new TH1D( "he2phi", ";#phi_{He1} Normal (rad); Combos / .04 rad", 160, -3.2, 3.2 );
	dHist_he2phiNarrow = new TH1D( "he2phiNarrow", ";#phi_{He1} Normal (rad); Combos / .04 rad", 160, -3.2, 3.2 );
       	gDirectory->cd( ".." );


	dHist_lambdaOmega  = new TH1D( "lambdaOmega", ";#lambda_{#omega}; Combinations / 0.01", 115, 0, 1.15 );
	dHist_lambdaLowSideband  = new TH1D( "lambdaLowSideband", ";#lambda_{lowSideband}; Combinations / 0.01", 115, 0, 1.15 );
	dHist_lambdaHighSideband  = new TH1D( "lambdaHighSideband", ";#lambda_{highSideband}; Combinations / 0.01", 115, 0, 1.15 );
	dHist_dalitz3Pi = new TH2D( "dalitz3Pi", ";Mass[#pi^{+}#pi^{0}]^{2} (GeV^{2}); Mass[#pi^{-}#pi^{0}]^{2} (GeV^{2})", 230, .2 , 2.5, 230, .2 , 2.5 );
	dHist_dalitz2PiEta = new TH2D( "dalitz2PiEta", ";Mass[#pi^{+}#eta]^{2} (GeV^{2}); Mass[#pi^{-}#eta]^{2} (GeV^{2})", 230, .5 , 2.5, 230, .5 , 2.5 );
	dHist_omegavsEta = new TH2D( "omegavsEta", ";Momentum #eta (GeV);Momentum 3#pi (GeV)", 100, 0, 8, 100, 0, 8 );
	gDirectory->cd( ".." );

	gDirectory->mkdir( "CL" )->cd();
	//Confidence Level 
	dHist_logCL = new TH1D( "logCL", ";log CL; Combos/ 2 a.u.", 90, -45, 0);
	dHist_CLsimple = new TH1D( "CLsimple", "; CL; Combos / .01", 100, 0, 1);
	dHist_ChiSq = new TH1D( "ChiSq", ";#Chi^{2}; Combos / 2  a.u.", 500, 0, 1000 );

       	int locNumBins = 0;
	double* locConLevLogBinning = dAnalysisUtilities.Generate_LogBinning(-50, 0, 5, locNumBins); // Make sure that you have added the header file for dAnalysisUtilities
	double* locConLevLogBinning2 = dAnalysisUtilities.Generate_LogBinning(-50, 0, 5, locNumBins); // Make sure that you have added the header file for dAnalysisUtilities
	if(locConLevLogBinning != NULL){
	  dHist_ConfidenceLevel_logX = new TH1D( "CL", ";Confidence Level", locNumBins, locConLevLogBinning );
	  dHist_VertexVsConfidenceLevel_logX = new TH2D( "VertexVsCL_logX", ";Confidence Level; Proton Z Vertex(cm) ", locNumBins, locConLevLogBinning, 1000, 45, 95 );
	  dHist_MMSVsConfidenceLevel_logX = new TH2D( "MMSVsCL_logX", ";Confidence Level; MMS (GeV^{2})", locNumBins, locConLevLogBinning, 1000, -.1, .1 );
	  dHist_MEVsConfidenceLevel_logX = new TH2D( "MEVsCL_logX", "Confidence Level; ME (GeV)", locNumBins, locConLevLogBinning, 600, -3, 3 );
	  dHist_Mass3PiVsConfidenceLevel_logX = new TH2D( "Mass3piVsCL_logX", ";Confidence Level; Mass[3#pi] (GeV)", locNumBins, locConLevLogBinning, 100, 0.3, 3.3 );
	  dHist_Mass2PiEtaVsConfidenceLevel_logX = new TH2D( "Mass2piEtaVsCL_logX", ";Confidence Level; Mass[2#pi#eta] (GeV)", locNumBins, locConLevLogBinning, 100, 0.3, 3.3 );
	
	  dHist_ChiSqVsConfidenceLevel_logX = new TH2D( "ChiSqVsCL_logX", ";Confidence Level; #Chi^{2}", locNumBins, locConLevLogBinning, 500, 0, 1000 );
	}
	else{
	  dHist_ConfidenceLevel_logX = NULL;
	  dHist_VertexVsConfidenceLevel_logX = NULL;
	  dHist_MMSVsConfidenceLevel_logX = NULL;
	  dHist_MEVsConfidenceLevel_logX = NULL;
	  dHist_Mass3PiVsConfidenceLevel_logX = NULL;
	  dHist_Mass2PiEtaVsConfidenceLevel_logX = NULL;
	  dHist_ChiSqVsConfidenceLevel_logX = NULL;
	}
	gDirectory->cd( "..");

	gDirectory->mkdir( "Pol_angle" )->cd();
	dHist_PolarizationAngle = new TH1D("PolarizationAngle","", 100, -50 , 150);
	gDirectory->cd( "..");

	gDirectory->mkdir( "Number_of_Particles" )->cd();
	//Number of Particles
	dHist_PhotonNumber = new TH1D( "PhotonNumber", ";Number of Photons Candidates in an Event", 14, 3, 17); 
	dHist_NeutralHypoNumber = new TH1D( "NeutralNumber", ";Number of Neutral Candidates in an Event", 14, 3, 17); 
	dHist_UnusedShowerNumber = new TH1D( "UnusedShowerNumber", ";Number of Unused Showers in an Event", 14, 1, 15);
	dHist_ProtonNumber = new TH1D( "ProtonNumber", ";Number of Protons Candidates in an Event", 14, 1, 15);
	dHist_PipNumber = new TH1D( "PipNumber", ";Number of #pi^{+} Candidates in an Event", 14, 1, 15);
	dHist_PimNumber = new TH1D( "PimNumber", ";Number of #pi^{-} Candidates in an Event", 14, 1, 15);
	dHist_BeamNumber = new TH1D( "BeamNumber", ";Number of Beam Candidates in an Event", 14, 1, 15);
	dHist_ComboNumber = new TH1D( "ComboNumber", ";Number of Combos in an Event", 14, 1, 15);
	gDirectory->cd( ".." );	


	/************************** EXAMPLE USER INITIALIZATION: CUSTOM OUTPUT BRANCHES - MAIN TREE *************************/


	/************************** EXAMPLE USER INITIALIZATION: CUSTOM OUTPUT BRANCHES - FLAT TREE *************************/


	/************************************* ADVANCED EXAMPLE: CHOOSE BRANCHES TO READ ************************************/


	/************************************** DETERMINE IF ANALYZING SIMULATED DATA *************************************/

	dIsMC = (dTreeInterface->Get_Branch("MCWeight") != NULL);

}

Bool_t DSelector_omegaEta::Process(Long64_t locEntry)
{
	// The Process() function is called for each entry in the tree. The entry argument
	// specifies which entry in the currently loaded tree is to be processed.
	//
	// This function should contain the "body" of the analysis. It can contain
	// simple or elaborate selection criteria, run algorithms on the data
	// of the event and typically fill histograms.
	//
	// The processing can be stopped by calling Abort().
	// Use fStatus to set the return value of TTree::Process().
	// The return value is currently not used.

	//CALL THIS FIRST
	DSelector::Process(locEntry); //Gets the data from the tree for the entry
	//cout << "RUN " << Get_RunNumber() << ", EVENT " << Get_EventNumber() << endl;
	//TLorentzVector locProductionX4 = Get_X4_Production();

	/******************************************** GET POLARIZATION ORIENTATION ******************************************/

	//Only if the run number changes
	//RCDB environment must be setup in order for this to work! (Will return false otherwise)
	UInt_t locRunNumber = Get_RunNumber();
	int locPolarizationAngle = 0;
	// if(locRunNumber != dPreviousRunNumber)
	// {
	// 	dIsPolarizedFlag = dAnalysisUtilities.Get_IsPolarizedBeam(locRunNumber, dIsPARAFlag);
	// 	dPreviousRunNumber = locRunNumber;
	// }

	/********************************************* SETUP UNIQUENESS TRACKING ********************************************/

	//ANALYSIS ACTIONS: Reset uniqueness tracking for each action
	//For any actions that you are executing manually, be sure to call Reset_NewEvent() on them here
	Reset_Actions_NewEvent();
	//dAnalyzeCutActions->Reset_NewEvent(); // manual action, must call Reset_NewEvent()

	//PREVENT-DOUBLE COUNTING WHEN HISTOGRAMMING
		//Sometimes, some content is the exact same between one combo and the next
			//e.g. maybe two combos have different beam particles, but the same data for the final-state
		//When histogramming, you don't want to double-count when this happens: artificially inflates your signal (or background)
		//So, for each quantity you histogram, keep track of what particles you used (for a given combo)
		//Then for each combo, just compare to what you used before, and make sure it's unique

	//EXAMPLE 1: Particle-specific info:
		//INSERT USER ANALYSIS UNIQUENESS TRACKING HERE
	set<Int_t> locUsedSoFar_Beam; //Int_t: Unique ID for beam particles. set: easy to use, fast to search
	set<Int_t> locUsedSoFar_Proton;
	set<Int_t> locUsedSoFar_PiPlus;
	set<Int_t> locUsedSoFar_PiMinus;
	set<Int_t> locUsedSoFar_Photon1;
	set<Int_t> locUsedSoFar_Photon2;
	set<Int_t> locUsedSoFar_Photon3;
	set<Int_t> locUsedSoFar_Photon4;

	//xCounting 
	set<Int_t> NumberOfPhotons;
	//set<Int_t> NumberOfUnusedShowers;not proper
	set<Int_t> NumberOfProtons;
	set<Int_t> NumberOfPiPlus;
	set<Int_t> NumberOfPiMinus;
	set<Int_t> NumberOfBeam;
	//set<Int_t> NumberOfCombos;// not proper

	//Cut on combos
	int comboNumber = 0; // adding count after cuts
	double combo_cl_max = 0;
	double combo_MMS_ME_min = 100;
	double combo_mass_eta = 100;
	double combo_mass_pi0 = 100;
	double combo_mass_pi0_eta = 100;
	int comboBeamNumber = 0;
	int beamIDNumber = -1;
	int cutOtherBeams = 0;
	//EXAMPLE 2: Combo-specific info:
	//In general: Could have multiple particles with the same PID: Use a set of Int_t's
	//In general: Multiple PIDs, so multiple sets: Contain within a map
	//Multiple combos: Contain maps within a set (easier, faster to search)

	//Photon Combos
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_Photons_1_2;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_Photons_1_3;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_Photons_1_4;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_Photons_2_3;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_Photons_2_4;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_Photons_3_4;

 	//3 Photons
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_3Photons1;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_3Photons2;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_3Photons3;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_3Photons4;

 	//4 Photons
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_4Photons;

	//3 Particle Combos
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_3piMass;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_2piEtaMass;

	//Baryons
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPipP;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPimP;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPi0P;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassEtaP;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_Mass3PiP;

	//Mesons
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPipPim;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPipPi0;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPipEta;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPimPi0;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPimEta;
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MassPi0Eta;

	//3PiEta
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_3piEtaMass;

	//All(no Beam)
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_5Particles;

	//All
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_AllParticles;


	/**************************************** EXAMPLE: FILL CUSTOM OUTPUT BRANCHES **************************************/

	/************************************************* LOOP OVER COMBOS *************************************************/
	//Loop hist
	for(UInt_t loc_i = 0; loc_i < Get_NumCombos(); ++loc_i)
	{

	        //Set branch array indices for combo and all combo particles
                dComboWrapper->Set_ComboIndex(loc_i);

		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut()) // Is false when tree originally created
			continue; // Combo has been cut previously

		/********************************************** GET PARTICLE INDICES *********************************************/

		//Used for tracking uniqueness when filling histograms, and for determining unused particles

		//Step 0
		Int_t locBeamID = dComboBeamWrapper->Get_BeamID();
		Int_t locPiPlusTrackID = dPiPlusWrapper->Get_TrackID();
		Int_t locPiMinusTrackID = dPiMinusWrapper->Get_TrackID();
		Int_t locProtonTrackID = dProtonWrapper->Get_TrackID();

		//Step 1
		Int_t locPhoton1NeutralID = dPhoton1Wrapper->Get_NeutralID();
		Int_t locPhoton2NeutralID = dPhoton2Wrapper->Get_NeutralID();

		//Step 2
		Int_t locPhoton3NeutralID = dPhoton3Wrapper->Get_NeutralID();
		Int_t locPhoton4NeutralID = dPhoton4Wrapper->Get_NeutralID();

		/*********************************************** GET FOUR-MOMENTUM **********************************************/

		// Get P4's: //is kinfit if kinfit performed, else is measured
		//dTargetP4 is target p4
		//Step 0
		TLorentzVector locBeamP4 = dComboBeamWrapper->Get_P4();
		TLorentzVector locPiPlusP4 = dPiPlusWrapper->Get_P4();
		TLorentzVector locPiMinusP4 = dPiMinusWrapper->Get_P4();
		TLorentzVector locProtonP4 = dProtonWrapper->Get_P4();
		//Step 1
		TLorentzVector locPhoton1P4 = dPhoton1Wrapper->Get_P4();
		TLorentzVector locPhoton2P4 = dPhoton2Wrapper->Get_P4();
		//Step 2
		TLorentzVector locPhoton3P4 = dPhoton3Wrapper->Get_P4();
		TLorentzVector locPhoton4P4 = dPhoton4Wrapper->Get_P4();

		// Get Measured P4's:
		//Step 0
		TLorentzVector locBeamP4_Measured = dComboBeamWrapper->Get_P4_Measured();
		TLorentzVector locPiPlusP4_Measured = dPiPlusWrapper->Get_P4_Measured();
		TLorentzVector locPiMinusP4_Measured = dPiMinusWrapper->Get_P4_Measured();
		TLorentzVector locProtonP4_Measured = dProtonWrapper->Get_P4_Measured();
		//Step 1
		TLorentzVector locPhoton1P4_Measured = dPhoton1Wrapper->Get_P4_Measured();
		TLorentzVector locPhoton2P4_Measured = dPhoton2Wrapper->Get_P4_Measured();
		//Step 2
		TLorentzVector locPhoton3P4_Measured = dPhoton3Wrapper->Get_P4_Measured();
		TLorentzVector locPhoton4P4_Measured = dPhoton4Wrapper->Get_P4_Measured();

		/*********************************************** GET FOUR-VECTOR ************************************************/

		//Step 0
		TLorentzVector locBeamX4 = dComboBeamWrapper->Get_X4();
		TLorentzVector locPiPlusX4 = dPiPlusWrapper->Get_X4();
		TLorentzVector locPiMinusX4 = dPiMinusWrapper->Get_X4();
		TLorentzVector locProtonX4 = dProtonWrapper->Get_X4();
		//Step 1
		TLorentzVector locPhoton1X4 = dPhoton1Wrapper->Get_X4();
		TLorentzVector locPhoton2X4 = dPhoton2Wrapper->Get_X4();
		//Step 1
		TLorentzVector locPhoton3X4 = dPhoton3Wrapper->Get_X4();
		TLorentzVector locPhoton4X4 = dPhoton4Wrapper->Get_X4();

		// Get Measured X4's:
		//Step 0
		TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
		TLorentzVector locPiPlusX4_Measured = dPiPlusWrapper->Get_X4_Measured();
		TLorentzVector locPiMinusX4_Measured = dPiMinusWrapper->Get_X4_Measured();
		TLorentzVector locProtonX4_Measured = dProtonWrapper->Get_X4_Measured();

		//Step 1
		TLorentzVector locPhoton1X4_Measured = dPhoton1Wrapper->Get_X4_Measured();
		TLorentzVector locPhoton2X4_Measured = dPhoton2Wrapper->Get_X4_Measured();

		//Step 2
		TLorentzVector locPhoton3X4_Measured = dPhoton3Wrapper->Get_X4_Measured();
		TLorentzVector locPhoton4X4_Measured = dPhoton4Wrapper->Get_X4_Measured();

	        
		/********************************************* COMBINE FOUR-MOMENTUM ********************************************/

		// DO YOUR STUFF HERE

		// Combine 4-vectors
		TLorentzVector locMissingP4_Measured = locBeamP4_Measured + dTargetP4;
		locMissingP4_Measured -= locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locMissingP4 = locBeamP4 + dTargetP4;
		locMissingP4 -= locPiPlusP4 + locPiMinusP4 + locProtonP4 + locPhoton1P4 + locPhoton2P4 + locPhoton3P4 + locPhoton4P4;

		//Photons Combos
		TLorentzVector locPhotons_1_2_Measured = locPhoton1P4_Measured + locPhoton2P4_Measured;
		TLorentzVector locPhotons_1_3_Measured = locPhoton1P4_Measured + locPhoton3P4_Measured;
		TLorentzVector locPhotons_1_4_Measured = locPhoton1P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhotons_2_3_Measured = locPhoton2P4_Measured + locPhoton3P4_Measured;
		TLorentzVector locPhotons_2_4_Measured = locPhoton2P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhotons_3_4_Measured = locPhoton3P4_Measured + locPhoton4P4_Measured;

		TLorentzVector locPhotons_1_2 = locPhoton1P4 + locPhoton2P4;//Pi0 hypothesis
		TLorentzVector locPhotons_1_3 = locPhoton1P4 + locPhoton3P4;
		TLorentzVector locPhotons_1_4 = locPhoton1P4 + locPhoton4P4;
		TLorentzVector locPhotons_2_3 = locPhoton2P4 + locPhoton3P4;
		TLorentzVector locPhotons_2_4 = locPhoton2P4 + locPhoton4P4;
		TLorentzVector locPhotons_3_4 = locPhoton3P4 + locPhoton4P4;//eta hypothesis

		//3 Photons
		TLorentzVector locPhotons_1_2_3 = locPhoton1P4 + locPhoton2P4 + locPhoton3P4;
		TLorentzVector locPhotons_1_2_4 = locPhoton1P4 + locPhoton2P4 + locPhoton4P4;
		TLorentzVector locPhotons_1_3_4 = locPhoton1P4 + locPhoton3P4 + locPhoton4P4;
		TLorentzVector locPhotons_2_3_4 = locPhoton2P4 + locPhoton3P4 + locPhoton4P4;

		//4Photons
		TLorentzVector locPhotons_1_2_3_4 = locPhoton1P4 + locPhoton2P4 + locPhoton3P4 + locPhoton4P4;

		//3Pi combos
		TLorentzVector loc3Pi_Measured = locPiPlusP4_Measured + locPiMinusP4_Measured + locPhotons_1_2_Measured;
		TLorentzVector loc2Pi_Eta_Measured = locPiPlusP4_Measured + locPiMinusP4_Measured + locPhotons_3_4_Measured;

		TLorentzVector loc3Pi = locPiPlusP4 + locPiMinusP4 + locPhotons_1_2;
		TLorentzVector loc2Pi_Eta = locPiPlusP4 + locPiMinusP4 + locPhotons_3_4;

		//Baryons
		TLorentzVector locPipP = locPiPlusP4 + locProtonP4;
		TLorentzVector locPimP = locPiMinusP4 + locProtonP4;
		TLorentzVector locPi0P = locPhotons_1_2 + locProtonP4;
		TLorentzVector locEtaP = locPhotons_3_4 + locProtonP4;
		TLorentzVector locOmegaP = loc3Pi + locProtonP4;

		TLorentzVector locPipP_Measured = locPiPlusP4_Measured + locProtonP4_Measured;
		TLorentzVector locPimP_Measured = locPiMinusP4_Measured + locProtonP4_Measured;
		TLorentzVector locPi0P_Measured = locPhotons_1_2_Measured + locProtonP4_Measured;
		TLorentzVector locEtaP_Measured = locPhotons_3_4_Measured + locProtonP4_Measured;
		TLorentzVector locOmegaP_Measured = loc3Pi_Measured + locProtonP4_Measured;

		//Meson 
		TLorentzVector locPipPim = locPiPlusP4 + locPiMinusP4;
		TLorentzVector locPipPi0 = locPiPlusP4 + locPhotons_1_2;
		TLorentzVector locPipEta = locPiPlusP4 + locPhotons_3_4;
		TLorentzVector locPimPi0 = locPiMinusP4 + locPhotons_1_2;
		TLorentzVector locPimEta = locPiMinusP4 + locPhotons_3_4;
		TLorentzVector locPi0Eta = locPhotons_1_2 + locPhotons_3_4;

		//4 Particle
		TLorentzVector loc3piEta_Measured = locPiPlusP4_Measured + locPiMinusP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector loc3piEta = locPiPlusP4 + locPiMinusP4 + locPhoton1P4 + locPhoton2P4 + locPhoton3P4 + locPhoton4P4;


		//////////////////////////////////////////

		TLorentzVector locPipPimM_Measured =  locBeamP4_Measured + dTargetP4;
		locPipPimM_Measured -=  locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;

		TLorentzVector locPhoton1M_Measured =  locBeamP4_Measured + dTargetP4;
	        locPhoton1M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured +  locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhoton2M_Measured =  locBeamP4_Measured + dTargetP4;
		locPhoton2M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhoton3M_Measured =  locBeamP4_Measured + dTargetP4;
	        locPhoton3M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhoton4M_Measured =  locBeamP4_Measured + dTargetP4;
	        locPhoton4M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured;

		TLorentzVector locg1g2M_Measured = locPhoton1M_Measured + locPhoton2P4_Measured;
		TLorentzVector locg1g3M_Measured = locPhoton1M_Measured + locPhoton3P4_Measured;
		TLorentzVector locg1g4M_Measured = locPhoton1M_Measured + locPhoton4P4_Measured;
		TLorentzVector locg2g3M_Measured = locPhoton2M_Measured + locPhoton3P4_Measured;
		TLorentzVector locg2g4M_Measured = locPhoton2M_Measured + locPhoton4P4_Measured;
		TLorentzVector locg3g4M_Measured = locPhoton3M_Measured + locPhoton4P4_Measured;

		TLorentzVector locg1g2g3M_Measured = locPhoton1M_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured;
		TLorentzVector locg1g2g4M_Measured = locPhoton1M_Measured + locPhoton2P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locg1g3g4M_Measured = locPhoton1M_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locg2g3g4M_Measured = locPhoton2M_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;

		///////////////////////////////////////////////////////////////////////////////////////

		//Calculating Delta T (using Measured data)
		double locRFTime = dComboWrapper->Get_RFTime();
		//Beam
		double locPropagatedRFTimeBeam =  locRFTime + ( locBeamX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locBeamDeltaT = locBeamX4_Measured.T() - locPropagatedRFTimeBeam;
		//Proton
		double locPropagatedRFTimeProton =  locRFTime + ( locProtonX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locProtonDeltaT = locProtonX4_Measured.T() - locPropagatedRFTimeProton;		
		//PiP
		double locPropagatedRFTimePiPlus = locRFTime + ( locPiPlusX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPiPlusDeltaT = locPiPlusX4_Measured.T() - locPropagatedRFTimePiPlus;		
		//PiM
		double locPropagatedRFTimePiMinus = locRFTime + ( locPiMinusX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPiMinusDeltaT = locPiMinusX4_Measured.T() - locPropagatedRFTimePiMinus;
		//Photon1
		double locPropagatedRFTimePhoton1 = locRFTime + ( locPhoton1X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton1DeltaT = locPhoton1X4_Measured.T() - locPropagatedRFTimePhoton1;
		//Photon2
		double locPropagatedRFTimePhoton2 = locRFTime + ( locPhoton2X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton2DeltaT = locPhoton2X4_Measured.T() - locPropagatedRFTimePhoton2;
		//Photon3
		double locPropagatedRFTimePhoton3 = locRFTime + ( locPhoton3X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton3DeltaT = locPhoton3X4_Measured.T() - locPropagatedRFTimePhoton3;
		//Photon4
		double locPropagatedRFTimePhoton4 = locRFTime + ( locPhoton4X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton4DeltaT = locPhoton4X4_Measured.T() - locPropagatedRFTimePhoton4;

		///////////////////////////////////////////////////////////////////////////////////////

		//Calculating t min for omega eta system
		TLorentzVector locMomentumTransfer = locBeamP4  - loc3piEta;//[needs to be squared to be t [.M2()]
		TLorentzVector sMandelstam = locBeamP4 + dTargetP4; //This is not s until .M2() [it needs to be squared]
	   
		double E3CM = ( sMandelstam.M2() + loc3piEta.M2() - locProtonP4.M2() ) / (2*sMandelstam.M());// equation 47.36 pdg book
		double p3CM = sqrt( E3CM*E3CM - loc3piEta.M2()); // equation 47.37
		double p1CM = ( locBeamP4.Vect() ).Mag() * dTargetP4.M() / sMandelstam.M() ; // equation 47.37
		double t_1term =  ( locBeamP4.M2() - loc3piEta.M2() - dTargetP4.M2() + locProtonP4.M2() )/ (2*sMandelstam.M()); //  First term in equation 47.35
		double tmin = (t_1term)*(t_1term) - (p1CM - p3CM)*(p1CM - p3CM); // Eq 47.35
		double tprime = (locMomentumTransfer.M2() - tmin); 
		tprime = -1 * tprime;


		//Calculating t min for omega system
		TLorentzVector locMomentumTransfer_omega = locBeamP4  - loc3Pi;//[needs to be squared to be t [.M2()]
		TLorentzVector sMandelstam_omega = locBeamP4 + dTargetP4; //This is not s until .M2() [it needs to be squared]
	   
		double E3CM_omega = ( sMandelstam_omega.M2() + loc3Pi.M2() - locEtaP.M2() ) / (2*sMandelstam_omega.M());// equation 47.36 pdg book
		double p3CM_omega = sqrt( E3CM_omega*E3CM_omega - loc3Pi.M2()); // equation 47.37
		double p1CM_omega = ( locBeamP4.Vect() ).Mag() * dTargetP4.M() / sMandelstam_omega.M() ; // equation 47.37
		double t_1term_omega =  ( locBeamP4.M2() - loc3Pi.M2() - dTargetP4.M2() + locEtaP.M2() )/ (2*sMandelstam_omega.M()); //  First term in equation 47.35
		double tmin_omega = (t_1term_omega)*(t_1term_omega) - (p1CM_omega - p3CM_omega)*(p1CM_omega - p3CM_omega); // Eq 47.35
		double tprime_omega = (locMomentumTransfer_omega.M2() - tmin_omega); 
		tprime_omega = -1 * tprime_omega;


		/////t's
		double t_eta = -1*(locBeamP4 - locPhotons_3_4).M2();
		double t_etaP = -1*(locBeamP4 - locEtaP).M2();
		double t_omegaEta = -1*(locBeamP4 - loc3piEta).M2();
		double t_omega = -1*(locBeamP4 - loc3Pi).M2();
		double t_omegaP = -1*(locBeamP4 - locOmegaP).M2();
		double t_proton = -1*(locBeamP4 - locProtonP4).M2();


		///////////////////////////////////////////////////////////////////////////////////////

		// Calculate LAB angles
		double threePiCosLAB = (loc3Pi.Vect()).CosTheta();
		double threePiPhiLAB = (loc3Pi.Vect()).Phi();

		double etaCosLAB = (locPhotons_3_4.Vect()).CosTheta();
		double etaPhiLAB = (locPhotons_3_4.Vect()).Phi();

		double piPlusCosLAB = (locPiPlusP4.Vect()).CosTheta();
		double piPlusPhiLAB = (locPiPlusP4.Vect()).Phi();

		double piMinusCosLAB = (locPiMinusP4.Vect()).CosTheta();
		double piMinusPhiLAB = (locPiMinusP4.Vect()).Phi();

		double pi0CosLAB = (locPhotons_1_2.Vect()).CosTheta();
		double pi0PhiLAB = (locPhotons_1_2.Vect()).Phi();

		double protonCosLAB = (locProtonP4.Vect()).CosTheta();
		double protonPhiLAB = (locProtonP4.Vect()).Phi();

		// Boost  FROM: LAB  ---> TO: CM Frame
		TLorentzVector centerOfMass = locBeamP4 + dTargetP4;
		TLorentzRotation centerofMassBoost( -centerOfMass.BoostVector() );

		TLorentzVector beamCM = centerofMassBoost * locBeamP4;
		TLorentzVector targetCM = centerofMassBoost * dTargetP4;
		TLorentzVector piPlusCM = centerofMassBoost * locPiPlusP4;
		TLorentzVector piMinusCM = centerofMassBoost * locPiMinusP4;
		TLorentzVector protonCM = centerofMassBoost * locProtonP4;
		TLorentzVector photon1CM = centerofMassBoost * locPhoton1P4;
		TLorentzVector photon2CM = centerofMassBoost * locPhoton2P4;
		TLorentzVector photon3CM = centerofMassBoost * locPhoton3P4;
		TLorentzVector photon4CM = centerofMassBoost * locPhoton4P4;
		TLorentzVector particleXCM = centerofMassBoost * loc3piEta;

		TLorentzVector etaProtonCM = ( photon3CM + photon4CM ) + protonCM;

		TVector3 threePiCMV3 = ( piMinusCM + piPlusCM + photon1CM + photon2CM).Vect();

		TVector3 etaCMV3 = ( photon3CM+ photon4CM ).Vect();
		TVector3 piPlusCMV3 = piPlusCM.Vect();
		TVector3 piMinusCMV3 = piMinusCM.Vect();
		TVector3 pi0CMV3 = photon1CM.Vect() + photon2CM.Vect();

		TVector3 omegaEtaCM =  particleXCM.Vect();

		TVector3 z_cm = beamCM.Vect().Unit();
		TVector3 y_cm = (beamCM.Vect().Cross( -protonCM.Vect() ) ).Unit();
		TVector3 x_cm = (y_cm).Cross(z_cm).Unit();

	    
		// Calculate CM angles

		double threePiCMMag = threePiCMV3.Mag();
		double threePiCosCM = threePiCMV3.Dot(z_cm) / threePiCMMag ;
		double threePiPhiCM = TMath::ATan2( threePiCMV3.Dot(y_cm), threePiCMV3.Dot(x_cm) );		

		double etaCMMag = etaCMV3.Mag();
		double etaCosCM = etaCMV3.Dot(z_cm) / etaCMMag ;
		double etaPhiCM = TMath::ATan2( etaCMV3.Dot(y_cm), etaCMV3.Dot(x_cm) );		

		double piPlusCMMag = piPlusCMV3.Mag();
		double piPlusCosCM = piPlusCMV3.Dot(z_cm) / piPlusCMMag ;
		double piPlusPhiCM = TMath::ATan2( piPlusCMV3.Dot(y_cm), piPlusCMV3.Dot(x_cm) );		

		double piMinusCMMag = piMinusCMV3.Mag();
		double piMinusCosCM = piMinusCMV3.Dot(z_cm) / piMinusCMMag ;
		double piMinusPhiCM = TMath::ATan2( piMinusCMV3.Dot(y_cm), piMinusCMV3.Dot(x_cm) );		

		double pi0CMMag = pi0CMV3.Mag();
		double pi0CosCM = pi0CMV3.Dot(z_cm) / pi0CMMag ;
		double pi0PhiCM = TMath::ATan2( pi0CMV3.Dot(y_cm), pi0CMV3.Dot(x_cm) );	


		double protonCosCM =  (protonCM.Vect()).Dot(z_cm) / (protonCM.Vect()).Mag() ;	

		////////////////////////////////////////////////////////////////////////////////////////////////////////////
		//VanHove
		TLorentzVector vH_piPlus = piPlusCM;
		TLorentzVector vH_piMinus = piMinusCM;
		TLorentzVector vH_photon1 = photon1CM;
		TLorentzVector vH_photon2 = photon2CM;
		TLorentzVector vH_photon3 = photon3CM;
		TLorentzVector vH_photon4 = photon4CM;
		TLorentzVector vH_proton = protonCM;

		TLorentzVector vH_omega = vH_piPlus + vH_piMinus + vH_photon1 + vH_photon2;
		TLorentzVector vH_eta =  vH_photon3 + vH_photon4;

		double locParticle1_VH = vH_omega.Pz();
		double locParticle2_VH = vH_eta.Pz();
		double locParticle3_VH = vH_proton.Pz();
		double locVanHoveQ = TMath::Sqrt( locParticle1_VH* locParticle1_VH + locParticle2_VH* locParticle2_VH + locParticle3_VH* locParticle3_VH );
		double locVanHovePhi = TMath::ATan2(  -1*TMath::Sqrt(3.)*locParticle1_VH, 2*locParticle2_VH+locParticle1_VH ) + TMath::Pi();// added pi to map [-pi,pi] on [0,2pi]
		double vHX = locVanHoveQ*TMath::Cos(locVanHovePhi);
		double vHY = locVanHoveQ*TMath::Sin(locVanHovePhi);


		////////////////////////////////////////////////////////////////////////////////////////////////////////////
       		// Boost!    FROM: CM Frame  ---> TO: etaP Rest Frame (EP)
		TLorentzRotation restFrameEPBoost( -etaProtonCM.BoostVector() );
	
		TLorentzVector beamEP = restFrameEPBoost * beamCM;
		TLorentzVector targetEP = restFrameEPBoost * targetCM;
		TLorentzVector protonEP = restFrameEPBoost * protonCM;
		TLorentzVector piPlusEP = restFrameEPBoost * piPlusCM;
		TLorentzVector piMinusEP = restFrameEPBoost * piMinusCM;
		TLorentzVector photon1EP = restFrameEPBoost * photon1CM;
		TLorentzVector photon2EP = restFrameEPBoost * photon2CM;
		TLorentzVector photon3EP = restFrameEPBoost * photon3CM;
		TLorentzVector photon4EP = restFrameEPBoost * photon4CM;


		TLorentzVector etaEP = photon3EP + photon4EP; 
		TLorentzVector etaProtonEP = etaEP + protonEP;


		////////////////////////////////////////////////////////////////////////////////////////////////////////////

       		// Boost!  FROM: CM Frame ---> TO: X Rest Frame (GJ)
		TLorentzRotation restFrameXBoost( -particleXCM.BoostVector() );
	
		TLorentzVector beamGJ = restFrameXBoost * beamCM;
		TLorentzVector targetGJ = restFrameXBoost * targetCM;
		TLorentzVector protonGJ = restFrameXBoost * protonCM;
		TLorentzVector piPlusGJ = restFrameXBoost * piPlusCM;
		TLorentzVector piMinusGJ = restFrameXBoost * piMinusCM;
		TLorentzVector photon1GJ = restFrameXBoost * photon1CM;
		TLorentzVector photon2GJ = restFrameXBoost * photon2CM;
		TLorentzVector photon3GJ = restFrameXBoost * photon3CM;
		TLorentzVector photon4GJ = restFrameXBoost * photon4CM;
		TLorentzVector particleXGJ = restFrameXBoost * particleXCM;  

		//Particles
		TLorentzVector threePiGJ = piPlusGJ + piMinusGJ + photon1GJ + photon2GJ;
		TLorentzVector etaGJ = photon3GJ + photon4GJ; 
			
		//Particles
		TVector3 threePiGJ3V = threePiGJ.Vect();
	
		TVector3 piPlusGJ3V = piPlusGJ.Vect();
		TVector3 piMinusGJ3V = piMinusGJ.Vect();
		TVector3 pi0GJ3V = (photon1GJ + photon2GJ).Vect();
		TVector3 etaGJ3V = (photon3GJ + photon4GJ).Vect();		

		TVector3 particleXGJV3 = particleXGJ.Vect();
		
		
		// Calculate x, y and z GJ
		TVector3 z_gj = (beamGJ.Vect()).Unit();
		TVector3 y_gj = ((beamCM.Vect()).Cross( -protonCM.Vect() )).Unit();//((beamCM.Vect()).Cross( omegaEtaCM )).Unit();
		TVector3 x_gj = (( y_gj ).Cross( z_gj )).Unit();

		// Calculate GJ angles
		double threePiGJMag = threePiGJ3V.Mag();
		double threePiCosGJ = threePiGJ3V.Dot(z_gj) / threePiGJMag ;
		double threePiPhiGJ = TMath::ATan2( threePiGJ3V.Dot(y_gj), threePiGJ3V.Dot(x_gj) );		

		double etaGJMag = etaGJ3V.Mag();
		double etaCosGJ = etaGJ3V.Dot(z_gj) / etaGJMag ;
		double etaPhiGJ = TMath::ATan2( etaGJ3V.Dot(y_gj), etaGJ3V.Dot(x_gj) );		

		double piPlusGJMag = piPlusGJ3V.Mag();
		double piPlusCosGJ = piPlusGJ3V.Dot(z_gj) / piPlusGJMag ;
		double piPlusPhiGJ = TMath::ATan2( piPlusGJ3V.Dot(y_gj), piPlusGJ3V.Dot(x_cm) );		

		double piMinusGJMag = piMinusGJ3V.Mag();
		double piMinusCosGJ = piMinusGJ3V.Dot(z_gj) / piMinusGJMag ;
		double piMinusPhiGJ = TMath::ATan2( piMinusGJ3V.Dot(y_gj), piMinusGJ3V.Dot(x_gj) );		

		double pi0GJMag = pi0GJ3V.Mag();
		double pi0CosGJ = pi0GJ3V.Dot(z_gj) / pi0GJMag ;
		double pi0PhiGJ = TMath::ATan2( pi0GJ3V.Dot(y_gj), pi0GJ3V.Dot(x_gj) );		



		////////////////// AMPTOOLS ANGLES //////////////////////////////

		// Boost!  FROM: CM Frame ---> TO: X Rest Frame (He_1)
		// TLorentzRotation restFrameXBoost( -particleXCM.BoostVector() ); //defined earlier
		TLorentzVector beamHe_1 = restFrameXBoost * beamCM;
		TLorentzVector targetHe_1 = restFrameXBoost * targetCM;
		TLorentzVector protonHe_1 = restFrameXBoost * protonCM;
		TLorentzVector piPlusHe_1 = restFrameXBoost * piPlusCM;
		TLorentzVector piMinusHe_1 = restFrameXBoost * piMinusCM;
		TLorentzVector photon1He_1 = restFrameXBoost * photon1CM;
		TLorentzVector photon2He_1 = restFrameXBoost * photon2CM;
		TLorentzVector photon3He_1 = restFrameXBoost * photon3CM;
		TLorentzVector photon4He_1 = restFrameXBoost * photon4CM;
		TLorentzVector particleXHe_1 = restFrameXBoost * particleXCM;  

		//Particles
		TLorentzVector threePiHe_1 = piPlusHe_1 + piMinusHe_1 + photon1He_1 + photon2He_1;
		TLorentzVector etaHe_1 = photon3He_1 + photon4He_1; 
			
		//Particles
		TVector3 threePiHe_13V = threePiHe_1.Vect();
	
		TVector3 piPlusHe_13V = piPlusHe_1.Vect();
		TVector3 piMinusHe_13V = piMinusHe_1.Vect();
		TVector3 pi0He_13V = (photon1He_1 + photon2He_1).Vect();
		TVector3 etaHe_13V = (photon3He_1 + photon4He_1).Vect();		

		TVector3 particleXHe_1V3 = particleXHe_1.Vect();
		
		
		// Calculate x, y and z He_1
		TVector3 z_he_1 = (particleXCM.Vect()).Unit();
		TVector3 y_he_1 = ((beamCM.Vect()).Cross(z_he_1)).Unit();//((beamCM.Vect()).Cross( -protonCM.Vect() )).Unit();
		TVector3 x_he_1 = (( y_he_1 ).Cross( z_he_1 )).Unit();

		// Calculate He_1 angles
		double threePiHe_1Mag = threePiHe_13V.Mag();
		double threePiCosHe_1 = threePiHe_13V.Dot(z_he_1) / threePiHe_1Mag ;
		double threePiPhiHe_1 = TMath::ATan2( threePiHe_13V.Dot(y_he_1), threePiHe_13V.Dot(x_he_1) );		


		// Boost!  FROM: X Rest Frame ---> TO: Omega Rest Frame (He_2 = OG)
		TLorentzRotation restFrameOGBoost( -threePiGJ.BoostVector() ); 
		TLorentzVector beamOG = restFrameOGBoost * beamGJ;
		TLorentzVector piPlusOG = restFrameOGBoost * piPlusGJ;
		TLorentzVector piMinusOG = restFrameOGBoost * piMinusGJ;
		TLorentzVector photon1OG = restFrameOGBoost * photon1GJ;
		TLorentzVector photon2OG = restFrameOGBoost * photon2GJ;
	
		TLorentzVector pi0_OG = photon1OG + photon2OG;

		TVector3 z_og = (threePiHe_13V).Unit();
		TVector3 y_og = ((particleXCM.Vect()).Cross( z_og )).Unit();
		TVector3 x_og = ( y_og ).Cross( z_og );		
		
		// Calculating lambda for omega		
		TVector3 piZeroOG3V = photon1OG.Vect() + photon2OG.Vect();
		TVector3 piPlusOG3V = piPlusOG.Vect();
		TVector3 piMinusOG3V = piMinusOG.Vect();

		double piZeroOG3VMag = piZeroOG3V.Mag();
				
		TLorentzVector m3Pions = photon1OG + photon2OG + piPlusOG + piMinusOG ;
        
		double  denominator_lambda = ( (1. / 9.) * m3Pions.M2() ) - ( .140 * .140 );
		double lambdaMax = (3./4.) * ( denominator_lambda * denominator_lambda );

		TVector3 lambdaPions = piPlusOG3V.Cross( piMinusOG3V );
		
		double ratioLambda = lambdaPions.Mag2() / lambdaMax;

		TVector3 normalPlane = (piPlusOG3V.Cross(piMinusOG3V)).Unit();
		
		TVector3 angles_he_2(normalPlane.Dot(x_og),normalPlane.Dot(y_og),normalPlane.Dot(z_og));

		double theta_he_2 =  TMath::Cos(angles_he_2.Theta());
		double phi_he_2 =   angles_he_2.Phi();

		// Boost!    FROM: OG Frame  ---> TO: Pi0 He (PHE)
		TLorentzRotation restFramePi0HEBoost( -pi0_OG.BoostVector() );
	
		TLorentzVector beamPHE = restFramePi0HEBoost * beamOG;
		TLorentzVector photon1PHE = restFramePi0HEBoost * photon1OG;
		TLorentzVector photon2PHE = restFramePi0HEBoost * photon2OG;
	
		TVector3 z_phe = (pi0_OG.Vect()).Unit();
		TVector3 y_phe = ((m3Pions.Vect()).Cross( z_phe )).Unit(); ///I do not know if this is right
		TVector3 x_phe = ( y_phe ).Cross( z_phe );	

		TVector3 photon2PHEV = photon2PHE.Vect();

		double photon2PHeMag = photon2PHEV.Mag();
		double photon2CosHe = photon2PHEV.Dot(z_phe) / photon2PHeMag ;
		double photon2PhiHe = TMath::ATan2( photon2PHEV.Dot(y_phe), photon2PHEV.Dot(x_phe) );		


		// Boost!    FROM: GJ Frame  ---> TO: omega He (HE)
		TLorentzRotation restFrameOmegaHEBoost( -threePiGJ.BoostVector() );
	
		TLorentzVector beamHE = restFrameOmegaHEBoost * beamGJ;
		TLorentzVector piPlusHE = restFrameOmegaHEBoost * piPlusGJ;
		TLorentzVector piMinusHE = restFrameOmegaHEBoost * piMinusGJ;
		TLorentzVector photon1HE = restFrameOmegaHEBoost * photon1GJ;
		TLorentzVector photon2HE = restFrameOmegaHEBoost * photon2GJ;
	
		TVector3 z_he = (-threePiGJ3V).Unit();
		TVector3 y_he = ((particleXCM.Vect()).Cross( z_he )).Unit();
		TVector3 x_he = ( y_he ).Cross( z_he );	


		TVector3 piPpiMHeV = (piPlusHE + piMinusHE).Vect();

		double piPpiMHeMag = piPpiMHeV.Mag();
		double piPpiMCosHe = piPpiMHeV.Dot(z_gj) / piPpiMHeMag ;
		double piPpiMPhiHe = TMath::ATan2( piPpiMHeV.Dot(y_he), piPpiMHeV.Dot(x_he) );		


		// Boost!    FROM: GJ Frame  ---> TO: Eta He (EHE)
		TLorentzRotation restFrameEtaHEBoost( -etaGJ.BoostVector() );
	
		TLorentzVector beamEHE = restFrameEtaHEBoost * beamGJ;
		TLorentzVector photon3EHE = restFrameEtaHEBoost * photon3GJ;
		TLorentzVector photon4EHE = restFrameEtaHEBoost * photon4GJ;
	
		TVector3 z_ehe = (etaGJ.Vect()).Unit();
		TVector3 y_ehe = ( (particleXCM.Vect()).Cross( z_ehe ) ).Unit();
		TVector3 x_ehe = ( y_ehe ).Cross( z_ehe );	

		TVector3 photon3EHEV = photon3EHE.Vect();

		double photon3EHeMag = photon3EHEV.Mag();
		double photon3CosHe = photon3EHEV.Dot(z_gj) / photon3EHeMag ;
		double photon3PhiHe = TMath::ATan2( photon3EHEV.Dot(y_ehe), photon3EHEV.Dot(x_ehe) );		

		/******************************************** EXECUTE ANALYSIS ACTIONS *******************************************/

		// Loop through the analysis actions, executing them in order for the active particle combo
		//dAnalyzeCutActions->Perform_Action(); // Must be executed before Execute_Actions()
		if(!Execute_Actions()) //if the active combo fails a cut, IsComboCutFlag automatically set
			continue;

		//if you manually execute any actions, and it fails a cut, be sure to call:
			//dComboWrapper->Set_IsComboCut(true);


		/**************************************** CUTS  *****************************************/

		//xcuts
		//Defining booleans for cuts

	        	//************************************* Stage 1 Cuts *************************************************//
		bool confidenceLevel =  dComboWrapper->Get_ConfidenceLevel_KinFit( "" ) < 1e-4; //Cut to remove tons of data

		bool showerQuality_Photon1 = false;
		bool showerQuality_Photon2 = false;
		bool showerQuality_Photon3 = false;
		bool showerQuality_Photon4 = false;

		//// suggested in the FCAL quality paper. This could be studied in detail if needed
		if( dPhoton1Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		  showerQuality_Photon1 = dPhoton1Wrapper->Get_Shower_Quality() < .5; 
		
		if( dPhoton2Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		  showerQuality_Photon2 = dPhoton2Wrapper->Get_Shower_Quality() < .5;
	        
		if( dPhoton3Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		  showerQuality_Photon3 = dPhoton3Wrapper->Get_Shower_Quality() < .5;
	       
		if( dPhoton4Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		  showerQuality_Photon4 = dPhoton4Wrapper->Get_Shower_Quality() < .5;

		bool zVertex =  locProtonX4_Measured.Z()  <  52 || locProtonX4_Measured.Z() > 78; // Usused in other GlueX analysis, it might be the standard

		bool stage1Cuts = confidenceLevel ||
				  showerQuality_Photon1 ||
				  showerQuality_Photon2 ||
				  showerQuality_Photon3 ||
				  showerQuality_Photon4 ||
				  zVertex;

		//************************************* Stage 2 Cuts *************************************************//
		bool deltaTBeam = locBeamDeltaT > 2.|| locBeamDeltaT < -2.;  // ontime
		//bool deltaTBeam = locBeamDeltaT < 6. && locBeamDeltaT > -6.;  // accidental skip first off-time peak

		//************************************* Stage 2.1 Cuts *************************************************//

		//Reducing photon candidates window (Needed for better fits)
		bool pi0Window =  locPhotons_1_2.M() < .09 ||  locPhotons_1_2.M() > .19;
		bool etaWindow =  locPhotons_3_4.M() < .4 ||  locPhotons_3_4.M() > .75;

		bool stage2Cuts = deltaTBeam ||
				  pi0Window ||
				  etaWindow;
		

		//************************************* Stage 3 Cuts *************************************************//

		//Removing double pi0 Events
		//Photons Combos	
		//This might be redundant!
		TLorentzVector pi0 = locPhotons_1_2; 
		double pi0_g1g3 = locPhotons_1_3.M();
		double pi0_g1g4 = locPhotons_1_4.M();
		double pi0_g2g3 = locPhotons_2_3.M();
		double pi0_g2g4 = locPhotons_2_4.M();
		TLorentzVector eta = locPhotons_3_4;

		//Fitted values for on-Time Photons
		double g1g3Mean = (.131 + .135)/2; double g1g3Var = (.0166*.0166 + .0064*.0064)/2;
		double g2g4Mean = (.130 + .134)/2; double g2g4Var = (.0169*.0169 + .0063*.0063)/2;

		double g1g4Mean = (.131 + .135)/2; double g1g4Var = (.0171*.0171 + .0064*.0064)/2;
		double g2g3Mean = (.131 + .134)/2; double g2g3Var = (.0165*.0165 + .0062*.0062)/2;

		int sigmaNumber = 3;

		double pi0overlap1 = (pi0_g1g3 - g1g3Mean)*(pi0_g1g3 - g1g3Mean)/(sigmaNumber*sigmaNumber*g1g3Var) + (pi0_g2g4 - g2g4Mean)*(pi0_g2g4 - g2g4Mean)/(sigmaNumber*sigmaNumber*g2g4Var);//ellipse
		bool pi0Veto1 = pi0overlap1 < 1;

		double pi0overlap2 = (pi0_g1g4 - g1g4Mean)*(pi0_g1g4 - g1g4Mean)/(sigmaNumber*sigmaNumber*g1g4Var) + (pi0_g2g3 - g2g3Mean)*(pi0_g2g3 - g2g3Mean)/(sigmaNumber*sigmaNumber*g2g3Var);//ellipse
		bool pi0Veto2 = pi0overlap2 < 1;


		bool stage3Cuts = pi0Veto1 ||
				  pi0Veto2;	      

		//************************************* Stage 4 Cuts *************************************************//


		bool beamEnergy = locBeamP4_Measured.E() < 8.2 || locBeamP4_Measured.E() > 8.8; //Collaboration standard
		bool missingEnergy =  locMissingP4_Measured.E() < (.115 - 3*.303) || locMissingP4_Measured.E() > (.115 + 3*.303); //Value for this was fitted
		bool missingMassSquared = locMissingP4_Measured.M2() < -0.04 || locMissingP4_Measured.M2() > 0.04;

		bool omegaWindow = loc3Pi.M() < .66 || loc3Pi.M() > .9;

		bool stage4Cuts = beamEnergy ||
				  missingEnergy||
				  missingMassSquared||
				  omegaWindow;

		//************************************* Stage 5 Cuts *************************************************//

		bool tOmegaEtaCut = -1*locMomentumTransfer.M2() > .6;

		bool stage5Cuts = tOmegaEtaCut;

		//*****************************************************************************************************//
		
		//Cuts
		//Stage Cuts 

		if( stage1Cuts || stage2Cuts || stage3Cuts || stage4Cuts || stage5Cuts ){
		  dComboWrapper->Set_IsComboCut(true);
		  continue;
		}

		// //Testing Number of Neutral Hypothesis
		// if( Get_NumNeutralHypos() <= 4 ){
		//    dComboWrapper->Set_IsComboCut(true);
		//    continue;
		//  }

		//Select best cl combo
		double current_cl =  dComboWrapper->Get_ConfidenceLevel_KinFit( "" );
		if( combo_cl_max < current_cl ) combo_cl_max = current_cl;


	}


	/************************************************* LOOP OVER COMBOS *************************************************/
	//Loop hist
	for(UInt_t loc_i = 0; loc_i < Get_NumCombos(); ++loc_i)
	{

	        //Set branch array indices for combo and all combo particles
                dComboWrapper->Set_ComboIndex(loc_i);

		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut()) // Is false when tree originally created
			continue; // Combo has been cut previously

		/********************************************** GET PARTICLE INDICES *********************************************/

		//Used for tracking uniqueness when filling histograms, and for determining unused particles

		//Step 0
		Int_t locBeamID = dComboBeamWrapper->Get_BeamID();
		Int_t locPiPlusTrackID = dPiPlusWrapper->Get_TrackID();
		Int_t locPiMinusTrackID = dPiMinusWrapper->Get_TrackID();
		Int_t locProtonTrackID = dProtonWrapper->Get_TrackID();

		//Step 1
		Int_t locPhoton1NeutralID = dPhoton1Wrapper->Get_NeutralID();
		Int_t locPhoton2NeutralID = dPhoton2Wrapper->Get_NeutralID();

		//Step 2
		Int_t locPhoton3NeutralID = dPhoton3Wrapper->Get_NeutralID();
		Int_t locPhoton4NeutralID = dPhoton4Wrapper->Get_NeutralID();

		/*********************************************** GET FOUR-MOMENTUM **********************************************/

		// Get P4's: //is kinfit if kinfit performed, else is measured
		//dTargetP4 is target p4
		//Step 0
		TLorentzVector locBeamP4 = dComboBeamWrapper->Get_P4();
		TLorentzVector locPiPlusP4 = dPiPlusWrapper->Get_P4();
		TLorentzVector locPiMinusP4 = dPiMinusWrapper->Get_P4();
		TLorentzVector locProtonP4 = dProtonWrapper->Get_P4();
		//Step 1
		TLorentzVector locPhoton1P4 = dPhoton1Wrapper->Get_P4();
		TLorentzVector locPhoton2P4 = dPhoton2Wrapper->Get_P4();
		//Step 2
		TLorentzVector locPhoton3P4 = dPhoton3Wrapper->Get_P4();
		TLorentzVector locPhoton4P4 = dPhoton4Wrapper->Get_P4();

		// Get Measured P4's:
		//Step 0
		TLorentzVector locBeamP4_Measured = dComboBeamWrapper->Get_P4_Measured();
		TLorentzVector locPiPlusP4_Measured = dPiPlusWrapper->Get_P4_Measured();
		TLorentzVector locPiMinusP4_Measured = dPiMinusWrapper->Get_P4_Measured();
		TLorentzVector locProtonP4_Measured = dProtonWrapper->Get_P4_Measured();
		//Step 1
		TLorentzVector locPhoton1P4_Measured = dPhoton1Wrapper->Get_P4_Measured();
		TLorentzVector locPhoton2P4_Measured = dPhoton2Wrapper->Get_P4_Measured();
		//Step 2
		TLorentzVector locPhoton3P4_Measured = dPhoton3Wrapper->Get_P4_Measured();
		TLorentzVector locPhoton4P4_Measured = dPhoton4Wrapper->Get_P4_Measured();

		/*********************************************** GET FOUR-VECTOR ************************************************/

		//Step 0
		TLorentzVector locBeamX4 = dComboBeamWrapper->Get_X4();
		TLorentzVector locPiPlusX4 = dPiPlusWrapper->Get_X4();
		TLorentzVector locPiMinusX4 = dPiMinusWrapper->Get_X4();
		TLorentzVector locProtonX4 = dProtonWrapper->Get_X4();
		//Step 1
		TLorentzVector locPhoton1X4 = dPhoton1Wrapper->Get_X4();
		TLorentzVector locPhoton2X4 = dPhoton2Wrapper->Get_X4();
		//Step 1
		TLorentzVector locPhoton3X4 = dPhoton3Wrapper->Get_X4();
		TLorentzVector locPhoton4X4 = dPhoton4Wrapper->Get_X4();

		// Get Measured X4's:
		//Step 0
		TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
		TLorentzVector locPiPlusX4_Measured = dPiPlusWrapper->Get_X4_Measured();
		TLorentzVector locPiMinusX4_Measured = dPiMinusWrapper->Get_X4_Measured();
		TLorentzVector locProtonX4_Measured = dProtonWrapper->Get_X4_Measured();

		//Step 1
		TLorentzVector locPhoton1X4_Measured = dPhoton1Wrapper->Get_X4_Measured();
		TLorentzVector locPhoton2X4_Measured = dPhoton2Wrapper->Get_X4_Measured();

		//Step 2
		TLorentzVector locPhoton3X4_Measured = dPhoton3Wrapper->Get_X4_Measured();
		TLorentzVector locPhoton4X4_Measured = dPhoton4Wrapper->Get_X4_Measured();

	        
		/********************************************* COMBINE FOUR-MOMENTUM ********************************************/

		// DO YOUR STUFF HERE

		// Combine 4-vectors
		TLorentzVector locMissingP4_Measured = locBeamP4_Measured + dTargetP4;
		locMissingP4_Measured -= locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locMissingP4 = locBeamP4 + dTargetP4;
		locMissingP4 -= locPiPlusP4 + locPiMinusP4 + locProtonP4 + locPhoton1P4 + locPhoton2P4 + locPhoton3P4 + locPhoton4P4;

		//Photons Combos
		TLorentzVector locPhotons_1_2_Measured = locPhoton1P4_Measured + locPhoton2P4_Measured;
		TLorentzVector locPhotons_1_3_Measured = locPhoton1P4_Measured + locPhoton3P4_Measured;
		TLorentzVector locPhotons_1_4_Measured = locPhoton1P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhotons_2_3_Measured = locPhoton2P4_Measured + locPhoton3P4_Measured;
		TLorentzVector locPhotons_2_4_Measured = locPhoton2P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhotons_3_4_Measured = locPhoton3P4_Measured + locPhoton4P4_Measured;

		TLorentzVector locPhotons_1_2 = locPhoton1P4 + locPhoton2P4;//Pi0 hypothesis
		TLorentzVector locPhotons_1_3 = locPhoton1P4 + locPhoton3P4;
		TLorentzVector locPhotons_1_4 = locPhoton1P4 + locPhoton4P4;
		TLorentzVector locPhotons_2_3 = locPhoton2P4 + locPhoton3P4;
		TLorentzVector locPhotons_2_4 = locPhoton2P4 + locPhoton4P4;
		TLorentzVector locPhotons_3_4 = locPhoton3P4 + locPhoton4P4;//eta hypothesis

		//3 Photons
		TLorentzVector locPhotons_1_2_3 = locPhoton1P4 + locPhoton2P4 + locPhoton3P4;
		TLorentzVector locPhotons_1_2_4 = locPhoton1P4 + locPhoton2P4 + locPhoton4P4;
		TLorentzVector locPhotons_1_3_4 = locPhoton1P4 + locPhoton3P4 + locPhoton4P4;
		TLorentzVector locPhotons_2_3_4 = locPhoton2P4 + locPhoton3P4 + locPhoton4P4;

		//4Photons
		TLorentzVector locPhotons_1_2_3_4 = locPhoton1P4 + locPhoton2P4 + locPhoton3P4 + locPhoton4P4;

		//3Pi combos
		TLorentzVector loc3Pi_Measured = locPiPlusP4_Measured + locPiMinusP4_Measured + locPhotons_1_2_Measured;
		TLorentzVector loc2Pi_Eta_Measured = locPiPlusP4_Measured + locPiMinusP4_Measured + locPhotons_3_4_Measured;

		TLorentzVector loc3Pi = locPiPlusP4 + locPiMinusP4 + locPhotons_1_2;
		TLorentzVector loc2Pi_Eta = locPiPlusP4 + locPiMinusP4 + locPhotons_3_4;

		//Baryons
		TLorentzVector locPipP = locPiPlusP4 + locProtonP4;
		TLorentzVector locPimP = locPiMinusP4 + locProtonP4;
		TLorentzVector locPi0P = locPhotons_1_2 + locProtonP4;
		TLorentzVector locEtaP = locPhotons_3_4 + locProtonP4;
		TLorentzVector locOmegaP = loc3Pi + locProtonP4;

		TLorentzVector locPipP_Measured = locPiPlusP4_Measured + locProtonP4_Measured;
		TLorentzVector locPimP_Measured = locPiMinusP4_Measured + locProtonP4_Measured;
		TLorentzVector locPi0P_Measured = locPhotons_1_2_Measured + locProtonP4_Measured;
		TLorentzVector locEtaP_Measured = locPhotons_3_4_Measured + locProtonP4_Measured;
		TLorentzVector locOmegaP_Measured = loc3Pi_Measured + locProtonP4_Measured;

		//Meson 
		TLorentzVector locPipPim = locPiPlusP4 + locPiMinusP4;
		TLorentzVector locPipPi0 = locPiPlusP4 + locPhotons_1_2;
		TLorentzVector locPipEta = locPiPlusP4 + locPhotons_3_4;
		TLorentzVector locPimPi0 = locPiMinusP4 + locPhotons_1_2;
		TLorentzVector locPimEta = locPiMinusP4 + locPhotons_3_4;
		TLorentzVector locPi0Eta = locPhotons_1_2 + locPhotons_3_4;

		//4 Particle
		TLorentzVector loc3piEta_Measured = locPiPlusP4_Measured + locPiMinusP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector loc3piEta = locPiPlusP4 + locPiMinusP4 + locPhoton1P4 + locPhoton2P4 + locPhoton3P4 + locPhoton4P4;


		//////////////////////////////////////////

		TLorentzVector locPipPimM_Measured =  locBeamP4_Measured + dTargetP4;
		locPipPimM_Measured -=  locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;

		TLorentzVector locPhoton1M_Measured =  locBeamP4_Measured + dTargetP4;
	        locPhoton1M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured +  locPhoton2P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhoton2M_Measured =  locBeamP4_Measured + dTargetP4;
		locPhoton2M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhoton3M_Measured =  locBeamP4_Measured + dTargetP4;
	        locPhoton3M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locPhoton4M_Measured =  locBeamP4_Measured + dTargetP4;
	        locPhoton4M_Measured -=  locPiPlusP4_Measured + locPiMinusP4_Measured + locProtonP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured;

		TLorentzVector locg1g2M_Measured = locPhoton1M_Measured + locPhoton2P4_Measured;
		TLorentzVector locg1g3M_Measured = locPhoton1M_Measured + locPhoton3P4_Measured;
		TLorentzVector locg1g4M_Measured = locPhoton1M_Measured + locPhoton4P4_Measured;
		TLorentzVector locg2g3M_Measured = locPhoton2M_Measured + locPhoton3P4_Measured;
		TLorentzVector locg2g4M_Measured = locPhoton2M_Measured + locPhoton4P4_Measured;
		TLorentzVector locg3g4M_Measured = locPhoton3M_Measured + locPhoton4P4_Measured;

		TLorentzVector locg1g2g3M_Measured = locPhoton1M_Measured + locPhoton2P4_Measured + locPhoton3P4_Measured;
		TLorentzVector locg1g2g4M_Measured = locPhoton1M_Measured + locPhoton2P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locg1g3g4M_Measured = locPhoton1M_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;
		TLorentzVector locg2g3g4M_Measured = locPhoton2M_Measured + locPhoton3P4_Measured + locPhoton4P4_Measured;

		///////////////////////////////////////////////////////////////////////////////////////

		//Calculating Delta T (using Measured data)
		double locRFTime = dComboWrapper->Get_RFTime();
		//Beam
		double locPropagatedRFTimeBeam =  locRFTime + ( locBeamX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locBeamDeltaT = locBeamX4_Measured.T() - locPropagatedRFTimeBeam;
		//Proton
		double locPropagatedRFTimeProton =  locRFTime + ( locProtonX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locProtonDeltaT = locProtonX4_Measured.T() - locPropagatedRFTimeProton;		
		//PiP
		double locPropagatedRFTimePiPlus = locRFTime + ( locPiPlusX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPiPlusDeltaT = locPiPlusX4_Measured.T() - locPropagatedRFTimePiPlus;		
		//PiM
		double locPropagatedRFTimePiMinus = locRFTime + ( locPiMinusX4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPiMinusDeltaT = locPiMinusX4_Measured.T() - locPropagatedRFTimePiMinus;
		//Photon1
		double locPropagatedRFTimePhoton1 = locRFTime + ( locPhoton1X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton1DeltaT = locPhoton1X4_Measured.T() - locPropagatedRFTimePhoton1;
		//Photon2
		double locPropagatedRFTimePhoton2 = locRFTime + ( locPhoton2X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton2DeltaT = locPhoton2X4_Measured.T() - locPropagatedRFTimePhoton2;
		//Photon3
		double locPropagatedRFTimePhoton3 = locRFTime + ( locPhoton3X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton3DeltaT = locPhoton3X4_Measured.T() - locPropagatedRFTimePhoton3;
		//Photon4
		double locPropagatedRFTimePhoton4 = locRFTime + ( locPhoton4X4_Measured.Z() - dTargetCenter.Z() )/29.9792458;
		double locPhoton4DeltaT = locPhoton4X4_Measured.T() - locPropagatedRFTimePhoton4;

		///////////////////////////////////////////////////////////////////////////////////////

		//Calculating t min for omega eta system
		TLorentzVector locMomentumTransfer = locBeamP4  - loc3piEta;//[needs to be squared to be t [.M2()]
		TLorentzVector sMandelstam = locBeamP4 + dTargetP4; //This is not s until .M2() [it needs to be squared]
	   
		double E3CM = ( sMandelstam.M2() + loc3piEta.M2() - locProtonP4.M2() ) / (2*sMandelstam.M());// equation 47.36 pdg book
		double p3CM = sqrt( E3CM*E3CM - loc3piEta.M2()); // equation 47.37
		double p1CM = ( locBeamP4.Vect() ).Mag() * dTargetP4.M() / sMandelstam.M() ; // equation 47.37
		double t_1term =  ( locBeamP4.M2() - loc3piEta.M2() - dTargetP4.M2() + locProtonP4.M2() )/ (2*sMandelstam.M()); //  First term in equation 47.35
		double tmin = (t_1term)*(t_1term) - (p1CM - p3CM)*(p1CM - p3CM); // Eq 47.35
		double tprime = (locMomentumTransfer.M2() - tmin); 
		tprime = -1 * tprime;


		//Calculating t min for omega system
		TLorentzVector locMomentumTransfer_omega = locBeamP4  - loc3Pi;//[needs to be squared to be t [.M2()]
		TLorentzVector sMandelstam_omega = locBeamP4 + dTargetP4; //This is not s until .M2() [it needs to be squared]
	   
		double E3CM_omega = ( sMandelstam_omega.M2() + loc3Pi.M2() - locEtaP.M2() ) / (2*sMandelstam_omega.M());// equation 47.36 pdg book
		double p3CM_omega = sqrt( E3CM_omega*E3CM_omega - loc3Pi.M2()); // equation 47.37
		double p1CM_omega = ( locBeamP4.Vect() ).Mag() * dTargetP4.M() / sMandelstam_omega.M() ; // equation 47.37
		double t_1term_omega =  ( locBeamP4.M2() - loc3Pi.M2() - dTargetP4.M2() + locEtaP.M2() )/ (2*sMandelstam_omega.M()); //  First term in equation 47.35
		double tmin_omega = (t_1term_omega)*(t_1term_omega) - (p1CM_omega - p3CM_omega)*(p1CM_omega - p3CM_omega); // Eq 47.35
		double tprime_omega = (locMomentumTransfer_omega.M2() - tmin_omega); 
		tprime_omega = -1 * tprime_omega;


		/////t's
		double t_eta = -1*(locBeamP4 - locPhotons_3_4).M2();
		double t_etaP = -1*(locBeamP4 - locEtaP).M2();
		double t_omegaEta = -1*(locBeamP4 - loc3piEta).M2();
		double t_omega = -1*(locBeamP4 - loc3Pi).M2();
		double t_omegaP = -1*(locBeamP4 - locOmegaP).M2();
		double t_proton = -1*(locBeamP4 - locProtonP4).M2();


		///////////////////////////////////////////////////////////////////////////////////////

		// Calculate LAB angles
		double threePiCosLAB = (loc3Pi.Vect()).CosTheta();
		double threePiPhiLAB = (loc3Pi.Vect()).Phi();

		double etaCosLAB = (locPhotons_3_4.Vect()).CosTheta();
		double etaPhiLAB = (locPhotons_3_4.Vect()).Phi();

		double piPlusCosLAB = (locPiPlusP4.Vect()).CosTheta();
		double piPlusPhiLAB = (locPiPlusP4.Vect()).Phi();

		double piMinusCosLAB = (locPiMinusP4.Vect()).CosTheta();
		double piMinusPhiLAB = (locPiMinusP4.Vect()).Phi();

		double pi0CosLAB = (locPhotons_1_2.Vect()).CosTheta();
		double pi0PhiLAB = (locPhotons_1_2.Vect()).Phi();

		double protonCosLAB = (locProtonP4.Vect()).CosTheta();
		double protonPhiLAB = (locProtonP4.Vect()).Phi();

		// Boost  FROM: LAB  ---> TO: CM Frame
		TLorentzVector centerOfMass = locBeamP4 + dTargetP4;
		TLorentzRotation centerofMassBoost( -centerOfMass.BoostVector() );

		TLorentzVector beamCM = centerofMassBoost * locBeamP4;
		TLorentzVector targetCM = centerofMassBoost * dTargetP4;
		TLorentzVector piPlusCM = centerofMassBoost * locPiPlusP4;
		TLorentzVector piMinusCM = centerofMassBoost * locPiMinusP4;
		TLorentzVector protonCM = centerofMassBoost * locProtonP4;
		TLorentzVector photon1CM = centerofMassBoost * locPhoton1P4;
		TLorentzVector photon2CM = centerofMassBoost * locPhoton2P4;
		TLorentzVector photon3CM = centerofMassBoost * locPhoton3P4;
		TLorentzVector photon4CM = centerofMassBoost * locPhoton4P4;
		TLorentzVector particleXCM = centerofMassBoost * loc3piEta;

		TLorentzVector etaProtonCM = ( photon3CM + photon4CM ) + protonCM;

		TVector3 threePiCMV3 = ( piMinusCM + piPlusCM + photon1CM + photon2CM).Vect();

		TVector3 etaCMV3 = ( photon3CM+ photon4CM ).Vect();
		TVector3 piPlusCMV3 = piPlusCM.Vect();
		TVector3 piMinusCMV3 = piMinusCM.Vect();
		TVector3 pi0CMV3 = photon1CM.Vect() + photon2CM.Vect();

		TVector3 omegaEtaCM =  particleXCM.Vect();

		TVector3 z_cm = beamCM.Vect().Unit();
		TVector3 y_cm = (beamCM.Vect().Cross( -protonCM.Vect() ) ).Unit();
		TVector3 x_cm = (y_cm).Cross(z_cm).Unit();

	    
		// Calculate CM angles

		double threePiCMMag = threePiCMV3.Mag();
		double threePiCosCM = threePiCMV3.Dot(z_cm) / threePiCMMag ;
		double threePiPhiCM = TMath::ATan2( threePiCMV3.Dot(y_cm), threePiCMV3.Dot(x_cm) );		

		double etaCMMag = etaCMV3.Mag();
		double etaCosCM = etaCMV3.Dot(z_cm) / etaCMMag ;
		double etaPhiCM = TMath::ATan2( etaCMV3.Dot(y_cm), etaCMV3.Dot(x_cm) );		

		double piPlusCMMag = piPlusCMV3.Mag();
		double piPlusCosCM = piPlusCMV3.Dot(z_cm) / piPlusCMMag ;
		double piPlusPhiCM = TMath::ATan2( piPlusCMV3.Dot(y_cm), piPlusCMV3.Dot(x_cm) );		

		double piMinusCMMag = piMinusCMV3.Mag();
		double piMinusCosCM = piMinusCMV3.Dot(z_cm) / piMinusCMMag ;
		double piMinusPhiCM = TMath::ATan2( piMinusCMV3.Dot(y_cm), piMinusCMV3.Dot(x_cm) );		

		double pi0CMMag = pi0CMV3.Mag();
		double pi0CosCM = pi0CMV3.Dot(z_cm) / pi0CMMag ;
		double pi0PhiCM = TMath::ATan2( pi0CMV3.Dot(y_cm), pi0CMV3.Dot(x_cm) );	


		double protonCosCM =  (protonCM.Vect()).Dot(z_cm) / (protonCM.Vect()).Mag() ;	

		////////////////////////////////////////////////////////////////////////////////////////////////////////////
		//VanHove
		TLorentzVector vH_piPlus = piPlusCM;
		TLorentzVector vH_piMinus = piMinusCM;
		TLorentzVector vH_photon1 = photon1CM;
		TLorentzVector vH_photon2 = photon2CM;
		TLorentzVector vH_photon3 = photon3CM;
		TLorentzVector vH_photon4 = photon4CM;
		TLorentzVector vH_proton = protonCM;

		TLorentzVector vH_omega = vH_piPlus + vH_piMinus + vH_photon1 + vH_photon2;
		TLorentzVector vH_eta =  vH_photon3 + vH_photon4;

		double locParticle1_VH = vH_omega.Pz();
		double locParticle2_VH = vH_eta.Pz();
		double locParticle3_VH = vH_proton.Pz();
		double locVanHoveQ = TMath::Sqrt( locParticle1_VH* locParticle1_VH + locParticle2_VH* locParticle2_VH + locParticle3_VH* locParticle3_VH );
		double locVanHovePhi = TMath::ATan2(  -1*TMath::Sqrt(3.)*locParticle1_VH, 2*locParticle2_VH+locParticle1_VH ) + TMath::Pi();// added pi to map [-pi,pi] on [0,2pi]
		double vHX = locVanHoveQ*TMath::Cos(locVanHovePhi);
		double vHY = locVanHoveQ*TMath::Sin(locVanHovePhi);


		////////////////////////////////////////////////////////////////////////////////////////////////////////////
       		// Boost!    FROM: CM Frame  ---> TO: etaP Rest Frame (EP)
		TLorentzRotation restFrameEPBoost( -etaProtonCM.BoostVector() );
	
		TLorentzVector beamEP = restFrameEPBoost * beamCM;
		TLorentzVector targetEP = restFrameEPBoost * targetCM;
		TLorentzVector protonEP = restFrameEPBoost * protonCM;
		TLorentzVector piPlusEP = restFrameEPBoost * piPlusCM;
		TLorentzVector piMinusEP = restFrameEPBoost * piMinusCM;
		TLorentzVector photon1EP = restFrameEPBoost * photon1CM;
		TLorentzVector photon2EP = restFrameEPBoost * photon2CM;
		TLorentzVector photon3EP = restFrameEPBoost * photon3CM;
		TLorentzVector photon4EP = restFrameEPBoost * photon4CM;


		TLorentzVector etaEP = photon3EP + photon4EP; 
		TLorentzVector etaProtonEP = etaEP + protonEP;


		////////////////////////////////////////////////////////////////////////////////////////////////////////////

       		// Boost!  FROM: CM Frame ---> TO: X Rest Frame (GJ)
		TLorentzRotation restFrameXBoost( -particleXCM.BoostVector() );
	
		TLorentzVector beamGJ = restFrameXBoost * beamCM;
		TLorentzVector targetGJ = restFrameXBoost * targetCM;
		TLorentzVector protonGJ = restFrameXBoost * protonCM;
		TLorentzVector piPlusGJ = restFrameXBoost * piPlusCM;
		TLorentzVector piMinusGJ = restFrameXBoost * piMinusCM;
		TLorentzVector photon1GJ = restFrameXBoost * photon1CM;
		TLorentzVector photon2GJ = restFrameXBoost * photon2CM;
		TLorentzVector photon3GJ = restFrameXBoost * photon3CM;
		TLorentzVector photon4GJ = restFrameXBoost * photon4CM;
		TLorentzVector particleXGJ = restFrameXBoost * particleXCM;  

		//Particles
		TLorentzVector threePiGJ = piPlusGJ + piMinusGJ + photon1GJ + photon2GJ;
		TLorentzVector etaGJ = photon3GJ + photon4GJ; 
			
		//Particles
		TVector3 threePiGJ3V = threePiGJ.Vect();
	
		TVector3 piPlusGJ3V = piPlusGJ.Vect();
		TVector3 piMinusGJ3V = piMinusGJ.Vect();
		TVector3 pi0GJ3V = (photon1GJ + photon2GJ).Vect();
		TVector3 etaGJ3V = (photon3GJ + photon4GJ).Vect();		

		TVector3 particleXGJV3 = particleXGJ.Vect();
		
		
		// Calculate x, y and z GJ
		TVector3 z_gj = (beamGJ.Vect()).Unit();
		TVector3 y_gj = ((beamCM.Vect()).Cross( -protonCM.Vect() )).Unit();//((beamCM.Vect()).Cross( omegaEtaCM )).Unit();
		TVector3 x_gj = (( y_gj ).Cross( z_gj )).Unit();

		// Calculate GJ angles
		double threePiGJMag = threePiGJ3V.Mag();
		double threePiCosGJ = threePiGJ3V.Dot(z_gj) / threePiGJMag ;
		double threePiPhiGJ = TMath::ATan2( threePiGJ3V.Dot(y_gj), threePiGJ3V.Dot(x_gj) );		

		double etaGJMag = etaGJ3V.Mag();
		double etaCosGJ = etaGJ3V.Dot(z_gj) / etaGJMag ;
		double etaPhiGJ = TMath::ATan2( etaGJ3V.Dot(y_gj), etaGJ3V.Dot(x_gj) );		

		double piPlusGJMag = piPlusGJ3V.Mag();
		double piPlusCosGJ = piPlusGJ3V.Dot(z_gj) / piPlusGJMag ;
		double piPlusPhiGJ = TMath::ATan2( piPlusGJ3V.Dot(y_gj), piPlusGJ3V.Dot(x_cm) );		

		double piMinusGJMag = piMinusGJ3V.Mag();
		double piMinusCosGJ = piMinusGJ3V.Dot(z_gj) / piMinusGJMag ;
		double piMinusPhiGJ = TMath::ATan2( piMinusGJ3V.Dot(y_gj), piMinusGJ3V.Dot(x_gj) );		

		double pi0GJMag = pi0GJ3V.Mag();
		double pi0CosGJ = pi0GJ3V.Dot(z_gj) / pi0GJMag ;
		double pi0PhiGJ = TMath::ATan2( pi0GJ3V.Dot(y_gj), pi0GJ3V.Dot(x_gj) );		



		////////////////// AMPTOOLS ANGLES //////////////////////////////

		// Boost!  FROM: CM Frame ---> TO: X Rest Frame (He_1)
		// TLorentzRotation restFrameXBoost( -particleXCM.BoostVector() ); //defined earlier
		TLorentzVector beamHe_1 = restFrameXBoost * beamCM;
		TLorentzVector targetHe_1 = restFrameXBoost * targetCM;
		TLorentzVector protonHe_1 = restFrameXBoost * protonCM;
		TLorentzVector piPlusHe_1 = restFrameXBoost * piPlusCM;
		TLorentzVector piMinusHe_1 = restFrameXBoost * piMinusCM;
		TLorentzVector photon1He_1 = restFrameXBoost * photon1CM;
		TLorentzVector photon2He_1 = restFrameXBoost * photon2CM;
		TLorentzVector photon3He_1 = restFrameXBoost * photon3CM;
		TLorentzVector photon4He_1 = restFrameXBoost * photon4CM;
		TLorentzVector particleXHe_1 = restFrameXBoost * particleXCM;  

		//Particles
		TLorentzVector threePiHe_1 = piPlusHe_1 + piMinusHe_1 + photon1He_1 + photon2He_1;
		TLorentzVector etaHe_1 = photon3He_1 + photon4He_1; 
			
		//Particles
		TVector3 threePiHe_13V = threePiHe_1.Vect();
	
		TVector3 piPlusHe_13V = piPlusHe_1.Vect();
		TVector3 piMinusHe_13V = piMinusHe_1.Vect();
		TVector3 pi0He_13V = (photon1He_1 + photon2He_1).Vect();
		TVector3 etaHe_13V = (photon3He_1 + photon4He_1).Vect();		

		TVector3 particleXHe_1V3 = particleXHe_1.Vect();
		
		
		// Calculate x, y and z He_1
		TVector3 z_he_1 = (particleXCM.Vect()).Unit();
		TVector3 y_he_1 = ((beamCM.Vect()).Cross(z_he_1)).Unit();//((beamCM.Vect()).Cross( -protonCM.Vect() )).Unit();
		TVector3 x_he_1 = (( y_he_1 ).Cross( z_he_1 )).Unit();

		// Calculate He_1 angles
		double threePiHe_1Mag = threePiHe_13V.Mag();
		double threePiCosHe_1 = threePiHe_13V.Dot(z_he_1) / threePiHe_1Mag ;
		double threePiPhiHe_1 = TMath::ATan2( threePiHe_13V.Dot(y_he_1), threePiHe_13V.Dot(x_he_1) );		


		// Boost!  FROM: X Rest Frame ---> TO: Omega Rest Frame (He_2 = OG)
		TLorentzRotation restFrameOGBoost( -threePiGJ.BoostVector() ); 
		TLorentzVector beamOG = restFrameOGBoost * beamGJ;
		TLorentzVector piPlusOG = restFrameOGBoost * piPlusGJ;
		TLorentzVector piMinusOG = restFrameOGBoost * piMinusGJ;
		TLorentzVector photon1OG = restFrameOGBoost * photon1GJ;
		TLorentzVector photon2OG = restFrameOGBoost * photon2GJ;
	
		TLorentzVector pi0_OG = photon1OG + photon2OG;

		TVector3 z_og = (threePiHe_13V).Unit();
		TVector3 y_og = ((particleXCM.Vect()).Cross( z_og )).Unit();
		TVector3 x_og = ( y_og ).Cross( z_og );		
		
		// Calculating lambda for omega		
		TVector3 piZeroOG3V = photon1OG.Vect() + photon2OG.Vect();
		TVector3 piPlusOG3V = piPlusOG.Vect();
		TVector3 piMinusOG3V = piMinusOG.Vect();

		double piZeroOG3VMag = piZeroOG3V.Mag();
				
		TLorentzVector m3Pions = photon1OG + photon2OG + piPlusOG + piMinusOG ;
        
		double  denominator_lambda = ( (1. / 9.) * m3Pions.M2() ) - ( .140 * .140 );
		double lambdaMax = (3./4.) * ( denominator_lambda * denominator_lambda );

		TVector3 lambdaPions = piPlusOG3V.Cross( piMinusOG3V );
		
		double ratioLambda = lambdaPions.Mag2() / lambdaMax;

		TVector3 normalPlane = (piPlusOG3V.Cross(piMinusOG3V)).Unit();
		
		TVector3 angles_he_2(normalPlane.Dot(x_og),normalPlane.Dot(y_og),normalPlane.Dot(z_og));

		double theta_he_2 =  TMath::Cos(angles_he_2.Theta());
		double phi_he_2 =   angles_he_2.Phi();

		// Boost!    FROM: OG Frame  ---> TO: Pi0 He (PHE)
		TLorentzRotation restFramePi0HEBoost( -pi0_OG.BoostVector() );
	
		TLorentzVector beamPHE = restFramePi0HEBoost * beamOG;
		TLorentzVector photon1PHE = restFramePi0HEBoost * photon1OG;
		TLorentzVector photon2PHE = restFramePi0HEBoost * photon2OG;
	
		TVector3 z_phe = (pi0_OG.Vect()).Unit();
		TVector3 y_phe = ((m3Pions.Vect()).Cross( z_phe )).Unit(); ///I do not know if this is right
		TVector3 x_phe = ( y_phe ).Cross( z_phe );	

		TVector3 photon2PHEV = photon2PHE.Vect();

		double photon2PHeMag = photon2PHEV.Mag();
		double photon2CosHe = photon2PHEV.Dot(z_phe) / photon2PHeMag ;
		double photon2PhiHe = TMath::ATan2( photon2PHEV.Dot(y_phe), photon2PHEV.Dot(x_phe) );		


		// Boost!    FROM: GJ Frame  ---> TO: omega He (HE)
		TLorentzRotation restFrameOmegaHEBoost( -threePiGJ.BoostVector() );
	
		TLorentzVector beamHE = restFrameOmegaHEBoost * beamGJ;
		TLorentzVector piPlusHE = restFrameOmegaHEBoost * piPlusGJ;
		TLorentzVector piMinusHE = restFrameOmegaHEBoost * piMinusGJ;
		TLorentzVector photon1HE = restFrameOmegaHEBoost * photon1GJ;
		TLorentzVector photon2HE = restFrameOmegaHEBoost * photon2GJ;
	
		TVector3 z_he = (-threePiGJ3V).Unit();
		TVector3 y_he = ((particleXCM.Vect()).Cross( z_he )).Unit();
		TVector3 x_he = ( y_he ).Cross( z_he );	


		TVector3 piPpiMHeV = (piPlusHE + piMinusHE).Vect();

		double piPpiMHeMag = piPpiMHeV.Mag();
		double piPpiMCosHe = piPpiMHeV.Dot(z_gj) / piPpiMHeMag ;
		double piPpiMPhiHe = TMath::ATan2( piPpiMHeV.Dot(y_he), piPpiMHeV.Dot(x_he) );		


		// Boost!    FROM: GJ Frame  ---> TO: Eta He (EHE)
		TLorentzRotation restFrameEtaHEBoost( -etaGJ.BoostVector() );
	
		TLorentzVector beamEHE = restFrameEtaHEBoost * beamGJ;
		TLorentzVector photon3EHE = restFrameEtaHEBoost * photon3GJ;
		TLorentzVector photon4EHE = restFrameEtaHEBoost * photon4GJ;
	
		TVector3 z_ehe = (etaGJ.Vect()).Unit();
		TVector3 y_ehe = ( (particleXCM.Vect()).Cross( z_ehe ) ).Unit();
		TVector3 x_ehe = ( y_ehe ).Cross( z_ehe );	

		TVector3 photon3EHEV = photon3EHE.Vect();

		double photon3EHeMag = photon3EHEV.Mag();
		double photon3CosHe = photon3EHEV.Dot(z_gj) / photon3EHeMag ;
		double photon3PhiHe = TMath::ATan2( photon3EHEV.Dot(y_ehe), photon3EHEV.Dot(x_ehe) );		

		/******************************************** EXECUTE ANALYSIS ACTIONS *******************************************/

		// Loop through the analysis actions, executing them in order for the active particle combo
		//dAnalyzeCutActions->Perform_Action(); // Must be executed before Execute_Actions()
		if(!Execute_Actions()) //if the active combo fails a cut, IsComboCutFlag automatically set
			continue;

		//if you manually execute any actions, and it fails a cut, be sure to call:
			//dComboWrapper->Set_IsComboCut(true);

		
		// /**************************************** CUTS  *****************************************/

		// //xcuts
		// //Defining booleans for cuts

	        // 	//************************************* Stage 1 Cuts *************************************************//
		// bool confidenceLevel =  dComboWrapper->Get_ConfidenceLevel_KinFit( "" ) < 1e-4; //Cut to remove tons of data

		// bool showerQuality_Photon1 = false;
		// bool showerQuality_Photon2 = false;
		// bool showerQuality_Photon3 = false;
		// bool showerQuality_Photon4 = false;

		// //// suggested in the FCAL quality paper. This could be studied in detail if needed
		// if( dPhoton1Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		//   showerQuality_Photon1 = dPhoton1Wrapper->Get_Shower_Quality() < .5; 
		
		// if( dPhoton2Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		//   showerQuality_Photon2 = dPhoton2Wrapper->Get_Shower_Quality() < .5;
	        
		// if( dPhoton3Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		//   showerQuality_Photon3 = dPhoton3Wrapper->Get_Shower_Quality() < .5;
	       
		// if( dPhoton4Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		//   showerQuality_Photon4 = dPhoton4Wrapper->Get_Shower_Quality() < .5;

		// bool zVertex =  locProtonX4_Measured.Z()  <  52 || locProtonX4_Measured.Z() > 78; // Usused in other GlueX analysis, it might be the standard

		// bool stage1Cuts = confidenceLevel ||
		// 		  showerQuality_Photon1 ||
		// 		  showerQuality_Photon2 ||
		// 		  showerQuality_Photon3 ||
		// 		  showerQuality_Photon4 ||
		// 		  zVertex;

		// //************************************* Stage 2 Cuts *************************************************//
		// bool deltaTBeam = locBeamDeltaT > 2.|| locBeamDeltaT < -2.;  // ontime
		// //bool deltaTBeam = locBeamDeltaT < 6. && locBeamDeltaT > -6.;  // accidental skip first off-time peak

		// //************************************* Stage 2.1 Cuts *************************************************//

		// //Reducing photon candidates window (Needed for better fits)
		// bool pi0Window =  locPhotons_1_2.M() < .09 ||  locPhotons_1_2.M() > .19;
		// bool etaWindow =  locPhotons_3_4.M() < .4 ||  locPhotons_3_4.M() > .75;

		// bool stage2Cuts = deltaTBeam ||
		// 		  pi0Window ||
		// 		  etaWindow;
		

		// //************************************* Stage 3 Cuts *************************************************//

		// //Removing double pi0 Events
		// //Photons Combos	
		// //This might be redundant!
		// TLorentzVector pi0 = locPhotons_1_2; 
		// double pi0_g1g3 = locPhotons_1_3.M();
		// double pi0_g1g4 = locPhotons_1_4.M();
		// double pi0_g2g3 = locPhotons_2_3.M();
		// double pi0_g2g4 = locPhotons_2_4.M();
		// TLorentzVector eta = locPhotons_3_4;

		// //Fitted values for on-Time Photons
		// double g1g3Mean = (.131 + .135)/2; double g1g3Var = (.0166*.0166 + .0064*.0064)/2;
		// double g2g4Mean = (.130 + .134)/2; double g2g4Var = (.0169*.0169 + .0063*.0063)/2;

		// double g1g4Mean = (.131 + .135)/2; double g1g4Var = (.0171*.0171 + .0064*.0064)/2;
		// double g2g3Mean = (.131 + .134)/2; double g2g3Var = (.0165*.0165 + .0062*.0062)/2;

		// int sigmaNumber = 3;

		// double pi0overlap1 = (pi0_g1g3 - g1g3Mean)*(pi0_g1g3 - g1g3Mean)/(sigmaNumber*sigmaNumber*g1g3Var) + (pi0_g2g4 - g2g4Mean)*(pi0_g2g4 - g2g4Mean)/(sigmaNumber*sigmaNumber*g2g4Var);//ellipse
		// bool pi0Veto1 = pi0overlap1 < 1;

		// double pi0overlap2 = (pi0_g1g4 - g1g4Mean)*(pi0_g1g4 - g1g4Mean)/(sigmaNumber*sigmaNumber*g1g4Var) + (pi0_g2g3 - g2g3Mean)*(pi0_g2g3 - g2g3Mean)/(sigmaNumber*sigmaNumber*g2g3Var);//ellipse
		// bool pi0Veto2 = pi0overlap2 < 1;


		// bool stage3Cuts = pi0Veto1 ||
		// 		  pi0Veto2;	      

		// //************************************* Stage 4 Cuts *************************************************//


		// bool beamEnergy = locBeamP4_Measured.E() < 8.2 || locBeamP4_Measured.E() > 8.8; //Collaboration standard
		// bool missingEnergy =  locMissingP4_Measured.E() < (.115 - 3*.303) || locMissingP4_Measured.E() > (.115 + 3*.303); //Value for this was fitted
		// bool missingMassSquared = locMissingP4_Measured.M2() < -0.04 || locMissingP4_Measured.M2() > 0.04;

		// bool omegaWindow = loc3Pi.M() < .66 || loc3Pi.M() > .9;

		// bool stage4Cuts = beamEnergy ||
		// 		  missingEnergy||
		// 		  missingMassSquared||
		// 		  omegaWindow;

		// //************************************* Stage 5 Cuts *************************************************//

		// bool tOmegaEtaCut = -1*locMomentumTransfer.M2() > .6;

		// bool stage5Cuts = tOmegaEtaCut;

		// //*****************************************************************************************************//
		
		// //Cuts
		// //Stage Cuts 
		// // if( stage1Cuts || stage2Cuts || stage3Cuts || stage4Cuts || stage5Cuts  ){
		// if( stage1Cuts || stage2Cuts || stage3Cuts || stage4Cuts || stage5Cuts ){
		//   dComboWrapper->Set_IsComboCut(true);
		//   continue;
		// }

		//************************************* Stage 6 Cuts *************************************************//
		//extra loop needed to get highest combo CL
		bool single_comboCut = dComboWrapper->Get_ConfidenceLevel_KinFit( "" ) <  combo_cl_max;
		if( single_comboCut ){
		  dComboWrapper->Set_IsComboCut(true);
		  continue;
		}

		/**************************************** EXAMPLE: HISTOGRAM BEAM ENERGY *****************************************/

		//search label: xhist

		//Histogram beam energy
		if(locUsedSoFar_Beam.find( locBeamID ) == locUsedSoFar_Beam.end() ){ 
		  dHist_BeamEnergy->Fill( locBeamP4_Measured.E() );
		  dHist_BeamTiming->Fill( locBeamDeltaT );
		  locUsedSoFar_Beam.insert( locBeamID );
		}

		//Proton
		if(locUsedSoFar_Proton.find( locProtonTrackID ) == locUsedSoFar_Proton.end() ){
		  //Timing
		  if( dProtonWrapper->Get_Detector_System_Timing() == SYS_BCAL )
		    dHist_DeltaTVsP_Proton_BCAL->Fill( locProtonP4_Measured.P(), locProtonDeltaT );  
		  		  
		  if( dProtonWrapper->Get_Detector_System_Timing() == SYS_TOF )
		    dHist_DeltaTVsP_Proton_TOF->Fill( locProtonP4_Measured.P(), locProtonDeltaT );  
		  
		  //CDC dE/dx
		  if( dProtonWrapper->Get_dEdx_CDC() > 0. )
		  dHist_dEdxVsP_Proton_CDC->Fill( locProtonP4_Measured.P(), dProtonWrapper->Get_dEdx_CDC()*1e6 );

		  //Vertex
		  dHist_VertexProtonZ->Fill( locProtonX4_Measured.Z() );
		  dHist_VertexProtonXY->Fill( locProtonX4_Measured.X(), locProtonX4_Measured.Y() );

		  locUsedSoFar_Proton.insert( locProtonTrackID );
		}

		//PiPlus
		if(locUsedSoFar_PiPlus.find( locPiPlusTrackID ) == locUsedSoFar_PiPlus.end() ){

		  if( dPiPlusWrapper->Get_Detector_System_Timing() == SYS_BCAL )
		    dHist_DeltaTVsP_PiP_BCAL->Fill( locPiPlusP4_Measured.P(), locPiPlusDeltaT );  
		  		  
		  if( dPiPlusWrapper->Get_Detector_System_Timing() == SYS_TOF )
		    dHist_DeltaTVsP_PiP_TOF->Fill( locPiPlusP4_Measured.P(), locPiPlusDeltaT );  
		  		  
		  if( dPiPlusWrapper->Get_dEdx_CDC() > 0. )
		    dHist_dEdxVsP_PiP_CDC->Fill( locPiPlusP4_Measured.P(), dPiPlusWrapper->Get_dEdx_CDC()*1e6 );

		  locUsedSoFar_PiPlus.insert( locPiPlusTrackID );
		}

		//PiMinus
		if(locUsedSoFar_PiMinus.find( locPiMinusTrackID ) == locUsedSoFar_PiMinus.end() ){

		  if( dPiMinusWrapper->Get_Detector_System_Timing() == SYS_BCAL )
		    dHist_DeltaTVsP_PiM_BCAL->Fill( locPiMinusP4_Measured.P(), locPiMinusDeltaT );  
		  
		  if( dPiMinusWrapper->Get_Detector_System_Timing() == SYS_TOF )
		    dHist_DeltaTVsP_PiM_TOF->Fill( locPiMinusP4_Measured.P(), locPiMinusDeltaT );  
		  		  
		  if( dPiMinusWrapper->Get_dEdx_CDC() > 0. )
		    dHist_dEdxVsP_PiM_CDC->Fill( locPiMinusP4_Measured.P(), dPiMinusWrapper->Get_dEdx_CDC()*1e6 );

		  locUsedSoFar_PiMinus.insert( locPiMinusTrackID );
		}

		//Photon1
		if( locUsedSoFar_Photon1.find( locPhoton1NeutralID ) == locUsedSoFar_Photon1.end() ){
		 
		  //Timing
		  if( dPhoton1Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		    dHist_DeltaTVsP_Photon_FCAL->Fill( locPhoton1P4_Measured.P(), locPhoton1DeltaT );
		  
		  if( dPhoton1Wrapper->Get_Detector_System_Timing() == SYS_BCAL )
		    dHist_DeltaTVsP_Photon_BCAL->Fill( locPhoton1P4_Measured.P(), locPhoton1DeltaT );
		  
		  //Shower Quality
		  dHist_ShowerQuality1->Fill( dPhoton1Wrapper->Get_Shower_Quality() );
		  
		 locUsedSoFar_Photon1.insert( locPhoton1NeutralID );
		}

		  //Photon2
		  if( locUsedSoFar_Photon2.find( locPhoton2NeutralID ) == locUsedSoFar_Photon2.end() ){

		    //Timing
		    if( dPhoton2Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		      dHist_DeltaTVsP_Photon_FCAL->Fill( locPhoton2P4_Measured.P(), locPhoton2DeltaT );
		  
		    if( dPhoton2Wrapper->Get_Detector_System_Timing() == SYS_BCAL )
		      dHist_DeltaTVsP_Photon_BCAL->Fill( locPhoton2P4_Measured.P(), locPhoton2DeltaT );
		    
		    //Shower Quality
		    dHist_ShowerQuality2->Fill( dPhoton2Wrapper->Get_Shower_Quality() );

		    locUsedSoFar_Photon2.insert( locPhoton2NeutralID );
		  }

		  //Photon3
		  if( locUsedSoFar_Photon3.find( locPhoton3NeutralID ) == locUsedSoFar_Photon3.end() ){
		    
		    //Timing
		    if( dPhoton3Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		      dHist_DeltaTVsP_Photon_FCAL->Fill( locPhoton3P4_Measured.P(), locPhoton3DeltaT );
		    
		    if( dPhoton3Wrapper->Get_Detector_System_Timing() == SYS_BCAL )
		      dHist_DeltaTVsP_Photon_BCAL->Fill( locPhoton3P4_Measured.P(), locPhoton3DeltaT );  
		    
		    //Shower Quality
		    dHist_ShowerQuality3->Fill( dPhoton3Wrapper->Get_Shower_Quality() ); 

		    locUsedSoFar_Photon3.insert( locPhoton3NeutralID );
		  }

		  //Photon4
		  if( locUsedSoFar_Photon4.find( locPhoton4NeutralID ) == locUsedSoFar_Photon4.end() ){

		    //Timing
		    if( dPhoton4Wrapper->Get_Detector_System_Timing() == SYS_FCAL )
		      dHist_DeltaTVsP_Photon_FCAL->Fill( locPhoton4P4_Measured.P(), locPhoton4DeltaT );
		    
		    if( dPhoton4Wrapper->Get_Detector_System_Timing() == SYS_BCAL )
		      dHist_DeltaTVsP_Photon_BCAL->Fill( locPhoton4P4_Measured.P(), locPhoton4DeltaT );
		    
		    //Shower Quality
		    dHist_ShowerQuality4->Fill( dPhoton4Wrapper->Get_Shower_Quality() );      
		    
		    locUsedSoFar_Photon4.insert( locPhoton4NeutralID );
		  }

		/************************************ EXAMPLE: HISTOGRAM MISSING MASS SQUARED ************************************/

		//Uniqueness tracking: Build the map of particles used for the missing mass
		//For beam: Don't want to group with final-state photons. Instead use "Unknown" PID (not ideal, but it's easy).
 		map<Particle_t, set<Int_t> > locUsedThisCombo_AllParticles;
 		locUsedThisCombo_AllParticles[Unknown].insert(locBeamID);
 		locUsedThisCombo_AllParticles[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_AllParticles[PiMinus].insert(locPiMinusTrackID);
 		locUsedThisCombo_AllParticles[Proton].insert(locProtonTrackID);
 		locUsedThisCombo_AllParticles[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_AllParticles[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_AllParticles[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_AllParticles[Gamma].insert(locPhoton4NeutralID);
 		if( locUsedSoFar_AllParticles.find( locUsedThisCombo_AllParticles ) == locUsedSoFar_AllParticles.end() ){

 		  //***************************** Momentum Transfer **********************************//
		  //t omegaEta
		  dHist_t->Fill( -locMomentumTransfer.M2() );
 		  dHist_tprime->Fill( tprime );		  
 		  dHist_tprimeVs4Mass->Fill( loc3piEta.M(), tprime );
 		  dHist_tprimeVs3piMass->Fill( loc3Pi.M(), tprime );
 		  dHist_tprimeVs2piEtaMass->Fill( loc2Pi_Eta.M(), tprime );
 		  dHist_t_omegaEtaVsOmegaEtaMass->Fill( loc3piEta.M(), t_omegaEta );
 		  dHist_t_omegaEtaVsEtaPMass->Fill( locEtaP.M(), t_omegaEta );
 		  dHist_t_omegaEtaVsPi0EtaMass->Fill( locPhotons_1_2_3_4.M(), t_omegaEta );
 		  dHist_t_omegaEtaVsVHAngle->Fill( locVanHovePhi, t_omegaEta );

 		  //t eta
 		  dHist_t_etaVsOmegaEtaMass->Fill( loc3piEta.M(), t_eta );
 		  dHist_t_etaVsEtaPMass->Fill( locEtaP.M(), t_eta );
 		  dHist_t_etaVsPi0EtaMass->Fill( locPhotons_1_2_3_4.M(), t_eta );
 		  dHist_t_etaVsVHAngle->Fill( locVanHovePhi, t_eta ); 

 		  //t omega
 		  dHist_tprime_omega->Fill( tprime_omega );		  
 		  dHist_t_omegaVsOmegaEtaMass->Fill( loc3piEta.M(), t_omega );
 		  dHist_tprime_omegaVsEtaPMass->Fill( locEtaP.M(), tprime_omega );
 		  dHist_t_omegaVsEtaPMass->Fill( locEtaP.M(), t_omega );
 		  dHist_t_omegaVsPi0EtaMass->Fill( locPhotons_1_2_3_4.M(), t_omega );
 		  dHist_t_omegaVsVHAngle->Fill( locVanHovePhi, t_omega );

 		  //t etap
 		  dHist_t_etaPVsOmegaEtaMass->Fill( loc3piEta.M(), t_etaP );
 		  dHist_t_etaPVsEtaPMass->Fill( locEtaP.M(), t_etaP );
 		  dHist_t_etaPVsPi0EtaMass->Fill( locPhotons_1_2_3_4.M(), t_etaP );
 		  dHist_t_etaPVsVHAngle->Fill( locVanHovePhi, t_etaP );

 		  //t omegap
 		  dHist_t_omegaPVsOmegaEtaMass->Fill( loc3piEta.M(), t_omegaP );
 		  dHist_t_omegaPVsEtaPMass->Fill( locEtaP.M(), t_omegaP );
 		  dHist_t_omegaPVsPi0EtaMass->Fill( locPhotons_1_2_3_4.M(), t_omegaP );
 		  dHist_t_omegaPVsVHAngle->Fill( locVanHovePhi, t_omegaP );

 		  //t proton
 		  dHist_t_pVsOmegaEtaMass->Fill( loc3piEta.M(), t_proton );
 		  dHist_t_pVsEtaPMass->Fill( locEtaP.M(), t_proton );
 		  dHist_t_pVsPi0EtaMass->Fill( locPhotons_1_2_3_4.M(), t_proton );
 		  dHist_t_pVsVHAngle->Fill( locVanHovePhi, t_proton );

		  //***************************************************************************************//

 		  //Missing Mass/Energy
 		  dHist_MissingMassSquared->Fill( locMissingP4_Measured.M2() );
 		  dHist_MissingEnergy->Fill( locMissingP4_Measured.E() );

		  dHist_MEvsUS->Fill( dComboWrapper->Get_Energy_UnusedShowers(), locMissingP4_Measured.E() );

		  //Confidence Level
		  dHist_logCL->Fill( log10(dComboWrapper->Get_ConfidenceLevel_KinFit( "" )) );
		  dHist_CLsimple->Fill( dComboWrapper->Get_ConfidenceLevel_KinFit( "" ));
 		  dHist_ConfidenceLevel_logX->Fill( dComboWrapper->Get_ConfidenceLevel_KinFit( "" ) );
 		  dHist_VertexVsConfidenceLevel_logX->Fill( dComboWrapper->Get_ConfidenceLevel_KinFit( "" ), locProtonX4_Measured.Z() );
 		  dHist_MMSVsConfidenceLevel_logX->Fill( dComboWrapper->Get_ConfidenceLevel_KinFit( "" ), locMissingP4_Measured.M2() );
 		  dHist_MEVsConfidenceLevel_logX->Fill( dComboWrapper->Get_ConfidenceLevel_KinFit( "" ), locMissingP4_Measured.E() );
 		  dHist_ChiSq->Fill( dComboWrapper->Get_ChiSq_KinFit( "" ) );
 		  dHist_ChiSqVsConfidenceLevel_logX->Fill( dComboWrapper->Get_ConfidenceLevel_KinFit( "" ) , dComboWrapper->Get_ChiSq_KinFit( "" ) );

 		  ///Angles
 		  //GJ
 		  dHist_etaGJcos->Fill( etaCosGJ );
 		  dHist_etaGJphi->Fill( etaPhiGJ );
 		  dHist_etaPhivsMass->Fill( loc3piEta.M(), etaPhiGJ );
 		  dHist_etaCosvsMass->Fill( loc3piEta.M(), etaCosGJ );
	
 		  dHist_3piGJcos->Fill(  threePiCosGJ );
 		  dHist_3piGJphi->Fill(  threePiPhiGJ );
 		  dHist_3piPhivsMass->Fill( loc3piEta.M(), threePiPhiGJ ); 
 		  dHist_3piCosvsMass->Fill( loc3piEta.M(), threePiCosGJ );

		  dHist_3piPhivsVHAngle->Fill( locVanHovePhi, threePiPhiGJ ); 
 		  dHist_3piCosvsVHAngle->Fill( locVanHovePhi, threePiCosGJ );
		  
 		  dHist_GJcosVs3pi->Fill( loc3Pi.M(), threePiCosGJ );
 		  dHist_GJphiVs3pi->Fill( loc3Pi.M(), threePiPhiGJ );

 		  dHist_pi0GJcos->Fill( pi0CosGJ );
 		  dHist_pi0GJphi->Fill( pi0PhiGJ );

 		  dHist_piPlusGJcos->Fill( piPlusCosGJ );
 		  dHist_piPlusGJphi->Fill( piPlusPhiGJ );

 		  dHist_piMinusGJcos->Fill( piMinusCosGJ );
 		  dHist_piMinusGJphi->Fill( piMinusPhiGJ );

 		  dHist_3piCosvsProtonEtaMass->Fill( locEtaP.M(), etaGJ3V.CosTheta() );

		  //He 1
		  dHist_he1cos->Fill( threePiCosHe_1 );
		  dHist_he1phi->Fill( threePiPhiHe_1 );
		  
		  //He 2
		  dHist_he2cos->Fill( theta_he_2 );
		  dHist_he2phi->Fill( phi_he_2 );


		  //Smaller selection
		  bool PWA_selection = -1*locMomentumTransfer.M2() < .3;
		  if(PWA_selection){
		    //He 1
		    dHist_he1cosNarrow->Fill( threePiCosHe_1 );
		    dHist_he1phiNarrow->Fill( threePiPhiHe_1 );
		  
		    //He 2
		    dHist_he2cosNarrow->Fill( theta_he_2 );
		    dHist_he2phiNarrow->Fill( phi_he_2 );
		  }

 		  //CM
 		  dHist_etaCMcos->Fill( etaCosCM );
 		  dHist_etaCMphi->Fill( etaPhiCM );
		  	
 		  dHist_3piCMcos->Fill( threePiCosCM );
 		  dHist_3piCMphi->Fill( threePiPhiCM );		 

 		  dHist_CMcosVs3pi->Fill( loc3Pi.M(), threePiCosCM );
 		  dHist_CMphiVs3pi->Fill( loc3Pi.M(), threePiPhiCM );		 

 		  dHist_etaPhiCMvsMassEtaP->Fill( locEtaP.M(), etaPhiCM );
 		  dHist_3piCosCMvsProtonEtaMass->Fill( locEtaP.M(), threePiCosCM );

 		  dHist_pi0CMcos->Fill( pi0CosCM );
 		  dHist_pi0CMphi->Fill( pi0PhiCM );

 		  dHist_piPlusCMcos->Fill( piPlusCosCM );
 		  dHist_piPlusCMphi->Fill( piPlusPhiCM );

 		  dHist_piMinusCMcos->Fill( piMinusCosCM );
 		  dHist_piMinusCMphi->Fill( piMinusPhiCM );

 		  //LAB
 		  dHist_etaLABcos->Fill( etaCosLAB );
 		  dHist_etaLABphi->Fill( etaPhiLAB );
		  	
 		  dHist_3piLABcos->Fill( threePiCosLAB );
 		  dHist_3piLABphi->Fill( threePiPhiLAB );

 		  dHist_LABcosVs3pi->Fill( loc3Pi.M(), threePiCosLAB );
 		  dHist_LABphiVs3pi->Fill( loc3Pi.M(), threePiPhiLAB );		 

 		  dHist_pi0LABcos->Fill( pi0CosLAB );
 		  dHist_pi0LABphi->Fill( pi0PhiLAB );

 		  dHist_piPlusLABcos->Fill( piPlusCosLAB );
 		  dHist_piPlusLABphi->Fill( piPlusPhiLAB );

 		  dHist_piMinusLABcos->Fill( piMinusCosLAB );
 		  dHist_piMinusLABphi->Fill( piMinusPhiLAB );

 		  dHist_protonLABcos->Fill( protonCosLAB );
 		  dHist_protonLABphi->Fill( protonPhiLAB );

		  //dHist_alpha->Fill(alpha); // what was this for?

 		  //VanHove
 		  dHist_VanHove3->Fill( vHX, vHY );
 		  dHist_MomentumIsobar->Fill(vH_proton.Pz(),vH_eta.Pz());//(eta_ISO.Pz(),proton_ISO.Pz()); // Need to revise that this is
 		  // dHist_rhoIsobar->Fill(rho);

		
 		  //Kin test 
 		  dHist_VanHoveAngleVsM3pi->Fill( loc3Pi.M(), locVanHovePhi );
 		  dHist_VanHoveAngleVsMeta->Fill( locPhotons_3_4_Measured.M(), locVanHovePhi );
 		  dHist_VanHoveAngleVsMomegaEta->Fill( loc3piEta.M(), locVanHovePhi );
 		  dHist_VanHoveAngleVsMprotonEta->Fill( locEtaP.M(), locVanHovePhi );
 		  dHist_VanHoveAngleVsCosCMEta->Fill( etaCosCM, locVanHovePhi);
 		  dHist_etaCosCMvsMassEtaP->Fill( locEtaP.M(), etaCosCM );
 		  dHist_etaCosCMvsOmegaEtaMass->Fill( loc3piEta.M(), etaCosCM );

        
		  //Unused Shower Energy
		  dHist_UnusedShowerEnergy->Fill( dComboWrapper->Get_Energy_UnusedShowers() );
		  dHist_UnusedShowerNumber->Fill( dComboWrapper->Get_NumUnusedShowers());// It's not affetted by cuts


 		  locUsedSoFar_AllParticles.insert( locUsedThisCombo_AllParticles );
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_Photons_1_2;
 		locUsedThisCombo_Photons_1_2[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_Photons_1_2[Gamma].insert(locPhoton2NeutralID);
 		if(locUsedSoFar_Photons_1_2.find(locUsedThisCombo_Photons_1_2) == locUsedSoFar_Photons_1_2.end()){
 		  //Mass
 		  dHist_Mass_g1_g2_M->Fill( locPhotons_1_2_Measured.M() );
 		  dHist_Mass_g1_g2->Fill( locPhotons_1_2.M() );
 		  //Mass Vs Unused Shower Energy
 		  dHist_MassPi0_MvsUS->Fill( dComboWrapper->Get_Energy_UnusedShowers(), locPhotons_1_2_Measured.M() );
 		  locUsedSoFar_Photons_1_2.insert(locUsedThisCombo_Photons_1_2);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_Photons_1_3;
 		locUsedThisCombo_Photons_1_3[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_Photons_1_3[Gamma].insert(locPhoton3NeutralID);
 		if(locUsedSoFar_Photons_1_3.find(locUsedThisCombo_Photons_1_3) == locUsedSoFar_Photons_1_3.end()){
 		  //Mass
 		  dHist_Mass_g1_g3_M->Fill( locPhotons_1_3_Measured.M() );
 		  dHist_Mass_g1_g3->Fill( locPhotons_1_3.M() );
 		  locUsedSoFar_Photons_1_3.insert(locUsedThisCombo_Photons_1_3);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_Photons_1_4;
 		locUsedThisCombo_Photons_1_4[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_Photons_1_4[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_Photons_1_4.find(locUsedThisCombo_Photons_1_4) == locUsedSoFar_Photons_1_4.end()){
 		  //Mass
 		  dHist_Mass_g1_g4_M->Fill( locPhotons_1_4_Measured.M() );
 		  dHist_Mass_g1_g4->Fill( locPhotons_1_4.M() );
 		  locUsedSoFar_Photons_1_4.insert(locUsedThisCombo_Photons_1_4);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_Photons_2_3;
 		locUsedThisCombo_Photons_2_3[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_Photons_2_3[Gamma].insert(locPhoton3NeutralID);
 		if(locUsedSoFar_Photons_2_3.find(locUsedThisCombo_Photons_2_3) == locUsedSoFar_Photons_2_3.end()){
 		  //Mass
 		  dHist_Mass_g2_g3_M->Fill( locPhotons_2_3_Measured.M() );
 		  dHist_Mass_g2_g3->Fill( locPhotons_2_3.M() );
 		  locUsedSoFar_Photons_2_3.insert(locUsedThisCombo_Photons_2_3);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_Photons_2_4;
 		locUsedThisCombo_Photons_2_4[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_Photons_2_4[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_Photons_2_4.find(locUsedThisCombo_Photons_2_4) == locUsedSoFar_Photons_2_4.end()){
 		  //Mass
 		  dHist_Mass_g2_g4_M->Fill( locPhotons_2_4_Measured.M() );
 		  dHist_Mass_g2_g4->Fill( locPhotons_2_4.M() );
 		  locUsedSoFar_Photons_2_4.insert(locUsedThisCombo_Photons_2_4);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_Photons_3_4;
 		locUsedThisCombo_Photons_3_4[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_Photons_3_4[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_Photons_3_4.find(locUsedThisCombo_Photons_3_4) == locUsedSoFar_Photons_3_4.end()){
 		  //Mass
 		  dHist_Mass_g3_g4_M->Fill( locPhotons_3_4_Measured.M() );
 		  dHist_Mass_g3_g4->Fill( locPhotons_3_4.M() );
 		  //Mass Vs Unused Shower Energy
 		  dHist_MassEtavsUS->Fill( dComboWrapper->Get_Energy_UnusedShowers(), locPhotons_3_4_Measured.M() );
		  locUsedSoFar_Photons_3_4.insert(locUsedThisCombo_Photons_3_4);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_3Photons1;
 		locUsedThisCombo_3Photons1[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_3Photons1[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_3Photons1[Gamma].insert(locPhoton3NeutralID);
 		if(locUsedSoFar_3Photons1.find(locUsedThisCombo_3Photons1) == locUsedSoFar_3Photons1.end()){
 		  //3 Photons
 		  dHist_Mass_g1_g2_g3->Fill(locPhotons_1_2_3.M());
 		  locUsedSoFar_3Photons1.insert(locUsedThisCombo_3Photons1);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_3Photons2;
 		locUsedThisCombo_3Photons2[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_3Photons2[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_3Photons2[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_3Photons2.find(locUsedThisCombo_3Photons2) == locUsedSoFar_3Photons2.end()){
 		  //3 Photons
 		  dHist_Mass_g1_g2_g4->Fill(locPhotons_1_2_4.M());		  
 		  locUsedSoFar_3Photons2.insert(locUsedThisCombo_3Photons2);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_3Photons3;
 		locUsedThisCombo_3Photons3[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_3Photons3[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_3Photons3[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_3Photons3.find(locUsedThisCombo_3Photons3) == locUsedSoFar_3Photons3.end()){
 		  //3 Photons
 		  dHist_Mass_g1_g3_g4->Fill(locPhotons_1_3_4.M()); 
 		  locUsedSoFar_3Photons3.insert(locUsedThisCombo_3Photons3);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_3Photons4;
 		locUsedThisCombo_3Photons4[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_3Photons4[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_3Photons4[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_3Photons4.find(locUsedThisCombo_3Photons4) == locUsedSoFar_3Photons4.end()){
 		  //3 Photons
 		  dHist_Mass_g2_g3_g4->Fill(locPhotons_2_3_4.M());
 		  locUsedSoFar_3Photons4.insert(locUsedThisCombo_3Photons4);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_4Photons;
 		locUsedThisCombo_4Photons[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_4Photons[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_4Photons[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_4Photons[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_4Photons.find(locUsedThisCombo_4Photons) == locUsedSoFar_4Photons.end()){
 		  dHist_g1g2vsg3g4_M->Fill( locPhotons_3_4_Measured.M(), locPhotons_1_2_Measured.M() );
 		  dHist_g1g3vsg2g4_M->Fill( locPhotons_2_4_Measured.M(), locPhotons_1_3_Measured.M() );
 		  dHist_g1g4vsg2g3_M->Fill( locPhotons_2_3_Measured.M(), locPhotons_1_4_Measured.M() );

 		  dHist_g1g2vsg3g4->Fill( locPhotons_3_4.M(), locPhotons_1_2.M() );
 		  dHist_g1g3vsg2g4->Fill( locPhotons_2_4.M(), locPhotons_1_3.M() );
 		  dHist_g1g4vsg2g3->Fill( locPhotons_2_3.M(), locPhotons_1_4.M() );

 		  dHist_Mass_g1_g2_g3_g4->Fill(locPhotons_1_2_3_4.M());

 		  dHist_MassPi0Eta->Fill( locPi0Eta.M());

 		  locUsedSoFar_4Photons.insert(locUsedThisCombo_4Photons);
 		}


 		//Baryons
 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPipP;
 		locUsedThisCombo_MassPipP[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_MassPipP[Proton].insert(locProtonTrackID);
       		if(locUsedSoFar_MassPipP.find(locUsedThisCombo_MassPipP) == locUsedSoFar_MassPipP.end()){
 		   dHist_MassPipP->Fill( locPipP.M());
 		  locUsedSoFar_MassPipP.insert(locUsedThisCombo_MassPipP);
 		}
	
 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPimP;
 		locUsedThisCombo_MassPimP[PiMinus].insert(locPiMinusTrackID);
 		locUsedThisCombo_MassPimP[Proton].insert(locProtonTrackID);
       		if(locUsedSoFar_MassPimP.find(locUsedThisCombo_MassPimP) == locUsedSoFar_MassPimP.end()){
 		   dHist_MassPimP->Fill( locPimP.M());
 		  locUsedSoFar_MassPimP.insert(locUsedThisCombo_MassPimP);
 		}
	
 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPi0P;
 		locUsedThisCombo_MassPi0P[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_MassPi0P[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_MassPi0P[Proton].insert(locProtonTrackID);
       		if(locUsedSoFar_MassPi0P.find(locUsedThisCombo_MassPi0P) == locUsedSoFar_MassPi0P.end()){
 		   dHist_MassPi0P->Fill( locPi0P.M());
 		  locUsedSoFar_MassPi0P.insert(locUsedThisCombo_MassPi0P);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassEtaP;
 		locUsedThisCombo_MassPi0P[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_MassPi0P[Gamma].insert(locPhoton4NeutralID);
 		locUsedThisCombo_MassEtaP[Proton].insert(locProtonTrackID);
       		if(locUsedSoFar_MassEtaP.find(locUsedThisCombo_MassEtaP) == locUsedSoFar_MassEtaP.end()){
 		  dHist_MassEtaP->Fill( locEtaP.M());
 		  locUsedSoFar_MassEtaP.insert(locUsedThisCombo_MassEtaP);
 		}

 		//Mesons
 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPipPim;
 		locUsedThisCombo_MassPipPim[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_MassPipPim[PiMinus].insert(locPiMinusTrackID);
       		if(locUsedSoFar_MassPipPim.find(locUsedThisCombo_MassPipPim) == locUsedSoFar_MassPipPim.end()){
 		   dHist_MassPipPim->Fill( locPipPim.M());
 		  locUsedSoFar_MassPipPim.insert(locUsedThisCombo_MassPipPim);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPipPi0;
 		locUsedThisCombo_MassPipPi0[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_MassPipPi0[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_MassPipPi0[Gamma].insert(locPhoton2NeutralID);
 		if(locUsedSoFar_MassPipPi0.find(locUsedThisCombo_MassPipPi0) == locUsedSoFar_MassPipPi0.end()){
 		  dHist_MassPipPi0->Fill( locPipPi0.M());
 		  locUsedSoFar_MassPipPi0.insert(locUsedThisCombo_MassPipPi0);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPipEta;
 		locUsedThisCombo_MassPipEta[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_MassPipEta[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_MassPipEta[Gamma].insert(locPhoton4NeutralID);	
    		if(locUsedSoFar_MassPipEta.find(locUsedThisCombo_MassPipEta) == locUsedSoFar_MassPipEta.end()){
 		  dHist_MassPipEta->Fill( locPipEta.M());
 		  locUsedSoFar_MassPipEta.insert(locUsedThisCombo_MassPipEta);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPimPi0;
 		locUsedThisCombo_MassPimPi0[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_MassPimPi0[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_MassPimPi0[Gamma].insert(locPhoton2NeutralID);	  
  		if(locUsedSoFar_MassPimPi0.find(locUsedThisCombo_MassPimPi0) == locUsedSoFar_MassPimPi0.end()){
 		  dHist_MassPimPi0->Fill( locPimPi0.M());
 		  locUsedSoFar_MassPimPi0.insert(locUsedThisCombo_MassPimPi0);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_MassPimEta;
 		locUsedThisCombo_MassPimEta[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_MassPimEta[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_MassPimEta[Gamma].insert(locPhoton4NeutralID);
 		if(locUsedSoFar_MassPimEta.find(locUsedThisCombo_MassPimEta) == locUsedSoFar_MassPimEta.end()){
 		  dHist_MassPimEta->Fill( locPimEta.M());
 		  locUsedSoFar_MassPimEta.insert(locUsedThisCombo_MassPimEta);
 		}

 		//3pi
 		map<Particle_t, set<Int_t> > locUsedThisCombo_3piMass;
 		locUsedThisCombo_3piMass[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_3piMass[PiMinus].insert(locPiMinusTrackID);
 		locUsedThisCombo_3piMass[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_3piMass[Gamma].insert(locPhoton2NeutralID);
       		if(locUsedSoFar_3piMass.find(locUsedThisCombo_3piMass) == locUsedSoFar_3piMass.end()){
 		  //Measured
 		  dHist_Mass3pi->Fill( loc3Pi_Measured.M());
 		  dHist_3pivsg3g4_M->Fill( locPhotons_3_4_Measured.M(), loc3Pi_Measured.M() );
 		  //KinFit
 		  dHist_Mass3pi_KinFit->Fill( loc3Pi.M());
 		  dHist_3pivsg3g4->Fill( locPhotons_3_4.M(), loc3Pi.M() );

 		  //Lambda 
 		  if( loc3Pi.M() > .74 && loc3Pi.M() < .84)
 		    dHist_lambdaOmega->Fill( ratioLambda );
		    
 		  //low sideband
 		  if( loc3Pi.M() > .68 && loc3Pi.M() < .73)
 		    dHist_lambdaLowSideband->Fill( ratioLambda );

 		  //high sideband
 		  if( loc3Pi.M() > .85 && loc3Pi.M() < .9)
 		    dHist_lambdaHighSideband->Fill( ratioLambda );

 		  locUsedSoFar_3piMass.insert(locUsedThisCombo_3piMass);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_2piEtaMass;
 		locUsedThisCombo_2piEtaMass[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_2piEtaMass[PiMinus].insert(locPiMinusTrackID);
 		locUsedThisCombo_2piEtaMass[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_2piEtaMass[Gamma].insert(locPhoton4NeutralID);
       		if(locUsedSoFar_2piEtaMass.find(locUsedThisCombo_2piEtaMass) == locUsedSoFar_2piEtaMass.end()){
 		  //Measured
 		  dHist_Mass2pi_eta->Fill( loc2Pi_Eta_Measured.M());
 		  //KinFit
 		  dHist_Mass2pi_eta_KinFit->Fill( loc2Pi_Eta.M());

 		  //Dalitz //Decide on the mass window size
		  dHist_dalitz2PiEta->Fill( locPipEta.M2(), locPimEta.M2() );
 		  locUsedSoFar_2piEtaMass.insert(locUsedThisCombo_2piEtaMass);
 		}

 		//3PiEta
 		map<Particle_t, set<Int_t> > locUsedThisCombo_3piEtaMass;
 		locUsedThisCombo_3piEtaMass[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_3piEtaMass[PiMinus].insert(locPiMinusTrackID);
 		locUsedThisCombo_3piEtaMass[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_3piEtaMass[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_3piEtaMass[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_3piEtaMass[Gamma].insert(locPhoton4NeutralID);
       		if(locUsedSoFar_3piEtaMass.find(locUsedThisCombo_3piEtaMass) == locUsedSoFar_3piEtaMass.end()){
 		  ////////////////////////  Measured ////////////////////////
 		  dHist_Mass3piEta->Fill( loc3piEta_Measured.M() );
 		  dHist_Mass3pivs2piEta->Fill( loc2Pi_Eta_Measured.M(),loc3Pi_Measured.M() );
 		  if( loc3Pi_Measured.M() > .74 && loc3Pi_Measured.M() < .84 ){
 		    dHist_MassOmegaEta->Fill( loc3piEta_Measured.M() );
 		  }
		  
 		  dHist_OmegaEtavsEtaP->Fill( locEtaP_Measured.M(), loc3piEta_Measured.M() ); //not sure if this one goes here becuse of the proton
 		  dHist_MassOmegaP->Fill( locOmegaP.M() );

		  ////////
		  //Omega vs Eta Momentum
 		  dHist_omegavsEta->Fill(  (locPhotons_3_4.Vect()).Mag(), (loc3Pi.Vect()).Mag() );

 		  //////////////////////// KinFit ////////////////////////
 		  dHist_Mass3piEta_KinFit->Fill( loc3piEta.M());
 		  dHist_Mass3pivs2piEta_KinFit->Fill( loc2Pi_Eta.M(), loc3Pi.M() );

 		  if( loc3Pi.M() > .74 && loc3Pi.M() < .84 )
 		    dHist_MassOmegaEta_KinFit->Fill( loc3piEta.M() );

 		  //Meson vs Meson
 		  dHist_pipPimvspi0Eta->Fill( locPi0Eta.M(), locPipPim.M() );
 		  dHist_pipPi0vspimEta->Fill( locPimEta.M(), locPipPi0.M() );
 		  dHist_pipEtavspimPi0->Fill( locPimPi0.M(), locPipEta.M() );

	
 		  locUsedSoFar_3piEtaMass.insert(locUsedThisCombo_3piEtaMass);
 		}

 		map<Particle_t, set<Int_t> > locUsedThisCombo_5Particles;
 		locUsedThisCombo_5Particles[PiPlus].insert(locPiPlusTrackID);
 		locUsedThisCombo_5Particles[PiMinus].insert(locPiMinusTrackID);
 		locUsedThisCombo_5Particles[Proton].insert(locProtonTrackID);
 		locUsedThisCombo_5Particles[Gamma].insert(locPhoton1NeutralID);
 		locUsedThisCombo_5Particles[Gamma].insert(locPhoton2NeutralID);
 		locUsedThisCombo_5Particles[Gamma].insert(locPhoton3NeutralID);
 		locUsedThisCombo_5Particles[Gamma].insert(locPhoton4NeutralID);
 		if( locUsedSoFar_5Particles.find( locUsedThisCombo_5Particles ) == locUsedSoFar_5Particles.end() ){

 		  dHist_pipPvspimPi0->Fill( locPimPi0.M(), locPipP.M() );
 		  dHist_pipPvspimEta->Fill( locPimEta.M(), locPipP.M() );
 		  dHist_pipPvspi0Eta->Fill( locPi0Eta.M(), locPipP.M() );

 		  dHist_pimPvspipPi0->Fill( locPipPi0.M(), locPimP.M() );
 		  dHist_pimPvspipEta->Fill( locPipEta.M(), locPimP.M() );
 		  dHist_pimPvspi0Eta->Fill( locPi0Eta.M(), locPimP.M() );

 		  dHist_pi0PvspipPim->Fill( locPipPim.M(), locPi0P.M() );
 		  dHist_pi0PvspipEta->Fill( locPipEta.M(), locPi0P.M() );
 		  dHist_pi0PvspimEta->Fill( locPimEta.M(), locPi0P.M() );

 		  dHist_etaPvspipPim->Fill( locPipPim.M(), locEtaP.M() );
 		  dHist_etaPvspipPi0->Fill( locPipPi0.M(), locEtaP.M() );
 		  dHist_etaPvspimPi0->Fill( locPimPi0.M(), locEtaP.M() );

 		  locUsedSoFar_5Particles.insert( locUsedThisCombo_5Particles );
 		}

		++comboNumber;
        		
		//Number Of particles
		NumberOfPhotons.insert(locPhoton1NeutralID);
		NumberOfPhotons.insert(locPhoton2NeutralID);
		NumberOfPhotons.insert(locPhoton3NeutralID);
		NumberOfPhotons.insert(locPhoton4NeutralID);
		NumberOfProtons.insert(locProtonTrackID);
		NumberOfPiPlus.insert(locPiPlusTrackID);
		NumberOfPiMinus.insert(locPiMinusTrackID);
		NumberOfBeam.insert(locBeamID);

		dHist_NeutralHypoNumber->Fill( Get_NumNeutralHypos() );

	} // end of combo loop

	//FILL HISTOGRAMS: Num combos / events surviving actions
	Fill_NumCombosSurvivedHists();

	//xCounting   
	dHist_PhotonNumber->Fill( NumberOfPhotons.size() );
	dHist_ProtonNumber->Fill( NumberOfProtons.size() );
	dHist_PipNumber->Fill( NumberOfPiPlus.size() );
	dHist_PimNumber->Fill( NumberOfPiMinus.size() );
	dHist_ComboNumber->Fill( comboNumber );
	dHist_BeamNumber->Fill( NumberOfBeam.size() );

	/******************************************* LOOP OVER THROWN DATA (OPTIONAL) ***************************************/
/*
	//Thrown beam: just use directly
	if(dThrownBeam != NULL)
		double locEnergy = dThrownBeam->Get_P4().E();

	//Loop over throwns
	for(UInt_t loc_i = 0; loc_i < Get_NumThrown(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dThrownWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}
*/
	/****************************************** LOOP OVER OTHER ARRAYS (OPTIONAL) ***************************************/
/*
	//Loop over beam particles (note, only those appearing in combos are present)
	for(UInt_t loc_i = 0; loc_i < Get_NumBeam(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dBeamWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}

	//Loop over charged track hypotheses
	for(UInt_t loc_i = 0; loc_i < Get_NumChargedHypos(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dChargedHypoWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}

	//Loop over neutral particle hypotheses
	for(UInt_t loc_i = 0; loc_i < Get_NumNeutralHypos(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dNeutralHypoWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
	}
*/

	/************************************ EXAMPLE: FILL CLONE OF TTREE HERE WITH CUTS APPLIED ************************************/
/*
	Bool_t locIsEventCut = true;
	for(UInt_t loc_i = 0; loc_i < Get_NumCombos(); ++loc_i) {
		//Set branch array indices for combo and all combo particles
		dComboWrapper->Set_ComboIndex(loc_i);
		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut())
			continue;
		locIsEventCut = false; // At least one combo succeeded
		break;
	}
	if(!locIsEventCut && dOutputTreeFileName != "")
		Fill_OutputTree();
*/

	return kTRUE;
}

void DSelector_omegaEta::Finalize(void)
{
	//Save anything to output here that you do not want to be in the default DSelector output ROOT file.

	//Otherwise, don't do anything else (especially if you are using PROOF).
		//If you are using PROOF, this function is called on each thread,
		//so anything you do will not have the combined information from the various threads.
		//Besides, it is best-practice to do post-processing (e.g. fitting) separately, in case there is a problem.

	//DO YOUR STUFF HERE

	//CALL THIS LAST
	DSelector::Finalize(); //Saves results to the output file
}
