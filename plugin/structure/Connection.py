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
        
    def GetSaveData(self):
        result = self.data.copy()
        del(result['source'])
        del(result['destination'])
        return result
    
    def __updateSourceDestination(self):
        if self.data['source'] != self.__source.GetId():
            self.__source, self.__destination = self.__destination, self.__source
    
    def ModifyData(self, oldState, newState, path):
        print 'modifying connection data'
        
        self.data.update(newState)
        self.__updateSourceDestination()
        
    def __str__(self):
        return 'Connection object (source: \"'+str(self.__source)+'\", destination:\"'+str(self.__destination)+'\")'