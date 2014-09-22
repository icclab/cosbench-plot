__author__ = 'gank'

import matplotlib
from plotter.plotgenerator import StagePlotGenerator,\
    WorkloadPlotGenerator, RTPlotGenerator
from parser.StageFileParser import StageFileParser

BASE_INPUT_PATH = '/Users/gank/src/'
BASE_OUTPUT = '/Users/gank/src/graphs/'

swift_workload_ids = [20]

def createStageGraphsForEachStat():
    outdir=BASE_OUTPUT + '/stage/'
    plotgen = StagePlotGenerator(BASE_INPUT_PATH, outdir, '^s[0-9]+-')
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    plotgen.createAllStagePlots(outdir)



def createAggregatedGraphsForStages():
    lineStyleRule = lambda stname: '-'
    outdir = BASE_OUTPUT + '/throughput/'
    plotgen = StagePlotGenerator(BASE_INPUT_PATH, outdir, 's.*')
    plotgen.addWorkloadIds('swift', swift_workload_ids)

    plotgen.setWorkloadFilter('w20-eagle')
    plotgen.setFilenameFilter('s[0-9]+.*$')
    plotgen.createAggregatedChart(outdir, 'w20_eagle' + "swiftbox", '(.*)', ['Throughputread'], lineStyleRule)


if __name__ == '__main__':
    print matplotlib.__version__
    createAggregatedGraphsForStages()