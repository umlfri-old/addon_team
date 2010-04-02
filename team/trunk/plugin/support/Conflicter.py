'''
Created on 2.4.2010

@author: Peterko
'''
from Differ import CDiffer
from DiffActions import EDiffActions
import itertools
from structure import CProjectTreeNode

class CConflicter(object):
    '''
    classdocs
    '''


    def __init__(self, newProject, oldProject, workProject):
        '''
        Constructor
        '''
        self.__new = newProject
        self.__old = oldProject
        self.__work= workProject
        
        self.__oldNewDiffer = CDiffer(self.__old, self.__new)
        self.__oldWorkDiffer = CDiffer(self.__old, self.__work)
        
        self.__TryConflictSolve()
        
    def __TryConflictSolve(self):
        # pokus sa zakomponovat zmeny z new do worku
        # ak to nepojde vyhlas to za konflikt a ponukni pouzivatelovi riesenie
        
        # najskor projektovy strom
        
        
        for diff in self.__oldNewDiffer.projectTreeDiff:
            print diff
        
        # potom vizualny diff
        
        for diff in self.__oldNewDiffer.visualDiff:
            print diff
            
        
        # nakoniec diff datovych zloziek
        for diff in self.__oldNewDiffer.dataDiff:
            print diff
        
    
        
       
    
    
    
    def __str__(self):
        return 'new: '+str(self.__new.GetProjectTreeRoot()) \
            + 'old: '+str(self.__old.GetProjectTreeRoot()) \
            + 'work: '+str(self.__work.GetProjectTreeRoot())