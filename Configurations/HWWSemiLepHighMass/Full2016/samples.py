import os
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # Full2018
configurations = os.path.dirname(configurations) # HWWSemiLepHighMass
configurations = os.path.dirname(configurations) # Configurations

from LatinoAnalysis.Tools.commonTools import getSampleFiles, getBaseW, addSampleWeight

def nanoGetSampleFiles(inputDir, sample):
    try:
        if _samples_noload:
            return []
    except NameError:
        pass

    return getSampleFiles(inputDir, sample, True, 'nanoLatino_')

# samples

try:
    len(samples)
except NameError:
    import collections
    samples = collections.OrderedDict()

################################################
######### Higgs mass samples and models ########
################################################

massesAndModelsFile = "massesAndModels.py"
if os.path.exists(massesAndModelsFile) :
    handle = open(massesAndModelsFile,'r')
    exec(handle)
    handle.close()
else:
    print "!!! ERROR file ", massesAndModelsFile, " does not exist."

model_I_MSSM = '(cprime1.0BRnew0.0_I/cprime1.0BRnew0.0)' # For MSSM -> No Ewk singlet interpretation # TODO: Do this differently # 'MSSModel_I'
model_I = model+'_I'
model_name = '_'+model.replace("cprime","c").replace(".","").replace("BRnew","brn")

################################################
################# SKIMS ########################
################################################

mcProduction = 'Summer16_102X_nAODv5_Full2016v6'

dataReco = 'Run2016_102X_nAODv5_Full2016v6'

# mcSteps = 'MCl1loose2018v5__MCCorr2018v5'
mcSteps = 'MCl1loose2016v6__MCCorr2016v6__Semilep2016'

dataSteps = 'DATAl1loose2016v6__Semilep2016'

##############################################
###### Tree base directory for the site ######
##############################################

SITE=os.uname()[1]
if    'iihe' in SITE:
  treeBaseDir = '/pnfs/iihe/cms/store/user/xjanssen/HWW2015'
elif  'cern' in SITE:
  treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
  # treeBaseDir = '/eos/user/s/ssiebert/HWWNano'

def makeMCDirectory(var=''):
    if var:
        return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var='__' + var))
    else:
        return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))

mcDirectory = makeMCDirectory()
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

################################################
############ DATA DECLARATION ##################
################################################

# DataRun = [
#             ['A','Run2018A-Nano1June2019-v1'] ,
#             ['B','Run2018B-Nano1June2019-v1'] ,
#             ['C','Run2018C-Nano1June2019-v1'] ,
#             ['D','Run2018D-Nano1June2019_ver2-v1'] ,
#           ]
#
# DataSets = ['MuonEG','DoubleMuon','SingleMuon','EGamma']
#
# DataTrig = {
#             'MuonEG'         : 'Trigger_ElMu' ,
#             'DoubleMuon'     : '!Trigger_ElMu && Trigger_dblMu' ,
#             'SingleMuon'     : '!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu' ,
#             'EGamma'         : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl)' ,
#            }


#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeightNoMatch = 'XSWeight*SFweight*METFilter_MC'
mcCommonWeight = 'XSWeight*SFweight*Lepton_genmatched[0]*METFilter_MC'

###########################################
#############  BACKGROUNDS  ###############
###########################################

###### DY #######

ptllDYW_NLO = '(0.87*(gen_ptll<10)+(0.379119+0.099744*gen_ptll-0.00487351*gen_ptll**2+9.19509e-05*gen_ptll**3-6.0212e-07*gen_ptll**4)*(gen_ptll>=10 && gen_ptll<45)+(9.12137e-01+1.11957e-04*gen_ptll-3.15325e-06*gen_ptll**2-4.29708e-09*gen_ptll**3+3.35791e-11*gen_ptll**4)*(gen_ptll>=45 && gen_ptll<200) + 1*(gen_ptll>200))'
ptllDYW_LO = '((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.19374e-07*gen_ptll*gen_ptll*gen_ptll*gen_ptll+6.99751e-10*gen_ptll*gen_ptll*gen_ptll*gen_ptll*gen_ptll)*(gen_ptll>0)*(gen_ptll<100)+(1.41713-0.00165342*gen_ptll)*(gen_ptll>=100)*(gen_ptll<300)+1*(gen_ptll>=300))'

files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50') + \
    nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Sum$(GenPart_pdgId == 22 && TMath::Odd(GenPart_statusFlags) && GenPart_pt > 20.) == 0)',
    'FilesPerJob': 1,
}
addSampleWeight(samples,'DY','DYJetsToLL_M-10to50',ptllDYW_NLO)
addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO',ptllDYW_LO)

###### Top #######

files = nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic') + \
    nanoGetSampleFiles(mcDirectory, 'ST_s-channel') + \
    nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
    nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
    nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop') + \
    nanoGetSampleFiles(mcDirectory, 'ST_tW_top')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}
# FIXME: ???
addSampleWeight(samples,'top','TTToSemiLeptonic','Top_pTrw')


###### WW ########

files = nanoGetSampleFiles(mcDirectory, 'WW-LO_ext1') #+ \
#    nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight, # + '*nllW', #FIXME: what is this weight
    'FilesPerJob': 3
}

samples['WWewk'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK'),
    'weight': mcCommonWeight + '*(Sum$(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)',
    #FIXME there are other samples that dont contain top/higgs to begin with
    #filter tops and Higgs
    'FilesPerJob': 4
}

# # k-factor 1.4 already taken into account in XSWeight
# files = nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENEN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENMN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENTN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNEN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNMN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNTN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNEN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNMN') + \
#     nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNTN')
#
# samples['ggWW'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*1.53/1.4', # updating k-factor
#     'FilesPerJob': 4
# }
############# ggWW semileptonic ##############
#FIXME: samples for this are being produced
#FIXME: in the meantime use interference weights?
samples['ggWW'] = {
    'name'   : nanoGetSampleFiles(mcDirectory, 'GluGluHToWWToLNuQQ_M400'),
    'weight' : mcCommonWeight +'* RelW0.05_B ', #FIXME: is this right?
    'FilesPerJob': 4
}


########## W+jets #########

files = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-LO_ext2') +\
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_ext2')

samples['Wjets'] = {
    'name'   : files,
    'weight' : mcCommonWeight,
    'FilesPerJob' : 4,
}




######## Vg ########
# files = nanoGetSampleFiles(mcDirectory, 'Wg_MADGRAPHMLM') + \
#     nanoGetSampleFiles(mcDirectory, 'Zg')

# samples['Vg'] = {
#     'name': files,
#     'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)',
#     'FilesPerJob': 5
# }
# addSampleWeight(samples, 'Vg', 'Zg', '(Sum$(GenPart_pdgId == 22 && TMath::Odd(GenPart_statusFlags) && GenPart_pt < 20.) == 0)')

######## VgS ########
# files = nanoGetSampleFiles(mcDirectory, 'Wg_MADGRAPHMLM') + \
#     nanoGetSampleFiles(mcDirectory, 'Zg') + \
#     nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin01')

# samples['VgS'] = {
#     'name': files,
#     'weight': mcCommonWeight + ' * (gstarLow * 0.94 + gstarHigh * 1.14)',
#     'FilesPerJob': 5,
#     'subsamples': {
#       'L': 'gstarLow',
#       'H': 'gstarHigh'
#     }
# }
# addSampleWeight(samples, 'VgS', 'Wg_MADGRAPHMLM', '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 0.1)')
# addSampleWeight(samples, 'VgS', 'Zg', '(Gen_ZGstar_mass > 0)*(Sum$(GenPart_pdgId == 22 && TMath::Odd(GenPart_statusFlags) && GenPart_pt < 20.) == 0)')
# addSampleWeight(samples, 'VgS', 'WZTo3LNu_mllmin01', '(Gen_ZGstar_mass > 0.1)')


# ############ VZ ############
#
# files = nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu_ext1') + \
#     nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Q') + \
#     nanoGetSampleFiles(mcDirectory, 'ZZTo4L_ext1') + \
#     nanoGetSampleFiles(mcDirectory, 'WZTo2L2Q')
#
# samples['VZ'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*1.11',
#     'FilesPerJob': 1
# }
#
# ########## VVV #########
#
# files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
#     nanoGetSampleFiles(mcDirectory, 'WZZ') + \
#     nanoGetSampleFiles(mcDirectory, 'WWZ') + \
#     nanoGetSampleFiles(mcDirectory, 'WWW')
# #+ nanoGetSampleFiles(mcDirectory, 'WWG'), #should this be included? or is it already taken into account in the WW sample?
#
# samples['VVV'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 4
# }

########### QCD ###########

# files = nanoGetSampleFiles(mcDirectory,'QCD_Pt-15to20_MuEnrichedPt5') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-20to30_MuEnrichedPt5') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-30to50_MuEnrichedPt5') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-50to80_MuEnrichedPt5') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-80to120_MuEnrichedPt5') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-120to170_MuEnrichedPt5') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-170to300_MuEnrichedPt5') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-15to20_EMEnriched') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-20to30_EMEnriched') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-30to50_EMEnriched') + \
#     nanoGetSampleFiles(mcDirectory,'QCD_Pt-50to80_EMEnriched')

    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-300to470_MuEnrichedPt5') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-470to600_MuEnrichedPt5') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-600to800_MuEnrichedPt5') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-800to1000_MuEnrichedPt5') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-1000toInf_MuEnrichedPt5') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-80to120_EMEnriched') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-120to170_EMEnriched') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-170to300_EMEnriched') + \
    # nanoGetSampleFiles(mcDirectory,'QCD_Pt-300toInf_EMEnriched')
file = nanoGetSampleFiles(mcDirectory,'QCD_Pt-15to20_MuEnrichedPt5') + \
       nanoGetSampleFiles(mcDirectory,'QCD_Pt-20toInf_MuEnrichedPt15') + \
       nanoGetSampleFiles(mcDirectory,'QCD_Pt-20to30_EMEnriched') + \
       nanoGetSampleFiles(mcDirectory,'QCD_Pt-30toInf_DoubleEMEnriched')

samples['FakeQCD'] = {
    'name'   :   files,
    'weight' : mcCommonWeight,
    'FilesPerJob' : 5,
}

# Filter efficiency for FakeQCD (https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns)
addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-15to20_MuEnrichedPt5', '0.0022')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-20to30_MuEnrichedPt5', '0.0045')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-30to50_MuEnrichedPt5', '0.00974')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-50to80_MuEnrichedPt5', '0.0196')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-80to120_MuEnrichedPt5', '0.0322')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-120to170_MuEnrichedPt5', '0.04518')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-170to300_MuEnrichedPt5', '0.0598')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-15to20_EMEnriched', '0.0096')  #missing sample
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-20to30_EMEnriched', '0.0088')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-30to50_EMEnriched', '0.0470')
# addSampleWeight(samples, 'FakeQCD', 'QCD_Pt-50to80_EMEnriched', '0.100')



###########################################
#############   SIGNALS  ##################
###########################################

#List_MX=[115,125,200,210,230,250,300,350,400,500,550,600,650,700,750,800,900,1500,2000,2500,3000,4000,5000]
List_MX=[500]

signals = []

####### ggH -> WW #################
for MX in massggh:
    samples['ggHWWlnuqq_M'+str(MX)] = {
        'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWToLNuQQ_M'+str(MX)),
        'weight': mcCommonWeight+'*RelW0.05',
        'FilesPerJob': 5
    }
    signals.append('ggHWWlnuqq_M'+str(MX))

############ VBF H->WW ############
for MX in massvbf:
    samples['qqHWWlnuqq_M'+str(MX)] = {
        'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWToLNuQQ_M'+str(MX)),
        'weight': mcCommonWeight+'*RelW0.05',
        'FilesPerJob': 5
    }
    signals.append('qqHWWlnuqq_M'+str(MX))

# ############ ZH H->WW ############
#
# samples['ZH_hww'] = {
#     'name':   nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125'),
#     'weight': mcCommonWeight,
#     'FilesPerJob': 4
# }
#
# signals.append('ZH_hww')
#
# samples['ggZH_hww'] = {
#     'name':   nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125'),
#     'weight': mcCommonWeight,
#     'FilesPerJob': 4
# }
#
# signals.append('ggZH_hww')
#
# ############ WH H->WW ############
#
# samples['WH_hww'] = {
#     'name':   nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125') + nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125'),
#     'weight': mcCommonWeight,
#     'FilesPerJob': 4
# }
#
# signals.append('WH_hww')
#
# ############ ttH ############
#
# samples['ttH_hww'] = {
#     'name':   nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
#     'weight': mcCommonWeight,
#     'FilesPerJob': 1
# }
#
# signals.append('ttH_hww')


###########################################
################## DATA ###################
###########################################

# samples['DATA'] = {
#   'name': [],
#   'weight': 'METFilter_DATA*LepWPCut',
#   'weights': [],
#   'isData': ['all'],
#   'FilesPerJob': 80
# }
#
# for _, sd in DataRun:
#   for pd in DataSets:
#     files = nanoGetSampleFiles(dataDirectory, pd + '_' + sd)
#     samples['DATA']['name'].extend(files)
#     samples['DATA']['weights'].extend([DataTrig[pd]] * len(files))
