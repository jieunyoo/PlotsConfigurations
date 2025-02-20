import os
import subprocess
import string
from LatinoAnalysis.Tools.commonTools import *

for tag in ['em', 'ee', 'mm']:
  if tag in opt.pycfg: EMorEEorMM = tag

samples={}

##############################################
############### Tree Directory ###############
##############################################

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/'

directory = treeBaseDir+'Summer16_102X_nAODv7_Full2016v7/MCl1loose2016v7__MCCorr2016v7__l2loose__l2tightOR2016v7'
directoryDY = treeBaseDir+'Summer16_102X_nAODv7_Full2016v7/MCl1loose2016v7__MCCorr2016v7__l2loose__l2tightOR2016v7__recoilDY'
directoryHM = treeBaseDir+'Summer16_102X_nAODv7_Full2016v7/MCl1loose2016v7__MCCorr2016v7__l2loose__l2tightOR2016v7__BWReweight'

################################################
############### Lepton WP ######################
################################################

eleWP='mva_90p_Iso2016'
muWP='cut_Tight80x'

LepWPCut        = 'LepCut2l__ele_'+eleWP+'__mu_'+muWP
LepWPweight     = 'LepSF2l__ele_'+eleWP+'__mu_'+muWP


################################################
############ BASIC MC WEIGHTS ##################
################################################

#SFweight      = 'SFweight2l*'+LepWPweight+'*'+LepWPCut+'*PrefireWeight'
#SFweight += '*btagSF'
#SFweight += '*PUJetIdSF'
GenLepMatch   = 'PromptGenLepMatch2l'
TotalMC       = 'XSWeight*SFweight*'+GenLepMatch+'*METFilter_MC'


################################################
############## FAKE WEIGHTS ####################
################################################

fakeW = 'fakeW2l_ele_'+eleWP+'_mu_'+muWP


################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
            ['B','Run2016B-02Apr2020_ver2-v1'] ,
            ['C','Run2016C-02Apr2020-v1'] ,
            ['D','Run2016D-02Apr2020-v1'] ,
            ['E','Run2016E-02Apr2020-v1'] ,
            ['F','Run2016F-02Apr2020-v1'] ,
            ['G','Run2016G-02Apr2020-v1'] ,
            ['H','Run2016H-02Apr2020-v1']
          ]

DataSets = ['MuonEG','DoubleMuon','SingleMuon','DoubleEG','SingleElectron']

DataTrig = {
            'MuonEG'         : 'Trigger_ElMu' ,
            'DoubleMuon'     : '!Trigger_ElMu && Trigger_dblMu' ,
            'SingleMuon'     : '!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu' ,
            'DoubleEG'       : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && Trigger_dblEl' ,
            'SingleElectron' : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && !Trigger_dblEl && Trigger_sngEl' ,
           }


############################################
############ MORE MC STAT ##################
############################################

def CombineBaseW(samples, proc, samplelist):
  newbaseW = getBaseWnAOD(directory, 'Summer16_102X_nAODv7_Full2016v7', samplelist)
  for s in samplelist:
    addSampleWeight(samples, proc, s, newbaseW+'/baseW')


###########################################
#############  BACKGROUNDS  ###############
###########################################

############ DY ############

useEmbeddedDY = True
useDYtt = True
useDYHT = False

if EMorEEorMM in ['ee', 'mm']:
  useEmbeddedDY = False
  useDYtt = False
  useDYHT = True

embed_tautauveto = '' #Setup
if useEmbeddedDY:
  embed_tautauveto = '*embed_tautauveto'


if useEmbeddedDY:
  # Actual embedded data
  samples['DYemb']  = {   'name': [ ] ,
                         'weight' : 'METFilter_DATA*'+LepWPCut+'*embed_total_mva16*genWeight*(genWeight<=1)',
                         'weights' : [ ] ,
                         'isData': ['all'],
                         'FilesPerJob' : 400,
                         'suppressNegative' :['all'],
                         'suppressNegativeNuisances' :['all'],
                      }

  for Run in DataRun :
          directoryEmb = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Embedding2016_102X_nAODv7_Full2016v7/DATAl1loose2016v7__l2loose__l2tightOR2016v7__Embedding'
          FileTarget = getSampleFiles(directoryEmb,'DYToTT_MuEle_Embedded_Run2016'+Run[0],True,'nanoLatino_')
          for iFile in FileTarget:
                  samples['DYemb']['name'].append(iFile)
                  samples['DYemb']['weights'].append('Trigger_ElMu')

  # Vetoed MC: Needed for uncertainty
  samples['DYveto']  = {   'name': getSampleFiles(directory,'TTTo2L2Nu',False,'nanoLatino_')
                                 + getSampleFiles(directory,'ST_tW_antitop',False,'nanoLatino_')
                                 + getSampleFiles(directory,'ST_tW_top',False,'nanoLatino_')

                                 + getSampleFiles(directory,'WWTo2L2Nu',False,'nanoLatino_')
                                 + getSampleFiles(directory,'WpWmJJ_EWK_noTop',False,'nanoLatino_')
                                 + getSampleFiles(directory,'GluGluWWTo2L2Nu_MCFM',False,'nanoLatino_')
                                 + getSampleFiles(directory,'WpWmJJ_QCD_noTop',False,'nanoLatino_')

                                 + getSampleFiles(directory,'Zg',False,'nanoLatino_')
                                 + getSampleFiles(directory,'WZTo3LNu_mllmin01',False,'nanoLatino_')
                                 + getSampleFiles(directory,'WZTo3LNu_mllmin01_ext1',False,'nanoLatino_')

                                 + getSampleFiles(directory,'ZZTo2L2Nu',False,'nanoLatino_')
                                 + getSampleFiles(directory,'ZZTo2L2Nu_ext1',False,'nanoLatino_')
                                 + getSampleFiles(directory,'ZZTo2L2Q',False,'nanoLatino_')
                                 + getSampleFiles(directory,'ZZTo4L',False,'nanoLatino_')
                                 + getSampleFiles(directory,'ZZTo4L_ext1',False,'nanoLatino_')
                                 + getSampleFiles(directory,'WZTo2L2Q',False,'nanoLatino_'),

                         'weight' : TotalMC+'*'+'(1-embed_tautauveto)',
                         'FilesPerJob' : 1, # There's some error about not finding sample-specific variables like "nllW" when mixing different samples into a single job; so split them all up instead
                      }
  CombineBaseW(samples, 'DYveto', ['ZZTo2L2Nu', 'ZZTo2L2Nu_ext1'])
  CombineBaseW(samples, 'DYveto', ['ZZTo4L', 'ZZTo4L_ext1'])
  CombineBaseW(samples, 'DYveto', ['WZTo3LNu_mllmin01', 'WZTo3LNu_mllmin01_ext1'])

  veto_dict = {'TTTo2L2Nu'     : '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) * (TMath::Sqrt(TMath::Exp(1.61468e-03 + 3.46659e-06*topGenPt - 8.90557e-08*topGenPt*topGenPt) * TMath::Exp(1.61468e-03 + 3.46659e-06*antitopGenPt - 8.90557e-08*antitopGenPt*antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)' ,
               'ST_tW_antitop' : '1' ,
               'ST_tW_top'     : '1' ,

               'WWTo2L2Nu'        : 'nllW*(mjjGen_OTF<100)' ,
               'WpWmJJ_EWK_noTop' : '(Sum$(abs(GenPart_pdgId)==6)==0 && Sum$(GenPart_pdgId==25)==0)*(lhe_mW1[0] > 60. && lhe_mW1[0] < 100. && lhe_mW2[0] > 60. && lhe_mW2[0] < 100.)',
               'GluGluWWTo2L2Nu_MCFM' : '1.53/1.4' ,
               'WpWmJJ_QCD_noTop' : '(mjjGen_OTF>=100)' ,

               'Zg'                     : '(Gen_ZGstar_mass <= 0)+(Gen_ZGstar_mass > 0)*((Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4) * 0.94 + (Gen_ZGstar_mass <0 || Gen_ZGstar_mass > 4) * 1.14)' ,
               'WZTo3LNu_mllmin01'      : '(Gen_ZGstar_mass > 0.1)*((Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4) * 0.94 + (Gen_ZGstar_mass <0 || Gen_ZGstar_mass > 4) * 1.14)' ,
               'WZTo3LNu_mllmin01_ext1' : '(Gen_ZGstar_mass > 0.1)*((Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4) * 0.94 + (Gen_ZGstar_mass <0 || Gen_ZGstar_mass > 4) * 1.14)' ,

               'ZZTo2L2Nu'      : '1.11' ,
               'ZZTo2L2Nu_ext1' : '1.11' ,
               'ZZTo2L2Q'       : '1.11' ,
               'ZZTo4L'         : '1.11' ,
               'ZZTo4L_ext1'    : '1.11' ,
               'WZTo2L2Q'       : '1.11'
              }

  for v_samp,v_weight in veto_dict.items():
          if v_weight != '1': addSampleWeight(samples,'DYveto',v_samp,v_weight)

if useDYtt :
    samples['DY'] = {    'name'   :   getSampleFiles(directory,'DYJetsToTT_MuEle_M-50',False,'nanoLatino_')
                                    + getSampleFiles(directory,'DYJetsToTT_MuEle_M-50_ext1',False,'nanoLatino_')
                                    + getSampleFiles(directory,'DYJetsToLL_M-10to50_ext1',False,'nanoLatino_'), # There also a nominal sample without ext, but it IS the same sample as the ext one!
                         'weight' : TotalMC+embed_tautauveto + '*( !(Sum$(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))' ,# To remove some overlap between DY/Vg
                         'FilesPerJob' : 10,
                         'EventsPerJob' : 500000,
                         'suppressNegative' :['all'],
                         'suppressNegativeNuisances' :['all'],
                    }
    CombineBaseW(samples, 'DY', ['DYJetsToTT_MuEle_M-50', 'DYJetsToTT_MuEle_M-50_ext1'])
    addSampleWeight(samples,'DY','DYJetsToTT_MuEle_M-50','DY_NLO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToTT_MuEle_M-50_ext1','DY_NLO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-10to50_ext1','DY_NLO_pTllrw')
    
else:
  samples['DY'] = {    'name'   :   getSampleFiles(directoryDY,'DYJetsToLL_M-50_ext2',True,'nanoLatino_') # LO_ext1 is DYMVA Training!
                                  + getSampleFiles(directoryDY,'DYJetsToLL_M-10to50_ext1',True,'nanoLatino_'), # NLO(_ext0) is DYMVA Training!
                       'weight' : TotalMC+embed_tautauveto + '*( !(Sum$(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))' ,
                       'FilesPerJob' : 10,
                       'EventsPerJob' : 500000,
                       'suppressNegative' :['all'],
                       'suppressNegativeNuisances' :['all'],
                   }
  addSampleWeight(samples,'DY','DYJetsToLL_M-50_ext2','DY_NLO_pTllrw')
  addSampleWeight(samples,'DY','DYJetsToLL_M-10to50_ext1','DY_NLO_pTllrw')

  if useDYHT:
    samples['DY']['name'] += getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-70to100',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-100to200',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-100to200_ext1',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-200to400',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-200to400_ext1',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-400to600',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-400to600_ext1',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-600to800',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-800to1200',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-1200to2500',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-50_HT-2500toInf',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-70to100',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-100to200',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-200to400',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-200to400_ext1',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-400to600',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-400to600_ext1',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-600toinf',True,'nanoLatino_') \
                           + getSampleFiles(directoryDY,'DYJetsToLL_M-5to50_HT-600toinf_ext1',True,'nanoLatino_')
    CombineBaseW(samples, 'DY', ['DYJetsToLL_M-50_HT-100to200', 'DYJetsToLL_M-50_HT-100to200_ext1'])
    CombineBaseW(samples, 'DY', ['DYJetsToLL_M-50_HT-200to400', 'DYJetsToLL_M-50_HT-200to400_ext1'])
    CombineBaseW(samples, 'DY', ['DYJetsToLL_M-50_HT-400to600', 'DYJetsToLL_M-50_HT-400to600_ext1'])
    CombineBaseW(samples, 'DY', ['DYJetsToLL_M-5to50_HT-200to400', 'DYJetsToLL_M-5to50_HT-200to400_ext1'])
    CombineBaseW(samples, 'DY', ['DYJetsToLL_M-5to50_HT-400to600', 'DYJetsToLL_M-5to50_HT-400to600_ext1'])
    CombineBaseW(samples, 'DY', ['DYJetsToLL_M-5to50_HT-600toinf', 'DYJetsToLL_M-5to50_HT-600toinf_ext1'])
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_ext2',               '(LHE_HT < 70)')
    addSampleWeight(samples,'DY','DYJetsToLL_M-10to50_ext1',           '(LHE_HT < 70)')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-70to100',         'DY_LO_pTllrw') # HT-binned are LO!
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-100to200',        'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-100to200_ext1',   'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-200to400',        'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-200to400_ext1',   'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-400to600',        'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-400to600_ext1',   'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-600to800',        'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-800to1200',       'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-1200to2500',      'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-50_HT-2500toInf',       'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-70to100',      'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-100to200',     'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-200to400',     'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-200to400_ext1','DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-400to600',     'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-400to600_ext1','DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-600toinf',     'DY_LO_pTllrw')
    addSampleWeight(samples,'DY','DYJetsToLL_M-5to50_HT-600toinf_ext1','DY_LO_pTllrw')



############ Top ############

samples['top'] = {    'name'   :   getSampleFiles(directory,'TTTo2L2Nu',False,'nanoLatino_') 
                                 + getSampleFiles(directory,'ST_s-channel',False,'nanoLatino_') 
                                 + getSampleFiles(directory,'ST_t-channel_antitop',False,'nanoLatino_') 
                                 + getSampleFiles(directory,'ST_t-channel_top',False,'nanoLatino_') 
                                 + getSampleFiles(directory,'ST_tW_antitop',False,'nanoLatino_') 
                                 + getSampleFiles(directory,'ST_tW_top',False,'nanoLatino_') ,
                     'weight' : TotalMC+embed_tautauveto ,
                     'FilesPerJob' : 10,
                     'EventsPerJob' : 300000,
                     'suppressNegative' :['all'],
                     'suppressNegativeNuisances' :['all'],
                 }

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')
# Wrong XSec in t-channel: Samples are for inclusive W decay; our XSec is for leptonic only
lepD_to_incD = '(100./(10.75 + 10.57 + 11.25))' # 100% / (W->e+nu & W->mu+nu & W->tau+nu)
addSampleWeight(samples,'top','ST_t-channel_antitop', lepD_to_incD)
addSampleWeight(samples,'top','ST_t-channel_top',     lepD_to_incD)

############ WW ############

samples['WW'] = {    'name'   :   getSampleFiles(directory,'WWTo2L2Nu',False,'nanoLatino_') ,
                     'weight' : TotalMC+'*nllW*(mjjGen_OTF<100)'+embed_tautauveto ,
                     'FilesPerJob' : 10,
                     'EventsPerJob' : 500000,
                     'suppressNegative' :['all'],
                     'suppressNegativeNuisances' :['all'],
                 }

samples['WWewk'] = {   'name'  : getSampleFiles(directory, 'WpWmJJ_EWK_noTop',False,'nanoLatino_'),
                       'weight': TotalMC+embed_tautauveto+ '*(Sum$(abs(GenPart_pdgId)==6)==0 && Sum$(GenPart_pdgId==25)==0)'+'*(lhe_mW1[0] > 60. && lhe_mW1[0] < 100. && lhe_mW2[0] > 60. && lhe_mW2[0] < 100.)', #filter tops and higgs, limit w mass to remove some overlap between DY/WWewk/Vg (2016 only)
                       'suppressNegative' :['all'],
                       'suppressNegativeNuisances' :['all'],
                   }

samples['ggWW']  = {  'name'   :   getSampleFiles(directory,'GluGluWWTo2L2Nu_MCFM',False,'nanoLatino_'),
                      'weight' : TotalMC+embed_tautauveto + '*1.53/1.4' , #update k-factor
                      'FilesPerJob' : 10,
                      'EventsPerJob' : 500000,
                      'suppressNegative' :['all'],
                      'suppressNegativeNuisances' :['all'],
                   }

samples['qqWWqq'] = {  'name'   :   getSampleFiles(directory,'WpWmJJ_QCD_noTop',False,'nanoLatino_') ,
                       'weight' : TotalMC+'*(Sum$(abs(GenPart_pdgId)==6)==0)*(mjjGen_OTF>=100)*(GenLHE)'+embed_tautauveto ,
                       'FilesPerJob' : 10,
                       'EventsPerJob' : 500000,
                       'suppressNegative' :['all'],
                       'suppressNegativeNuisances' :['all'],
                 }

samples['WW2J'] = {  'name'   :   getSampleFiles(directory,'WpWmJJ_QCD_noTop',False,'nanoLatino_') ,
                     'weight' : TotalMC+'*(Sum$(abs(GenPart_pdgId)==6)==0)*(mjjGen_OTF>=100)*(!GenLHE)'+embed_tautauveto ,
                     'FilesPerJob' : 10,
                     'EventsPerJob' : 500000,
                     'suppressNegative' :['all'],
                     'suppressNegativeNuisances' :['all'],
                 }



############ VZ ############

samples['VZ']  = {  'name'   :   getSampleFiles(directory,'ZZTo2L2Nu',False,'nanoLatino_')
                               + getSampleFiles(directory,'ZZTo2L2Nu_ext1',False,'nanoLatino_')
                               + getSampleFiles(directory,'ZZTo2L2Q',False,'nanoLatino_')
                               + getSampleFiles(directory,'ZZTo4L',False,'nanoLatino_') 
                               + getSampleFiles(directory,'ZZTo4L_ext1',False,'nanoLatino_') 
                               + getSampleFiles(directory,'WZTo2L2Q',False,'nanoLatino_'),
                    'weight' : TotalMC+embed_tautauveto + '*1.11' ,
                    'FilesPerJob' : 10,
                    'EventsPerJob' : 500000,
                    'suppressNegative' :['all'],
                    'suppressNegativeNuisances' :['all'],
                 }
CombineBaseW(samples, 'VZ', ['ZZTo2L2Nu', 'ZZTo2L2Nu_ext1'])
CombineBaseW(samples, 'VZ', ['ZZTo4L', 'ZZTo4L_ext1'])

############ Vg ############

samples['Vg']  = {  'name'   :   getSampleFiles(directory,'Wg_MADGRAPHMLM',False,'nanoLatino_')
                               + getSampleFiles(directory,'Zg',False,'nanoLatino_'),
                    'weight' : 'XSWeight*SFweight*METFilter_MC'+'*(Gen_ZGstar_mass <= 0)'+embed_tautauveto,
                    'FilesPerJob' : 10,
                    'EventsPerJob' : 500000,
                    'suppressNegative' :['all'],
                    'suppressNegativeNuisances' :['all'],
                  }


############ VgS ############

samples['VgS']  =  {  'name'   :   getSampleFiles(directory,'Wg_MADGRAPHMLM',False,'nanoLatino_')
                                 + getSampleFiles(directory,'Zg',False,'nanoLatino_')
                                 + getSampleFiles(directory,'WZTo3LNu_mllmin01',False,'nanoLatino_')
                                 + getSampleFiles(directory,'WZTo3LNu_mllmin01_ext1',False,'nanoLatino_'),
                      'weight' : TotalMC+embed_tautauveto + ' * (gstarLow * 0.94 + gstarHigh * 1.14)',
                      'FilesPerJob' : 10,
                      'EventsPerJob' : 500000,
                      'suppressNegative' :['all'],
                      'suppressNegativeNuisances' :['all'],
                      'subsamples': {
                        'L': 'gstarLow',
                        'H': 'gstarHigh'
                      }
                   }
CombineBaseW(samples, 'VgS', ['WZTo3LNu_mllmin01', 'WZTo3LNu_mllmin01_ext1'])

# 14.02.2020: Changed Vg treatment
addSampleWeight(samples,'VgS','Wg_MADGRAPHMLM',    '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 0.1)')
addSampleWeight(samples,'VgS','Zg',                '(Gen_ZGstar_mass > 0)')
addSampleWeight(samples,'VgS','WZTo3LNu_mllmin01', '(Gen_ZGstar_mass > 0.1)')
addSampleWeight(samples,'VgS','WZTo3LNu_mllmin01_ext1', '(Gen_ZGstar_mass > 0.1)')


############ VVV ############

samples['VVV']  = {  'name'   :   getSampleFiles(directory,'ZZZ',False,'nanoLatino_')
                                + getSampleFiles(directory,'WZZ',False,'nanoLatino_')
                                + getSampleFiles(directory,'WWZ',False,'nanoLatino_')
                                + getSampleFiles(directory,'WWW',False,'nanoLatino_'),
                    'weight' : TotalMC ,
                    'FilesPerJob' : 10,
                    'suppressNegative' :['all'],
                    'suppressNegativeNuisances' :['all'],
                  }



##########################################
################ SIGNALS #################
##########################################

massesAndModelsFile = "massesAndModels.py"
if os.path.exists(massesAndModelsFile) :
  handle = open(massesAndModelsFile,'r')
  exec(handle)
  handle.close()
else:
  print "!!! ERROR file ", massesAndModelsFile, " does not exist."

INToverSBI = False
noSMxsec = '(1.0/Xsec)'

for model in models:
  model_I = model+'_I'
  model_name = '_'+model.replace(".","")

  ############ HIGH MASS ggH H->WW ############

  for mass in massggh:

    # Special names in 2016 for mass >= 300
    jhugen = ''
    if int(mass) >= 300: jhugen = '_JHUGen698'
    if int(mass) >= 4000: jhugen = '_JHUGen714'

    # Xsec*BR is applied in later step, so remove "SM"-Xsec*BR 
    samples['GGH_'+mass+model_name]  = {  'name'   :   getSampleFiles(directoryHM,'GluGluHToWWTo2L2Nu'+jhugen+'_M'+mass,True,'nanoLatino_'),
                        'weight' : TotalMC+'*'+noSMxsec+'*'+model ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 250000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }

    if INToverSBI:
      samples['GGHINT_'+mass+model_name]  = {  'name'   :   getSampleFiles(directoryHM,'GluGluHToWWTo2L2Nu'+jhugen+'_M'+mass,True,'nanoLatino_'),
                        'weight' : TotalMC+'*'+noSMxsec+'*'+'('+model_I+'*(abs('+model_I+')<20))' , # abs<100 cut removes 0.035% of all events, abs<50 cut removes 0.074% of all events, abs<20 cut removes 0.180% of all events
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 250000,
                     }

    else:
      samples['GGHSBI_'+mass+model_name]  = {  'name'   :   getSampleFiles(directoryHM,'GluGluHToWWTo2L2Nu'+jhugen+'_M'+mass,True,'nanoLatino_')
                                                      + getSampleFiles(directory,'GluGluWWTo2L2Nu_MCFM',False,'nanoLatino_')
                                                      + getSampleFiles(directory,'GluGluHToWWTo2L2Nu_alternative_M125',False,'nanoLatino_'),
                        'weight' : TotalMC ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 250000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }

      addSampleWeight(samples, 'GGHSBI_'+mass+model_name, 'GluGluHToWWTo2L2Nu'+jhugen+'_M'+mass, noSMxsec+'*'+'('+model+' + '+model_I+'*(abs('+model_I+')<20))')
      addSampleWeight(samples, 'GGHSBI_'+mass+model_name, 'GluGluWWTo2L2Nu_MCFM', '1.53/1.4'+embed_tautauveto)
      addSampleWeight(samples, 'GGHSBI_'+mass+model_name, 'GluGluHToWWTo2L2Nu_alternative_M125', 'MINLO')

  ############ HIGS MASS VBF H->WW ############

  for mass in massvbf:

    # Special names in 2016 for mass >= 300
    jhugen = ''
    if int(mass) >= 300: jhugen = '_JHUGen698'
    if int(mass) >= 4000: jhugen = '_JHUGen714'

    # Xsec*BR is applied in later step, so remove "SM"-Xsec*BR 
    samples['QQH_'+mass+model_name]  = {  'name'   :   getSampleFiles(directoryHM,'VBFHToWWTo2L2Nu'+jhugen+'_M'+mass,True,'nanoLatino_'),
                        'weight' : TotalMC+'*'+noSMxsec+'*'+model ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 250000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }

    if INToverSBI:
      samples['QQHINT_'+mass+model_name]  = {  'name'   :   getSampleFiles(directoryHM,'VBFHToWWTo2L2Nu'+jhugen+'_M'+mass,True,'nanoLatino_'),
                        'weight' : TotalMC+'*'+noSMxsec+'*'+'('+model_I+'*(abs('+model_I+')<20))' ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 250000,
                     }

    else:
      samples['QQHSBI_'+mass+model_name]  = {  'name'   :   getSampleFiles(directoryHM,'VBFHToWWTo2L2Nu'+jhugen+'_M'+mass,True,'nanoLatino_')
                                                      + getSampleFiles(directory,'WpWmJJ_QCD_noTop',False,'nanoLatino_')
                                                      + getSampleFiles(directory,'VBFHToWWTo2L2Nu_alternative_M125',False,'nanoLatino_'),
                        'weight' : TotalMC ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 250000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }

      addSampleWeight(samples, 'QQHSBI_'+mass+model_name, 'VBFHToWWTo2L2Nu'+jhugen+'_M'+mass, noSMxsec+'*'+'('+model+' + '+model_I+'*(abs('+model_I+')<20))')
      addSampleWeight(samples, 'QQHSBI_'+mass+model_name, 'WpWmJJ_QCD_noTop', '(mjjGen_OTF>100)*(GenLHE)'+embed_tautauveto)


############ ggH H->WW ############

samples['ggH_hww']  = {  'name'   :   getSampleFiles(directory,'GluGluHToWWTo2L2Nu_alternative_M125',False,'nanoLatino_'),
                        'weight' : TotalMC,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 500000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }
addSampleWeight(samples, 'ggH_hww', 'GluGluHToWWTo2L2NuPowheg_M125', 'MINLO')

############ VBF H->WW ############

samples['qqH_hww']  = {  'name'   :   getSampleFiles(directory,'VBFHToWWTo2L2Nu_alternative_M125',False,'nanoLatino_'),
                        'weight' : TotalMC ,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }

############ ZH H->WW ############

samples['ZH_hww']  = {  'name'   :   getSampleFiles(directory,'HZJ_HToWW_M125',False,'nanoLatino_'),
                        'weight' : TotalMC ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 500000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }

############ WH H->WW ############

samples['WH_hww']  = {  'name'   :   getSampleFiles(directory,'HWplusJ_HToWW_M125',False,'nanoLatino_')
                                   + getSampleFiles(directory,'HWminusJ_HToWW_M125',False,'nanoLatino_'),
                        'weight' : TotalMC ,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                     }

############ H->TauTau ############

samples['ggH_htt']  = {  'name'   : getSampleFiles(directory,'GluGluHToTauTau_M125',False,'nanoLatino_'),
                         'weight' : TotalMC ,
                         'suppressNegative' :['all'],
                         'suppressNegativeNuisances' :['all'],
                      }

samples['qqH_htt']  = {  'name'   : getSampleFiles(directory,'VBFHToTauTau_M125',False,'nanoLatino_'),
                         'weight' : TotalMC ,
                         'suppressNegative' :['all'],
                         'suppressNegativeNuisances' :['all'],
                      }

samples['ZH_htt']  = {  'name'   : getSampleFiles(directory,'HZJ_HToTauTau_M125',False,'nanoLatino_'),
                        'weight' : TotalMC ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 500000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                      }

samples['WH_htt']  = {  'name'   :  getSampleFiles(directory,'HWplusJ_HToTauTau_M125',False,'nanoLatino_')
                                  + getSampleFiles(directory,'HWminusJ_HToTauTau_M125',False,'nanoLatino_'),
                        'weight' : TotalMC ,
                        'FilesPerJob' : 10,
                        'EventsPerJob' : 500000,
                        'suppressNegative' :['all'],
                        'suppressNegativeNuisances' :['all'],
                      }


###########################################
################## FAKE ###################
###########################################

if EMorEEorMM == 'em':
  fakesamples = ['em', 'me']
elif EMorEEorMM == 'ee':
  fakesamples = ['ee']
elif EMorEEorMM == 'mm':
  fakesamples = ['mm']

for fakesamp in fakesamples:
  lepone = '11' if fakesamp[0] == 'e' else '13'
  leptwo = '11' if fakesamp[1] == 'e' else '13'

  samples['Fake_'+fakesamp]  = {   'name': [ ] ,
                         'weight' : 'METFilter_DATA*'+fakeW+'*(abs(Lepton_pdgId[0])=='+lepone+' && abs(Lepton_pdgId[1])=='+leptwo+')',
                         'weights' : [ ] ,
                         'isData': ['all'],
                         'FilesPerJob' : 400 ,
                         'suppressNegative' :['all'],
                         'suppressNegativeNuisances' :['all'],
                      }

for Run in DataRun :
        directory = treeBaseDir+'Run2016_102X_nAODv7_Full2016v7/DATAl1loose2016v7__l2loose__fakeW'
        for DataSet in DataSets :
                FileTarget = getSampleFiles(directory,DataSet+'_'+Run[1],True,'nanoLatino_')
                for iFile in FileTarget:
                    for fakesamp in fakesamples:
                        samples['Fake_'+fakesamp]['name'].append(iFile)
                        samples['Fake_'+fakesamp]['weights'].append(DataTrig[DataSet])

###########################################
################## DATA ###################
###########################################

samples['DATA']  = {   'name': [ ] ,
                       'weight' : 'METFilter_DATA*'+LepWPCut,
                       'weights' : [ ],
                       'isData': ['all'],
                       'FilesPerJob' : 800,
                  }

for Run in DataRun :
        directory = treeBaseDir+'Run2016_102X_nAODv7_Full2016v7/DATAl1loose2016v7__l2loose__l2tightOR2016v7'
        for DataSet in DataSets :
                FileTarget = getSampleFiles(directory,DataSet+'_'+Run[1],True,'nanoLatino_')
                for iFile in FileTarget:
                        #print(iFile)
                        samples['DATA']['name'].append(iFile)
                        samples['DATA']['weights'].append(DataTrig[DataSet])

