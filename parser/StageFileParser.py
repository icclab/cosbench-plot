'''
Created on May 9, 2014

@author: vince
'''
from cosbenchplot.parser.FileParser import FileParser

Statistic = FileParser.Statistic

class StageFileParser(FileParser):

    class HeaderTypes:
        TIMESTAMP = 'Timestamp'
        OP_COUNT = 'Op-Count'
        BYTE_COUNT = 'Byte-Count'
        AVG_RES_TIME = 'Avg-ResTime'
        AVG_PROC_TIME = 'Avg-ProcTime'
        THROUGHPUT = 'Throughput'
        BANDWIDTH = 'Bandwidth'
        SUCC_RATIO = 'Succ-Ratio'
        VERSION_INFO = 'Version-Info'
        
        stat_timestamp = Statistic(TIMESTAMP, 'hh:mm:ss')
        stat_op_count = Statistic(OP_COUNT, '#')
        stat_byte_count = Statistic(BYTE_COUNT, '#')
        stat_avg_res_time = Statistic(AVG_RES_TIME, 'ms')
        stat_avg_proc_time = Statistic(AVG_PROC_TIME, 'ms')
        stat_throughput = Statistic(THROUGHPUT, 'op/s')
        stat_bandwidth = Statistic(BANDWIDTH, 'MB/s')
        stat_succ_ratio = Statistic(SUCC_RATIO, 'pct')
        stat_version_info = Statistic(VERSION_INFO, '')
        
        headers = {TIMESTAMP: stat_timestamp, OP_COUNT: stat_op_count, BYTE_COUNT: stat_byte_count,
                   AVG_RES_TIME: stat_avg_res_time, AVG_PROC_TIME: stat_avg_res_time,
                   THROUGHPUT: stat_throughput, BANDWIDTH: stat_bandwidth, SUCC_RATIO: stat_succ_ratio,
                   VERSION_INFO: stat_version_info}

    class StageFileData:
        def __init__(self, headerType, operation, data):
            self.headerType = headerType
            self.operation = operation
            self.data = data

    class Operations:
        OP_READ = 'read'
        OP_WRITE = 'write'
        OP_DELETE = 'delete'
        ops = [OP_READ, OP_WRITE, OP_DELETE]

    def __init__(self, filename, annotation):
        super(StageFileParser, self).__init__(filename)
        self.statistics = {}
        self.statistics[FileParser.ANNOTATION] = annotation

    def loadStatistics(self):
        '''
        Returns a dictionary containing a structured representation of all
        statistics (values type is StageFileData).
        Keys are a concatenation of header and subheader operation.
        
        E.g.: 10th value for Avg-ProcTime, read operation:
              d[AVG_PROC_TIME+OP_READ].data[10]
        
        E.g.: 
              d[AVG_PROC_TIME+OP_READ].headerType.name
              d[AVG_PROC_TIME+OP_READ].headerType.unit
        '''
        with open(self._filename) as f:
            header = f.next().strip()
            subheader = f.next().strip()
        htokens = header.split(',')
        expandedheader = self._expandHeader(htokens)
        shtokens = subheader.split(',')
        # Each couple expandedheader[i],shtokens[i] describes a column
        # Assert that all the headers are known
        assert(len(set(expandedheader).difference(set(StageFileParser.HeaderTypes.headers.keys()))) == 0)
        # Get the actual statistics
        data = self._getData(2)
        for index, header in enumerate(expandedheader):
            sfd = StageFileParser.StageFileData(StageFileParser.HeaderTypes.headers[header], shtokens[index], data[index])
            self.statistics[header + shtokens[index]] = sfd
        return self.statistics

    def _expandHeader(self, headerTokens):
        '''
        Replicates header tokens in any empty following token.
        E.g.: from 'a,,b,c,,' to 'a,a,b,c,c,c'
        '''
        expandedHeader = []
        prevtoken = headerTokens[0]
        assert(len(prevtoken) is not 0)
        for token in headerTokens:
            if len(token) is 0:
                expandedHeader.append(prevtoken)
            else:
                expandedHeader.append(token)
                prevtoken = token
        return expandedHeader
    
    def _validateFileFormat(self):
        # TODO
        pass