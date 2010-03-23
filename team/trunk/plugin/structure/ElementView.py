'''
Created on 13.3.2010

@author: Peterko
'''
from BaseView import CBaseView


class CElementView(CBaseView):
    '''
    classdocs
    '''


    def __init__(self, element, position = None, size = None):
        '''
        Constructor
        '''
        super(CElementView, self).__init__(element)
        self.__element = element
        self.__position = position
        self.__size = size
        
    def GetPosition(self):
        return self.__position
    
    def GetSize(self):
        return self.__size
    