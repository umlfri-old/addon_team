'''
Created on 24.3.2010

@author: Peterko
'''

class CDictDiffer(object):
    '''
    classdocs
    '''


    def __init__(self, dict1, dict2):
        '''
        Constructor
        '''
        self.__dict1, self.__dict2 = dict1, dict2
        self.__setDict1, self.__setDict2 = set(dict1.keys()), set(dict2.keys())
        self.__intersect = self.__setDict1.intersection(self.__setDict2)
    
    
    def added(self):
        return list(self.__setDict1 - self.__intersect)
    
    
    def removed(self):
        return list(self.__setDict2 - self.__intersect)
    
    def changed(self):
        return [o for o in self.__intersect if self.__dict2[o] != self.dict1[o]]
    
    def unchanged(self):
        return [o for o in self.__intersect if self.__dict1[o] == self.__dict2[o]]