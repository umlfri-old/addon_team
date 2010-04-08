'''
Created on 6.3.2010

@author: Peterko
'''
from Base import CBase

class CElement(CBase):
    '''
    classdocs
    '''


    def __init__(self, id, type):
        '''
        Constructor
        '''
        super(CElement, self).__init__(id, type)
        
    def ModifyData(self, oldState, newState, path):
        print 'modifying element data'
        
        r = self.data
        for item in path[0:len(path)-1]:
            r = r[item]
        
        if oldState is None:
            # pridanie
            print 'inserting'
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
            print 'deleting'
            r.pop(path[len(path)-1])
        else:
            print 'updating'
            r.update(newState)
            