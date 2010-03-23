'''
Created on 27.2.2010

@author: Peterko
'''
from difflib import *

class CDiffer(object):
    '''
    classdocs
    '''


    def __init__(self, project1, project2):
        '''
        Constructor
        '''
        self.__project1 = project1
        self.__project2 = project2
        
    def diffProjects(self):
        sm = SequenceMatcher(None, self.__project1.GetElements().values(), self.__project2.GetElements().values())
        print sm.get_opcodes()
        sm = SequenceMatcher(None, self.__project1.GetDiagrams().values(), self.__project2.GetDiagrams().values())
        print sm.get_opcodes()
        sm = SequenceMatcher(None, self.__project1.GetConnections().values(), self.__project2.GetConnections().values())
        print sm.get_opcodes()

    
        