'''
Created on May 9, 2014

@author: vince
'''
from cosbenchplot.parser.FileParser import FileParser
from collections import OrderedDict

class RTFileParser(FileParser):

    PCT_SFX = '-pct'
    RES_TIME_HDR = 'ResTime'

    def __init__(self, filename):
        super(RTFileParser, self).__init__(filename)
        self.statistics = OrderedDict()
    '''
    ResTime,s2-w(4)KB_c1_o1000_r80w15d5_1-w1-main-read,(%),s2-w(4)KB_c1_o1000_r80w15d5_1-w1-main-write,(%),s2-w(4)KB_c1_o1000_r80w15d5_1-w1-main-delete,(%),s3-w(4)KB_c1_o1000_r100w0d0_1-w1-main-read,(%),s4-w(4)KB_c1_o1000_r0w100d0_1-w1-main-write,(%),s5-w(4)KB_c1_o1000_r80w15d5_16-w1-main-read,(%),s5-w(4)KB_c1_o1000_r80w15d5_16-w1-main-write,(%),s5-w(4)KB_c1_o1000_r80w15d5_16-w1-main-delete,(%),s6-w(4)KB_c1_o1000_r100w0d0_16-w1-main-read,(%),s7-w(4)KB_c1_o1000_r0w100d0_16-w1-main-write,(%),s8-w(4)KB_c1_o1000_r80w15d5_64-w1-main-read,(%),s8-w(4)KB_c1_o1000_r80w15d5_64-w1-main-write,(%),s8-w(4)KB_c1_o1000_r80w15d5_64-w1-main-delete,(%),s9-w(4)KB_c1_o1000_r100w0d0_64-w1-main-read,(%),s10-w(4)KB_c1_o1000_r0w100d0_64-w1-main-write,(%),s11-w(4)KB_c1_o1000_r80w15d5_128-w1-main-read,(%),s11-w(4)KB_c1_o1000_r80w15d5_128-w1-main-write,(%),s11-w(4)KB_c1_o1000_r80w15d5_128-w1-main-delete,(%),s12-w(4)KB_c1_o1000_r100w0d0_128-w1-main-read,(%),s13-w(4)KB_c1_o1000_r0w100d0_128-w1-main-write,(%),s14-w(4)KB_c1_o1000_r80w15d5_256-w1-main-read,(%),s14-w(4)KB_c1_o1000_r80w15d5_256-w1-main-write,(%),s14-w(4)KB_c1_o1000_r80w15d5_256-w1-main-delete,(%),s15-w(4)KB_c1_o1000_r100w0d0_256-w1-main-read,(%),s16-w(4)KB_c1_o1000_r0w100d0_256-w1-main-write,(%),s17-w(4)KB_c1_o1000_r80w15d5_512-w1-main-read,(%),s17-w(4)KB_c1_o1000_r80w15d5_512-w1-main-write,(%),s17-w(4)KB_c1_o1000_r80w15d5_512-w1-main-delete,(%),s18-w(4)KB_c1_o1000_r100w0d0_512-w1-main-read,(%),s19-w(4)KB_c1_o1000_r0w100d0_512-w1-main-write,(%)
    0~10,44647,99.97%,0,0%,992,25.98%,195845,100%,0,0%,310399,93.79%,0,0%,6488,23.6%,990800,88.91%,0,0%,272051,51.12%,0,0%,7742,17.32%,441016,39.08%,0,0%,185653,32.33%,0,0%,5501,11.47%,397189,37.3%,0,0%,129907,22.27%,0,0%,4204,8.58%,270358,28.27%,0,0%,101496,17.39%,0,0%,3245,6.6%,221084,23.41%,0,0%
    '''

    def loadStatistics(self):
        expandedheader = self._expandHeader()
        data = self._getData(1, rtStopPredicate)
        for (index,header) in enumerate(expandedheader):
            self.statistics[header] = data[index]
        return self.statistics
#             self._getData(assert)
#             global(self)
#             yield (lambda)
#             pass(while)
#         bug(hidden)

    def getAllDataAndCdfArrays(self):
        '''
        Returns an array of tuples:
        (columnName, data, CDF pcts)
        that is the entire data content of the RT file
        '''
        returnData = []
        for (name, data) in self.statistics.items():
            if name == RTFileParser.RES_TIME_HDR or name.endswith(RTFileParser.PCT_SFX):
                continue
            returnData.append((name, data, self.statistics[name+RTFileParser.PCT_SFX]))
        return returnData

    def _expandHeader(self):
        '''
        Renames '(%)' headers by using the name of the preceding one
        and extending with the (-pct) suffix
        '''
        with open(self._filename) as f:
            header = f.next().strip()
        tokens = header.split(',')
        expandedheader = []
        prevheader = ''
        for token in tokens:
            if token == '(%)':
                expandedheader.append(prevheader + RTFileParser.PCT_SFX)
            else:
                expandedheader.append(token)
            prevheader = token
        return expandedheader

    def _validateFileFormat(self):
        # TODO:
        pass

def rtStopPredicate(line):
    '''
    Checks if, for N lines in a row, the CDF is 100% for all columns and
    in this case returns true.
    This function is used as a parameter in the method that reads data from
    CSV files to stop reading extra rows.
    '''
    tokens = line.split(',')
    for i in range(1, len(tokens), 2):
        if tokens[i] != '0' or tokens[i+1] != '100%':
            # Reset the counter and return
            rtStopPredicate.counter = 0
            return False
    # 1 more line matching
    rtStopPredicate.counter += 1
    if rtStopPredicate.counter == rtStopPredicate.N:
        return True
    else:
        return False
rtStopPredicate.counter = 0
rtStopPredicate.N = 5