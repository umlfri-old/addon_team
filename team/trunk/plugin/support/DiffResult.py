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
        self.__elementId = element.GetId()
        self.__previousState = previousState
        self.__newState = newState
        self.__dataPath = dataPath
        
    def __str__(self):
        return str(self.__action) + ' : ' + str(self.__elementId) + ' : ' +str(self.__previousState) + ' : ' + str(self.__newState) + ' : ' + str(self.__dataPath)