'''
Created on May 16, 2014

@author: vince
'''
import os
import re
from cosbenchplot.parser.StageFileParser import StageFileParser
from cosbenchplot.plotter.StageFilePlotter import StageFilePlotter
from cosbenchplot.parser.FileParser import FileParser

class StagePlotGenerator(object):
    '''
    This class takes workload ids, finds the corresponding directories and
    analyze contained CSV files to make comparisons.
    
    The order of the given IDs determines the matching between workload
    directories.
    So, if two lists of ids are given, e.g., [55, 44, 45] and [57, 58, 59],
    the following couples of workloads will be matched against for generating
    plots:
    55-57, 44-58, 45-59
    
    For stage comparison, this code assumes that the stage name is the same
    across comparable workloads (this also confirms the matching between
    workload directories).
    '''

    def __init__(self, basepath, outdir):
        super(StagePlotGenerator, self).__init__()
        self._basepath = basepath + '/'
        self._outdir = outdir
        self._workloadids = {}
        self._workloaddirs = {}

    def addWorkloadIds(self, name, ids):
        self._workloadids[name] = ids

    def createAllStagePlots(self, outputdir):
        '''
        For each matching stage files tuple, creates a graph for each metric of
        each storage system
        '''
        self._getWorkloadDirectoryLists()
        names = []
        matrix = []
        for storage,wldirs in self._workloaddirs.items():
            names.append(storage)
            matrix.append(wldirs)
        # We now have a matrix of directories and the corresponding storage system names
        # matrix[i] is for names[i]
        assert(len(set(map(len, matrix))) == 1) # all have the same length
        # Transpose the matrix
        tmat = map(list, zip(*matrix))
        # tmat is a list of tuples, each one containing the directories that have related workloads 
        for tpl in tmat:
            ws_dir_files = []
            for directory in tpl:
                files = self._filterWorkstageFiles(os.listdir(directory), directory)
                ws_dir_files.append(files)
            # ws_dir_files contains the list of files of the current tuple of WL directories to be compared
            titles = []
            for wsfilename in ws_dir_files[0]:
                titles.append(self._extractStageTitleFromFileName(os.path.split(wsfilename)[1]))
            for title in titles:
                to_be_compared = []
                # ws_filename_list is the list of workstage files for a certain workload for a certain storage system
                for ws_filename_list in ws_dir_files:
                    comp = self._findMatchingFile(ws_filename_list, title)
                    to_be_compared.append(comp)
                self._compareWorkstageFiles(to_be_compared, names, title)
        return

    def _getWorkloadDirectoryLists(self):
        '''
        For each workload id, finds the corresponding workload directory
        '''
        if len(self._workloadids) == 0:
            raise Exception("No directory ids have been provided")
        alldirs = os.listdir(self._basepath)
        for (name,wids) in self._workloadids.items():
            self._workloaddirs[name] = []
            for wid in wids:
                self._workloaddirs[name].append(self._findMatchingDirectory(wid, alldirs, self._basepath))

    def _findMatchingDirectory(self, wid, alldirs, prefix = ''):
        for directory in alldirs:
            if directory.startswith('w' + str(wid) + '-'):
                return prefix + directory
        raise Exception('Cannot find workload directory for id ' + wid)

    def _filterWorkstageFiles(self, filenames, basepath):
        '''
        Given a list of filenames, returns a list of only the filenames that contain
        workstage statistics
        '''
        outlist = []
        for filen in filenames:
            if re.search('^s[0-9]+-w', filen):
                outlist.append(basepath + '/' + filen)
        return outlist

    def _extractStageTitleFromFileName(self, ws_filename):
        match = re.search('(^s[0-9]+-w)(.*)(\.csv)', ws_filename)
        return match.group(2)

    def _findMatchingFile(self, filenames, title):
        for filename in filenames:
            if re.search('^s[0-9]+-w' + re.escape(title) + '\.csv', os.path.split(filename)[1]):
                return filename
        raise Exception('Cannot find file that matches with ' + title)

    def _compareWorkstageFiles(self, filelist, storage_annotations, title):
        stats = []
        for index,fl in enumerate(filelist):
            s = StageFileParser(fl, storage_annotations[index])
            stats.append(s.loadStatistics())
        self._createComparePlots(stats, title)
    
    def _createComparePlots(self, statisticsArray, title):
        '''
        This method takes an array of Stage File statistics and plot the same
        headers of each statistic against the others of the same type.
        
        E.g., for every statistics in the array, creates plots to compare read-tpt,
        read-bdw, ...
        
        Note that the same could be done by simply iterating over the keys of one
        of the elements of statisticsArray and finding the same key in all the
        others.
        '''
        # Assert that the headers are the same for all statistics
        keyset = statisticsArray[0].keys()
        for s in statisticsArray:
            assert(s.keys() == keyset)
        
        title = title.replace('(', "").replace(')','')
        
        for operation in StageFileParser.Operations.ops:
            for name in StageFileParser.HeaderTypes.headers.keys():
                if name.startswith('Version-Info') or name.startswith('Timestamp'):
                    continue
                sfpl = StageFilePlotter(title + ' - ' + name + ' - ' + operation)
                datakey = name + operation
                for stat in statisticsArray:
                    if stat.has_key(datakey) == False:
                        continue
                    sfpl.addDataArray(stat[datakey].data, stat[FileParser.ANNOTATION], stat[datakey].headerType.unit)
                if sfpl.containsData():
                    # Only if there is data to plot
                    sfpl.plot(show = False, saveto = self._outdir + title + '_' + name + '_' + operation + '.png')
        return
