'''
Created on 6.4.2010

@author: Peterko
'''
from Conflicter import CConflicter
from structure import *
from DiffActions import EDiffActions
from Merger import CMerger





class CUpdater(object):
    '''
    classdocs
    '''


    def __init__(self, mine, base, upd):
        '''
        Constructor
        '''
        
        self.__baseProject = CProject(None, base)
        self.__updProject  = CProject(None, upd)
        self.__mineProject = CProject(None, mine)
        
        self.__newXml = None
        self.__isInConflict = False
        self.__conflicter = None
        self.__merger = None
        
        
        self.__TryUpdate()
        
        
        
        
        
    def GetNewXml(self):
        self.__newXml = self.__baseProject.GetSaveXml()
        return self.__newXml
    
    def IsInConflict(self):
        return self.__isInConflict
    
    def GetConflicter(self):
        return self.__conflicter
    
    def GetMerger(self):
        return self.__merger
        
    def __TryUpdate(self):
        
        
        self.__conflicter = CConflicter(self.__updProject, self.__baseProject, self.__mineProject)
        if len(self.__conflicter.GetConflicting()) == 0:
            # ok nechaj vsetko tak
            print 'no conflicts'
        else:
            self.__isInConflict = True
            
        self.__merger = CMerger(self.__baseProject)
        self.__merger.MergeDiffs(self.__conflicter.merging)
            
        
        self.__baseProject.UpdateCounters(self.__mineProject.GetCounters())
        
        self.__baseProject.UpdateCounters(self.__updProject.GetCounters())
        
        
        
    
        