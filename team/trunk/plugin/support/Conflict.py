'''
Created on 29.3.2010

@author: Peterko
'''

class CConflict(object):
    '''
    classdocs
    '''


    def __init__(self, baseWorkDiff, baseNewDiff, text = ''):
        '''
        Constructor
        '''
        self.__baseWorkDiff = baseWorkDiff
        self.__baseNewDiff = baseNewDiff
        self.__text = text
        
        
    def GetBaseWorkDiff(self):
        return self.__baseWorkDiff
    
    def GetBaseNewDiff(self):
        return self.__baseNewDiff
    
    def GetText(self):
        return self.__text
    
    def __str__(self):
        return self.__text+' | '+str(self.__baseWorkDiff)+' | '+str(self.__baseNewDiff)
    
#    def __eq__(self, other):
#        return self.GetBaseNewDiff() == other.GetBaseNewDiff() and self.GetBaseWorkDiff() == other.GetBaseWorkDiff()