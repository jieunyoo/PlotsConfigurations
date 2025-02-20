# cuts

supercut = '   mll>20 \
            && Lepton_pt[0]>30 \
            && Lepton_pt[1]>20 \
            && (nLepton>=2 && Alt$(Lepton_pt[2],0)<10) \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 30 \
           '

# mll > 20        : Remove Fakes and Vg
# 1.lep pt > 30   : Seems pretty baseline, doesn't remove many events with all other cuts.
# 2.lep pt > 20   : Loose cut that removes few background (good in 0j)
# 3.lep veto      : Absolutely no signal here
# Lep eta < 2.5   : Actually useless because there's already no events here
# ptll > 30       : Loose cut that removes few background
# PuppiMET > 30   : Loose cut that removes few background

# mth > 60        : Orthogonality with tautau analysis
# bVeto           : Remove tops

# HM dphilmet     : dphilmet = min(dphi_l1,met ; dphi_l2,met). Distribution similar to dphi_l2,met, but dphi_l2,met has signal events in tail


## Default Signal regions

cuts['hww2l2v_13TeV_em_incl']  = '   mth>60 \
                                && bVeto \
                                && finalstate \
                              '

cuts['hww2l2v_13TeV_em_0j']  = '   mth>60 \
                                && njet0 \
                                && bVeto \
                                && finalstate \
                              '

cuts['hww2l2v_13TeV_em_1j']  = '   mth>60 \
                                && njet1 \
                                && bVeto \
                                && finalstate \
                              '

cuts['hww2l2v_13TeV_em_2j']  = '   mth>60 \
                                && njet2 \
                                && bVeto \
                                && finalstate \
                              '

#cuts['hww2l2v_13TeV_em_ggh']  = '   mth>60 \
#                                && !VBFcut \
#                                && bVeto \
#                                && finalstate \
#                              '

#cuts['hww2l2v_13TeV_em_vbf']  = '   mth>60 \
#                                && VBFcut \
#                                && bVeto \
#                                && finalstate \
#                              '

cuts['hww2l2v_13TeV_em_newggh']  = '   mth>60 \
                                && !VBFcut_NEW && ggFcut_NEW \
                                && bVeto \
                                && finalstate \
                              '

cuts['hww2l2v_13TeV_em_newvbf']  = '   mth>60 \
                                && VBFcut_NEW \
                                && bVeto \
                                && finalstate \
                              '

cuts['hww2l2v_13TeV_em_newnotag']  = '   mth>60 \
                                && !VBFcut_NEW && !ggFcut_NEW \
                                && bVeto \
                                && finalstate \
                              '

#cuts['hww2l2v_13TeV_em_newggh_01j']  = '   mth>60 \
#                                && (njet0 || njet1) \
#                                && !VBFcut_NEW && ggFcut_NEW \
#                                && bVeto \
#                                && finalstate \
#                              '

#cuts['hww2l2v_13TeV_em_newvbf_01j']  = '   mth>60 \
#                                && (njet0 || njet1) \
#                                && VBFcut_NEW \
#                                && bVeto \
#                                && finalstate \
#                              '

#cuts['hww2l2v_13TeV_em_newnotag_01j']  = '   mth>60 \
#                                && (njet0 || njet1) \
#                                && !VBFcut_NEW && !ggFcut_NEW \
#                                && bVeto \
#                                && finalstate \
#                              '

#cuts['hww2l2v_13TeV_em_newggh_2j']  = '   mth>60 \
#                                && njet2 \
#                                && !VBFcut_NEW && ggFcut_NEW \
#                                && bVeto \
#                                && finalstate \
#                              '

#cuts['hww2l2v_13TeV_em_newvbf_2j']  = '   mth>60 \
#                                && njet2 \
#                                && VBFcut_NEW \
#                                && bVeto \
#                                && finalstate \
#                              '

#cuts['hww2l2v_13TeV_em_newnotag_2j']  = '   mth>60 \
#                                && njet2 \
#                                && !VBFcut_NEW && !ggFcut_NEW \
#                                && bVeto \
#                                && finalstate \
#                              '


## Default Top control regions

cuts['hww2l2v_13TeV_em_top_incl']  = '   mth>60 \
                                    && bReq \
                                    && finalstate \
                                   '

cuts['hww2l2v_13TeV_em_top_0j']  = '   mth>60 \
                                    && njet0 \
                                    && bReq0j \
                                    && finalstate \
                                   '

cuts['hww2l2v_13TeV_em_top_1j']  = '   mth>60 \
                                    && njet1 \
                                    && bReq \
                                    && finalstate \
                                   '

cuts['hww2l2v_13TeV_em_top_2j']  = '   mth>60 \
                                    && njet2 \
                                    && bReq \
                                    && finalstate \
                                   '

#cuts['hww2l2v_13TeV_em_top_ggh']  = '   mth>60 \
#                                    && !VBFcut \
#                                    && bReq \
#                                    && finalstate \
#                                   '

#cuts['hww2l2v_13TeV_em_top_vbf']  = '   mth>60 \
#                                     && VBFcut \
#                                     && bReq \
#                                     && finalstate \
#                                    '

cuts['hww2l2v_13TeV_em_top_newggh']  = '   mth>60 \
                                    && !VBFcut_NEW && ggFcut_NEW \
                                    && bReq \
                                    && finalstate \
                                   '

cuts['hww2l2v_13TeV_em_top_newvbf']  = '   mth>60 \
                                     && VBFcut_NEW \
                                     && bReq \
                                     && finalstate \
                                    '

cuts['hww2l2v_13TeV_em_top_newnotag']  = '   mth>60 \
                                    && !VBFcut_NEW && !ggFcut_NEW \
                                    && bReq \
                                    && finalstate \
                                   '

#cuts['hww2l2v_13TeV_em_top_newggh_01j']  = '   mth>60 \
#                                    && (njet0 || njet1) \
#                                    && !VBFcut_NEW && ggFcut_NEW \
#                                    && (bReq0j || (bReq && njet1)) \
#                                    && finalstate \
#                                   '

#cuts['hww2l2v_13TeV_em_top_newvbf_01j']  = '   mth>60 \
#                                     && (njet0 || njet1) \
#                                     && VBFcut_NEW \
#                                     && (bReq0j || (bReq && njet1)) \
#                                     && finalstate \
#                                    '

#cuts['hww2l2v_13TeV_em_top_newnotag_01j']  = '   mth>60 \
#                                    && (njet0 || njet1) \
#                                    && !VBFcut_NEW && !ggFcut_NEW \
#                                    && (bReq0j || (bReq && njet1)) \
#                                    && finalstate \
#                                   '

#cuts['hww2l2v_13TeV_em_top_newggh_2j']  = '   mth>60 \
#                                    && njet2 \
#                                    && !VBFcut_NEW && ggFcut_NEW \
#                                    && bReq \
#                                    && finalstate \
#                                   '

#cuts['hww2l2v_13TeV_em_top_newvbf_2j']  = '   mth>60 \
#                                     && njet2 \
#                                     && VBFcut_NEW \
#                                     && bReq \
#                                     && finalstate \
#                                    '

#cuts['hww2l2v_13TeV_em_top_newnotag_2j']  = '   mth>60 \
#                                    && njet2 \
#                                    && !VBFcut_NEW && !ggFcut_NEW \
#                                    && bReq \
#                                    && finalstate \
#                                   '


## Default DYtt control regions

cuts['hww2l2v_13TeV_em_dy_incl']  = '   mth<=60 \
                                   && mll<90 \
                                   && bVeto \
                                   && finalstate \
                                  '

cuts['hww2l2v_13TeV_em_dy_0j']  = '   mth<=60 \
                                   && mll<90 \
                                   && njet0 \
                                   && bVeto \
                                   && finalstate \
                                  '

cuts['hww2l2v_13TeV_em_dy_1j']  = '   mth<=60 \
                                   && mll<90 \
                                   && njet1 \
                                   && bVeto \
                                   && finalstate \
                                  '

cuts['hww2l2v_13TeV_em_dy_2j']  = '   mth<=60 \
                                   && mll<90 \
                                   && njet2 \
                                   && bVeto \
                                   && finalstate \
                                  '

#cuts['hww2l2v_13TeV_em_dy_ggh']  = '   mth<=60 \
#                                   && mll<90 \
#                                   && !VBFcut \
#                                   && bVeto \
#                                   && finalstate \
#                                  '

#cuts['hww2l2v_13TeV_em_dy_vbf']  = '   mth<=60 \
#                                    && mll<90 \
#                                    && VBFcut \
#                                    && bVeto \
#                                    && finalstate \
#                                   '

cuts['hww2l2v_13TeV_em_dy_newggh']  = '   mth<=60 \
                                   && mll<90 \
                                   && !VBFcut_NEW && ggFcut_NEW \
                                   && bVeto \
                                   && finalstate \
                                  '

cuts['hww2l2v_13TeV_em_dy_newvbf']  = '   mth<=60 \
                                    && mll<90 \
                                    && VBFcut_NEW \
                                    && bVeto \
                                    && finalstate \
                                   '

cuts['hww2l2v_13TeV_em_dy_newnotag']  = '   mth<=60 \
                                   && mll<90 \
                                   && !VBFcut_NEW && !ggFcut_NEW \
                                   && bVeto \
                                   && finalstate \
                                  '

#cuts['hww2l2v_13TeV_em_dy_newggh_01j']  = '   mth<=60 \
#                                   && mll<90 \
#                                   && (njet0 || njet1) \
#                                   && !VBFcut_NEW && ggFcut_NEW \
#                                   && bVeto \
#                                   && finalstate \
#                                  '

#cuts['hww2l2v_13TeV_em_dy_newvbf_01j']  = '   mth<=60 \
#                                    && mll<90 \
#                                    && (njet0 || njet1) \
#                                    && VBFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                   '

#cuts['hww2l2v_13TeV_em_dy_newnotag_01j']  = '   mth<=60 \
#                                   && mll<90 \
#                                   && (njet0 || njet1) \
#                                   && !VBFcut_NEW && !ggFcut_NEW \
#                                   && bVeto \
#                                   && finalstate \
#                                  '

#cuts['hww2l2v_13TeV_em_dy_newggh_2j']  = '   mth<=60 \
#                                   && mll<90 \
#                                   && njet2 \
#                                   && !VBFcut_NEW && ggFcut_NEW \
#                                   && bVeto \
#                                   && finalstate \
#                                  '

#cuts['hww2l2v_13TeV_em_dy_newvbf_2j']  = '   mth<=60 \
#                                    && mll<90 \
#                                    && njet2 \
#                                    && VBFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                   '

#cuts['hww2l2v_13TeV_em_dy_newnotag_2j']  = '   mth<=60 \
#                                   && mll<90 \
#                                   && njet2 \
#                                   && !VBFcut_NEW && !ggFcut_NEW \
#                                   && bVeto \
#                                   && finalstate \
#                                  '


## High mass Signal regions

cuts['hww2l2v_13TeV_em_highincl']  = '   mth>60 \
                                    && bVeto \
                                    && finalstate \
                                    && HighMass \
                              '

cuts['hww2l2v_13TeV_em_high0j']  = '   mth>60 \
                                    && njet0 \
                                    && bVeto \
                                    && finalstate \
                                    && HighMass \
                              '

cuts['hww2l2v_13TeV_em_high1j']  = '   mth>60 \
                                    && njet1 \
                                    && bVeto \
                                    && finalstate \
                                    && HighMass \
                              '

cuts['hww2l2v_13TeV_em_high2j']  = '   mth>60 \
                                    && njet2 \
                                    && bVeto \
                                    && finalstate \
                                    && HighMass \
                              '

#cuts['hww2l2v_13TeV_em_highggh']  = '   mth>60 \
#                                    && !VBFcut \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '

#cuts['hww2l2v_13TeV_em_highvbf']  = '   mth>60 \
#                                    && VBFcut \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '

cuts['hww2l2v_13TeV_em_highnewggh']  = '   mth>60 \
                                    && !VBFcut_NEW && ggFcut_NEW \
                                    && bVeto \
                                    && finalstate \
                                    && HighMass \
                              '

cuts['hww2l2v_13TeV_em_highnewvbf']  = '   mth>60 \
                                    && VBFcut_NEW \
                                    && bVeto \
                                    && finalstate \
                                    && HighMass \
                              '

cuts['hww2l2v_13TeV_em_highnewnotag']  = '   mth>60 \
                                    && !VBFcut_NEW && !ggFcut_NEW \
                                    && bVeto \
                                    && finalstate \
                                    && HighMass \
                              '

#cuts['hww2l2v_13TeV_em_highnewggh_01j']  = '   mth>60 \
#                                    && (njet0 || njet1) \
#                                    && !VBFcut_NEW && ggFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '

#cuts['hww2l2v_13TeV_em_highnewvbf_01j']  = '   mth>60 \
#                                    && (njet0 || njet1) \
#                                    && VBFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '

#cuts['hww2l2v_13TeV_em_highnewnotag_01j']  = '   mth>60 \
#                                    && (njet0 || njet1) \
#                                    && !VBFcut_NEW && !ggFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '

#cuts['hww2l2v_13TeV_em_highnewggh_2j']  = '   mth>60 \
#                                    && njet2 \
#                                    && !VBFcut_NEW && ggFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '

#cuts['hww2l2v_13TeV_em_highnewvbf_2j']  = '   mth>60 \
#                                    && njet2 \
#                                    && VBFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '

#cuts['hww2l2v_13TeV_em_highnewnotag_2j']  = '   mth>60 \
#                                    && njet2 \
#                                    && !VBFcut_NEW && !ggFcut_NEW \
#                                    && bVeto \
#                                    && finalstate \
#                                    && HighMass \
#                              '


## High mass Top control regions

#cuts['hww2l2v_13TeV_em_top_highggh']  = '   mth>60 \
#                                        && !VBFcut_HM \
#                                        && bReq \
#                                        && finalstate \
#                                        && HighMass \
#                                   '

#cuts['hww2l2v_13TeV_em_top_highvbf']  = '   mth>60 \
#                                         && VBFcut_HM \
#                                         && bReq \
#                                         && finalstate \
#                                         && HighMass \
#                                    '
