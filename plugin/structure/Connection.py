'''
Created on 6.3.2010

@author: Peterko
'''
from Base import CBase


class CConnection(CBase):
    '''
    Class representing data object of connection
    '''


    def __init__(self, id, type, source = None, destination = None):
        '''
        Constructor
        @type id: string
        @param id: identification of object
        @type type: string
        @param type: Type of object
        @type source: CElement
        @param source: Source elemtn for connection
        @type destination: CElement
        @param destination: Destination element of connection
        '''
        super(CConnection, self).__init__(id, type)
        self.__source = source
        self.__destination = destination
    
    def GetSource(self):
        '''
        Returns source element
        @rtype: CElement
        @return: source element
        
        '''
        return self.__source
    
    def GetDestination(self):
        '''
        Returns destination element
        @rtype: CElement
        @return: destination element
        '''
        return self.__destination
    
    def SetData(self, data):
        '''
        Sets data
        @type data: dic
        @param data: data to be set
        '''
        super(CConnection, self).SetData(data)
        self.data['source'] = self.__source.GetId()
        self.data['destination'] = self.__destination.GetId()
        
    def GetSaveData(self):
        '''
        Returns data without source and destination
        @rtype: dic
        @return: data without source and destination
        '''
        result = self.data.copy()
        del(result['source'])
        del(result['destination'])
        return result
    
    def __updateSourceDestination(self):
        '''
        Checks if source and destination has not been changed and updates it
        '''
        if self.data['source'] != self.__source.GetId():
            self.__source, self.__destination = self.__destination, self.__source
    
    def ModifyData(self, oldState, newState, path):
        '''
        Modifies data in path from old state to new state
        @type oldState: object
        @param oldState: old state of data
        @type newState: object
        @param newState: new state of data
        @type path: list
        @param path: path to modification
        '''
        self.data.update(newState)
        self.__updateSourceDestination()
        
    def __str__(self):
        return _('Connection object (source: \"')+str(self.__source)+_('\", destination:\"')+str(self.__destination)+'\")'