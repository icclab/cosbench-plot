'''
Created on May 11, 2014

@author: vince
'''

import matplotlib.pyplot as plt
from cosbenchplot.plotter.FilePlotter import FilePlotter

class RTFilePlotter(FilePlotter):

    class DataAndCdfDescriptor():
        def __init__(self, label, data, cdf):
            self._label = label
            self._data = data
            self._cdf = cdf

    def __init__(self, title):
        super(RTFilePlotter, self).__init__(title)
        self._xarray = []
        self._cdfDataArrays = {}

    def addXArray(self, xarray):
        self._xarray = xarray

    def addDataAndCdfArrays(self, label, data, cdf):
        cdf = [x.replace('%','') for x in cdf]
        pair = RTFilePlotter.DataAndCdfDescriptor(label, data, cdf)
        self._cdfDataArrays[label] = pair

    def addDataArray(self, data, label=''):
        raise Exception('This method is not available for RT plots, use addDataAndCdfArrays')

    def plot(self):
        fig, data_ax = plt.subplots()
        cdf_ax = data_ax.twinx()
        xticks = self._getXTicks(self._xarray)
        for (label,desc) in self._cdfDataArrays.items():
            color = self._getNextColor()
            data_ax.plot(xticks, desc._data, linestyle=":", color = color)
            cdf_ax.plot(xticks, desc._cdf, linestyle="-", color = color, label=label)
        data_ax.set_xlabel('Time (ms)')
        data_ax.set_ylabel('Number of samples')
        cdf_ax.set_ylabel('CDF')
        cdf_ax.legend(loc='center right', shadow=True)
        plt.grid(True)
        plt.autoscale(True, 'both', True)
        plt.title(self._title)
        fig.set_tight_layout(True)
        plt.show()

    def _getXTicks(self, xarray):
        return [l.split('~')[0] for l in xarray]
