// This DSelector was made from a file similar to this, in the same directory:
// /lustre19/expphy/cache/halld/RunPeriod-2018-08/analysis/ver23/tree_pi0kplamb__B4_M18/merged/tree_pi0kplamb__B4_M18_051730.root
// The purpose is to investigate the pi0kplamb final state reported in this article:
// https://halldweb.jlab.org/analysis/pdf/RunPeriod-2018-08/ver10/tree_pi0kplamb.pdf

#include "DSelector_pi0kplamb_flat.h"

void DSelector_pi0kplamb_flat::Init(TTree *locTree)
{
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = ""; //"" for none
	dOutputTreeFileName = ""; //"" for none
	dFlatTreeFileName = "pi0kplamb_flat_2018_08.root"; //output flat tree (one combo per tree entry), "" for none
	dFlatTreeName = "pi0kplamb_flat"; //if blank, default name will be chosen
	dSaveDefaultFlatBranches = false; // False: don't save default branches, reduce disk footprint.
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

	// EXAMPLE: Create deque for histogramming particle masses:
	// // For histogramming the phi mass in phi -> K+ K-
	// // Be sure to change this and dAnalyzeCutActions to match reaction
	std::deque<Particle_t> MyPhi;
	MyPhi.push_back(KPlus); MyPhi.push_back(Pi0); MyPhi.push_back(Lambda);

	//ANALYSIS ACTIONS: //Executed in order if added to dAnalysisActions
	//false/true below: use measured/kinfit data

	//PID
	dAnalysisActions.push_back(new DHistogramAction_ParticleID(dComboWrapper, false));
	//below: value: +/- N ns, Unknown: All PIDs, SYS_NULL: all timing systems
	//dAnalysisActions.push_back(new DCutAction_PIDDeltaT(dComboWrapper, false, 0.5, KPlus, SYS_BCAL));

	//PIDFOM (for charged tracks)
	dAnalysisActions.push_back(new DHistogramAction_PIDFOM(dComboWrapper));
	//dAnalysisActions.push_back(new DCutAction_PIDFOM(dComboWrapper, KPlus, 0.1));
	//dAnalysisActions.push_back(new DCutAction_EachPIDFOM(dComboWrapper, 0.1));

	//MASSES
	//dAnalysisActions.push_back(new DHistogramAction_InvariantMass(dComboWrapper, false, Lambda, 1000, 1.0, 1.2, "Lambda"));
	//dAnalysisActions.push_back(new DHistogramAction_MissingMassSquared(dComboWrapper, false, 1000, -0.1, 0.1));

	//KINFIT RESULTS
	dAnalysisActions.push_back(new DHistogramAction_KinFitResults(dComboWrapper));

	//CUT MISSING MASS
	//dAnalysisActions.push_back(new DCutAction_MissingMassSquared(dComboWrapper, false, -0.03, 0.02));

	//CUT ON SHOWER QUALITY
	//dAnalysisActions.push_back(new DCutAction_ShowerQuality(dComboWrapper, SYS_FCAL, 0.5));

	//BEAM ENERGY
	dAnalysisActions.push_back(new DHistogramAction_BeamEnergy(dComboWrapper, false));
	//dAnalysisActions.push_back(new DCutAction_BeamEnergy(dComboWrapper, false, 8.2, 8.8));  // Coherent peak for runs in the range 30000-59999

	//KINEMATICS
	dAnalysisActions.push_back(new DHistogramAction_ParticleComboKinematics(dComboWrapper, false));

	// ANALYZE CUT ACTIONS
	// // Change MyPhi to match reaction
	dAnalyzeCutActions = new DHistogramAction_AnalyzeCutActions( dAnalysisActions, dComboWrapper, false, 0, MyPhi, 1000, 0.9, 2.4, "CutActionEffect" );

	//INITIALIZE ACTIONS
	//If you create any actions that you want to run manually (i.e. don't add to dAnalysisActions), be sure to initialize them here as well
	Initialize_Actions();
	dAnalyzeCutActions->Initialize(); // manual action, must call Initialize()

	/******************************** EXAMPLE USER INITIALIZATION: STAND-ALONE HISTOGRAMS *******************************/

	//EXAMPLE MANUAL HISTOGRAMS:
	dHist_MissingMassSquared = new TH1I("MissingMassSquared", ";Missing Mass Squared (GeV/c^{2})^{2}", 600, -0.06, 0.06);
	dHist_BeamEnergy = new TH1I("BeamEnergy", ";Beam Energy (GeV)", 600, 0.0, 12.0);

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("beam_e");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("beam_e_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_m_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_m2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kp_m2_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("decayingPi0_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("decayingPi0_m2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon1_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon1_E_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon1_p");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon1_p_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon2_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon2_E_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon2_p");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("photon2_p_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_m_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_m2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_m2_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("protonRecoil_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("protonRecoil_m_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("protonRecoil_m2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("protonRecoil_m2_measured");

	// combined masses or energies
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDPi0_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDPi0_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDphoton1_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDphoton1_E_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDphoton2_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDphoton2_E_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDlambda_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDlambda_m_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDlambda_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDproton_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDproton_m_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDpim_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kpANDpim_m_measured");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pi0ANDlambda_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pi0ANDproton_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pi0ANDpim_m");

	// dEdx values. Energy loss per distance traveled.  Bethe-Bloch formula.
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("dEdx_cdc_kplus");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("dEdx_fdc_kplus");

	// Mandelstam variables: momentum transfer (t), COM frame energy (s).
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("t");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("t0");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("tPrime");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("s");



	/************************** EXAMPLE USER INITIALIZATION: CUSTOM OUTPUT BRANCHES - MAIN TREE *************************/

	//EXAMPLE MAIN TREE CUSTOM BRANCHES (OUTPUT ROOT FILE NAME MUST FIRST BE GIVEN!!!! (ABOVE: TOP)):
	//The type for the branch must be included in the brackets
	//1st function argument is the name of the branch
	//2nd function argument is the name of the branch that contains the size of the array (for fundamentals only)
	/*
	dTreeInterface->Create_Branch_Fundamental<Int_t>("my_int"); //fundamental = char, int, float, double, etc.
	dTreeInterface->Create_Branch_FundamentalArray<Int_t>("my_int_array", "my_int");
	dTreeInterface->Create_Branch_FundamentalArray<Float_t>("my_combo_array", "NumCombos");
	dTreeInterface->Create_Branch_NoSplitTObject<TLorentzVector>("my_p4");
	dTreeInterface->Create_Branch_ClonesArray<TLorentzVector>("my_p4_array");
	*/

	/************************** EXAMPLE USER INITIALIZATION: CUSTOM OUTPUT BRANCHES - FLAT TREE *************************/

	// RECOMMENDED: CREATE ACCIDENTAL WEIGHT BRANCH
	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("accidweight");

	//EXAMPLE FLAT TREE CUSTOM BRANCHES (OUTPUT ROOT FILE NAME MUST FIRST BE GIVEN!!!! (ABOVE: TOP)):
	//The type for the branch must be included in the brackets
	//1st function argument is the name of the branch
	//2nd function argument is the name of the branch that contains the size of the array (for fundamentals only)
	/*
	dFlatTreeInterface->Create_Branch_Fundamental<Int_t>("flat_my_int"); //fundamental = char, int, float, double, etc.
	dFlatTreeInterface->Create_Branch_FundamentalArray<Int_t>("flat_my_int_array", "flat_my_int");
	dFlatTreeInterface->Create_Branch_NoSplitTObject<TLorentzVector>("flat_my_p4");
	dFlatTreeInterface->Create_Branch_ClonesArray<TLorentzVector>("flat_my_p4_array");
	*/

	/************************************* ADVANCED EXAMPLE: CHOOSE BRANCHES TO READ ************************************/

	//TO SAVE PROCESSING TIME
		//If you know you don't need all of the branches/data, but just a subset of it, you can speed things up
		//By default, for each event, the data is retrieved for all branches
		//If you know you only need data for some branches, you can skip grabbing data from the branches you don't need
		//Do this by doing something similar to the commented code below

	//dTreeInterface->Clear_GetEntryBranches(); //now get none
	//dTreeInterface->Register_GetEntryBranch("Proton__P4"); //manually set the branches you want

	/************************************** DETERMINE IF ANALYZING SIMULATED DATA *************************************/

	dIsMC = (dTreeInterface->Get_Branch("MCWeight") != NULL);

}

Bool_t DSelector_pi0kplamb_flat::Process(Long64_t locEntry)
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
	if(locRunNumber != dPreviousRunNumber)
	{
		dIsPolarizedFlag = dAnalysisUtilities.Get_IsPolarizedBeam(locRunNumber, dIsPARAFlag);
		dPreviousRunNumber = locRunNumber;
	}

	/********************************************* SETUP UNIQUENESS TRACKING ********************************************/

	//ANALYSIS ACTIONS: Reset uniqueness tracking for each action
	//For any actions that you are executing manually, be sure to call Reset_NewEvent() on them here
	Reset_Actions_NewEvent();
	dAnalyzeCutActions->Reset_NewEvent(); // manual action, must call Reset_NewEvent()

	//PREVENT-DOUBLE COUNTING WHEN HISTOGRAMMING
		//Sometimes, some content is the exact same between one combo and the next
			//e.g. maybe two combos have different beam particles, but the same data for the final-state
		//When histogramming, you don't want to double-count when this happens: artificially inflates your signal (or background)
		//So, for each quantity you histogram, keep track of what particles you used (for a given combo)
		//Then for each combo, just compare to what you used before, and make sure it's unique

	//EXAMPLE 1: Particle-specific info:
	set<Int_t> locUsedSoFar_BeamEnergy; //Int_t: Unique ID for beam particles. set: easy to use, fast to search

	//EXAMPLE 2: Combo-specific info:
		//In general: Could have multiple particles with the same PID: Use a set of Int_t's
		//In general: Multiple PIDs, so multiple sets: Contain within a map
		//Multiple combos: Contain maps within a set (easier, faster to search)
	set<map<Particle_t, set<Int_t> > > locUsedSoFar_MissingMass;

	//INSERT USER ANALYSIS UNIQUENESS TRACKING HERE

	/**************************************** EXAMPLE: FILL CUSTOM OUTPUT BRANCHES **************************************/

	/*
	Int_t locMyInt = 7;
	dTreeInterface->Fill_Fundamental<Int_t>("my_int", locMyInt);

	TLorentzVector locMyP4(4.0, 3.0, 2.0, 1.0);
	dTreeInterface->Fill_TObject<TLorentzVector>("my_p4", locMyP4);

	for(int loc_i = 0; loc_i < locMyInt; ++loc_i)
		dTreeInterface->Fill_Fundamental<Int_t>("my_int_array", 3*loc_i, loc_i); //2nd argument = value, 3rd = array index
	*/

	/************************************************* LOOP OVER COMBOS *************************************************/

	//Loop over combos
	double best_chi2 = 100000000;
	int best_combo = -1;
	
	for(UInt_t loc_i = 0; loc_i < Get_NumCombos(); ++loc_i)
	{
		//Set branch array indices for combo and all combo particles
		dComboWrapper->Set_ComboIndex(loc_i);

		// Is used to indicate when combos have been cut
		if(dComboWrapper->Get_IsComboCut()) // Is false when tree originally created
			continue; // Combo has been cut previously

		/********************************************** GET PARTICLE INDICES
    	 * *********************************************/
    	double locRFTime = dComboWrapper->Get_RFTime();
    	TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();

    	// Beam
    	double locPropagatedRFTimeBeam =
        locRFTime + (locBeamX4_Measured.Z() - dTargetCenter.Z()) / 29.9792458;
    	double locBeamDeltaT = locBeamX4_Measured.T() - locPropagatedRFTimeBeam;

    	double chi2 = dComboWrapper->Get_ChiSq_KinFit();
    	double ndf = dComboWrapper->Get_NDF_KinFit();
    	// Used for tracking uniqueness when filling histograms, and for determining
    	// unused particles
    	if (chi2 / ndf < best_chi2) {
    	  best_chi2 = chi2 / ndf;
    	  best_combo = loc_i;
    	}

	} // end of combo loop

  	if (best_combo == -1) {
  	  return kTRUE;
  	}
  	dComboWrapper->Set_ComboIndex(best_combo);

			/********************************************** GET PARTICLE INDICES *********************************************/

		//Used for tracking uniqueness when filling histograms, and for determining unused particles

		//Step 0
		Int_t locBeamID = dComboBeamWrapper->Get_BeamID();
		Int_t locKPlusTrackID = dKPlusWrapper->Get_TrackID();

		//Step 1
		Int_t locPhoton1NeutralID = dPhoton1Wrapper->Get_NeutralID();
		Int_t locPhoton2NeutralID = dPhoton2Wrapper->Get_NeutralID();

		//Step 2
		Int_t locPiMinusTrackID = dPiMinusWrapper->Get_TrackID();
		Int_t locProtonTrackID = dProtonWrapper->Get_TrackID();

		/*********************************************** GET FOUR-MOMENTUM **********************************************/

		// Get P4's: //is kinfit if kinfit performed, else is measured
		//dTargetP4 is target p4
		//Step 0
		TLorentzVector locBeamP4 = dComboBeamWrapper->Get_P4();
		TLorentzVector locKPlusP4 = dKPlusWrapper->Get_P4();
		//Step 1
		TLorentzVector locDecayingPi0P4 = dDecayingPi0Wrapper->Get_P4();
		TLorentzVector locPhoton1P4 = dPhoton1Wrapper->Get_P4();
		TLorentzVector locPhoton2P4 = dPhoton2Wrapper->Get_P4();
		//Step 2
		TLorentzVector locPiMinusP4 = dPiMinusWrapper->Get_P4();
		TLorentzVector locProtonP4 = dProtonWrapper->Get_P4();

		// Get Measured P4's:
		//Step 0
		TLorentzVector locBeamP4_Measured = dComboBeamWrapper->Get_P4_Measured();
		TLorentzVector locKPlusP4_Measured = dKPlusWrapper->Get_P4_Measured();
		//Step 1
		TLorentzVector locPhoton1P4_Measured = dPhoton1Wrapper->Get_P4_Measured();
		TLorentzVector locPhoton2P4_Measured = dPhoton2Wrapper->Get_P4_Measured();
		//Step 2
		TLorentzVector locPiMinusP4_Measured = dPiMinusWrapper->Get_P4_Measured();
		TLorentzVector locProtonP4_Measured = dProtonWrapper->Get_P4_Measured();



		/********************************************* GET COMBO RF TIMING INFO *****************************************/

		TLorentzVector locBeamX4_Measured = dComboBeamWrapper->Get_X4_Measured();
		//Double_t locBunchPeriod = dAnalysisUtilities.Get_BeamBunchPeriod(Get_RunNumber());
		// Double_t locDeltaT_RF = dAnalysisUtilities.Get_DeltaT_RF(Get_RunNumber(), locBeamX4_Measured, dComboWrapper);
		// Int_t locRelBeamBucket = dAnalysisUtilities.Get_RelativeBeamBucket(Get_RunNumber(), locBeamX4_Measured, dComboWrapper); // 0 for in-time events, non-zero integer for out-of-time photons
		// Int_t locNumOutOfTimeBunchesInTree = XXX; //YOU need to specify this number
			//Number of out-of-time beam bunches in tree (on a single side, so that total number out-of-time bunches accepted is 2 times this number for left + right bunches) 

		// Bool_t locSkipNearestOutOfTimeBunch = true; // True: skip events from nearest out-of-time bunch on either side (recommended).
		// Int_t locNumOutOfTimeBunchesToUse = locSkipNearestOutOfTimeBunch ? locNumOutOfTimeBunchesInTree-1:locNumOutOfTimeBunchesInTree; 
		// Double_t locAccidentalScalingFactor = dAnalysisUtilities.Get_AccidentalScalingFactor(Get_RunNumber(), locBeamP4.E(), dIsMC); // Ideal value would be 1, but deviations require added factor, which is different for data and MC.
		// Double_t locAccidentalScalingFactorError = dAnalysisUtilities.Get_AccidentalScalingFactorError(Get_RunNumber(), locBeamP4.E()); // Ideal value would be 1, but deviations observed, need added factor.
		// Double_t locHistAccidWeightFactor = locRelBeamBucket==0 ? 1 : -locAccidentalScalingFactor/(2*locNumOutOfTimeBunchesToUse) ; // Weight by 1 for in-time events, ScalingFactor*(1/NBunches) for out-of-time
		// if(locSkipNearestOutOfTimeBunch && abs(locRelBeamBucket)==1) { // Skip nearest out-of-time bunch: tails of in-time distribution also leak in
		// 	dComboWrapper->Set_IsComboCut(true); 
		// 	continue; 
		// } 

		/********************************************* COMBINE FOUR-MOMENTUM ********************************************/

		// DO YOUR STUFF HERE

		// remove the vector.M2 cause you don't use those for Dalitz plots.  instead yuou add the 4-vectors together, square then square root

		// Individual masses, momenta, & energies: beam, target -> K+, photon1, photon2, pi-, proton
		double beam_e = locBeamP4.E();
		double beam_e_measured = locBeamP4_Measured.E();
		double kp_m = locKPlusP4.M();
		double kp_m_measured = locKPlusP4_Measured.M();
		double kp_m2 = locKPlusP4.M2();
		double kp_m2_measured = locKPlusP4_Measured.M2();
		double kp_E = locKPlusP4.E();
		double kp_E_measured = locKPlusP4_Measured.E();
		double decayingPi0_m = locDecayingPi0P4.M();
		double decayingPi0_m_measured = locDecayingPi0P4.M();
		double decayingPi0_m2 = locDecayingPi0P4.M2();
		double decayingPi0_m2_measured = locDecayingPi0P4.M2();
		double decayingPi0_E = locDecayingPi0P4.E();
		double photon1_E = locPhoton1P4.E();
		double photon1_E_measured = locPhoton1P4_Measured.E();
		double photon1_p = locPhoton1P4.P();
		double photon1_p_measured = locPhoton1P4_Measured.P();
		double photon2_E = locPhoton2P4.E();
		double photon2_E_measured = locPhoton2P4_Measured.E();
		double photon2_p = locPhoton2P4.P();
		double photon2_p_measured = locPhoton2P4_Measured.P();
		double decayingLambda_m = (locPiMinusP4 + locProtonP4).M();
		double decayingLambda_m_measured = (locPiMinusP4_Measured + locProtonP4_Measured).M();
		double decayingLambda_m2 = (locPiMinusP4 + locProtonP4).M2();
		double decayingLambda_E = (locPiMinusP4 + locProtonP4).E();
		double decayingLambda_E_measured = (locPiMinusP4_Measured + locProtonP4_Measured).E();
		double pim_m = locPiMinusP4.M();
		double pim_m_measured = locPiMinusP4_Measured.M();
		double pim_m2 = locPiMinusP4.M2();
		double pim_m2_measured = locPiMinusP4_Measured.M2();
		double pim_E = locPiMinusP4.E();
		double pim_E_measured = locPiMinusP4_Measured.E();
		double protonRecoil_m = locProtonP4.M();
		double protonRecoil_m_measured = locProtonP4_Measured.M();
		double protonRecoil_m2 = locProtonP4.M2();
		double protonRecoil_m2_measured = locProtonP4_Measured.M2();
		double protonRecoul_E = locProtonP4.E();
		double protonRecoul_E_measured = locProtonP4_Measured.E();

		// Various combinations of final state particles
		double kpANDPi0_m = (locKPlusP4 + locDecayingPi0P4).M();
		double kpANDPi0_E = (locKPlusP4 + locDecayingPi0P4).E();
		double kpANDPi0COMBO_E = (locKPlusP4 + locPhoton1P4 + locPhoton2P4).E();
		double kpANDphoton1_E = (locKPlusP4 + locPhoton1P4).E();
		double kpANDphoton1_E_measured = (locKPlusP4_Measured + locPhoton1P4_Measured).E();
		double kpANDphoton2_E = (locKPlusP4 + locPhoton2P4).E();
		double kpANDphoton2_E_measured = (locKPlusP4_Measured + locPhoton2P4_Measured).E();
		double kpANDlambda_m = (locKPlusP4 + locProtonP4 + locPiMinusP4).M();
		double kpANDlambda_m_measured = (locKPlusP4_Measured + locProtonP4_Measured + locPiMinusP4_Measured).M();
		double kpANDlambda_E = (locKPlusP4 + locProtonP4 + locPiMinusP4).E();
		double kpANDproton_m = (locKPlusP4 + locProtonP4).M();
		double kpANDproton_m_measured = (locKPlusP4_Measured + locProtonP4_Measured).M();
		double kpANDpim_m = (locKPlusP4 + locPiMinusP4).M();
		double kpANDpim_m_measured = (locKPlusP4_Measured + locPiMinusP4_Measured).M();
		double pi0ANDlambda_m = (locDecayingPi0P4 + locProtonP4 + locPiMinusP4).M();
		double pi0ANDproton_m = (locDecayingPi0P4 + locProtonP4).M();
		double pi0ANDpim_m = (locDecayingPi0P4 + locPiMinusP4).M();

		// Get dEdx values.  dEdx is energy loss per distance traveled.  The formula is known as Bethe-Bloch formula.
		double dEdx_cdc_kplus = dKPlusWrapper->Get_dEdx_CDC();
		double dEdx_fdc_kplus = dKPlusWrapper->Get_dEdx_FDC();

		// need if statement checking if there is energy in FCD or CDC

		// Mandelstam variables: momentum transfer (t), COM frame energy (s).
		double t = (locBeamP4 - locKPlusP4 - locDecayingPi0P4).M2();
		double t0 = (locBeamP4 - locKPlusP4 - locDecayingPi0P4).M2();
		double tPrime = (t - t0);
		double s = (locBeamP4 + dTargetP4).M2();

		// Combine 4-vectors
		TLorentzVector locMissingP4_Measured = locBeamP4_Measured + dTargetP4;
		locMissingP4_Measured -= locKPlusP4_Measured + locPhoton1P4_Measured + locPhoton2P4_Measured + locPiMinusP4_Measured + locProtonP4_Measured;

		/******************************************** EXECUTE ANALYSIS ACTIONS *******************************************/

		// Loop through the analysis actions, executing them in order for the active particle combo
		dAnalyzeCutActions->Perform_Action(); // Must be executed before Execute_Actions()
		if(!Execute_Actions()) //if the active combo fails a cut, IsComboCutFlag automatically set
			return kTRUE;

		//if you manually execute any actions, and it fails a cut, be sure to call:
			//dComboWrapper->Set_IsComboCut(true);

		/**************************************** EXAMPLE: FILL CUSTOM OUTPUT BRANCHES **************************************/

		/*
		TLorentzVector locMyComboP4(8.0, 7.0, 6.0, 5.0);
		//for arrays below: 2nd argument is value, 3rd is array index
		//NOTE: By filling here, AFTER the cuts above, some indices won't be updated (and will be whatever they were from the last event)
			//So, when you draw the branch, be sure to cut on "IsComboCut" to avoid these.
		dTreeInterface->Fill_Fundamental<Float_t>("my_combo_array", -2*loc_i, loc_i);
		dTreeInterface->Fill_TObject<TLorentzVector>("my_p4_array", locMyComboP4, loc_i);
		*/

		/**************************************** EXAMPLE: HISTOGRAM BEAM ENERGY *****************************************/

		//Histogram beam energy (if haven't already)
		if(locUsedSoFar_BeamEnergy.find(locBeamID) == locUsedSoFar_BeamEnergy.end())
		{
			dHist_BeamEnergy->Fill(locBeamP4.E()); // Fills in-time and out-of-time beam photon combos
			//dHist_BeamEnergy->Fill(locBeamP4.E(),locHistAccidWeightFactor); // Alternate version with accidental subtraction

			locUsedSoFar_BeamEnergy.insert(locBeamID);
		}

		/************************************ EXAMPLE: HISTOGRAM MISSING MASS SQUARED ************************************/

		//Missing Mass Squared
		double locMissingMassSquared = locMissingP4_Measured.M2();

		//Uniqueness tracking: Build the map of particles used for the missing mass
			//For beam: Don't want to group with final-state photons. Instead use "Unknown" PID (not ideal, but it's easy).
		map<Particle_t, set<Int_t> > locUsedThisCombo_MissingMass;
		locUsedThisCombo_MissingMass[Unknown].insert(locBeamID); //beam
		locUsedThisCombo_MissingMass[KPlus].insert(locKPlusTrackID);
		locUsedThisCombo_MissingMass[Gamma].insert(locPhoton1NeutralID);
		locUsedThisCombo_MissingMass[Gamma].insert(locPhoton2NeutralID);
		locUsedThisCombo_MissingMass[PiMinus].insert(locPiMinusTrackID);
		locUsedThisCombo_MissingMass[Proton].insert(locProtonTrackID);

		//compare to what's been used so far
		if(locUsedSoFar_MissingMass.find(locUsedThisCombo_MissingMass) == locUsedSoFar_MissingMass.end())
		{
			//unique missing mass combo: histogram it, and register this combo of particles
			dHist_MissingMassSquared->Fill(locMissingMassSquared); // Fills in-time and out-of-time beam photon combos
			//dHist_MissingMassSquared->Fill(locMissingMassSquared,locHistAccidWeightFactor); // Alternate version with accidental subtraction

			locUsedSoFar_MissingMass.insert(locUsedThisCombo_MissingMass);
		}

		//E.g. Cut
		//if((locMissingMassSquared < -0.04) || (locMissingMassSquared > 0.04))
		//{
		//	dComboWrapper->Set_IsComboCut(true);
		//	continue;
		//}

		/****************************************** FILL FLAT TREE (IF DESIRED) ******************************************/

		// RECOMMENDED: FILL ACCIDENTAL WEIGHT
		// dFlatTreeInterface->Fill_Fundamental<Double_t>("accidweight",locHistAccidWeightFactor);

		/*
		//FILL ANY CUSTOM BRANCHES FIRST!!
		Int_t locMyInt_Flat = 7;
		dFlatTreeInterface->Fill_Fundamental<Int_t>("flat_my_int", locMyInt_Flat);

		TLorentzVector locMyP4_Flat(4.0, 3.0, 2.0, 1.0);
		dFlatTreeInterface->Fill_TObject<TLorentzVector>("flat_my_p4", locMyP4_Flat);

		for(int loc_j = 0; loc_j < locMyInt_Flat; ++loc_j)
		{
			dFlatTreeInterface->Fill_Fundamental<Int_t>("flat_my_int_array", 3*loc_j, loc_j); //2nd argument = value, 3rd = array index
			TLorentzVector locMyComboP4_Flat(8.0, 7.0, 6.0, 5.0);
			dFlatTreeInterface->Fill_TObject<TLorentzVector>("flat_my_p4_array", locMyComboP4_Flat, loc_j);
		}
		*/

		// FILL CUSTOM BRANCHES: individual masses, momenta, & energies: beam, target -> K+, photon1, photon2, pi-, proton

		dFlatTreeInterface->Fill_Fundamental<Double_t>("beam_e", beam_e);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("beam_e_measured", beam_e_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_m", kp_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_m_measured", kp_m_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_m2", kp_m2);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kp_m2_measured", kp_m2_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("decayingPi0_m", decayingPi0_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("decayingPi0_m2", decayingPi0_m2);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon1_E", photon1_E);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon1_E_measured", photon1_E_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon1_p", photon1_p);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon1_p_measured", photon1_p_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon2_E", photon2_E);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon2_E_measured", photon2_E_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon2_p", photon2_p);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("photon2_p_measured", photon2_p_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_m", pim_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_m_measured", pim_m_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_m2", pim_m2);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_m2_measured", pim_m2_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("protonRecoil_m", protonRecoil_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("protonRecoil_m_measured", protonRecoil_m_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("protonRecoil_m2", protonRecoil_m2);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("protonRecoil_m2_measured", protonRecoil_m2_measured);

		// FILL CUSTOM BRANCHES: combined masses or energies
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDPi0_m", kpANDPi0_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDPi0_E", kpANDPi0_E);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDphoton1_E", kpANDphoton1_E);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDphoton1_E_measured", kpANDphoton1_E_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDphoton2_E", kpANDphoton2_E);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDphoton2_E_measured", kpANDphoton2_E_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDlambda_m", kpANDlambda_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDlambda_m_measured", kpANDlambda_m_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDlambda_E", kpANDlambda_E);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDproton_m", kpANDproton_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDproton_m_measured", kpANDproton_m_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDpim_m", kpANDpim_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("kpANDpim_m_measured", kpANDpim_m_measured);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pi0ANDlambda_m", pi0ANDlambda_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pi0ANDproton_m", pi0ANDproton_m);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("pi0ANDpim_m", pi0ANDpim_m);

		// FILL CUSTOM BRANCHES: dEdx values
		dFlatTreeInterface->Fill_Fundamental<Double_t>("dEdx_cdc_kplus", dEdx_cdc_kplus);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("dEdx_fdc_kplus", dEdx_fdc_kplus);

		// FILL CUSTOM BRANCHES: Mandelstam variables
		dFlatTreeInterface->Fill_Fundamental<Double_t>("t", t);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("t0", t0);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("tPrime", tPrime);
		dFlatTreeInterface->Fill_Fundamental<Double_t>("s", s);


		//FILL FLAT TREE
		Fill_FlatTree(); //for the active combo

	//FILL HISTOGRAMS: Num combos / events surviving actions
	Fill_NumCombosSurvivedHists();

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

void DSelector_pi0kplamb_flat::Finalize(void)
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
