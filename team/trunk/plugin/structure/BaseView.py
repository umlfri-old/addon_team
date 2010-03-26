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
        self.viewData = {}
        
    def GetObject(self):
        return self.__objectRepresentation
        
    def GetViewData(self):
        return self.viewData
    
    def __str__(self):
        return self.__objectRepresentation.GetId()