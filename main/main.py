'''
Created on May 8, 2014

@author: vince
'''
from cosbenchplot.main.plotgenerator import StagePlotGenerator,\
    WorkloadPlotGenerator, RTPlotGenerator

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
    outdir = '/home/vince/cosbench-data/graphs/throughput/'
    plotgen = StagePlotGenerator(BP, outdir)
    plotgen.addWorkloadIds('ceph', ceph_workload_ids)
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    for workloadFilter in workloadFilters:
        plotgen.setWorkloadFilter(workloadFilter[0])
        plotgen.setFilenameFilter('r100w0d0')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "100% read - Read throughput", '_([0-9]+)$', ['Throughputread'], lineStyleRule)
        plotgen.setFilenameFilter('r0w100d0')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "100% write - Write throughput", '_([0-9]+)$', ['Throughputwrite'], lineStyleRule)
        plotgen.setFilenameFilter('r80w15d5')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "r:80% w:15% d:5% - Write throughput", '_([0-9]+)$', ['Throughputwrite'], lineStyleRule)
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "r:80% w:15% d:5% - Read throughput", '_([0-9]+)$', ['Throughputread'], lineStyleRule)
    outdir = '/home/vince/cosbench-data/graphs/bandwidth/'
    plotgen._outdir = outdir
    for workloadFilter in workloadFilters:
        plotgen.setWorkloadFilter(workloadFilter[0])
        plotgen.setFilenameFilter('r100w0d0')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "100% read - Read bandwidth", '_([0-9]+)$', ['Bandwidthread'], lineStyleRule)
        plotgen.setFilenameFilter('r0w100d0')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "100% write - Write bandwidth", '_([0-9]+)$', ['Bandwidthwrite'], lineStyleRule)
        plotgen.setFilenameFilter('r80w15d5')
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "r:80% w:15% d:5% - Write bandwidth", '_([0-9]+)$', ['Bandwidthwrite'], lineStyleRule)
        plotgen.createAggregatedChart(outdir, workloadFilter[1] + "r:80% w:15% d:5% - Read bandwidth", '_([0-9]+)$', ['Bandwidthread'], lineStyleRule)

def createMaxWorkloadsCharts():
    '''
    These charts plot, for each workloads of each storage system, a single point
    representing the maximum of the averages for that given metric across all the
    available workstages (the ones that are not filtered out).
    '''
    outdir = '/home/vince/cosbench-data/graphs/workstages-throughput/'
    wlplotgen = WorkloadPlotGenerator(BP, outdir)
    wlplotgen.addWorkloadIds('ceph', ceph_workload_ids)
    wlplotgen.addWorkloadIds('swift', swift_workload_ids)
    wlplotgen.setUnit('op/s')
    wlplotgen.createWorkloadsMaxChart('r100w0d0', 'read', 'Throughput', '100% read - Read throughput - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')
    wlplotgen.createWorkloadsMaxChart('r0w100d0', 'write', 'Throughput', '100% write - Write throughput - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')
    wlplotgen.createWorkloadsMaxChart('r80w15d5', 'read', 'Throughput', 'r:80% w:15% d:5% - Read throughput - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')
    wlplotgen.createWorkloadsMaxChart('r80w15d5', 'write', 'Throughput', 'r:80% w:15% d:5% - Write throughput - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')

def createIndividualRtCharts():
    outdir = '/home/vince/cosbench-data/graphs/test/'
    plotgen = RTPlotGenerator(BP, outdir)
    plotgen.addWorkloadIds('ceph', ceph_workload_ids)
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    plotgen.createRtPlots('r:80% w:15% d:5% - Response time ceph', ['ceph'], 'w[0-9]+-20cont_5mb', '.*r80w15d5_(64|256|512).*main-read')
    plotgen.createRtPlots('r:80% w:15% d:5% - Response time swift', ['swift'], 'w[0-9]+-20cont_5mb', '.*r80w15d5_(64|256|512).*main-read')

if __name__ == '__main__':
    #createStageGraphsForEachStat()
    #createAggregatedGraphsForStages()
    #createMaxWorkloadsCharts()
    createIndividualRtCharts()