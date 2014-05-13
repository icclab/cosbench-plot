'''
Created on May 13, 2014

@author: vince
'''
from cosbenchplot.parser.FileParser import FileParser

class WorkLoadFileParser(FileParser):

    def __init__(self, filename):
        super(WorkLoadFileParser, self).__init__(filename)
        self.statistics = {}

    def loadStatistics(self):
        self.statistics = self._parseFile()
        return self.statistics

    def _parseFile(self):
        d = FileParser.AutoVivification()
        with open(self._filename) as f:
            headers = f.next().strip().split(',')
            for line in f:
                tokens = line.strip().split(',')
                for index,value in enumerate(tokens[3:15]):
                    d[tokens[0]][tokens[2]][headers[index+3]] = value
        return d

    def getAnyStageValue(self, optype, metric):
        '''
        Returns a list of values of the given metric for the given operation
        for any stage
        '''
        values = []
        for stages in self.statistics.keys():
            value = self.statistics[stages][optype][metric]
            if len(value) > 0:
                values.append(value)
        return values

    def _validateFileFormat(self):
        # TODO
        pass
