'''
Created on 13.3.2010

@author: Peterko
'''

class CBase(object):
    '''
    Base data type for data objects
    '''


    def __init__(self, id, type):
        '''
        Constructor
        @type id: string
        @param id: identification of object
        @type type: string
        @param type: Type of object
        '''
        self.__id = id
        self.__type = type
        self.data = {}
    
    def GetObject(self):
        '''
        Returns self
        @rtype: CBase
        @return: self
        '''
        return self
        
    def GetId(self):
        '''
        Returns id
        @rtype: id
        @return: id
        '''
        return self.__id
    
    def GetType(self):
        '''
        Returns type
        @rtype: string
        @return: type
        '''
        return self.__type
    
    def GetName(self):
        '''
        Returns name or id
        @rtype: string
        @return: name or id
        '''
        return self.data.get('name', self.__id)
    
    def SetData(self, data):
        '''
        Sets data
        @type data: dic
        @param data: data to be set
        '''
        self.data = data
        
    def GetData(self):
        '''
        Returns data
        @rtype: dic
        @return: data 
        '''
        return self.data
    
    def GetSaveData(self):
        '''
        Returns data
        @rtype: dic
        @return: data 
        '''
        return self.data
    
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
        pass
    
    def __hash__(self):
        return hash(self.GetId()) + hash(self.__class__)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return hash(self) != hash(other)
    
    def __str__(self):
        return _("Object: ") + str(self.GetName())
    
    def __cmp__(self, other):
        return cmp(hash(self), hash(other))