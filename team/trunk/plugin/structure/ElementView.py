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
        self.__position = position
        self.__size = size
        self.viewData = {
                'position':{'x':self.__position[0],'y':self.__position[1]},
                'size':{'dw':self.__size[0], 'dh': self.__size[1]}
                }
        
    def GetPosition(self):
        return self.__position
    
    def GetSize(self):
        return self.__size
    
    