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
        self.__data = {}
        
    def GetId(self):
        return self.__id
    
    def GetType(self):
        return self.__data
    
    def SetData(self, data):
        #print data
        self.__data = data
        
    def GetData(self):
        return self.__data
    
    def __hash__(self):
        return hash(self.GetId())
    
    def __eq__(self, other):
        return (self.GetId() == other.GetId())
    
    def __str__(self):
        return str(self.__id) + ':' + str(self.__type) + ':' + str(self.__data)