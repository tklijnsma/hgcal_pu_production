# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --filein file:test.root --fileout testNanoML.root --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions auto:mc --step NANO
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import common
from time import strftime

cms_single = VarParsing.multiplicity.singleton
cms_int = VarParsing.varType.int
cms_bool = VarParsing.varType.bool

process = cms.Process('NANO')
options = VarParsing('python')
# options.setDefault('outputFile', 'testNanoML.root')
options.register("nThreads", 1, cms_single, cms_int, "number of threads")
options.register("runPFTruth", 0, cms_single, cms_int, "Don't run PFTruth (currently not working with pileup)")
options.register("merge", True, cms_single, cms_bool, "Run the SimCluster merging steps")
options.register('outputfile', None, VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Path to output file')
options.parseArguments()

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('DPGAnalysis.HGCalNanoAOD.nanoHGCML_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


# Not needed and crashes stuff with PU
process.nanoHGCMLSequence.remove(process.caloParticleTables)
process.nanoHGCMLSequence.remove(process.layerClusterTables)
process.nanoHGCMLRecoSequence.remove(process.pfTICLCandTable)


# This isn't working with pileup
if not options.runPFTruth:
    process.pfTruth = cms.Sequence()
    process.trackSCAssocTable = cms.Sequence()

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)
process.options.numberOfThreads=cms.untracked.uint32(options.nThreads)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    # SkipEvent = cms.untracked.vstring('ProductNotFound'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(1)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
if options.outputfile:
    output_file = options.outputfile
else:
    output_file = f'file:{common.guntype(options.inputFiles[0])}_nanoml_D86_fine_n{2}_{strftime("%b%d")}.root'
    if not options.merge: output_file = output_file.replace('.root', '_notmerged.root')
common.logger.info('Output: %s', output_file)

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(output_file),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

process.NANOAODSIMoutput.outputCommands.remove("keep edmTriggerResults_*_*_*")

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoHGCMLSequence)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.
from DPGAnalysis.HGCalNanoAOD.nanoHGCML_cff import customizeReco, customizeMergedSimClusters, customizeNoMergedCaloTruth
# Uncomment if you didn't schedule SimClusters/CaloParticles
# process = customizeNoMergedCaloTruth(process)
# merged simclusters (turn off if you aren't running through PEPR)

if options.merge:
    common.logger.info('Adding merge options')
    process = customizeMergedSimClusters(process)
    process = customizeReco(process)
else:
    common.logger.info('Not running merging')

# Use the complete SimTrack and SimVertex collections, including PU
process.hgcSimTruth.simVertices = cms.InputTag("AllSimTracksAndVerticesProducer", "AllSimVertices")
process.hgcSimTruth.simTracks = cms.InputTag("AllSimTracksAndVerticesProducer", "AllSimTracks")

# End of customisation functions


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
