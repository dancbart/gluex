#ifndef DSelector_KKpi_mcThrown_genamp2_h
#define DSelector_KKpi_mcThrown_genamp2_h

#include <iostream>

#include "DSelector/DSelector.h"

#include "TH1I.h"
#include "TH2I.h"

class DSelector_KKpi_mcThrown_genamp2 : public DSelector
{
	public:

		DSelector_KKpi_mcThrown_genamp2(TTree* locTree = NULL) : DSelector(locTree){}
		virtual ~DSelector_KKpi_mcThrown_genamp2(){}

		void Init(TTree *tree);
		Bool_t Process(Long64_t entry);

	private:

		void Finalize(void);

		// BEAM POLARIZATION INFORMATION
		UInt_t dPreviousRunNumber;
		bool dIsPolarizedFlag; //else is AMO
		bool dIsPARAFlag; //else is PERP or AMO

	ClassDef(DSelector_KKpi_mcThrown_genamp2, 0);
};

#endif // DSelector_KKpi_mcThrown_genamp2_h
