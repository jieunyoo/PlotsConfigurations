# nuisances

#nuisances = {}

# name of samples here must match keys in samples.py 

# imported from samples.py:
# samples, treeBaseDir, mcProduction, mcSteps
# imported from cuts.py
# cuts

from LatinoAnalysis.Tools.commonTools import getSampleFiles, getBaseW, addSampleWeight

def nanoGetSampleFiles(inputDir, Sample):
    return getSampleFiles(inputDir, Sample, False, 'nanoLatino_')

try:
    mc_emb = [skey for skey in samples if skey != 'DATA' and skey != 'Dyveto' and not skey.startswith('Fake')]
    mc = [skey for skey in mc_emb if skey != 'Dyemb']
except NameError:
    mc = []
    mc_emb = []
    cuts = {}
    nuisances = {}
    useEmbeddedDY = True
    treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
    def makeMCDirectory(x=''):
        return ''

runDYveto = True

from LatinoAnalysis.Tools.HiggsXSection import HiggsXSection
HiggsXS = HiggsXSection()

cuts0j = []
cuts1j = []
cuts2j = []

for k in cuts:
  if 'categories' not in cuts[k]: continue
  for cat in cuts[k]['categories']:
    if '0j' in cat: cuts0j.append(k+'_'+cat)
    elif '1j' in cat: cuts1j.append(k+'_'+cat)
    elif '2j' in cat: cuts2j.append(k+'_'+cat)
    else: print 'WARNING: name of category does not contain on either 0j,1j,2j'

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

nuisances['lumi_Uncorrelated'] = {
    'name': 'lumi_13TeV_2018',
    'type': 'lnN',
    'samples': dict((skey, '1.015') for skey in mc if skey not in ['WW', 'top'])
}

nuisances['lumi_XYFact'] = {
    'name': 'lumi_13TeV_XYFact',
    'type': 'lnN',
    'samples': dict((skey, '1.02') for skey in mc if skey not in ['WW', 'top'])
}

nuisances['lumi_LScale'] = {
    'name': 'lumi_13TeV_LSCale',
    'type': 'lnN',
    'samples': dict((skey, '1.002') for skey in mc if skey not in ['WW', 'top'])
}

nuisances['lumi_CurrCalib'] = {
    'name': 'lumi_13TeV_CurrCalib',
    'type': 'lnN',
    'samples': dict((skey, '1.002') for skey in mc if skey not in ['WW', 'top'])
}

#### FAKES

nuisances['fake_syst_em'] = {
    'name': 'CMS_fake_syst_em',
    'type': 'lnN',
    'samples': {
        'Fake_em': '1.3'
    },
    'cutspost': lambda self, cuts: [cut for cut in cuts if 'me' not in cut],
}

nuisances['fake_syst_me'] = {
    'name': 'CMS_fake_syst_me',
    'type': 'lnN',
    'samples': {
        'Fake_me': '1.3'
    },
    'cutspost': lambda self, cuts: [cut for cut in cuts if 'em' not in cut],
}

nuisances['fake_ele'] = {
    'name': 'CMS_fake_e_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown']
    }
}

nuisances['fake_mu'] = {
    'name': 'CMS_fake_m_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWMuUp', 'fakeWMuDown'],
    }
}

nuisances['fake_mu_stat'] = {
    'name': 'CMS_fake_stat_m_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}

##### B-tagger

for shift in ['jes', 'lf', 'hf', 'hfstats1', 'hfstats2', 'lfstats1', 'lfstats2', 'cferr1', 'cferr2']:
    btag_syst = ['(btagSF%sup)/(btagSF)' % shift, '(btagSF%sdown)/(btagSF)' % shift]

    name = 'CMS_btag_%s' % shift
    if 'stats' in shift:
        name += '_2018'

    nuisances['btag_shape_%s' % shift] = {
        'name': name,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, btag_syst) for skey in mc),
    }

##### Trigger Efficiency

trig_syst = ['((TriggerEffWeight_2l_u)/(TriggerEffWeight_2l))*(TriggerEffWeight_2l>0.02) + (TriggerEffWeight_2l<=0.02)', '(TriggerEffWeight_2l_d)/(TriggerEffWeight_2l)']

nuisances['trigg'] = {
    'name': 'CMS_eff_hwwtrigger_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc_emb),
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc_emb),
}

nuisances['electronpt'] = {
    'name': 'CMS_scale_e_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'ElepTup',
    'mapDown': 'ElepTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('ElepTup_suffix'),
    'folderDown': makeMCDirectory('ElepTdo_suffix'),
    'AsLnN': '1'
}

if useEmbeddedDY:
  nuisances['electronpt_emb'] = {
    'name': 'CMS_scale_e_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp' : 'ElepTup',
    'mapDown': 'ElepTdo',
    'samples': {'Dyemb': ['1', '1']},
    'folderUp': treeBaseDir+'/Embedding2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__l2tightOR2018v7__Embedding__EmbElepTup_suffix/',
    'folderDown': treeBaseDir+'/Embedding2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__l2tightOR2018v7__Embedding__EmbElepTdo_suffix/',
    'AsLnN': '1'
  }

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc_emb),
}

nuisances['muonpt'] = {
    'name': 'CMS_scale_m_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'MupTup',
    'mapDown': 'MupTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('MupTup_suffix'),
    'folderDown': makeMCDirectory('MupTdo_suffix'),
    'AsLnN': '1'
}

if useEmbeddedDY:
  nuisances['muonpt_emb'] = {
    'name': 'CMS_scale_m_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp' : 'MupTup',
    'mapDown': 'MupTdo',
    'samples': {'Dyemb': ['1', '1']},
    'folderUp': treeBaseDir+'/Embedding2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__l2tightOR2018v7__Embedding__EmbMupTup_suffix/',
    'folderDown': treeBaseDir+'/Embedding2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__l2tightOR2018v7__Embedding__EmbMupTdo_suffix/',
    'AsLnN': '1'
  }

##### Jet energy scale
jes_systs = ['JESAbsolute','JESAbsolute_2018','JESBBEC1','JESBBEC1_2018','JESEC2','JESEC2_2018','JESFlavorQCD','JESHF','JESHF_2018','JESRelativeBal','JESRelativeSample_2018']

for js in jes_systs:
  if 'Absolute' in js: 
    folderup = makeMCDirectory('JESAbsoluteup_suffix')
    folderdo = makeMCDirectory('JESAbsolutedo_suffix')
  elif 'BBEC1' in js:
    folderup = makeMCDirectory('JESBBEC1up_suffix')
    folderdo = makeMCDirectory('JESBBEC1do_suffix')
  elif 'EC2' in js:
    folderup = makeMCDirectory('JESEC2up_suffix')
    folderdo = makeMCDirectory('JESEC2do_suffix')
  elif 'HF' in js:
    folderup = makeMCDirectory('JESHFup_suffix')
    folderdo = makeMCDirectory('JESHFdo_suffix')
  elif 'Relative' in js:
    folderup = makeMCDirectory('JESRelativeup_suffix')
    folderdo = makeMCDirectory('JESRelativedo_suffix')
  elif 'FlavorQCD' in js:
    folderup = makeMCDirectory('JESFlavorQCDup_suffix')
    folderdo = makeMCDirectory('JESFlavorQCDdo_suffix')

  nuisances[js] = {
      'name': 'CMS_scale_'+js,
      'kind': 'suffix',
      'type': 'shape',
      'mapUp': js+'up',
      'mapDown': js+'do',
      'samples': dict((skey, ['1', '1']) for skey in mc if skey not in ['VZ', 'Vg', 'VgS']), #FIXME
      'folderUp': folderup,
      'folderDown': folderdo,
      'AsLnN': '1'
  }

##### Jet energy resolution
nuisances['JER'] = {
    'name': 'CMS_res_j_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'JERup',
    'mapDown': 'JERdo',
    'samples': dict((skey, ['1', '1']) for skey in mc if skey not in ['VZ', 'Vg', 'VgS']), #FIXME
    'folderUp': makeMCDirectory('JERup_suffix'),
    'folderDown': makeMCDirectory('JERdo_suffix'),
    'AsLnN': '1'
}


##### MET energy scale

nuisances['met'] = {
    'name': 'CMS_scale_met_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'METup',
    'mapDown': 'METdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('METup_suffix'),
    'folderDown': makeMCDirectory('METdo_suffix'),
    'AsLnN': '1'
}

##### Di-Tau vetoing for embedding
if useEmbeddedDY: 
  if runDYveto:
    nuisances['embedveto']  = {
                    'name'  : 'CMS_embed_veto_2018',
                    'kind'  : 'weight',
                    'type'  : 'shape',
                    'samples'  : {
                       'Dyemb'    : ['1', '1'],
                       'Dyveto'   : ['0.1', '-0.1'],
                    }
             }
  '''
  else:
    # These hardcoded numbers have been obtained by running the full Dyveto (with runDYveto=True in samples.py) 
    # and computing the lnN uncertainty as variation of the up/down integral with respect to the nominal Dyemb integral
    unc_dict = {}
    unc_dict['hww2l2v_13TeV_me_pm_0j_pt2lt20']   =  '1.01407' 
    unc_dict['hww2l2v_13TeV_em_pm_0j_pt2ge20']   =  '1.02195'
    unc_dict['hww2l2v_13TeV_me_mp_0j_pt2ge20']   =  '1.02491'
    unc_dict['hww2l2v_13TeV_em_mp_0j_pt2lt20']   =  '1.01688'
    unc_dict['hww2l2v_13TeV_em_pm_0j_pt2lt20']   =  '1.03110'
    unc_dict['hww2l2v_13TeV_em_mp_0j_pt2ge20']   =  '1.02300'
    unc_dict['hww2l2v_13TeV_me_pm_0j_pt2ge20']   =  '1.02149'
    unc_dict['hww2l2v_13TeV_me_mp_0j_pt2lt20']   =  '1.02521'
    unc_dict['hww2l2v_13TeV_me_pm_1j_pt2lt20']   =  '1.01241'
    unc_dict['hww2l2v_13TeV_me_pm_1j_pt2ge20']   =  '1.01400'
    unc_dict['hww2l2v_13TeV_me_mp_1j_pt2ge20']   =  '1.01162'
    unc_dict['hww2l2v_13TeV_em_mp_1j_pt2lt20']   =  '1.00842'
    unc_dict['hww2l2v_13TeV_em_pm_1j_pt2lt20']   =  '1.00516'
    unc_dict['hww2l2v_13TeV_em_pm_1j_pt2ge20']   =  '1.01565'
    unc_dict['hww2l2v_13TeV_em_mp_1j_pt2ge20']   =  '1.01445'
    unc_dict['hww2l2v_13TeV_me_mp_1j_pt2lt20']   =  '1.00711'
    unc_dict['hww2l2v_13TeV_2j']                 =  '1.01211'
    unc_dict['hww2l2v_13TeV_dytt_0j']            =  '1.00339'
    unc_dict['hww2l2v_13TeV_dytt_1j']            =  '1.00172'
    unc_dict['hww2l2v_13TeV_dytt_2j']            =  '1.00267'
    unc_dict['hww2l2v_13TeV_top_0j']             =  '1.01575'
    unc_dict['hww2l2v_13TeV_top_1j']             =  '1.02345'
    unc_dict['hww2l2v_13TeV_top_2j']             =  '1.05881'
    unc_dict['hww2l2v_13TeV_ww_0j']              =  '1.06107'
    unc_dict['hww2l2v_13TeV_ww_1j']              =  '1.05379'
    unc_dict['hww2l2v_13TeV_ww_2j']              =  '1.03267'

    for category,uncertainty in unc_dict.iteritems():
      nuisances['embedveto_'+category]  = {
                      'name'  : 'CMS_embed_veto_2017',
                      'type'  : 'lnN',
                      'samples'  : {
                         'Dyemb'    : uncertainty,
                         },
                       'cuts': [category],
                     }
    '''

##### Pileup

nuisances['PU'] = {
    'name': 'CMS_PU_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'DY': ['0.993259983266*(puWeightUp/puWeight)', '0.997656381501*(puWeightDown/puWeight)'],
        'top': ['1.00331969187*(puWeightUp/puWeight)', '0.999199609528*(puWeightDown/puWeight)'],
        'WW': ['1.0033022059*(puWeightUp/puWeight)', '0.997085330608*(puWeightDown/puWeight)'],

	'VBF_H0PM':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0M_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0M_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0M_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0M_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0PH_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0PH_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0PH_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0PH_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0L1_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0L1_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0L1_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PM_H0L1_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0PM':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0M_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0M_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0M_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0M_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0PH_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0PH_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0PH_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0PH_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0L1_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0L1_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0L1_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0M_H0L1_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0PM':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0M_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0M_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0M_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0M_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0PH_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0PH_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0PH_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0PH_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0L1_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0L1_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0L1_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0Mf05_H0L1_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0PM':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0M_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0M_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0M_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0M_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0PH_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0PH_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0PH_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0PH_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0L1_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0L1_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0L1_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PH_H0L1_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0PM':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0M_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0M_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0M_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0M_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0PH_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0PH_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0PH_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0PH_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0L1_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0L1_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0L1_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0PHf05_H0L1_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0PM':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0M_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0M_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0M_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0M_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0PH_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0PH_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0PH_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0PH_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0L1_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0L1_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0L1_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1_H0L1_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0PM':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0M_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0M_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0M_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0M_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0PH_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0PH_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0PH_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0PH_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0L1_M0':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0L1_M1':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0L1_M2':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],
        'VBF_H0L1f05_H0L1_M3':['1.00374694528*(puWeightUp/puWeight)', '0.995878596852*(puWeightDown/puWeight)'],    

	'H0PM':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0M':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0Mf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PH':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PHf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1f05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PM_H0M':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PM_H0Mf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PM_H0PH':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PM_H0PHf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PM_H0L1':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PM_H0L1f05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0M_H0PM':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0M_H0Mf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0M_H0PH':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0M_H0PHf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0M_H0L1':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0M_H0L1f05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0Mf05_H0PM':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0Mf05_H0M':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0Mf05_H0PH':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0Mf05_H0PHf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0Mf05_H0L1':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0Mf05_H0L1f05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PH_H0PM':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PH_H0M':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PH_H0Mf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PH_H0PHf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PH_H0L1':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PH_H0L1f05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PHf05_H0PM':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PHf05_H0M':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PHf05_H0Mf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PHf05_H0PH':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PHf05_H0L1':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0PHf05_H0L1f05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1_H0PM':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1_H0M':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1_H0Mf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1_H0PH':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1_H0PHf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1_H0L1f05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1f05_H0PM':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1f05_H0M':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1f05_H0Mf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1f05_H0PH':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1f05_H0PHf05':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],
        'H0L1f05_H0L1':['1.0036768006*(puWeightUp/puWeight)', '0.995996570285*(puWeightDown/puWeight)'],

    },
    'AsLnN': '1',
}

### PU ID SF uncertainty
puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name': 'CMS_PUID_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, puid_syst) for skey in mc)
}

##### PS
nuisances['PS_ISR']  = {
    'name': 'PS_ISR',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc if skey not in ['Vg','VgS','WWewk']), #PSWeights are buggy for some samples, we add them back by hand below
}

nuisances['PS_FSR']  = {
    'name': 'PS_FSR',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc if skey not in ['Vg','VgS','WWewk']), #PSWeights are buggy for some samples, we add them back by hand below
}

## PS nuisances computed by hand as a function of nCleanGenJets using alternative samples (when available). Needed if nominal samples have buggy PSWeights
nuisances['PS_ISR_ForBuggySamples']  = {
    'name': 'PS_ISR',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Vg'     : ['1.00227428567253*(nCleanGenJet==0) + 1.00572014989997*(nCleanGenJet==1) + 0.970824885256465*(nCleanGenJet==2) + 0.927346068071086*(nCleanGenJet>=3)', '0.996488506572636*(nCleanGenJet==0) + 0.993582795375765*(nCleanGenJet==1) + 1.03643678934568*(nCleanGenJet==2) + 1.09735277266955*(nCleanGenJet>=3)'],
        'VgS'    : ['1.0000536116408023*(nCleanGenJet==0) + 1.0100100693580492*(nCleanGenJet==1) + 0.959068359375*(nCleanGenJet==2) + 0.9117049260469496*(nCleanGenJet>=3)', '0.9999367833485968*(nCleanGenJet==0) + 0.9873682892005163*(nCleanGenJet==1) + 1.0492717737268518*(nCleanGenJet==2) + 1.1176958835210322*(nCleanGenJet>=3)'],
    },
}

nuisances['PS_FSR_ForBuggySamples']  = {
    'name': 'PS_FSR',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Vg'     : ['0.999935529935028*(nCleanGenJet==0) + 0.997948255568351*(nCleanGenJet==1) + 1.00561645493085*(nCleanGenJet==2) + 1.0212896960035*(nCleanGenJet>=3)', '1.00757702771109*(nCleanGenJet==0) + 1.00256681166083*(nCleanGenJet==1) + 0.93676371569867*(nCleanGenJet==2) + 0.956448336052435*(nCleanGenJet>=3)'],
        'VgS'    : ['0.9976593177227735*(nCleanGenJet==0) + 1.0016125187585532*(nCleanGenJet==1) + 1.0049344618055556*(nCleanGenJet==2) + 1.0195631514301164*(nCleanGenJet>=3)', '1.0026951855766457*(nCleanGenJet==0) + 1.0008132148661049*(nCleanGenJet==1) + 1.003949291087963*(nCleanGenJet==2) + 0.9708160910230832*(nCleanGenJet>=3)'],
    },
}

# An overall 1.5% UE uncertainty will cover all the UEup/UEdo variations
# And we don't observe any dependency of UE variations on njet
nuisances['UE']  = {
                'name'  : 'UE_CP5',
                'skipCMS' : 1,
                'type': 'lnN',
                'samples': dict((skey, '1.015') for skey in mc), 
}

####### Generic "cross section uncertainties"

apply_on = {
    'top': [
        '(topGenPt * antitopGenPt <= 0.) * 1.0816 + (topGenPt * antitopGenPt > 0.)',
        '(topGenPt * antitopGenPt <= 0.) * 0.9184 + (topGenPt * antitopGenPt > 0.)'
    ]
}

nuisances['singleTopToTTbar'] = {
    'name': 'singleTopToTTbar',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': apply_on
}

## Top pT reweighting uncertainty
### Top pT reweighting uncertainty -> not needed if the DATA/MC agreement is within the uncertainties after reweighting
#nuisances['TopPtRew'] = {
#    'name': 'CMS_topPtRew',   # Theory uncertainty
#    'kind': 'weight',
#    'type': 'shape',
#    'samples': {'top': ["Top_pTrw*Top_pTrw", "1."]},
#    'symmetrize': True
#}

nuisances['VgStar'] = {
    'name': 'CMS_hww_VgStarScale',
    'type': 'lnN',
    'samples': {
        'VgS_L': '1.25'
    }
}

nuisances['VZ'] = {
    'name': 'CMS_hww_VZScale',
    'type': 'lnN',
    'samples': {
        'VgS_H': '1.16'
    }
}

###### pdf uncertainties

valuesggh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggH','125.09','pdf','sm')
valuesggzh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','pdf','sm')
valuesbbh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','bbH','125.09','pdf','sm')

nuisances['pdf_Higgs_gg'] = {
    'name': 'pdf_Higgs_gg',
    'samples': {

        'H0PM':valuesggh,
        'H0M':valuesggh,
        'H0Mf05':valuesggh,
        'H0PH':valuesggh,
        'H0PHf05':valuesggh,
        'H0L1':valuesggh,
        'H0L1f05':valuesggh,
        'H0PM_H0M':valuesggh,
        'H0PM_H0Mf05':valuesggh,
        'H0PM_H0PH':valuesggh,
        'H0PM_H0PHf05':valuesggh,
        'H0PM_H0L1':valuesggh,
        'H0PM_H0L1f05':valuesggh,
        'H0M_H0PM':valuesggh,
        'H0M_H0Mf05':valuesggh,
        'H0M_H0PH':valuesggh,
        'H0M_H0PHf05':valuesggh,
        'H0M_H0L1':valuesggh,
        'H0M_H0L1f05':valuesggh,
        'H0Mf05_H0PM':valuesggh,
        'H0Mf05_H0M':valuesggh,
        'H0Mf05_H0PH':valuesggh,
        'H0Mf05_H0PHf05':valuesggh,
        'H0Mf05_H0L1':valuesggh,
        'H0Mf05_H0L1f05':valuesggh,
        'H0PH_H0PM':valuesggh,
        'H0PH_H0M':valuesggh,
        'H0PH_H0Mf05':valuesggh,
        'H0PH_H0PHf05':valuesggh,
        'H0PH_H0L1':valuesggh,
        'H0PH_H0L1f05':valuesggh,
        'H0PHf05_H0PM':valuesggh,
        'H0PHf05_H0M':valuesggh,
        'H0PHf05_H0Mf05':valuesggh,
        'H0PHf05_H0PH':valuesggh,
        'H0PHf05_H0L1':valuesggh,
        'H0PHf05_H0L1f05':valuesggh,
        'H0L1_H0PM':valuesggh,
        'H0L1_H0M':valuesggh,
        'H0L1_H0Mf05':valuesggh,
        'H0L1_H0PH':valuesggh,
        'H0L1_H0PHf05':valuesggh,
        'H0L1_H0L1f05':valuesggh,
        'H0L1f05_H0PM':valuesggh,
        'H0L1f05_H0M':valuesggh,
        'H0L1f05_H0Mf05':valuesggh,
        'H0L1f05_H0PH':valuesggh,
        'H0L1f05_H0PHf05':valuesggh,
        'H0L1f05_H0L1':valuesggh,
        #'ggH_hww': valuesggh,
        #'ggH_htt': valuesggh,
        #'ggZH_hww': valuesggzh,
        #'bbH_hww': valuesbbh
    },
    'type': 'lnN',
}
'''
values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','pdf','sm')

nuisances['pdf_Higgs_ttH'] = {
    'name': 'pdf_Higgs_ttH',
    'samples': {
        'ttH_hww': values
    },
    'type': 'lnN',
}
'''
valuesqqh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','pdf','sm')
valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','pdf','sm')
valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','pdf','sm')

nuisances['pdf_Higgs_qqbar'] = {
    'name': 'pdf_Higgs_qqbar',
    'type': 'lnN',
    'samples': {
        #'qqH_hww': valuesqqh,
        #'qqH_htt': valuesqqh,

	'VBF_H0PM':valuesqqh,
        'VBF_H0M':valuesqqh,
        'VBF_H0Mf05':valuesqqh,
        'VBF_H0PH':valuesqqh,
        'VBF_H0PHf05':valuesqqh,
        'VBF_H0L1':valuesqqh,
        'VBF_H0L1f05':valuesqqh,
        'VBF_H0PM_H0M_M0':valuesqqh,
        'VBF_H0PM_H0M_M1':valuesqqh,
        'VBF_H0PM_H0M_M2':valuesqqh,
        'VBF_H0PM_H0M_M3':valuesqqh,
        'VBF_H0PM_H0PH_M0':valuesqqh,
        'VBF_H0PM_H0PH_M1':valuesqqh,
        'VBF_H0PM_H0PH_M2':valuesqqh,
        'VBF_H0PM_H0PH_M3':valuesqqh,
        'VBF_H0PM_H0L1_M0':valuesqqh,
        'VBF_H0PM_H0L1_M1':valuesqqh,
        'VBF_H0PM_H0L1_M2':valuesqqh,
        'VBF_H0PM_H0L1_M3':valuesqqh,
        'VBF_H0M_H0PM':valuesqqh,
        'VBF_H0M_H0M_M0':valuesqqh,
        'VBF_H0M_H0M_M1':valuesqqh,
        'VBF_H0M_H0M_M2':valuesqqh,
        'VBF_H0M_H0M_M3':valuesqqh,
        'VBF_H0M_H0PH_M0':valuesqqh,
        'VBF_H0M_H0PH_M1':valuesqqh,
        'VBF_H0M_H0PH_M2':valuesqqh,
        'VBF_H0M_H0PH_M3':valuesqqh,
        'VBF_H0M_H0L1_M0':valuesqqh,
        'VBF_H0M_H0L1_M1':valuesqqh,
        'VBF_H0M_H0L1_M2':valuesqqh,
        'VBF_H0M_H0L1_M3':valuesqqh,
        'VBF_H0Mf05_H0PM':valuesqqh,
        'VBF_H0Mf05_H0M_M0':valuesqqh,
        'VBF_H0Mf05_H0M_M1':valuesqqh,
        'VBF_H0Mf05_H0M_M2':valuesqqh,
        'VBF_H0Mf05_H0M_M3':valuesqqh,
        'VBF_H0Mf05_H0PH_M0':valuesqqh,
        'VBF_H0Mf05_H0PH_M1':valuesqqh,
        'VBF_H0Mf05_H0PH_M2':valuesqqh,
        'VBF_H0Mf05_H0PH_M3':valuesqqh,
        'VBF_H0Mf05_H0L1_M0':valuesqqh,
        'VBF_H0Mf05_H0L1_M1':valuesqqh,
        'VBF_H0Mf05_H0L1_M2':valuesqqh,
        'VBF_H0Mf05_H0L1_M3':valuesqqh,
        'VBF_H0PH_H0PM':valuesqqh,
        'VBF_H0PH_H0M_M0':valuesqqh,
        'VBF_H0PH_H0M_M1':valuesqqh,
        'VBF_H0PH_H0M_M2':valuesqqh,
        'VBF_H0PH_H0M_M3':valuesqqh,
        'VBF_H0PH_H0PH_M0':valuesqqh,
        'VBF_H0PH_H0PH_M1':valuesqqh,
        'VBF_H0PH_H0PH_M2':valuesqqh,
        'VBF_H0PH_H0PH_M3':valuesqqh,
        'VBF_H0PH_H0L1_M0':valuesqqh,
        'VBF_H0PH_H0L1_M1':valuesqqh,
        'VBF_H0PH_H0L1_M2':valuesqqh,
        'VBF_H0PH_H0L1_M3':valuesqqh,
        'VBF_H0PHf05_H0PM':valuesqqh,
        'VBF_H0PHf05_H0M_M0':valuesqqh,
        'VBF_H0PHf05_H0M_M1':valuesqqh,
        'VBF_H0PHf05_H0M_M2':valuesqqh,
        'VBF_H0PHf05_H0M_M3':valuesqqh,
        'VBF_H0PHf05_H0PH_M0':valuesqqh,
        'VBF_H0PHf05_H0PH_M1':valuesqqh,
        'VBF_H0PHf05_H0PH_M2':valuesqqh,
        'VBF_H0PHf05_H0PH_M3':valuesqqh,
        'VBF_H0PHf05_H0L1_M0':valuesqqh,
        'VBF_H0PHf05_H0L1_M1':valuesqqh,
        'VBF_H0PHf05_H0L1_M2':valuesqqh,
        'VBF_H0PHf05_H0L1_M3':valuesqqh,
        'VBF_H0L1_H0PM':valuesqqh,
        'VBF_H0L1_H0M_M0':valuesqqh,
        'VBF_H0L1_H0M_M1':valuesqqh,
        'VBF_H0L1_H0M_M2':valuesqqh,
        'VBF_H0L1_H0M_M3':valuesqqh,
        'VBF_H0L1_H0PH_M0':valuesqqh,
        'VBF_H0L1_H0PH_M1':valuesqqh,
        'VBF_H0L1_H0PH_M2':valuesqqh,
        'VBF_H0L1_H0PH_M3':valuesqqh,
        'VBF_H0L1_H0L1_M0':valuesqqh,
        'VBF_H0L1_H0L1_M1':valuesqqh,
        'VBF_H0L1_H0L1_M2':valuesqqh,
        'VBF_H0L1_H0L1_M3':valuesqqh,
        'VBF_H0L1f05_H0PM':valuesqqh,
        'VBF_H0L1f05_H0M_M0':valuesqqh,
        'VBF_H0L1f05_H0M_M1':valuesqqh,
        'VBF_H0L1f05_H0M_M2':valuesqqh,
        'VBF_H0L1f05_H0M_M3':valuesqqh,
        'VBF_H0L1f05_H0PH_M0':valuesqqh,
        'VBF_H0L1f05_H0PH_M1':valuesqqh,
        'VBF_H0L1f05_H0PH_M2':valuesqqh,
        'VBF_H0L1f05_H0PH_M3':valuesqqh,
        'VBF_H0L1f05_H0L1_M0':valuesqqh,
        'VBF_H0L1f05_H0L1_M1':valuesqqh,
        'VBF_H0L1f05_H0L1_M2':valuesqqh,
        'VBF_H0L1f05_H0L1_M3':valuesqqh,

        'WH_H0PM':valueswh,
        'WH_H0M':valueswh,
        'WH_H0Mf05':valueswh,
        'WH_H0PH':valueswh,
        'WH_H0PHf05':valueswh,
        'WH_H0L1':valueswh,
        'WH_H0L1f05':valueswh,
        'WH_H0PM_H0M_M0':valueswh,
        'WH_H0PM_H0M_M1':valueswh,
        'WH_H0PM_H0M_M2':valueswh,
        'WH_H0PM_H0M_M3':valueswh,
        'WH_H0PM_H0PH_M0':valueswh,
        'WH_H0PM_H0PH_M1':valueswh,
        'WH_H0PM_H0PH_M2':valueswh,
        'WH_H0PM_H0PH_M3':valueswh,
        'WH_H0PM_H0L1_M0':valueswh,
        'WH_H0PM_H0L1_M1':valueswh,
        'WH_H0PM_H0L1_M2':valueswh,
        'WH_H0PM_H0L1_M3':valueswh,
        'WH_H0M_H0PM':valueswh,
        'WH_H0M_H0M_M0':valueswh,
        'WH_H0M_H0M_M1':valueswh,
        'WH_H0M_H0M_M2':valueswh,
        'WH_H0M_H0M_M3':valueswh,
        'WH_H0M_H0PH_M0':valueswh,
        'WH_H0M_H0PH_M1':valueswh,
        'WH_H0M_H0PH_M2':valueswh,
        'WH_H0M_H0PH_M3':valueswh,
        'WH_H0M_H0L1_M0':valueswh,
        'WH_H0M_H0L1_M1':valueswh,
        'WH_H0M_H0L1_M2':valueswh,
        'WH_H0M_H0L1_M3':valueswh,
        'WH_H0Mf05_H0PM':valueswh,
        'WH_H0Mf05_H0M_M0':valueswh,
        'WH_H0Mf05_H0M_M1':valueswh,
        'WH_H0Mf05_H0M_M2':valueswh,
        'WH_H0Mf05_H0M_M3':valueswh,
        'WH_H0Mf05_H0PH_M0':valueswh,
        'WH_H0Mf05_H0PH_M1':valueswh,
        'WH_H0Mf05_H0PH_M2':valueswh,
        'WH_H0Mf05_H0PH_M3':valueswh,
        'WH_H0Mf05_H0L1_M0':valueswh,
        'WH_H0Mf05_H0L1_M1':valueswh,
        'WH_H0Mf05_H0L1_M2':valueswh,
        'WH_H0Mf05_H0L1_M3':valueswh,
        'WH_H0PH_H0PM':valueswh,
        'WH_H0PH_H0M_M0':valueswh,
        'WH_H0PH_H0M_M1':valueswh,
        'WH_H0PH_H0M_M2':valueswh,
        'WH_H0PH_H0M_M3':valueswh,
        'WH_H0PH_H0PH_M0':valueswh,
        'WH_H0PH_H0PH_M1':valueswh,
        'WH_H0PH_H0PH_M2':valueswh,
        'WH_H0PH_H0PH_M3':valueswh,
        'WH_H0PH_H0L1_M0':valueswh,
        'WH_H0PH_H0L1_M1':valueswh,
        'WH_H0PH_H0L1_M2':valueswh,
        'WH_H0PH_H0L1_M3':valueswh,
        'WH_H0PHf05_H0PM':valueswh,
        'WH_H0PHf05_H0M_M0':valueswh,
        'WH_H0PHf05_H0M_M1':valueswh,
        'WH_H0PHf05_H0M_M2':valueswh,
        'WH_H0PHf05_H0M_M3':valueswh,
        'WH_H0PHf05_H0PH_M0':valueswh,
        'WH_H0PHf05_H0PH_M1':valueswh,
        'WH_H0PHf05_H0PH_M2':valueswh,
        'WH_H0PHf05_H0PH_M3':valueswh,
        'WH_H0PHf05_H0L1_M0':valueswh,
        'WH_H0PHf05_H0L1_M1':valueswh,
        'WH_H0PHf05_H0L1_M2':valueswh,
        'WH_H0PHf05_H0L1_M3':valueswh,
        'WH_H0L1_H0PM':valueswh,
        'WH_H0L1_H0M_M0':valueswh,
        'WH_H0L1_H0M_M1':valueswh,
        'WH_H0L1_H0M_M2':valueswh,
        'WH_H0L1_H0M_M3':valueswh,
        'WH_H0L1_H0PH_M0':valueswh,
        'WH_H0L1_H0PH_M1':valueswh,
        'WH_H0L1_H0PH_M2':valueswh,
        'WH_H0L1_H0PH_M3':valueswh,
        'WH_H0L1_H0L1_M0':valueswh,
        'WH_H0L1_H0L1_M1':valueswh,
        'WH_H0L1_H0L1_M2':valueswh,
        'WH_H0L1_H0L1_M3':valueswh,
        'WH_H0L1f05_H0PM':valueswh,
        'WH_H0L1f05_H0M_M0':valueswh,
        'WH_H0L1f05_H0M_M1':valueswh,
        'WH_H0L1f05_H0M_M2':valueswh,
        'WH_H0L1f05_H0M_M3':valueswh,
        'WH_H0L1f05_H0PH_M0':valueswh,
        'WH_H0L1f05_H0PH_M1':valueswh,
        'WH_H0L1f05_H0PH_M2':valueswh,
        'WH_H0L1f05_H0PH_M3':valueswh,
        'WH_H0L1f05_H0L1_M0':valueswh,
        'WH_H0L1f05_H0L1_M1':valueswh,
        'WH_H0L1f05_H0L1_M2':valueswh,
        'WH_H0L1f05_H0L1_M3':valueswh,

        'ZH_H0PM':valueszh,
        'ZH_H0M':valueszh,
        'ZH_H0Mf05':valueszh,
        'ZH_H0PH':valueszh,
        'ZH_H0PHf05':valueszh,
        'ZH_H0L1':valueszh,
        'ZH_H0L1f05':valueszh,
        'ZH_H0PM_H0M_M0':valueszh,
        'ZH_H0PM_H0M_M1':valueszh,
        'ZH_H0PM_H0M_M2':valueszh,
        'ZH_H0PM_H0M_M3':valueszh,
        'ZH_H0PM_H0PH_M0':valueszh,
        'ZH_H0PM_H0PH_M1':valueszh,
        'ZH_H0PM_H0PH_M2':valueszh,
        'ZH_H0PM_H0PH_M3':valueszh,
        'ZH_H0PM_H0L1_M0':valueszh,
        'ZH_H0PM_H0L1_M1':valueszh,
        'ZH_H0PM_H0L1_M2':valueszh,
        'ZH_H0PM_H0L1_M3':valueszh,
        'ZH_H0M_H0PM':valueszh,
        'ZH_H0M_H0M_M0':valueszh,
        'ZH_H0M_H0M_M1':valueszh,
        'ZH_H0M_H0M_M2':valueszh,
        'ZH_H0M_H0M_M3':valueszh,
        'ZH_H0M_H0PH_M0':valueszh,
        'ZH_H0M_H0PH_M1':valueszh,
        'ZH_H0M_H0PH_M2':valueszh,
        'ZH_H0M_H0PH_M3':valueszh,
        'ZH_H0M_H0L1_M0':valueszh,
        'ZH_H0M_H0L1_M1':valueszh,
        'ZH_H0M_H0L1_M2':valueszh,
        'ZH_H0M_H0L1_M3':valueszh,
        'ZH_H0Mf05_H0PM':valueszh,
        'ZH_H0Mf05_H0M_M0':valueszh,
        'ZH_H0Mf05_H0M_M1':valueszh,
        'ZH_H0Mf05_H0M_M2':valueszh,
        'ZH_H0Mf05_H0M_M3':valueszh,
        'ZH_H0Mf05_H0PH_M0':valueszh,
        'ZH_H0Mf05_H0PH_M1':valueszh,
        'ZH_H0Mf05_H0PH_M2':valueszh,
        'ZH_H0Mf05_H0PH_M3':valueszh,
        'ZH_H0Mf05_H0L1_M0':valueszh,
        'ZH_H0Mf05_H0L1_M1':valueszh,
        'ZH_H0Mf05_H0L1_M2':valueszh,
        'ZH_H0Mf05_H0L1_M3':valueszh,
        'ZH_H0PH_H0PM':valueszh,
        'ZH_H0PH_H0M_M0':valueszh,
        'ZH_H0PH_H0M_M1':valueszh,
        'ZH_H0PH_H0M_M2':valueszh,
        'ZH_H0PH_H0M_M3':valueszh,
        'ZH_H0PH_H0PH_M0':valueszh,
        'ZH_H0PH_H0PH_M1':valueszh,
        'ZH_H0PH_H0PH_M2':valueszh,
        'ZH_H0PH_H0PH_M3':valueszh,
        'ZH_H0PH_H0L1_M0':valueszh,
        'ZH_H0PH_H0L1_M1':valueszh,
        'ZH_H0PH_H0L1_M2':valueszh,
        'ZH_H0PH_H0L1_M3':valueszh,
        'ZH_H0PHf05_H0PM':valueszh,
        'ZH_H0PHf05_H0M_M0':valueszh,
        'ZH_H0PHf05_H0M_M1':valueszh,
        'ZH_H0PHf05_H0M_M2':valueszh,
        'ZH_H0PHf05_H0M_M3':valueszh,
        'ZH_H0PHf05_H0PH_M0':valueszh,
        'ZH_H0PHf05_H0PH_M1':valueszh,
        'ZH_H0PHf05_H0PH_M2':valueszh,
        'ZH_H0PHf05_H0PH_M3':valueszh,
        'ZH_H0PHf05_H0L1_M0':valueszh,
        'ZH_H0PHf05_H0L1_M1':valueszh,
        'ZH_H0PHf05_H0L1_M2':valueszh,
        'ZH_H0PHf05_H0L1_M3':valueszh,
        'ZH_H0L1_H0PM':valueszh,
        'ZH_H0L1_H0M_M0':valueszh,
        'ZH_H0L1_H0M_M1':valueszh,
        'ZH_H0L1_H0M_M2':valueszh,
        'ZH_H0L1_H0M_M3':valueszh,
        'ZH_H0L1_H0PH_M0':valueszh,
        'ZH_H0L1_H0PH_M1':valueszh,
        'ZH_H0L1_H0PH_M2':valueszh,
        'ZH_H0L1_H0PH_M3':valueszh,
        'ZH_H0L1_H0L1_M0':valueszh,
        'ZH_H0L1_H0L1_M1':valueszh,
        'ZH_H0L1_H0L1_M2':valueszh,
        'ZH_H0L1_H0L1_M3':valueszh,
        'ZH_H0L1f05_H0PM':valueszh,
        'ZH_H0L1f05_H0M_M0':valueszh,
        'ZH_H0L1f05_H0M_M1':valueszh,
        'ZH_H0L1f05_H0M_M2':valueszh,
        'ZH_H0L1f05_H0M_M3':valueszh,
        'ZH_H0L1f05_H0PH_M0':valueszh,
        'ZH_H0L1f05_H0PH_M1':valueszh,
        'ZH_H0L1f05_H0PH_M2':valueszh,
        'ZH_H0L1f05_H0PH_M3':valueszh,
        'ZH_H0L1f05_H0L1_M0':valueszh,
        'ZH_H0L1f05_H0L1_M1':valueszh,
        'ZH_H0L1f05_H0L1_M2':valueszh,
        'ZH_H0L1f05_H0L1_M3':valueszh,

        #'WH_hww': valueswh,
        #'WH_htt': valueswh,
        #'ZH_hww': valueszh,
        #'ZH_htt': valueszh
    },
}

nuisances['pdf_qqbar'] = {
    'name': 'pdf_qqbar',
    'type': 'lnN',
    'samples': {
        'Vg': '1.04',
        'VZ': '1.04',  # PDF: 0.0064 / 0.1427 = 0.0448493
        'VgS': '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
    },
}

nuisances['pdf_Higgs_gg_ACCEPT'] = {
    'name': 'pdf_Higgs_gg_ACCEPT',
    'samples': {
        #'ggH_hww': '1.006',
        'H0PM':'1.006',
        'H0M':'1.006',
        'H0Mf05':'1.006',
        'H0PH':'1.006',
        'H0PHf05':'1.006',
        'H0L1':'1.006',
        'H0L1f05':'1.006',
        'H0PM_H0M':'1.006',
        'H0PM_H0Mf05':'1.006',
        'H0PM_H0PH':'1.006',
        'H0PM_H0PHf05':'1.006',
        'H0PM_H0L1':'1.006',
        'H0PM_H0L1f05':'1.006',
        'H0M_H0PM':'1.006',
        'H0M_H0Mf05':'1.006',
        'H0M_H0PH':'1.006',
        'H0M_H0PHf05':'1.006',
        'H0M_H0L1':'1.006',
        'H0M_H0L1f05':'1.006',
        'H0Mf05_H0PM':'1.006',
        'H0Mf05_H0M':'1.006',
        'H0Mf05_H0PH':'1.006',
        'H0Mf05_H0PHf05':'1.006',
        'H0Mf05_H0L1':'1.006',
        'H0Mf05_H0L1f05':'1.006',
        'H0PH_H0PM':'1.006',
        'H0PH_H0M':'1.006',
        'H0PH_H0Mf05':'1.006',
        'H0PH_H0PHf05':'1.006',
        'H0PH_H0L1':'1.006',
        'H0PH_H0L1f05':'1.006',
        'H0PHf05_H0PM':'1.006',
        'H0PHf05_H0M':'1.006',
        'H0PHf05_H0Mf05':'1.006',
        'H0PHf05_H0PH':'1.006',
        'H0PHf05_H0L1':'1.006',
        'H0PHf05_H0L1f05':'1.006',
        'H0L1_H0PM':'1.006',
        'H0L1_H0M':'1.006',
        'H0L1_H0Mf05':'1.006',
        'H0L1_H0PH':'1.006',
        'H0L1_H0PHf05':'1.006',
        'H0L1_H0L1f05':'1.006',
        'H0L1f05_H0PM':'1.006',
        'H0L1f05_H0M':'1.006',
        'H0L1f05_H0Mf05':'1.006',
        'H0L1f05_H0PH':'1.006',
        'H0L1f05_H0PHf05':'1.006',
        'H0L1f05_H0L1':'1.006',

        #'ggH_htt': '1.006',
        #'ggZH_hww': '1.006',
        #'bbH_hww': '1.006'
    },
    'type': 'lnN',
}

nuisances['pdf_gg_ACCEPT'] = {
    'name': 'pdf_gg_ACCEPT',
    'samples': {
        'ggWW': '1.006',
    },
    'type': 'lnN',
}

nuisances['pdf_Higgs_qqbar_ACCEPT'] = {
    'name': 'pdf_Higgs_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        #'qqH_hww': '1.002',

        'VBF_H0PM':'1.002',
        'VBF_H0M':'1.002',
        'VBF_H0Mf05':'1.002',
        'VBF_H0PH':'1.002',
        'VBF_H0PHf05':'1.002',
        'VBF_H0L1':'1.002',
        'VBF_H0L1f05':'1.002',
        'VBF_H0PM_H0M_M0':'1.002',
        'VBF_H0PM_H0M_M1':'1.002',
        'VBF_H0PM_H0M_M2':'1.002',
        'VBF_H0PM_H0M_M3':'1.002',
        'VBF_H0PM_H0PH_M0':'1.002',
        'VBF_H0PM_H0PH_M1':'1.002',
        'VBF_H0PM_H0PH_M2':'1.002',
        'VBF_H0PM_H0PH_M3':'1.002',
        'VBF_H0PM_H0L1_M0':'1.002',
        'VBF_H0PM_H0L1_M1':'1.002',
        'VBF_H0PM_H0L1_M2':'1.002',
        'VBF_H0PM_H0L1_M3':'1.002',
        'VBF_H0M_H0PM':'1.002',
        'VBF_H0M_H0M_M0':'1.002',
        'VBF_H0M_H0M_M1':'1.002',
        'VBF_H0M_H0M_M2':'1.002',
        'VBF_H0M_H0M_M3':'1.002',
        'VBF_H0M_H0PH_M0':'1.002',
        'VBF_H0M_H0PH_M1':'1.002',
        'VBF_H0M_H0PH_M2':'1.002',
        'VBF_H0M_H0PH_M3':'1.002',
        'VBF_H0M_H0L1_M0':'1.002',
        'VBF_H0M_H0L1_M1':'1.002',
        'VBF_H0M_H0L1_M2':'1.002',
        'VBF_H0M_H0L1_M3':'1.002',
        'VBF_H0Mf05_H0PM':'1.002',
        'VBF_H0Mf05_H0M_M0':'1.002',
        'VBF_H0Mf05_H0M_M1':'1.002',
        'VBF_H0Mf05_H0M_M2':'1.002',
        'VBF_H0Mf05_H0M_M3':'1.002',
        'VBF_H0Mf05_H0PH_M0':'1.002',
        'VBF_H0Mf05_H0PH_M1':'1.002',
        'VBF_H0Mf05_H0PH_M2':'1.002',
        'VBF_H0Mf05_H0PH_M3':'1.002',
        'VBF_H0Mf05_H0L1_M0':'1.002',
        'VBF_H0Mf05_H0L1_M1':'1.002',
        'VBF_H0Mf05_H0L1_M2':'1.002',
        'VBF_H0Mf05_H0L1_M3':'1.002',
        'VBF_H0PH_H0PM':'1.002',
        'VBF_H0PH_H0M_M0':'1.002',
        'VBF_H0PH_H0M_M1':'1.002',
        'VBF_H0PH_H0M_M2':'1.002',
        'VBF_H0PH_H0M_M3':'1.002',
        'VBF_H0PH_H0PH_M0':'1.002',
        'VBF_H0PH_H0PH_M1':'1.002',
        'VBF_H0PH_H0PH_M2':'1.002',
        'VBF_H0PH_H0PH_M3':'1.002',
        'VBF_H0PH_H0L1_M0':'1.002',
        'VBF_H0PH_H0L1_M1':'1.002',
        'VBF_H0PH_H0L1_M2':'1.002',
        'VBF_H0PH_H0L1_M3':'1.002',
        'VBF_H0PHf05_H0PM':'1.002',
        'VBF_H0PHf05_H0M_M0':'1.002',
        'VBF_H0PHf05_H0M_M1':'1.002',
        'VBF_H0PHf05_H0M_M2':'1.002',
        'VBF_H0PHf05_H0M_M3':'1.002',
        'VBF_H0PHf05_H0PH_M0':'1.002',
        'VBF_H0PHf05_H0PH_M1':'1.002',
        'VBF_H0PHf05_H0PH_M2':'1.002',
        'VBF_H0PHf05_H0PH_M3':'1.002',
        'VBF_H0PHf05_H0L1_M0':'1.002',
        'VBF_H0PHf05_H0L1_M1':'1.002',
        'VBF_H0PHf05_H0L1_M2':'1.002',
        'VBF_H0PHf05_H0L1_M3':'1.002',
        'VBF_H0L1_H0PM':'1.002',
        'VBF_H0L1_H0M_M0':'1.002',
        'VBF_H0L1_H0M_M1':'1.002',
        'VBF_H0L1_H0M_M2':'1.002',
        'VBF_H0L1_H0M_M3':'1.002',
        'VBF_H0L1_H0PH_M0':'1.002',
        'VBF_H0L1_H0PH_M1':'1.002',
        'VBF_H0L1_H0PH_M2':'1.002',
        'VBF_H0L1_H0PH_M3':'1.002',
        'VBF_H0L1_H0L1_M0':'1.002',
        'VBF_H0L1_H0L1_M1':'1.002',
        'VBF_H0L1_H0L1_M2':'1.002',
        'VBF_H0L1_H0L1_M3':'1.002',
        'VBF_H0L1f05_H0PM':'1.002',
        'VBF_H0L1f05_H0M_M0':'1.002',
        'VBF_H0L1f05_H0M_M1':'1.002',
        'VBF_H0L1f05_H0M_M2':'1.002',
        'VBF_H0L1f05_H0M_M3':'1.002',
        'VBF_H0L1f05_H0PH_M0':'1.002',
        'VBF_H0L1f05_H0PH_M1':'1.002',
        'VBF_H0L1f05_H0PH_M2':'1.002',
        'VBF_H0L1f05_H0PH_M3':'1.002',
        'VBF_H0L1f05_H0L1_M0':'1.002',
        'VBF_H0L1f05_H0L1_M1':'1.002',
        'VBF_H0L1f05_H0L1_M2':'1.002',
        'VBF_H0L1f05_H0L1_M3':'1.002',

        'WH_H0PM':'1.003',
        'WH_H0M':'1.003',
        'WH_H0Mf05':'1.003',
        'WH_H0PH':'1.003',
        'WH_H0PHf05':'1.003',
        'WH_H0L1':'1.003',
        'WH_H0L1f05':'1.003',
        'WH_H0PM_H0M_M0':'1.003',
        'WH_H0PM_H0M_M1':'1.003',
        'WH_H0PM_H0M_M2':'1.003',
        'WH_H0PM_H0M_M3':'1.003',
        'WH_H0PM_H0PH_M0':'1.003',
        'WH_H0PM_H0PH_M1':'1.003',
        'WH_H0PM_H0PH_M2':'1.003',
        'WH_H0PM_H0PH_M3':'1.003',
        'WH_H0PM_H0L1_M0':'1.003',
        'WH_H0PM_H0L1_M1':'1.003',
        'WH_H0PM_H0L1_M2':'1.003',
        'WH_H0PM_H0L1_M3':'1.003',
        'WH_H0M_H0PM':'1.003',
        'WH_H0M_H0M_M0':'1.003',
        'WH_H0M_H0M_M1':'1.003',
        'WH_H0M_H0M_M2':'1.003',
        'WH_H0M_H0M_M3':'1.003',
        'WH_H0M_H0PH_M0':'1.003',
        'WH_H0M_H0PH_M1':'1.003',
        'WH_H0M_H0PH_M2':'1.003',
        'WH_H0M_H0PH_M3':'1.003',
        'WH_H0M_H0L1_M0':'1.003',
        'WH_H0M_H0L1_M1':'1.003',
        'WH_H0M_H0L1_M2':'1.003',
        'WH_H0M_H0L1_M3':'1.003',
        'WH_H0Mf05_H0PM':'1.003',
        'WH_H0Mf05_H0M_M0':'1.003',
        'WH_H0Mf05_H0M_M1':'1.003',
        'WH_H0Mf05_H0M_M2':'1.003',
        'WH_H0Mf05_H0M_M3':'1.003',
        'WH_H0Mf05_H0PH_M0':'1.003',
        'WH_H0Mf05_H0PH_M1':'1.003',
        'WH_H0Mf05_H0PH_M2':'1.003',
        'WH_H0Mf05_H0PH_M3':'1.003',
        'WH_H0Mf05_H0L1_M0':'1.003',
        'WH_H0Mf05_H0L1_M1':'1.003',
        'WH_H0Mf05_H0L1_M2':'1.003',
        'WH_H0Mf05_H0L1_M3':'1.003',
        'WH_H0PH_H0PM':'1.003',
        'WH_H0PH_H0M_M0':'1.003',
        'WH_H0PH_H0M_M1':'1.003',
        'WH_H0PH_H0M_M2':'1.003',
        'WH_H0PH_H0M_M3':'1.003',
        'WH_H0PH_H0PH_M0':'1.003',
        'WH_H0PH_H0PH_M1':'1.003',
        'WH_H0PH_H0PH_M2':'1.003',
        'WH_H0PH_H0PH_M3':'1.003',
        'WH_H0PH_H0L1_M0':'1.003',
        'WH_H0PH_H0L1_M1':'1.003',
        'WH_H0PH_H0L1_M2':'1.003',
        'WH_H0PH_H0L1_M3':'1.003',
        'WH_H0PHf05_H0PM':'1.003',
        'WH_H0PHf05_H0M_M0':'1.003',
        'WH_H0PHf05_H0M_M1':'1.003',
        'WH_H0PHf05_H0M_M2':'1.003',
        'WH_H0PHf05_H0M_M3':'1.003',
        'WH_H0PHf05_H0PH_M0':'1.003',
        'WH_H0PHf05_H0PH_M1':'1.003',
        'WH_H0PHf05_H0PH_M2':'1.003',
        'WH_H0PHf05_H0PH_M3':'1.003',
        'WH_H0PHf05_H0L1_M0':'1.003',
        'WH_H0PHf05_H0L1_M1':'1.003',
        'WH_H0PHf05_H0L1_M2':'1.003',
        'WH_H0PHf05_H0L1_M3':'1.003',
        'WH_H0L1_H0PM':'1.003',
        'WH_H0L1_H0M_M0':'1.003',
        'WH_H0L1_H0M_M1':'1.003',
        'WH_H0L1_H0M_M2':'1.003',
        'WH_H0L1_H0M_M3':'1.003',
        'WH_H0L1_H0PH_M0':'1.003',
        'WH_H0L1_H0PH_M1':'1.003',
        'WH_H0L1_H0PH_M2':'1.003',
        'WH_H0L1_H0PH_M3':'1.003',
        'WH_H0L1_H0L1_M0':'1.003',
        'WH_H0L1_H0L1_M1':'1.003',
        'WH_H0L1_H0L1_M2':'1.003',
        'WH_H0L1_H0L1_M3':'1.003',
        'WH_H0L1f05_H0PM':'1.003',
        'WH_H0L1f05_H0M_M0':'1.003',
        'WH_H0L1f05_H0M_M1':'1.003',
        'WH_H0L1f05_H0M_M2':'1.003',
        'WH_H0L1f05_H0M_M3':'1.003',
        'WH_H0L1f05_H0PH_M0':'1.003',
        'WH_H0L1f05_H0PH_M1':'1.003',
        'WH_H0L1f05_H0PH_M2':'1.003',
        'WH_H0L1f05_H0PH_M3':'1.003',
        'WH_H0L1f05_H0L1_M0':'1.003',
        'WH_H0L1f05_H0L1_M1':'1.003',
        'WH_H0L1f05_H0L1_M2':'1.003',
        'WH_H0L1f05_H0L1_M3':'1.003',

        'ZH_H0PM':'1.002',
        'ZH_H0M':'1.002',
        'ZH_H0Mf05':'1.002',
        'ZH_H0PH':'1.002',
        'ZH_H0PHf05':'1.002',
        'ZH_H0L1':'1.002',
        'ZH_H0L1f05':'1.002',
        'ZH_H0PM_H0M_M0':'1.002',
        'ZH_H0PM_H0M_M1':'1.002',
        'ZH_H0PM_H0M_M2':'1.002',
        'ZH_H0PM_H0M_M3':'1.002',
        'ZH_H0PM_H0PH_M0':'1.002',
        'ZH_H0PM_H0PH_M1':'1.002',
        'ZH_H0PM_H0PH_M2':'1.002',
        'ZH_H0PM_H0PH_M3':'1.002',
        'ZH_H0PM_H0L1_M0':'1.002',
        'ZH_H0PM_H0L1_M1':'1.002',
        'ZH_H0PM_H0L1_M2':'1.002',
        'ZH_H0PM_H0L1_M3':'1.002',
        'ZH_H0M_H0PM':'1.002',
        'ZH_H0M_H0M_M0':'1.002',
        'ZH_H0M_H0M_M1':'1.002',
        'ZH_H0M_H0M_M2':'1.002',
        'ZH_H0M_H0M_M3':'1.002',
        'ZH_H0M_H0PH_M0':'1.002',
        'ZH_H0M_H0PH_M1':'1.002',
        'ZH_H0M_H0PH_M2':'1.002',
        'ZH_H0M_H0PH_M3':'1.002',
        'ZH_H0M_H0L1_M0':'1.002',
        'ZH_H0M_H0L1_M1':'1.002',
        'ZH_H0M_H0L1_M2':'1.002',
        'ZH_H0M_H0L1_M3':'1.002',
        'ZH_H0Mf05_H0PM':'1.002',
        'ZH_H0Mf05_H0M_M0':'1.002',
        'ZH_H0Mf05_H0M_M1':'1.002',
        'ZH_H0Mf05_H0M_M2':'1.002',
        'ZH_H0Mf05_H0M_M3':'1.002',
        'ZH_H0Mf05_H0PH_M0':'1.002',
        'ZH_H0Mf05_H0PH_M1':'1.002',
        'ZH_H0Mf05_H0PH_M2':'1.002',
        'ZH_H0Mf05_H0PH_M3':'1.002',
        'ZH_H0Mf05_H0L1_M0':'1.002',
        'ZH_H0Mf05_H0L1_M1':'1.002',
        'ZH_H0Mf05_H0L1_M2':'1.002',
        'ZH_H0Mf05_H0L1_M3':'1.002',
        'ZH_H0PH_H0PM':'1.002',
        'ZH_H0PH_H0M_M0':'1.002',
        'ZH_H0PH_H0M_M1':'1.002',
        'ZH_H0PH_H0M_M2':'1.002',
        'ZH_H0PH_H0M_M3':'1.002',
        'ZH_H0PH_H0PH_M0':'1.002',
        'ZH_H0PH_H0PH_M1':'1.002',
        'ZH_H0PH_H0PH_M2':'1.002',
        'ZH_H0PH_H0PH_M3':'1.002',
        'ZH_H0PH_H0L1_M0':'1.002',
        'ZH_H0PH_H0L1_M1':'1.002',
        'ZH_H0PH_H0L1_M2':'1.002',
        'ZH_H0PH_H0L1_M3':'1.002',
        'ZH_H0PHf05_H0PM':'1.002',
        'ZH_H0PHf05_H0M_M0':'1.002',
        'ZH_H0PHf05_H0M_M1':'1.002',
        'ZH_H0PHf05_H0M_M2':'1.002',
        'ZH_H0PHf05_H0M_M3':'1.002',
        'ZH_H0PHf05_H0PH_M0':'1.002',
        'ZH_H0PHf05_H0PH_M1':'1.002',
        'ZH_H0PHf05_H0PH_M2':'1.002',
        'ZH_H0PHf05_H0PH_M3':'1.002',
        'ZH_H0PHf05_H0L1_M0':'1.002',
        'ZH_H0PHf05_H0L1_M1':'1.002',
        'ZH_H0PHf05_H0L1_M2':'1.002',
        'ZH_H0PHf05_H0L1_M3':'1.002',
        'ZH_H0L1_H0PM':'1.002',
        'ZH_H0L1_H0M_M0':'1.002',
        'ZH_H0L1_H0M_M1':'1.002',
        'ZH_H0L1_H0M_M2':'1.002',
        'ZH_H0L1_H0M_M3':'1.002',
        'ZH_H0L1_H0PH_M0':'1.002',
        'ZH_H0L1_H0PH_M1':'1.002',
        'ZH_H0L1_H0PH_M2':'1.002',
        'ZH_H0L1_H0PH_M3':'1.002',
        'ZH_H0L1_H0L1_M0':'1.002',
        'ZH_H0L1_H0L1_M1':'1.002',
        'ZH_H0L1_H0L1_M2':'1.002',
        'ZH_H0L1_H0L1_M3':'1.002',
        'ZH_H0L1f05_H0PM':'1.002',
        'ZH_H0L1f05_H0M_M0':'1.002',
        'ZH_H0L1f05_H0M_M1':'1.002',
        'ZH_H0L1f05_H0M_M2':'1.002',
        'ZH_H0L1f05_H0M_M3':'1.002',
        'ZH_H0L1f05_H0PH_M0':'1.002',
        'ZH_H0L1f05_H0PH_M1':'1.002',
        'ZH_H0L1f05_H0PH_M2':'1.002',
        'ZH_H0L1f05_H0PH_M3':'1.002',
        'ZH_H0L1f05_H0L1_M0':'1.002',
        'ZH_H0L1f05_H0L1_M1':'1.002',
        'ZH_H0L1f05_H0L1_M2':'1.002',
        'ZH_H0L1f05_H0L1_M3':'1.002',
 
        #'qqH_htt': '1.002',
        #'WH_hww': '1.003',
        #'WH_htt': '1.003',
        #'ZH_hww': '1.002',
        #'ZH_htt': '1.002',
    },
}

nuisances['pdf_qqbar_ACCEPT'] = {
    'name': 'pdf_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        'VZ': '1.001',
    },
}

##### Renormalization & factorization scales

## Shape nuisance due to QCD scale variations for DY
# LHE scale variation weights (w_var / w_nominal)

## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
variations = ['LHEScaleWeight[0]', 'LHEScaleWeight[1]', 'LHEScaleWeight[3]', 'LHEScaleWeight[Length$(LHEScaleWeight)-4]', 'LHEScaleWeight[Length$(LHEScaleWeight)-2]', 'LHEScaleWeight[Length$(LHEScaleWeight)-1]']
topvars0j = []
topvars1j = []
topvars2j = []

## Factors computed to renormalize the top scale variations such that the integral is not changed in each RECO jet bin (we have rateParams for that)
topScaleNormFactors0j = {'LHEScaleWeight[3]': 1.0026322046882807, 'LHEScaleWeight[0]': 1.0761381504953040, 'LHEScaleWeight[1]': 1.0758902481739956, 'LHEScaleWeight[Length$(LHEScaleWeight)-1]': 0.9225780960271310, 'LHEScaleWeight[Length$(LHEScaleWeight)-4]': 1.0006689791003040, 'LHEScaleWeight[Length$(LHEScaleWeight)-2]': 0.9242759920995479}
topScaleNormFactors1j = {'LHEScaleWeight[3]': 1.0088973745933350, 'LHEScaleWeight[0]': 1.0858717477880675, 'LHEScaleWeight[1]': 1.0809970696561464, 'LHEScaleWeight[Length$(LHEScaleWeight)-1]': 0.9115155831354494, 'LHEScaleWeight[Length$(LHEScaleWeight)-4]': 0.9950909615738225, 'LHEScaleWeight[Length$(LHEScaleWeight)-2]': 0.9194241285459210}
topScaleNormFactors2j = {'LHEScaleWeight[3]': 1.0236911155246506, 'LHEScaleWeight[0]': 1.1249360990045656, 'LHEScaleWeight[1]': 1.1054771659922622, 'LHEScaleWeight[Length$(LHEScaleWeight)-1]': 0.8819750427294990, 'LHEScaleWeight[Length$(LHEScaleWeight)-4]': 0.9819208264038879, 'LHEScaleWeight[Length$(LHEScaleWeight)-2]': 0.9025818187649589}

for var in variations:
  topvars0j.append(var+'/'+str(topScaleNormFactors0j[var]))
  topvars1j.append(var+'/'+str(topScaleNormFactors1j[var]))
  topvars2j.append(var+'/'+str(topScaleNormFactors2j[var]))

## QCD scale nuisances for top are decorrelated for each RECO jet bin: the QCD scale is different for different jet multiplicities so it doesn't make sense to correlate them
nuisances['QCDscale_top_0j']  = {
    'name'  : 'QCDscale_top_0j',
    'skipCMS' : 1,
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'cutspost' : lambda self, cuts: [cut for cut in cuts if '0j' in cut],
    'samples'  : {
       'top' : topvars0j,
    }
}

nuisances['QCDscale_top_1j']  = {
    'name'  : 'QCDscale_top_1j',
    'skipCMS' : 1,
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'cutspost' : lambda self, cuts: [cut for cut in cuts if '1j' in cut],
    'samples'  : {
       'top' : topvars1j,
    }
}
'''
nuisances['QCDscale_top_2j']  = {
    'name'  : 'QCDscale_top_2j',
    'skipCMS' : 1,
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'cutspost' : lambda self, cuts: [cut for cut in cuts if '2j' in cut],
    'samples'  : {
       'top' : topvars2j,
    }
}
'''
nuisances['QCDscale_V'] = {
    'name': 'QCDscale_V',
    'skipCMS': 1,
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': {'DY': variations},
    'AsLnN': '1'
}

nuisances['QCDscale_VV'] = {
    'name': 'QCDscale_VV',
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': {
        'Vg': variations,
        'VZ': variations,
        'VgS': variations
    }
}

# ggww and interference
nuisances['QCDscale_ggVV'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggWW': '1.15',
    },
}

# NLL resummation variations
nuisances['WWresum0j']  = {
  'name'  : 'CMS_hww_WWresum_0j',
  'skipCMS' : 1,
  'kind'  : 'weight',
  'type'  : 'shape',
  'samples'  : {
     'WW'   : ['nllW_Rup/nllW', 'nllW_Rdown/nllW'],
   },
  'cutspost'  : lambda self, cuts: [cut for cut in cuts if '0j' in cut]
} 

nuisances['WWqscale0j']  = {
   'name'  : 'CMS_hww_WWqscale_0j',
   'skipCMS' : 1,
   'kind'  : 'weight',
   'type'  : 'shape',
   'samples'  : {
      'WW'   : ['nllW_Qup/nllW', 'nllW_Qdown/nllW'],
    },
   'cutspost'  : lambda self, cuts: [cut for cut in cuts if '0j' in cut]
}

nuisances['WWresum1j']  = {
  'name'  : 'CMS_hww_WWresum_1j',
  'skipCMS' : 1,
  'kind'  : 'weight',
  'type'  : 'shape',
  'samples'  : {
     'WW'   : ['nllW_Rup/nllW', 'nllW_Rdown/nllW'],
   },
  'cutspost'  : lambda self, cuts: [cut for cut in cuts if '1j' in cut]
} 

nuisances['WWqscale1j']  = {
   'name'  : 'CMS_hww_WWqscale_1j',
   'skipCMS' : 1,
   'kind'  : 'weight',
   'type'  : 'shape',
   'samples'  : {
      'WW'   : ['nllW_Qup/nllW', 'nllW_Qdown/nllW'],
    },
   'cutspost'  : lambda self, cuts: [cut for cut in cuts if '1j' in cut]
}
'''
nuisances['WWresum2j']  = {
  'name'  : 'CMS_hww_WWresum_2j',
  'skipCMS' : 1,
  'kind'  : 'weight',
  'type'  : 'shape',
  'samples'  : {
     'WW'   : ['nllW_Rup/nllW', 'nllW_Rdown/nllW'],
   },
  'cutspost'  : lambda self, cuts: [cut for cut in cuts if '2j' in cut]
} 

nuisances['WWqscale2j']  = {
   'name'  : 'CMS_hww_WWqscale_2j',
   'skipCMS' : 1,
   'kind'  : 'weight',
   'type'  : 'shape',
   'samples'  : {
      'WW'   : ['nllW_Qup/nllW', 'nllW_Qdown/nllW'],
    },
   'cutspost'  : lambda self, cuts: [cut for cut in cuts if '2j' in cut]
}
'''
# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_DY'] = {
    'name': 'CMS_hww_CRSR_accept_DY',
    'type': 'lnN',
    'samples': {'DY': '1.02'},
    'cuts': ['hww2l2v_13TeV_dytt_0j','hww2l2v_13TeV_dytt_1j'],
    #'cuts': [cut for cut in cuts if '_CR_' in cut],
    #'cutspost': (lambda self, cuts: [cut for cut in cuts if '_dytt_' in cut]),
}

# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_top'] = {
    'name': 'CMS_hww_CRSR_accept_top',
    'type': 'lnN',
    'samples': {'top': '1.01'},
    'cuts': ['hww2l2v_13TeV_top_0j','hww2l2v_13TeV_top_1j'],
    #'cuts': [cut for cut in cuts if '_CR_' in cut],
    #'cutspost': (lambda self, cuts: [cut for cut in cuts if '_top_' in cut]),
}

# Theory uncertainty for ggH
#
#
#   THU_ggH_Mu, THU_ggH_Res, THU_ggH_Mig01, THU_ggH_Mig12, THU_ggH_VBF2j, THU_ggH_VBF3j, THU_ggH_PT60, THU_ggH_PT120, THU_ggH_qmtop
#
#   see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SignalModelingTools

thus = [
    ('THU_ggH_Mu', 'ggH_mu_2'),
    ('THU_ggH_Res', 'ggH_res_2'),
    ('THU_ggH_Mig01', 'ggH_mig01_2'),
    ('THU_ggH_Mig12', 'ggH_mig12_2'),
    ('THU_ggH_VBF2j', 'ggH_VBF2j_2'),
    ('THU_ggH_VBF3j', 'ggH_VBF3j_2'),
    ('THU_ggH_PT60', 'ggH_pT60_2'),
    ('THU_ggH_PT120', 'ggH_pT120_2'),
    ('THU_ggH_qmtop', 'ggH_qmtop_2')
]


for name, vname in thus:
    updown = [vname, '2.-%s' % vname]
    
    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
          #'ggH_hww': updown,
           'H0PM':updown,
           'H0M':updown,
           'H0Mf05':updown,
           'H0PH':updown,
           'H0PHf05':updown,
           'H0L1':updown,
           'H0L1f05':updown,
           'H0PM_H0M':updown,
           'H0PM_H0Mf05':updown,
           'H0PM_H0PH':updown,
           'H0PM_H0PHf05':updown,
           'H0PM_H0L1':updown,
           'H0PM_H0L1f05':updown,
           'H0M_H0PM':updown,
           'H0M_H0Mf05':updown,
           'H0M_H0PH':updown,
           'H0M_H0PHf05':updown,
           'H0M_H0L1':updown,
           'H0M_H0L1f05':updown,
           'H0Mf05_H0PM':updown,
           'H0Mf05_H0M':updown,
           'H0Mf05_H0PH':updown,
           'H0Mf05_H0PHf05':updown,
           'H0Mf05_H0L1':updown,
           'H0Mf05_H0L1f05':updown,
           'H0PH_H0PM':updown,
           'H0PH_H0M':updown,
           'H0PH_H0Mf05':updown,
           'H0PH_H0PHf05':updown,
           'H0PH_H0L1':updown,
           'H0PH_H0L1f05':updown,
           'H0PHf05_H0PM':updown,
           'H0PHf05_H0M':updown,
           'H0PHf05_H0Mf05':updown,
           'H0PHf05_H0PH':updown,
           'H0PHf05_H0L1':updown,
           'H0PHf05_H0L1f05':updown,
           'H0L1_H0PM':updown,
           'H0L1_H0M':updown,
           'H0L1_H0Mf05':updown,
           'H0L1_H0PH':updown,
           'H0L1_H0PHf05':updown,
           'H0L1_H0L1f05':updown,
           'H0L1f05_H0PM':updown,
           'H0L1f05_H0M':updown,
           'H0L1f05_H0Mf05':updown,
           'H0L1f05_H0PH':updown,
           'H0L1f05_H0PHf05':updown,
           'H0L1f05_H0L1':updown,


          #'ggH_htt': updown
        }
    }
# Theory uncertainty for qqH 
#
#
#   see https://gitlab.cern.ch/LHCHIGGSXS/LHCHXSWG2/STXS/VBF-Uncertainties/-/blob/master/qq2Hqq_uncert_scheme.cpp

thusQQH = [
  ("THU_qqH_YIELD","qqH_YIELD"),
  ("THU_qqH_PTH200","qqH_PTH200"),
  ("THU_qqH_Mjj60","qqH_Mjj60"),
  ("THU_qqH_Mjj120","qqH_Mjj120"),
  ("THU_qqH_Mjj350","qqH_Mjj350"),
  ("THU_qqH_Mjj700","qqH_Mjj700"),
  ("THU_qqH_Mjj1000","qqH_Mjj1000"),
  ("THU_qqH_Mjj1500","qqH_Mjj1500"),
  ("THU_qqH_PTH25","qqH_PTH25"),
  ("THU_qqH_JET01","qqH_JET01"),
  ("THU_qqH_EWK","qqH_EWK"),
]

for name, vname in thusQQH:
    updown = [vname, '2.-%s' % vname]
    
    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
          #'qqH_hww': updown,

           'VBF_H0PM':updown,
           'VBF_H0M':updown,
           'VBF_H0Mf05':updown,
           'VBF_H0PH':updown,
           'VBF_H0PHf05':updown,
           'VBF_H0L1':updown,
           'VBF_H0L1f05':updown,
           'VBF_H0PM_H0M_M0':updown,
           'VBF_H0PM_H0M_M1':updown,
           'VBF_H0PM_H0M_M2':updown,
           'VBF_H0PM_H0M_M3':updown,
           'VBF_H0PM_H0PH_M0':updown,
           'VBF_H0PM_H0PH_M1':updown,
           'VBF_H0PM_H0PH_M2':updown,
           'VBF_H0PM_H0PH_M3':updown,
           'VBF_H0PM_H0L1_M0':updown,
           'VBF_H0PM_H0L1_M1':updown,
           'VBF_H0PM_H0L1_M2':updown,
           'VBF_H0PM_H0L1_M3':updown,
           'VBF_H0M_H0PM':updown,
           'VBF_H0M_H0M_M0':updown,
           'VBF_H0M_H0M_M1':updown,
           'VBF_H0M_H0M_M2':updown,
           'VBF_H0M_H0M_M3':updown,
           'VBF_H0M_H0PH_M0':updown,
           'VBF_H0M_H0PH_M1':updown,
           'VBF_H0M_H0PH_M2':updown,
           'VBF_H0M_H0PH_M3':updown,
           'VBF_H0M_H0L1_M0':updown,
           'VBF_H0M_H0L1_M1':updown,
           'VBF_H0M_H0L1_M2':updown,
           'VBF_H0M_H0L1_M3':updown,
           'VBF_H0Mf05_H0PM':updown,
           'VBF_H0Mf05_H0M_M0':updown,
           'VBF_H0Mf05_H0M_M1':updown,
           'VBF_H0Mf05_H0M_M2':updown,
           'VBF_H0Mf05_H0M_M3':updown,
           'VBF_H0Mf05_H0PH_M0':updown,
           'VBF_H0Mf05_H0PH_M1':updown,
           'VBF_H0Mf05_H0PH_M2':updown,
           'VBF_H0Mf05_H0PH_M3':updown,
           'VBF_H0Mf05_H0L1_M0':updown,
           'VBF_H0Mf05_H0L1_M1':updown,
           'VBF_H0Mf05_H0L1_M2':updown,
           'VBF_H0Mf05_H0L1_M3':updown,
           'VBF_H0PH_H0PM':updown,
           'VBF_H0PH_H0M_M0':updown,
           'VBF_H0PH_H0M_M1':updown,
           'VBF_H0PH_H0M_M2':updown,
           'VBF_H0PH_H0M_M3':updown,
           'VBF_H0PH_H0PH_M0':updown,
           'VBF_H0PH_H0PH_M1':updown,
           'VBF_H0PH_H0PH_M2':updown,
           'VBF_H0PH_H0PH_M3':updown,
           'VBF_H0PH_H0L1_M0':updown,
           'VBF_H0PH_H0L1_M1':updown,
           'VBF_H0PH_H0L1_M2':updown,
           'VBF_H0PH_H0L1_M3':updown,
           'VBF_H0PHf05_H0PM':updown,
           'VBF_H0PHf05_H0M_M0':updown,
           'VBF_H0PHf05_H0M_M1':updown,
           'VBF_H0PHf05_H0M_M2':updown,
           'VBF_H0PHf05_H0M_M3':updown,
           'VBF_H0PHf05_H0PH_M0':updown,
           'VBF_H0PHf05_H0PH_M1':updown,
           'VBF_H0PHf05_H0PH_M2':updown,
           'VBF_H0PHf05_H0PH_M3':updown,
           'VBF_H0PHf05_H0L1_M0':updown,
           'VBF_H0PHf05_H0L1_M1':updown,
           'VBF_H0PHf05_H0L1_M2':updown,
           'VBF_H0PHf05_H0L1_M3':updown,
           'VBF_H0L1_H0PM':updown,
           'VBF_H0L1_H0M_M0':updown,
           'VBF_H0L1_H0M_M1':updown,
           'VBF_H0L1_H0M_M2':updown,
           'VBF_H0L1_H0M_M3':updown,
           'VBF_H0L1_H0PH_M0':updown,
           'VBF_H0L1_H0PH_M1':updown,
           'VBF_H0L1_H0PH_M2':updown,
           'VBF_H0L1_H0PH_M3':updown,
           'VBF_H0L1_H0L1_M0':updown,
           'VBF_H0L1_H0L1_M1':updown,
           'VBF_H0L1_H0L1_M2':updown,
           'VBF_H0L1_H0L1_M3':updown,
           'VBF_H0L1f05_H0PM':updown,
           'VBF_H0L1f05_H0M_M0':updown,
           'VBF_H0L1f05_H0M_M1':updown,
           'VBF_H0L1f05_H0M_M2':updown,
           'VBF_H0L1f05_H0M_M3':updown,
           'VBF_H0L1f05_H0PH_M0':updown,
           'VBF_H0L1f05_H0PH_M1':updown,
           'VBF_H0L1f05_H0PH_M2':updown,
           'VBF_H0L1f05_H0PH_M3':updown,
           'VBF_H0L1f05_H0L1_M0':updown,
           'VBF_H0L1f05_H0L1_M1':updown,
           'VBF_H0L1f05_H0L1_M2':updown,
           'VBF_H0L1f05_H0L1_M3':updown,

        }
    }

#### QCD scale uncertainties for Higgs signals other than ggH

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','scale','sm')

nuisances['QCDscale_qqH'] = {
    'name': 'QCDscale_qqH', 
    'samples': {
        #'qqH_hww': values,

	'VBF_H0PM':values,
        'VBF_H0M':values,
        'VBF_H0Mf05':values,
        'VBF_H0PH':values,
        'VBF_H0PHf05':values,
        'VBF_H0L1':values,
        'VBF_H0L1f05':values,
        'VBF_H0PM_H0M_M0':values,
        'VBF_H0PM_H0M_M1':values,
        'VBF_H0PM_H0M_M2':values,
        'VBF_H0PM_H0M_M3':values,
        'VBF_H0PM_H0PH_M0':values,
        'VBF_H0PM_H0PH_M1':values,
        'VBF_H0PM_H0PH_M2':values,
        'VBF_H0PM_H0PH_M3':values,
        'VBF_H0PM_H0L1_M0':values,
        'VBF_H0PM_H0L1_M1':values,
        'VBF_H0PM_H0L1_M2':values,
        'VBF_H0PM_H0L1_M3':values,
        'VBF_H0M_H0PM':values,
        'VBF_H0M_H0M_M0':values,
        'VBF_H0M_H0M_M1':values,
        'VBF_H0M_H0M_M2':values,
        'VBF_H0M_H0M_M3':values,
        'VBF_H0M_H0PH_M0':values,
        'VBF_H0M_H0PH_M1':values,
        'VBF_H0M_H0PH_M2':values,
        'VBF_H0M_H0PH_M3':values,
        'VBF_H0M_H0L1_M0':values,
        'VBF_H0M_H0L1_M1':values,
        'VBF_H0M_H0L1_M2':values,
        'VBF_H0M_H0L1_M3':values,
        'VBF_H0Mf05_H0PM':values,
        'VBF_H0Mf05_H0M_M0':values,
        'VBF_H0Mf05_H0M_M1':values,
        'VBF_H0Mf05_H0M_M2':values,
        'VBF_H0Mf05_H0M_M3':values,
        'VBF_H0Mf05_H0PH_M0':values,
        'VBF_H0Mf05_H0PH_M1':values,
        'VBF_H0Mf05_H0PH_M2':values,
        'VBF_H0Mf05_H0PH_M3':values,
        'VBF_H0Mf05_H0L1_M0':values,
        'VBF_H0Mf05_H0L1_M1':values,
        'VBF_H0Mf05_H0L1_M2':values,
        'VBF_H0Mf05_H0L1_M3':values,
        'VBF_H0PH_H0PM':values,
        'VBF_H0PH_H0M_M0':values,
        'VBF_H0PH_H0M_M1':values,
        'VBF_H0PH_H0M_M2':values,
        'VBF_H0PH_H0M_M3':values,
        'VBF_H0PH_H0PH_M0':values,
        'VBF_H0PH_H0PH_M1':values,
        'VBF_H0PH_H0PH_M2':values,
        'VBF_H0PH_H0PH_M3':values,
        'VBF_H0PH_H0L1_M0':values,
        'VBF_H0PH_H0L1_M1':values,
        'VBF_H0PH_H0L1_M2':values,
        'VBF_H0PH_H0L1_M3':values,
        'VBF_H0PHf05_H0PM':values,
        'VBF_H0PHf05_H0M_M0':values,
        'VBF_H0PHf05_H0M_M1':values,
        'VBF_H0PHf05_H0M_M2':values,
        'VBF_H0PHf05_H0M_M3':values,
        'VBF_H0PHf05_H0PH_M0':values,
        'VBF_H0PHf05_H0PH_M1':values,
        'VBF_H0PHf05_H0PH_M2':values,
        'VBF_H0PHf05_H0PH_M3':values,
        'VBF_H0PHf05_H0L1_M0':values,
        'VBF_H0PHf05_H0L1_M1':values,
        'VBF_H0PHf05_H0L1_M2':values,
        'VBF_H0PHf05_H0L1_M3':values,
        'VBF_H0L1_H0PM':values,
        'VBF_H0L1_H0M_M0':values,
        'VBF_H0L1_H0M_M1':values,
        'VBF_H0L1_H0M_M2':values,
        'VBF_H0L1_H0M_M3':values,
        'VBF_H0L1_H0PH_M0':values,
        'VBF_H0L1_H0PH_M1':values,
        'VBF_H0L1_H0PH_M2':values,
        'VBF_H0L1_H0PH_M3':values,
        'VBF_H0L1_H0L1_M0':values,
        'VBF_H0L1_H0L1_M1':values,
        'VBF_H0L1_H0L1_M2':values,
        'VBF_H0L1_H0L1_M3':values,
        'VBF_H0L1f05_H0PM':values,
        'VBF_H0L1f05_H0M_M0':values,
        'VBF_H0L1f05_H0M_M1':values,
        'VBF_H0L1f05_H0M_M2':values,
        'VBF_H0L1f05_H0M_M3':values,
        'VBF_H0L1f05_H0PH_M0':values,
        'VBF_H0L1f05_H0PH_M1':values,
        'VBF_H0L1f05_H0PH_M2':values,
        'VBF_H0L1f05_H0PH_M3':values,
        'VBF_H0L1f05_H0L1_M0':values,
        'VBF_H0L1f05_H0L1_M1':values,
        'VBF_H0L1f05_H0L1_M2':values,
        'VBF_H0L1f05_H0L1_M3':values,
        #'qqH_htt': values
    },
    'type': 'lnN'
}

valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','scale','sm')
valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','scale','sm')

nuisances['QCDscale_VH'] = {
    'name': 'QCDscale_VH', 
    'samples': {
        #'WH_hww': valueswh,

        'WH_H0PM':valueswh,
        'WH_H0M':valueswh,
        'WH_H0Mf05':valueswh,
        'WH_H0PH':valueswh,
        'WH_H0PHf05':valueswh,
        'WH_H0L1':valueswh,
        'WH_H0L1f05':valueswh,
        'WH_H0PM_H0M_M0':valueswh,
        'WH_H0PM_H0M_M1':valueswh,
        'WH_H0PM_H0M_M2':valueswh,
        'WH_H0PM_H0M_M3':valueswh,
        'WH_H0PM_H0PH_M0':valueswh,
        'WH_H0PM_H0PH_M1':valueswh,
        'WH_H0PM_H0PH_M2':valueswh,
        'WH_H0PM_H0PH_M3':valueswh,
        'WH_H0PM_H0L1_M0':valueswh,
        'WH_H0PM_H0L1_M1':valueswh,
        'WH_H0PM_H0L1_M2':valueswh,
        'WH_H0PM_H0L1_M3':valueswh,
        'WH_H0M_H0PM':valueswh,
        'WH_H0M_H0M_M0':valueswh,
        'WH_H0M_H0M_M1':valueswh,
        'WH_H0M_H0M_M2':valueswh,
        'WH_H0M_H0M_M3':valueswh,
        'WH_H0M_H0PH_M0':valueswh,
        'WH_H0M_H0PH_M1':valueswh,
        'WH_H0M_H0PH_M2':valueswh,
        'WH_H0M_H0PH_M3':valueswh,
        'WH_H0M_H0L1_M0':valueswh,
        'WH_H0M_H0L1_M1':valueswh,
        'WH_H0M_H0L1_M2':valueswh,
        'WH_H0M_H0L1_M3':valueswh,
        'WH_H0Mf05_H0PM':valueswh,
        'WH_H0Mf05_H0M_M0':valueswh,
        'WH_H0Mf05_H0M_M1':valueswh,
        'WH_H0Mf05_H0M_M2':valueswh,
        'WH_H0Mf05_H0M_M3':valueswh,
        'WH_H0Mf05_H0PH_M0':valueswh,
        'WH_H0Mf05_H0PH_M1':valueswh,
        'WH_H0Mf05_H0PH_M2':valueswh,
        'WH_H0Mf05_H0PH_M3':valueswh,
        'WH_H0Mf05_H0L1_M0':valueswh,
        'WH_H0Mf05_H0L1_M1':valueswh,
        'WH_H0Mf05_H0L1_M2':valueswh,
        'WH_H0Mf05_H0L1_M3':valueswh,
        'WH_H0PH_H0PM':valueswh,
        'WH_H0PH_H0M_M0':valueswh,
        'WH_H0PH_H0M_M1':valueswh,
        'WH_H0PH_H0M_M2':valueswh,
        'WH_H0PH_H0M_M3':valueswh,
        'WH_H0PH_H0PH_M0':valueswh,
        'WH_H0PH_H0PH_M1':valueswh,
        'WH_H0PH_H0PH_M2':valueswh,
        'WH_H0PH_H0PH_M3':valueswh,
        'WH_H0PH_H0L1_M0':valueswh,
        'WH_H0PH_H0L1_M1':valueswh,
        'WH_H0PH_H0L1_M2':valueswh,
        'WH_H0PH_H0L1_M3':valueswh,
        'WH_H0PHf05_H0PM':valueswh,
        'WH_H0PHf05_H0M_M0':valueswh,
        'WH_H0PHf05_H0M_M1':valueswh,
        'WH_H0PHf05_H0M_M2':valueswh,
        'WH_H0PHf05_H0M_M3':valueswh,
        'WH_H0PHf05_H0PH_M0':valueswh,
        'WH_H0PHf05_H0PH_M1':valueswh,
        'WH_H0PHf05_H0PH_M2':valueswh,
        'WH_H0PHf05_H0PH_M3':valueswh,
        'WH_H0PHf05_H0L1_M0':valueswh,
        'WH_H0PHf05_H0L1_M1':valueswh,
        'WH_H0PHf05_H0L1_M2':valueswh,
        'WH_H0PHf05_H0L1_M3':valueswh,
        'WH_H0L1_H0PM':valueswh,
        'WH_H0L1_H0M_M0':valueswh,
        'WH_H0L1_H0M_M1':valueswh,
        'WH_H0L1_H0M_M2':valueswh,
        'WH_H0L1_H0M_M3':valueswh,
        'WH_H0L1_H0PH_M0':valueswh,
        'WH_H0L1_H0PH_M1':valueswh,
        'WH_H0L1_H0PH_M2':valueswh,
        'WH_H0L1_H0PH_M3':valueswh,
        'WH_H0L1_H0L1_M0':valueswh,
        'WH_H0L1_H0L1_M1':valueswh,
        'WH_H0L1_H0L1_M2':valueswh,
        'WH_H0L1_H0L1_M3':valueswh,
        'WH_H0L1f05_H0PM':valueswh,
        'WH_H0L1f05_H0M_M0':valueswh,
        'WH_H0L1f05_H0M_M1':valueswh,
        'WH_H0L1f05_H0M_M2':valueswh,
        'WH_H0L1f05_H0M_M3':valueswh,
        'WH_H0L1f05_H0PH_M0':valueswh,
        'WH_H0L1f05_H0PH_M1':valueswh,
        'WH_H0L1f05_H0PH_M2':valueswh,
        'WH_H0L1f05_H0PH_M3':valueswh,
        'WH_H0L1f05_H0L1_M0':valueswh,
        'WH_H0L1f05_H0L1_M1':valueswh,
        'WH_H0L1f05_H0L1_M2':valueswh,
        'WH_H0L1f05_H0L1_M3':valueswh,

        'ZH_H0PM':valueszh,
        'ZH_H0M':valueszh,
        'ZH_H0Mf05':valueszh,
        'ZH_H0PH':valueszh,
        'ZH_H0PHf05':valueszh,
        'ZH_H0L1':valueszh,
        'ZH_H0L1f05':valueszh,
        'ZH_H0PM_H0M_M0':valueszh,
        'ZH_H0PM_H0M_M1':valueszh,
        'ZH_H0PM_H0M_M2':valueszh,
        'ZH_H0PM_H0M_M3':valueszh,
        'ZH_H0PM_H0PH_M0':valueszh,
        'ZH_H0PM_H0PH_M1':valueszh,
        'ZH_H0PM_H0PH_M2':valueszh,
        'ZH_H0PM_H0PH_M3':valueszh,
        'ZH_H0PM_H0L1_M0':valueszh,
        'ZH_H0PM_H0L1_M1':valueszh,
        'ZH_H0PM_H0L1_M2':valueszh,
        'ZH_H0PM_H0L1_M3':valueszh,
        'ZH_H0M_H0PM':valueszh,
        'ZH_H0M_H0M_M0':valueszh,
        'ZH_H0M_H0M_M1':valueszh,
        'ZH_H0M_H0M_M2':valueszh,
        'ZH_H0M_H0M_M3':valueszh,
        'ZH_H0M_H0PH_M0':valueszh,
        'ZH_H0M_H0PH_M1':valueszh,
        'ZH_H0M_H0PH_M2':valueszh,
        'ZH_H0M_H0PH_M3':valueszh,
        'ZH_H0M_H0L1_M0':valueszh,
        'ZH_H0M_H0L1_M1':valueszh,
        'ZH_H0M_H0L1_M2':valueszh,
        'ZH_H0M_H0L1_M3':valueszh,
        'ZH_H0Mf05_H0PM':valueszh,
        'ZH_H0Mf05_H0M_M0':valueszh,
        'ZH_H0Mf05_H0M_M1':valueszh,
        'ZH_H0Mf05_H0M_M2':valueszh,
        'ZH_H0Mf05_H0M_M3':valueszh,
        'ZH_H0Mf05_H0PH_M0':valueszh,
        'ZH_H0Mf05_H0PH_M1':valueszh,
        'ZH_H0Mf05_H0PH_M2':valueszh,
        'ZH_H0Mf05_H0PH_M3':valueszh,
        'ZH_H0Mf05_H0L1_M0':valueszh,
        'ZH_H0Mf05_H0L1_M1':valueszh,
        'ZH_H0Mf05_H0L1_M2':valueszh,
        'ZH_H0Mf05_H0L1_M3':valueszh,
        'ZH_H0PH_H0PM':valueszh,
        'ZH_H0PH_H0M_M0':valueszh,
        'ZH_H0PH_H0M_M1':valueszh,
        'ZH_H0PH_H0M_M2':valueszh,
        'ZH_H0PH_H0M_M3':valueszh,
        'ZH_H0PH_H0PH_M0':valueszh,
        'ZH_H0PH_H0PH_M1':valueszh,
        'ZH_H0PH_H0PH_M2':valueszh,
        'ZH_H0PH_H0PH_M3':valueszh,
        'ZH_H0PH_H0L1_M0':valueszh,
        'ZH_H0PH_H0L1_M1':valueszh,
        'ZH_H0PH_H0L1_M2':valueszh,
        'ZH_H0PH_H0L1_M3':valueszh,
        'ZH_H0PHf05_H0PM':valueszh,
        'ZH_H0PHf05_H0M_M0':valueszh,
        'ZH_H0PHf05_H0M_M1':valueszh,
        'ZH_H0PHf05_H0M_M2':valueszh,
        'ZH_H0PHf05_H0M_M3':valueszh,
        'ZH_H0PHf05_H0PH_M0':valueszh,
        'ZH_H0PHf05_H0PH_M1':valueszh,
        'ZH_H0PHf05_H0PH_M2':valueszh,
        'ZH_H0PHf05_H0PH_M3':valueszh,
        'ZH_H0PHf05_H0L1_M0':valueszh,
        'ZH_H0PHf05_H0L1_M1':valueszh,
        'ZH_H0PHf05_H0L1_M2':valueszh,
        'ZH_H0PHf05_H0L1_M3':valueszh,
        'ZH_H0L1_H0PM':valueszh,
        'ZH_H0L1_H0M_M0':valueszh,
        'ZH_H0L1_H0M_M1':valueszh,
        'ZH_H0L1_H0M_M2':valueszh,
        'ZH_H0L1_H0M_M3':valueszh,
        'ZH_H0L1_H0PH_M0':valueszh,
        'ZH_H0L1_H0PH_M1':valueszh,
        'ZH_H0L1_H0PH_M2':valueszh,
        'ZH_H0L1_H0PH_M3':valueszh,
        'ZH_H0L1_H0L1_M0':valueszh,
        'ZH_H0L1_H0L1_M1':valueszh,
        'ZH_H0L1_H0L1_M2':valueszh,
        'ZH_H0L1_H0L1_M3':valueszh,
        'ZH_H0L1f05_H0PM':valueszh,
        'ZH_H0L1f05_H0M_M0':valueszh,
        'ZH_H0L1f05_H0M_M1':valueszh,
        'ZH_H0L1f05_H0M_M2':valueszh,
        'ZH_H0L1f05_H0M_M3':valueszh,
        'ZH_H0L1f05_H0PH_M0':valueszh,
        'ZH_H0L1f05_H0PH_M1':valueszh,
        'ZH_H0L1f05_H0PH_M2':valueszh,
        'ZH_H0L1f05_H0PH_M3':valueszh,
        'ZH_H0L1f05_H0L1_M0':valueszh,
        'ZH_H0L1f05_H0L1_M1':valueszh,
        'ZH_H0L1f05_H0L1_M2':valueszh,
        'ZH_H0L1f05_H0L1_M3':valueszh,

        #'WH_htt': valueswh,
        #'ZH_hww': valueszh,
        #'ZH_htt': valueszh
    },
    'type': 'lnN',
}
'''
values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','scale','sm')

nuisances['QCDscale_ggZH'] = {
    'name': 'QCDscale_ggZH', 
    'samples': {
        'ggZH_hww': values
    },
    'type': 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','scale','sm')

nuisances['QCDscale_ttH'] = {
    'name': 'QCDscale_ttH',
    'samples': {
        'ttH_hww': values
    },
    'type': 'lnN',
}
'''
nuisances['QCDscale_WWewk'] = {
    'name': 'QCDscale_WWewk',
    'samples': {
        'WWewk': '1.11',
    },
    'type': 'lnN'
}

nuisances['QCDscale_qqbar_ACCEPT'] = {
    'name': 'QCDscale_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        #'qqH_hww': '1.003',

	'VBF_H0PM':'1.003',
        'VBF_H0M':'1.003',
        'VBF_H0Mf05':'1.003',
        'VBF_H0PH':'1.003',
        'VBF_H0PHf05':'1.003',
        'VBF_H0L1':'1.003',
        'VBF_H0L1f05':'1.003',
        'VBF_H0PM_H0M_M0':'1.003',
        'VBF_H0PM_H0M_M1':'1.003',
        'VBF_H0PM_H0M_M2':'1.003',
        'VBF_H0PM_H0M_M3':'1.003',
        'VBF_H0PM_H0PH_M0':'1.003',
        'VBF_H0PM_H0PH_M1':'1.003',
        'VBF_H0PM_H0PH_M2':'1.003',
        'VBF_H0PM_H0PH_M3':'1.003',
        'VBF_H0PM_H0L1_M0':'1.003',
        'VBF_H0PM_H0L1_M1':'1.003',
        'VBF_H0PM_H0L1_M2':'1.003',
        'VBF_H0PM_H0L1_M3':'1.003',
        'VBF_H0M_H0PM':'1.003',
        'VBF_H0M_H0M_M0':'1.003',
        'VBF_H0M_H0M_M1':'1.003',
        'VBF_H0M_H0M_M2':'1.003',
        'VBF_H0M_H0M_M3':'1.003',
        'VBF_H0M_H0PH_M0':'1.003',
        'VBF_H0M_H0PH_M1':'1.003',
        'VBF_H0M_H0PH_M2':'1.003',
        'VBF_H0M_H0PH_M3':'1.003',
        'VBF_H0M_H0L1_M0':'1.003',
        'VBF_H0M_H0L1_M1':'1.003',
        'VBF_H0M_H0L1_M2':'1.003',
        'VBF_H0M_H0L1_M3':'1.003',
        'VBF_H0Mf05_H0PM':'1.003',
        'VBF_H0Mf05_H0M_M0':'1.003',
        'VBF_H0Mf05_H0M_M1':'1.003',
        'VBF_H0Mf05_H0M_M2':'1.003',
        'VBF_H0Mf05_H0M_M3':'1.003',
        'VBF_H0Mf05_H0PH_M0':'1.003',
        'VBF_H0Mf05_H0PH_M1':'1.003',
        'VBF_H0Mf05_H0PH_M2':'1.003',
        'VBF_H0Mf05_H0PH_M3':'1.003',
        'VBF_H0Mf05_H0L1_M0':'1.003',
        'VBF_H0Mf05_H0L1_M1':'1.003',
        'VBF_H0Mf05_H0L1_M2':'1.003',
        'VBF_H0Mf05_H0L1_M3':'1.003',
        'VBF_H0PH_H0PM':'1.003',
        'VBF_H0PH_H0M_M0':'1.003',
        'VBF_H0PH_H0M_M1':'1.003',
        'VBF_H0PH_H0M_M2':'1.003',
        'VBF_H0PH_H0M_M3':'1.003',
        'VBF_H0PH_H0PH_M0':'1.003',
        'VBF_H0PH_H0PH_M1':'1.003',
        'VBF_H0PH_H0PH_M2':'1.003',
        'VBF_H0PH_H0PH_M3':'1.003',
        'VBF_H0PH_H0L1_M0':'1.003',
        'VBF_H0PH_H0L1_M1':'1.003',
        'VBF_H0PH_H0L1_M2':'1.003',
        'VBF_H0PH_H0L1_M3':'1.003',
        'VBF_H0PHf05_H0PM':'1.003',
        'VBF_H0PHf05_H0M_M0':'1.003',
        'VBF_H0PHf05_H0M_M1':'1.003',
        'VBF_H0PHf05_H0M_M2':'1.003',
        'VBF_H0PHf05_H0M_M3':'1.003',
        'VBF_H0PHf05_H0PH_M0':'1.003',
        'VBF_H0PHf05_H0PH_M1':'1.003',
        'VBF_H0PHf05_H0PH_M2':'1.003',
        'VBF_H0PHf05_H0PH_M3':'1.003',
        'VBF_H0PHf05_H0L1_M0':'1.003',
        'VBF_H0PHf05_H0L1_M1':'1.003',
        'VBF_H0PHf05_H0L1_M2':'1.003',
        'VBF_H0PHf05_H0L1_M3':'1.003',
        'VBF_H0L1_H0PM':'1.003',
        'VBF_H0L1_H0M_M0':'1.003',
        'VBF_H0L1_H0M_M1':'1.003',
        'VBF_H0L1_H0M_M2':'1.003',
        'VBF_H0L1_H0M_M3':'1.003',
        'VBF_H0L1_H0PH_M0':'1.003',
        'VBF_H0L1_H0PH_M1':'1.003',
        'VBF_H0L1_H0PH_M2':'1.003',
        'VBF_H0L1_H0PH_M3':'1.003',
        'VBF_H0L1_H0L1_M0':'1.003',
        'VBF_H0L1_H0L1_M1':'1.003',
        'VBF_H0L1_H0L1_M2':'1.003',
        'VBF_H0L1_H0L1_M3':'1.003',
        'VBF_H0L1f05_H0PM':'1.003',
        'VBF_H0L1f05_H0M_M0':'1.003',
        'VBF_H0L1f05_H0M_M1':'1.003',
        'VBF_H0L1f05_H0M_M2':'1.003',
        'VBF_H0L1f05_H0M_M3':'1.003',
        'VBF_H0L1f05_H0PH_M0':'1.003',
        'VBF_H0L1f05_H0PH_M1':'1.003',
        'VBF_H0L1f05_H0PH_M2':'1.003',
        'VBF_H0L1f05_H0PH_M3':'1.003',
        'VBF_H0L1f05_H0L1_M0':'1.003',
        'VBF_H0L1f05_H0L1_M1':'1.003',
        'VBF_H0L1f05_H0L1_M2':'1.003',
        'VBF_H0L1f05_H0L1_M3':'1.003',

        'WH_H0PM':'1.010',
        'WH_H0M':'1.010',
        'WH_H0Mf05':'1.010',
        'WH_H0PH':'1.010',
        'WH_H0PHf05':'1.010',
        'WH_H0L1':'1.010',
        'WH_H0L1f05':'1.010',
        'WH_H0PM_H0M_M0':'1.010',
        'WH_H0PM_H0M_M1':'1.010',
        'WH_H0PM_H0M_M2':'1.010',
        'WH_H0PM_H0M_M3':'1.010',
        'WH_H0PM_H0PH_M0':'1.010',
        'WH_H0PM_H0PH_M1':'1.010',
        'WH_H0PM_H0PH_M2':'1.010',
        'WH_H0PM_H0PH_M3':'1.010',
        'WH_H0PM_H0L1_M0':'1.010',
        'WH_H0PM_H0L1_M1':'1.010',
        'WH_H0PM_H0L1_M2':'1.010',
        'WH_H0PM_H0L1_M3':'1.010',
        'WH_H0M_H0PM':'1.010',
        'WH_H0M_H0M_M0':'1.010',
        'WH_H0M_H0M_M1':'1.010',
        'WH_H0M_H0M_M2':'1.010',
        'WH_H0M_H0M_M3':'1.010',
        'WH_H0M_H0PH_M0':'1.010',
        'WH_H0M_H0PH_M1':'1.010',
        'WH_H0M_H0PH_M2':'1.010',
        'WH_H0M_H0PH_M3':'1.010',
        'WH_H0M_H0L1_M0':'1.010',
        'WH_H0M_H0L1_M1':'1.010',
        'WH_H0M_H0L1_M2':'1.010',
        'WH_H0M_H0L1_M3':'1.010',
        'WH_H0Mf05_H0PM':'1.010',
        'WH_H0Mf05_H0M_M0':'1.010',
        'WH_H0Mf05_H0M_M1':'1.010',
        'WH_H0Mf05_H0M_M2':'1.010',
        'WH_H0Mf05_H0M_M3':'1.010',
        'WH_H0Mf05_H0PH_M0':'1.010',
        'WH_H0Mf05_H0PH_M1':'1.010',
        'WH_H0Mf05_H0PH_M2':'1.010',
        'WH_H0Mf05_H0PH_M3':'1.010',
        'WH_H0Mf05_H0L1_M0':'1.010',
        'WH_H0Mf05_H0L1_M1':'1.010',
        'WH_H0Mf05_H0L1_M2':'1.010',
        'WH_H0Mf05_H0L1_M3':'1.010',
        'WH_H0PH_H0PM':'1.010',
        'WH_H0PH_H0M_M0':'1.010',
        'WH_H0PH_H0M_M1':'1.010',
        'WH_H0PH_H0M_M2':'1.010',
        'WH_H0PH_H0M_M3':'1.010',
        'WH_H0PH_H0PH_M0':'1.010',
        'WH_H0PH_H0PH_M1':'1.010',
        'WH_H0PH_H0PH_M2':'1.010',
        'WH_H0PH_H0PH_M3':'1.010',
        'WH_H0PH_H0L1_M0':'1.010',
        'WH_H0PH_H0L1_M1':'1.010',
        'WH_H0PH_H0L1_M2':'1.010',
        'WH_H0PH_H0L1_M3':'1.010',
        'WH_H0PHf05_H0PM':'1.010',
        'WH_H0PHf05_H0M_M0':'1.010',
        'WH_H0PHf05_H0M_M1':'1.010',
        'WH_H0PHf05_H0M_M2':'1.010',
        'WH_H0PHf05_H0M_M3':'1.010',
        'WH_H0PHf05_H0PH_M0':'1.010',
        'WH_H0PHf05_H0PH_M1':'1.010',
        'WH_H0PHf05_H0PH_M2':'1.010',
        'WH_H0PHf05_H0PH_M3':'1.010',
        'WH_H0PHf05_H0L1_M0':'1.010',
        'WH_H0PHf05_H0L1_M1':'1.010',
        'WH_H0PHf05_H0L1_M2':'1.010',
        'WH_H0PHf05_H0L1_M3':'1.010',
        'WH_H0L1_H0PM':'1.010',
        'WH_H0L1_H0M_M0':'1.010',
        'WH_H0L1_H0M_M1':'1.010',
        'WH_H0L1_H0M_M2':'1.010',
        'WH_H0L1_H0M_M3':'1.010',
        'WH_H0L1_H0PH_M0':'1.010',
        'WH_H0L1_H0PH_M1':'1.010',
        'WH_H0L1_H0PH_M2':'1.010',
        'WH_H0L1_H0PH_M3':'1.010',
        'WH_H0L1_H0L1_M0':'1.010',
        'WH_H0L1_H0L1_M1':'1.010',
        'WH_H0L1_H0L1_M2':'1.010',
        'WH_H0L1_H0L1_M3':'1.010',
        'WH_H0L1f05_H0PM':'1.010',
        'WH_H0L1f05_H0M_M0':'1.010',
        'WH_H0L1f05_H0M_M1':'1.010',
        'WH_H0L1f05_H0M_M2':'1.010',
        'WH_H0L1f05_H0M_M3':'1.010',
        'WH_H0L1f05_H0PH_M0':'1.010',
        'WH_H0L1f05_H0PH_M1':'1.010',
        'WH_H0L1f05_H0PH_M2':'1.010',
        'WH_H0L1f05_H0PH_M3':'1.010',
        'WH_H0L1f05_H0L1_M0':'1.010',
        'WH_H0L1f05_H0L1_M1':'1.010',
        'WH_H0L1f05_H0L1_M2':'1.010',
        'WH_H0L1f05_H0L1_M3':'1.010',

        'ZH_H0PM':'1.015',
        'ZH_H0M':'1.015',
        'ZH_H0Mf05':'1.015',
        'ZH_H0PH':'1.015',
        'ZH_H0PHf05':'1.015',
        'ZH_H0L1':'1.015',
        'ZH_H0L1f05':'1.015',
        'ZH_H0PM_H0M_M0':'1.015',
        'ZH_H0PM_H0M_M1':'1.015',
        'ZH_H0PM_H0M_M2':'1.015',
        'ZH_H0PM_H0M_M3':'1.015',
        'ZH_H0PM_H0PH_M0':'1.015',
        'ZH_H0PM_H0PH_M1':'1.015',
        'ZH_H0PM_H0PH_M2':'1.015',
        'ZH_H0PM_H0PH_M3':'1.015',
        'ZH_H0PM_H0L1_M0':'1.015',
        'ZH_H0PM_H0L1_M1':'1.015',
        'ZH_H0PM_H0L1_M2':'1.015',
        'ZH_H0PM_H0L1_M3':'1.015',
        'ZH_H0M_H0PM':'1.015',
        'ZH_H0M_H0M_M0':'1.015',
        'ZH_H0M_H0M_M1':'1.015',
        'ZH_H0M_H0M_M2':'1.015',
        'ZH_H0M_H0M_M3':'1.015',
        'ZH_H0M_H0PH_M0':'1.015',
        'ZH_H0M_H0PH_M1':'1.015',
        'ZH_H0M_H0PH_M2':'1.015',
        'ZH_H0M_H0PH_M3':'1.015',
        'ZH_H0M_H0L1_M0':'1.015',
        'ZH_H0M_H0L1_M1':'1.015',
        'ZH_H0M_H0L1_M2':'1.015',
        'ZH_H0M_H0L1_M3':'1.015',
        'ZH_H0Mf05_H0PM':'1.015',
        'ZH_H0Mf05_H0M_M0':'1.015',
        'ZH_H0Mf05_H0M_M1':'1.015',
        'ZH_H0Mf05_H0M_M2':'1.015',
        'ZH_H0Mf05_H0M_M3':'1.015',
        'ZH_H0Mf05_H0PH_M0':'1.015',
        'ZH_H0Mf05_H0PH_M1':'1.015',
        'ZH_H0Mf05_H0PH_M2':'1.015',
        'ZH_H0Mf05_H0PH_M3':'1.015',
        'ZH_H0Mf05_H0L1_M0':'1.015',
        'ZH_H0Mf05_H0L1_M1':'1.015',
        'ZH_H0Mf05_H0L1_M2':'1.015',
        'ZH_H0Mf05_H0L1_M3':'1.015',
        'ZH_H0PH_H0PM':'1.015',
        'ZH_H0PH_H0M_M0':'1.015',
        'ZH_H0PH_H0M_M1':'1.015',
        'ZH_H0PH_H0M_M2':'1.015',
        'ZH_H0PH_H0M_M3':'1.015',
        'ZH_H0PH_H0PH_M0':'1.015',
        'ZH_H0PH_H0PH_M1':'1.015',
        'ZH_H0PH_H0PH_M2':'1.015',
        'ZH_H0PH_H0PH_M3':'1.015',
        'ZH_H0PH_H0L1_M0':'1.015',
        'ZH_H0PH_H0L1_M1':'1.015',
        'ZH_H0PH_H0L1_M2':'1.015',
        'ZH_H0PH_H0L1_M3':'1.015',
        'ZH_H0PHf05_H0PM':'1.015',
        'ZH_H0PHf05_H0M_M0':'1.015',
        'ZH_H0PHf05_H0M_M1':'1.015',
        'ZH_H0PHf05_H0M_M2':'1.015',
        'ZH_H0PHf05_H0M_M3':'1.015',
        'ZH_H0PHf05_H0PH_M0':'1.015',
        'ZH_H0PHf05_H0PH_M1':'1.015',
        'ZH_H0PHf05_H0PH_M2':'1.015',
        'ZH_H0PHf05_H0PH_M3':'1.015',
        'ZH_H0PHf05_H0L1_M0':'1.015',
        'ZH_H0PHf05_H0L1_M1':'1.015',
        'ZH_H0PHf05_H0L1_M2':'1.015',
        'ZH_H0PHf05_H0L1_M3':'1.015',
        'ZH_H0L1_H0PM':'1.015',
        'ZH_H0L1_H0M_M0':'1.015',
        'ZH_H0L1_H0M_M1':'1.015',
        'ZH_H0L1_H0M_M2':'1.015',
        'ZH_H0L1_H0M_M3':'1.015',
        'ZH_H0L1_H0PH_M0':'1.015',
        'ZH_H0L1_H0PH_M1':'1.015',
        'ZH_H0L1_H0PH_M2':'1.015',
        'ZH_H0L1_H0PH_M3':'1.015',
        'ZH_H0L1_H0L1_M0':'1.015',
        'ZH_H0L1_H0L1_M1':'1.015',
        'ZH_H0L1_H0L1_M2':'1.015',
        'ZH_H0L1_H0L1_M3':'1.015',
        'ZH_H0L1f05_H0PM':'1.015',
        'ZH_H0L1f05_H0M_M0':'1.015',
        'ZH_H0L1f05_H0M_M1':'1.015',
        'ZH_H0L1f05_H0M_M2':'1.015',
        'ZH_H0L1f05_H0M_M3':'1.015',
        'ZH_H0L1f05_H0PH_M0':'1.015',
        'ZH_H0L1f05_H0PH_M1':'1.015',
        'ZH_H0L1f05_H0PH_M2':'1.015',
        'ZH_H0L1f05_H0PH_M3':'1.015',
        'ZH_H0L1f05_H0L1_M0':'1.015',
        'ZH_H0L1f05_H0L1_M1':'1.015',
        'ZH_H0L1f05_H0L1_M2':'1.015',
        'ZH_H0L1f05_H0L1_M3':'1.015',

       #'qqH_htt': '1.003',
        #'WH_hww': '1.010',
        #'WH_htt': '1.010',
        #'ZH_hww': '1.015',
        #'ZH_htt': '1.015',
    }
}

nuisances['QCDscale_gg_ACCEPT'] = {
    'name': 'QCDscale_gg_ACCEPT',
    'samples': {
        #FIXME add ggH_htt and ggZH_hww
        'ggWW': '1.012',
        'H0PM':'1.012',
        'H0M':'1.012',
        'H0Mf05':'1.012',
        'H0PH':'1.012',
        'H0PHf05':'1.012',
        'H0L1':'1.012',
        'H0L1f05':'1.012',
        'H0PM_H0M':'1.012',
        'H0PM_H0Mf05':'1.012',
        'H0PM_H0PH':'1.012',
        'H0PM_H0PHf05':'1.012',
        'H0PM_H0L1':'1.012',
        'H0PM_H0L1f05':'1.012',
        'H0M_H0PM':'1.012',
        'H0M_H0Mf05':'1.012',
        'H0M_H0PH':'1.012',
        'H0M_H0PHf05':'1.012',
        'H0M_H0L1':'1.012',
        'H0M_H0L1f05':'1.012',
        'H0Mf05_H0PM':'1.012',
        'H0Mf05_H0M':'1.012',
        'H0Mf05_H0PH':'1.012',
        'H0Mf05_H0PHf05':'1.012',
        'H0Mf05_H0L1':'1.012',
        'H0Mf05_H0L1f05':'1.012',
        'H0PH_H0PM':'1.012',
        'H0PH_H0M':'1.012',
        'H0PH_H0Mf05':'1.012',
        'H0PH_H0PHf05':'1.012',
        'H0PH_H0L1':'1.012',
        'H0PH_H0L1f05':'1.012',
        'H0PHf05_H0PM':'1.012',
        'H0PHf05_H0M':'1.012',
        'H0PHf05_H0Mf05':'1.012',
        'H0PHf05_H0PH':'1.012',
        'H0PHf05_H0L1':'1.012',
        'H0PHf05_H0L1f05':'1.012',
        'H0L1_H0PM':'1.012',
        'H0L1_H0M':'1.012',
        'H0L1_H0Mf05':'1.012',
        'H0L1_H0PH':'1.012',
        'H0L1_H0PHf05':'1.012',
        'H0L1_H0L1f05':'1.012',
        'H0L1f05_H0PM':'1.012',
        'H0L1f05_H0M':'1.012',
        'H0L1f05_H0Mf05':'1.012',
        'H0L1f05_H0PH':'1.012',
        'H0L1f05_H0PHf05':'1.012',
        'H0L1f05_H0L1':'1.012',
    },
    'type': 'lnN',
}

## Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat'] = {
    'type': 'auto',
    'maxPoiss': '10',
    'includeSignal': '0',
    #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
    #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
    'samples': {}
}

## rate parameters
nuisances['DYembnorm0j']  = {
               'name'  : 'CMS_hww_DYttnorm0j',
               'samples'  : {
                   'Dyemb' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }

nuisances['DYembnorm1j']  = {
               'name'  : 'CMS_hww_DYttnorm1j',
               'samples'  : {
                   'Dyemb' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
'''
nuisances['DYembnorm2j']  = {
                 'name'  : 'CMS_hww_DYttnorm2j',
                 'samples'  : {
                   'Dyemb' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts'  : cuts2j
                }
'''
nuisances['WWnorm0j']  = {
               'name'  : 'CMS_hww_WWnorm0j',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }

nuisances['ggWWnorm0j']  = {
               'name'  : 'CMS_hww_WWnorm0j',
               'samples'  : {
                   'ggWW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }


nuisances['WWnorm1j']  = {
               'name'  : 'CMS_hww_WWnorm1j',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }

nuisances['ggWWnorm1j']  = {
               'name'  : 'CMS_hww_WWnorm1j',
               'samples'  : {
                   'ggWW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }

'''
nuisances['WWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }


nuisances['ggWWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'samples'  : {
                   'ggWW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }
'''

nuisances['Topnorm0j']  = {
               'name'  : 'CMS_hww_Topnorm0j',
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }

nuisances['Topnorm1j']  = {
               'name'  : 'CMS_hww_Topnorm1j',
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
'''
nuisances['Topnorm2j']  = {
               'name'  : 'CMS_hww_Topnorm2j',
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }
'''


for n in nuisances.values():
    n['skipCMS'] = 1

print ' '.join(nuis['name'] for nname, nuis in nuisances.iteritems() if nname not in ('lumi', 'stat'))

print("SHAPE UP/DO NUISANCE LIST:")
print ' '.join(nuis['name'] for nname, nuis in nuisances.iteritems() if ((nuis['type'] == 'shape' or 'folderUp' in nuis.keys()) and (len(nuis['samples'].keys())==0 or "VBF_H0PM" in nuis['samples'].keys() or "H0PM" in nuis['samples'].keys() or "WH_H0PM" in nuis['samples'].keys() or "ZH_H0PM" in nuis['samples'].keys() )))
