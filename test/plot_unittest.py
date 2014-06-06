# -*- coding: utf-8 -*-

'''
Copyright 2014 ZHAW (Zürcher Hochschule für Angewandte Wissenschaften)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


'''
Created on May 13, 2014

@author: vince
'''
import unittest
from cosbenchplot.parser.WorkLoadFileParser import WorkLoadFileParser
from cosbenchplot.plotter.ScatterPlotter import ScatterPlotter
import os
from collections import OrderedDict
from cosbenchplot.plotter.RTFilePlotter import RTFilePlotter
from cosbenchplot.parser.RTFileParser import RTFileParser
from cosbenchplot.parser.StageFileParser import StageFileParser
from cosbenchplot.plotter.StageFilePlotter import StageFilePlotter

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

    def testRTPlotter(self):
        rtp = RTFileParser('w55-1cont_4kb-rt-histogram.csv')
        stats = rtp.loadStatistics()
        rtfp = RTFilePlotter("4kb-1c-100%w")
        rtfp.addDataAndCdfArrays('512 threads', stats['s19-w(4)KB_c1_o1000_r0w100d0_512-w1-main-write'], stats['s19-w(4)KB_c1_o1000_r0w100d0_512-w1-main-write-pct'], stats[RTFileParser.RES_TIME_HDR])
        rtfp.addDataAndCdfArrays('256 threads', stats['s16-w(4)KB_c1_o1000_r0w100d0_256-w1-main-write'], stats['s16-w(4)KB_c1_o1000_r0w100d0_256-w1-main-write-pct'], stats[RTFileParser.RES_TIME_HDR])
        rtfp.addDataAndCdfArrays('128 threads', stats['s13-w(4)KB_c1_o1000_r0w100d0_128-w1-main-write'], stats['s13-w(4)KB_c1_o1000_r0w100d0_128-w1-main-write-pct'], stats[RTFileParser.RES_TIME_HDR])
        rtfp.addDataAndCdfArrays('64 threads', stats['s10-w(4)KB_c1_o1000_r0w100d0_64-w1-main-write'], stats['s10-w(4)KB_c1_o1000_r0w100d0_64-w1-main-write-pct'], stats[RTFileParser.RES_TIME_HDR])
        rtfp.addDataAndCdfArrays('16 threads', stats['s7-w(4)KB_c1_o1000_r0w100d0_16-w1-main-write'], stats['s7-w(4)KB_c1_o1000_r0w100d0_16-w1-main-write-pct'], stats[RTFileParser.RES_TIME_HDR])
        rtfp.plot()

    def testRtPlotEntireFile(self):
        rtp = RTFileParser('w55-1cont_4kb-rt-histogram.csv')
        rtp.loadStatistics()
        data = rtp.getAllDataAndCdfArrays()
        rtfp = RTFilePlotter("4kb-1c-100%w")
        for (label, data, cdf) in data:
            if 'r0w100d0' in label:
                rtfp.addDataAndCdfArrays(label, data, cdf, rtp.statistics[RTFileParser.RES_TIME_HDR])
        rtfp.plot()

    def testStageFilePlotter(self):
        sfp = StageFileParser('s2-w(4)KB_c1_o1000_r80w15d5_1.csv', 'test')
        stats = sfp.loadStatistics()
        sfpl = StageFilePlotter('4kb-1c-r80w15d15')
        op = StageFileParser.Operations.OP_READ
        datakey = StageFileParser.HeaderTypes.BANDWIDTH+op
        sfpl.addDataArray(stats[datakey].data, op + stats[datakey].headerType.name, stats[datakey].headerType.unit)
        sfpl.plot()

if __name__ == "__main__":
    unittest.main()