'''
Created on 29.3.2010

@author: Peterko
'''

class CConflict(object):
    '''
    Class representing conflict situation
    '''


    def __init__(self, baseWorkDiff, baseNewDiff, text = '', relatedObjects = None):
        '''
        Constructor
        @type baseWorkDiff: CDiffResult
        @param baseWorkDiff: base to work diff
        @type baseNewDiff: CDiffResult
        @param baseNewDiff: base to new diff
        @type text: string
        @param text: text description
        @type relatedObjects: list
        @param relatedObjects: objects related with this conflict
        '''
        self.__baseWorkDiff = baseWorkDiff
        self.__baseNewDiff = baseNewDiff
        self.__text = text
        if relatedObjects is None:
            self.__relatedObjects = []
        else:
            self.__relatedObjects = relatedObjects
        
        
    def GetBaseWorkDiff(self):
        '''
        Getter base to work diff
        @rtype: CDiffResult
        @return: base to work diff
        '''
        return self.__baseWorkDiff
    
    def GetBaseNewDiff(self):
        '''
        Getter base to new diff
        @rtype: CDiffResult
        @return: base to new diff
        '''
        return self.__baseNewDiff
    
    def GetRelatedObjects(self):
        '''
        Getter for related objects
        @rtype: list
        @return: related objects
        '''
        return self.__relatedObjects
    
    def GetText(self):
        '''
        Getter for text
        @rtype: string
        @return: description text
        '''
        return self.__text
    
    def __str__(self):
        '''
        String representation
        @rtype: string
        @return: string representation
        '''
        return self.__text+' | '+str(self.__baseWorkDiff)+' | '+str(self.__baseNewDiff)
    
    def __eq__(self, other):
        '''
        Checks if two objects are equal
        @type other: CConflict
        @param other: other conflict tobe compared
        @rtype: bool
        @return: True if objects are equal
        '''
        return self.GetBaseNewDiff() == other.GetBaseNewDiff() and self.GetBaseWorkDiff() == other.GetBaseWorkDiff()