'''
Created on 13.3.2010

@author: Peterko
'''
from BaseView import CBaseView


class CElementView(CBaseView):
    '''
    classdocs
    '''


    def __init__(self, element, parentDiagram, position = None, size = None):
        '''
        Constructor
        '''
        super(CElementView, self).__init__(element, parentDiagram)
        self.__element = element
        #self.__position = position
        #self.__size = size
        
            
        
        self.viewData = {}
        self.SetPosition(position)
        self.SetSize(size)
        
    def GetPosition(self):
        return self.viewData['position']
    
    def SetPosition(self, position):
        if type(position) == type({}):
            position = (position['x'], position['y'])
        self.viewData['position'] = {'x':position[0], 'y':position[1]}
    
    def GetSize(self):
        return self.viewData['size']
    
    def SetSize(self, size):
        if type(size) == type({}):
            size = (size['dw'], size['dh'])
        self.viewData['size'] = {'dw':size[0], 'dh': size[1]}
    
    def GetSizeRelative(self):
        return self.viewData['size']
    
    def ModifyData(self, oldState, newState, path):
        print 'modifying element view'
        
        self.viewData[path[0]].update(newState)
        print self.viewData