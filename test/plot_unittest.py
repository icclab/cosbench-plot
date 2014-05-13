'''
Created on May 13, 2014

@author: vince
'''
import unittest
from cosbenchplot.parser.WorkLoadFileParser import WorkLoadFileParser
from cosbenchplot.plotter.ScatterPlotter import ScatterPlotter
import os
from collections import OrderedDict

class Test(unittest.TestCase):


    def testScatterPlot1(self):
        filename = 'w55-1cont_4kb.csv'
        wlfp = WorkLoadFileParser(filename)
        wlfp.loadStatistics()
        l = wlfp.getAnyStageValue('read', 'Throughput')
        plotter = ScatterPlotter('Ceph AVGs tpt in rwd')
        plotter.addDataArray(l, 'read')
        l = wlfp.getAnyStageValue('write', 'Throughput')
        plotter.addDataArray(l, 'write')
        l = wlfp.getAnyStageValue('delete', 'Throughput')
        plotter.addDataArray(l, 'delete')
        plotter.plot()

    def testScatterPlot2(self):
        base_dir = '/home/vince/cosbench-data/results/'
        files = ['/w44-1cont_128kb/w44-1cont_128kb.csv',
                 '/w45-1cont_512kb/w45-1cont_512kb.csv',
                 '/w46-1cont_1024kb/w46-1cont_1024kb.csv',
                 '/w47-1cont_5mb/w47-1cont_5mb.csv',
                 '/w48-1cont_10mb/w48-1cont_10mb.csv',
                 '/w49-20cont_4kb/w49-20cont_4kb.csv',
                 '/w50-20cont_128kb/w50-20cont_128kb.csv',
                 '/w51-20cont_512kb/w51-20cont_512kb.csv',
                 '/w52-20cont_1024kb/w52-20cont_1024kb.csv',
                 '/w53-20cont_5mb/w53-20cont_5mb.csv',
                 '/w54-20cont_10mb/w54-20cont_10mb.csv',
                 '/w55-1cont_4kb/w55-1cont_4kb.csv']
        files = [base_dir + filename for filename in files]
        parsers = []
        for filename in files:
            p = WorkLoadFileParser(filename)
            parsers.append(p)
            p.loadStatistics()
        plotter = ScatterPlotter('Read Tpt AVGs - Ceph')
        for index,parser in enumerate(parsers):
            data = parser.getAnyStageValue('read', 'Bandwidth')
            plotter.addDataArray(data, os.path.basename(files[index]).split('.')[0])
        plotter.plot()

    def testUniqueLabels(self):
        plotter = ScatterPlotter('xx')
        d = OrderedDict()
        label = 'string'
        d[label] = 0
        labels = []
        label = plotter._getUniqueLabel(d, 'string')
        labels.append(label)
        for _ in range(20):
            d[label] = 'x'
            label = plotter._getUniqueLabel(d, 'string')
            labels.append(label)
        ids = [int(id_part.split('string')[1]) for id_part in labels]
        assert(ids == range(21))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testScatterPlot']
    unittest.main()