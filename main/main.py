'''
Created on May 8, 2014

@author: vince
'''
from cosbenchplot.main.plotgenerator import StagePlotGenerator

BP = '/home/vince/cosbench-data/results/'

ceph_workload_ids = [55]
ceph_workload_ids.extend([i for i in range(44,55)])

swift_workload_ids = [i for i in range(57, 69)]

def createStageGraphsForEachStat():
    STAGE_OUT_DIR='/home/vince/cosbench-data/graphs/stage/'
    plotgen = StagePlotGenerator(BP, STAGE_OUT_DIR)
    plotgen.addWorkloadIds('ceph', ceph_workload_ids)
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    plotgen.createAllStagePlots(STAGE_OUT_DIR)

def createAggregatedGrpahsForStat():
    outdir = '/home/vince/cosbench-data/graphs/test/'
    plotgen = StagePlotGenerator(BP, outdir)
    plotgen.addWorkloadIds('ceph', ceph_workload_ids)
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    plotgen.setWorkloadFilter('\/w[0-9]+-1cont_4kb$')
    plotgen.setFilenameFilter('r100w0d0')
    lineStyleRule = lambda stname: '-' if 'ceph' in stname else '--'
    plotgen.createAggregatedChart(outdir, "1 cont - 4kb - 100% read - Read bandwidth", '_([0-9]+)$', ['Bandwidthread'], lineStyleRule)
    plotgen.createAggregatedChart(outdir, "1 cont - 4kb - 100% read - Read op-count", '_([0-9]+)$', ['Op-Countread'], lineStyleRule)

if __name__ == '__main__':
    #createStageGraphsForEachStat()
    createAggregatedGrpahsForStat()