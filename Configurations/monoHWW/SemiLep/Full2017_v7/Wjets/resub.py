import os

resubs = [
    #'Wjets_NLOptMRaw.0',
    #'Wjets_NLOptMRaw.1',
    #'Wjets_NLOptMRaw.2',
    #'Wjets_NLOptMRaw.3',
    #'Wjets_NLOptMRaw.4',
    #'Wjets_NLOptMRaw.5',
    #'Wjets_NLOptMRaw.6',
    #'Wjets_NLOptMRaw.7',
    #'Wjets_NLOptMRaw.8',
    #'Wjets_NLOptMRaw.9',
    #'Wjets_NLOptMRaw.10',
    #'Wjets_NLOptMRaw.11',
    #'Wjets_NLOptMRaw.12',
    #'Wjets_NLOptMRaw.13',
    #'Wjets_NLOptMRaw.14',
    #'Wjets_NLOptMRaw.15',
    #'Wjets_NLOptMRaw.16',
    #'Wjets_NLOptMRaw.17',
    #'Wjets_NLOptMRaw.18',
    #'Wjets_NLOptMRaw.19',
    #'Wjets_NLOptMRaw.20',
    #'Wjets_NLOptMRaw.21',
    #'Wjets_NLOptMRaw.22',
    #'Wjets_NLOptMRaw.23',
    #'Wjets_NLOptMRaw.24',
    #'Wjets_NLOptMRaw.25',
    #'Wjets_NLOptMRaw.26',
    #'Wjets_NLOptMRaw.27',
    #'Wjets_NLOptMRaw.28',
    #'Wjets_NLOptMRaw.29',
    #'Wjets_NLOptMRaw.30',
    #'Wjets_NLOptMRaw.31',
    #'Wjets_NLOptMRaw.32',
    #'Wjets_NLOptMRaw.33',
    #'Wjets_NLOptMRaw.34',
    #'Wjets_NLOptMRaw.35',
    #'Wjets_NLOptMRaw.36',
    #'Wjets_NLOptMRaw.37',
    #'Wjets_NLOptMRaw.38',
    #'Wjets_NLOptMRaw.39',
    #'Wjets_NLOptMRaw.40',
    #'Wjets_NLOptMRaw.41',
    #'Wjets_NLOptMRaw.42',
    #'Wjets_NLOptMRaw.43',
    #'Wjets_NLOptMRaw.44',
    #'Wjets_NLOptMRaw.45',
    #'Wjets_NLOptMRaw.46',
    #'Wjets_NLOptMRaw.47',
    #'Wjets_NLOptMRaw.48',
    #'Wjets_NLOptMRaw.49',
    #'Wjets_NLOptMRaw.50',
    #'Wjets_NLOptMRaw.51',
    #'Wjets_NLOptMRaw.52',
    #'Wjets_NLOptMRaw.53',
    #'Wjets_NLOptMRaw.54',
    #'Wjets_NLOptMRaw.55',
    #'Wjets_NLOptMRaw.56',
    #'Wjets_NLOptMRaw.57',
    #'Wjets_NLOptMRaw.58',
    #'Wjets_NLOptMRaw.59',
    #'Wjets_NLOptMRaw.60',
    #'Wjets_NLOptMRaw.61',
    #'Wjets_NLOptMRaw.62',
    #'Wjets_NLOptMRaw.63',
    #'Wjets_NLOptMRaw.64',
    #'Wjets_NLOptMRaw.65',
    #'Wjets_NLOptMRaw.66',
    #'Wjets_NLOptMRaw.67',
    #'Wjets_NLOptMRaw.68',
    #'Wjets_NLOptMRaw.69',
    #'Wjets_NLOptMRaw.70',
    #'Wjets_NLOptMRaw.71',
    #'Wjets_NLOptMRaw.72',
    #'Wjets_NLOptMRaw.73',
    #'Wjets_NLOptMRaw.74',
    #'Wjets_NLOptMRaw.75',
    #'Wjets_NLOptMRaw.76',
    #'Wjets_NLOptMRaw.77',
    #'Wjets_NLOptMRaw.78',
    #'Wjets_NLOptMRaw.79',
    #'Wjets_NLOptMRaw.80',
    #'Wjets_NLOptMRaw.81',
    #'Wjets_NLOptMRaw.82',
    #'Wjets_NLOptMRaw.83',
    #'Wjets_NLOptMRaw.84',
    #'Wjets_NLOptMRaw.85',
    #'Wjets_NLOptMRaw.86',
    #'Wjets_NLOptMRaw.87',
    #'Wjets_NLOptMRaw.88',
    #'Wjets_NLOptMRaw.89',
    #'Wjets_NLOptMRaw.90',
    #'Wjets_NLOptMRaw.91',
    #'Wjets_NLOptMRaw.92',
    #'Wjets_NLOptMRaw.93',
    #'Wjets_NLOptMRaw.94',
    #'Wjets_NLOptMRaw.95',
    #'Wjets_NLOptMRaw.96',
    #'Wjets_NLOptMRaw.97',
    #'Wjets_NLOptMRaw.98',
    ##
    #'Wjets_NLOnjRaw.0',
    #'Wjets_NLOnjRaw.1',
    #'Wjets_NLOnjRaw.2',
    #'Wjets_NLOnjRaw.3',
    #'Wjets_NLOnjRaw.4',
    #'Wjets_NLOnjRaw.5',
    #'Wjets_NLOnjRaw.6',
    #'Wjets_NLOnjRaw.7',
    #'Wjets_NLOnjRaw.8',
    #'Wjets_NLOnjRaw.9',
    #'Wjets_NLOnjRaw.10',
    #'Wjets_NLOnjRaw.11',
    #'Wjets_NLOnjRaw.12',
    #'Wjets_NLOnjRaw.13',
    #'Wjets_NLOnjRaw.14',
    #'Wjets_NLOnjRaw.15',
    #'Wjets_NLOnjRaw.16',
    #'Wjets_NLOnjRaw.17',
    #'Wjets_NLOnjRaw.18',
    #'Wjets_NLOnjRaw.19',
    #'Wjets_NLOnjRaw.20',
    #'Wjets_NLOnjRaw.21',
    #'Wjets_NLOnjRaw.22',
    #'Wjets_NLOnjRaw.23',
    #'Wjets_NLOnjRaw.24',
    #'Wjets_NLOnjRaw.25',
    #'Wjets_NLOnjRaw.26',
    #'Wjets_NLOnjRaw.27',
    #'Wjets_NLOnjRaw.28',
    #'Wjets_NLOnjRaw.29',
    #'Wjets_NLOnjRaw.30',
    #'Wjets_NLOnjRaw.31',
    #'Wjets_NLOnjRaw.32',
    #'Wjets_NLOnjRaw.33',
    #'Wjets_NLOnjRaw.34',
    #'Wjets_NLOnjRaw.35',
    #'Wjets_NLOnjRaw.36',
    #'Wjets_NLOnjRaw.37',
    #'Wjets_NLOnjRaw.38',
    #'Wjets_NLOnjRaw.39',
    #'Wjets_NLOnjRaw.40',
    #'Wjets_NLOnjRaw.41',
    #'Wjets_NLOnjRaw.42',
    #'Wjets_NLOnjRaw.43',
    #'Wjets_NLOnjRaw.44',
    #'Wjets_NLOnjRaw.45',
    #'Wjets_NLOnjRaw.46',
    #'Wjets_NLOnjRaw.47',
    #'Wjets_NLOnjRaw.48',
    #'Wjets_NLOnjRaw.49',
    #'Wjets_NLOnjRaw.50',
    #'Wjets_NLOnjRaw.51',
    #'Wjets_NLOnjRaw.52',
    #'Wjets_NLOnjRaw.53',
    #'Wjets_NLOnjRaw.54',
    #'Wjets_NLOnjRaw.55',
    #'Wjets_NLOnjRaw.56',
    #'Wjets_NLOnjRaw.57',
    #'Wjets_NLOnjRaw.58',
    #'Wjets_NLOnjRaw.59',
    #'Wjets_NLOnjRaw.60',
    #'Wjets_NLOnjRaw.61',
    #'Wjets_NLOnjRaw.62',
    #'Wjets_NLOnjRaw.63',
    #'Wjets_NLOnjRaw.64',
    #'Wjets_NLOnjRaw.65',
    #'Wjets_NLOnjRaw.66',
    #'Wjets_NLOnjRaw.67',
    #'Wjets_NLOnjRaw.68',
    #'Wjets_NLOnjRaw.69',
    #'Wjets_NLOnjRaw.70',
    #'Wjets_NLOnjRaw.71',
    #'Wjets_NLOnjRaw.72',
    #'Wjets_NLOnjRaw.73',
    #'Wjets_NLOnjRaw.74',
    #'Wjets_NLOnjRaw.75',
    #'Wjets_NLOnjRaw.76',
    #'Wjets_NLOnjRaw.77',
    #'Wjets_NLOnjRaw.78',
    #'Wjets_NLOnjRaw.79',
    #'Wjets_NLOnjRaw.80',
    #'Wjets_NLOnjRaw.81',
    #'Wjets_NLOnjRaw.82',
    #'Wjets_NLOnjRaw.83',
    #'Wjets_NLOnjRaw.84',
    #'Wjets_NLOnjRaw.85',
    #'Wjets_NLOnjRaw.86',
    #'Wjets_NLOnjRaw.87',
    #'Wjets_NLOnjRaw.88',
    #'Wjets_NLOnjRaw.89',
    #'Wjets_NLOnjRaw.90',
    #'Wjets_NLOnjRaw.91',
    #'Wjets_NLOnjRaw.92',
    #'Wjets_NLOnjRaw.93',
    #'Wjets_NLOnjRaw.94',
    #'Wjets_NLOnjRaw.95',
    #'Wjets_NLOnjRaw.96',
    #'Wjets_NLOnjRaw.97',
    #'Wjets_NLOnjRaw.98',
    #'Wjets_NLOnjRaw.99',
    #'Wjets_NLOnjRaw.100',
    #'Wjets_NLOnjRaw.101',
    #'Wjets_NLOnjRaw.102',
    #'Wjets_NLOnjRaw.103',
    #'Wjets_NLOnjRaw.104',
    #'Wjets_NLOnjRaw.105',
    #'Wjets_NLOnjRaw.106',
    #'Wjets_NLOnjRaw.107',
    #'Wjets_NLOnjRaw.108',
    #'Wjets_NLOnjRaw.109',
    #'Wjets_NLOnjRaw.110',
    #'Wjets_NLOnjRaw.111',
    #'Wjets_NLOnjRaw.112',
    #'Wjets_NLOnjRaw.113',
    #'Wjets_NLOnjRaw.114',
    #'Wjets_NLOnjRaw.115',
    #'Wjets_NLOnjRaw.116',
    #'Wjets_NLOnjRaw.117',
    #'Wjets_NLOnjRaw.118',
    #'Wjets_NLOnjRaw.119',
    #'Wjets_NLOnjRaw.120',
    #'Wjets_NLOnjRaw.121',
    #'Wjets_NLOnjRaw.122',
    #'Wjets_NLOnjRaw.123',
    #'Wjets_NLOnjRaw.124',
    #'Wjets_NLOnjRaw.125',
    #'Wjets_NLOnjRaw.126',
    #'Wjets_NLOnjRaw.127',
    #'Wjets_NLOnjRaw.128',
    #'Wjets_NLOnjRaw.129',
    #'Wjets_NLOnjRaw.130',
    #'Wjets_NLOnjRaw.131',
    #'Wjets_NLOnjRaw.132',
    #'Wjets_NLOnjRaw.133',
    #'Wjets_NLOnjRaw.134',
    #'Wjets_NLOnjRaw.135',
    #'Wjets_NLOnjRaw.136',
    #'Wjets_NLOnjRaw.137',
    #'Wjets_NLOnjRaw.138',
    #'Wjets_NLOnjRaw.139',
    #'Wjets_NLOnjRaw.140',
    #'Wjets_NLOnjRaw.141',
    #'Wjets_NLOnjRaw.142',
    #'Wjets_NLOnjRaw.143',
    #'Wjets_NLOnjRaw.144',
    #'Wjets_NLOnjRaw.145',
    #'Wjets_NLOnjRaw.146',
    #'Wjets_NLOnjRaw.147',
    #'Wjets_NLOnjRaw.148',
    #'Wjets_NLOnjRaw.149',
    #'Wjets_NLOnjRaw.150',
    #'Wjets_NLOnjRaw.151',
    #'Wjets_NLOnjRaw.152',
    #'Wjets_NLOnjRaw.153',
    #'Wjets_NLOnjRaw.154',
    #
    #'Wjets_NLOstatM.0',
    #'Wjets_NLOstatM.1',
    #'Wjets_NLOstatM.2',
    #'Wjets_NLOstatM.3',
    #'Wjets_NLOstatM.4',
    #'Wjets_NLOstatM.5',
    #'Wjets_NLOstatM.6',
    #'Wjets_NLOstatM.7',
    #'Wjets_NLOstatM.8',
    #'Wjets_NLOstatM.9',
    #'Wjets_NLOstatM.10',
    #'Wjets_NLOstatM.11',
    #'Wjets_NLOstatM.12',
    #'Wjets_NLOstatM.13',
    #'Wjets_NLOstatM.14',
    #'Wjets_NLOstatM.15',
    #'Wjets_NLOstatM.16',
    #'Wjets_NLOstatM.17',
    #'Wjets_NLOstatM.18',
    #'Wjets_NLOstatM.19',
    #'Wjets_NLOstatM.20',
    #'Wjets_NLOstatM.21',
    #'Wjets_NLOstatM.22',
    #'Wjets_NLOstatM.23',
    #'Wjets_NLOstatM.24',
    #'Wjets_NLOstatM.25',
    #'Wjets_NLOstatM.26',
    #'Wjets_NLOstatM.27',
    #'Wjets_NLOstatM.28',
    #'Wjets_NLOstatM.29',
    #'Wjets_NLOstatM.30',
    #'Wjets_NLOstatM.31',
    #'Wjets_NLOstatM.32',
    #'Wjets_NLOstatM.33',
    #'Wjets_NLOstatM.34',
    #'Wjets_NLOstatM.35',
    #'Wjets_NLOstatM.36',
    #'Wjets_NLOstatM.37',
    #'Wjets_NLOstatM.38',
    #'Wjets_NLOstatM.39',
    #'Wjets_NLOstatM.40',
    #'Wjets_NLOstatM.41',
    #'Wjets_NLOstatM.42',
    #'Wjets_NLOstatM.43',
    #'Wjets_NLOstatM.44',
    #'Wjets_NLOstatM.45',
    #'Wjets_NLOstatM.46',
    #'Wjets_NLOstatM.47',
    #'Wjets_NLOstatM.48',
    #'Wjets_NLOstatM.49',
    #'Wjets_NLOstatM.50',
    #'Wjets_NLOstatM.51',
    #'Wjets_NLOstatM.52',
    #'Wjets_NLOstatM.53',
    #'Wjets_NLOstatM.54',
    #'Wjets_NLOstatM.55',
    #'Wjets_NLOstatM.56',
    #'Wjets_NLOstatM.57',
    #'Wjets_NLOstatM.58',
    #'Wjets_NLOstatM.59',
    #'Wjets_NLOstatM.60',
    #'Wjets_NLOstatM.61',
    #'Wjets_NLOstatM.62',
    #'Wjets_NLOstatM.63',
    #'Wjets_NLOstatM.64',
    #'Wjets_NLOstatM.65',
    #'Wjets_NLOstatM.66',
    #'Wjets_NLOstatM.67',
    #'Wjets_NLOstatM.68',
    #'Wjets_NLOstatM.69',
    #'Wjets_NLOstatM.70',
    #'Wjets_NLOstatM.71',
    #'Wjets_NLOstatM.72',
    #'Wjets_NLOstatM.73',
    #'Wjets_NLOstatM.74',
    #'Wjets_NLOstatM.75',
    #'Wjets_NLOstatM.76',
    #'Wjets_NLOstatM.77',
    #'Wjets_NLOstatM.78',
    #'Wjets_NLOstatM.79',
    #'Wjets_NLOstatM.80',
    #'Wjets_NLOstatM.81',
    #'Wjets_NLOstatM.82',
    #'Wjets_NLOstatM.83',
    #'Wjets_NLOstatM.84',
    #'Wjets_NLOstatM.85',
    #'Wjets_NLOstatM.86',
    #'Wjets_NLOstatM.87',
    #'Wjets_NLOstatM.88',
    #'Wjets_NLOstatM.89',
    #'Wjets_NLOstatM.90',
    #'Wjets_NLOstatM.91',
    #'Wjets_NLOstatM.92',
    #'Wjets_NLOstatM.93',
    #'Wjets_NLOstatM.94',
    #'Wjets_NLOstatM.95',
    #'Wjets_NLOstatM.96',
    #'Wjets_NLOstatM.97',
    #'Wjets_NLOstatM.98',
    #'Wjets_NLOstatM.99',
    #'Wjets_NLOstatM.100',
    #'Wjets_NLOstatM.101',
    #'Wjets_NLOstatM.102',
    #'Wjets_NLOstatM.103',
    #'Wjets_NLOstatM.104',
    #'Wjets_NLOstatM.105',
    #'Wjets_NLOstatM.106',
    #'Wjets_NLOstatM.107',
    #'Wjets_NLOstatM.108',
    #'Wjets_NLOstatM.109',
    #'Wjets_NLOstatM.110',
    #'Wjets_NLOstatM.111',
    #'Wjets_NLOstatM.112',
    #'Wjets_NLOstatM.113',
    #'Wjets_NLOstatM.114',
    #'Wjets_NLOstatM.115',
    #'Wjets_NLOstatM.116',
    #'Wjets_NLOstatM.117',
    #'Wjets_NLOstatM.118',
    #'Wjets_NLOstatM.119',
    #'Wjets_NLOstatM.120',
    #'Wjets_NLOstatM.121',
    #'Wjets_NLOstatM.122',
    #'Wjets_NLOstatM.123',
    #'Wjets_NLOstatM.124',
    #'Wjets_NLOstatM.125',
    #'Wjets_NLOstatM.126',
    #'Wjets_NLOstatM.127',
    #'Wjets_NLOstatM.128',
    #'Wjets_NLOstatM.129',
    #'Wjets_NLOstatM.130',
    #'Wjets_NLOstatM.131',
    #'Wjets_NLOstatM.132',
    #'Wjets_NLOstatM.133',
    #'Wjets_NLOstatM.134',
    #'Wjets_NLOstatM.135',
    #'Wjets_NLOstatM.136',
    #'Wjets_NLOstatM.137',
    #'Wjets_NLOstatM.138',
    #'Wjets_NLOstatM.139',
    #'Wjets_NLOstatM.140',
    #'Wjets_NLOstatM.141',
    #'Wjets_NLOstatM.142',
    #'Wjets_NLOstatM.143',
    #'Wjets_NLOstatM.144',
    #'Wjets_NLOstatM.145',
    #'Wjets_NLOstatM.146',
    #'Wjets_NLOstatM.147',
    #'Wjets_NLOstatM.148',
    #'Wjets_NLOstatM.149',
    #'Wjets_NLOstatM.150',
    #'Wjets_NLOstatM.151',
    #'Wjets_NLOstatM.152',
    #'Wjets_NLOstatM.153',
    #'Wjets_NLOstatM.154',
    #'Wjets_NLOstatM.155',
    #'Wjets_NLOstatM.156',
    #'Wjets_NLOstatM.157',
    #'Wjets_NLOstatM.158',
    #'Wjets_NLOstatM.159',
    #'Wjets_NLOstatM.160',
    #'Wjets_NLOstatM.161',
    #'Wjets_NLOstatM.162',
    #'Wjets_NLOstatM.163',
    #'Wjets_NLOstatM.164',
    #'Wjets_NLOstatM.165',
    #'Wjets_NLOstatM.166',
    #'Wjets_NLOstatM.167',
    #'Wjets_NLOstatM.168',
    #'Wjets_NLOstatM.169',
    #'Wjets_NLOstatM.170',
    #'Wjets_NLOstatM.171',
    #'Wjets_NLOstatM.172',
    #'Wjets_NLOstatM.173',
    #'Wjets_NLOstatM.174',
    #'Wjets_NLOstatM.175',
    #'Wjets_NLOstatM.176',
    #'Wjets_NLOstatM.177',
    #'Wjets_NLOstatM.178',
    #'Wjets_NLOstatM.179',
    #'Wjets_NLOstatM.180',
    #'Wjets_NLOstatM.181',
    #'Wjets_NLOstatM.182',
    #'Wjets_NLOstatM.183',
    #'Wjets_NLOstatM.184',
    #'Wjets_NLOstatM.185',
    #'Wjets_NLOstatM.186',
    #'Wjets_NLOstatM.187',
    #'Wjets_NLOstatM.188',
    #'Wjets_NLOstatM.189',
    #'Wjets_NLOstatM.190',
    #'Wjets_NLOstatM.191',
    #'Wjets_NLOstatM.192',
    #'Wjets_NLOstatM.193',
    #'Wjets_NLOstatM.194',
    #'Wjets_NLOstatM.195',
    #'Wjets_NLOstatM.196',
    #'Wjets_NLOstatM.197',
    #'Wjets_NLOstatM.198',
    #'Wjets_NLOstatM.199',
    #'Wjets_NLOstatM.200',
    #'Wjets_NLOstatM.201',
    #'Wjets_NLOstatM.202',
    #'Wjets_NLOstatM.203',
    #'Wjets_NLOstatM.204',
    #'Wjets_NLOstatM.205',
    #'Wjets_NLOstatM.206',
    #'Wjets_NLOstatM.207',
    #'Wjets_NLOstatM.208',
    #'Wjets_NLOstatM.209',
    #'Wjets_NLOstatM.210',
    #'Wjets_NLOstatM.211',
    #'Wjets_NLOstatM.212',
    #'Wjets_NLOstatM.213',
    #'Wjets_NLOstatM.214',
    #'Wjets_NLOstatM.215',
    #'Wjets_NLOstatM.216',
    #'Wjets_NLOstatM.217',
    #'Wjets_NLOstatM.218',
    #'Wjets_NLOstatM.219',
    #'Wjets_NLOstatM.220',
    #'Wjets_NLOstatM.221',
    #'Wjets_NLOstatM.222',
    #'Wjets_NLOstatM.223',
    #'Wjets_NLOstatM.224',
    #'Wjets_NLOstatM.225',
    #'Wjets_NLOstatM.226',
    #'Wjets_NLOstatM.227',
    #'Wjets_NLOstatM.228',
    'Wjets_NLOstatM.6',
    'Wjets_NLOstatM.4',
    'Wjets_NLOstatM.0',
    'Wjets_NLOstatM.23',
    'Wjets_NLOstatM.5',
    'Wjets_NLOstatM.38',
    'Wjets_NLOstatM.157',
    'Wjets_NLOstatM.212',
]


resub_str = 'ssh m8 qsub -l walltime=168:00:00 -N mkShapes__Wjets_inv_2017v7__ALL__JOB -q localgrid@cream02 -o /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB.out -e /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB.err /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB_Sing.sh > /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB.jid'

for job in resubs:
    comd = resub_str.replace('JOB', job)
    os.system(comd)

#ssh m8 qsub -l walltime=168:00:00 -N mkShapes__Wjets_inv_2017v7__ALL__JOB -q localgrid@cream02 -o /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB.out -e /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB.err /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB_Sing.sh > /user/svanputt/monoHiggs/sl7/CMSSW_10_6_5/src/job//mkShapes__Wjets_inv_2017v7__ALL/JOB/mkShapes__Wjets_inv_2017v7__ALL__JOB.jid
