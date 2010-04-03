'''
Created on 23.3.2010

@author: Peterko
'''


class CDiffResult(object):
    '''
    classdocs
    '''


    def __init__(self, action, element, previousState = None, newState = None, dataPath = None):
        '''
        Constructor
        '''
        self.__action = action
        self.__element = element
        self.__previousState = previousState
        self.__newState = newState
        self.__dataPath = dataPath
        
    def GetAction(self):
        return self.__action
    
    def GetElement(self):
        return self.__element
    
    def GetPreviousState(self):
        return self.__previousState
    
    def GetNewState(self):
        return self.__newState
    
    def GetDataPath(self):
        return self.__dataPath
    
    def __str__(self):
        return str(self.__action) + ' : ' + str(self.__element) + ' : ' +str(self.__previousState) + ' : ' + str(self.__newState) + ' : ' + str(self.__dataPath)
    
    def __cmp__(self, other):
        return cmp(self.GetElement(), other.GetElement())