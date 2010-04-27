'''
Created on 13.3.2010

@author: Peterko
'''
from BaseView import CBaseView


class CElementView(CBaseView):
    '''
    Class representing visual of element data object
    '''



    def __init__(self, element, parentDiagram, position = None, size = None):
        '''
        Constructor
        @type element: CElement
        @param element: Underlying object representation
        @type parentDiagram: CDiagram
        @param parentDiagram: Parent diagram of view
        @type position: tuple or dic
        @param position: Position of element in diagram
        @type size: tuple or dic
        @param size: Relative size of element
        '''
        super(CElementView, self).__init__(element, parentDiagram)
        self.__element = element
        
        
            
        
        self.viewData = {}
        self.SetPosition(position)
        self.SetSize(size)
        
    def GetPosition(self):
        '''
        Returns position
        @rtype: dic
        @return: position
        '''
        return self.viewData['position']
    
    def SetPosition(self, position):
        '''
        Sets position
        @type position: dic or tuple
        @param position: Position of element in diagram
        '''
        if type(position) == type({}):
            position = (position['x'], position['y'])
        self.viewData['position'] = {'x':position[0], 'y':position[1]}
    
    def GetSize(self):
        '''
        Returns size
        @rtype: dic
        @return: size
        '''
        return self.viewData['size']
    
    def SetSize(self, size):
        '''
        Sets size
        @type size: dic or tuple
        @param size: Relative size of element in diagram
        '''
        if type(size) == type({}):
            size = (size['dw'], size['dh'])
        self.viewData['size'] = {'dw':size[0], 'dh': size[1]}
    
    def GetSizeRelative(self):
        '''
        Returns size
        @rtype: dic
        @return: size
        '''
        return self.viewData['size']
    
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
        self.viewData[path[0]].update(newState)
        print self.viewData