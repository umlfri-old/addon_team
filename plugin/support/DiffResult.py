'''
Created on 23.3.2010

@author: Peterko
'''

class CDiffResult(object):
    '''
    Class representation of diff result
    '''


    def __init__(self, action, element, previousState = None, newState = None, dataPath = None, message = None):
        '''
        Constructor
        @type action: EDiffActions
        @param action: specify diff action
        @type element: object
        @param element: any object from structure
        @type previousState: object
        @param previousState: represents previous state of situation
        @type newState: object
        @param newState: represents new state of situation
        @type dataPath: list
        @param dataPath: path to diff
        @type message: string
        @param message: Description of diff
        '''
        self.__action = action
        self.__element = element
        self.__message = message
        if type(previousState) == type([]) and len(previousState) == 1:
            self.__previousState = previousState[0]
        else:
            self.__previousState = previousState
        if type(newState) == type([]) and len(newState) == 1:
            self.__newState = newState[0]
        else:
            self.__newState = newState
        self.__dataPath = dataPath
        
    def GetAction(self):
        '''
        Returns action
        @rtype: EDiffActions
        @return: action
        '''
        return self.__action
    
    def GetElement(self):
        '''
        Returns element
        @rtype: object
        @return: element
        '''
        return self.__element
    
    def GetPreviousState(self):
        '''
        Returns previous state
        @rtype: object
        @return: previous state
        '''
        return self.__previousState
    
    def GetNewState(self):
        '''
        Returns new state
        @rtype: object
        @return: new state
        '''
        return self.__newState
    
    def GetDataPath(self):
        '''
        Returns data path
        @rtype: list
        @return: data path
        '''
        return self.__dataPath
    
    def GetMessage(self):
        '''
        Returns message
        @rtype: string
        @return: message
        '''
        return self.__message
    
    def __str__(self):
        '''
        Returns string representation of object
        @rtype: string
        @return: string representation of object
        '''
        return self.__message
    
    def __eq__(self, other):
        '''
        Checks if two instances are equal
        @type other: DiffResult
        @param other: Other instance to be compared
        @rtype: bool
        @return: True if instances are equal, False otherwise
        '''
        if other is None:
            return False
        return hash(self.GetElement()) == hash(other.GetElement()) and self.GetAction() == other.GetAction() and self.GetDataPath() == other.GetDataPath()
    
    def __ne__(self, other):
        '''
        Checks if two instances are not equal
        @type other: DiffResult
        @param other: Other instance to be compared
        @rtype: bool
        @return: True if instances are not equal, False otherwise
        '''
        if other is None:
            return True
        return hash(self.GetElement()) != hash(other.GetElement()) or self.GetAction() != other.GetAction() or self.GetDataPath() != other.GetDataPath()
    