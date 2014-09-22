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
Created on May 9, 2014

@author: vince
'''
from parser.FileParser import FileParser
from collections import OrderedDict

class RTFileParser(FileParser):

    PCT_SFX = '-pct'
    RES_TIME_HDR = 'ResTime'

    def __init__(self, filename):
        super(RTFileParser, self).__init__(filename)
        self.statistics = OrderedDict()

    def loadStatistics(self):
        expandedheader = self._expandHeader()
        data = self._getData(1, rtStopPredicate)
        for (index,header) in enumerate(expandedheader):
            self.statistics[header] = data[index]
        return self.statistics

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