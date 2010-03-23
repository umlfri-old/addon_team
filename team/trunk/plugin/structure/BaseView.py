'''
Created on 15.3.2010

@author: Peterko
'''

class CBaseView(object):
    '''
    classdocs
    '''


    def __init__(self, objectRepresentation):
        '''
        Constructor
        '''
        self.__objectRepresentation = objectRepresentation
        
    def GetObject(self):
        return self.__objectRepresentation
    
    def __str__(self):
        return self.__objectRepresentation.GetId()