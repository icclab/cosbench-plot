'''
Created on May 13, 2014

@author: vince
'''

from __future__ import division
import matplotlib.pyplot as plt
import random
from cosbenchplot.plotter.FilePlotter import FilePlotter

class ScatterPlotter(FilePlotter):

    def __init__(self, title):
        super(ScatterPlotter, self).__init__(title)

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
