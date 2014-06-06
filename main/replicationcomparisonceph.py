'''
Created on Jun 5, 2014

@author: vince
'''

from cosbenchplot.plotter.plotgenerator import StagePlotGenerator,\
    WorkloadPlotGenerator, RTPlotGenerator
from cosbenchplot.parser.StageFileParser import StageFileParser

BP = '/home/vince/cosbench-data/results/'
BASE_OUTPUT = '/home/vince/cosbench-data/ceph-replication-analysis/'

replication_workload_ids = [91]
no_replication_workload_ids = [92]

if __name__ == '__main__':
    outdir=BASE_OUTPUT + '/stage/'
    plotgen = StagePlotGenerator(BP, outdir)
#     plotgen.plotOnlyAverage()
    plotgen.addWorkloadIds('3-replicas', replication_workload_ids)
    plotgen.addWorkloadIds('1-replica', no_replication_workload_ids)
    plotgen.createAllStagePlots(outdir)
    
    outdir = BASE_OUTPUT + '/responsetime/'
    plotgen = RTPlotGenerator(BP, outdir)
    plotgen.addWorkloadIds('3-replicas', replication_workload_ids)
    plotgen.addWorkloadIds('1-replica', no_replication_workload_ids)
    plotgen.createRtPlots('RT - 100% write - 1cont_128kb', ['3-replicas', '1-replica'], 'w[0-9]+-1cont_128kb.*$', '.*-main-(write)')
