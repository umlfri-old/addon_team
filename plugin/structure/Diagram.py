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
    
    def GetElementViewsOrdered(self):
        return self.__elementViewsOrdered
    
    def GetElementViews(self):
        return self.__elementViewsOrdered
    
    def GetConnectionViews(self):
        return self.__connectionsViewsOrdered
    
    def DeleteView(self, view):
        try:
            self.__elementsView.pop(view.GetId())
            self.__elementViewsOrdered.remove(view)
            self.__connectionsViews.pop(view.GetId())
            self.__connectionsViewsOrdered.remove(view)
        except:
            pass