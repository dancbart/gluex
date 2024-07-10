
// Should be able to run any DSelector on CentOS or Alma9 servers when running interactively (i.e. directly on your terminal).  However, if using SWIF2 to run the DSelector you may have to use CentOS because SWIF2 relies on a python file 'launch.py'.

// Notes on how this DSelector was made 6/3/2024:
// $ gxenv // if this command not found 'source' gluex_env_boot_jlab.csh below -->
// $ source /group/halld/Software/build_scripts/gluex_env_boot_jlab.csh //  (7/2024) This is necessary because Alma9 servers may not see 'gxenv' unless this file is 'sourced' first.
// $ gxenv // now try 'gxenv' again.  It should work.
// $ MakeDSelector /lustre19/expphy/cache/halld/gluex_simulations/REQUESTED_MC/dbarton_MC_v1_pipkmks_genr8_2017_01_anaVer50_3837/trees/tree_pipkmks__B4_M16_genr8/tree_pipkmks__B4_M16_genr8_031029.root pipkmks__B4_M16_Tree KKpi_mcThrown
// Documentation: https://halldweb.jlab.org/wiki/index.php/DSelector

// Debugging: when running DSelector over your .root files you may encounter errors.  I address any error(s) here:

// CCDB error: if you get a 'CCDB' error, try sourcing gxenv in a different .xml environment:
// $ gxenv /group/halld/www/halldweb/html/halld_versions/version_5.17.0.xml
// If that doesn't work step back from *_5.17.0.xml one-by-one, attempting to run your DSelector over your set of .ROOT file(s) each time.
// You'll know you're successful if you see the output file(s) in your directory, e.g. KKpi_mcThrown.root
// You will still need to inspect the file to see if the DSelector created the data you expected in your .ROOT file.  But the above at least makes sure the machinery of creating an output file works.  Validating if it created good data is up to you.

// Thrown tree error: There is an error when analyzing Thrown trees causing a crash.  To avoid the crash add the line:
// dSkipNoTriggerEvents = false;
// This is per issue 170 logged on Github here (3/12/2024): // https://github.com/JeffersonLab/gluex_root_analysis/issues/170
// This line added to Init() below, but causes a crash.  So commented out for now (7/6/2024).
// Reason may be I haven't filled out the DSelector file yet, just starting.  so I'll comment it back in at some point.


#include "DSelector_KKpi_mcThrown.h"

void DSelector_KKpi_mcThrown::Init(TTree *locTree)
{
	
	// Debugging:
	// outputFile = new TFile("debuggingOutput.root", "RECREATE");
	// outputTree = new TTree("tree", "tree");
	// outputTree->Branch("loc_i", &locIArray);
	// outputTree->Branch("locPID", &locPIDArray);
	
	
	// USERS: IN THIS FUNCTION, ONLY MODIFY SECTIONS WITH A "USER" OR "EXAMPLE" LABEL. LEAVE THE REST ALONE.

	// The Init() function is called when the selector needs to initialize a new tree or chain.
	// Typically here the branch addresses and branch pointers of the tree will be set.
	// Init() will be called many times when running on PROOF (once per file to be processed).

	//USERS: SET OUTPUT FILE NAME //can be overriden by user in PROOF
	dOutputFileName = ""; //"" for none
	dOutputTreeFileName = ""; //"" for none
	dFlatTreeFileName = "KKpi_mcThrown.root"; //output flat tree (one combo per tree entry), "" for none
	dFlatTreeName = "pipkmks_flat_Thrown"; //if blank, default name will be chosen
	dSaveDefaultFlatBranches = false; // False: don't save default branches, reduce disk footprint.
	//dSaveTLorentzVectorsAsFundamentaFlatTree = false; // Default (or false): save particles as TLorentzVector objects. True: save as four doubles instead.

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

	// Get_ComboWrappers();
	dPreviousRunNumber = 0;

	dFlatTreeInterface->Create_Branch_Fundamental<Int_t>("nParticles");
	dFlatTreeInterface->Create_Branch_Fundamental<Int_t>("nThrown");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("beam_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("beam_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("beam_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("beam_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("target_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("target_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("target_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("target_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip1_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pip2_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("pim_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("km_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("proton_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("proton_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("proton_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("proton_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_px");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_py");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_pz");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("ks_E");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_p");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_p");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_p");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_km");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_km");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_km");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_pip1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_pip1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_pip1");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_pip2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_pip2");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_pip2");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_pim");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_pim");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_pim");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("theta_f1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mom_f1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_f1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mass_f1");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mpippim");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mppip1");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("mKsKm");

    dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("men_s");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("men_t");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("cosTheta_f1_cm");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_f1_cm");

	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("cosTheta_Ks_cm");
	dFlatTreeInterface->Create_Branch_Fundamental<Double_t>("phi_Ks_cm");

	/************************************** DETERMINE IF ANALYZING SIMULATED DATA *************************************/

	// dIsMC = (dTreeInterface->Get_Branch("MCWeight") != NULL);

}

Bool_t DSelector_KKpi_mcThrown::Process(Long64_t locEntry)
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


	/******************************************* LOOP OVER THROWN DATA ***************************************/

	//Thrown beam: just use directly
	double locBeamEnergyUsedForBinning = 0.0;
	if(dThrownBeam != NULL)
		locBeamEnergyUsedForBinning = dThrownBeam->Get_P4().E();
		TLorentzVector locBeamP4 = dThrownBeam->Get_P4();
		TLorentzVector locProdSpacetimeVertex =dThrownBeam->Get_X4();//Get production vertex


	TLorentzVector dTargetP4;
	dTargetP4.SetXYZM(0.0,0.0,0.0,0.938);

	TLorentzVector locProtonP4;
	TLorentzVector locPiPlus1P4;
	TLorentzVector locPiMinusP4;
	TLorentzVector locPiPlus2P4;
	TLorentzVector locKMinusP4;
	TLorentzVector locKShortP4;

	TLorentzVector PiPlusHypo1;
	TLorentzVector PiPlusHypo2;
	

	Bool_t piPlusChecked = false;
	int nparticles = 0;
	int nThrown = Get_NumThrown();

	Int_t KsThrown_Index;

	// create a vector for potential pi+ candidates indices
	vector<int> piPlusIndices;

	//Loop over throwns
	for(UInt_t loc_i = 0; loc_i < Get_NumThrown(); ++loc_i)
	{
		//Set branch array indices corresponding to this particle
		dThrownWrapper->Set_ArrayIndex(loc_i);
		
		//Do stuff with the wrapper here ...
		Particle_t locPID = dThrownWrapper->Get_PID();
		TLorentzVector locThrownP4 = dThrownWrapper->Get_P4();
		// cout << "Thrown " << loc_i << ": " << locPID << ", " << locThrownP4.Px() << ", " << locThrownP4.Py() << ", " << locThrownP4.Pz() << ", " << locThrownP4.E() << endl;

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
	
		// locPIDArray.push_back(dThrownWrapper->Get_PID());
		// locIArray.push_back(loc_i);
	
	}


	double proton_theta = locProtonP4.Theta() * 180/3.141592653;
	double proton_phi = locProtonP4.Phi() * 180/3.141592653;
	double proton_mom = locProtonP4.P();

	double piplus1_theta = locPiPlus1P4.Theta() * 180/3.141592653;
	double piplus1_phi = locPiPlus1P4.Phi() * 180/3.141592653;
	double piplus1_mom = locPiPlus1P4.P();

	double Kminus_theta = locKMinusP4.Theta() * 180/3.141592653;
	double Kminus_phi = locKMinusP4.Phi() * 180/3.141592653;
	double Kminus_mom = locKMinusP4.P();

	double piminus_theta = locPiMinusP4.Theta() * 180/3.141592653;
	double piminus_phi = locPiMinusP4.Phi() * 180/3.141592653;
	double piminus_mom = locPiMinusP4.P();

	double piplus2_theta = locPiPlus2P4.Theta() * 180/3.141592653;
	double piplus2_phi = locPiPlus2P4.Phi() * 180/3.141592653;
	double piplus2_mom = locPiPlus2P4.P();


	double s_men = (locBeamP4 + dTargetP4).M2();
	double w_var = (locBeamP4 + dTargetP4).M();
	double t_kmks  = (dTargetP4 - locProtonP4).M2();
	double minus_t_kmks = (-(t_kmks));

	TLorentzVector locPip2Pim_P4 = locPiPlus2P4 + locPiMinusP4;
	TLorentzVector locProtonPip1_P4 = locProtonP4 + locPiPlus1P4;
	TLorentzVector locKmKsPip_P4 = locKMinusP4 + locPiPlus1P4 + locKShortP4;

	double ks_theta = locKShortP4.Theta() * 180/3.141592653;
	double ks_phi = locKShortP4.Phi() * 180/3.141592653;
	double ks_mom = locKShortP4.P();

	double f1_phi = locKmKsPip_P4.Phi() * 180/3.141592653;
	double f1_theta =  locKmKsPip_P4.Theta() * 180/3.141592653;
	double f1_mom = locKmKsPip_P4.P();
	double f1_mass = locKmKsPip_P4.M();
	

	TLorentzVector locF1P4 = locKmKsPip_P4;
	// Boosting in CM frame

	TLorentzVector cms = locBeamP4 + dTargetP4;
	TVector3 locBoost_cms = -cms.BoostVector();

	TLorentzVector locBeamP4_CM = locBeamP4 ;
	TLorentzVector locPiPlus1P4_CM = locPiPlus1P4 ;
	TLorentzVector locKMinusP4_CM = locKMinusP4;
	TLorentzVector locProtonP4_CM = locProtonP4;
	//Step 1
	TLorentzVector locPiMinusP4_CM = locPiMinusP4;
	TLorentzVector locPiPlus2P4_CM = locPiPlus2P4;

	TLorentzVector locKmPip2PimP4_CM = locKmKsPip_P4;
	TLorentzVector locProtonPip1P4_CM = locProtonPip1_P4;
	// TLorentzVector locKshortP4_CM = locPip2Pim_P4;
	TLorentzVector locKshortP4_CM = locKShortP4;

	TLorentzVector locF1P4_CM = locKmPip2PimP4_CM;


	locBeamP4_CM.Boost(locBoost_cms);
	locKMinusP4_CM.Boost(locBoost_cms);
	locProtonP4_CM.Boost(locBoost_cms);
	locKmPip2PimP4_CM.Boost(locBoost_cms);
	locProtonPip1P4_CM.Boost(locBoost_cms);
	locKshortP4_CM.Boost(locBoost_cms);

	locF1P4_CM.Boost(locBoost_cms);

	dFlatTreeInterface->Fill_Fundamental<Int_t>("nParticles", nparticles);
	dFlatTreeInterface->Fill_Fundamental<Int_t>("nThrown", nThrown);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("beam_E", locBeamP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("beam_px", locBeamP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("beam_py", locBeamP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("beam_pz", locBeamP4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("target_E", dTargetP4.M());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("target_px", dTargetP4.X());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("target_py", dTargetP4.Y());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("target_pz", dTargetP4.Z());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_E", locPiPlus1P4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_px", locPiPlus1P4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_py", locPiPlus1P4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip1_pz", locPiPlus1P4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_E", locPiPlus2P4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_px", locPiPlus2P4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_py", locPiPlus2P4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pip2_pz", locPiPlus2P4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_E", locPiMinusP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_px", locPiMinusP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_py", locPiMinusP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("pim_pz", locPiMinusP4.Pz());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_E", locKMinusP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_px", locKMinusP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_py", locKMinusP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("km_pz", locKMinusP4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_E", locKShortP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_px", locKShortP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_py", locKShortP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("ks_pz", locKShortP4.Pz());

	dFlatTreeInterface->Fill_Fundamental<Double_t>("proton_E", locProtonP4.E());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("proton_px", locProtonP4.Px());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("proton_py", locProtonP4.Py());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("proton_pz", locProtonP4.Pz());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_p", proton_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_p",proton_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_p", proton_phi);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_pip1", piplus1_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_pip1", piplus1_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_pip1", piplus1_phi );

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_km", Kminus_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_km",Kminus_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_km", Kminus_phi);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_pip2", piplus2_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_pip2", piplus2_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_pip2", piplus2_phi );

	dFlatTreeInterface->Fill_Fundamental<Double_t>("theta_pim", piminus_theta);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mom_pim", piminus_mom);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_pim", piminus_phi);				

	dFlatTreeInterface->Fill_Fundamental<Double_t>("mass_f1", f1_mass);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("mpippim",locPip2Pim_P4.M());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mKsKm", locKmKsPip_P4.M());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("mppip1", locProtonPip1_P4.M());


	dFlatTreeInterface->Fill_Fundamental<Double_t>("men_s",s_men);
	dFlatTreeInterface->Fill_Fundamental<Double_t>("men_t",minus_t_kmks);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("cosTheta_Ks_cm", locKshortP4_CM.CosTheta());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_Ks_cm", locKshortP4_CM.Phi()*180/3.141592653);

	dFlatTreeInterface->Fill_Fundamental<Double_t>("cosTheta_f1_cm", locF1P4_CM.CosTheta());
	dFlatTreeInterface->Fill_Fundamental<Double_t>("phi_f1_cm", locF1P4_CM.Phi()*180/3.141592653);

	//OR Manually:
	//BEWARE: Do not expect the particles to be at the same array indices from one event to the next!!!!
	//Why? Because while your channel may be the same, the pions/kaons/etc. will decay differently each event.

	//BRANCHES: https://halldweb.jlab.org/wiki/index.php/Analysis_TTreeFormat#TTree_Format:_Simulated_Data
	TClonesArray** locP4Array = dTreeInterface->Get_PointerToPointerTo_TClonesArray("Thrown__P4");
	TBranch* locPIDBranch = dTreeInterface->Get_Branch("Thrown__PID");

	Fill_FlatTree();
	return kTRUE;
}

void DSelector_KKpi_mcThrown::Finalize(void)
{
	
	// outputTree->Fill();
	// outputFile->Write();
	
	//CALL THIS LAST
	DSelector::Finalize(); //Saves results to the output file
}