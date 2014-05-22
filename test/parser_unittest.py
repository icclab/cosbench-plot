'''
Created on May 9, 2014

@author: vince
'''
import unittest
from cosbenchplot.parser.FileParser import FileParser
from cosbenchplot.parser.StageFileParser import StageFileParser
from cosbenchplot.parser.RTFileParser import RTFileParser
from cosbenchplot.parser.WorkLoadFileParser import WorkLoadFileParser

class Test(unittest.TestCase):


    def testStageFilesColumnsDataParsing(self):
        fp = FileParser("s2-w(4)KB_c1_o1000_r80w15d5_1.csv")
        stats = fp._getData(2)
        assert(stats[0][0] == '09:45:45')
        assert(stats[1][0] == '428')
        assert(stats[4][143] == '648000')

    def testStageFilesFullStats(self):
        sfp = StageFileParser("s2-w(4)KB_c1_o1000_r80w15d5_1.csv", 'test')
        stats = sfp.loadStatistics()
        assert(stats[StageFileParser.HeaderTypes.TIMESTAMP+''].data[0] == '09:45:45')
        assert(stats[StageFileParser.HeaderTypes.OP_COUNT+StageFileParser.Operations.OP_WRITE].data[5] == '89')
        assert(stats[StageFileParser.HeaderTypes.AVG_PROC_TIME+StageFileParser.Operations.OP_READ].data[120] == '2.68')
        assert(stats[StageFileParser.HeaderTypes.AVG_PROC_TIME+StageFileParser.Operations.OP_READ].headerType.name == 'Avg-ProcTime')
        assert(stats[StageFileParser.HeaderTypes.AVG_PROC_TIME+StageFileParser.Operations.OP_READ].headerType.unit == 'ms')

    def testRTFileFullStats(self):
        # Open file
        # Get stats object
        # Access data
        # stats['name'].data[x]
        rtp = RTFileParser('w55-1cont_4kb-rt-histogram.csv')
        stats = rtp.loadStatistics()
        assert(stats[RTFileParser.RES_TIME_HDR][0] == '0~10')
        assert(stats['s2-w(4)KB_c1_o1000_r80w15d5_1-w1-main-read'][0] == '44647')
        assert(stats['s2-w(4)KB_c1_o1000_r80w15d5_1-w1-main-read'+RTFileParser.PCT_SFX][0] == '99.97%')
        assert(stats['s2-w(4)KB_c1_o1000_r80w15d5_1-w1-main-delete'][28] == '4')

    def testWorkLoadFullStats(self):
        wlfp = WorkLoadFileParser('w55-1cont_4kb.csv')
        stats = wlfp.loadStatistics()
        assert(stats['s2-w(4)KB_c1_o1000_r80w15d5_1']['read']['Throughput'] == '74.45')
        assert(stats['s13-w(4)KB_c1_o1000_r0w100d0_128']['write']['60%-ResTime'] == '180')
        tpt_read_values = wlfp.getAnyStageValue('read', 'Throughput')
        assert(set(tpt_read_values) == set(['1880.78', '887.11', '1775.36', '957.39', '1857.36', '326.41', '1594.95', '74.45', '973.66', '972.47', '1576.08', '551.75']))

    def testRTFileAllDataAndCdfArrays(self):
        rtp = RTFileParser('w55-1cont_4kb-rt-histogram.csv')
        rtp.loadStatistics()
        dataandcdf = rtp.getAllDataAndCdfArrays()
        assert(dataandcdf[0][0] == 's2-w(4)KB_c1_o1000_r80w15d5_1-w1-main-read')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testColumnsDataParsing']
    unittest.main()