# example of configuration file
treeName= 'Events'


tag = 'Full2016_mm'


# used by mkShape to define output directory for root files
outputDir = 'rootFile_'+tag # '../../../../../../../../../../../../eos/home-d/dmroy/temp_shapes/2021_01_20_OwnShapes_AN/rootFile_'+tag # 'rootFile_'+tag

# file with TTree aliases
aliasesFile = 'aliases.py'

# file with list of variables
variablesFile = 'variables_forANplot.py'

# file with list of cuts
cutsFile = 'cuts_ee_mm.py' 

# file with list of samples
samplesFile = 'samples.py' 

# file with list of samples
plotFile = 'plot.py' 



# luminosity to normalize to (in 1/fb)
lumi = 35.867

# used by mkPlot to define output directory for plots
# different from "outputDir" to do things more tidy
outputDirPlots = 'plot_'+tag


# used by mkDatacards to define output directory for datacards
outputDirDatacard = 'datacards'


# structure file for datacard
#structureFile = 'structure.py' # Is this even needed still?


# nuisances file for mkDatacards and for mkShape
nuisancesFile = 'nuisances.py'


