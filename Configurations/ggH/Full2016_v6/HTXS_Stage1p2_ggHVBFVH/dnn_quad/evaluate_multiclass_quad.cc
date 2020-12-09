#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"
#include <vector>
#include "TVector2.h"
#include "TLorentzVector.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include <iostream>
#include <TMath.h>
#include "generated_code_new_quad.h"
#include <math.h>


float mlj(float ptl, float etal, float phil, float ptj, float etaj, float phij){
        TLorentzVector l;
        TLorentzVector j;
        l.SetPtEtaPhiM(ptl, etal, phil, 0.);
        j.SetPtEtaPhiM(ptj, etaj, phij, 0.);

        return (l+j).M();
}



class evaluate_multiclass: public multidraw::TTreeFunction {
public:
  evaluate_multiclass(int const nclass);

  char const* getName() const override { return "evaluate_multiclass"; }
  TTreeFunction* clone() const override { return new evaluate_multiclass(nclass_); }

  unsigned getNdata() override { return 1; }
  double evaluate(unsigned) override;

protected:
  int nclass_;
  void bindTree_(multidraw::FunctionLibrary&) override;
  IntArrayReader*   jetid{};
  FloatArrayReader* ptl{};
  FloatArrayReader* etal{};
  FloatArrayReader* phil{};
  FloatArrayReader* ptj{};
  FloatArrayReader* etaj{};
  FloatArrayReader* phij{};
  FloatArrayReader* qgl{};
  FloatValueReader* mjj{};
  FloatValueReader* mll{};
  FloatValueReader* ptll{};
  FloatValueReader* detajj{};
  FloatValueReader* dphill{};
  FloatValueReader* metpt{};
  FloatValueReader* mti{};
  FloatValueReader* dphillmet{};
  FloatValueReader* drll{};
  FloatValueReader* ht{};
  FloatValueReader* mth{};
};

evaluate_multiclass::evaluate_multiclass(int const nclass) :
  TTreeFunction()
{
  nclass_ = nclass;
}

double
evaluate_multiclass::evaluate(unsigned)
{
  int jetid0 = jetid->At(0);
  int jetid1 = jetid->At(1);
  
  float input[26];
  input[0] = *mjj->Get();
  input[1] = *mll->Get();
  input[2] = *ptll->Get();
  input[3] = *detajj->Get();
  input[4] = *dphill->Get();
  input[5] = *metpt->Get();
  input[6] = *mti->Get();
  input[7] = *dphillmet->Get();
  input[8] = *drll->Get();
  input[9] = *ht->Get();
  input[10] = *mth->Get();

  input[11] = ptl->At(0);
  input[12] = ptl->At(1);
  input[13] = etal->At(0);
  input[14] = etal->At(1);

  input[15] = ptj->At(0);
  input[16] = ptj->At(1);
  input[17] = etaj->At(0);
  input[18] = etaj->At(1);

  input[19] = mlj(ptl->At(0), etal->At(0), phil->At(0), ptj->At(0), etaj->At(0), phij->At(0));
  input[20] = mlj(ptl->At(0), etal->At(0), phil->At(0), ptj->At(1), etaj->At(1), phij->At(1));
  input[21] = mlj(ptl->At(1), etal->At(1), phil->At(1), ptj->At(0), etaj->At(0), phij->At(0));
  input[22] = mlj(ptl->At(1), etal->At(1), phil->At(1), ptj->At(1), etaj->At(1), phij->At(1));

  input[23] = log((abs(2*etal->At(0)-etaj->At(0)-etaj->At(1))+abs(2*etal->At(1)-etaj->At(0)-etaj->At(1)))/(*detajj->Get()));

  input[24] = qgl->At(jetid0);
  input[25] = qgl->At(jetid1);

  return guess_digit(input, nclass_);
}

void
evaluate_multiclass::bindTree_(multidraw::FunctionLibrary& _library)
{
  _library.bindBranch(jetid, "CleanJet_jetIdx");
  _library.bindBranch(ptl, "Lepton_pt");
  _library.bindBranch(etal, "Lepton_eta");
  _library.bindBranch(phil, "Lepton_phi");
  _library.bindBranch(ptj, "CleanJet_pt");
  _library.bindBranch(etaj, "CleanJet_eta");
  _library.bindBranch(phij, "CleanJet_phi");
  _library.bindBranch(qgl, "Jet_qgl");
  _library.bindBranch(mjj, "mjj");
  _library.bindBranch(mll, "mll");
  _library.bindBranch(ptll, "ptll");
  _library.bindBranch(detajj, "detajj");
  _library.bindBranch(dphill, "dphill");
  _library.bindBranch(metpt, "PuppiMET_pt");
  _library.bindBranch(mti, "mTi");
  _library.bindBranch(dphillmet, "dphillmet");
  _library.bindBranch(drll, "drll");
  _library.bindBranch(ht, "ht");
  _library.bindBranch(mth, "mth");
}
