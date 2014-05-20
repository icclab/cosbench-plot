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

def createAggregatedGraphsForStages():
    outdir = '/home/vince/cosbench-data/graphs/throughput/'
    plotgen = StagePlotGenerator(BP, outdir)
    plotgen.addWorkloadIds('ceph', ceph_workload_ids)
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    lineStyleRule = lambda stname: '-' if 'ceph' in stname else '--'
    workloadFilters = [('\/w[0-9]+-1cont_4kb$', '1 cont - 4kb - '),
                       ('\/w[0-9]+-1cont_128kb$', '1 cont - 128kb - '),
                       ('\/w[0-9]+-1cont_512kb$', '1 cont - 512kb - '),
                       ('\/w[0-9]+-1cont_1024kb$', '1 cont - 1024kb - '),
                       ('\/w[0-9]+-1cont_5mb$', '1 cont - 5mb - '),
                       ('\/w[0-9]+-1cont_10mb$', '1 cont - 10mb - '),
                       ('\/w[0-9]+-20cont_4kb$', '20 cont - 4kb - '),
                       ('\/w[0-9]+-20cont_128kb$', '20 cont - 128kb - '),
                       ('\/w[0-9]+-20cont_512kb$', '20 cont - 512kb - '),
                       ('\/w[0-9]+-20cont_1024kb$', '20 cont - 1024kb - '),
                       ('\/w[0-9]+-20cont_5mb$', '20 cont - 5mb - '),
                       ('\/w[0-9]+-20cont_10mb$', '20 cont - 10mb - ')]
    for workloadFilter in workloadFilters:
        plotgen.setWorkloadFilter(workloadFilter[0])
        plotgen.setFilenameFilter('r100w0d0')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "100% read - Read throughput", '_([0-9]+)$', ['Throughputread'], lineStyleRule)
        plotgen.setFilenameFilter('r0w100d0')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "100% write - Write throughput", '_([0-9]+)$', ['Throughputwrite'], lineStyleRule)
        plotgen.setFilenameFilter('r80w15d5')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "r:80% w:15% d:5% - Write throughput", '_([0-9]+)$', ['Throughputwrite'], lineStyleRule)
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "r:80% w:15% d:5% - Read throughput", '_([0-9]+)$', ['Throughputread'], lineStyleRule)

if __name__ == '__main__':
    #createStageGraphsForEachStat()
    createAggregatedGraphsForStages()