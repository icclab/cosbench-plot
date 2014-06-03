'''
Created on May 8, 2014

@author: vince
'''
from cosbenchplot.plotter.plotgenerator import StagePlotGenerator,\
    WorkloadPlotGenerator, RTPlotGenerator
from cosbenchplot.parser.StageFileParser import StageFileParser

BP = '/home/vince/cosbench-data/results/'
BASE_OUTPUT = '/home/vince/cosbench-data/graphs-ii/'

ceph_workload_ids = [55]
ceph_workload_ids.extend([i for i in range(44,55)])

#swift_workload_ids = [i for i in range(57, 69)]
swift_workload_ids = [i for i in range(69, 81)]

def createStageGraphsForEachStat():
    outdir=BASE_OUTPUT + '/stage/'
    plotgen = StagePlotGenerator(BP, outdir)
    plotgen.addWorkloadIds('ceph', ceph_workload_ids)
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    plotgen.createAllStagePlots(outdir)

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
    outdir = BASE_OUTPUT + '/throughput/'
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
    outdir = BASE_OUTPUT + '/bandwidth/'
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
    for study in ['Throughput', 'Bandwidth', 'Succ-Ratio']:
        outdir = BASE_OUTPUT + '/workstages-{}/'.format(study.lower())
        wlplotgen = WorkloadPlotGenerator(BP, outdir)
        wlplotgen.addWorkloadIds('ceph', ceph_workload_ids)
        wlplotgen.addWorkloadIds('swift', swift_workload_ids)
        wlplotgen.setUnit(StageFileParser.HeaderTypes.headers[study].unit)
        wlplotgen.createWorkloadsMaxChart('r100w0d0', 'read', study, '100% read - Read ' + study + ' - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')
        wlplotgen.createWorkloadsMaxChart('r0w100d0', 'write', study, '100% write - Write ' + study + ' - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')
        wlplotgen.createWorkloadsMaxChart('r80w15d5', 'read', study, 'r:80% w:15% d:5% - Read ' + study + ' - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')
        wlplotgen.createWorkloadsMaxChart('r80w15d5', 'write', study, 'r:80% w:15% d:5% - Write ' + study + ' - Max of workstage averages', '^w[0-9]+-([0-9]+cont_.*)\.csv', '_([0-9]+)$')

def createIndividualRtCharts():
    outdir = BASE_OUTPUT + '/responsetime/'
    plotgen = RTPlotGenerator(BP, outdir)
    plotgen.addWorkloadIds('ceph', ceph_workload_ids)
    plotgen.addWorkloadIds('swift', swift_workload_ids)
    plotgen.createRtPlots('RT ceph - r:80% w:15% d:5% - Read 20cont_5mb', ['ceph'], 'w[0-9]+-20cont_5mb', '.*r80w15d5_(64|256|512).*main-read')
    plotgen.createRtPlots('RT swift - r:80% w:15% d:5% - Read 20cont_5mb', ['swift'], 'w[0-9]+-20cont_5mb', '.*r80w15d5_(64|256|512).*main-read')
    plotgen.createRtPlots('RT swift and ceph - r:80% w:15% d:5% - Read 1cont_10mb', ['swift','ceph'], 'w[0-9]+-1cont_10mb', '.*r80w15d5_(16|64|256|512).*main-read')
    plotgen.createRtPlots('RT swift and ceph - r:80% w:15% d:5% - Write 20cont_10mb', ['swift','ceph'], 'w[0-9]+-1cont_10mb', '.*r80w15d5_(16|512).*main-write')
    plotgen.createRtPlots('RT swift - r:80% w:15% d:5% - Write 20cont_10mb', ['swift'], 'w[0-9]+-1cont_10mb', '.*r80w15d5_(16).*main-write')
    plotgen.createRtPlots('RT swift - 100% Read - Read 1cont_1024kb', ['swift'], 'w[0-9]+-1cont_1024kb', '.*r100w0d0_(16|64|128|256|512).*main-read')
    plotgen.createRtPlots('RT ceph - 100% Read - Read 1cont_1024kb', ['ceph'], 'w[0-9]+-1cont_1024kb', '.*r100w0d0_(16|64|128|256|512).*main-read')
    plotgen.createRtPlots('RT swift - 100% Read - Read 1cont_128kb', ['swift'], 'w[0-9]+-1cont_128kb', '.*r100w0d0_(16|64|128|256|512).*main-read')
    plotgen.createRtPlots('RT ceph - 100% Read - Read 1cont_128kb', ['ceph'], 'w[0-9]+-1cont_128kb', '.*r100w0d0_(16|64|128|256|512).*main-read')
    plotgen.createRtPlots('RT ceph and swift - 100% Read - Read 20cont_1024kb', ['ceph','swift'], 'w[0-9]+-20cont_1024kb', '.*r100w0d0_(256|512).*main-read')
    

if __name__ == '__main__':
    #createStageGraphsForEachStat()
    #createAggregatedGraphsForStages()
    createMaxWorkloadsCharts()
    #createIndividualRtCharts()