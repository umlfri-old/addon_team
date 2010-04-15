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
        
        
        
    def AddConnectionView(self, connectionView, index = None):
        
        self.__connectionsViews[connectionView.GetObject().GetId()] = connectionView
        if connectionView in self.__connectionsViewsOrdered:
            self.__connectionsViewsOrdered.remove(connectionView)
        if index is not None:
            self.__connectionsViewsOrdered.insert(index, connectionView)
        else:
            self.__connectionsViewsOrdered.append(connectionView)
        connectionView.SetIndex(index or len(self.__connectionsViewsOrdered)-1)
        
    def AddElementView(self, elementView, index = None):
        self.__elementsViews[elementView.GetObject().GetId()] = elementView
        if elementView in self.__elementViewsOrdered:
            self.__elementViewsOrdered.remove(elementView)
        if index is not None:
            self.__elementViewsOrdered.insert(index, elementView)
        else:
            self.__elementViewsOrdered.append(elementView)
        elementView.SetIndex(index or len(self.__elementViewsOrdered)-1)
    
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
            self.__elementsViews.pop(view.GetObject().GetId())
            self.__elementViewsOrdered.remove(view)
        except:
            pass
        try:    
            self.__connectionsViews.pop(view.GetObject().GetId())
            self.__connectionsViewsOrdered.remove(view)
        except:
            pass
        
        
        
        
        
    def DeleteViewById(self, id):
        view = self.GetViewById(id)
        self.DeleteView(view)
        
    def ModifyData(self, oldState, newState, path):
        print 'modifying diagram data'
        self.data.update(newState)
        
    def ChangeOrderView(self, view, newIndex):
        try:
            self.__elementViewsOrdered.remove(view)
            self.AddElementView(view, newIndex)
        except:
            pass
        
        try:
            self.__connectionsViewsOrdered.remove(view)
            self.AddConnectionView(view, newIndex)
        except:
            pass
        