#include <TString.h>

#ifndef KPILAMB_VARS_H
#define KPILAMB_VARS_H

namespace kpilamb {

// Constants
const TString DecayingLambda = "1";
const TString Proton = "1a";
const TString PiMinus2 = "1b";
const TString DecayingKShort = "2";
const TString PiPlus2 = "2a";
const TString PiMinus1 = "2b";
const TString PiPlus1 = "3";
const TString NegOne = "-1.*";

// Inline function MUST be defined before usage:
inline TString mand_t0(const TString& I, const TString& J) {
    return "MASS2(" + I + "," + J + ") - 2*(ENERGY(" + I + ")*ENERGY(" + J + ") - MOMENTUM(" + I + ")*MOMENTUM(" + J + "))";
}

// Variables depending on mand_t0 must come AFTER mand_t0 definition:
const TString mand_t     = NegOne + "MASS2(GLUEXTARGET,-" + DecayingLambda + ")";
const TString mand_t_k   = NegOne + "MASS2(GLUEXBEAM,-" + DecayingKShort + ")";
const TString mand_t_pi  = NegOne + "MASS2(GLUEXBEAM,-" + PiPlus1 + ")";
const TString mand_t_kpi = NegOne + "MASS2(GLUEXBEAM,-" + DecayingKShort + ",-" + PiPlus1 + ")";

const TString mand_tPrime     = mand_t     + " - (" + mand_t0("GLUEXTARGET", DecayingLambda) + ")";
const TString mand_tPrime_k   = mand_t_k   + " - (" + mand_t0("GLUEXBEAM", DecayingKShort) + ")";
const TString mand_tPrime_pi  = mand_t_pi  + " - (" + mand_t0("GLUEXBEAM", PiPlus1) + ")";
const TString mand_tPrime_kpi = mand_t_kpi + " - (" + mand_t0(DecayingKShort, PiPlus1) + ")";

// 2D variables
const TString mand_t_kVSkpi = mand_t_k + ":" + mand_t_kpi;
const TString mand_t_piVSkpi = mand_t_pi + ":" + mand_t_kpi;

const TString mand_t0_kVSkpi = mand_t_k + ":" + mand_t_kpi;
const TString mand_t0_piVSkpi = mand_t_pi + ":" + mand_t_kpi;

const TString mand_tPrime_kVSkpi = mand_t_k + ":" + mand_t_kpi;
const TString mand_tPrime_piVSkpi = mand_t_pi + ":" + mand_t_kpi;

// Define function to declare cuts (must be implemented in your .C or .cpp)
inline void define_kpilamb_cuts();

} // namespace kpilamb

#endif // KPILAMB_VARS_H

