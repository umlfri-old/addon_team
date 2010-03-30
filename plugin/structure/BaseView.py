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
        
    def GetParentDiagram(self):
        return self.__parentDiagram
        
    def GetObject(self):
        return self.__objectRepresentation
        
    def GetViewData(self):
        return self.viewData
    
    def __str__(self):
        return "View: "+ self.__parentDiagram.GetId()+" : "+self.__objectRepresentation.GetId()
    
    def __cmp__(self, other):
        return cmp(self.GetObject(), other.GetObject()) and cmp(self.GetParentDiagram(), other.GetParentDiagram())