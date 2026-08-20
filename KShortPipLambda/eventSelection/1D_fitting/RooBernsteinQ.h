#ifndef ROOBERNSTEINQ
#define ROOBERNSTEINQ

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooListProxy.h"

class RooAbsReal;
class RooArgList;

class RooBernsteinQ : public RooAbsPdf {
public:
  RooBernsteinQ() {} ;
  RooBernsteinQ(const char *name, const char *title,
                RooAbsReal& _x,
                RooAbsReal& _massA,
                RooAbsReal& _massB,
                RooAbsReal& _qmin,
                RooAbsReal& _qmax,
                const RooArgList& _coefList);

  RooBernsteinQ(const RooBernsteinQ& other, const char* name = 0);
  virtual TObject* clone(const char* newname) const { return new RooBernsteinQ(*this, newname); }
  inline virtual ~RooBernsteinQ() { }

  Double_t breakupMomentum(double mass0, double mass1, double mass2) const;

protected:

  RooRealProxy x;
  RooRealProxy massA;
  RooRealProxy massB;
  RooRealProxy qmin;
  RooRealProxy qmax;
  RooListProxy coefList;

  Double_t evaluate() const;

private:

  ClassDef(RooBernsteinQ,1)
};

#endif