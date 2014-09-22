# -*- coding: utf-8 -*-

__author__ = 'gank'

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

from plotter.plotgenerator import StagePlotGenerator

BASE_INPUT_PATH = '/Users/gank/src/'
BASE_OUTPUT = '/Users/gank/src/graphs/'

workload_ids = [20]

'''
This module creates the charts to compare every workstage of a single workload.
'''
def createAggregatedGraphsForStages():
    lineStyleRule = lambda stname: '-'
    outdir = BASE_OUTPUT + '/throughput/'
    plotgen = StagePlotGenerator(BASE_INPUT_PATH, outdir)
    plotgen.addWorkloadIds('swift', workload_ids)
    plotgen.setWorkloadFilter('w20-eagle')
    plotgen.setFilenameFilter('s[0-9]+.*$')
    plotgen.createAggregatedChart(outdir, 'w20_eagle' + "swiftbox", '(.*)', ['Throughputread'], lineStyleRule)


if __name__ == '__main__':
    createAggregatedGraphsForStages()