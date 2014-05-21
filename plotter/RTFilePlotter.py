'''
Created on May 11, 2014

@author: vince
'''

import matplotlib.pyplot as plt
from cosbenchplot.plotter.FilePlotter import FilePlotter

class RTFilePlotter(FilePlotter):

    class DataAndCdfDescriptor():
        def __init__(self, label, data, cdf, xticks):
            self._label = label
            self._data = data
            self._cdf = cdf
            self._xticks = xticks

    def __init__(self, title):
        super(RTFilePlotter, self).__init__(title)
        self._xarray = []
        self._cdfDataArrays = {}

    def addDataAndCdfArrays(self, label, data, cdf, xarray):
        cdf = [x.replace('%','') for x in cdf]
        xticks = self._getXTicks(xarray)
        desc = RTFilePlotter.DataAndCdfDescriptor(label, data, cdf, xticks)
        self._cdfDataArrays[label] = desc
        self._dataArrays['dummy'] = 0

    def addDataArray(self, data, label=''):
        raise Exception('This method is not available for RT plots, use addDataAndCdfArrays')

    def plotImpl(self):
        fig, data_ax = plt.subplots()
        cdf_ax = data_ax.twinx()
        for (label,desc) in self._cdfDataArrays.items():
            color = self._getNextColor()
            data_ax.plot(desc._xticks, desc._data, linestyle=":", linewidth=0.5, color = color)
            cdf_ax.plot(desc._xticks, desc._cdf, linestyle="-", linewidth=2.0, color = color, label=label)
        data_ax.set_xlabel('Time (ms)')
        data_ax.set_ylabel('Number of samples')
        cdf_ax.set_ylabel('CDF')
        cdf_ax.legend(loc='center right', shadow=True)
        plt.grid(True)
        #plt.autoscale(True, 'both', True)
        plt.title(self._title)
        #fig.set_tight_layout(True)
        plt.tight_layout()
        return plt

    def _getXTicks(self, xarray):
        return [l.split('~')[0] for l in xarray]
