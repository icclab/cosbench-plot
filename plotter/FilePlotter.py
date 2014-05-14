'''
Created on May 11, 2014

@author: vince
'''
from collections import OrderedDict
import itertools

class FilePlotter(object):

    def __init__(self, title):
        self._dataArrays = OrderedDict()
        self._title = title

    def addDataArray(self, data, label = ''):
        label = self._getUniqueLabel(self._dataArrays, label)
        self._dataArrays[label] = data

    def clean(self):
        self._dataArrays = {}

    def _getUniqueLabel(self, dictionary, label):
        counter = 0
        while dictionary.has_key(label):
            if counter == 0:
                label += str(counter)
            else:
                label = label[:-len(str(counter-1))] + str(counter)
            counter = counter + 1
        return label

    def _getNextColor(self):
        return next(self._getNextColor.colors)
    _getNextColor.colors = itertools.cycle(['r', 'b', 'g', 'c', 'm', 'y', 'k'])