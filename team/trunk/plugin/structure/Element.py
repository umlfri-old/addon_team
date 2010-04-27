'''
Created on 6.3.2010

@author: Peterko
'''
from Base import CBase

class CElement(CBase):
    '''
    Class representing data object of element
    '''


    def __init__(self, id, type):
        '''
        Constructor
        @type id: string
        @param id: identification of object
        @type type: string
        @param type: Type of object
        '''
        super(CElement, self).__init__(id, type)
        
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
        
        r = self.data
        for item in path[0:len(path)-1]:
            r = r[item]
        
        if oldState is None:
            # pridanie
            
            if type(r) == type([]):
                if type(newState) == type([]):
                    r.extend(newState)
                else:
                    r.append(newState)
            elif type(r) == type({}):
                if type(newState) == type([]):
                    r[path[len(path)-1]].extend(newState)
                else:
                    r[path[len(path)-1]].append(newState)
                
            
        elif newState is None:
            # odobratie
            
            r[path[len(path)-1]].remove(oldState)
        else:
            
            r.update(newState)
            
    def __str__(self):
        return "Element "+self.GetName()