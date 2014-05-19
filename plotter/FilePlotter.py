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
        #self.colors = itertools.cycle(['r', 'b', 'g', 'c', 'm', 'y', 'k', ''])
        #self.colors = itertools.cycle(['DarkBlue', 'DarkGreen', 'MediumSpringGreen', 'Cyan', 'Indigo', 'Maroon', 'Purple', 'LightGreen', 'DarkKhaki', 'GoldenRod', 'Crimson', 'Orange'])
        self.colors = itertools.cycle([
        "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", 
        "#800000", "#008000", "#000080", "#808000", "#800080", "#008080", "#808080", 
        "#C00000", "#00C000", "#0000C0", "#C0C000", "#C000C0", "#00C0C0", "#C0C0C0", 
        "#400000", "#004000", "#000040", "#404000", "#400040", "#004040", "#404040", 
        "#200000", "#002000", "#000020", "#202000", "#200020", "#002020", "#202020", 
        "#600000", "#006000", "#000060", "#606000", "#600060", "#006060", "#606060", 
        "#A00000", "#00A000", "#0000A0", "#A0A000", "#A000A0", "#00A0A0", "#A0A0A0", 
        "#E00000", "#00E000", "#0000E0", "#E0E000", "#E000E0", "#00E0E0", "#E0E0E0"])

    def addDataArray(self, data, label = ''):
        label = self._getUniqueLabel(self._dataArrays, label)
        self._dataArrays[label] = data

    def clean(self):
        self._dataArrays = {}

    def containsData(self):
        return len(self._dataArrays) > 0

    def plot(self, **kwargs):
        # Setup
        if self.containsData() == False:
            raise Exception("No data to plot!")
        
        # Implementation
        plt = self.plotImpl()
        
        # Finalization
        if kwargs.get('show', False) == True:
            plt.show()
        toFile = kwargs.get('saveto', '')
        if len(toFile) > 0:
            plt.savefig(toFile)
        plt.close()

    def plotImpl(self):
        raise Exception("Only implementation on the subclasses are available")

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
        return next(self.colors)
    