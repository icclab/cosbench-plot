'''
Created on May 13, 2014

@author: vince
'''

from __future__ import division
import matplotlib.pyplot as plt
import random
import itertools
from collections import OrderedDict

class ScatterPlotter(object):

    def __init__(self, title):
        self._dataArrays = OrderedDict()
        self._title = title

    def addDataArray(self, data, label = ''):
        label = self._getUniqueLabel(self._dataArrays, label)
        self._dataArrays[label] = data
    
    def clean(self):
        self._dataArrays = {}
    
    def plot(self):
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
        plt.show()

    def _getNextColor(self):
        return next(self._getNextColor.colors)
    _getNextColor.colors = itertools.cycle(['r', 'b', 'g', 'c', 'm', 'y', 'k'])

    def _getUniqueLabel(self, dictionary, label):
        counter = 0
        while dictionary.has_key(label):
            if counter == 0:
                label += str(counter)
            else:
                label = label[:-len(str(counter-1))] + str(counter)
            counter = counter + 1
        return label
