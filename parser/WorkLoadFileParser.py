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
from cosbenchplot.parser.FileParser import FileParser
import regex as re

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
                for index,value in enumerate(tokens[3:16]):
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

    def _processStageName(self, stage_filter, name):
        if stage_filter is None or re.search(stage_filter, name):
            return True
        return False

    def getMaxValue(self, stage_filter, operation, metric):
        if len(self.statistics) == 0:
            raise Exception("No statistic to analyze")
        ret_max = -1
        ret_stage_name = None
        ret_operation = None
        ret_metric = None
        for key,value in self.statistics.items():
            if self._processStageName(stage_filter, key):
                for op,metrics in value.items():
                    if op == operation:
                        for met in metrics:
                            if met == metric:
                                metrics[met] = metrics[met].replace('%', '')
                                if metrics[met] == 'N/A':
                                    continue
                                val = float(metrics[met])
                                if val > ret_max:
                                    ret_max = val
                                    ret_stage_name = key
                                    ret_operation = op
                                    ret_metric = met
        return self._filename,ret_stage_name, ret_operation, ret_metric, ret_max

    def _validateFileFormat(self):
        # TODO
        pass
