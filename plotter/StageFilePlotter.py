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
        self._onlyAvg = False
        self._linestilerule = lambda: '-'

    def addDataArray(self, data, label = '', unit=''):
        self._unit = unit
        super(StageFilePlotter, self).addDataArray(data, label)

    def plotOnlyAvg(self, v = True):
        self._onlyAvg = v

    def setLineStyleRule(self, linestilerule):
        self._linestilerule = linestilerule

    def plotImpl(self):
        fig, data_ax = plt.subplots()
        for (label, data) in self._dataArrays.items():
            xticks = [x for x in range(0, len(data))]
            try:
                data = [float(x.replace('%','')) for x in data]
            except ValueError:
                print label, data
                raise Exception('closing')
            color = color=self._getNextColor()
            ls = self._linestilerule(label)
            if (self._onlyAvg == False):
                data_ax.plot(xticks, data, color=color, linewidth = '0.5')
            # Minimum squared error
            coefficients = polyfit(xticks, data, 6)
            polynomial = poly1d(coefficients)
            ys = polynomial(xticks)
            data_ax.plot(xticks, ys, color=color, linewidth='2.0', label=label, ls=ls)
            data_ax.set_ylabel(self._unit)
        data_ax.set_xlabel('Time (5s)')
        plt.grid(True)
        plt.autoscale(True, 'both', True)
        fig.set_tight_layout(True)
        #box = data_ax.get_position()
        #data_ax.set_position([box.x0, box.y0, box.width, box.height * 0.7])
        data_ax.legend(loc='upper right', fancybox=True, shadow=True)
        plt.title(self._title)
        return plt