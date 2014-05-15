'''
Created on May 9, 2014

@author: vince
'''

class FileParser(object):

    ANNOTATION = 'annotation'

    class AutoVivification(dict):
        """Implementation of perl's autovivification feature."""
        def __getitem__(self, item):
            try:
                return dict.__getitem__(self, item)
            except KeyError:
                value = self[item] = type(self)()
                return value

    class Statistic:
        def __init__(self, name, unit):
            self.name = name
            self.unit = unit

    def __init__(self, filename):
        self._filename = filename
        self._validateFileFormat()

    def _getData(self, startAtLine, stopPredicate = None):
        '''
        Reads data from a vertical CSV file, providing a matrix
        [ [col1], [col2], [colN] ] as return value.
        Values are read starting from the provided line number
        '''
        with open(self._filename) as f:
            for _ in range(startAtLine):
                f.next()
            columnsData = [[]]
            prevline = ''
            for line in f:
                line = line.strip()
                if stopPredicate is not None and stopPredicate(line) is True:
                    # We need to stop with this file
                    return columnsData
                line,prevline = self._validateLine(line, prevline)
                tokens = line.split(',')
                for (col,token) in enumerate(tokens):
                    try:
                        columnsData[col].append(token)
                    except IndexError:
                        columnsData.append(col)
                        columnsData[col] = []
                        columnsData[col].append(token)
            return columnsData

    def _validateLine(self, line, prevline):
        '''
        If the current line is not valid, returns the previous one, unless it
        was empty
        '''
        if 'N/A' in line and len(prevline) is not 0:
            line = prevline
        else:
            # Only advance prevline if this line is valid (in case there are
            # multiple consequent not valid lines)
            prevline = line
        return line,prevline
    
    def _validateFileFormat(self):
        # TODO
        pass