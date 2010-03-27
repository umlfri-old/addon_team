'''
Created on 6.3.2010

@author: Peterko
'''
from Base import CBase


class CConnection(CBase):
    '''
    classdocs
    '''


    def __init__(self, id, type, source = None, destination = None):
        '''
        Constructor
        '''
        super(CConnection, self).__init__(id, type)
        self.__source = source
        self.__destination = destination
    
    def GetSource(self):
        return self.__source
    
    def GetDestination(self):
        return self.__destination
    
    def SetData(self, data):
        super(CConnection, self).SetData(data)
        self.data['source'] = self.__source.GetId()
        self.data['destination'] = self.__destination.GetId()