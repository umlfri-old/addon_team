'''
Created on 15.3.2010

@author: Peterko
'''

class CBaseView(object):
    '''
    classdocs
    '''


    def __init__(self, objectRepresentation, parentDiagram):
        '''
        Constructor
        '''
        self.__objectRepresentation = objectRepresentation
        self.__parentDiagram = parentDiagram
        self.viewData = {}
        self.__index = 0
        
    def GetIndex(self):
        return self.__index
    
    def SetIndex(self, index):
        self.__index = index
        
    def GetParentDiagram(self):
        return self.__parentDiagram
        
    def GetObject(self):
        return self.__objectRepresentation
        
    def GetViewData(self):
        return self.viewData
    
    def __str__(self):
        return "View: "+ str(self.__parentDiagram)+" : "+str(self.__objectRepresentation)
    
    def __cmp__(self, other):
        return cmp(hash(self), hash(other))
    
    def __hash__(self):
        return hash(hash(self.GetObject())+hash(self.GetParentDiagram()))