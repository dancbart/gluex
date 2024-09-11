#include "DSelector_KKpi_mcThrown_genamp2.h"

void DSelector_KKpi_mcThrown_genamp2::Init(TTree *locTree)
{
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = ""; //"" for none
	dOutputTreeFileName = "";
	dFlatTreeFileName = "KKpi_mc_flatte_THROWN.root";
	dFlatTreeName = "pipkmks_flat_mc";
	dSaveDefaultFlatBranches = false;
	//USERS: SET OUTPUT TREE FILES/NAMES //e.g. binning into separate files for AmpTools
	//dOutputTreeFileNameMap["Bin1"] = "mcgen_bin1.root"; //key is user-defined, value is output file name
	//dOutputTreeFileNameMap["Bin2"] = "mcgen_bin2.root"; //key is user-defined, value is output file name
	//dOutputTreeFileNameMap["Bin3"] = "mcgen_bin3.root"; //key is user-defined, value is output file name

	// 3/12/2024: There is an error when analyzing Thrown trees causing a crash.  To avoid the crash add the line:
	dSkipNoTriggerEvents = false;
	// This is per issue 170 logged on Github here: // https://github.com/JeffersonLab/gluex_root_analysis/issues/170

	//Because this function gets called for each TTree in the TChain, we must be careful:
		//We need to re-initialize the tree interface & branch wrappers, but don't want to recreate histograms
	bool locInitializedPriorFlag = dInitializedFlag; //save whether have been initialized previously
	DSelector::Init(locTree); //This must be called to initialize wrappers for each new TTree
	//gDirectory now points to the output file with name dOutputFileName (if any)
	if(locInitializedPriorFlag)
		return; //have already created histograms, etc. below: exit

	dPreviousRunNumber = 0;

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_m");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_m");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_m");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_m");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_E");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_m");

	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("missing_mass_measured");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kShort_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("kmkspip1_m");
	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ProtonPip1_m");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("a0_m");

	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("s_men");
	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("w_var");
	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("t_kmks");
	// dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("minus_t_kmks");

	/******************************** EXAMPLE USER INITIALIZATION: STAND-ALONE HISTOGRAMS *******************************/

	/************************************* ADVANCED EXAMPLE: CHOOSE BRANCHES TO READ ************************************/

	//TO SAVE PROCESSING TIME
		//If you know you don't need all of the branches/data, but just a subset of it, you can speed things up
		//By default, for each event, the data is retrieved for all branches
		//If you know you only need data for some branches, you can skip grabbing data from the branches you don't need
		//Do this by doing something similar to the commented code below

	//dTreeInterface->Clear_GetEntryBranches(); //now get none
	//dTreeInterface->Register_GetEntryBranch("Proton__P4"); //manually set the branches you want
}

Bool_t DSelector_KKpi_mcThrown_genamp2::Process(Long64_t locEntry)
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

	//INSERT USER ANALYSIS UNIQUENESS TRACKING HERE

	/******************************************* LOOP OVER THROWN DATA ***************************************/

	//Thrown beam: just use directly
	double locBeamEnergyUsedForBinning = 0.0;
	if(dThrownBeam != NULL)
		locBeamEnergyUsedForBinning = dThrownBeam->Get_P4().E();

	TLorentzVector locPiPlus1P4;
	TLorentzVector locKMinusP4;
	TLorentzVector locKShortP4;
	TLorentzVector locPiPlus2P4;
	TLorentzVector locPiMinusP4;

	//Loop over throwns
	for(UInt_t loc_i = 0; loc_i < Get_NumThrown(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dThrownWrapper->Set_ArrayIndex(loc_i);

		//Do stuff with the wrapper here ...
		Particle_t locPID = dThrownWrapper->Get_PID();
		TLorentzVector locThrownP4 = dThrownWrapper->Get_P4();
		//cout << "Thrown " << loc_i << ": " << locPID << ", " << locThrownP4.Px() << ", " << locThrownP4.Py() << ", " << locThrownP4.Pz() << ", " << locThrownP4.E() << endl;

		if (locPID == 8){
			locPiPlus1P4 = locThrownP4;
		}
		if (locPID == 12){
			locKMinusP4 = locThrownP4;
		}
		if(locPID == 16){
			locKShortP4 = locThrownP4;
		}
		if (locPID == 8){
			locPiPlus2P4 = locThrownP4;
		}
		if (locPID == 9){
			locPiMinusP4 = locThrownP4;
		}

	}

	// TLorentzVector locMissingP4_Measured = locBeamP4_Measured + dTargetP4;
	// locMissingP4_Measured -= locPiPlus1P4_Measured + locKMinusP4_Measured + locProtonP4_Measured + locPiMinusP4_Measured + locPiPlus2P4_Measured;

	TLorentzVector locPip2PimP4 = locPiPlus2P4 + locPiMinusP4; // kShort (built manually to check above KShort)
	TLorentzVector locKmKsPip1P4 = locKMinusP4 + locPiPlus1P4 + locKShortP4; // f1(1285)
	// TLorentzVector locProtonPip1P4 = locProtonP4 + locPiPlus1P4;
	TLorentzVector locA0P4 = locKMinusP4 + locPiPlus2P4 + locPiMinusP4; // a0(980)

	// double s_men = (locBeamP4 + dTargetP4).M2();
	// double w_var = (locBeamP4 + dTargetP4).M();
	// double t_kmks  = (dTargetP4 - locProtonP4).M2();
	// double minus_t_kmks = (-(t_kmks));
	

	//OR Manually:
	//BEWARE: Do not expect the particles to be at the same array indices from one event to the next!!!!
	//Why? Because while your channel may be the same, the pions/kaons/etc. will decay differently each event.

	//BRANCHES: https://halldweb.jlab.org/wiki/index.php/Analysis_TTreeFormat#TTree_Format:_Simulated_Data
	TClonesArray** locP4Array = dTreeInterface->Get_PointerToPointerTo_TClonesArray("Thrown__P4");
	TBranch* locPIDBranch = dTreeInterface->Get_Branch("Thrown__PID");
/*
	Particle_t locThrown1PID = PDGtoPType(((Int_t*)locPIDBranch->GetAddress())[0]);
	TLorentzVector locThrown1P4 = *((TLorentzVector*)(*locP4Array)->At(0));
	cout << "Particle 1: " << locThrown1PID << ", " << locThrown1P4.Px() << ", " << locThrown1P4.Py() << ", " << locThrown1P4.Pz() << ", " << locThrown1P4.E() << endl;
	Particle_t locThrown2PID = PDGtoPType(((Int_t*)locPIDBranch->GetAddress())[1]);
	TLorentzVector locThrown2P4 = *((TLorentzVector*)(*locP4Array)->At(1));
	cout << "Particle 2: " << locThrown2PID << ", " << locThrown2P4.Px() << ", " << locThrown2P4.Py() << ", " << locThrown2P4.Pz() << ", " << locThrown2P4.E() << endl;
*/


	/******************************************* BIN THROWN DATA INTO SEPARATE TREES FOR AMPTOOLS ***************************************/

/*
	//THESE KEYS MUST BE DEFINED IN THE INIT SECTION (along with the output file names)
	if((locBeamEnergyUsedForBinning >= 8.0) && (locBeamEnergyUsedForBinning < 9.0))
		Fill_OutputTree("Bin1"); //your user-defined key
	else if((locBeamEnergyUsedForBinning >= 9.0) && (locBeamEnergyUsedForBinning < 10.0))
		Fill_OutputTree("Bin2"); //your user-defined key
	else if((locBeamEnergyUsedForBinning >= 10.0) && (locBeamEnergyUsedForBinning < 11.0))
		Fill_OutputTree("Bin3"); //your user-defined key
*/

	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_E", locPiPlus1P4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_px", locPiPlus1P4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_py", locPiPlus1P4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_pz", locPiPlus1P4.Pz());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_m", locPiPlus1P4.M());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_E", locPiPlus2P4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_px", locPiPlus2P4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_py", locPiPlus2P4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_pz", locPiPlus2P4.Pz());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_m", locPiPlus2P4.M());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_E", locPiMinusP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_px", locPiMinusP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_py", locPiMinusP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_pz", locPiMinusP4.Pz());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_m", locPiMinusP4.M());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_E", locKMinusP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_px", locKMinusP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_py", locKMinusP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_pz", locKMinusP4.Pz());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_m", locKMinusP4.M());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_E", locKShortP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_px", locKShortP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_py", locKShortP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_pz", locKShortP4.Pz());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_m", locKShortP4.M());

	// dFlatTreeInterface->Fill_Fundamental<Double_t>("missing_mass_measured", locMissingP4_Measured.M());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("kShort_m", locPip2PimP4.M());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("kmkspip1_m", locKmKsPip1P4.M());
	// dFlatTreeInterface->Fill_Fundamental<Double_t>("ProtonPip1_m", locProtonPip1P4.M());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("a0_m", locA0P4.M());

	// dFlatTreeInterface->Fill_Fundamental<Double_t>("s_men",s_men);
	// dFlatTreeInterface->Fill_Fundamental<Double_t>("minus_t_kmks";minus_t_kmks);


	Fill_FlatTree();
	return kTRUE;
}

void DSelector_KKpi_mcThrown_genamp2::Finalize(void)
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
