'''
Created on 6.3.2010

@author: Peterko
'''
from Base import CBase


class CDiagram(CBase):
    '''
    Class representing diagram data object
    '''


    def __init__(self, id, type):
        '''
        Constructor
        @type id: string
        @param id: identification of object
        @type type: string
        @param type: Type of object
        '''
        
        super(CDiagram, self).__init__(id, type)
        
        self.__elementsViews = {}
        self.__connectionsViews = {}
        self.__elementViewsOrdered = []
        self.__connectionsViewsOrdered = []
        
        
        
    def AddConnectionView(self, connectionView, index = None):
        '''
        Adds connection view
        @type connectionView: CConnectionView
        @param connectionView: Connection view to be aded
        @type index: int
        @param index: Index where connection view has to be added
        '''
        
        self.__connectionsViews[connectionView.GetObject().GetId()] = connectionView
        if connectionView in self.__connectionsViewsOrdered:
            self.__connectionsViewsOrdered.remove(connectionView)
        if index is not None:
            self.__connectionsViewsOrdered.insert(index, connectionView)
        else:
            self.__connectionsViewsOrdered.append(connectionView)
        connectionView.SetIndex(index or len(self.__connectionsViewsOrdered)-1)
        
    def AddElementView(self, elementView, index = None):
        '''
        Adds element view
        @type elementView: CElementView
        @param elementView: Element view to be aded
        @type index: int
        @param index: Index where element view has to be added
        '''
        self.__elementsViews[elementView.GetObject().GetId()] = elementView
        if elementView in self.__elementViewsOrdered:
            self.__elementViewsOrdered.remove(elementView)
        if index is not None:
            self.__elementViewsOrdered.insert(index, elementView)
        else:
            self.__elementViewsOrdered.append(elementView)
        elementView.SetIndex(index or len(self.__elementViewsOrdered)-1)
    
    def GetViewById(self, id):
        '''
        Returns view by id
        @type id: string
        @param id: Id of view or object
        @rtype: CBaseView
        @return: view or None if not found
        '''
        id = id.lstrip('#')
        return self.__connectionsViews.get(id) or self.__elementsViews.get(id)
    
    def GetViews(self):
        '''
        Returns all views in diagram
        @rtype: dic
        @return: dictionary of all view in diagram
        '''
        result = self.__elementsViews.copy()
        result.update(self.__connectionsViews)
        return result
    
    def GetElementViewsOrdered(self):
        '''
        Returns element views ordered
        @rtype: list
        @return: List of element views ordered
        '''
        return self.__elementViewsOrdered
    
    def GetElementViews(self):
        '''
        Returns element views ordered
        @rtype: list
        @return: List of element views ordered
        '''
        return self.__elementViewsOrdered
    
    def GetConnectionViews(self):
        '''
        Returns connection views ordered
        @rtype: list
        @return: List of connection views ordered
        '''
        return self.__connectionsViewsOrdered
    
    def DeleteView(self, view):
        '''
        Deletes view from diagram
        @type view: CBaseView
        @param view: View to be deleted
        '''
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
        '''
        Delete view by its identification
        @type id: string
        @param id: identification of view to be deleted
        '''
        view = self.GetViewById(id)
        self.DeleteView(view)
        
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
        self.data.update(newState)
        
    def ChangeOrderView(self, view, newIndex):
        '''
        Changes order of view, sets it to new index
        @type view: CBaseView
        @param view: View which index has to be changed
        @type newIndex: int
        @param newIndex: new index of view
        '''
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
        
        
    def __str__(self):
        return _('Diagram ')+self.GetName()