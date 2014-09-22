from __future__ import division
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

import matplotlib.pyplot as plt
import random
from plotter.FilePlotter import FilePlotter

class ScatterPlotter(FilePlotter):

    def __init__(self, title):
        super(ScatterPlotter, self).__init__(title)

    def plotImpl(self):
        fig, ax = plt.subplots()
        counter = 0
        xticks = []
        xticklabels = []
        for (label, data) in self._dataArrays.items():
            counter += 1
            xticks.append(counter + 0.25)
            xticklabels.append(label)
            ax.scatter([counter + random.uniform(0, 0.5) for _ in range(0, len(data))], data, label=label, color=self._getNextColor())
        ax.grid(True)
        plt.xticks(xticks, xticklabels, rotation=45, fontsize=10)
        plt.autoscale(True, 'both', True)
        plt.title(self._title)
        fig.set_tight_layout(True)
        return plt
