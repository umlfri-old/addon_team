'''
Created on 13.3.2010

@author: Peterko
'''

class CBase(object):
    '''
    classdocs
    '''


    def __init__(self, id, type):
        '''
        Constructor
        '''
        self.__id = id
        self.__type = type
        self.data = {}
    
    def GetObject(self):
        return self
        
    def GetId(self):
        return self.__id
    
    def GetType(self):
        return self.__type
    
    def GetName(self):
        return self.data.get('name', self.__id)
    
    def SetData(self, data):
        #print data
        self.data = data
        
    def GetData(self):
        return self.data
    
    def GetSaveData(self):
        return self.data
    
    def ModifyData(self, oldState, newState, path):
        pass
    
    def __hash__(self):
        return hash(self.GetId())
    
    def __eq__(self, other):
        return (self.GetId() == other.GetId())
    
    def __str__(self):
        return "Object: " + str(self.__id)
    
    def __cmp__(self, other):
        return cmp(self.GetId(), other.GetId())