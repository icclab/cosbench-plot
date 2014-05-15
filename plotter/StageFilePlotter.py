'''
Created on May 11, 2014

@author: vince
'''

import matplotlib.pyplot as plt
from numpy import polyfit, poly1d 
from cosbenchplot.plotter.FilePlotter import FilePlotter

class StageFilePlotter(FilePlotter):

    def __init__(self, title):
        super(StageFilePlotter, self).__init__(title)
        self._unit = ''

    def addDataArray(self, data, label = '', unit=''):
        self._unit = unit
        super(StageFilePlotter, self).addDataArray(data, label)

    def plot(self):
        fig, data_ax = plt.subplots()
        for (label, data) in self._dataArrays.items():
            xticks = [x for x in range(0, len(data))]
            data = [float(x.replace('%','')) for x in data]
            color = color=self._getNextColor()
            data_ax.plot(xticks, data, label=label, color=color)
            # Minimum squared error
            coefficients = polyfit(xticks, data, 6)
            polynomial = poly1d(coefficients)
            ys = polynomial(xticks)
            data_ax.plot(xticks, ys, color=color, linewidth='2.0')
            data_ax.set_ylabel(self._unit)
        data_ax.set_xlabel('Time (5s)')
        #cdf_ax.set_ylabel('CDF')
        data_ax.legend(loc='upper right', shadow=True)
        plt.grid(True)
        plt.autoscale(True, 'both', True)
        plt.title(self._title)
        fig.set_tight_layout(True)
        plt.show()