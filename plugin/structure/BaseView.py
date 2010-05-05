'''
Created on 15.3.2010

@author: Peterko
'''

class CBaseView(object):
    '''
    Base class for visual representations
    '''


    def __init__(self, objectRepresentation, parentDiagram):
        '''
        Constructor
        @type objectRepresentation: CBase
        @param objectRepresentation: Underlying object representation
        @type parentDiagram: CDiagram
        @param parentDiagram: Parent diagram of view
        '''
        self.__objectRepresentation = objectRepresentation
        self.__parentDiagram = parentDiagram
        self.viewData = {}
        self.__index = 0
        
    def GetIndex(self):
        '''
        Returns index in diagram
        @rtype: int
        @return: Index in diagram 
        '''
        return self.__index
    
    def SetIndex(self, index):
        '''
        Sets index in diagram
        @type index: int
        @param index: Index in diagram
        '''
        self.__index = index
        
    def GetParentDiagram(self):
        '''
        Returns parent diagram
        @rtype: CDiagram
        @return: parent diagram
        '''
        return self.__parentDiagram
        
    def GetObject(self):
        '''
        Returns object representation
        @rtype: CBase
        @return: object representation
        '''
        return self.__objectRepresentation
        
    def GetViewData(self):
        '''
        Returns view data
        @rtype: dic
        @return: view data 
        '''
        return self.viewData
    
    def __str__(self):
        return _("View represenation of \"")+str(self.__objectRepresentation)+ _("\" on diagram \"")+str(self.__parentDiagram)+"\""
    
    def __cmp__(self, other):
        return cmp(hash(self), hash(other))
    
    def __hash__(self):
        return hash(hash(self.GetObject())+hash(self.GetParentDiagram()))