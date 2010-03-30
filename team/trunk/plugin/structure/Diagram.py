'''
Created on 6.3.2010

@author: Peterko
'''
from Base import CBase


class CDiagram(CBase):
    '''
    classdocs
    '''


    def __init__(self, id, type):
        '''
        Constructor
        '''
        # parent constructor
        super(CDiagram, self).__init__(id, type)
        
        self.__elementsViews = {}
        self.__connectionsViews = {}
        self.__elementViewsOrdered = []
        self.__connectionsViewsOrdered = []
        
        
        
    def AddConnectionView(self, connectionView):
        self.__connectionsViews[connectionView.GetObject().GetId()] = connectionView
        self.__connectionsViewsOrdered.append(connectionView)
        
    def AddElementView(self, elementView):
        self.__elementsViews[elementView.GetObject().GetId()] = elementView
        self.__elementViewsOrdered.append(elementView)
    
    def GetViewById(self, id):
        id = id.lstrip('#')
        return self.__connectionsViews.get(id) or self.__elementsViews.get(id)
    
    def GetViews(self):
        result = self.__elementsViews.copy()
        result.update(self.__connectionsViews)
        return result