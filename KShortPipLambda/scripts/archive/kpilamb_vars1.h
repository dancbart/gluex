#ifndef KPILAMB_VARS_H
#define KPILAMB_VARS_H

#include "TString.h"

// Particle ID aliases
const TString DecayingLambda   = "1";
const TString Proton           = "1a";
const TString PiMinus2         = "1b";
const TString DecayingKShort   = "2";
const TString PiPlus2          = "2a";
const TString PiMinus1         = "2b";
const TString PiPlus1          = "3";
const TString NegOne           = "-1.*";

inline void define_kpilamb_cuts() {

  // Single-sided or range cuts
  FSCut::defineCut("flightSigLambda", "VeeLP1>5.0");
  FSCut::defineCut("flightSigKShort", "VeeLP2>5.0");
  FSCut::defineCut("chi2DOF", "Chi2DOF", "0.0", "3.0");
  FSCut::defineCut("unusedE", "EnUnusedSh", "0.0", "0.1");
  FSCut::defineCut("unusedTracks", "NumUnusedTracks<1");
  FSCut::defineCut("coherentPeak", "EnPB", "8.2", "8.8");
  
  // Mass window cuts with extended sidebands and fit regions
  FSCut::defineCut("constrainLambda", 
      "MASS(1a,1b)",      // Proton = 1a, PiMinus2 = 1b
      "1.1", "1.132",     // signal window
      "1.08", "1.1",      // low sideband
      "1.132", "1.22");   // high sideband
  
  FSCut::defineCut("constrainKShort", 
      "MASS(2)", 
      "0.49", "0.51", 
      "0.0", "0.49", 
      "0.51", "1.0");
  
  FSCut::defineCut("constrainKSTAR892", 
      "MASS(2,3)", 
      "0.85", "0.95", 
      "0.0", "0.85", 
      "0.95", "1.0");
  
  FSCut::defineCut("constrainKSTAR1430", 
      "MASS(2,3)", 
      "0.85", "0.95", 
      "0.0", "0.85", 
      "0.95", "1.0");
  
  
  // Mandelstam t variables
  const TString mand_t     = NegOne + "MASS2(GLUEXTARGET,-" + DecayingLambda + ")";
  const TString mand_t_k   = NegOne + "MASS2(GLUEXBEAM,-"   + DecayingKShort + ")";
  const TString mand_t_pi  = NegOne + "MASS2(GLUEXBEAM,-"   + PiPlus1 + ")";
  const TString mand_t_kpi = NegOne + "MASS2(GLUEXBEAM,-"   + DecayingKShort + ",-" + PiPlus1 + ")";
  
  // Function to construct t0
  inline TString mand_t0(const TString& I, const TString& J) {
      return "MASS2(" + I + "," + J + ") - 2*(ENERGY(" + I + ")*ENERGY(" + J + ") - MOMENTUM(" + I + ")*MOMENTUM(" + J + "))";
  }
  
  // Mandelstam t prime variables
  const TString mand_tPrime     = mand_t     + " - (" + mand_t0("GLUEXTARGET", DecayingLambda) + ")";
  const TString mand_tPrime_k   = mand_t_k   + " - (" + mand_t0("GLUEXBEAM", DecayingKShort) + ")";
  const TString mand_tPrime_pi  = mand_t_pi  + " - (" + mand_t0("GLUEXBEAM", PiPlus1) + ")";
  const TString mand_tPrime_kpi = mand_t_kpi + " - (" + mand_t0(DecayingKShort, PiPlus1) + ")";
  
  // 2D variable projections
  const TString mand_t_kVSkpi       = mand_t_k + ":" + mand_t_kpi;
  const TString mand_t_piVSkpi      = mand_t_pi + ":" + mand_t_kpi;
  const TString mand_t0_kVSkpi      = mand_t_k + ":" + mand_t_kpi; // Placeholder
  const TString mand_t0_piVSkpi     = mand_t_pi + ":" + mand_t_kpi;
  const TString mand_tPrime_kVSkpi  = mand_tPrime_k + ":" + mand_tPrime_kpi;
  const TString mand_tPrime_piVSkpi = mand_tPrime_pi + ":" + mand_tPrime_kpi;
  
#endif // KPILAMB_VARS_H

